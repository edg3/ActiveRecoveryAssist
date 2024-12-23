# Retrieved by copilot on Bing, prompt: python connect to azure database
import pyodbc

# When model is setup use: git update-index --skip-worktree
# only THEN can put these details in, don't broadcast it to the world
print('Connecting to Azure SQL Database...')
server = 'edg3.database.windows.net'
database = 'ActiveRecoveryAssist'
username = 'Hackathon'
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER=tcp:{server},1433;DATABASE={database};UID={username};PWD={password};Encrypted=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Connect
conn = pyodbc.connect(connection_string)
print('Connected to Azure SQL Database')

# Organise model we will use
import os
import torch
MODEL_NAME = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
os.environ['CUDA_VISIBLE_DEVICES'] ='0'
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Using device:',device)

# Load the model
from transformers import AutoTokenizer, AutoModelForCausalLM

print('Loading model...')
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
print('Model loaded')

# Get 1 question row
import time
print('Listening for questions...')
while True: # TODO: consider a better way to handle this
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 [QuestionID],[Device],[Text],[Answer] FROM [dbo].[Question] WHERE Answer IS NULL OR Answer = '';")
    for row in cursor.fetchall():
        print('Received question:',row)
        input_text = row[2]
        input_ids = tokenizer(input_text, return_tensors='pt').input_ids.to(device)
        generated_ids = model.generate(input_ids, max_length=1024)
        generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        print('Generated answer:',generated_text)
        cursor.close()
        cursor = conn.cursor()
        cursor.execute("UPDATE [dbo].[Question] SET Answer = ? WHERE QuestionID = ?",generated_text,row[0])
        conn.commit()
        print('Saved response')
        print('---')
    cursor.close()
    time.sleep(30)

# Close connection
conn.close()