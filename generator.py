from llama_cpp import Llama


class Generator:
    """Generates children's stories with exercises, answers, and options."""

    # def __init__(self, model_path="model/mistral-7b-instruct-v0.1.Q6_K.gguf"):
    # def __init__(self, model_path="model/dolphin-2.5-mixtral-8x7b.Q6_K.gguf"):
    # def __init__(self, model_path="model/dolphin-2.5-mixtral-8x7b.Q4_K_M.gguf"):
    def __init__(self, model_path="model/mixtral-8x7b-instruct-v0.1.Q6_K.gguf"):
        """Initializes the StoryGenerator with the provided model path."""

        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_batch=1024,
                n_threads=16,
                n_gpu_layers=0,
                seed=42,
                use_mlock=False,
            )
            # Llama(model_path=model, n_ctx=512, n_batch=512, n_threads=12, n_gpu_layers=-1, verbose=True, seed=42,
            #       use_mlock=True)

        except FileNotFoundError as e:
            raise ValueError(f"Model file not found: {e}")

    def generate_story(self, name, setting, hero, villain, story_type, age):
        """Generates a single story with the given parameters."""

        try:
            name = "Kian"  # Name of the child audience
            setting = "Jungle"  # Story setting
            hero = "Scientist"  # Main character
            villain = "Banana bandit"  # Antagonist or challenge
            story_type = "math"  # Type of educational content
            age = 4  # Age of target audience
            math_concept = "basic arithmetic"  # Specific math concept
            sidekick = "Robo, the Robot Companion"  # Sidekick character
            hero_trait = "curious and brave"  # Hero's traits
            villain_trait = "smelly and rotten"  # Villain's trait
            narrative_style = "Story teller"  # Narrative style
            conflict_resolution = "using math skills"  # Conflict resolution method
            emotional_theme = "courage and friendship"  # Emotional theme
            educational_goal = "introduce basic arithmetic"  # Educational goal

            system_prompt = f"""
            ### Generalized Story Development Plan for an Educational Narrative

            
            #### 1. **Detailed Setting Introduction:**
               - **Environment Description:** A vivid depiction of `{setting}` including celestial bodies and unique phenomena.
               - **Backstory:** Historical and cultural background of `{setting}`.
               - **Daily Life:** Day-to-day experiences in `{setting}`, relatable and engaging for `{name}`.
            
            #### 2. **In-Depth Character Profiles:**
               - **Hero Backstory:** `{hero}`'s upbringing, motivations, and embodiment of `{hero_trait}`.
               - **Sidekick Introduction:** Origin and skills of `{sidekick}`, and their synergy with `{hero}`.
               - **Villain Characteristics:** Nature and role of `{villain}`, including their `{villain_trait}`.
            
            #### 3. **Complex Conflict and Challenges:**
               - **Initial Problem:** A challenge involving `{villain}`.
               - **Series of Challenges:** Various scenarios each focusing on a different aspect of `{math_concept}`.
               - **Character Development:** Each challenge enhances the story arc and character growth.
            
            #### 4. **Educational and Engaging Dialogue:**
               - **Dialogue Scripting:** Conversational introduction of `{math_concept}`.
               - **Plot Progression:** Dialogues that advance the storyline and reveal traits.
               - **Educational Explanations:** `{hero}` or `{sidekick}` articulating `{math_concept}` concepts.
            
            #### 5. **Climactic Build-Up and Resolution:**
               - **Climax Design:** A test of `{hero}`'s `{math_concept}` skills and emotional strength.
               - **Resolution Planning:** `{hero}` applies knowledge to defeat `{villain}`.
               - **Satisfying Conclusion:** Upholding story themes in climax and resolution.
            
            #### 6. **Embedding Moral and Educational Values:**
               - **Moral Lessons:** Themes of friendship, courage, and perseverance.
               - **Educational Progression:** Reinforcing `{math_concept}` throughout the narrative.
            
            #### 7. **Detailed Emotional Landscape:**
               - **Emotional Depth:** Detailed depiction of characters' emotions.
               - **Engagement Tool:** Using emotions to enhance audience connection and character depth.
            
            #### 8. **Narrative and Educational Balance:**
               - **Balancing Act:** Equilibrium between fantasy elements and educational content.
               - **Age Appropriateness:** Tailoring the story to be suitable for `{name}`'s age and interests.

            Remember, the story should not only teach {math_concept} but also instill important life values. Each 
            chapter should be a mini-adventure, contributing to the larger narrative, and keeping {name} captivated 
            throughout.
            The reader should have an unsolved question to think about and solve after every chapter
            The narrative of the story and wording should be at the level of a {age} year old. 
            
            ### Tailored Story Outline
            
            #### **Customizable Story Outline**
            - **Chapter 1:** Introduction to `{setting}`, with an arithmetic puzzle related to its features.
            - **Chapter 2:** `{hero}` and `{sidekick}` facing a `{math_concept}` challenge.
            - **Chapter 3-5:** Progressive `{math_concept}` challenges involving `{villain}`.
            - **Chapter 6:** Emotional growth of `{hero}` and `{sidekick}` through challenges.
            - **Chapter 7:** Climactic `{math_concept}` puzzle against `{villain}`.
            - **Chapter 8:** Resolution highlighting the journey and lessons learned.
            
            This template provides a structured approach to creating an educational and entertaining story for `{name}`, focusing on `{math_concept}` while also instilling important life values. Each chapter is designed as a mini-adventure, ensuring `{name}` stays engaged throughout.

            """

            user_prompt = f"""
Use the template to write a story
"""

            prompt = f"<s>[INST] {system_prompt} [/INST]</s>{user_prompt}"
            prompt = f"""
            <s> [INST] {system_prompt}[/INST] Model answer</s> [INST] {user_prompt}[/INST]

            """
            print("===========================================================================================")
            print(prompt)
            print("===========================================================================================")
            output = self.llm(prompt, max_tokens=512, temperature=0.7, top_p=1.0, top_k=50)
            return output["choices"][0]["text"].strip()
        except Exception as e:
            raise ValueError(f"Answer generation failed: {e}")

    def generate_exercise(self, story_text, name, setting, hero, villain, story_type, age):
        """Generates an exercise related to the provided story text."""

        pass

    def generate_options(self, exercise_text, num_options=3):
        """Generates answer options for a given exercise text."""

        pass

    def generate_answer(self, exercise_text, options):
        """Identifies the correct answer from a list of options."""

        pass
