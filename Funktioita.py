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
        location_distance = distance.distance(current_location_cordinates, get_location_cordinates_by_ident(location[0])).meters
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
    vastaus = 0
    while vastaus not in ['1','2','3','4','5']:
        vastaus = input("Mihin kohteeseen haluat matkustaa?: (1-5)")
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


#tämä funkkito lisää tietokantaan uuden kentän "ident" ja kuljetun matkan (m)
def set_new_location_and_distance(ident,distance):
    sql = f'UPDATE game SET location = "{ident}", travel_distance = travel_distance + {distance};'
    cursor = connection.cursor()
    cursor.execute(sql)
    return
'''
#esimerkki millä saa 5 random kenttää ja kysyy käyttäjältä mihin liikutaan. ja lisää tarvittavat tiedot tietokantaan

location = get_5_random_location()
set_new_location_and_distance(location[0][0],int(location[1]))
'''

# Laskee lopulliset pisteet (kertoimet[vakiot] tulee vielä kokeilla)
def calculate_final_points(points, distance_travelled):
    final_points = points - (distance_travelled // 2_000)
    return final_points

# funktio lisää pelaajan nimen ja hänen pisteet tietokantaan.
def screen_name_and_points(name,points):
    sql = f"INSERT INTO scoreboard (screen_name,points) VALUES ('{name}','{points}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()
    return

# funktio, joka näyttää TOP-10 pelaajaa.
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
