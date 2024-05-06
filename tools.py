import pandas as pd

# To write a list into a file
def write_list_to_file(lst, filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write(str(item) + '\n')

# To add a new row to existing data frame in pandas
def add_row(data_list, columns):
    # global df
    new_row = pd.DataFrame([data_list], columns=columns)
    df = pd.concat([df, new_row], ignore_index=True)


# To extract number from file names of images in the folder for individual wells
def extract_number(square):
    return int(square.split('_')[1].split('.')[0])

def extract_number_org(square):
    return int(square.split('l')[1].split('.')[0])