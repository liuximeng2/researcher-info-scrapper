import json
import os
import argparse

from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Fileds(BaseModel):
    first_name: str
    last_name: str
    emory_email: str
    title: str
    school: str
    department: str
    research_focus: list[str]
    research_focus_description: str
    link_to_bio: list[str]

def extract_fileds(website_text,
                   instruction_path='prompt/instruction.txt',
                   structurer_path='prompt/structurer.txt'):

    with open(instruction_path, 'r') as file, open(structurer_path, 'r') as structurer:
        instruction = file.read()
        structurer_instruction = structurer.read()


    agent = client.chat.completions.create(
            model='gpt-4o',
            messages=[{"role": "system", "content": f"{instruction}"},
                      {"role": "user", "content": f"{website_text}"}],
            stream=False)
    response = agent.choices[0].message.content

    structure_agent = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": f"{structurer_instruction}"},
                      {"role": "user", "content": f"{response}"}],
            response_format=Fileds)
    structure_response = structure_agent.choices[0].message.parsed

    return structure_response