# Analytical Visualization Project

## Assignment Specifications

The World Health Organization compiles data about immunization levels around the world. The file 'measles.csv' contains data about the level of measels vacinations in various countries over time.
Each line of the file contains the following information.

* Country (50 Characters)
  * Contains the name of the country
* Income Level (6 Characters)
  * Identifies the income category assigned to that country by The World Bank
    * **WB_LI** - Low Income
    * **WB_LMI** - Lower Middle Income
    * **WB_UMI** - Upper Middle Income
    * **WB_HI** - High Income
* Percent Vaccinated (3 Characters)
  * Contains an integer representing the percentage of children in that country who have received the measles vaccine by age one
* Region (25 Characters)
* Year (4 Characters)
  * Contains the year for which the data was compiled

## Part 1: Importing & Querying the Data

1. Program will copy selected lines from 'measles.csv' into a file selected by the user
2. The program will *always* read from 'measles.csv'. If the file cannot be opened, the program will display an error message and then terminate
3. The program will prompt user for the name of the output file. If that file doesn't exist, create it. If it does exist, overrite current contents.
4. The program will prompt the user to enter a year and income level. The income level must be one of the characters in the set {1, 2, 3, 4} where 1 represents **WB_LI** & 4 represents **WB_HI**.

The program will copy all data from 'measles.csv' selected by the users input. A column is selected if the users response matches the Year field. A row (country) is selected if the income level matches. All data (in either/both rows and columns) are selected if the users reponse is 'all' or 'ALL'.

5. The output file created by the program will have the same format as the input file. Note that when the user selects all lines, the output file will be identical to the input file
6. The program will identify all records in the input file which match the users criteria for year and income level, and the program will display a report with the following information to console

* The count of records in the input file that match the users criteria
* The average percentage for those records to one decimal place
* The country with the lowest percentage for those records
* The country with the highest percentage for those records
* The name of the country and the percent of children vaccinated will be displayed for the last two items

7. The program will display appropriate message to inform the user about any errors

## Part 2: Visualization

Use a toolkit to graph the data. Save and include a good quality view of the image; include it in part 3.

## Part 3: Reflection Essay

1. Discuss what was learned and compare and contrast the kinds of questions that can be asked and answered by the data queries vs the visualization.
2. Explore an ethical issue introducted by the data and explained by the data.

Each part should be between 750 - 1000 words and using APA format for in-text citations and references.



## Learning Goals

1. Understanding how to process CSV file information
2. Practice using an external toolkit to support major functionality (i.e visualization)
3. Understand the realtionship between methods for processing real world data and the kinds of conclusions that can be drawn