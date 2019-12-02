import sqlite3 as sqlite
import sys
import csv

# Constants
MEASLES_DATA = 'measles.csv'

INCOME_LEVELS = {
    1: 'WB_LI',
    2: 'WB_LMI',
    3: 'WB_UMI',
    4: 'WB_UI'
}

INDEX_COUNTRY = 0
INDEX_INCOME_LEVEL = 1

MIN_YEAR = 1980
MAX_YEAR = 2017

# Strings
YEAR_PROMPT = 'Enter a year between 1980 & 2017: '

INCOME_PROMPT = \
'''1 - Low Income
2 - Lower Middle Income
3 - Upper Middle Income
4 - High Income
Enter one of the above income levels: '''

def terminate(msg, error_code=1):
    print(msg)
    sys.exit(error_code)

if __name__ =='__main__':

    try:
        measles_file = open(MEASLES_DATA, 'r')
    except:
        terminate('Cannot find %s. Program will terminate.' % (MEASLES_DATA))

    output_file_dir = input('Enter the name of the output file: ')
    output_file_dir += '.csv' if output_file_dir[-4:] != '.csv' else ''

    with open(output_file_dir, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        reader = csv.reader(measles_file)

        # Get desired year from user
        year = int(input(YEAR_PROMPT))

        # Get desired income level from user
        income_level = int(input(INCOME_PROMPT))

        # If the user input for income level is not a valid income level, terminate program
        if not 0 < income_level < 5:
            terminate('That income level is not supported. Program will terminate.')
    
        for row in reader:
            if row[INDEX_INCOME_LEVEL] != INCOME_LEVELS[income_level]:
                continue
            
            print('Country: %s |%s: %s' % (row[INDEX_COUNTRY], int(year), row[2 + MAX_YEAR - int(year)]))


    measles_file.close()
    