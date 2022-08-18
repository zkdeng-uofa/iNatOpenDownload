import yaml
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    '--input',
    type = int
)
args = parser.parse_args()

dict_file = [{'test_index': args.input}]

os.mkdir(f'yaml/test_folder_{args.input}')
with open(f'yaml/test_folder_{args.input}/test.yaml', 'w') as file:
    documents = yaml.dump(dict_file, file)
  
