import os

#path for data files
input_path = os.getcwd() + '/data'
output_path = os.getcwd() + '/output'

col_name = {
    'year': 'Year',
    'per_female': 'Female Percentage',
    'per_male': 'Male Percentage',
    'top_names_female': 'Female Top Names',
    'top_names_male': 'Male Top Names'}


def make_output_dir():
    """ Create folder to place output file        """

    #check if folder exist otherwise create folder    
    if not os.path.isdir(os.getcwd() + '/output'):
        os.makedirs(os.getcwd() + '/output')