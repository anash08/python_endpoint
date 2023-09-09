import requests
import json
from fastapi import FastAPI

app = FastAPI()

@app.get('/latex')
async def get_latex():
    result = requests.get(url='http://localhost:5000/convertedValue')
    result_dict = json.loads(result.text)
    result_str = result_dict['convertedValue']
    return result_str





#################??????????/////
import requests
import json
from langchain.llms import OpenAI
from langchain.chains.llm_symbolic_math.base import LLMSymbolicMathChain
from langchain import PromptTemplate
from fastapi import FastAPI
from langchain import LLMMathChain

app = FastAPI()

llm = OpenAI(temperature=0, openai_api_key="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")

#template = """This is the latex equation. Solve the equation for 'x'. Also give the steps on how to solve it Equation: {equation}"""


template = """Respond according to the in  5 steps and respond appropriately, explain in brief and where its been used. Equation: {equation}"""


prompt = PromptTemplate(template=template, input_variables=['equation'])

llm_math = LLMSymbolicMathChain.from_llm(llm)

llm_math1 = LLMMathChain.from_llm(llm, verbose=True)

def get_latex():
    result = requests.get(url='http://localhost:5000/convertedValue')
    result_dict = json.loads(result.text)
    result_str = result_dict['convertedValue']
    return str(result_str)

i= get_latex()

@app.get('/chain')
def run_chain():
    i = get_latex()
    input_to_llm=prompt.format(equation=i)
    result = llm_math.run(input_to_llm)
    return result

#@app.get('/chain1')
#def run_chain1():
#    i=get_latex()
#    llm_math = LLMMathChain.from_llm(llm, verbose=True)
#    input_to_llm=prompt.format(equation=i)
#    result = llm_math.run(input_to_llm)
#    return {'message':result}

@app.get('/chain1')
def run_chain():
    i = get_latex()
    input_to_llm = template.format(equation=i)
    result = llm_math.run(input_to_llm)
    return result

