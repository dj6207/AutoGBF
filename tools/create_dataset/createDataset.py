import cv2
import numpy as np

# duplicates images and spread them across the a canvas
# image: the image to be duplicated path to the image that will be duplicated
# duplicates: the number of times the image will be duplicated
# background: the background image path to the background image
# class_number: the class number corresponding to the image
# size: the size of the canvas
# file_name: the name of the label file
def duplicate_image(image, duplicates, background=None, class_number="?", size=(1080, 1920, 3), label_file_name="labels.txt", image_file_name="output.jpg"):
    occupied = []
    log = []
    h, w, _ = image.shape
    size = np.zeros(size, dtype=np.uint8)

    # adds a background if one is given, otherwise background is black
    if background is not None:
        b_h, b_w, _ = background.shape
        size[:b_h, :b_w, :] = background
    # for each duplicated image it will be resized and placed randomly on the canvas
    for _ in range(duplicates):
        # the image will be resized to a random size between 50% and 200% of the original size
        factor = np.random.uniform(0.5, 2)
        new_h, new_w = int(h * factor), int(w * factor)
        new_image = cv2.resize(image, (new_w, new_h), cv2.INTER_CUBIC)
        # makes sure that the image does not overlap with any other image
        while True:
            x = np.random.randint(0, size.shape[1] - new_w)
            y = np.random.randint(0, size.shape[0] - new_h)
            if not any([x < item[0]+item[2] and x+new_w > item[0] and y < item[1]+item[3] and y+new_h > item[1] for item in occupied]):
                occupied.append((x, y, new_w, new_h))
                break
        # add the duplicated image to the canvas
        size[y:y+new_h, x:x+new_w, :] = new_image
        # logs the center coordinates and distance from center to each side of the duplicated image
        log.append([(x + new_w // 2) / size.shape[1], (y + new_h // 2) / size.shape[0], new_w / size.shape[1], new_h / size.shape[0]])
    # creates a label file for the duplicated images
    # label_file_name = "".join(f"{hash_number}-{label_file_name}")
    create_labels("".join(f".\\dataset\\labels\\{label_file_name}"), log, class_number)
    # image_file_name = "".join(f"{hash_number}-{image_file_name}")
    cv2.imwrite("".join(f".\\dataset\\images\\{image_file_name}"), size)
    # return size, log    
    return log

def create_labels(label_file_name, log, class_number):
    with open(label_file_name, "w") as file:
        for item in log:
            file.write(f"".join(f"{class_number} {str(item[0])} {str(item[1])} {str(item[2])} {str(item[3])}\n"))

def generate_hash_num(image, duplicates, background=None, class_number="?", image_path="", background_path="", rand_num=0):
    hash_num = hash(f"{class_number}{duplicates}{image}{image_path}{background}{background_path}{rand_num}")
    return abs(hash_num)

if __name__ == '__main__':
    # image to duplicate
    image_path = input("Enter the path to the image to be duplicated (leave blank for input.jpg): ")
    image = cv2.imread(image_path) if image_path else cv2.imread("input.jpg")
    # number of images to duplicate
    n = int(input("Enter the number of duplications greater than 0 and less than 50: "))
    # set a custom background image
    background_path = input("Enter the path to the custom background image (leave blank for white background): ")
    background = cv2.imread(background_path) if background_path else None

    hash_num = hash(f"{n}{image}{image_path}{background}{background_path}")
    print(hash_num)
    # create the duplicated images and return the log
    log = duplicate_image(image, n, background, hash_number=hash_num)
    # output_image, log = duplicate_image(image, n, background)
    # cv2.imwrite("output.jpg", output_image)
    print("Log of center coordinates and distance from center to each side:")
    for x, y, w, h in log:
        print(f"center: ({x}, {y}), distance from center to each side: ({w}, {h})")
