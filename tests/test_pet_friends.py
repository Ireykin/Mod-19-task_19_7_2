from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    """Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result"""
    assert status == 200
    assert 'key' in result
    """Сверяем полученные данные с нашими ожиданиями"""

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet(name="Жужу", animal_type="Жужелица", age='1', pet_photo="images/zhu.jpg"):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    """Получаем полный путь изображения питомца и сохраняем в переменную pet_photo"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """Запрашиваем ключ api и сохраняем в переменую auth_key"""
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    """Добавляем питомца"""
    assert status == 200
    assert result['name'] == name
    """Сверяем полученный ответ с ожидаемым результатом"""

def test_successful_update_self_pet_info(name='Жужу', animal_type='Жужелица', age=3):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    """Получаем ключ auth_key и список своих питомцев"""
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        """Если список не пустой, то пробуем обновить его имя, тип и возраст"""
        assert status == 200
        assert result['name'] == name
        """Проверяем что статус ответа = 200 и имя питомца соответствует заданному"""
    else:
        raise Exception("Свои питомцы отсутствуют.")
    """если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев"""

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    """Получаем ключ auth_key и запрашиваем список своих питомцев"""
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Махито", "махаон", "1", "images/mah.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        """Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев"""
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    """Берём id первого питомца из списка и отправляем запрос на удаление"""
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    """Ещё раз запрашиваем список своих питомцев"""
    assert status == 200
    assert pet_id not in my_pets.values()
    """Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца"""

def test_add_new_pet_without_foto_valid_data(name="Бобик", animal_type="Собака", age='3'):
    """Проверяем что можно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """Запрашиваем ключ api и сохраняем в переменую auth_key"""
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    """Добавляем питомца"""
    assert status == 200
    assert result['name'] == name
    """Сверяем полученный ответ с ожидаемым результатом"""

def test_successful_update_self_pet_photo(pet_photo="images/mah.jpg"):
    """Проверяем возможность добавления фото к питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    """Получаем полный путь изображения питомца и сохраняем в переменную pet_photo"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    """Получаем ключ auth_key и список своих питомцев"""
    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        """Если список не пустой, то пробуем обновить фото"""
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        """Проверяем что статус ответа = 200 и фото питомца соответствует заданному"""
    else:
        raise Exception("Питомцы отсутствуют.")
    """если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомца"""

def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с валидным паролем и с невалидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
