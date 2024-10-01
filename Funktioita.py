#Hakee 4 lentokenttää 4 eri ilmansuunnasta
def get_4_random_airports():
    def get_current_location():
        sql = f'SELECT location FROM game;'
        cursor = connection.cursor()
        cursor.execute(sql)
        current_location = cursor.fetchall()
        return current_location

    def get_location_cordinates_by_icao(icao):
        sql = f'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = "{icao}"'
        cursor = connection.cursor()
        cursor.execute(sql)
        location_cordinates = cursor.fetchall()
        return location_cordinates

    def get_random_locations_nort_south(min,max):
        def get_random_locations(min, max):
            sql = f'SELECT ident FROM airport WHERE latitude_deg > "{min}" AND latitude_deg < "{max}";'
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            airport_north = cursor.fetchall()
            return airport_north
        airports = get_random_locations(str(float(current_latitude)+min),str(float(current_latitude)+max))
        randomnum = random.randint(0, len(airports))
        airport = airports[randomnum]
        return airport

    def get_random_locations_east_west(min,max):
        def get_random_locations(min, max):
            sql = f'SELECT ident FROM airport WHERE longitude_deg > "{min}" AND longitude_deg < "{max}";'
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            airport_north = cursor.fetchall()
            return airport_north
        airports = get_random_locations(str(float(current_longitude)+min),str(float(current_longitude)+max))
        randomnum = random.randint(0, len(airports))
        airport = airports[randomnum]
        return airport

    current_location = get_current_location()
    current_location_cordinates = get_location_cordinates_by_icao(current_location[0][0])
    current_latitude = current_location_cordinates[0][0]
    current_longitude = current_location_cordinates[0][1]

    location_north = get_random_locations_nort_south(10,20)
    location_south = get_random_locations_nort_south(-20,-10)
    location_east = get_random_locations_east_west(10,20)
    location_west = get_random_locations_east_west(-20,-10)

    return location_north, location_south, location_east, location_west

# Laskee lopulliset pisteet (kertoimet[vakiot] tulee vielä kokeilla)
def calculate_final_points(points, distance_travelled):
    final_points = points - (distance_travelled // 2_000)
    return final_points