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

class Country:

    def __init__(self, name, income_level, percentage):
        self.name = name
        self.income_level = income_level
        self.percentage = percentage

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

        # Total number of records that match search criteria
        record_count = 0
        # Total vaccination percentage
        total_percentage = 0
        # Average vaccination percentage of records 
        average_percetange = 0
        # Country with the lowest vaccination percentage
        lowest_country = None
        # Country with the highest vaccination percentage
        highest_country = None

        i = 0
        for row in reader:
            if i == 0 or (income_level != 'all' and row[INDEX_INCOME_LEVEL] != INCOME_LEVELS[int(income_level)]):
                i += 1
                continue

            info = [row[INDEX_COUNTRY], row[INDEX_INCOME_LEVEL]]

            if year == 'all':
                for j in range(2, len(row)):
                    info.append(row[j])
                    total_percentage += 0 if not row[j].isnumeric() else int(row[j])
                    record_count += 1
            else:
                index = 2 + MAX_YEAR - int(year)
                info.append(row[index])
                total_percentage += 0 if not row[index].isnumeric() else int(row[index])
                record_count += 1

            writer.writerow(info)

            i += 1

        average_percetange = total_percentage / record_count

        print('Total records meeting criteria: %d' % record_count)
        print('Average vaccination percentage: %.1f' % average_percetange)
    
    measles_file.close()
    