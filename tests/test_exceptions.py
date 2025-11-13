# tests/test_exceptions.py
import pytest
from exceptions import PetNotFoundError, OwnerNotFoundError
from registry import PetRegistry
from models import Pet, Breed, PetHouse, Owner, Address

@pytest.fixture
def pet_registry():
    return PetRegistry()

def test_pet_not_found():
    registry = PetRegistry()
    with pytest.raises(PetNotFoundError):
        registry.get_pet("NonExistentPet")

def test_owner_not_found():
    registry = PetRegistry()
    address = Address("Улица Ленина", "Москва", "123456")
    owner = Owner(1, "Анна", "12345", address)
    pet = Pet("Бобик", 3, Breed("Корги", "Собака"), PetHouse("Квартира", "Средний"), owner)
    with pytest.raises(OwnerNotFoundError):
        registry.add_pet(pet)

def test_owner_not_found_by_id():
    registry = PetRegistry()
    with pytest.raises(OwnerNotFoundError):
        registry.get_owner(999)
