import createDataset
import os
import glob
import cv2
import random
# the name format of the input files will be (class number)_(image name).jpg
# the name format for the dataset image will be (hash number)-(image name).jpg
# the name format for the dataset label will be (hash number)-(image name).txt
def createMultipleDataset(x=50, duplicates=30):
    # get the path to the input folder
    soure_folder = f"{os.getcwd()}\\input"
    background_folder_size = len(os.listdir(f"{os.getcwd()}\\backgrounds"))
    background_paths = glob.glob(os.path.join(f"{os.getcwd()}\\backgrounds", '*'))
    # interate through all the files in the input folder and create n number of new images with labels
    for _ in range(x):
        # duplicates = random.randint(3, duplicates)
        for n, filename in enumerate(glob.glob(os.path.join(soure_folder, '*'))):
            dup_num = random.randint(1, duplicates)
            # get the name of the image
            image_name = filename.split("\\")[-1]

            class_number = image_name.split("_")[0]

            output_name = image_name.split("_")[1].split(".")[0]

            background = random.randint(0, background_folder_size-1)
            background = background_paths[background]
            background = cv2.imread(background)

            image = cv2.imread(filename)

            rand_num = random.randint(5, 1000)

            hash_num = createDataset.generate_hash_num(image=image, duplicates=n, background=background, class_number=class_number, image_path=filename, rand_num=rand_num)
            image_file_name = "".join(f"{hash_num}-{output_name}.jpg")
            label_file_name = "".join(f"{hash_num}-{output_name}.txt")
            createDataset.duplicate_image(image=image, duplicates=dup_num, background=background, class_number=class_number, label_file_name=label_file_name, image_file_name=image_file_name)
            # print(f"Generated {duplicates} images for {image_name}")

if __name__ == "__main__":
    createMultipleDataset()
    print()