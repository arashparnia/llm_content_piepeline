import pandas as pd
import json

# JSON data
json_data = '''{
    "story": "🌲 In the heart of the Farm jungle...",
    "exercises": [
        {"exercise": "Piggy and Elmo heard a soft 'Moo-Moo' 🐮 sound...", "answer": "Cow", "options": {"wrong": ["Chicken", "Duck", "Lion"], "correct": "Cow"}},
        {"exercise": "Next, they stumbled upon a 'Cluck-Cluck' 🐔...", "answer": "Chicken", "options": {"wrong": ["Frog", "Sheep", "Horse"], "correct": "Chicken"}}
    ]
}'''

# Load JSON data into a Python dictionary
data = json.loads(json_data)

# Flatten the exercises and include the story
df = pd.json_normalize(
    data,
    record_path='exercises',
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
    item = {'id': exercise_id}
    for column in df.columns:
        if isinstance(row[column], dict):  # Convert dictionaries to JSON string
            item[column] = json.dumps(row[column])
        else:
            item[column] = row[column]

    # Put item in DynamoDB
    table.put_item(Item=item)

print("Data inserted into DynamoDB.")
