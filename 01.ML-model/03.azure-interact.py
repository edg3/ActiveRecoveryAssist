# Retrieved by copilot on Bing, prompt: python connect to azure database
import pyodbc

# When model is setup use: git update-index --skip-worktree
# only THEN can put these details in, don't broadcast it to the world
server = '<your_server>.database.windows.net'
database = '<your_database>'
username = '<your_username>'
password = '<your_password>'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

# Connect
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Get 1 question row
while True: # TODO: consider a better way to handle this
    cursor.execute("SELECT TOP 1 * FROM [dbo].[Question] WHERE Answer IS NULL OR Answer = '';")
    for row in cursor.fetchall():
        print(row)
        # TODO: send query to ML model
        # TODO: send update answer text to Azure row as update

# Close connection
cursor.close()
conn.close()