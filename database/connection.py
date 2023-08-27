import pyodbc

SERVER = ''
DATABASE = ''
USERNAME = ''
PASSWORD = ''
connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
cnxn = pyodbc.connect(connectionString)