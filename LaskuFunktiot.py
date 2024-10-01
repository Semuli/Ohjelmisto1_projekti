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
