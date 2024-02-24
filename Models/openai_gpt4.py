# -*- coding: utf-8 -*-
import requests
import base64

import time
import openai
from random import choice
from typing import List
from openai import OpenAI


class OpenaiAPI:
    def __init__(self, api_key, base_url, model_name, temperature, max_tokens):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def forward(self, prompt, question, picture):
        usr_content = [{"type": "text","text": question}]
        for pic in picture:
            usr_content.append({
                'type': "image_url",
                'image_url': {
                    'url': f"data:image/png;base64,{self.encode_image(pic)}"
                }
            })
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": [{"type": "text", "text": prompt}]
                        },
                        {   
                            "role": "user",
                            "content": usr_content
                        }
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                break
            except openai.BadRequestError as e:
                print('BadRequestError:', e)
                response = "Your input image may contain content that is not allowed by our safety system."
                break
            except Exception as e:
                print('Exception:', e)
                time.sleep(1)
                continue
        
        return response

    def postprocess(self, response):
        """
        """
        model_output = None
        
        if isinstance(response, str):
            model_output = response
        else:
            model_output = response.choices[0].message.content
        return model_output
    
    def __call__(self, prompt:str, question:str, picture: list):
        response = self.forward(prompt, question, picture)
        model_output = self.postprocess(response)
        return model_output

def test(model, prompt:str, question:str, picture: list):
    response = model(prompt, question, picture)

    return response


if __name__ == "__main__":

    openai_key = "Input Your OpenAI API Key Here"
    openai_base_url = "https://api.openai.com/v1"

    model_api = OpenaiAPI(openai_key, openai_base_url, model_name="gpt-4-vision-preview", temperature=0.3, max_tokens=4096)
    data_example = {
            "year": "2017",
            "category": "新课标Ⅰ",
            "question": "3. (12 分) (三) 实用类文本阅读。阅读下面的文字, 完成下列各题。\n材料一:\n2011 年 1 月 1 日 8 点整, 中央电视台纪录频道正式开播, 信号覆盖全球。作为中国第一个国家级的专业纪录片频道, 也是第一个从开播之始就面向全球采用双语播出的频道, 它向世人亮出了拥有人文精神的中国形象。央视纪录频道在内容编排上进行了详细的规划, 主要呈现四大主体内容, 六大主题时段的播出特点, 以期达到规模化的播出效应。央视纪录频道同时采用国际纪录片频道的通行方式, 淡化栏目概念, 强化大时段编排, 以主题化、系列化和播出季的方式, 提升自身的影响力和美誉度。\n(摘编自杨玉洁等《真实聚焦: 2010 2011 中国纪录片频道运营与纪录片产业发展记录》)\n材料二\n2011 年中央电视台记录频道在 71 个大中城市的观众构成和集中度\n（资料来源于中国广视索福瑞媒介探究）\n注: 群众构成反映的是收视人群的构成, 回答了“谁在看该频道”的问题。集中度是目标群众收视率与总体群众收视率的比值, 表示的是目标群众相对于总体群众的收视集中程度, 能够回答“谁更喜欢收看这个频道”的问题; 集中度的比值大于 $100 \\%$, 表示该类目标群众的收视倾向高于平均水平。\n材料三:\n在制播运营模式方面, 央视纪录频道实行的是频道化运营模式。央视是纪录片的主要制作基地, 制作出的精品节目数量众多。当然, 频道化运营模式也有其自身的劣势, 劣势在于频道可以调动的资源非常有限, 其融资渠道、产品设计、人财物资源调度都会受到种种限制。央视纪录频道目前正积极推进制播分离模式，节目制作以社会招标、联合制作、购买作为主要方式，并辅以自制精品, 为建立较为健全的制作管理模式做好准备。\n(摘编自张同道等《2011 年国家纪录片频道发展报告 (下) 》)\n材料四:\n总部位于美国首都华盛顿的国家地理频道是一个全球性的付费有线电视网。目前, 国家地理频道已经以 34 种语言转播至全球 166 个国家和地区逾 2 亿 9 千万用户。作为一个纯纪录片频道能够取得如此卓越的成就, 除了高质量,高观赏性的节目内容之外, 与其频道自身的制播运营模式是分不开的。其制播运营模式如下: 有线电视系统是在地方政府的批准下由有线电视系统运营商投资建立的, 有线电视系统直接面向订户收取费用。有线电视系统运营商是指拥有并运营有线电视系统的企业实体。有线电视节目提供商为有线电视系统运营商提供节目。具体到国家地理频道而言, 美国国家地理电视公司以及其他渠道承担提供片源的任务; 国家地理频道承担的是节目制作等任务,即让来自国家地理电视公司等渠道的单个的片源变成有机结合的整体, 适于在电视上播放; 康卡斯特信公司作\n作为有线电视系统运营商, 则承担把电视信号传送到千家万户的电视机上的技术性播出任务。\n（摘编自楚慧萍《多元延伸, 有机互动- - 美国国家地理频道运营模式初探》)\n（1）下列对材料相关内容的梳理，不正确的一项是 (3 分)",
            "picture": [
                "../Data/2010-2023_Chinese_Pratical_Lit/2010-2023_Chinese_Pratical_Lit_0_0.png",
                "../Data/2010-2023_Chinese_Pratical_Lit/2010-2023_Chinese_Pratical_Lit_0_1.png",
                "../Data/2010-2023_Chinese_Pratical_Lit/2010-2023_Chinese_Pratical_Lit_0_2.png",
                "../Data/2010-2023_Chinese_Pratical_Lit/2010-2023_Chinese_Pratical_Lit_0_3.png",
                "../Data/2010-2023_Chinese_Pratical_Lit/2010-2023_Chinese_Pratical_Lit_0_4.png"
            ],
            "answer": [
                "D"
            ],
            "analysis": "【解答】(1) D “国家地理频道”应该是传送给“有线电视系统运营商”, “有线电视系统运营商”再传送给“电视观众”, 原文为“具体到国家地理频道而言, 美国国家地理电视公司以及其他渠道承担提供片源的任务; 国家地理频道承担的是节目制作等任务, 即让来自国家地理电视公司等渠道的单个的片源变成有机结合的整体, 适于在电视上播放; 康卡斯特电信公司作为有线电视系统运营商, 则承担把电视信号传送到千家万户的电视机上的技术性播出任务”,最后应该是“康卡斯特电信公司作为有线电视系统运营商把电视信号传送到千家万户的电视机上”.",
            "index": 0,
            "score": 3
        }
    choice_question = data_example['question']
    choice_picture = data_example['picture']
    choice_prompt = "请你做一道语文阅读理解题。\n请你结合文字和图片一步一步思考。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答。\n题目如下："

    result = test(model_api, choice_prompt, choice_question, choice_picture)

    print("Model output:\n" + result)
    
