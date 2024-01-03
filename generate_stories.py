import os
import glob
import pandas as pd
from itertools import product
from tqdm import tqdm
from llama_cpp import Llama
import pandas as pd

# Initialize the Llama model
model = "model/mistral-7b-instruct-v0.1.Q6_K.gguf"
llm = Llama(model_path=model, n_ctx=10260, n_batch=1024, n_threads=12, n_gpu_layers=-1, verbose=False,
            use_mlock=False)



def generate(system, user):
    message = f"<s>[INST] {system} [/INST]</s>{user}"
    output = llm(message, echo=False, stream=False, max_tokens=4096)
    output = output['choices'][0]['text'].replace(message, '')

    return {"content": output.strip()}



# To read from a JSON file in Python, follow these steps:

# Import the json module
import json

# Assume the file name is 'data.json' and it's in the same directory as your Python script
file_name = 'schema.json'
from prompts import prompt_schema

# Read from the JSON file
with open(file_name, 'r') as file:
    schema = json.load(file)

prompt = prompt_schema

# Replace placeholders with actual values from the schema
for key, value in schema.items():
    prompt = prompt.replace(f'[{key.capitalize()}]', str(value))


sections = prompt.split("**")


# Generate text for each section and carry over the context
story_context = ""
for section in sections:
    if section.strip():  # Check if the section is not empty
        # Append the current section to the story context
        next_prompt = section.strip()
        # Generate continuation based on the updated context
        generated_section = generate(system=story_context, user=f"Continue the story using :{next_prompt}")
        # Append the generated content to the story context
        story_context += generated_section['content']

print(story_context)


exit(0)


def generate(name, setting, hero, villain, story_type, age):
    system = f"""
    You are a teacher for young children, you turn {story_type} questions into children's stories.
    """
    user = f"""
    Write a 500 characters short story about a {age} year old named {name} who is a {hero}, traveling to {setting} to face {villain}, and uses their {story_type} skills to defeat them. 
    Provide a {story_type} excercise or a question within the story as a means for learning. 
    The story should be short, fantastical, yet exciting, with a happy ending where the hero wins if the excercise is answere correctly.

    """

    message = f"<s>[INST] {system} [/INST]</s>{user}"
    output = llm(message, echo=True, stream=False, max_tokens=4096)
    output = output['choices'][0]['text'].replace(message, '')


# Function to consolidate existing checkpoint files
def consolidate_checkpoints():
    checkpoint_files = sorted(glob.glob('children_stories_checkpoint_*.json'))
    data = []
    last_iteration = 0

    for file in checkpoint_files:
        df = pd.read_json(file, orient='records')
        data.extend(df.to_dict(orient='records'))
        last_iteration = int(file.split('_')[-1].split('.')[0])
        os.remove(file)  # Delete the file after loading its data

    if data:
        consolidated_file = f'children_stories_checkpoint_{last_iteration}.json'
        pd.DataFrame(data).to_json(consolidated_file, orient='records', indent=4)
        return data, last_iteration
    else:
        return [], 0



# Define the lists for scenarios
names = ["Kian"]
settings = ["mountains", "deep ocean", "magical forest", "outer space", "African savannah", "a pirate ship",
            "an overgrown garden", "ancient Egypt", "icy tundra", "a haunted castle"]  # on the rainbow ,
heroes = ["a brave mountaineer", "a curious mermaid", "a wise old owl", "an adventurous astronaut", "a daring explorer",
          "a cunning pirate", "a kind gardener", "an archaeologist", "a snowman",
          "a brave knight"]  # Super hero, scientist, robot,
villains = ["a wicked witch", "a fierce dragon", "a sly fox", "an evil emperor", "a rogue robot", "a mischievous gnome",
            "a giant spider", "a space alien", "a ghostly specter", "a mad scientist"]  #
story_types = ["math", "science", "animal sounds", "astronomy", "history"]
ages = [5]

# Generate all combinations
all_combinations = list(product(names, settings, heroes, villains, story_types, ages))

# Setup for intermediate saving
checkpoint_interval = 10
data, last_checkpoint = consolidate_checkpoints()
start_iteration = last_checkpoint + 1

# Generate stories from the start_iteration
for i, combo in tqdm(enumerate(all_combinations[start_iteration:], start=start_iteration), total=len(all_combinations),
                     desc="Generating stories"):
    name, setting, hero, villain, story_type, age = combo
    story_content = generate(name, setting, hero, villain, story_type, age)
    data.append({
        "name": name,
        "setting": setting,
        "hero": hero,
        "villain": villain,
        "story_type": story_type,
        "age": age,
        "content": story_content['content']
    })

    if (i + 1 - start_iteration) % checkpoint_interval == 0 or i + 1 == len(all_combinations):
        df_checkpoint = pd.DataFrame(data[-checkpoint_interval:])
        checkpoint_file_path = f'children_stories_checkpoint_{i + 1}.json'
        df_checkpoint.to_json(checkpoint_file_path, orient='records', indent=4)
        print(f"Checkpoint saved at iteration {i + 1}")

# Combine all data into the final dataset
final_file_path = '../../mojo/children_stories_final.json'
pd.DataFrame(data).to_json(final_file_path, orient='records', indent=4)
print(f"Final stories written to {final_file_path}")

# Delete remaining checkpoint files
checkpoint_files = glob.glob('children_stories_checkpoint_*.json')
for file in checkpoint_files:
    os.remove(file)
    print(f"Deleted checkpoint file: {file}")

print("All checkpoint files have been deleted.")
