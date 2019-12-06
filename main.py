import os, sys, csv
import sqlite3 as sqlite
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
MEASLES_DATA        = 'measles.csv'
OUTPUT_DIR          = 'output'

INCOME_LEVELS       = { 1: 'WB_LI', 2: 'WB_LMI', 3: 'WB_UMI', 4: 'WB_HI' }

INDEX_COUNTRY       = 0
INDEX_INCOME_LEVEL  = 1

MIN_YEAR            = 1980
MAX_YEAR            = 2017

# Strings
YEAR_PROMPT         = 'Enter a year between 1980 & 2017: '
INCOME_PROMPT       = '1 - Low Income\n2 - Lower Middle Income\n3 - Upper Middle Income\n4 - High Income\nEnter one of the above income levels: '

COUNTRY             = 'Country'
WB_IL               = 'World_Bank_Income_Level'

def terminate(msg, error_code=1):
    '''
    Prints a message to the user and then terminates the program
    with the given code, default is 1.
    '''

    print(msg)
    sys.exit(error_code)

def get_info_based_on_year(year, row, total_percentage=None, record_count=None):
    '''
    Returns a tuple containing the percent of country vaccinated, the total percentage
    calculated for all countries and the total number of records that have been counted
    given a specified year (or all) and row in the csv file.

    Returns -1 if this row is invalid.

    A row is invalid if either their is no percentage at the year index or the data
    doesn't make sense.
    '''

    percentage = 0

    # If checking countries average percentage over all years, get the average across
    # all of the columns for that country
    if year == 'all':
        k = 0
        for j in range(2, len(row)):
            if not row[j].isnumeric():
                k += 1
            else:
                percentage += int(row[j])

            if not total_percentage is None or not total_percentage is None:
                total_percentage += 0 if not row[j].isnumeric() else int(row[j])
                record_count += 0 if not row[j].isnumeric() else 1
        
        number_of_years_checked = len(row) - 2 - k

        # Not sure if this can happen but better safe than sorry
        if number_of_years_checked <= 0:
            return -1

        percentage /= number_of_years_checked
    # If checking specific year, get the value at the years index for the country
    else:
        index = 2 + MAX_YEAR - int(year)

        if not row[index].isnumeric():
            return -1, total_percentage, record_count
        else:
            percentage = float(row[index])
        
            if not total_percentage is None or not total_percentage is None:
                total_percentage += 0 if not row[index].isnumeric() else int(row[index])
                record_count += 0 if not row[index].isnumeric() else 1

    return percentage, total_percentage, record_count

class Country:
    ''' 
    Helper class to store the name, income level and percentage
    of a country
    '''

    def __init__(self, name, income_level, percentage=0):
        self.name = name
        self.income_level = income_level
        self.percentage = percentage

if __name__ =='__main__':

    # Attempt to open measles file, terminate program if it cannot be found
    try:
        measles_file = open(MEASLES_DATA, 'r')
    except:
        terminate('Cannot find %s. Program will terminate.' % (MEASLES_DATA))

    # Create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # Get the output file name and add .csv on the end of it unless it is already a .csv
    output_file_dir = input('Enter the name of the output file: ')
    output_file_dir += '.csv' if output_file_dir[-4:] != '.csv' else ''

    full_dir = OUTPUT_DIR + '//' + output_file_dir

    # Open the output file
    with open(full_dir, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        reader = csv.reader(measles_file)

        # Create the first 2 indicies of the file header
        header = [COUNTRY, WB_IL]
        
        # Get desired year from user
        year = input(YEAR_PROMPT)

        # If the user wants all years in the file, add them to the header
        if year.lower() == 'all':
            for i in range(2017, 1979, -1):
                header.append(str(i))
            plot_title = 'Percentage of Countries Vaccinated between 1980 & 2017'
        # Append the year to header
        else:
            header.append(year)
            plot_title = 'Percentage of Countries Vaccinated in %s' % year

        # Get desired income level from user
        income_level = input(INCOME_PROMPT)

        # If the user input for income level is not a valid income level, terminate program
        try:
            if income_level != 'all' and not 0 < int(income_level) < 5:
                terminate('The income level \'%s\' is not valid. Program will terminate.' % income_level)
        except ValueError:
            terminate('The income level \'%s\' is not valid. Program will terminate.' % income_level)
    
        # Write the header to the output file
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
            # Get the countries name, income level based on the row and 
            # set percentage to 0 temporarily
            country = row[INDEX_COUNTRY]
            income = row[INDEX_INCOME_LEVEL]
            percentage = 0
            
            # Skip the header and skip rows that don't match search criteria
            if i == 0 or (income_level != 'all' and row[INDEX_INCOME_LEVEL] != INCOME_LEVELS[int(income_level)]):
                i += 1
                continue

            # If the lowest and highest countries haven't been set, set
            # them based on if the user wants all countries, or one country
            if lowest_country == None or highest_country == None:
                # Get initial percentage
                percentage,_,_ = get_info_based_on_year(year, row)
                if percentage == -1:
                    continue

                lowest_country = Country(country, income, percentage)
                highest_country = Country(country, income, percentage)

            # Setting up data to be written
            info = [country, income]

            # Store the countries percentage, the running percentage and number of records
            # records counted in a tuple for later use
            percentage, total_percentage, record_count = get_info_based_on_year(year, row, total_percentage, record_count)
            if percentage == -1:
                continue

            # Add the percentage to last column of info to be displayed
            info.append(percentage)
            
            # Update smallest and largest country vaccination percentages
            if percentage < lowest_country.percentage:
                lowest_country = Country(country, income, percentage)
            
            if percentage > highest_country.percentage:
                highest_country = Country(country, income, percentage)

            # Write info to file
            writer.writerow(info)

            i += 1
        
        if record_count == 0:
            terminate('Found no countries matching an income level %s in year %s' % (INCOME_LEVELS[int(income_level)], year))

        average_percetange = total_percentage / record_count

        # Print details to user
        print('Total records meeting criteria: %d' % record_count)
        print('Average vaccination percentage: %.1f%%' % average_percetange)
        print('%s has the lowest vaccination percentage with an average of %.1f%%' % (lowest_country.name, lowest_country.percentage))
        print('%s has the highest vaccination percentage with an average of %.1f%%' % (highest_country.name, highest_country.percentage))

    # Close the input file
    measles_file.close()

    # Get data to display in a plot
    vaccinations = pd.read_csv(full_dir, header=0, names=header)
    countries = vaccinations[COUNTRY].values
    percentages = vaccinations[year].values
    y_pos = np.arange(len(countries))

    # Plot setup
    fig, ax = plt.subplots(figsize = (8, 8))
    
    plt.barh(y_pos, percentages)
    plt.yticks(y_pos, countries)
    plt.xlabel('Percent of Country Vaccinated')
    plt.title(plot_title)

    for t in ax.yaxis.get_major_ticks():
        t.label.set_fontsize(6)

    plt.show()
