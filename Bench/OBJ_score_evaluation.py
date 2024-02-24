## This script is used to evaluate the accuracy of the model output in the form of json file.
import json
import os
from statistics import mean
import codecs
import argparse


score_dict = {
        "model_name": None,
        "correct_question_num": 0.0,
        "question_num": 646,
        "accuracy": 0.0,
        'subject':{
            'Math': {
                'correct_question_num': 0.0,
                'accuracy': 0.0,
                'question_num': 80,
                'type': 
                {
                    '2010-2023_Math_MCQs': {'correct_question_num': 0.0, 'question_num': 80, 'accuracy': 0.0},
                }
            }, 
            'Chinese': {
                'correct_question_num': 0.0, 
                'accuracy': 0.0,
                'question_num': 16,
                'type': 
                {
                    '2010-2023_Chinese_Pratical_Lit': {'correct_question_num': 0.0, 'question_num': 16, 'accuracy': 0.0},
                }
            },
            'Physics': {
                
                'correct_question_num': 0.0, 
                'accuracy': 0.0,
                'question_num': 174,
                'type':
                {
                    '2010-2023_Physics_MCQs': {'correct_question_num': 0.0, 'question_num': 174, 'accuracy': 0.0},
                }
            },
            'Chemistry': {
                
                'correct_question_num': 0.0, 
                'accuracy': 0.0,
                'question_num': 67,
                'type':
                {
                    '2010-2023_Chemistry_MCQs': {'correct_question_num': 0.0, 'question_num': 67, 'accuracy': 0.0},
                }
            },
            'Biology': {
                
                'correct_question_num': 0.0, 
                'accuracy': 0.0,
                'question_num': 21,
                'type': 
                {
                    '2010-2023_Biology_MCQs': {'correct_question_num': 0.0, 'question_num': 21, 'accuracy': 0.0},
                }
            },
            'History': {
                
                'correct_question_num': 0.0, 
                'accuracy': 0.0,
                'question_num': 34,
                'type': 
                {
                    '2010-2023_History_MCQs': {'correct_question_num': 0.0, 'question_num': 34, 'accuracy': 0.0},
                }
            },
            'Geography': {
                
                'correct_question_num': 0.0, 
                'accuracy': 0.0,
                'question_num': 221,
                'type': 
                {
                    '2010-2023_Geography_MCQs': {'correct_question_num': 0.0, 'question_num': 221, 'accuracy': 0.0},
                }
            },
            'Politics': {
                
                'correct_question_num': 0.0, 
                'accuracy': 0.0,
                'question_num': 33,
                'type': 
                {
                    '2010-2023_Political_Science_MCQs': {'correct_question_num': 0.0, 'question_num': 33, 'accuracy': 0.0},
                }
            }
        }
    }



def check_length_equal(item, filename):
    if len(item["model_answer"]) != len(item["standard_answer"]):
        print("model_answer and standard_answer length is not equal, filename:"+filename+"\tindex:"+str(item["index"]))
        item["model_answer"]=["Z"]*len(item["standard_answer"])


def obj_score_eval(obj_output_dir: str) -> None:

    obj_files = [os.path.join(obj_output_dir, file) for file in os.listdir(obj_output_dir) if file.endswith(".json") and file != 'correction_score.json']

    for file in obj_files:
        if "correction_score" in file:
            continue

        with codecs.open(file, "r", 'utf-8') as f:
            data = json.load(f)
            f.close()
        
        if 'keyword' in data.keys():
            keyword = data['keyword']
        else:
            keyword = data['keywords']
            
        model_name = data['model_name']

        score_dict['model_name'] = model_name


        c_q_num = 0.0
        ac = 0.0

        print(f"Calculating {keyword} {model_name} score")

        for key, value in score_dict['subject'].items():
            if keyword in value['type'].keys():
                break
        
        for item in data['example']:
            assert len(item['standard_answer']) == 1, "standard_answer length is not 1"
            check_length_equal(item, file)

            if keyword in ['2010-2023_Physics_MCQs', '2010-2023_Chinese_Pratical_Lit']:
                if item['model_answer'][0].lower() == item['standard_answer'][0].lower():
                    c_q_num += 1
                elif item['model_answer'][0].lower() in item['standard_answer'][0].lower():
                    c_q_num += 0.5

            else:
                if item['model_answer'][0].lower() == item['standard_answer'][0].lower():
                    c_q_num += 1


        score_dict['subject'][key]['type'][keyword]['correct_question_num'] = c_q_num
        ac = round(c_q_num / score_dict['subject'][key]['type'][keyword]['question_num'], 3)
        score_dict['subject'][key]['type'][keyword]['accuracy'] = ac

        score_dict['subject'][key]['correct_question_num'] += c_q_num
            

    c_q_num = 0.0

    for value in score_dict['subject'].values():
        value['accuracy'] = round(value['correct_question_num'] / value['question_num'], 3)
        c_q_num += value['correct_question_num']
    
    score_dict['correct_question_num'] = c_q_num
    score_dict['accuracy'] = round(c_q_num / score_dict['question_num'], 3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--obj_output_dir', type=str)

    args = parser.parse_args()

    obj_output_dir = args.obj_output_dir

    obj_score_eval(obj_output_dir)
    with open(os.path.join(obj_output_dir, 'correction_score.json'), 'w+') as f:
        json.dump(score_dict, f, ensure_ascii=False, indent=4)

    

    
