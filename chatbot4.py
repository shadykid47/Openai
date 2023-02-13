import openai
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
# import streamlit as st
# from streamlit_chat import message
import atomic as atom
import pandas as pd
import time, random
from flask import Flask, request, render_template

engine = 'text-davinci-003'
tokens = 100
api_key = "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"
# openai.api_key = st.secrets['api_key']
temperature = 0.1

bot = ChatBot(name='Buddy', logic_adapters=['chatterbot.logic.BestMatch'])

# eng_trainer = ChatterBotCorpusTrainer(bot)
# eng_trainer.train('chatterbot.corpus.english.greetings', 'chatterbot.corpus.english.conversations', 'chatterbot.corpus.english.psychology', 'chatterbot.corpus.english.emotion', )

# custom_trainer = ListTrainer(bot)

# training_data = pd.read_csv(r"D:\Work\Hiring Assignments\Customer Shastra\Cleaned Data.csv")

# training_data['Message'] = training_data['From'] + ' : ' + training_data['Message']
# training_data['Work Message'] = 'Bot : ' + training_data['Work Message'] 

# training_data.drop(columns=['Unnamed: 0', 'Sentiment', 'Channel Name', 'From'])

# # custom_trainer.train(training_data['Message'].to_list())
# # custom_trainer.train(training_data['Work Message'].to_list())

# for i in range(len(training_data)):
#     message = training_data.iloc[i]['Message']
#     response = training_data.iloc[i]['Work Message']
#     custom_trainer.train([message, response])
#     time.sleep(.5)

exit_conditions = (":q", "quit", "exit")

while True:

    query = input("> ")
    
    if query in exit_conditions:

        break

    else :

        print(f"🪴 {bot.get_response(query)}")


# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/get_response", methods=["POST"])
# def get_response():
#     user_input = request.form["user_input"]
#     response = generate_response(model, user_input)
#     return response


# if __name__ == "__main__":
#     app.run(debug=True)
    