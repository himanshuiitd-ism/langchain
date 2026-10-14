from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.3-70B-Instruct",
    task="text-generation",
)

model = ChatHuggingFace(llm = llm)

# class Review(TypedDict):
#   summary: str
#   sentiment: str

# class Review(TypedDict):
#   key_themes: Annotated[list[str],"write down all the key themes discussed in the review in a list"]
#   summary: Annotated[str, "A brief summary of the review"]
#   sentiment: Annotated[str, "The summary of sentiment of the review"]
#   pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
#   cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]

class Review(TypedDict):
  key_themes: Annotated[list[str],"write down all the key themes discussed in the review in a list"]
  summary: Annotated[str, "A brief summary of the review"]
  sentiment: Annotated[Literal["pos","neg"], "The sentiment of the review"]
  pros: Annotated[Optional[list[str]], "Write down all the pros inside a list"]
  cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]

structured_model = model.with_structured_output(Review)

while(True):
  x = str(input("Enter your review: "))
  if(x=="exit"):
    break
  print("\n")
  result = structured_model.invoke(x)
  print("The review is ------->",result)
  print("\n")