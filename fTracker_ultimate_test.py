# Copyright (c) 2024 Antony Kiran K David
import os
import cv2
import numpy as np
import pandas as pd
import fTracker_functions_test as ft
import tools
import fish_picker
import converter

# global columns
def add_row(data_list, columns):
    global df
    new_row = pd.DataFrame(data_list, columns=columns)
    df = pd.concat([df, new_row], ignore_index=True)

# To subtract the background of the fish using the MOG2 algorithm; MOG2 is a background subtractor algorithm
# video_folder = '/home/antony/projects/habituation_saunri/test 001_27-02-2024/control 20_wells/'
video_folder = '/home/antony/projects/roopsali/Habituation/code_tester/1_wells/'
video_name = '0_1.avi'

# Function to read images from the folder
def read_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
    return images

def lessgoo(video_folder, video_name, parent_folder):

    # masterCSV = pd.read_csv(parent_folder + video_name[:-4] + '_stim_data.csv')
    input_video_link = video_folder + video_name

    output_video_link = video_folder + 'motion_selected_' + video_name

    threshold = 100 #Threshold for the MOG2 algorithm
    fps = 120
    head_radius = 9
    number_of_points = 10
    hunter_radius = 7
    sweep_angle = 60 #sweeps this angle on either side. ie. total sweep is 2x

    fish_picker.picker(input_video_link, output_video_link, fps, threshold)
    converter.mp4_to_bmp(video_folder, 'motion_selected_' + video_name) # To save the MOG2 processed video into a BMP image series

    series = os.listdir(video_folder + 'motion_selected_' + video_name[:-4])
    series = sorted(series, key=tools.extract_number)
    flag = 0
    image_stack = read_images_from_folder(input_video_link[:-4])
    # Compute the maximum intensity projection
    max_intensity_projection = np.max(np.array(image_stack), axis=0)

    # cv2.imshow("MIP", max_intensity_projection)
    # cv2.waitKey(0)

    background_sub_img_path = video_folder + 'motion_selected_' + video_name[:-4]
    original_img_path = video_folder + video_name[:-4]
    fish_skeleton_path = video_folder + 'skeletonised_' + video_name[:-4]
    extra_image_path = video_folder + 'extra_' + video_name[:-4]
    tracked_fish_skeleton_path = video_folder + 'tracked_skeleton_' + video_name[:-4]
    convolved_image_path = video_folder + 'convolved_skeleton_' + video_name[:-4]

    os.makedirs(fish_skeleton_path,exist_ok=True)
    os.makedirs(extra_image_path,exist_ok=True) # This is an extra folder incase we need it for testing somthing or needs special kinds of output
    os.makedirs(tracked_fish_skeleton_path,exist_ok=True)
    os.makedirs(convolved_image_path, exist_ok=True)

    # global cloumns
    columns = ['Frame', 'Centroid_status', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y'] + [f'P{i}_{c}' for i in range(1, number_of_points) for c in ['x', 'y']]
    df = pd.DataFrame(columns=columns)
    dataframe_path = video_folder

    # print('Skeletonised image saved. \nTracking begins...')

    for filename in series:
        if filename.endswith('.bmp'):
            # print(filename)
            # head_x, head_y = 'no_fish', 'no_fish'
            background_sub_image = os.path.join(background_sub_img_path, filename)
            original_image = os.path.join(original_img_path, filename)
            skeleton_image = os.path.join(fish_skeleton_path, filename)
            extra_image = os.path.join(extra_image_path, filename)
            tracked_fish_image = os.path.join(tracked_fish_skeleton_path, filename)
            convolved_image = os.path.join(convolved_image_path, filename)

            image_original = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
            image_subtracted = cv2.imread(background_sub_image, cv2.IMREAD_GRAYSCALE)
            image_diff_mip = cv2.absdiff(max_intensity_projection, image_original)

            disk_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            image_convolved = cv2.filter2D(image_diff_mip, -1, disk_kernel)
            cv2.imwrite(convolved_image, image_convolved)
            cv2.imwrite(extra_image, image_diff_mip)

            #
            # cv2.imshow("Difference", image_diff_mip)
            # cv2.waitKey(0)
            # Determine the MIP along the desired axis (for example, Z-axis)
            # mip_original = np.max(image, axis=2)

            # centroid_corr_radius = 10
            cv2.imwrite(extra_image, image_diff_mip)
            image_extra = cv2.imread(extra_image, cv2.IMREAD_GRAYSCALE)
            if cv2.integral(image_subtracted)[-1, -1] > 1000:
                # Threshold the convolved image to create a binary image
                _, binary_image_conv = cv2.threshold(image_convolved, 200, 255, cv2.THRESH_BINARY)

                # # Display the binary image
                # cv2.imshow('Binary Image', binary_image_conv)
                # cv2.waitKey(0)

                # Find contours in the binary image
                contours, _ = cv2.findContours(binary_image_conv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Find the centroid of the largest contour (assuming the head is the largest connected component)
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    M = cv2.moments(largest_contour)
                    centroid_x = int(M["m10"] / M["m00"])
                    centroid_y = int(M["m01"] / M["m00"])
                    centroid = (centroid_x, centroid_y)
                else:
                    centroid_x, centroid_y = 'no_fish', 'no_fish'
            else:
                centroid_x, centroid_y = 'no_fish', 'no_fish'

            # if cv2.integral(image_subtracted)[-1, -1] > 1000:
            #     centroid_x, centroid_y = ft.find_centroid(background_sub_image, cutoff=1000)  # find centroid
            # else:
            #     centroid_x, centroid_y = 'no_fish', 'no_fish'

            # Find the head point

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(image_convolved)
            if centroid_y != 'no_fish':
                # head_x, head_y = max_loc
                head_x, head_y = ft.head_finder(int(centroid_x), int(centroid_y), head_radius, convolved_image)
            else:
                head_x, head_y = 'no_fish', 'no_fish'

            # Image operations
            # ----------------------------------------------------------------
            _, binary_image = cv2.threshold(image_convolved, 100, 255, cv2.THRESH_BINARY)


            # print(thresh)

            # cv2.imwrite(output_path3, binary_image)

            # Define a kernel (structuring element) for morphological operations
            kernel_size = 1
            kernel = np.ones((kernel_size, kernel_size), np.uint8)

            # Perform morphological closing
            closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
            # cv2.imwrite(output_path4, closed_image)

            # Apply skeletonization
            skeleton = cv2.ximgproc.thinning(closed_image)
            cv2.imwrite(skeleton_image, skeleton)

            marked_image = cv2.cvtColor(image_original, cv2.COLOR_GRAY2BGR)

            # The fish hunting begins................

            points_x, points_y = ft.fish_hunter(hunter_radius, sweep_angle, skeleton_image, head_x, head_y, centroid_x, centroid_y, number_of_points)

            # columns = ['Frame', 'Centroid_x', 'Centroid_y', 'Head_x', 'Head_y'] + [f'P{i}_x' for i in range(1, number_of_points)] + [
            #     f'P{i}_y' for i in range(1, number_of_points)]
            new_row_data = pd.DataFrame([['no_fish'] * (len(columns))], columns=columns)
            new_row_data.iloc[0, 0] = filename

            if centroid_x != 'no_fish':
                new_row_data.loc[0] = [filename, 1, centroid_x, centroid_y, head_x, head_y] + points_x[:number_of_points - 1] + points_y[:number_of_points - 1]
                # add_row(new_row_data.iloc[0], columns)
                df = pd.concat([df, new_row_data], ignore_index=True)
                # print(new_row_data)
                # print('There is fish in this frame...yaay!')

                cv2.circle(marked_image, (int(centroid_x), int(centroid_y)), 1, (0, 0, 255), -1)
                if head_x != 'no_fish':
                    cv2.circle(marked_image, (int(head_x), int(head_y)), 1, (0, 255, 0), -1)
                for i in range(1, min(len(points_x), number_of_points)):
                    if points_x[i] != 'no_fish':
                        cv2.circle(marked_image, (int(points_x[i]), int(points_y[i])), 1, (255, 0, 0), -1)

            # add_row(new_row_data, columns)
            df = pd.concat([df, new_row_data], ignore_index=True)
            cv2.imwrite(tracked_fish_image, marked_image)
    # print(df)
    df.to_csv(video_folder + video_name[:-4] + '.csv', index=False)
    cv2.destroyAllWindows()
    # print(flag)
    # print("Images processed and saved in the output folder.")

# lessgoo(video_folder, video_name)