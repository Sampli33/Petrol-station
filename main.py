# Case- study #7 "Petrol station"
# Developers : Setskov M. (%)
#              Osokina A. (%)
# This program generates a report on the operation of the filling station


# Choice of language

language = input('Choose your language:\n1.English\n2.Russian\n').lower()
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
