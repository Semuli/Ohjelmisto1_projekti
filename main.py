import csv
import random
import mysql.connector
import Funktioita
import LaskuFunktiot
import random
import text
import time

#Tyhjentää datan game-taulusta:
def clear_game_data():
    clear = (f'DELETE FROM game;')
    #print(clear)
    cursor = connection.cursor()
    cursor.execute(clear)
    return

#Luo uuden pelin/lisää aloitusdatan game-tauluun:
def create_new_game(player):
    new_game = (f'INSERT INTO game(id,screen_name,points,travel_distance,location,start_location,max_trophy,current_trophy) '
                f'VALUES(1,"{player}",0,0,"EFHK","EFHK",7,0);')
    #print(new_game)
    cursor = connection.cursor()
    cursor.execute(new_game)
    return

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

#Vertaa max_trophyn arvoa current_trophyn arvoon. Paluttaa True/False arvon,
#jolla voidaan katsoa, jatkuuko looppi. Funktio myös tulostaa tiedon matkamuistojen määrästä:
def check_trophy_status():
    select_max_trophy = f'SELECT max_trophy FROM game WHERE game.id = 1;'
    #print(select_max_trophy)
    cursor = connection.cursor() #(dictionary=True)
    cursor.execute(select_max_trophy)
    max = cursor.fetchall()

    select_current_trophy = f'SELECT current_trophy FROM game WHERE game.id = 1;'
    #print(select_current_trophy)
    cursor = connection.cursor()  # (dictionary=True)
    cursor.execute(select_current_trophy)
    current = cursor.fetchall()
    if max == current:
        status = True
        print(f"Hienoa! Olet kerännyt kaikki {max[0][0]} matkamuistoa!")
    else:
        status = False
        print(f"Sinulla on {current[0][0]} matkamuistoa. Tarvitset vielä "
              f"{max[0][0]-current[0][0]} lisää.")

    return status

"""
# sql connection
user = input('SQL user: ')
pw = input('SQL Password: ')
db_name = input('SQL database name: ')
"""

connection = mysql.connector.connect(
         host = '127.0.0.1',
         port = 3306,
         database = 'demo_game',
         user = 'riikkoo',
         password = '2001Riikka',
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

clear_game_data()
create_new_game(screen_name)
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
    collect_trophy = input("Haluatko ottaa mukaasi matkamuiston tästä kohteesta? (Kyllä/En)\n"
                           "Voit jatkaa seuraavaan kohteeseen keräämättä matkamuistoa, jos haluat.\n: ")
    if collect_trophy.lower() == "kyllä":
        LaskuFunktiot.calculate_trophy_points()
        # update_current_trophy()
    else:
        print("Et ottanut matkamuistoa mukaasi.")
    print(check_trophy_status())
    print()
    if max_trophies_collected != True:
        print("Ennen kuin jatkat matkaasi seuraavaan kohteeseen, haluat varmaan tietää,\n"
              "paljonko pisteitä sinulla on.")
        print()
        get_current_points_by_screen_name(screen_name)
    time.sleep(1)

# LOOPPI LOPPU

#points_data = get_points()  # Tarvitsee funktion...
#distance_travelled = get_travel_distance()  # Tarvitsee funktion...
#final_score = calculate_final_points(distance_travelled, points_data)
#print(f"Olet palannut takaisin kotiin, ja matkasi on nyt tullut päätökseen.\n"
   #   f"Keräsit yhteensä {points_data} pistettä, mutta matkasi pituus,\n"
   #   f"joka oli {distance_travelled} kilometriä, vähensi pisteitäsi.")
print()
#print(f"Lopullinen pistemääräsi siis on: {final_score}")