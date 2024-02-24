### This file is used to generate the json file for the benchmarking of the model
import sys
import os
import codecs
import argparse

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)

from Models.openai_gpt4 import OpenaiAPI


from bench_function import export_distribute_json
import os
import json
import time


if __name__ == "__main__":

    # Load the MCQ_prompt.json file
    with open("MCQ_prompt.json", "r") as f:
        data = json.load(f)['examples']
    f.close()

    ### An example of using OpenAI GPT-4Vision model to generate the json file for the benchmarking of the model
    parser = argparse.ArgumentParser()
    parser.add_argument('--openai_api_key', type=str)
    args = parser.parse_args()

    model_name = "gpt-4-vision-preview"
    openai_key = args.openai_api_key
    openai_base_url = "https://api.openai.com/v1"
    model_api = OpenaiAPI(openai_key, openai_base_url, model_name="gpt-4-vision-preview", temperature=0.3, max_tokens=4096)

    multi_images = True # whether to support multi images input, True means support, False means not support

        
    for i in range(len(data)):
        directory = "../Data"
        
        keyword = data[i]['keyword']
        question_type = data[i]['type']
        zero_shot_prompt_text = data[i]['prefix_prompt']
        print(model_name)
        print(keyword)
        print(question_type)

        export_distribute_json(
            model_api, 
            model_name, 
            directory, 
            keyword, 
            zero_shot_prompt_text, 
            question_type, 
            multi_images=multi_images
        )

    
