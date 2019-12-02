import sqlite3 as sqlite
import sys
import csv

# Constants
MEASLES_DATA        = 'measles.csv'

INCOME_LEVELS       = {1: 'WB_LI', 2: 'WB_LMI', 3: 'WB_UMI', 4: 'WB_UI'}

INDEX_COUNTRY       = 0
INDEX_INCOME_LEVEL  = 1

MIN_YEAR = 1980
MAX_YEAR = 2017

# Strings
YEAR_PROMPT     = 'Enter a year between 1980 & 2017: '
INCOME_PROMPT   = '1 - Low Income\n2 - Lower Middle Income\n3 - Upper Middle Income\n4 - High Income\nEnter one of the above income levels: '

COUNTRY         = 'Country'
WB_IL           = 'World_Bank_Income_Level'

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

        header = [COUNTRY, WB_IL]
        
        # Get desired year from user
        year = input(YEAR_PROMPT)

        if year.lower() == 'all':
            for i in range(2017, 1979, -1):
                header.append(i)
        else:
            header.append(year)

        # Get desired income level from user
        income_level = input(INCOME_PROMPT)

        # If the user input for income level is not a valid income level, terminate program
        if income_level != 'all' and not 0 < int(income_level) < 5:
            terminate('That income level is not supported. Program will terminate.')
    
        writer.writerow(header)

        i = 0
        for row in reader:
            if i == 0 or (income_level != 'all' and row[INDEX_INCOME_LEVEL] != INCOME_LEVELS[income_level]):
                i += 1
                continue
            
            info = [row[INDEX_COUNTRY], row[INDEX_INCOME_LEVEL]]

            if year == 'all':
                for j in range(2, len(row)):
                    info.append(row[j])
            else:
                info.append(row[2 + MAX_YEAR - int(year)])

            writer.writerow(info)

            i += 1
    
    measles_file.close()
    