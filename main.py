import csv
import random

# Sattumatapahtumien satunnaishaku
def pick_random_event():
    events = []
    with open('events.csv', 'r', encoding='utf-8') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            events.append(row)
        event = events[random.randint(0, len(events) - 1)]
        return {"type": event[0], "string": event[1]}

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

