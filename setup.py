from setuptools import find_packages,setup

setup(
   name='mcqgenerator',
   version='0.0.1',
   author='merlyn',
   author_email='omagwamerlyn@gmail.com',
   install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain-google-genai","google-generativeai"],
   packages=find_packages()
)