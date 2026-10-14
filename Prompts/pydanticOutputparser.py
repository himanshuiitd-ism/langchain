from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
)

model = ChatHuggingFace(llm = llm)

class Person(BaseModel):
  
  name: str = Field(description="Name of the person")
  age: int = Field(description="Age of the person")
  city: str = Field(description="Name of the city the person belongs to")

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
  template='Generate the name, age and city name of a fictonal {place} person \n {format_instruction}',
  input_variables=['place'],
  partial_variables={'format_instruction':parser.get_format_instructions()}
)

while(True):
  x = str(input("Enter your review: "))
  if(x=="exit"):
    break
  print("\n")
  chain = template | model | parser
  result = chain.invoke({'place':x})
  print(result)


# Pydantic is more powerful than Typedict because in pydantic we can add more attributes like Field(description="...",default=...,gt=, lt=)etc
# In Typedict we cannot add these attributes