# tests/test_registry.py
import pytest
from models import Owner, Pet, Breed, PetHouse, Address
from registry import PetRegistry
from exceptions import PetNotFoundError

# Фикстура для создания реестра питомцев
@pytest.fixture
def pet_registry():
    return PetRegistry()

# Фикстура для создания владельца
@pytest.fixture
def owner():
    address = Address("123 Main St", "New York", "10001")
    return Owner(owner_id=1, name="John Doe", phone="123-456-7890", address=address)

# Тест для добавления владельца
def test_add_owner(pet_registry, owner):
    pet_registry.add_owner(owner)
    assert len(pet_registry.owners) == 1
    assert pet_registry.get_owner(1) == owner

# Тест для добавления питомца
def test_add_pet(pet_registry, owner):
    pet_registry.add_owner(owner)
    breed = Breed(name="Bulldog", species="Dog")
    house = PetHouse(house_type="Apartment", house_size="Medium")
    pet = Pet(name="Max", age=5, breed=breed, house=house, owner=owner)
    pet_registry.add_pet(pet)
    assert len(pet_registry.pets) == 1
    assert pet_registry.get_pet("Max") == pet

# Тест для обновления имени питомца
def test_update_pet_name(pet_registry, owner):
    pet_registry.add_owner(owner)
    breed = Breed(name="Bulldog", species="Dog")
    house = PetHouse(house_type="Apartment", house_size="Medium")
    pet = Pet(name="Max", age=5, breed=breed, house=house, owner=owner)
    pet_registry.add_pet(pet)
    
    new_name = "Buddy"
    pet_registry.update_pet("Max", new_name=new_name)
    assert pet.name == new_name

# Тест для обновления возраста питомца
def test_update_pet_age(pet_registry, owner):
    pet_registry.add_owner(owner)
    breed = Breed(name="Bulldog", species="Dog")
    house = PetHouse(house_type="Apartment", house_size="Medium")
    pet = Pet(name="Max", age=5, breed=breed, house=house, owner=owner)
    pet_registry.add_pet(pet)
    
    new_age = 6
    pet_registry.update_pet_age("Max", new_age)
    assert pet.age == new_age

# Тест для обновления владельца
def test_update_owner(pet_registry, owner):
    pet_registry.add_owner(owner)
    new_name = "Jane Doe"
    new_phone = "987-654-3210"
    pet_registry.update_owner(1, new_name=new_name, new_phone=new_phone)
    assert owner.name == new_name
    assert owner.phone == new_phone

# Тест для удаления питомца
def test_delete_pet(pet_registry, owner):
    pet_registry.add_owner(owner)
    breed = Breed(name="Bulldog", species="Dog")
    house = PetHouse(house_type="Apartment", house_size="Medium")
    pet = Pet(name="Max", age=5, breed=breed, house=house, owner=owner)
    pet_registry.add_pet(pet)
    
    pet_registry.delete_pet("Max")
    assert len(pet_registry.pets) == 0
    with pytest.raises(PetNotFoundError):
        pet_registry.get_pet("Max")

# Тест для удаления владельца
def test_delete_owner(pet_registry, owner):
    pet_registry.add_owner(owner)
    breed = Breed(name="Bulldog", species="Dog")
    house = PetHouse(house_type="Apartment", house_size="Medium")
    pet = Pet(name="Max", age=5, breed=breed, house=house, owner=owner)
    pet_registry.add_pet(pet)
    
    pet_registry.delete_owner(1)
    assert len(pet_registry.owners) == 0
    assert len(pet_registry.pets) == 0  # Питомцы тоже должны удалиться

