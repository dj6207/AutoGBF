# from tools.windowCapture import WinCapture
# import cv2 as cv

# capture = WinCapture(window_name="Task Manager")
# while (True):
#     frame = capture.get_frame()
#     cv.imshow("task", frame)
#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break

###########################################################################
# import torch
# model = torch.hub.load('ultralytics/yolov5', 'custom', path="./model/best_dataset1.pt", force_reload = True)
# image = "./dataset/test_images/test2.JPG"
# results = model(image)
# results.show()
###########################################################################
# from ai import Ai
# detect = Ai(browser_name="Parsec")
# detect.test_model()
###########################################################################
import cv2 as cv
import database.dataBase as db
from ai import Ai
db.init_database(".\\database\\data_classes.pickle")
slime = Ai(browser_name="Task Manager", use_model=False)
while (True):
    # slime.test_ai_vision()
    if (slime.run_ai()):
        break
    # if cv.waitKey(1) == ord('q'):
    #     cv.destroyAllWindows()
    #     break
