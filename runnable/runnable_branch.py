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
  model='gemini-2.5-flash',
)

parser = StrOutputParser()

prompt1 = PromptTemplate(
  template='Write a detailed report on {topic}',
  input_variables=['topic']
)

prompt2 = PromptTemplate(
  template='Summarize the following text \n {text}',
  input_variables=['text']
)

report_chain = RunnableSequence(prompt1, model, parser)

# branch_chain = RunnableBranch(
#   (condition, runnable),
#   default
# )

branch_chain = RunnableBranch(
  (lambda x: len(x.split()) >100, RunnableSequence(prompt2, model, parser)),
  RunnablePassthrough()
)

final_chain = RunnableSequence(report_chain, branch_chain)

print(final_chain.invoke({'topic':'AI'}))