import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import re

def clean_dataframe (sharks):
    
    sharks_clean = sharks.rename(columns={'Species ': 'Species'})
    sharks_clean = sharks_clean[['Year', 'Age', 'Country', 'Species', 'Type', 'Activity']]
    sharks_clean = sharks_clean.dropna(how='all')
    columns_to_check = ['Age', 'Country', 'Species', 'Type', 'Activity']
    sharks_clean.dropna(subset=columns_to_check, how='all', inplace = True)
    sharks_clean = sharks_clean.reset_index(drop=True)
    
    
    def extract_age(x):
        if pd.isna(x):
            return 'unknown'
        if x == 'teen' or x == 'Teen' or x == 'Teens':
            return '15'
        if x == 'adult' or x == '(adult)' or x == 'middle-aged':
            return '50'
        if x == '18 months':
            return '1'
        age_av = re.findall(r'(\d{1,2})\s*(&|or|to)\s*(\d{1,2})', str(x))
        if age_av:
            average_ages = [(int(match[0]) + int(match[2])) / 2 for match in age_av]
            return str(average_ages[0])
        age_match = re.search(r'\d{1,2}', str(x))
        if age_match:
            return age_match.group()
        return 'unknown'
    
    sharks_clean['Age'] = sharks_clean['Age'].apply(extract_age)
    
    def extract_size_1(x):
        if pd.isna(x):
            return 'unknown'
        x = x.replace(' ', '')
        contains_length = re.search(r'\d', str(x))
        if contains_length:
            contains_metres = re.search(r'\d+m|\sm\s', str(x)) #searches for ' m ' or number followed by 'm'
            contains_feet = re.search(r'\d+\'|\s\'\s', str(x)) # checks for apostrophes to see if it's in ft
            if contains_metres:
                pattern_metters = '(\d+(\.\d+)?)\s?m'
                pattern_metters_original = r'(\d+(\.\d+)?)\s*m\s*.*?m*'
                length_in_metres_string = re.search(pattern_metters, str(x)) #finds first numbers before the first m
                if length_in_metres_string:
                    length_in_metres_final = re.search('(\d+[\.\d+]*)', str(x))#isolates the numbers
                    return float(length_in_metres_final.group())
            elif contains_feet:
                length_in_feet_string = re.search(r'(\d+(\.\d+)?)(?:\s*\'\s*.*?\'*)', str(x)) #finds first numbers before the first'
                if length_in_feet_string:
                    length_in_feet_final = re.search(r'\d+', str(x)) #isolates the numbers
                    return 0.3048*(float(length_in_feet_final.group())) #converting feet to metres
    #now going to insert average length of each species for some of the most commonly ooccuring species
        elif 'white' in x or 'White' in x or 'Great White' in x or 'great white' in x or 'Great white' in x:
            return 4.2 #average length of a great white shark (wikipedia)
        elif 'tiger' in x or 'Tiger' in x:
            return 4.1 #average length of tiger shark (wikipedia)
        elif 'bull' in x or 'Bull' in x:
            return 2.3 #average length of bull shark (wikipedia)
        elif 'Mako' in x or 'mako' in x:
            return 2.8 #average length of mako shark (wikipedia)
        elif 'Bronze Whaler' in x or 'Bronze whaler' in x or 'bronze whaler' in x or 'Copper' in x or 'copper' in x or 'Narrowtooth' in x or 'narrowtooth' in x: #different names for the same species
            return 2 #average length of this type of shark (NIWA)
        elif 'Raggedtooth' in x or 'raggedtooth' in x or 'Gray Nurse' in x or 'gray nurse' in x or 'Gray nurse' in x :
            return 2.4 #average (wikipedia)
        else:
            return 'unknown'
    
    sharks_clean['Shark Size'] = sharks_clean['Species'].apply(extract_size_1)
    
    def activity_simplified(x):
        if pd.isna(x):
            return 'unknown'
        if 'surfing' in x or 'Surfing' in x or 'Boarding' in x or 'boarding' in x or 'Surf' in x or 'surf' in x:
            return 'Surfing'
        if 'spearfishing' in x or 'Spearfishing' in x: #putting this here because I'm gonna put 'fishing' below for 'Boat' so hoping if i specify spearfishing here it won't mess with it
            return 'Swimming'
        if 'Boat' in x or 'boating' in x or 'overboard' in x or 'Overboard' in x or 'Kayak' in x or 'kayak' in x or 'canoe' in x or 'Canoe' in x or 'Fishing' in x or 'fishing' in x:
            return 'Boat'
        else:
            return 'Swimming'
    
    sharks_clean['Simplified activity'] = sharks_clean['Activity'].apply(activity_simplified)
    
    sharks_clean.to_csv('data/sharks clean.csv', index=False)
    
    return