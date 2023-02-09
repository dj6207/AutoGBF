import cv2
import numpy as np

# duplicates images and spread them across the a canvas
def duplicate_image(image, duplicates, background=None, class_number="?", size=(1080, 1920, 3), file_name="labels.txt"):
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
    create_labels(file_name, log, class_number)
    return size, log

def create_labels(file_name, log, class_number):
    with open(file_name, "w") as file:
        for item in log:
            file.write(f"".join(f"{class_number} {str(item[0])} {str(item[1])} {str(item[2])} {str(item[3])}\n"))

if __name__ == '__main__':
    image = cv2.imread("input.jpg")
    n = int(input("Enter the number of duplications: "))
    background_path = input("Enter the path to the custom background image (leave blank for white background): ")
    background = cv2.imread(background_path) if background_path else None
    output_image, log = duplicate_image(image, n, background)
    cv2.imwrite("output.jpg", output_image)
    print("Log of center coordinates and distance from center to each side:")
    for x, y, w, h in log:
        print(f"center: ({x}, {y}), distance from center to each side: ({w}, {h})")
