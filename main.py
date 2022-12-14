import os
import json
from solc_compiler import compiler_helpers
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pragma_utils import Pragma


contracts_folder = 'contracts'
contract_name = 'temporary'
contract_result = 'analyze'

# init solc compiler class with helper functions
solc = compiler_helpers
pragma_utils = Pragma(solc)

class Contract(BaseModel): 
    sol_contract: str
    pragma: str
    
class Issues(BaseModel):
    optimization: int
    informational: int
    low: int
    medium: int
    high: int


class ContractIssues:
    def __init__(self) -> None:
        self.optimization = 0
        self.informational = 0
        self.low = 0
        self.medium = 0
        self.high = 0

    def increment(self,type: str):
        current_value = getattr(self, type)
        new_value = current_value + 1
        setattr(self, type, new_value)

    def get_self(self):
        return {
            'optimization': getattr(self, 'optimization'),
            'informational': getattr(self, 'informational'),
            'low': getattr(self, 'low'),
            'medium': getattr(self, 'medium'),
            'high': getattr(self, 'high'),
        }


# scans contract using slither command 
def scan_contract(contract_name: str, result_filename: str):
    global contracts_folder  
    if os.path.exists(result_filename):
        os.remove(result_filename)
    # scans contract and generates results in json file
    os.system(f"slither {contract_name} --json {result_filename}")


# reads generate results of contract analyzer
def read_analyzer_results(filename:str):
    result = open(filename)
    return json.load(result)
    
# checks if directory exists
def directory_exists(name: str):
    return os.path.isdir(name)

def aggregate_issues(contract_analysis: object):
    issues = ContractIssues()
    detectors = contract_analysis['results']['detectors']
    # register issue if found
    if isinstance(detectors, object):
     for issue in detectors:
        issue_type = issue['impact'].lower()

        if hasattr(issues, issue_type):
            issues.increment(issue_type)
        
    return issues.get_self()


# saves solidity contract to folder
def generate_issues(contract_string: str, pragma_version: str):
    global folder_exists
    global contracts_folder
    global contract_name
    global contract_result

    folder_exists = directory_exists(contracts_folder)
    # creates  folder where temporary contract file will be stored
    if not folder_exists:
        os.mkdir('contracts') 

    with open(f'./{contracts_folder}/{contract_name}.sol', 'w') as f:
        f.write(contract_string)

    contract_filename = f"./{contracts_folder}/{contract_name}.sol"
    result_filename = f"./{contracts_folder}/{contract_name}.json"
    scan_contract(contract_filename, result_filename)
    analyzed_data = read_analyzer_results(result_filename)
    issues = aggregate_issues(analyzed_data)
    return issues

# server
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# installs all solc version on server bootstrap
@app.on_event('startup')
async def install_solc_versions_on_bootstrap():
    solc_versions = solc.get_solc_versions()
    solc.install_solc_versions(solc_versions)
    # sets default solc compiler version
    os.system('solc-select use 0.8.0')
    


@app.post('/scanner',)
async def scan(contract: Contract, response_model=Issues):
    try:
        solidity_contract = contract.sol_contract
        pragma_version = pragma_utils.find_correct_version(contract.pragma) 
        solc.switch_solc_to_version(pragma_version)
        return generate_issues(solidity_contract, pragma_version)
    except BaseException as error: 
        return 'Something went wrong while evaluating contract security'


@app.get('/')
async def default():
    return 'Server is running'