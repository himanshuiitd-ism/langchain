from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
# from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash",
)

prompt1 = PromptTemplate(
  template='Generate short and simple notes from the following text \n {text}',
  input_variables=['text']
)

prompt2 = PromptTemplate(
  template='Generate 5 short question answer from the following text \n {text}',
  input_variables=['text']
)

prompt3 = PromptTemplate(
  template='Merge the provided notes and quiz into a single document \n notes -> {notes} and {quiz}',
  input_variables=['notes','quiz']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
  'notes' : prompt1 | model | parser,
  'quiz' : prompt2 | model | parser,
})

merge_chain = prompt3 | model | parser

chain = parallel_chain | merge_chain


text = """I. Introduction to Chains (0:00-8:11)
Concept: Chains in LangChain allow for creating automated pipelines by connecting multiple small, sequential steps (like prompting, LLM invocation, and parsing) into a single, cohesive workflow.
Benefits: Simplifies complex applications by avoiding manual handling of every component, enabling automation, and allowing for complex architectures like parallel and conditional processing.
II. Simple Chain (8:11-14:30)
Definition: A basic, linear pipeline consisting of a PromptTemplate, an LLM (e.g., ChatOpenAI), and an output parser (e.g., StrOutputParser).
Execution: Steps are joined using the pipe operator (|), part of the LangChain Expression Language (LCEL).
Process: User input → Prompt filled → LLM invoked → Output parsed to string.
III. Sequential Chain (14:30-19:48)
Functionality: Extends the concept by daisy-chaining multiple LLM calls where the output of one step becomes the input for the next.
Application: Useful for multi-step tasks, such as generating a detailed report and then summarizing that specific report.
IV. Parallel Chain (19:48-32:36)
Implementation: Uses RunnableParallel to execute multiple chains simultaneously.
Workflow: Allows processing a single input through different paths (e.g., generating notes and a quiz from one source document) and eventually merging the outputs using a final LLM call.
V. Conditional Chains (32:36-54:01)
Branching Logic: Uses RunnableBranch to implement if-else style decision-making.
Mechanism: Evaluates conditions (e.g., sentiment analysis results) to determine which path or chain should be executed.
Consistency: Employs PydanticOutputParser to ensure LLM outputs strictly adhere to expected categories (like 'positive' or 'negative'), which is critical for reliable branching.
Components: RunnableLambda is used to convert standard Python functions into runnable components within the chain structure."""
result = chain.invoke({'text' : text})

print(result)
print(chain.get_graph().print_ascii())
