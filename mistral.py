from llama_cpp import Llama
model = "mistral-7b-instruct-v0.1.Q6_K.gguf"  # instruction model
llm = Llama(model_path=model, n_ctx=8192, n_batch=512, n_threads=16, n_gpu_layers=40, verbose=True, seed=42)
def generate(name,setting,character,excercise):
    system = f"""
    You are a  teacher for young children, you turn {excercise} questions into children stories.
    """

    user = f"""
    Write a story about a 4 year old boy names {name} who is traveling to {setting} to face {character} and he uses his {excercise} skills to defeat them. 
    return a json with keys (story,excercise and answer ) 

    """

    message = f"<s>[INST] {system} [/INST]</s>{user}"
    output = llm(message, echo=True, stream=False, max_tokens=4096)
    print(output['usage'])
    output = output['choices'][0]['text'].replace(message, '')
    return (output)

l = [
    ("Oliver", "mountains", "a brave mountaineer", "climbing"),
    ("Sophia", "deep ocean", "a curious mermaid", "swimming"),
    ("Ethan", "magical forest", "a wise old owl", "flying"),
    ("Emma", "outer space", "an adventurous astronaut", "spacewalking"),
    ("Noah", "African savannah", "a daring explorer", "safari trekking"),
    ("Ava", "a pirate ship", "a cunning pirate", "sailing"),
    ("Liam", "an overgrown garden", "a kind gardener", "gardening"),
    ("Mia", "ancient Egypt", "an archaeologist", "exploring"),
    ("Jacob", "icy tundra", "a snowman", "skiing"),
    ("Isabella", "a haunted castle", "a brave knight", "sword fighting"),
    ("Aiden", "dense jungle", "a jungle researcher", "hiking"),
    ("Emily", "a land of sweets", "a gingerbread man", "running"),
    ("Jack", "a mystical cave", "a fearless dragon", "flying"),
    ("Zoe", "a distant planet", "an alien", "teleporting"),
    ("Luke", "futuristic city", "a robot", "coding"),
    ("Grace", "sunken city", "a treasure hunter", "diving"),
    ("Daniel", "different time periods", "a time traveler", "time traveling"),
    ("Lily", "wizardry school", "a young wizard", "spell casting"),
    ("Matthew", "a giant's house", "a tiny fairy", "hiding"),
    ("Charlotte", "galaxy", "a space racer", "space racing")
]

for name,setting,character,excercise in l:
    print(generate(name,setting,character,excercise))