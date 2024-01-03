prompt_schema = """
**Introduction**: 
"Welcome to the magical world of [Setting], where [Hero], the [Hero Trait] [Animal/Character], and [Sidekick], the clever and witty companion, embark on an incredible journey. In this [Story Type] tale, they aim to teach children about [Exercise Concept], focusing on [Educational Goal]."

**Chapter 1: The Mysterious Challenge**:
"[Hero] and [Sidekick] encounter their first challenge related to [Educational Goal]. In the heart of [Setting], something unusual catches their attention, leading them to a puzzle that only they can solve."

**Chapter 2: The Journey Begins**:
"Our heroes set out across [Setting], meeting various characters who offer them lessons in [Exercise Concept]. Their journey is filled with surprises and mini-exercises that are both fun and educational."

**Chapter 3: The Encounter with [Nemesis]**:
"As [Hero] and [Sidekick] venture deeper into [Setting], they encounter [Nemesis], the [Nemesis Trait] antagonist. A series of events unfold, challenging our heroes with problems that test their wit and bravery."

**Chapter 4: Learning Through Adventure**:
"Throughout their journey, [Hero] and [Sidekick] engage in activities that teach [Age]-appropriate lessons in [Exercise Concept]. These interactive exercises are seamlessly woven into their adventure."

**Chapter 5: The Parental Challenge**:
"Just when our heroes feel confident, they face a complex puzzle (Parental Control Question), designed for adult assistance. This challenge ensures parental involvement and adds an extra layer of learning."

**Chapter 6: Conflict and Resolution in [Setting]**:
"In the climax of their adventure, [Hero] and [Sidekick] must use everything they've learned to overcome the challenges set by [Nemesis]. Their journey highlights the themes of [Emotional Theme], imparting valuable lessons."

**Chapter 7: Interactive Decisions**:
"This part of the story includes interactive elements where readers make choices that influence the outcome. These decisions reinforce the educational content and engage the young reader more deeply."

**Chapter 8: The Journey Home**:
"As [Hero] and [Sidekick] conclude their adventure in [Setting], they reflect on their journey and the lessons learned. The story ends with a heartwarming return to their home, leaving young readers with lasting educational and emotional takeaways."

**Conclusion**:
"The story concludes, reinforcing the main educational goal of [Educational Goal]. Illustrations in the [Illustration Style] style enhance the narrative, making [Setting] come alive. The language level is perfectly suited for [Age]-year-old children, making the story both accessible and engaging."
"""

prompt_10_exercises = """
write 10 exercises that continues and develops the story. answers should be available in the exercises story. each exercise should have a background story that builds on the previous one. you have to use the content of the story to create the questions. the child should be able to answer the questions from the content of story of each exercise. provide their answers and provide multiple choice options with one correct option and 3 incorrect one
"""

prompt_main_story = """
write the story that will be narrated and read out loud. it should be like reading a book. 
"""