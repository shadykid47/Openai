import openai
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
# import streamlit as st
# from streamlit_chat import message
import atomic as atom
import pandas as pd
import time, random

engine = 'text-davinci-003'
tokens = 100
api_key = "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"
# openai.api_key = st.secrets['api_key']
temperature = 0.1

emotion_question = '| Is this positive or negative or ambiguous, answer in one word |'
category_question = '| is this a complaint or a feedback or a query or an appreciation or is it ambiguous, answer in one word |'
discipline_question = """'| Calssify this into - 'Generic', 'Follow Up_ Thank U Response', 'Promo', 'Distributor',
       'Collaboration', 'Greetings', 'Transverse', 'Product',
       'Legal Responses', 'Distributorship',
       'Supply', 'Sponsorship', 'Service Availability',
       'Fabelle Availability', 'Service', 'Online Orders', 'Customer',
       'Retailer', 'Salesman', 'Service Related', 'Consumer' |"""
issue_question = '| what is the issue conveyed in this message |'
interaction_question = "|classify this into - 'Complaint', 'Follow Up_ Thank U Response', 'Query', 'Universal', 'Feedback/Suggestion' |"

bot = ChatBot(name='Buddy', logic_adapters=['chatterbot.logic.BestMatch'])

discipline_list = ['Generic', 'Follow Up_ Thank U Response', 'Promo', 'Distributor',
       'Collaboration', 'Greetings', 'Transverse', 'Product',
       'Legal Responses', 'Distributorship',
       'Supply', 'Sponsorship', 'Service Availability',
       'Fabelle Availability', 'Service', 'Online Orders', 'Customer',
       'Retailer', 'Salesman', 'Service Related', 'Consumer' ]

interaction_list = ['Complaint', 'Follow Up_ Thank U Response', 'Query', 'Universal', 'Feedback/Suggestion']

eng_trainer = ChatterBotCorpusTrainer(bot)
eng_trainer.train('chatterbot.corpus.english.greetings', 'chatterbot.corpus.english.conversations', 'chatterbot.corpus.english.psychology', 'chatterbot.corpus.english.emotion', )

filepath = r"C:\Users\shubh\Downloads\generated_responses.csv"
df = pd.read_csv(filepath)
# df.drop(columns='Unnamed:4', inplace=True)
df['Train'] = df['interaction'].astype(str) + ' ' + df['discipline'].astype(str) + ' ' + df['issue'].astype(str) + ' , ' + df['message'].astype(str) + ','
TrainingData = df.Train.to_list()

custom_trainer = ListTrainer(bot)
custom_trainer.train(TrainingData)

exit_conditions = (":q", "quit", "exit")

while True:

    query = input("> ")
    try:
        interaction = atom.GetReasoningCompletions(api_key, query, interaction_question, engine, tokens, temperature)
    except Exception as e :
        print(e)
        time.sleep(0.5)
        
    try:
        discipline = atom.GetReasoningCompletions(api_key, query, discipline_question, engine, tokens, temperature)
    except Exception as e:
        print(e)
        time.sleep(0.5)
    
    chatterbot_query = interaction + ' , ' + discipline
    if query in exit_conditions:

        break

    elif interaction in interaction_list and discipline in discipline_list:

        print(f"🪴 {bot.get_response(chatterbot_query)}")
    
    else:
        response = atom.GetResponse(api_key, query, engine, tokens, temperature)
        print(f"🪴 {response}")



# question = '| Nature of Conversation | Issue | Sentiment Confusion Matrix | Brand | Department | Description |'
# sentiment_question = '| What is the Sentiment Confusion Matrix of this in one word |'
# complaint, query feedback, appreciation

# prompt = 'I would recommend making your sunfeast biscuits a crunchier'
# data_list = []
# filepath1 = r"C:\Users\shubh\Downloads\Simplify Data Dec 22.csv"
# df1 = pd.read_csv(filepath1)
# for l in range(len(df1)):
#     print(l)
#     message = df1.iloc[l]['Message']
#     print(' Message is  -  ',message)
#     str_en = message.encode("ascii", "ignore")
#     str_de = str_en.decode()
#     sentiment = atom.GetReasoningCompletions(api_key, str_de, sentiment_question, engine, tokens, temperature)
#     print(' Sentiment is  -  ' ,sentiment)
#     rand = random.randint(2, 10)
#     time.sleep(rand)
#     category = atom.GetReasoningCompletions(api_key, str_de, category_question, engine, tokens, temperature)
#     print(' Category is  -  ' ,category)
#     rand = random.randint(2, 10)
#     time.sleep(rand)
#     discipline = atom.GetReasoningCompletions(api_key, str_de, discipline_question, engine, tokens, temperature)
#     print(' Discipline is  -  ' ,discipline)
#     rand = random.randint(2, 10)
#     time.sleep(rand)
#     interaction = atom.GetReasoningCompletions(api_key, str_de, interaction_question, engine, tokens, temperature)
#     print(' Interaction is  -  ' ,interaction)
#     rand = random.randint(2, 10)
#     time.sleep(rand)
#     issue = atom.GetReasoningCompletions(api_key, str_de, issue_question, engine, tokens, temperature)
#     print(' Issue is  -  ' ,issue)
#     rand = random.randint(2, 10)
#     time.sleep(rand)
#     data = {'Message': str_de, 'Sentiment': sentiment, 'Category': category, 'Discipline':discipline, 'Interaction':interaction, 'Issue':issue}
#     data_list.append(data)

#     print('\n')

# data = pd.DataFrame(data_list)
# data.to_csv(r'D:\Work\Hiring Assignments\Customer Shastra\DATA.csv')
# response = atom.GetReasoningCompletions(api_key, prompt, question, engine, tokens, temperature)
# print(response)