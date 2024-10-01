import csv
import random
import mysql.connector

# kirjautuminen
def sql_user_and_password():
    user = input('SQL user: ')
    pw = input('SQL Password: ')
    return user, pw

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

# funktio lisää pelaajan nimen ja hänen pisteet tietokantaan.
def screen_name_and_points(name,points):
    sql = f"INSERT INTO scoreboard (screen_name,points) VALUES ('{name}','{points}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()
    return
# Funktio, joka näyttää TOP-10 pelaajaa.

def TOP_10_PLAYERS():
    sql = f"Select screen_name, points from scoreboard order by points desc limit 10"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    result = kursori.fetchall()
    return result

command = input("Do you want to know the TOP-10 players? \nEnter Y = yes or N = no \n: ").upper()
while command != 'Y' and command != 'N':
    print("Please enter Y or N")
    command = input("").upper()

if command == "Y":
    top_10_players = TOP_10_PLAYERS()
    for player in top_10_players:
        print(f"Name: {player[0]}, Points: {player[1]}")
elif command == "N":
    enter = input("press enter")

# sql yhteys ???
yhteys = mysql.connector.connect(
         host = '127.0.0.1',
         port = 3306,
         database = 'demo_game',
         user = user,
         password = password,
         autocommit = True
         )