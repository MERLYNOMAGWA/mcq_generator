import os
import PyPDF2
import json
import traceback
import re
from src.mcqgen.logger import logging  

def read_file(file):
   if file.name.endswith(".pdf"):
      try:
         pdf_reader = PyPDF2.PdfFileReader(file)
         text = ""
         for page in pdf_reader.pages:
            text += page.extract_text()
         return text
      except Exception as e:
         raise Exception("Error reading the PDF file")
        
   elif file.name.endswith(".txt"):
      return file.read().decode("utf-8")
    
   else:
      raise Exception("Unsupported file format. Only PDF and TXT are supported.")

def get_table_data(quiz_str):
   try:
      
      quiz_str = re.sub(r"```(?:json)?", "", quiz_str).strip("` \n")

      logging.info(f"Sanitized quiz string: {quiz_str[:100]}...")

      quiz_dict = json.loads(quiz_str)
      quiz_table_data = []

      for key, value in quiz_dict.items():
         mcq = value["mcq"]
         options = " || ".join([
            f"{option} -> {option_value}" 
            for option, option_value in value["options"].items()
         ])
         correct = value["correct"]
         quiz_table_data.append({
            "MCQ": mcq,
            "Choices": options,
            "Correct": correct
         })

      logging.info("Quiz JSON parsed and formatted successfully.")
      return quiz_table_data

   except Exception as e:
      logging.error(f"Error in get_table_data: {e}")
      traceback.print_exception(type(e), e, e.__traceback__)
      return False