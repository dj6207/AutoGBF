import pickle

class DataClass:
    def __init__(self, command, coordinate, delta_x, delta_y):
        self.command = command
        self.coordinate = coordinate
        self.delta_x = delta_x
        self.delta_y = delta_y

def save_data_classes(data_classes, file_name=".\\data_classes.pickle"):
    with open(file_name, 'wb') as file:
        pickle.dump(data_classes, file)

def load_data_classes(file_name=".\\data_classes.pickle"):
    try:
        with open(file_name, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError as e:
        print(e)

def delete_data_class(data_classes, name):
    data_classes = [data_class for data_class in data_classes if data_class.command != name]
    return data_classes

def search_data_class(data_classes, command):
    for data_class in data_classes:
        if data_class.command == command:
            return data_class
    return None

def print_data_classes(data_classes):
    for data_class in data_classes:
        print(f'Command:{data_class.command}, Coordinate:{data_class.coordinate}, Delta X:{data_class.delta_x}, Delta Y:{data_class.delta_y}')

def test(file_name=".\\test.pickle"):
    data_classes_0 = [DataClass('class1', 1, 1, 1), DataClass('class2', 2, 2, 2)]

    save_data_classes(data_classes_0, file_name)
    data_classes_1 = load_data_classes(file_name)
    print_data_classes(data_classes_1)

    data_classes_1.append(DataClass('class3', 3, 3, 3))
    save_data_classes(data_classes_1, file_name)
    print_data_classes(data_classes_1)

    data_classes_2 = load_data_classes(file_name)
    data_classes_2 = delete_data_class(data_classes_2, 'class3')
    print_data_classes(data_classes_2)

    print(search_data_class(data_classes_2, 'class2').command)

def init_database(file_name=".\\data_classes.pickle"):
    data_class = [
                    # DataClass('command', (x, y), delta_x, delta_y)
                    DataClass('back', (95, 1010), 5, 1), 
                    DataClass('slime', (265, 700), 50, 20),
                    DataClass('reload', (300, 1010), 5, 1),
                    DataClass('summon_slot_1', (230, 370), 60, 15),
                    DataClass('party_screen_ok', (300, 545), 30, 1),
                    DataClass('character_slot_1', (100, 465), 5, 20),
                    DataClass('skill_slot_1', (165, 485), 5, 5),
                    DataClass('skill_slot_2', (225, 485), 5, 5),
                    DataClass('attack_button', (310, 370), 25, 10),
                    DataClass('reload_button', (85, 60), 1, 1),

                    DataClass('sakura_event_raid_lvl60_play', (475, 90), 1, 1)
                    

                    ]
    save_data_classes(data_class, file_name)
    load = load_data_classes(file_name)
    print_data_classes(load)