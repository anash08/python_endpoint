import requests
import json
from langchain.llms import OpenAI
from langchain.chains.llm_symbolic_math.base import LLMSymbolicMathChain
from langchain import PromptTemplate
from fastapi import FastAPI
from langchain import LLMMathChain
from fastapi import FastAPI

app = FastAPI()

llm = OpenAI(temperature=0.2, openai_api_key="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")
llm_math = LLMMathChain.from_llm(llm, verbose=True)
llm_symbolic_math = LLMSymbolicMathChain.from_llm(llm, verbose=True)


template = """Respond according to the in  5 steps and respond appropriately,
 explain in brief and where its been used. Equation: {equation}"""

def get_latex():
    result = requests.get(url='http://localhost:5000/convertedValue')
    print("||RESULT||", result)
    result_dict = json.loads(result.text)
    print("||RESULT||", result_dict)

    result_str = result_dict['convertedValue']
    print("||RESULT_STR||", result_str)
    return str(result_str)

@app.get('/chain1')
def run_chain():
    i = get_latex()
    input_to_llm = template.format(equation=i)
    result = llm_math.run(input_to_llm)
    result_description = llm_symbolic_math.run(input_to_llm)
    print(result_description, "||||||||||||||||||||||||||||||")

    return (result)

