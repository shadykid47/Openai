import openai
import pandas as pd
import time
import openpyxl
import os, glob

def ReadExcelFile(filepath):
    try:
        df = pd.read_excel(filepath)
        filename = os.path.split(filepath)[1]
        folderpath = os.path.split(filepath)[0]
        df.to_csv(folderpath + '\Copy_Of_' + filename)
    except:
        df = pd.read_csv(filepath)
        filename = os.path.split(filepath)[1]
        df.to_csv(filepath + '\Copy_Of_' + filename)
    
    return df
  
def GetCompletions(api_key, prompt, question, engine, tokens):
    openai.organization = "org-S3POWFAdvhzHFxU7FLRAMh4g"
    openai.api_key = api_key
    completion = openai.Completion.create(engine=engine, max_tokens=tokens, prompt= str(prompt) + " || " + question)
    response = completion.choices[0].text
    response = str(response)
    return response.strip()

def GetResponseFromOpenAI(api_key, question1, engine, tokens, filename):
    filepath = '/content/drive/MyDrive/' + filename
    messages = ReadExcelFile(filepath)
    print("Number of messages - ", len(messages))
    xfile = openpyxl.load_workbook(filename)
    sheet = xfile.get_sheet_by_name('Sheet1')
    sheet['B1'] = 'OPENAI RESPONSE'

    for m in range(5):
        print("On message number - ", m)
        prompt = messages.iloc[m]['Message']
        prompt = str(prompt)
        print("PROMPT IS - \n", prompt)
        msgcell = 'A'+str(m+2)
        sheet[msgcell] = prompt
        response = GetCompletions(api_key, prompt, question1, engine, tokens)
        print("RESPONSE IS - \n", response)
        responsecell = 'B'+str(m+2)
        sheet[responsecell] = response
        xfile.save(filename)
        print("\n")
        time.sleep(5)



