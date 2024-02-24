### This file contains the functions for benchmarking the performance of the LLM on multiple-choice questions
import os
import json
import time
import re
from random import choice
import requests
from typing import List, Union, Dict
# from joblib import Parallel, delayed
import codecs

from tqdm import  tqdm



def extract_choice_answer(model_output, question_type, answer_lenth=None):
    """
    Extract choice answer from model output.

    Format of model_output that is expected:
    'single_choice': choice answer should be the last Capital Letter of the model_output, e.g.: "...【答案】 A <eoa>"
    'multi_choice': "...【答案】 ABD " or write the choice answers at the end of the model_output, e.g. "... ACD"
    """
    if question_type == 'single_choice':
        model_answer = []
        temp = re.findall(r'[A-D]', model_output[::-1])
        if len(temp) != 0:
            model_answer.append(temp[0])

    elif question_type == 'multi_choice':
        model_answer = []
        answer = ''
        content = re.sub(r'\s+', '', model_output)
        answer_index = content.find('【答案】')
        if answer_index > 0:
            temp = content[answer_index:]
            if len(re.findall(r'[A-D]', temp)) > 0:
                for t in re.findall(r'[A-D]', temp):
                    answer += t
        else:
            temp = content[-10:]
            if len(re.findall(r'[A-D]', temp)) > 0:
                for t in re.findall(r'[A-D]', temp):
                    answer += t
        if len(answer) != 0:
            model_answer.append(answer)
    
    return model_answer

def choice_test(**kwargs):
    """
    Test the LLM on multiple-choice questions
    """
    model_api = kwargs['model_api']
    model_name = kwargs['model_name']
    
    data = kwargs['data']['example']
    keyword = kwargs['keyword']
    prompt = kwargs['prompt']
    question_type = kwargs['question_type']
    multi_images = kwargs['multi_images']
    
    save_dir = f'../Results/{model_name}'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_file = os.path.join(save_dir, f'{model_name}_{keyword}.json')

    if os.path.exists(save_file):
        with open(save_file, 'r') as f:
            model_answer_dict = json.load(f)['example']
    else:
        model_answer_dict = []


    for i in tqdm(range(len(data))):
        if model_answer_dict != [] and i <= model_answer_dict[-1]['index']:
            continue

        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        picture = data[i]['picture']
        year = data[i]['year']
        category = data[i]['category']
        score = data[i]['score']
        standard_answer = data[i]['answer']
        answer_lenth = len(standard_answer)
        analysis = data[i]['analysis']

        if multi_images is False and len(picture) > 1:
            continue

        model_output = model_api(prompt, question, picture)
        model_answer = extract_choice_answer(model_output, question_type, answer_lenth)

        dict = {
            'index': index, 
            'year': year, 
            'category': category,
            'score': score,
            'question': question, 
            'standard_answer': standard_answer,
            'analysis': analysis,
            'model_answer': model_answer,
            'model_output': model_output
        }
        model_answer_dict.append(dict)

        time.sleep(1)

        with codecs.open(save_file, 'w+', 'utf-8') as f:
            output = {
                'keyword': keyword, 
                'model_name': model_name,
                'prompt': prompt,
                'example' : model_answer_dict
                }
            json.dump(output, f, ensure_ascii=False, indent=4)
            f.close()


def export_distribute_json(
        model_api,
        model_name: str, 
        directory: str, 
        keyword: str, 
        zero_shot_prompt_text: str, 
        question_type: str,
        multi_images: bool = True,
    ) -> None:
    """
    Distributes the task of processing examples in a JSON file across multiple processes.

    :param model_name: Name of the model to use
    :param directory: Directory containing the JSON file
    :param keyword: Keyword used to identify the JSON file
    :param zero_shot_prompt_text: Prompt text for zero-shot learning
    :param question_type: Type of questions in the JSON file (e.g. single_choice, five_out_of_seven, etc.)
    :param multi_images: Whether the LLM support multiple images inputs
    
    """
    # Find the JSON file with the specified keyword
    for root, _, files in os.walk(directory):
        for file in files:
            if file == f'{keyword}.json':
                filepath = os.path.join(root, file)
                with codecs.open(filepath, 'r', 'utf-8') as f:
                    data = json.load(f)
        
    
    kwargs = {
        'model_api': model_api,
        'model_name': model_name, 
        'data': data, 
        'keyword': keyword, 
        'prompt': zero_shot_prompt_text, 
        'question_type': question_type, 
        'multi_images': multi_images,
    }
    
    if question_type in ["single_choice", "multi_choice"]:
            choice_test(**kwargs)

