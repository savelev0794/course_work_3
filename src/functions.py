import json
from pathlib import Path
from datetime import datetime
FILE = Path(__file__).resolve().parent / 'operations.json'
# Импорты всех необходимых бибилиотек, а также запись в константу пути к файлу json

def load_json(file_path):
    """Загружаем файл json"""
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)
        return data


file_json = load_json(FILE)


def date_sorted(mate):
    '''Сортируем операции по дате от позднейшей к новейшей'''
    sorted_file = sorted(mate, key=lambda x: x.get('date'), reverse=True)
    return sorted_file


sorted_data = date_sorted(file_json)


# Cоздаем пустой список для записи последних 5 операций
last_five_operations = []


def load_last_five(resorted):
    '''Возвращаем последние 5 успешных операций'''
    count = 0

    for state_status in resorted:
        state = state_status.get('state', '')

        if state == 'EXECUTED':
            last_five_operations.append(state_status)
            count += 1

        if count == 5:
            break
    return last_five_operations


five_list = load_last_five(sorted_data)

# Создаем 2 списка для записи в них наименования банка и наименоваие счета
name_bank = []
name_card = []


def name_split(an):
    '''Разделяем значения статусов и наименований банков и записываем в два разных списка'''

    for r in an:
        from_1 = r.get('from', '')
        w = from_1.split(' ')

        name_bank.append(' '.join(w[:-1]))
        name_card.append(''.join(w[-1]))
    return name_bank, name_card


name_bank, name_card = name_split(five_list)

# Пустой список для замаскированных номеров

mask_card = []


def masking_stars(q):
    '''Маскируем нужные символы звездочками'''
    for o in q:
        stars = len(o) - 10

        mask_card.append(o[:6] + "*" * stars + o[-4:])
    return mask_card


name_card = masking_stars(name_card)

result_strings = []

for string in name_card:
    for i in range(0, len(string), 4):
        formatted_string = ' '.join([string[i:i + 4] for i in range(0, len(string), 4)])
        result_strings.append(formatted_string)

for list_bank, s, list_numb in zip(name_bank, last_five_operations, result_strings):
    data_operation = s['date']
    description = s['description']
    name = s['operationAmount']['currency']['name']
    summ_operation = s['operationAmount']['amount']
    date = datetime.strptime(s["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    to = s['to'][:-14].replace('Счет ', '')
    list_bank_1 = f'{list_bank} ' if list_bank else ''
    print(f'{date} {description}\n'
          f'{list_bank_1}{list_numb} -> Счет **{to[2:]}\n'
          f'{summ_operation} {name}\n')

