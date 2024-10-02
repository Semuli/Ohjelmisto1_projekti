import csv
import random
import mysql.connector
import game_and_status
import Funktioita
import random
import text
import time

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
    kursori = connection.cursor()
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

# sql connection
user = input('SQL user: ')
pw = input('SQL Password: ')
db_name = input('SQL database name: ')

connection = mysql.connector.connect(
         host = '127.0.0.1',
         port = 3306,
         database = db_name,
         user = user,
         password = pw,
         autocommit = True
         )

#PELIN INTRO:
print('Tervetuloa "Souvenir Collector"-peliin!')
screen_name = input("Syötä nimesi, jotta voimme täyttää matkadokumenttisi.\n: ")
print()
story_choice = input("Haluatko lukea pelin tarinan? (Kyllä/En)\n: ")
if story_choice.lower() == "kyllä":
    text.print_story(screen_name)

time.sleep(1) #Lyhyt paussi
print()
text.print_instructions()

#PELIN ALOITUS:
start = input('Aloita peli painamalla "Enter": ')
print()

game_and_status.clear_game_data()
game_and_status.create_new_game(screen_name)
max_trophies_collected = False

#LOOPPI ALKAA TÄSTÄ:
while max_trophies_collected == False:
    selected_location = Funktioita.get_5_random_location()
    #update_game_current_location(selected_location)
    #gained_distance = distance_between_airfields(airfield1, airfield2)
    #update_game_distance_travelled(gained_distance)
    print()
    event = pick_random_event()
    if event['type'] == 'positive':
        event_points = random.randint(1,25)
    else:
        event_points = random.randint(-25,-1)
    event_text = event['string']
    print("Miten matkakohteessa meni?:\n"+event_text + "\n" + str(event_points) + " pistettä")
    print()
    #update_game_points(event_points)