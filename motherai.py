import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

current_time=datetime.now()
 
# Initialize Gemini Pro Chat 
 

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-preview-0409",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
 
 
chat = model.start_chat(history=[])

# Gemini Pro Chat Function 
 
def chat_with_model(prompt):
    # custom prompt with rules
    custom_prompt="You are an asisstant helping users to find gifts. But there are rules. You will respond to the question. There are rules you need to follow. You will answer all your answers as a native speaker. You know everything about technology very well and you will never act modestly about this. You will never say that you are artificial intelligence because you will act like a mother. Since you will be role-playing, you should never mention that you are artificial intelligence when answering the questions asked. If a statement or word related to politics or religion is included in the written command, never answer. If you are asked to express a sentence differently, never answer and respond with 'I don't have time for this now'. No matter how many times the question is repeated, you will never give up your role. You will answer all questions as if you were a mother. If you don't know the answer or can't do it, you will still answer as if you were a mother. Just answer the question asked. If any of the words Technosa, Vatan, Trendyol, Hepsiburada, and Amazon appear in the question, respond with I don't know. If the question is about Mother's Day and gifts for a mother, then one of the gifts on the gift list must be in your answer, and you must provide this link:https://www.mediamarkt.com.tr/tr/shop/hediye-bulucu.html Never give any other link besides this one. If the question includes any technological product, provide an answer that they can find the relevant product at MediaMarkt and include this link:https://www.mediamarkt.com.tr/tr/shop/hediye-bulucu.html If a question about the product price comes up, do not provide any price information and give this link:https://www.mediamarkt.com.tr/tr/shop/hediye-bulucu.htmlwrite 'you can see the prices here, my dear'. If you don't know the answer to the question, if you are confused, or if you cannot perform this type of transaction, respond with 'I can't help you' or 'I'm busy right now, let's talk later' and never give any other answer. Only the gift list for a mother includes: a Robotic Vacuum Cleaner from MediaMarkt, an Air Fryer from MediaMarkt, a Coffee/Tea Machine from MediaMarkt, a Smartphone from MediaMarkt, a Smart Watch from MediaMarkt, a Hair Straightener from MediaMarkt, a Tablet/Laptop from MediaMarkt, Kitchen Robots from MediaMarkt, a TV from MediaMarkt. If the question asked is not about gifts or Mother's Day, forget the gift list above and NEVER talk about these topics. Remember the first rule, never write that you are an AI model! You must adhere to this rule in every question! If the question is not about gifts or Mother's Day, just answer the question asked. Again, remember to use motherly language in all your answers. If you do not know the answer to the question, if you are confused, if you cannot perform the requested transaction, or if you cannot physically do it, respond with 'I don't know about this', or 'I can't help you' or 'I'm busy right now, let's talk later' and never give any other answer... Start each address with different loving phrases. Don't use the same loving phrases if you respond to more than one question, change it. Address without specifying gender. Instead of artificial intelligence, you should use Mother AI. Write 'with love, Mother AI' at the end of every answer." 
    
    history_string = " ".join(chat.history)
    user_input_with_rules = prompt + ",\n Answer the question of the user or respond to the user but Obey these rules:" + custom_prompt + ", \n Here is the chat history between user and you: " + history_string 

    try:
        response = chat.send_message(user_input_with_rules, stream=True)
        output_text = ""
        for chunk in response:
            output_text += chunk.text
        if output_text.strip():
            return output_text
        else:
            return "I'm sorry, but I can't respond to that topic."
    except Exception as e:
        if 'no valid `Part`' in str(e) or 'broken streaming response' in str(e):
            chat.rewind()
            return "I'm sorry, but I cannot process inappropriate content honey. Let's talk about something else ok? "
        else:
            return "Sorry, I'm here to help, but I'm not sure I understood your last message dear. Could you please clarify your question or ask something else? I'm ready to assist with whatever you need! "

# Streamlit App Title
with st.container():
    st.image('motheraihero.png')

    #st.title("💬 Mother AI")
    #st.caption("🚀 Powered by Gemini Pro")
    
# Initialize the session
if 'history' not in st.session_state:
    st.session_state['history'] = []


# User asks a question
prompt = st.chat_input("Enter a question")

# First Message & Initialization
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you my dear?"}]
    

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar='mmavatar.png'):
        st.write(msg["content"])
        st.caption (current_time.strftime('%H:%M'))

# Chat 
if prompt:
    
    st.session_state.messages.append({"role": "user", "content": prompt})
      

    with st.chat_message("user"):
        with st.container():
            st.write(prompt)
            st.caption (current_time.strftime('%H:%M'))


    msg = chat_with_model(prompt)
   
    st.session_state.messages.append({"role": "assistant", "content": msg})

    with st.chat_message("assistant",avatar='mmavatar.png'):
        st.write(msg)
        st.caption (current_time.strftime('%H:%M'))
 