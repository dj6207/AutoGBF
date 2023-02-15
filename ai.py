import torch
import cv2 as cv
import pyautogui
import database.dataBase as db
import time
import random
from queue import Queue
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tools.windowCapture import WinCapture
from inputParser import InputParser 

# Notes
# Try to make the mouse movement more realistic
class Ai:
    #Inintalizes the ai
    def __init__(self, model_path="./model/best.pt", browser_name="Granblue Fantasy - Google Chrome", use_model=True, sleep_time=7, sleep_delta=3):
        # load custom model
        self.sleep_time = sleep_time
        self.sleep_delta = sleep_delta
        if use_model:
            self.use_model = True
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload = True)
            # takes all the class names from the model and puts them in the classes variable
            self.classes = self.model.names
            # select device
            if torch.cuda.is_available():
                self.device = 'cuda'
            else:
                self.device = 'cpu'
            print(f"Device: {self.device}")
            # init window capture
            self.wincap = WinCapture(browser_name)
        else:
            self.use_model = False
            print("No AI model is used")
        # load data base
        self.data_base = db.load_data_classes(".\\database\\data_classes.pickle")
        # load inputs into queue
        self.parser = InputParser()
        self.input_queue = self.parser.load_queue()
        self.found_queue = Queue()
    
    # Gives a score to the frame from 0 to 1 and returns teh labels and cords
    def score_frames(self, frame):
        self.model.to(self.device)
        # put the frames into a array
        frame = [frame]
        # the array is passed into the model
        result = self.model(frame)
        labels, cord = result.xyxyn[0][:,-1], result.xyxyn[0][:,:-1]
        return labels, cord

    def class_to_label(self, classes):
        return self.classes[int(classes)]

    # Passes in the scored frame so that it can be plotted
    # Passes in a item to look for.
    # If the item is found it will be added to teh found queue
    def ai_vision(self, score_results, frame, item=None):
        labels, cord = score_results
        # The shape of the frame
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(len(labels)):
            row = cord[i]
            # Row 4 is the score of the object
            # The higher the score the more confident the model is that the object is valid
            # Increase the score for a more accurate detectopm
            if row[4] >= 0.8:
                # row[0] is the x1 cord which is the top left x cord
                # row[1] is the y1 cord which is the top left y cord
                # row[2] is the x2 cord which is the bottom right x cord
                # row[3] is the y2 cord which is the bottom right y cord
                x1, y1, x2, y2, = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                # Color or rectangle box (b, g, r)
                rect_color = (0, 255, 0)
                # Color for text
                text_color = (0, 0, 255)
                label = self.class_to_label(labels[i])
                # plot the boxes and labels
                cv.rectangle(frame, (x1, y1), (x2, y2), rect_color)
                cv.putText(frame, f"{label} {str(row[4])[7:12]}", (x1, y2), cv.FONT_HERSHEY_SIMPLEX, 0.25, text_color, 1)
                # if the desired item is found add it to the found queue
                if item is not None and label in item:
                    self.found_queue.put((label, row))
        # displays the plotted frame
        cv.imshow("Browser GBF", frame)
        # if the item is found return true and the item
        return not self.found_queue.empty(), item

    def click(self, cord):
        x1 = cord[0].item()
        y1 = cord[1].item()
        x2 = cord[2].item()
        y2 = cord[3].item()
        x_cord = (x1 * (self.screen_x/2) + x2 * (self.screen_x/2))/2
        y_cord = (y1 * self.screem_y + y2 * self.screem_y)/2
        pyautogui.moveTo(x=x_cord, y=y_cord)
        pyautogui.click()

    def click_cord(self, x_cord, y_cord):
        pyautogui.moveTo(x=x_cord, y=y_cord, duration=0.2)
        pyautogui.click()
        wait_time = random.randint(self.sleep_time, self.sleep_time + self.sleep_delta)
        time.sleep(wait_time)
        
    
    def ai_neurons(self):
        # first get the command from the input queue
        command = self.input_queue.get()
        if self.use_model:
            # get the current frame
            frame = self.wincap.get_frame()
            # score the frame and get the labels and cords and store them in scored_frame
            scored_frame = self.score_frames(frame)
            # pass the scored frame and the frame into the ai_vision function and returns whether the item was found and the item
            found, item = self.ai_vision(score_results=scored_frame, frame=frame, item=command)
            # if the item was found then click the item
            if found:
                found_item = self.found_queue.get()
                # click the item
                # item 1 of the found item is the cords
                self.click(found_item[1])
            # clears the found queue
            self.found_queue.queue.clear()
        else:
            # search through a data based based on the command to get a known coordinate
            data = db.search_data_class(self.data_base, command[0])
            if data is not None:
                # click the coordinates
                offset_x = random.randint(-data.delta_x, data.delta_x)
                offset_y = random.randint(-data.delta_y, data.delta_y)
                self.click_cord(data.coordinate[0]+offset_x, data.coordinate[1]+offset_y)
            else:
                print("No data found")

    def run_ai(self):
        # checks if the input queue is empty
        # ai only runs if there is an input
        if (self.input_queue.empty()):
            print("No inputs")
            return 1
        else:
            self.ai_neurons()
            return 0

    def test_model(self):
        Tk().withdraw()
        image = askopenfilename()
        results = self.model(image)
        results.show()

    def test_ai_vision(self):
        frame = self.wincap.get_frame()
        scored_frame = self.score_frames(frame)
        self.ai_vision(score_results=scored_frame, frame=frame)