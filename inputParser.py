from queue import Queue

class InputParser:
    # Loads the sequence of inputs into a queue and returns a queue 
    # to be used by the ai to determine what to click next
    def __init__(self, input_path="./Input.txt", vaild_input_path="./ValidInput.txt"):
        # Establish the path of the files
        self.input_path = input_path
        self.vaild_input_path = vaild_input_path
        self.valid_set = []
        with open(self.vaild_input_path) as file:
            # Makes a list of valid commands 
            # Will be use to verify the commands
            for line in file:
                self.valid_set.append(line.strip().lower())

    def load_queue(self):
        queue = Queue()
        path = self.input_path
        with open(path) as file:
            for line in file:
                array = line.lower().split()
                if (self.valid_command(array)):
                    # Puts the valid command into the queue as a tuple
                    queue.put(tuple(array))
                else:
                    raise Exception("Invalid Command in Input.txt")
        # Adds the command stop for the ai know when to stop
        queue.put(tuple(['stop']))
        return queue
    
    def valid_command(self, array):
        # returns 0 if invalid comamdn else return 1
        for i in array:
            if not (i in self.valid_set):
                return 0
        return 1
    
    def print_queue(self, queue):
        # prints queue
        while queue.qsize():
            print(queue.get())