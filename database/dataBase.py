import pickle

class DataClass:
    def __init__(self, command, coordinate, delta_x, delta_y):
        self.command = command
        self.coordinate = coordinate
        self.delta_x = delta_x
        self.delta_y = delta_y

def save_data_classes(data_classes, file_name=".\\database\\data_classes.pickle"):
    with open(file_name, 'wb') as file:
        pickle.dump(data_classes, file)

def load_data_classes(file_name=".\\database\\data_classes.pickle"):
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

def test(file_name="test.pickle"):
    data_classes = [DataClass('class1', 1, 1, 1), DataClass('class2', 2, 2, 2)]

    save_data_classes(data_classes, file_name)
    data_classes_1 = load_data_classes(file_name)
    print_data_classes(data_classes_1)

    data_classes_1.append(DataClass('class3', 3, 3, 3))
    save_data_classes(data_classes_1, file_name)
    print_data_classes(data_classes_1)

    data_classes_2 = load_data_classes(file_name)
    data_classes_2 = delete_data_class(data_classes_2, 'class1')
    print_data_classes(data_classes_2)

def init_database(file_name=".\\database\\data_classes.pickle"):
    data_classes = [DataClass('Back', (95, 1010), 5, 1), 
                    DataClass('Slime', (265, 700), 50, 20)]
    save_data_classes(data_classes, file_name)
    load = load_data_classes(file_name)
    print_data_classes(load)