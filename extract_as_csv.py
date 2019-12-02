import pandas as pd

"""class extract_as_csv(object):
        def get_table(page, table_class, table_type=True):
            if table_type is True:
                #race
            else:
                #classification"
            """

ht_table = pd.read_html('https://www.statsf1.com/en/2019/abou-dhabi/grille.aspx', attrs={"class": 'GPgridline'})

print(ht_table)

i = 0
start_grid = []

while i < 20:
    start_grid.append(i)
    i = i + 1

print(start_grid)


"""test = ht_table[0]
string = str(test[0])

print(string)"""
