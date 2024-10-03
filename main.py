import csv
import random
from geopy import distance
import mysql.connector
import Funktioita
import random
import text
import time

#Tyhjentää datan game-taulusta:
def clear_game_data():
    clear = (f'DELETE FROM game;')
    #print(clear)
    cursor = connection.cursor()
    cursor.execute(clear)


#Luo uuden pelin/lisää aloitusdatan game-tauluun:
def create_new_game(player):
    new_game = (f'INSERT INTO game(id,screen_name,points,travel_distance,location,start_location,max_trophy,current_trophy) '
                f'VALUES(1,"{player}",0,0,"EFHK","EFHK",7,0);')
    #print(new_game)
    cursor = connection.cursor()
    cursor.execute(new_game)

#Hakee 5 lentokenttää 4 eri ilmansuunnasta ja yhden samalta mantereelta. Kysyy pelaajalta mihin kohteeseen haluua matkustaa ja palauttaa arvoina kohdekentän "ident" ja matka metreinä.
#10-20 deg atm mitat. 1 deg about 110km.

#hakee nykyisen sijainnin koordinaatit
def get_current_location_cordinates():
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident in(SELECT location FROM game);'
    cursor = connection.cursor()
    cursor.execute(sql)
    current_location_cordinates = cursor.fetchall()
    return current_location_cordinates
#hakee ident:in avulla koordinaatit
def get_location_cordinates_by_ident(ident):
    sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = "{ident}"'
    cursor = connection.cursor()
    cursor.execute(sql)
    location_cordinates = cursor.fetchall()
    return location_cordinates
#hakee listan random kenttiä. 1.arvo on joko latitude tai longtitude, ja seuraavat on min ja max arvot joilla haetaan.
def get_random_location(deg,min,max):
    sql = f'SELECT ident FROM airport WHERE {deg} > {min} AND {deg} < {max};'
    cursor = connection.cursor()
    cursor.execute(sql)
    random_location = cursor.fetchall()
    return random_location
#hakee ident:in avulla lentokentän nimen ja maan missä sijaitsee
def get_airport_name_country_by_ident(ident):
    sql = f'SELECT airport.name AS airport, country.name AS country FROM airport, country WHERE ident = "{ident}" AND airport.iso_country = country.iso_country;'
    cursor = connection.cursor()
    cursor.execute(sql)
    airport_name_country = cursor.fetchall()
    return airport_name_country
#Valitsee listalta yhden kentän randomilla, tulostaa kentän nimen, maan ja etäisyyden(KM)
def get_location_distance_name_country(location_list,num):
    if location_list[0] == None:
        print("Ei kenttiä tässä suunnassa.")
    else:
        random_num = random.randint(0,len(location_list)-1)
        location =location_list[random_num]
        location_distance = distance.distance(get_current_location_cordinates(), get_location_cordinates_by_ident(location[0])).meters
        location_name = get_airport_name_country_by_ident(location[0])
        print(f"{num}. {location_name[0][0]} {location_name[0][1]} {float(location_distance)/1000:.2f}km")
        return location, location_distance
#Hakee listan samalla mantereella olevista lentokentistä
def get_location_on_same_continent():
    sql = f'SELECT ident FROM airport WHERE continent IN (SELECT continent FROM airport WHERE ident IN( SELECT location FROM game));'
    cursor = connection.cursor()
    cursor.execute(sql)
    random_location = cursor.fetchall()
    return random_location
#hakee 5 random kenttää. Tulostaa vaihtoehdot ja kysyy käyttäjältä mihin haluaa matkustaa. Käyttäjän vastauksen mukaan palauttaa vain valitun kentän "ident" ja etäisyys nykyiseen(M)
def get_5_random_location():
    current_location_cordinates = get_current_location_cordinates()
    location_north_list = get_random_location("latitude_deg",str(float(current_location_cordinates[0][0]+10)),str(float(current_location_cordinates[0][0]+20)))
    location_north = get_location_distance_name_country(location_north_list,1)
    location_south_list = get_random_location("latitude_deg",str(float(current_location_cordinates[0][0]-20)),str(float(current_location_cordinates[0][0]-10)))
    location_south = get_location_distance_name_country(location_south_list,2)
    location_east_list = get_random_location("longitude_deg",str(float(current_location_cordinates[0][1]+10)),str(float(current_location_cordinates[0][1]+20)))
    location_east = get_location_distance_name_country(location_east_list,3)
    location_west_list = get_random_location("longitude_deg",str(float(current_location_cordinates[0][1]-20)),str(float(current_location_cordinates[0][1]-10)))
    location_west = get_location_distance_name_country(location_west_list,4)
    location_continent_list = get_location_on_same_continent()
    location_continent = get_location_distance_name_country(location_continent_list,5)
    print()
    vastaus = 0
    while vastaus not in ['1','2','3','4','5']:
        vastaus = input("Mihin kohteeseen haluat matkustaa? (1-5)\n: ")
        if vastaus == "1":
            return location_north
        elif vastaus == "2":
            return location_south
        elif vastaus == "3":
            return location_west
        elif vastaus == "4":
            return location_east
        elif vastaus == "5":
            return location_west
        else:
            print("väärä syöte!")

# Sattumatapahtumien satunnaishaku
def pick_random_event():
    sql = "SELECT text, points FROM random_events ORDER BY RAND() LIMIT 1;"
    cursor = connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()
    return {"points": res[1], "string": res[0]}

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

# Päivittää pisteet
def update_game_points(newPoints, gameId):
    sql = "UPDATE game SET points = %s WHERE id = %s;"
    cursor = connection.cursor()
    cursor.execute(sql, (newPoints, gameId))
    connection.commit()
    cursor.close()

# Päivittää tämänhetkisen matkamuiston
def update_game_current_trophy(currentTrophy, gameId):
    sql = "UPDATE game SET current_trophy = %s WHERE id = %s;"
    cursor = connection.cursor()
    cursor.execute(sql, (currentTrophy, gameId))
    connection.commit()
    cursor.close()

def update_game_distance_travelled(distance):
    print("dap")

# Päivittää tämänhetkisen sijainnin
def update_game_current_location(currentLocation, gameId):
    sql = "UPDATE game SET location = %s WHERE id = %s;"
    cursor = connection.cursor()
    cursor.execute(sql, (currentLocation, gameId))
    connection.commit()
    cursor.close()

def distance_between_airfields(airfield1, airfield2):
    print("dapetidap")

#Laskee matkamuiston pistearvon
#aloituslentokentän ja tämän hetkisen lentokentän välisen etäisyyden avulla:
def calculate_trophy_points():
    select_start_lat_long = (f'SELECT latitude_deg, longitude_deg FROM airport,game '
                             f'WHERE ident = game.start_location AND game.id = 1;')
    cursor = connection.cursor()
    cursor.execute(select_start_lat_long)
    start_lat_long = cursor.fetchall()

    select_current_lat_long = (f'SELECT latitude_deg, longitude_deg FROM airport,game '
                               f'WHERE ident = game.location AND game.id = 1;')
    cursor = connection.cursor()
    cursor.execute(select_current_lat_long)
    current_lat_long = cursor.fetchall()

    start_to_current_distance = distance.distance((start_lat_long[0][0], start_lat_long[0][1]),
                                        (current_lat_long[0][0], current_lat_long[0][1])).km

    points = 30 + int(start_to_current_distance / 125)
    return points

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


# sql connection
user = input('SQL user: ')
pw = input('SQL Password: ')
db_name = input('SQL database name: ')


connection = mysql.connector.connect(
         host = '127.0.0.1',
         port = 3306,
         database = f'{db_name}',
         user = f'{user}',
         password = f'{pw}',
         autocommit = True
         )

#PELIN INTRO:
print('Tervetuloa "Souvenir Collector"-peliin!')
screen_name = input("Syötä nimesi, jotta voimme täyttää matkadokumenttisi.\n: ")
while screen_name == "":
    print("Tyhjä syöte. Et voi matkustaa ilman nimeä!")
    screen_name = input("Syötä nimesi, jotta voimme täyttää matkadokumenttisi.\n: ")
print()
story_choice = input("Haluatko lukea pelin tarinan? (Kyllä/En)\n: ")
if story_choice.lower() == "kyllä":
    print()
    text.print_story(screen_name)
print()
show_instructions = input('Paina "Enter" jatkaaksesi\n')
print()
text.print_instructions()

#PELIN ALOITUS:
print()
start = input('Aloita peli painamalla "Enter"\n')

clear_game_data()
create_new_game(screen_name)
max_trophies_collected = False

#LOOPPI ALKAA TÄSTÄ:
while max_trophies_collected == False:
    print()
    print("Tässä on kohteet joihin voit matkata. Valitse yksi:")
    print()
    selected_location = get_5_random_location()
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
    time.sleep(0.25)
    collect_trophy = input("Haluatko ottaa mukaasi matkamuiston tästä kohteesta? (Kyllä/En)\n"
                           "Voit jatkaa seuraavaan kohteeseen keräämättä matkamuistoa, jos haluat.\n: ")
    if collect_trophy.lower() == "kyllä":
        calculate_trophy_points()
        #update_current_trophy()
    else:
        print("Et ottanut matkamuistoa mukaasi.")
    #print(check_trophy_status())
    print()
    time.sleep(0.5)
    if max_trophies_collected != True:
        print("Ennen kuin jatkat matkaasi seuraavaan kohteeseen, haluat varmaan tietää,\n"
          "paljonko pisteitä sinulla on.")
        print()
        get_current_points_by_screen_name(screen_name)
        print()
        print("Kohti seuraavaa kohdetta!")
    time.sleep(1)

#LOOPPI LOPPU

#points_data = get_points() #Tarvitsee funktion...
#distance_travelled = get_travel_distance() #Tarvitsee funktion...
#final_score = calculate_final_points(distance_travelled,points_data)
#print(f"Olet palannut takaisin kotiin, ja matkasi on nyt tullut päätökseen.\n"
    #  f"Keräsit yhteensä {points_data} pistettä, mutta matkasi pituus,\n"
   #   f"joka oli {distance_travelled} kilometriä, vähensi pisteitäsi.")
print()
#print(f"Lopullinen pistemääräsi siis on: {final_score}")