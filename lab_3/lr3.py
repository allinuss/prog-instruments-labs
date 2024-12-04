import re
import pandas as pd
import json


from checksum import calculate_checksum


# Функции для валидации данных с использованием регулярных выражений
def validate_telephone(telephone):
    pattern = r'^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$'
    return re.match(pattern, telephone) is not None

def validate_height(height):
    # Проверяем, что значение роста находится в пределах от 0.5 до 3.00 метров
    pattern = r'^(?:[1-2]?\d(\.\d{1,2})?|3(\.00)?)$'
    if re.match(pattern, str(height)):
        # Дополнительная проверка для роста больше 3 метров и меньше 0.5 метров
        height_value = float(height)
        if 0.5 <= height_value <= 3.00:
            return True
    return False


def validate_http_status_message(status_message):
    pattern = r'^\d{3} [A-Za-z ]+$'
    return re.match(pattern, status_message) is not None


def validate_inn(inn):
    pattern = r'^\d{12}$'
    return re.match(pattern, inn) is not None


def validate_identifier(identifier):
    pattern = r'^\d{2}-\d{2}\/\d{2}$'
    return re.match(pattern, identifier) is not None


def validate_ip_v4(ip_v4):
    pattern = r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    return re.match(pattern, ip_v4) is not None


def validate_latitude(latitude):
    pattern = r'^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$'
    return re.match(pattern, latitude) is not None


def validate_blood_type(blood_type):
    pattern = r'^(A|B|AB|O)[\+\−]$'
    return re.match(pattern, blood_type) is not None


def validate_isbn(isbn):
    pattern = r'^(\d{3}\-)?\d-\d{5}-\d{3}-\d$'
    return re.match(pattern, isbn) is not None


def validate_uuid(uuid):
    pattern = r'^[a-f0-9\-]{36}$'
    return re.match(pattern, uuid) is not None
def validate_occupation(occupation):
    # Регулярное выражение для проверки профессии
    pattern = r'^[A-Za-zА-Яа-яёЁ\- ]+$'
    return re.match(pattern, occupation) is not None

def validate_issn(issn):
    # Регулярное выражение для проверки ISSN
    pattern = r'^\d{4}-\d{4}$'
    return re.match(pattern, issn) is not None


def validate_date(date):
    pattern = r'^\d{4}-(([0]\d)|([1][0-2]))-(([0-2]\d)|([3][0-1]))$'
    return re.match(pattern, date) is not None


# Валидация всей строки данных
def validate_data(data):
    validation_results = {
        'telephone': validate_telephone(data['telephone']),
        'height':validate_height(data['height']),
        'inn': validate_inn(data['inn']),
        'identifier': validate_identifier(data['identifier']),
        'occupation': validate_identifier(data['occupation']),
        'latitude': validate_latitude(data['latitude']),
        'blood_type': validate_blood_type(data['blood_type']),
        'issn': validate_isbn(data['issn']),
        'uuid': validate_uuid(data['uuid']),
        'date': validate_date(data['date'])
    }
    return validation_results



# Сериализация результата в JSON
def serialize_result(variant: int, checksum: str) -> None:
    result = {
        'variant': variant,
        'checksum': checksum
    }

    with open('result.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)


# Чтение CSV с использованием pandas и валидация
def read_and_validate_csv(file_path, variant_number):
    df = pd.read_csv(file_path, sep=";", encoding="utf-16")

    validation_results = []
    error_rows = []

    # Перебираем строки DataFrame для валидации
    for index, row in df.iterrows():
        # Собираем данные для валидации
        data = {
            'telephone': row.get('telephone'),
            'height': row.get('height'),
            'inn': row.get('inn'),
            'identifier': row.get('identifier'),
            'occupation': row.get('occupation'),
            'latitude': row.get('latitude'),
            'blood_type': row.get('blood_type'),
            'issn': row.get('issn'),
            'uuid': row.get('uuid'),
            'date': row.get('date')
        }

        # Выполняем валидацию
        result = validate_data(data)
        validation_results.append(result)

        # Добавляем номера строк с ошибками
        if any(not valid for valid in result.values()):
            error_rows.append(index)

    # Вычисляем контрольную сумму
    checksum = calculate_checksum(error_rows)

    # Сериализуем результат в файл
    serialize_result(variant_number, checksum)

    return validation_results, error_rows


# Пример использования
file_path = '8.csv'  # Укажите путь к вашему файлу CSV
variant_number = "8"

validation_results, error_rows = read_and_validate_csv(file_path, variant_number)

