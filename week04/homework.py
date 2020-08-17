import pandas as pd
import numpy as np

data = {
    'id':[600, 700, None, 900, 1000, 1100, None, 1200, 1300, 1400, 1500, 1600, None],
    'age':[35, 34, 33, 32, None, 30, 29, 28, 27, 26, None, 40, 99]
}
table1 = {
    'id':[600, 700, None, 900, 1000, 1100, None, 1200, 700, 1400, 10, 900, None],
    'age':[35, 34, 33, 32, None, 30, 29, 28, 27, 26, None, 40, 99],
    'order_id':[10001, 10002, 10003, 10001, 10005, 10006, 10001, 10008, 10009, 10010, 10011, 10010, 10013]
}    

table2 ={
    'id':[650, 700, None, 900, 1050, 1100, None, 1200, 750, 1400, 1550, 900, None],
    'age':[35, 34, 37, 32, None, 30, 29, 28, 37, 26, None, 40, 59],
    'order_id':[10001, 10012, 10003, 10001, 10015, 10006, 10001, 10011, 10009, 10010, 10011, 10020, 10013]
}

df = pd.DataFrame(data)
df1 = pd.DataFrame(table1)
df2 = pd.DataFrame(table2)

# print('\n','*'*55,'\n')

# SELECT * FROM data;
print(df)

# SELECT * FROM data LIMIT 10;
print(df.head(10))

# SELECT id FROM data;
print(df['id'])

# SELECT COUNT(id) FROM data;
# print(df.id.count)
print(df['id'].count)

# SELECT * FROM data WHERE id<1000 AND age>30;
print (df[(df['id']<1000) & (df['age']>30)])

# SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
print(df1.groupby(by=['id']).agg({"order_id": pd.Series.nunique}))

# SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
df3 = pd.merge(df1, df2, left_on = 'id', right_on = 'id', how = 'inner')
df3

# SELECT * FROM table1 UNION SELECT * FROM table2;
df4 = pd.concat([df1, df2], axis = 0)
df4

# DELETE FROM table1 WHERE id=10;
df1[~df1['id'].isin([10])]

# ALTER TABLE table1 DROP COLUMN column_name;
df1.drop(columns=['age'])






