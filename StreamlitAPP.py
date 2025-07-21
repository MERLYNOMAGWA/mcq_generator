import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgen.utils import read_file,get_table_data
from src.mcqgen.logger import logging
from src.mcqgen.MCQGen import generate_evaluate_chain

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_core.runnables import RunnableSequence
import PyPDF2
import streamlit as st

logging.info("Streamlit app started.")

try:
   response_path = os.path.join(os.getcwd(), "Response.json")
   with open(response_path, 'r') as file:
      RESPONSE_JSON = json.load(file)
   logging.info("Loaded Response.json successfully.")
except Exception as e:
   logging.error(f"Failed to load Response.json: {e}")
   st.error("Failed to load Response.json.")
   st.stop()

st.title("🤖 AI MCQ Generator")

with st.form("user_inputs"):
   uploaded_file = st.file_uploader("Upload a PDF or txt file")
   mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
   subject = st.text_input("Insert Subject", max_chars=20)
   tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
   button = st.form_submit_button("Create MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
   with st.spinner("loading..."):
      try:
         logging.info("Reading uploaded file...")
         text = read_file(uploaded_file)
         logging.info("File read successfully.")
         
         logging.info("Generating MCQs using LLM...")
         response = generate_evaluate_chain(
            {
               "text": text,
               "number": mcq_count,
               "subject": subject,
               "tone": tone,
               "response_json": json.dumps(RESPONSE_JSON)
            }
         )
         logging.info("MCQ generation completed.")

         if isinstance(response, dict):
            quiz = response.get("quiz", None)     
            if quiz:
               table_data = get_table_data(quiz)
               if table_data:
                  df = pd.DataFrame(table_data)
                  df.index = df.index + 1
                  st.table(df)

                  st.text_area(label="Review", value=response.get("review", "No review found."))
                  logging.info("Quiz table and review displayed.")
               else:
                  st.error("Error in the table data")
                  logging.warning("Table data was None.")
            else:
               st.write(response)
               logging.warning("No quiz found in the response.")
         else:
            st.write(response)
            logging.warning("Unexpected response format.")

      except Exception as e:
         logging.error(f"Exception occurred during processing: {e}")
         traceback.print_exception(type(e), e, e.__traceback__)
         st.error("An error occurred while generating the MCQs.")
         