# Imported required langchain packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# This is the template that we use to tell the model how to act and respond
template = """Question: {question}
              You are a friendly and helpful chatbot that gently responds to the user query.
              Keep your response concise.
"""

prompt = ChatPromptTemplate.from_template(template)

# Here I initialized a model (we can use any model of our choice) 
model = OllamaLLM(model="llama3.2:1b")

chain = prompt | model
print("Enter ctrl + C to quit the chat")
# Take the input from the user
while True:
    question = input("Ask : ")
    response = chain.invoke({"question": f"{question}"})
    print(f"Response : {response}")
    
