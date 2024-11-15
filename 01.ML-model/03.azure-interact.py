# Retrieved by copilot on Bing, prompt: python connect to azure database
import pyodbc

# When model is setup use: git update-index --skip-worktree
# only THEN can put these details in, don't broadcast it to the world
server = '.database.windows.net'
database = 'ActiveRecoveryAssist'
username = ''
password = ""
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER=tcp:{server},1433;DATABASE={database};UID={username};PWD={password};Encrypted=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Connect
conn = pyodbc.connect(connection_string)

# Organise model we will use
import os
import torch
MODEL_NAME = 'Qwen/Qwen2.5-1.5B-Instruct'
os.environ['CUDA_VISIBLE_DEVICES'] ='0'
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Load the model
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)

# Get 1 question row
import time
while True: # TODO: consider a better way to handle this
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT TOP 1 [QuestionID],[Device],[Text],[Answer] FROM [dbo].[Question] WHERE Answer = '';")
        for row in cursor.fetchall():
            print('Received question:',row)
            input_text = row[2]
            input_ids = tokenizer(input_text, return_tensors='pt').input_ids.to(device)
            generated_ids = model.generate(input_ids, max_length=1024)
            generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            print('Generated answer:',generated_text)
            cursor.execute("UPDATE [dbo].[Question] SET Answer = ? WHERE QuestionID = ?",generated_text,row[0])
            conn.commit()
    except e:
        print('Error:',e)
    finally:
        print('Saved response')
    cursor.close()
    time.sleep(30)

# Close connection
conn.close()