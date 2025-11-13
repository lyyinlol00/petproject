class PetError(Exception):
    """Базовый класс для ошибок в системе питомцев."""
    pass

class PetNotFoundError(PetError):
    """Питомец не найден."""
    pass

class OwnerNotFoundError(PetError):
    """Владелец не найден."""
    pass

class InvalidDataError(PetError):
    """Неверный формат или тип данных."""
    pass

class FileProcessingError(PetError):
    """Ошибка при работе с файлами."""
    pass

class EmptyInputError(PetError):
    """Пустой ввод данных."""
    pass

class InvalidFileFormatError(PetError):
    """Неверный формат файла."""
    pass

class InvalidNumberError(PetError):
    """Неверный формат числа - нужно ввести цифры."""
    pass

