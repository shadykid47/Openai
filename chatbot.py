import openai
import streamlit as st
from streamlit_chat import message
import atomic as atom

api_key = openai.api_key = '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'
engine = 'text-davinci-003'

temperature = 0.5


question1 = 'Classify this sentence into Greeting or Query or Complaint, and give the response in only one word.'
question = 'Generate a response that a chat bot will give.'


prompt = "I am unable to find the Sunfeast Mom's Magic Biscuits in my area."
tokens = round(len(prompt)*1.5)
response = atom.GetReasoningCompletions(api_key, prompt, question, engine, tokens, temperature)
print(response)

# First message should be 'Hello, how may i help you ?
# Then classify the user input and 