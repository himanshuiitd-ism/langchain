from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser , PydanticOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
# from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatGoogleGenerativeAI(
  model="gemini-3.8-flash",
)

parser = StrOutputParser()

class Feedback(BaseModel):
  sentiment: Literal['positive','negative'] = Field(description='Give the sentiment of the feedback')

parser2 = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
  template='Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instructions}',
  input_variables=['feedback'],
  partial_variables={'format_instructions':parser2.get_format_instructions()}
)

classifier_chain = prompt1 | model | parser2

prompt2 = PromptTemplate(
  template='Write an appropriate general response to this positive feedback \n {feedback}',
  input_variables=['feedback']
)

prompt3 = PromptTemplate(
  template='Write an appropriate general response to this negative feedback \n {feedback}',
  input_variables=['feedback']
)

branch_chain = RunnableBranch(
  (lambda x:x.sentiment == 'positive', prompt2 | model | parser),
  (lambda x:x.sentiment == 'negative', prompt3 | model | parser),
  RunnableLambda(lambda x:"Couldn't find sentiment")
)

chain = classifier_chain | branch_chain

result = chain.invoke({'feedback': "This is a terrible phone, the battery drains too fast"})

print(result)

print(chain.get_graph().print_ascii())