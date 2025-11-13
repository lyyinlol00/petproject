# tests/test_storage_json.py
import pytest
import os
import json
from models import Owner, Pet, Breed, PetHouse, Address
from registry import PetRegistry
from storage import save_to_json, load_from_json

# Фикстура для создания реестра питомцев
@pytest.fixture
def pet_registry():
    return PetRegistry()

# Тест для сохранения в JSON
def test_save_to_json(pet_registry):
    # Создаем владельца
    address = Address("123 Main St", "New York", "10001")
    owner = Owner(owner_id=1, name="John Doe", phone="123-456-7890", address=address)
    pet_registry.add_owner(owner)
    
    # Создаем питомца
    breed = Breed(name="Bulldog", species="Dog")
    house = PetHouse(house_type="Apartment", house_size="Medium")
    pet = Pet(name="Max", age=5, breed=breed, house=house, owner=owner)
    pet_registry.add_pet(pet)
    
    # Сохраняем данные в JSON
    filename = "test_pets.json"
    save_to_json(pet_registry, filename)
    
    # Проверяем, что файл создан
    assert os.path.exists(filename)
    
    # Проверяем содержимое файла
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert 'owners' in data
        assert 'pets' in data
        assert len(data['owners']) == 1
        assert len(data['pets']) == 1
        assert data['owners'][0]['name'] == "John Doe"
        assert data['pets'][0]['name'] == "Max"
    
    # Удаляем тестовый файл
    os.remove(filename)

# Тест для загрузки из JSON
def test_load_from_json(pet_registry):
    # Создаем тестовый JSON файл
    test_data = {
        "owners": [
            {
                "owner_id": 1,
                "name": "John Doe",
                "phone": "123-456-7890",
                "address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "postal_code": "10001"
                }
            }
        ],
        "pets": [
            {
                "name": "Max",
                "age": 5,
                "breed": {
                    "name": "Bulldog",
                    "species": "Dog"
                },
                "house": {
                    "house_type": "Apartment",
                    "house_size": "Medium"
                },
                "owner_id": 1
            }
        ]
    }
    
    filename = "test_load.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    
    # Загружаем данные
    load_from_json(pet_registry, filename)
    
    # Проверяем, что данные загружены
    assert len(pet_registry.owners) == 1
    assert len(pet_registry.pets) == 1
    assert pet_registry.get_owner(1).name == "John Doe"
    assert pet_registry.get_pet("Max").age == 5
    
    # Удаляем тестовый файл
    os.remove(filename)
