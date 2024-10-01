# funktio lisää pelaajan nimen ja hänen pisteet tietokantaan.
def screen_name_and_points(name,points):
    sql = f"INSERT INTO scoreboard (screen_name,points) VALUES ('{name}','{points}')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()
    return