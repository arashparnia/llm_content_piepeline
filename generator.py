from llama_cpp import Llama


class Generator:
    """Generates children's stories with exercises, answers, and options."""

    def __init__(self, model_path="model/mistral-7b-instruct-v0.1.Q6_K.gguf"):
        """Initializes the StoryGenerator with the provided model path."""

        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=512,
                n_batch=10,
                n_threads=16,
                n_gpu_layers=-1,
                seed=42,
                use_mlock=True,
            )
        except FileNotFoundError as e:
            raise ValueError(f"Model file not found: {e}")

    def generate_story(self, name, setting, hero, villain, story_type, age):
        """Generates a single story with the given parameters."""

        try:
            story_type_formatted = f"{story_type}"  # Store story_type separately for f-string formatting
            prompt = f"""
            You are a teacher for young children, you turn {story_type_formatted} questions into children's stories.

            Write a 500 characters short story about a {age} year old named {name} who is a {hero}, traveling to {setting} to face {villain}, and uses their {story_type_formatted} skills to defeat them.
            Provide a {story_type_formatted} exercise or a question within the story as a means for learning.
            The story should be short, fantastical, yet exciting, with a happy ending where the hero wins if the exercise is answered correctly.
            """

            output = self.llm(prompt, max_tokens=1024, temperature=0.7, top_p=1.0, top_k=50)
            return output["choices"][0]["text"].strip()
        except Exception as e:
            raise ValueError(f"Answer generation failed: {e}")

    def generate_exercise(self, story_text):
        """Generates an exercise related to the provided story text."""

        try:
            prompt = f"""
            Based on the following story:

            {story_text}

            Generate a multiple-choice question that tests the child's understanding of the story's concepts.
            Provide at least three plausible answer choices.
            """

            output = self.llm(prompt, max_tokens=1024, temperature=0.7, top_p=1.0, top_k=50)
            return output["choices"][0]["text"].strip()

        except Exception as e:
            raise ValueError(f"Answer generation failed: {e}")

    def generate_options(self, exercise_text, num_options=3):
        """Generates answer options for a given exercise text."""

        try:
            prompt = f"""
            Generate {num_options} plausible answer choices for the following exercise:

            {exercise_text}
            """

            output = self.llm(prompt, max_tokens=1024 * num_options, temperature=0.7, top_p=1.0, top_k=50)
            return [choice["text"].strip() for choice in output["choices"]]
        except Exception as e:
            raise ValueError(f"Answer generation failed: {e}")

    def generate_answer(self, exercise_text, options):
        """Identifies the correct answer from a list of options."""

        try:
            newline = "\n"  # Store the newline character separately
            formatted_options = newline.join([f"- {option}" for option in options])

            prompt = f"""
            Given the following exercise:

            {exercise_text}

            And the following answer choices:
            {formatted_options}

            Which is the correct answer?
            """

            output = self.llm(prompt, max_tokens=1024, temperature=0.5, top_p=1.0,
                              top_k=1)  # Lower temperature for accuracy
            return output["choices"][0]["text"].strip()
        except Exception as e:
            raise ValueError(f"Answer generation failed: {e}")
