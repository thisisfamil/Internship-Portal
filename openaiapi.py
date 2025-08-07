from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import psycopg2
import io
import pdfplumber
import numpy as np
from database import get_db
from vacancies import job_requirements
from sentence_transformers import SentenceTransformer


load_dotenv()


model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def get_embedding(text: str):
    return model.encode(text).tolist()

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))







# from fastapi import FastAPI, HTTPException
# from dotenv import load_dotenv
# import os
# import psycopg2
# import io
# import pdfplumber
# import openai
# import numpy as np
# from database import get_db
# from vacancies import job_requirements 


# load_dotenv()


# openai.api_key = os.getenv("OPENAI_API_KEY")


# def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
#     with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
#         text = ""
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text


# def get_embedding(text: str):
#     response = openai.Embedding.create(
#         model="text-embedding-ada-002",
#         input=text
#     )
#     return response['data'][0]['embedding']


# def cosine_similarity(vec1, vec2):
#     v1 = np.array(vec1)
#     v2 = np.array(vec2)
#     return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


