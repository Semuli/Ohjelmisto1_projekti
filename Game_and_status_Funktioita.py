#Tyhjentää datan game-taulusta:
def clear_game_data():
    clear = (f'DELETE FROM game;')
    print(clear)
    cursor = connection.cursor()  # (dictionary=True)
    cursor.execute(clear)
    return

#Luo uuden pelin/lisää aloitusdatan game-tauluun:
def create_new_game(player):
    new_game = (f'INSERT INTO game(id,screen_name,points,travel_distance,location,start_location,max_trophy,current_trophy) '
                f'VALUES(1,"{player}",0,0,"EFHK","EFHK",7,0);')
    print(new_game)
    cursor = connection.cursor() #(dictionary=True)
    cursor.execute(new_game)
    return

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