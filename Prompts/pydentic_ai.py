from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel,EmailStr,Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.3-70B-Instruct",
    task="text-generation",
)

model = ChatHuggingFace(llm = llm)

class Review(BaseModel):

  key_themes : list[str] = Field(description="write down all the key themes discussed in the review in a list")
  summary: str = Field(description="A brief summary of the review")
  sentiment: Literal["pos","neg"] = Field(description= "The sentiment of the review")
  pros: Optional[list[str]] = Field(default=None, description= "Write down all the pros inside a list")
  cons: Optional[list[str]] = Field(default=None, description= "Write down all the cons inside a list")

structured_model = model.with_structured_output(Review)

while(True):
  x = str(input("Enter your review: "))
  if(x=="exit"):
    break
  print("\n")
  result = structured_model.invoke(x)
  print("The review is ------->",result)
  print("\n")


# Pydantic is more powerful than Typedict because in pydantic we can add more attributes like Field(description="...",default=...,gt=, lt=)etc
# In Typedict we cannot add these attributes