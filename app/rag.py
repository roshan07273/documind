
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are DocuMind, an intelligent document assistant.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I could not find that in the document."

Context: {context}

Question: {question}

Answer:"""
)

def get_rag_chain(vectorstore):
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain
