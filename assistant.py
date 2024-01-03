import openai.types.beta
from openai import OpenAI
import time

import time
from tqdm import tqdm


def wait_on_run(client, run, thread):
    with tqdm(total=100, desc="Run Progress", bar_format="{l_bar}{bar}{r_bar}") as pbar:
        while run.status == "queued" or run.status == "in_progress":
            run = client.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            # Update the progress bar based on some logic
            pbar.update(10)  # Example update, adjust as needed
            time.sleep(5)

    pbar.close()
    return run


def generate_educational_story(api_key, assistant_id, inputs):
    client = OpenAI(api_key=api_key).beta  # Create client with API key

    # Create a new thread
    thread = client.threads.create()

    message = client.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=inputs['system_prompt'],
    )

    # Create a message to append to our thread
    message = client.threads.messages.create(
        thread_id=thread.id, role="user", content=inputs['user_prompt']
    )

    assistant = client.assistants.retrieve(assistant_id)

    run = client.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    run = wait_on_run(client, run, thread)

    # Retrieve all the messages added after our last user message
    messages = client.threads.messages.list(
        thread_id=thread.id, order="asc", after=message.id
    )

    return messages


# Define the story details
story_details = {
    "name": "Liana",
    "setting": "Farm",
    "hero": "piggy",
    "nemesis": "eagle",
    "story_type": "animal sounds",
    "age": 1,
    "exercise_concept": "teaching babies to talk",
    "sidekick": "Elmo",
    "hero_trait": "curious and brave",
    "nemesis_trait": "watch up",
    "narrative_style": "Story teller",
    "conflict_resolution": "using animal sounds",
    "emotional_theme": "courage and friendship",
    "educational_goal": "learn animal sounds"
}

system_prompt = """ """

user_prompt = f"Please craft a story using {story_details}"

# Inputs for the story
inputs = {
    "system_prompt": system_prompt,
    "user_prompt": user_prompt,
}

# Example usage (replace with your actual API key and Assistant ID)
api_key =  # Replace with your API key
assistant_id =  # Replace with your Assistant ID
response = generate_educational_story(api_key, assistant_id, inputs)

for part in response:
    print('PARTS')
    print(part)

import pandas as pd
import json

json_string = ""
thread_message = ""
for thread_message in response:
    thread_message = thread_message
    json_string = thread_message.content[0].text.value  # Adjust the path as per the actual object structure
    # Rest of the parsing logic goes here...
# print(json_string)

json_string_cleaned = json_string.replace('```json\n', '').replace('\n```', '')
data = json.loads(json_string_cleaned)


# Dynamically find the record path
potential_keys = ['exercises', 'exercises_and_answers', 'questions', 'items']  # Add other potential keys as needed
record_path = next((key for key in potential_keys if key in data), None)

if record_path is None:
    raise KeyError("None of the expected keys found in JSON data")


# Flatten the exercises and include the story
df = pd.json_normalize(
    data,
    record_path=record_path,
    meta='story',
    record_prefix='exercise_'
)

# Adjust display settings to show all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Display the DataFrame
print(df)

import boto3
import json
import uuid

# Initialize a DynamoDB client
import boto3

session = boto3.Session(region_name='us-east-1')
dynamodb = session.resource('dynamodb')


# Get the DynamoDB table
table = dynamodb.Table('magical-academy')

# Iterate over DataFrame rows
for index, row in df.iterrows():
    # Generate a unique ID for each exercise
    exercise_id = str(uuid.uuid4())

    # Create a dictionary with column names as keys
    item = {'id': exercise_id,
            'thread_message_metadata': json.dumps({
                "thread_message_id": thread_message.id,
                "object": thread_message.object,
                "created_at": thread_message.created_at,
                "thread_id": thread_message.thread_id,
                "role": thread_message.role,
                "file_ids": thread_message.file_ids,
                "assistant_id": thread_message.assistant_id,
                "run_id": thread_message.run_id,
                "metadata": thread_message.metadata
            })}
    for column in df.columns:
        if isinstance(row[column], dict):  # Convert dictionaries to JSON string
            item[column] = json.dumps(row[column])
        else:
            item[column] = row[column]

    # Put item in DynamoDB
    table.put_item(Item=item)

print("Data inserted into DynamoDB.")
