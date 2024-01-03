import json

import pandas as pd

# Assuming the CSV file is uploaded and has columns 'title' and 'content'
csv_file_path = 'data/infantbooks.csv' # Replace with your actual file path

try:
    # Reading the CSV file
    df = pd.read_csv(csv_file_path)

    # Generating training data
    training_data = []
    for index, row in df.iterrows():
        title = row['title']
        content = row['content']

        training_example = {
            "messages": [
                {"role": "system", "content": "You are a children's storybook writer."},
                {"role": "user", "content": f"Write a story titled {title}."},
                {"role": "assistant", "content": content}
            ]
        }
        training_data.append(training_example)

    # Display the first few training data examples
    training_data[:3]
except Exception as e:
    training_data = []
    print(f"Error: {e}")

print(training_data[:3] ) # Displaying the first three examples for preview, if successful

# Save the training data to a JSON file
json_file_path = 'data/training_data.json'
try:
    with open(json_file_path, 'w') as json_file:
        json.dump(training_data, json_file, indent=4)
    print(f"Training data saved successfully to {json_file_path}")
except Exception as e:
    print(f"Error saving training data: {e}")
