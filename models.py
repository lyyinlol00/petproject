from typing import Optional
from datetime import datetime

class Address:
    def __init__(self, street: str, city: str, postal_code: str):
        self.street = street
        self.city = city
        self.postal_code = postal_code

# Класс для владельца питомца
class Owner:
    def __init__(self, owner_id: int, name: str, phone: str, address: Address):
        self.owner_id: int = owner_id
        self.name: str = name
        self.phone: str = phone
        self.address: Address = address

# Класс для породы питомца
class Breed:
    def __init__(self, name: str, species: str):
        self.name: str = name
        self.species: str = species

# Класс для дома питомца
class PetHouse:
    def __init__(self, house_type: str, house_size: str):
        self.house_type: str = house_type
        self.house_size: str = house_size

# Класс для питомца
class Pet:
    def __init__(self, name: str, age: int, breed: Breed, house: PetHouse, owner: Owner):
        self.name: str = name
        self.age: int = age
        self.breed: Breed = breed
        self.house: PetHouse = house
        self.owner: Owner = owner

# Класс для типа события (например, ухода или кормления питомца)
class PetEvent:
    def __init__(self, pet: Pet, event_type: str, date: str):
        self.pet: Pet = pet
        self.event_type: str = event_type
        self.date: str = date  # Здесь можно использовать datetime для более точного представления даты

# Класс для категории питомца (например, терапевтический питомец, спортивный питомец)
class PetCategory:
    def __init__(self, category_name: str):
        self.category_name: str = category_name

# Класс для ветеринара
class Veterinarian:
    def __init__(self, vet_id: int, name: str, phone: str):
        self.vet_id: int = vet_id
        self.name: str = name
        self.phone: str = phone

# Класс для визита питомца к ветеринару
class VetVisit:
    def __init__(self, pet: Pet, veterinarian: Veterinarian, date: str, reason: str):
        self.pet: Pet = pet
        self.veterinarian: Veterinarian = veterinarian
        self.date: str = date  # Опять же, можно использовать datetime
        self.reason: str = reason

# Класс для записи на услуги (например, стрижка, вакцинация)
class PetService:
    def __init__(self, service_name: str, price: float):
        self.service_name: str = service_name
        self.price: float = price

# Класс для записи на услугу питомцу
class PetServiceBooking:
    def __init__(self, pet: Pet, service: PetService, date: str):
        self.pet: Pet = pet
        self.service: PetService = service
        self.date: str = date  # Здесь тоже можно заменить на datetime для точности

# Класс для рецепта, выданного ветеринаром
class Prescription:
    def __init__(self, pet: Pet, medication: str, dosage: str, date: str):
        self.pet: Pet = pet
        self.medication: str = medication
        self.dosage: str = dosage
        self.date: str = date  # Здесь можно использовать datetime
