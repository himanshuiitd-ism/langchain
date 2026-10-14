from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser , PydanticOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda, RunnableSequence , RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatGoogleGenerativeAI(
  model = 'gemini-2.5-flash',
)

parser = StrOutputParser()

prompt1 = PromptTemplate(
  template='Write only one joke on topic : {topic}',
  input_variables=['topic']
)

def wordcount(joke):
  return len(joke.split())

joke_gen = RunnableSequence(prompt1, model , parser)

parallel_chain = RunnableParallel({
  'joke' : RunnablePassthrough(),
  'length': RunnableLambda(wordcount)
})

final_chain = RunnableSequence(joke_gen, parallel_chain)

result = final_chain.invoke({'topic':'AI'})
print(result)

# Used when you need to do some operation which cannot be done  entirely by llm and need any custom logic in it