# Case- study #7 "Petrol station"
# Developers : Setskov M. (%)
#              Osokina A. (%)
# This program generates a report on the operation of the filling station


# Choice of language
language = input('Choose your language:\n1. English\n2. Russian\n').lower()
while True:
    if language == 'english' or language == 'en' or \
            language == 'e' or language == '1':
        import lc_en as lc

        break
    elif language == 'russian' or language == 'ru' or \
            language == 'r' or language == '2':
        import lc_ru as lc

        break
    language = input('Please, write your answer correctly, type "1" or "2".\n')


def petrol_station_data():
    """
    Getting information about current gas station.

    :return: dictionary with information about gas station
    """
    petrol_station = {}
    with open('station_data.txt', 'r', encoding='utf-8') as file:
        for string in file:
            string = string.split()
            column_number = int(string[0])
            amount_of_places = int(string[1])
            gas_type = string[2:]
            petrol_station[column_number] = {}
            petrol_station[column_number]['queue'] = amount_of_places
            petrol_station[column_number]['gaz types'] = gas_type

    return petrol_station


"""
petrol_stations = {
    1: {'queue': 3, 'gaz types': ['АИ-80']},
    2: {'queue': 2, 'gaz types': ['АИ-92']},
    3: {'queue': 4, 'gaz types': ['АИ-92', 'АИ-95', 'АИ-98']}
}
"""


def arriving_cars():
    """
    Process data from an input file.

    :return: Dictionary in the format {"time": [litres, "gas type"]}
    """
    requests = {}
    with open('input.txt', 'r', encoding='utf-8') as file:
        for string in file:
            string = string.split()
            requests[string[0]] = [int(string[1]), string[2]]

    return requests


def fueling_time(litres):
    """
    Representation of liters as time.

    :param litres: fuel quantity
    :return: filling time
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


