from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

def generate_answer(query: str, context_chunks: list):
    """
    Constructs prompt and calls Azure OpenAI LLM to generate an answer based on context.
    """
    # Join context chunks into a single string
    context_text = "\n\n---\n\n".join([chunk.page_content for chunk in context_chunks])
    
    prompt_template = """
    Answer the question based ONLY on the following context:
    {context}
    
    Question: {question}
    
    If the answer is not present in the context, strictly say "I don't know".
    Do not use any external knowledge.
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0
    )
    
    # Create chain
    chain = (
        {"context": lambda x: context_text, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    response = chain.invoke(query)
    return response
