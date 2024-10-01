import csv
import random
import mysql.connector
import config

# Sattumatapahtumien satunnaishaku
def pick_random_event():
    events = []
    with open('events.csv', 'r', encoding='utf-8') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            events.append(row)
        event = events[random.randint(0, len(events) - 1)]
        return {"type": event[0], "string": event[1]}

# hakee tämänhetkiset pisteet (kunhan ne on päivitetty tietokantaan oikein)
def get_current_points_by_screen_name(screen_name):
    sql = f"""
    select points from game where screen_name = "{screen_name}";
    """
    print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if len(tulos) > 0:
        print(f'Pisteesi tällä hetkellä {tulos[0]}')
    else: # tämä on ehkä turha
        print('Pisteesi tällä hetkellä: 0')

def update_game_points(points):
    print("dapdap")

def update_game_trophy(trophy):
    print("dapdap")
    # lista?

def update_game_distance_travelled(distance):
    print("dap")

def update_game_current_location(newLocation):
    print("dap")

def distance_between_airfields(airfield1, airfield2):
    print("dapetidap")

# sql yhteys ???
yhteys = mysql.connector.connect(
         host = '127.0.0.1',
         port = 3306,
         database = 'demo_game',
         user = config.user,
         password = config.password,
         autocommit = True
         )