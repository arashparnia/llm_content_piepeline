

# from openai import OpenAI
# client = OpenAI(api_key=api_key)

# response = client.moderations.create(input="""
#                                      """)

# print(response)
from assistant import OpenAI
import json



# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def moderate_content(content):
    try:
        # Send the content for moderation
        response = client.moderations.create(input=content)

        # Check if all categories are False, set safe to True
        categories = response.results[0].categories.__dict__
        Category_scores = response.results[0].category_scores.__dict__
        boolean_categories = {key: value for key, value in categories.items() if isinstance(value, bool)}
        is_safe = all(value is False for value in boolean_categories.values())


        # Return a dictionary with moderation results and safety flag
        return {
            "moderation_id": response.id,
            "moderation_results_values": Category_scores,
            "moderation_results_boolean": boolean_categories,
            "safe": is_safe
        }
    except Exception as e:
        # Handle any errors that may occur during moderation
        return {
            "error": str(e)
        }

def process_json_file(input_file, output_file, limit=10):
    try:
        # Load JSON data from the input file
        with open(input_file, "r") as json_file:
            data = json.load(json_file)

        # Process each item in the JSON data, limiting to the first 'limit' items
        for item in data[:limit]:
            # Get the content from the item
            content = item.get("content", "")

            # Perform content moderation
            moderation_result = moderate_content(content)

            # Update the item with the moderation result
            item["moderation"] = moderation_result

            # Set the "safe" flag based on moderation results
            item["safe"] = moderation_result["safe"]
        # Save the updated JSON data to the output file
        with open(output_file, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Content moderation completed for the first {limit} items. Updated data saved to {output_file}")
    except Exception as e:
        print("Error:", str(e))



if __name__ == "__main__":
    # Specify the input JSON file and output JSON file
    input_json_file = "../../mojo/children_stories_final.json"
    output_json_file = "../../mojo/children_stories_final_moderated.json"

    # Process the first 10 items in the JSON file and perform content moderation
    process_json_file(input_json_file, output_json_file, limit=-1)
