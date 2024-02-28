# Case- study #7 "Petrol station"
# Developers : Setskov M. (%)
#              Osokina A. (63%)
# This program generates a report on the operation of the filling station

import lc_ru as lc

def data_petrol_stations():
    """
    Считывает информацию о заправочных станциях из файла 'azs.txt' и формирует словарь.

    Returns:
    dict: Словарь с информацией о заправочных станциях.
    """
    petrol_stations = {}

    with open('azs.txt', 'r', encoding='utf-8') as file:
        for string in file:
            string = string.split()
            station_number = int(string[0])
            queue_length = int(string[1])
            petrol_stations[station_number] = {}
            petrol_stations[station_number]['queue'] = queue_length
            petrol_stations[station_number]['gas_type'] = string[2:]

    return petrol_stations


def arriving_cars():
    """
    Считывает запросы на заправку из файла 'input.txt' и возвращает список запросов.

    Returns:
    list: Список запросов на заправку.
    """
    requests = []

    with open('input.txt', 'r', encoding='utf-8') as file:
        for string in file:
            requests.append(string.strip())

    return requests


def fueling_time(litres):
    """
    Рассчитывает время заправки автомобиля в зависимости от количества литров топлива.

    Args:
    litres (int): Количество литров топлива.

    Returns:
    int: Время заправки в минутах.
    """
    import random

    if litres % 10 != 0:
        minutes = litres // 10 + 1
    else:
        minutes = litres // 10

    assident = random.randint(-1, 1)
    minutes += assident
    if minutes == 0:
        minutes = 1

    return minutes


def current_queues(petrol_stations):
    """
    Создает словарь текущих очередей на заправочных станциях.

    Args:
    petrol_stations (dict): Информация о заправочных станциях.

    Returns:
    dict: Словарь текущих очередей.
    """
    current_queues = {}

    for station in petrol_stations:
        info = {}
        info['current_queue'] = 0
        info['max_queue'] = petrol_stations[station]['queue']
        current_queues[station] = info

    return current_queues


def gas_type_info(petrol_stations):
    """
    Формирует информацию о типах бензина на заправочных станциях.

    Args:
    petrol_stations (dict): Информация о заправочных станциях.

    Returns:
    dict: Информация о типах бензина.
    """
    gas_type_info = {}
    gas_type_info['total amount of petrol'] = 0

    for station in petrol_stations:
        for gas_type in petrol_stations[station]['gas_type']:
            if gas_type not in gas_type_info:
                info = {}

                if gas_type == 'АИ-80':
                    price = 44.74
                elif gas_type == 'АИ-92':
                    price = 49.60
                elif gas_type == 'АИ-95':
                    price = 53.00
                elif gas_type == 'АИ-98':
                    price = 59.90

                info['price'] = price
                info['stations'] = [station]
                info['amount of petrol'] = 0
                gas_type_info[gas_type] = info

            else:
                info = gas_type_info[gas_type]
                info['stations'] = info['stations'] + [station]

    return gas_type_info


def add_to_queue(requests, gas_type_info, current_queue, client_lost):
    """
    Добавляет запрос на заправку в очередь на ближайшую доступную заправку.

    Args:
    requests (str): Запрос на заправку.
    gas_type_info (dict): Информация о типах бензина.
    current_queue (dict): Текущие очереди на заправочных станциях.
    client_lost (int): Количество утерянных клиентов.

    Returns:
    str: Номер заправочной станции, на которую добавлен запрос.
    """
    gas_type = requests.split()[2]
    time = fueling_time(int(requests.split()[1]))
    choice = []

    for station in gas_type_info[gas_type]['stations']:
        if current_queue[station]['current_queue'] != current_queue[station]['max_queue']:
            choice.append((current_queue[station]['current_queue'], station))

    if choice:
        choice.sort()
        station = choice[0][1]
        current_queue[station]['current_queue'] += 1
        current_queue[station]['сar ' + str(len(current_queue[station]) - 2 + 1)] = {}
        current_queue[station]['сar ' + str(len(current_queue[station]) - 2)]['time left'] = time
        current_queue[station]['сar ' + str(len(current_queue[station]) - 2)]['car info'] = requests

        gas_type_info['total amount of petrol'] += int(requests.split()[1])
        gas_type_info[gas_type]['amount of petrol'] += int(requests.split()[1])

        return station

    else:
        client_lost += 1
        print(lc.MISSED_CLIENT)


def queue_shift(current_queue):
    """
    Сдвигает очередь на одну позицию.

    Args:
    current_queue (dict): Текущая очередь на заправочной станции.

    Returns:
    dict: Обновленная очередь.
    """
    current_queue.pop('сar 1')
    if current_queue['current_queue'] != 1:
        for car_number in range(1, current_queue['current_queue']):
            current_queue['сar ' + str(car_number)] = current_queue['сar ' + str(car_number + 1)].copy()
        current_queue.pop('сar ' + str(current_queue['current_queue']))

    current_queue['current_queue'] -= 1

    return current_queue


def main():

    client_lost = 0
    petrol_stations = data_petrol_stations()
    gas_type = gas_type_info(petrol_stations)
    current_queue = current_queues(petrol_stations)
    requests = arriving_cars()

    new_car = requests[0]
    new_car_time = new_car[:5]
    current_time = '00:00'

    while current_time != '23:59':

        for station in current_queue:
            if current_queue[station]['current_queue']:
                current_queue[station]['сar 1']['time left'] -= 1

                if current_queue[station]['сar 1']['time left'] == 0:
                    print(lc.CLIENT.format(current_time, current_queue[station]['сar 1']['car info']))
                    current_queue[station] = queue_shift(current_queue[station])

                    for station_number in petrol_stations:
                        print(lc.STATION_QUEUE.format(station_number, petrol_stations[station_number]['queue'],
                                                      ' '.join(petrol_stations[station_number]['gas_type'])), end='')
                        print('*' * current_queue[station_number]['current_queue'])
                    print()

        if new_car_time == current_time:
            station = add_to_queue(new_car, gas_type, current_queue, client_lost)
            print(lc.NEW_CLIENT.format(current_time, new_car, station))

            requests = requests[1:]
            new_car = requests[0]
            new_car_time = new_car[:5]

            for station in petrol_stations:
                print(lc.STATION_QUEUE.format(station, petrol_stations[station]['queue'],
                                              ' '.join(petrol_stations[station]['gas_type'])), end='')
                print('*' * current_queue[station]['current_queue'])
            print()

        hour, minute = map(int, current_time.split(':'))
        minute += 1

        if minute == 60:
            hour += 1
            minute = 0
        hour = '{:02d}'.format(hour)
        minute = '{:02d}'.format(minute)
        current_time = hour + ':' + minute

    print()
    print(lc.SUMM_LITERS, gas_type['total amount of petrol'])
    gas_type.pop('total amount of petrol')
    total_revenue = 0

    for type in gas_type:
        print(lc.DAY_LITERS.format(type), gas_type[type]['amount of petrol'])
        revenue = gas_type[type]['amount of petrol'] * gas_type[type]['price']
        print(lc.REVENUE, round(revenue, 2))
        total_revenue += revenue

    print(lc.TOTAL_REVENUE, round(total_revenue, 2))
    print(lc.LOST_CLIENTS, client_lost)


main()
