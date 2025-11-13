import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from typing import TYPE_CHECKING
from models import Owner, Pet, Address, Breed, PetHouse
from exceptions import FileProcessingError, OwnerNotFoundError, PetNotFoundError, InvalidFileFormatError

if TYPE_CHECKING:
    from registry import PetRegistry

def save_to_json(registry: 'PetRegistry', filename: str) -> None:
    data = {
        "owners": [
            {
                "owner_id": owner.owner_id,
                "name": owner.name,
                "phone": owner.phone,
                "address": {
                    "street": owner.address.street,
                    "city": owner.address.city,
                    "postal_code": owner.address.postal_code
                }
            } for owner in registry.owners
        ],
        "pets": [
            {
                "name": pet.name,
                "age": pet.age,
                "breed": {
                    "name": pet.breed.name,
                    "species": pet.breed.species
                },
                "house": {
                    "house_type": pet.house.house_type,  # изменили 'type' на 'house_type'
                    "house_size": pet.house.house_size   # изменили 'size' на 'house_size'
                },
                "owner_id": pet.owner.owner_id
            } for pet in registry.pets
        ]
    }

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise FileProcessingError(f"Ошибка при сохранении в JSON: {e}")


def load_from_json(registry: 'PetRegistry', filename: str) -> None:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise InvalidFileFormatError(f"Файл '{filename}' не является корректным JSON файлом. Ошибка: {e}")

        # Загружаем владельцев (проверяем на дубликаты по ID)
        for owner_data in data.get('owners', []):
            try:
                owner_id = int(owner_data['owner_id'])
            except (ValueError, TypeError, KeyError):
                raise InvalidFileFormatError(f"Неверный формат ID владельца в JSON файле: '{owner_data.get('owner_id')}'. Нужно ввести цифры.")
            # Проверяем, не существует ли уже владелец с таким ID
            try:
                existing_owner = registry.get_owner(owner_id)
                # Если владелец существует, пропускаем его
                continue
            except OwnerNotFoundError:
                # Владелец не найден, создаем нового
                address_data = owner_data['address']
                address = Address(address_data['street'], address_data['city'], address_data['postal_code'])
                owner = Owner(owner_id, owner_data['name'], owner_data['phone'], address)
                registry.add_owner(owner)

        # Загружаем питомцев (проверяем на дубликаты по имени)
        for pet_data in data.get('pets', []):
            pet_name = pet_data['name']
            # Проверяем, не существует ли уже питомец с таким именем
            try:
                existing_pet = registry.get_pet(pet_name)
                # Если питомец существует, пропускаем его
                continue
            except PetNotFoundError:
                # Питомец не найден, создаем нового
                try:
                    age = int(pet_data['age'])
                except (ValueError, TypeError, KeyError):
                    raise InvalidFileFormatError(f"Неверный формат возраста питомца в JSON файле: '{pet_data.get('age')}'. Нужно ввести цифры.")
                try:
                    owner_id = int(pet_data['owner_id'])
                except (ValueError, TypeError, KeyError):
                    raise InvalidFileFormatError(f"Неверный формат ID владельца питомца в JSON файле: '{pet_data.get('owner_id')}'. Нужно ввести цифры.")
                breed_data = pet_data['breed']
                breed = Breed(breed_data['name'], breed_data['species'])
                house_data = pet_data['house']
                house = PetHouse(house_data['house_type'], house_data['house_size'])
                owner = registry.get_owner(owner_id)
                pet = Pet(pet_name, age, breed, house, owner)
                registry.add_pet(pet)

    except Exception as e:
        raise FileProcessingError(f"Ошибка при загрузке из JSON: {e}")



def indent(elem, level=0):
    """Правильно форматирует XML с отступами"""
    indent_str = "\n" + level * "  "
    child_indent = "\n" + (level + 1) * "  "
    
    if elem is not None:
        # Если есть дочерние элементы
        if len(elem):
            # Устанавливаем отступ для содержимого элемента
            if not elem.text or not elem.text.strip():
                elem.text = child_indent
            
            # Обрабатываем каждый дочерний элемент
            for child in elem:
                indent(child, level + 1)
                # Устанавливаем tail для каждого дочернего элемента
                if child.tail is None or not child.tail.strip():
                    child.tail = child_indent
            
            # Последний дочерний элемент должен иметь tail на уровень выше
            if len(elem) > 0:
                elem[-1].tail = indent_str
        
        # Устанавливаем tail для самого элемента
        if level > 0:
            if elem.tail is None or not elem.tail.strip():
                elem.tail = indent_str

# Основная функция для сохранения в XML с отступами
def save_to_xml(registry: 'PetRegistry', filename: str) -> None:
    root = ET.Element("PetRegistry")

    # Сохраняем владельцев
    for owner in registry.owners:
        owner_elem = ET.SubElement(root, "Owner")
        owner_elem.set("id", str(owner.owner_id))
        owner_elem.set("name", owner.name)
        owner_elem.set("phone", owner.phone)
        address_elem = ET.SubElement(owner_elem, "Address")
        address_elem.set("street", owner.address.street)
        address_elem.set("city", owner.address.city)
        address_elem.set("postal_code", owner.address.postal_code)

    # Сохраняем питомцев
    for pet in registry.pets:
        pet_elem = ET.SubElement(root, "Pet")
        pet_elem.set("name", pet.name)
        pet_elem.set("age", str(pet.age))
        breed_elem = ET.SubElement(pet_elem, "Breed")
        breed_elem.set("name", pet.breed.name)
        breed_elem.set("species", pet.breed.species)
        house_elem = ET.SubElement(pet_elem, "House")
        house_elem.set("house_type", pet.house.house_type)
        house_elem.set("house_size", pet.house.house_size)
        owner_id_elem = ET.SubElement(pet_elem, "OwnerID")
        owner_id_elem.text = str(pet.owner.owner_id)

    try:
        # Создаем дерево
        tree = ET.ElementTree(root)
        
        # Используем minidom для красивого форматирования
        rough_string = ET.tostring(root, encoding='utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
        
        # Удаляем лишние пустые строки и сохраняем
        lines = [line for line in pretty_xml.decode('utf-8').split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)

    except Exception as e:
        raise FileProcessingError(f"Ошибка при сохранении в XML: {e}")


def load_from_xml(registry: 'PetRegistry', filename: str) -> None:
    try:
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
        except ET.ParseError as e:
            raise InvalidFileFormatError(f"Файл '{filename}' не является корректным XML файлом. Ошибка: {e}")

        # Загружаем владельцев (проверяем на дубликаты по ID)
        for owner_elem in root.findall("Owner"):
            try:
                owner_id = int(owner_elem.get("id"))
            except (ValueError, TypeError):
                raise InvalidFileFormatError(f"Неверный формат ID владельца в XML файле: '{owner_elem.get('id')}'. Нужно ввести цифры.")
            # Проверяем, не существует ли уже владелец с таким ID
            try:
                existing_owner = registry.get_owner(owner_id)
                # Если владелец существует, пропускаем его
                continue
            except OwnerNotFoundError:
                # Владелец не найден, создаем нового
                name = owner_elem.get("name")
                phone = owner_elem.get("phone")
                address_elem = owner_elem.find("Address")
                street = address_elem.get("street")
                city = address_elem.get("city")
                postal_code = address_elem.get("postal_code")
                address = Address(street, city, postal_code)
                owner = Owner(owner_id, name, phone, address)
                registry.add_owner(owner)

        # Загружаем питомцев (проверяем на дубликаты по имени)
        for pet_elem in root.findall("Pet"):
            name = pet_elem.get("name")
            # Проверяем, не существует ли уже питомец с таким именем
            try:
                existing_pet = registry.get_pet(name)
                # Если питомец существует, пропускаем его
                continue
            except PetNotFoundError:
                # Питомец не найден, создаем нового
                try:
                    age = int(pet_elem.get("age"))
                except (ValueError, TypeError):
                    raise InvalidFileFormatError(f"Неверный формат возраста питомца в XML файле: '{pet_elem.get('age')}'. Нужно ввести цифры.")
                breed_elem = pet_elem.find("Breed")
                breed_name = breed_elem.get("name")
                breed_species = breed_elem.get("species")
                breed = Breed(breed_name, breed_species)
                house_elem = pet_elem.find("House")
                house_type = house_elem.get("house_type")
                house_size = house_elem.get("house_size")
                house = PetHouse(house_type, house_size)
                try:
                    owner_id = int(pet_elem.find("OwnerID").text)
                except (ValueError, TypeError, AttributeError):
                    raise InvalidFileFormatError(f"Неверный формат ID владельца питомца в XML файле. Нужно ввести цифры.")
                owner = registry.get_owner(owner_id)
                pet = Pet(name, age, breed, house, owner)
                registry.add_pet(pet)

    except Exception as e:
        raise FileProcessingError(f"Ошибка при загрузке из XML: {e}")

