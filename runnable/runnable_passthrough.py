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
  model="gemini-2.5-flash",
)

prompt1 = PromptTemplate(
  template='Write a joke about {topic}',
  input_variables=['topic']
)

parser = StrOutputParser()

prompt2 = PromptTemplate(
  template='Explain the following joke - {text}',
  input_variables=['text']
)

joke_gen_chain = RunnableSequence(prompt1 , model , parser)

parallel_chain = RunnableParallel({
  'joke' : RunnablePassthrough(), #jb koi kaam na krna ho
  'explanation' : RunnableSequence(prompt2 , model , parser)
})

full_chain = RunnableSequence(
  joke_gen_chain ,
  parallel_chain
)

result = full_chain.invoke({'topic':'AI'})
print(result)