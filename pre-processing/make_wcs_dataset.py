
import csv
import os
from PIL import Image
root_directory = "../"
# dataset
dataset_path = root_directory + "wcs/"
# CSV
csv_directory = dataset_path + "compared_color_IR_wcs.csv"

# step 1
color_dataset_path = dataset_path+"color_dataset" + "/"
infrared_dataset_path = dataset_path+"infrared_dataset" + "/"

color_dataset_train_path = color_dataset_path+"train"+ "/"
color_dataset_test_path = color_dataset_path+"test"+ "/"
infrared_dataset_train_path = infrared_dataset_path+"train"+ "/"
infrared_dataset_test_path = infrared_dataset_path+"test"+ "/"

file_list = [dataset_path, color_dataset_path,infrared_dataset_path,color_dataset_train_path,color_dataset_test_path,infrared_dataset_train_path,infrared_dataset_test_path]

step1_completed = False
if step1_completed == False:
    for x in file_list:
        print(x)
        if not os.path.isdir(x):
            os.makedirs(x)

# step 2
train_category_num = 28
test_category_num = 11
train_category = []
test_category = []

exclude_list = ['unidentifiable', 'unidentified', 'start', 'groupe']
include_list = ['nasua narica', 'phacochoerus africanus']

with open(csv_directory) as f:
    temp_reader = csv.reader(f)
    reader = [row for row in temp_reader]

    del reader[0:4]

    for i in range(len(reader)):
        if reader[i][0] in exclude_list or 'unknown' in reader[i][0]:
            continue
        if (int(reader[i][1])>=500 and int(reader[i][2])>=500) or reader[i][0] in include_list:
            train_category.append(reader[i][0])

    test_category_info = []
    for i in range(len(reader)):
        if reader[i][0] in exclude_list or 'unknown' in reader[i][0] or reader[i][0] in train_category:
            continue
        if (int(reader[i][1])>=100 and int(reader[i][2])>=100) or reader[i][0] in include_list:
            test_category_info.append(reader[i])
            test_category.append(reader[i][0])

    for category in train_category:
        for i in range(len(test_category)):
            if test_category[i] == category:
                test_category.pop(i)
                test_category_info.pop(i)

    for i in range(len(test_category_info)):
        test_category_info[i].append(int(min(int(test_category_info[i][1]),int(test_category_info[i][2]))))
    sorted_list = sorted(test_category_info, key=lambda x: x[3], reverse=True)
    
    test_category.clear()

    for i in range(test_category_num):
        test_category.append(sorted_list[i][0])

# step 3, 4
def isImage_gray(image):
    mode = image.mode
    if(mode == "L"):
        print("grey1")
        return True

    size = image.size

    if mode == "RGBA":
        if(len(set(image.getpixel((0, 0))))==2):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==2):
                if(len(set(image.getpixel((size[0]//4, size[1]//4))))==2):
                    if(len(set(image.getpixel((size[0]//4*3, size[1]//4*3))))==2):
                        print("gray2")
                        return True

    elif mode == "RGB":
        if(len(set(image.getpixel((0, 0))))==1):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==1):
                if(len(set(image.getpixel((size[0]//4, size[1]//4))))==1):
                    if(len(set(image.getpixel((size[0]//4*3, size[1]//4*3))))==1):
                        print("gray3")
                        return True
    else:
        print("othermode:", print(mode))
        return False
    print("aaa")
    return False

def isNotImage_gray(image):
    mode = image.mode
    if(mode == "L"):
        print("grey1")
        return False

    size = image.size

    if mode == "RGBA":
        if(len(set(image.getpixel((0, 0))))==2):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==2):
                if(len(set(image.getpixel((size[0]//4, size[1]//4))))==2):
                    if(len(set(image.getpixel((size[0]//4*3, size[1]//4*3))))==2):
                        print("gray2")
                        return False
    elif mode == "RGB":
        if(len(set(image.getpixel((0, 0))))==1):
            if(len(set(image.getpixel((size[0]//2, size[1]//2))))==1):
                if(len(set(image.getpixel((size[0]//4, size[1]//4))))==1):
                    if(len(set(image.getpixel((size[0]//4*3, size[1]//4*3))))==1):
                        print("gray3")
                        return False
    else:
        print("othermode:", print(mode))
        return False
    return True

def save_image_to_category_folder(image,new_folder_path, new_filename_path):

    if not os.path.isdir(new_folder_path):
        print("mkcategorydir:",new_folder_path)
        os.makedirs(new_folder_path)

    image.save(new_filename_path)

train_category_image_num = 500
test_category_image_num = 100
color_category_path = dataset_path + "color_bboxes/"
infrared_category_path = dataset_path + "infrared_bboxes/"

min_image_size = 50

# step 3
step3_completed = False
if step3_completed == False:

    print('train_category_num: ', train_category_num)
    print('train_categroy length: ', len(train_category))
    for i in range(train_category_num):
        category_name = train_category[i]
        folderpath_color_category= color_category_path + category_name + "/"
        folderpath_infrared_category= infrared_category_path + category_name + "/"
        filenames_color = [f.path for f in os.scandir(folderpath_color_category)]
        filenames_infrared = [f.path for f in os.scandir(folderpath_infrared_category)]
        num_completed = 0

        for filename in filenames_color:
            try:
                im = Image.open(filename)
                print(filename)

                img_name = filename.replace(folderpath_color_category,"")
                size = im.size
                if size[0]>min_image_size and size[1]>min_image_size:
                    if isNotImage_gray(im):
                        new_folder_path = color_dataset_train_path + category_name + "/"
                        new_filename_path = new_folder_path + img_name
                        print("new_color_folder_path", new_folder_path)
                        print("new_color_filename_path", new_filename_path)
                        save_image_to_category_folder(im, new_folder_path, new_filename_path)
                        num_completed += 1

            except Exception as e:
                print("Error:", e)

            if num_completed >= train_category_image_num:
                break

        num_completed = 0
        for filename in filenames_infrared:
            try:
                im = Image.open(filename)
                print(filename)

                img_name = filename.replace(folderpath_infrared_category,"")
                print(img_name)
                print(category_name)
                size = im.size
                if size[0]>min_image_size and size[1]>min_image_size:
                    if isImage_gray(im):
                        print("yes!")
                        new_folder_path = infrared_dataset_train_path + category_name + "/"
                        new_filename_path = new_folder_path + img_name
                        print("new_infrared_folder_path: ", new_folder_path)
                        print("new_infrared_filename_path: ", new_filename_path)
                        save_image_to_category_folder(im, new_folder_path, new_filename_path)
                        num_completed += 1
            except Exception as e:
                print("Error:", e)
            if num_completed >= train_category_image_num:
                break

# step 4
step4_completed = False
if step4_completed == False:
    for i in range(test_category_num):
        category_name = test_category[i]
        folderpath_color_category= color_category_path + category_name + "/"
        folderpath_infrared_category= infrared_category_path + category_name + "/"
        filenames_color = [f.path for f in os.scandir(folderpath_color_category)]
        filenames_infrared = [f.path for f in os.scandir(folderpath_infrared_category)]

        num_completed = 0

        for filename in filenames_color:
            try:
                im = Image.open(filename)
                print(filename)
                img_name = filename.replace(folderpath_color_category,"")
                size = im.size
                if size[0]>min_image_size and size[1]>min_image_size:
                    if isNotImage_gray(im):
                        new_folder_path = color_dataset_test_path + category_name + "/"
                        new_filename_path = new_folder_path + img_name
                        print("new_color_folder_path", new_folder_path)
                        print("new_color_filename_path", new_filename_path)
                        save_image_to_category_folder(im, new_folder_path, new_filename_path)
                        num_completed += 1

            except Exception as e:
                print("Error:", e)

            if num_completed >= test_category_image_num:
                break

        num_completed = 0
        for filename in filenames_infrared:
            try:
                im = Image.open(filename)
                print(filename)
                img_name = filename.replace(folderpath_infrared_category,"")
                print(img_name)
                print(category_name)
                size = im.size
                if size[0]>min_image_size and size[1]>min_image_size:
                    if isImage_gray(im):
                        print("yes!")
                        new_folder_path = infrared_dataset_test_path + category_name + "/"
                        new_filename_path = new_folder_path + img_name
                        print("new_infrared_folder_path", new_folder_path)
                        print("new_infrared_filename_path", new_filename_path)
                        save_image_to_category_folder(im, new_folder_path, new_filename_path)
                        num_completed += 1

            except Exception as e:
                print("Error:", e)
            if num_completed >= test_category_image_num:
                break
print('finished making wcs dataset')