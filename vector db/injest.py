import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredFileLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant

# Use the updated HuggingFaceEmbeddings class
embeddings = HuggingFaceEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")

print(embeddings)

# Correct the glob pattern to be relative
loader = DirectoryLoader('data/', glob="**/*.pdf", show_progress=True, loader_cls=UnstructuredFileLoader)

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)

texts = text_splitter.split_documents(documents)

print(texts[1])

url = "http://localhost:6333"
qdrant = Qdrant.from_documents(
    texts,
    embeddings,
    url=url,
    prefer_grpc=False,
    collection_name="crop_vector_db"
)

print("Vector DB Successfully Created!")
