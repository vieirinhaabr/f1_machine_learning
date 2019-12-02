import pandas as pd

"""def get_table(page, table_class, what_you_want):
    
    race_tb = wikitables[1]
    race_tb = race_tb.drop(columns=['Laps', 'Grid', 'Points', 'Time/Retired'])

    try:
        if what_you_want is 'gp':
            wikitables = pd.read_html(page, index_col=0, header=0, attrs={"class": table_class})
            race_tb = wikitables[1]
            race_tb = race_tb.drop(columns=['Laps', 'Grid', 'Points', 'Time/Retired'])
            
            return race_tb
        elif what_you_want is 'cl':
            wikitables = pd.read_html(page, index_col=0, header=1, attrs={"class": table_class})
            classification_tb = wikitables[0]
            classification_tb = classification_tb.drop(columns=['Q1', 'Q2'])
        
            return classification_tb
    except ValueError:
        print('Pass what you want as `gp` (grand prix table) or `cl` (classification table)')"""

wikitables = pd.read_html('https://en.wikipedia.org/wiki/2019_Abu_Dhabi_Grand_Prix', header=1, attrs={"class": 'wikitable sortable'})

classification_tb = wikitables[0]
classification_tb = classification_tb.drop(columns=['Q1', 'Q2'])
