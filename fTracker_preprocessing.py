import converter
import os
import well_stripper


input_path = "/home/antony/projects/roopsali/Habituation/code_tester/120fps/"  # Replace with the path to your input folder
input_image = input_path + "control00000.BMP" # This is your first image, it us used for marking the area of intrest.

# Replace with the path to your output folder
os.chdir(os.path.abspath(os.path.join(input_path, os.pardir)))
os.makedirs(os.path.basename(os.path.normpath(input_path) + '_wells'), exist_ok=True)
output_path =  os.path.join(os.path.join(input_path, os.path.normpath(input_path) + '_wells'))  # Path to your output folder
print(output_path)

ncol = 5
nrow = 4

well_stripper.stripper(input_path, output_path, ncol, nrow)
