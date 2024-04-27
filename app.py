import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main():
    os.environ["OPENAI_KEY"] = "key"
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF")

    #upload the file
    pdf = st.file_uploader("Upload your pdf file here", type='pdf')
    
    #extract the text file
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text=""
        for page in pdf_reader.pages:
            text+=page.extract_text()

        #st.write(text)
        #split text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        #create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base =FAISS.from_texts(chunks,embeddings)


        #show user input
        user_question =  st.text_input("Ask a question about your PDF:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            
            llm = OpenAI()
            chain = load_qa_chain(llm,chain_type="stuff")
            response = chain.run(input_document=docs,question=user_question)

            st.write(response)


if __name__ == '__main__':
    main()