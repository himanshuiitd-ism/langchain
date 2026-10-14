from operator import mod
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage

load_dotenv()

llm = HuggingFaceEndpoint(
  repo_id="meta-llama/Llama-3.3-70B-Instruct",
  task="conversational",
)

model = ChatHuggingFace(llm = llm)

message = [
  SystemMessage(content='You are Bob, a langchain and langgraph expert , your date of birth is 19 sept 1980, your job is answer every query of user in point wise manner about langchain and langgraph, but if user asks question beyond your scope then give him a proper message that you are not able to answer this query currently because you are his tutor')
]

while(True):
  x = str(input("You: "))
  message.append(HumanMessage(content=x))
  if(x=="exit"):
    break
  result = model.invoke(message)
  message.append(AIMessage(content=result.content))
  print("Bob: ", result.content)
  print("\n")