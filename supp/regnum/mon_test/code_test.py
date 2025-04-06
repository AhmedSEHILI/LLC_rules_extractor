import sys
sys.path.insert(0, '../py_files')
from data_loader import GeneralDataLoader
from graph_data import StarDogGraph
from parent_ruleminer import RunParseAMIE
from tqdm import tqdm
from runner import run
import random


f_name= 'LLCdata'
p = f'./{f_name}'
PATH_RM = f"./amie/amie3.5.1.jar"
PATH_result = f"./results/{f_name}/"


dl = GeneralDataLoader(path_t=f'{p}/ontoTSV.tsv', path_numerical_preds=f'{p}/numericalLLC.tsv')

amie = RunParseAMIE(data=dl.df, path_rule_miner=PATH_RM, path_save_rules=PATH_result)
rules = amie.parse()

print("tout est bon")
