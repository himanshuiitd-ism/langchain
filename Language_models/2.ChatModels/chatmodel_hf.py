from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
  repo_id="meta-llama/Llama-3.3-70B-Instruct",
  task="text-generation"
)

model = ChatHuggingFace(llm=llm)

while(True):
  x=str(input("Enter your query: "))
  if(x=="exit"):
    break
  result = model.invoke(x)
  print(result.content)
  print("\n")
