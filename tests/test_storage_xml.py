# tests/test_storage_xml.py
import pytest
import os
import xml.etree.ElementTree as ET
from models import Owner, Pet, Breed, PetHouse, Address
from registry import PetRegistry
from storage import save_to_xml, load_from_xml

# Фикстура для создания реестра питомцев
@pytest.fixture
def pet_registry():
    return PetRegistry()

# Тест для сохранения в XML
def test_save_to_xml(pet_registry):
    # Создаем владельца
    address = Address("123 Main St", "New York", "10001")
    owner = Owner(owner_id=1, name="John Doe", phone="123-456-7890", address=address)
    pet_registry.add_owner(owner)
    
    # Создаем питомца
    breed = Breed(name="Bulldog", species="Dog")
    house = PetHouse(house_type="Apartment", house_size="Medium")
    pet = Pet(name="Max", age=5, breed=breed, house=house, owner=owner)
    pet_registry.add_pet(pet)
    
    # Сохраняем данные в XML
    filename = "test_pets.xml"
    save_to_xml(pet_registry, filename)
    
    # Проверяем, что файл создан
    assert os.path.exists(filename)
    
    # Проверяем содержимое файла
    tree = ET.parse(filename)
    root = tree.getroot()
    assert root.tag == "PetRegistry"
    owners = root.findall("Owner")
    pets = root.findall("Pet")
    assert len(owners) == 1
    assert len(pets) == 1
    assert owners[0].get("name") == "John Doe"
    assert pets[0].get("name") == "Max"
    
    # Удаляем тестовый файл
    os.remove(filename)

# Тест для загрузки из XML
def test_load_from_xml(pet_registry):
    # Создаем тестовый XML файл
    filename = "test_load.xml"
    xml_content = """<?xml version='1.0' encoding='utf-8'?>
<PetRegistry>
  <Owner id="1" name="John Doe" phone="123-456-7890">
    <Address street="123 Main St" city="New York" postal_code="10001" />
  </Owner>
  <Pet name="Max" age="5">
    <Breed name="Bulldog" species="Dog" />
    <House house_type="Apartment" house_size="Medium" />
    <OwnerID>1</OwnerID>
  </Pet>
</PetRegistry>"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    # Загружаем данные
    load_from_xml(pet_registry, filename)
    
    # Проверяем, что данные загружены
    assert len(pet_registry.owners) == 1
    assert len(pet_registry.pets) == 1
    assert pet_registry.get_owner(1).name == "John Doe"
    assert pet_registry.get_pet("Max").age == 5
    
    # Удаляем тестовый файл
    os.remove(filename)
