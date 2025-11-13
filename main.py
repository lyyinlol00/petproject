from models import Owner, Pet, Breed, PetHouse, Address
from registry import PetRegistry
from storage import save_to_json, load_from_json, save_to_xml, load_from_xml
from exceptions import OwnerNotFoundError, PetNotFoundError, InvalidDataError, FileProcessingError, EmptyInputError, InvalidFileFormatError, InvalidNumberError

def main():
    registry = PetRegistry()

    print("=== Добро пожаловать в систему домашних животных ===")

    while True:
        print("\nВыберите действие:")
        print("1. Добавить владельца")
        print("2. Добавить питомца")
        print("3. Показать всех владельцев")
        print("4. Показать всех питомцев")
        print("5. Сохранить в JSON")
        print("6. Загрузить из JSON")
        print("7. Сохранить в XML")
        print("8. Загрузить из XML")
        print("9. Обновить информацию о владельце")
        print("10. Обновить информацию о питомце")
        print("11. Удалить владельца")
        print("12. Удалить питомца")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        try:
            if choice == "1":
                owner_id_input = input("ID владельца: ")
                if not owner_id_input:
                    raise EmptyInputError("ID владельца не может быть пустым.")
                try:
                    owner_id = int(owner_id_input)
                except ValueError:
                    raise InvalidNumberError("Ошибка: нужно ввести цифры для ID владельца.")
                name = input("Имя владельца: ")
                phone = input("Телефон владельца: ")
                address_street = input("Улица: ")
                address_city = input("Город: ")
                address_postal_code = input("Почтовый индекс: ")
                address = Address(address_street, address_city, address_postal_code)
                owner = Owner(owner_id, name, phone, address)
                registry.add_owner(owner)
                print(f"Владелец {name} добавлен.")

            elif choice == "2":
                if not registry.owners:
                    print("Сначала добавьте хотя бы одного владельца.")
                    continue
                name = input("Имя питомца: ")
                age_input = input("Возраст питомца: ")
                if not age_input:
                    raise EmptyInputError("Возраст питомца не может быть пустым.")
                try:
                    age = int(age_input)
                except ValueError:
                    raise InvalidNumberError("Ошибка: нужно ввести цифры для возраста питомца.")
                breed_name = input("Порода питомца: ")
                species = input("Вид (Собака/Кошка и т.д.): ")
                house_type = input("Тип дома питомца: ")
                house_size = input("Размер дома питомца: ")
                owner_id_input = input("ID владельца питомца: ")
                if not owner_id_input:
                    raise EmptyInputError("ID владельца питомца не может быть пустым.")
                try:
                    owner_id = int(owner_id_input)
                except ValueError:
                    raise InvalidNumberError("Ошибка: нужно ввести цифры для ID владельца питомца.")

                owner = registry.get_owner(owner_id)
                breed = Breed(breed_name, species)
                house = PetHouse(house_type, house_size)
                pet = Pet(name, age, breed, house, owner)
                registry.add_pet(pet)
                print(f"Питомец {name} добавлен и привязан к владельцу {owner.name}.")

            elif choice == "3":
                if not registry.owners:
                    print("Владельцев пока нет.")
                for o in registry.owners:
                    print(f"ID: {o.owner_id}, Имя: {o.name}, Телефон: {o.phone}, Адрес: {o.address.street}, {o.address.city}, {o.address.postal_code}")


            elif choice == "4":
                if not registry.pets:
                    print("Питомцев пока нет.")
                for p in registry.pets:
                    print(f"Имя: {p.name}, Возраст: {p.age}, Владелец: {p.owner.name}, Порода: {p.breed.name} ({p.breed.species}), Дом: {p.house.house_type}, Размер дома: {p.house.house_size}")


            elif choice == "5":
                filename = input("Имя файла для сохранения JSON: ")
                save_to_json(registry, filename)
                print("Данные сохранены в JSON.")

            elif choice == "6":
                filename = input("Имя файла для загрузки JSON: ")
                owners_before = len(registry.owners)
                pets_before = len(registry.pets)
                load_from_json(registry, filename)
                owners_loaded = len(registry.owners) - owners_before
                pets_loaded = len(registry.pets) - pets_before
                print(f"Данные загружены из JSON.")
                print(f"Загружено владельцев: {owners_loaded}, питомцев: {pets_loaded}")
                print(f"Всего в системе: владельцев - {len(registry.owners)}, питомцев - {len(registry.pets)}")

            elif choice == "7":
                filename = input("Имя файла для сохранения XML: ")
                save_to_xml(registry, filename)
                print("Данные сохранены в XML.")

            elif choice == "8":
                filename = input("Имя файла для загрузки XML: ")
                owners_before = len(registry.owners)
                pets_before = len(registry.pets)
                load_from_xml(registry, filename)
                owners_loaded = len(registry.owners) - owners_before
                pets_loaded = len(registry.pets) - pets_before
                print(f"Данные загружены из XML.")
                print(f"Загружено владельцев: {owners_loaded}, питомцев: {pets_loaded}")
                print(f"Всего в системе: владельцев - {len(registry.owners)}, питомцев - {len(registry.pets)}")

            elif choice == "9":
                owner_id_input = input("ID владельца для обновления: ")
                if not owner_id_input:
                    raise EmptyInputError("ID владельца не может быть пустым.")
                try:
                    owner_id = int(owner_id_input)
                except ValueError:
                    raise InvalidNumberError("Ошибка: нужно ввести цифры для ID владельца.")
                new_name = input("Новое имя владельца (оставьте пустым для сохранения старого): ")
                new_phone = input("Новый телефон владельца (оставьте пустым для сохранения старого): ")
                new_address = input("Новый адрес владельца (оставьте пустым для сохранения старого): ")
                address = None
                if new_address:
                    street = input("Улица: ")
                    city = input("Город: ")
                    postal_code = input("Почтовый индекс: ")
                    address = Address(street, city, postal_code)
                registry.update_owner(owner_id, new_name if new_name else None, new_phone if new_phone else None, address)
                print("Информация о владельце обновлена.")

            elif choice == "10":
                pet_name = input("Имя питомца для обновления: ")
                new_name = input("Новое имя питомца (оставьте пустым для сохранения старого): ")
                new_age = input("Новый возраст питомца (оставьте пустым для сохранения старого): ")
                new_breed_name = input("Новая порода питомца (оставьте пустым для сохранения старой): ")
                new_breed_species = input("Новый вид питомца (оставьте пустым для сохранения старого): ")
                new_house_type = input("Новый тип дома питомца (оставьте пустым для сохранения старого): ")
                new_house_size = input("Новый размер дома питомца (оставьте пустым для сохранения старого): ")

                breed = None
                if new_breed_name and new_breed_species:
                    breed = Breed(new_breed_name, new_breed_species)
                house = None
                if new_house_type and new_house_size:
                    house = PetHouse(new_house_type, new_house_size)
                new_age_int = None
                if new_age:
                    try:
                        new_age_int = int(new_age)
                    except ValueError:
                        raise InvalidNumberError("Ошибка: нужно ввести цифры для возраста питомца.")
                registry.update_pet(pet_name, new_name if new_name else None, new_age_int, breed, house)
                print(f"Информация о питомце {pet_name} обновлена.")

            elif choice == "11":
                owner_id_input = input("ID владельца для удаления: ")
                if not owner_id_input:
                    raise EmptyInputError("ID владельца не может быть пустым.")
                try:
                    owner_id = int(owner_id_input)
                except ValueError:
                    raise InvalidNumberError("Ошибка: нужно ввести цифры для ID владельца.")
                owner = registry.get_owner(owner_id)
                registry.delete_owner(owner_id)
                print(f"Владелец {owner.name} и все его питомцы удалены.")

            elif choice == "12":
                pet_name = input("Имя питомца для удаления: ")
                if not pet_name:
                    raise EmptyInputError("Имя питомца не может быть пустым.")
                registry.delete_pet(pet_name)
                print(f"Питомец {pet_name} удален.")

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор, попробуйте снова.")

        except (OwnerNotFoundError, PetNotFoundError, InvalidDataError, FileProcessingError, EmptyInputError, InvalidFileFormatError, InvalidNumberError) as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
