import os
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv() 
api_key = os.environ.get("GROQ_API_KEY")

# Initialize the LLM 
def initialize_llm():
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.3-70b-versatile",
        groq_api_key = api_key
    )
    return llm

# Load or create Chroma vector database
def create_vector_db(data_path="./data/", db_path="./chroma_db"):
    loader = DirectoryLoader(
        data_path,
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(texts, embeddings, persist_directory=db_path)
    vector_db.persist()
    print("ChromaDB created and data saved")
    return vector_db

# Setup QA chain
def set_qa_chain(vector_db, llm):
    retriever = vector_db.as_retriever()
    prompt_template = prompt_template = """
You are a compassionate mental health chatbot. Your goal is to:
- Understand the user's emotions.
- Respond with empathy and thoughtful advice.
- Keep answers concise but helpful.
- If the user asks for factual information, provide it clearly.

Conversation Context:
{context}

User: {question}
Chatbot:
"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

# Initialize everything and expose a function
db_path = "./chroma_db"
data_path = "./data/"

llm = initialize_llm()

if not os.path.exists(db_path):
    vector_db = create_vector_db(data_path, db_path)
else:
    embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)

qa_chain = set_qa_chain(vector_db, llm)

def get_response(user_input):
    return qa_chain.run(user_input)