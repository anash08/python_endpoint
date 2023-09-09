import requests
import json
from langchain.llms import OpenAI
from langchain.chains.llm_symbolic_math.base import LLMSymbolicMathChain
from langchain import PromptTemplate
from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from langchain import LLMMathChain

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict origins as needed
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)



llm = OpenAI(temperature=0, openai_api_key="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")

# Template for generating prompts
template = """Respond accordingly in 5 steps mathematically and respond appropriately, explain in brief and where its been used and in the end show me the answer and if there is no answer describe why there is no answer. Equation: {equation}"""

# Initialize prompt template
prompt = PromptTemplate(template=template, input_variables=['equation'])

# Create LLMSymbolicMathChain instance
llm_math = LLMSymbolicMathChain.from_llm(llm, verbose=True)
llm_math_basic = LLMMathChain.from_llm(llm, verbose=True)


# Function to get the convertedValue from the frontend
def get_latex():
    result = requests.get(url='http://localhost:9000/fetchlatexValue')  # Change the URL as needed
    result_dict = json.loads(result.text)
    result_str = result_dict.get('convertedValue', '')
    return result_str


@app.get('/convertedValue')
def get_converted_value():
    return {"convertedValue": get_latex()}  # Use appropriate data structure here

# Endpoint to run the chain dynamically
@app.post('/run_chain_dynamically')
def run_chain_dynamically(data: dict):
    # Extract the convertedValue from the request data
    converted_value = data.get("convertedValue")
    
    if not converted_value:
        raise HTTPException(status_code=400, detail="convertedValue not found")
    
    input_to_llm = template.format(equation=converted_value)
    print(input_to_llm, "......|TEMPLATE|...")
    # Run LLMSymbolicMathChain
    result = llm_math.run(input_to_llm)
    # result_description = llm_math_basic.run(input_to_llm) 

    return result
