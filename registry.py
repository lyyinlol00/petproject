from typing import List, Optional
from models import Pet, Owner, Address, Breed, PetHouse
from exceptions import PetNotFoundError  
from exceptions import OwnerNotFoundError

class PetRegistry:
    def __init__(self) -> None:
        self.pets: List[Pet] = []
        self.owners: List[Owner] = []
        
        
    def get_owner(self, owner_id: int) -> Owner:
        for owner in self.owners:
            if owner.owner_id == owner_id:
                return owner
        raise OwnerNotFoundError(f"Владелец с ID {owner_id} не найден.")
    
    def add_owner(self, owner: Owner) -> None:
        self.owners.append(owner)

    def add_pet(self, pet: Pet) -> None:
        if pet.owner not in self.owners:
            raise OwnerNotFoundError(f"Владелец {pet.owner.name} не зарегистрирован.")
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Pet:
        pet = next((pet for pet in self.pets if pet.name == pet_name), None)
        if not pet:
            raise PetNotFoundError(f"Питомец с именем {pet_name} не найден.")
        return pet

    def update_owner(self, owner_id: int, new_name: Optional[str] = None, new_phone: Optional[str] = None, new_address: Optional[Address] = None) -> None:
        owner = self.get_owner(owner_id)
        if new_name:
            owner.name = new_name
        if new_phone:
            owner.phone = new_phone
        if new_address:
            owner.address = new_address

    def update_pet(self, pet_name: str, new_name: Optional[str] = None, new_age: Optional[int] = None, new_breed: Optional[Breed] = None, new_house: Optional[PetHouse] = None) -> None:
        pet = self.get_pet(pet_name)
        if new_name:
            pet.name = new_name
        if new_age is not None:
            pet.age = new_age
        if new_breed:
            pet.breed = new_breed
        if new_house:
            pet.house = new_house
        
    def update_pet_age(self, pet_name: str, new_age: int) -> None:
        pet = next((pet for pet in self.pets if pet.name == pet_name), None)
        if pet is None:
            raise PetNotFoundError(f"Питомец с именем {pet_name} не найден.")
        pet.age = new_age
    
    def delete_owner(self, owner_id: int) -> None:
        """Удаляет владельца по ID. Также удаляет всех его питомцев."""
        owner = self.get_owner(owner_id)
        # Удаляем всех питомцев этого владельца
        self.pets = [pet for pet in self.pets if pet.owner.owner_id != owner_id]
        # Удаляем владельца
        self.owners.remove(owner)
    
    def delete_pet(self, pet_name: str) -> None:
        """Удаляет питомца по имени."""
        pet = self.get_pet(pet_name)
        self.pets.remove(pet)

