import unittest
from generator import Generator
from unittest.mock import patch


class TestStoryGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = Generator()  # Update with your model path

    def test_generate_story(self):
        # Mock Llama responses for isolated testing
        with patch.object(self.generator.llm, "run") as mock_llm:
            mock_llm.return_value = {"choices": [{"text": "This is a mock story"}]}

            story = self.generator.generate_story(
                "Alice", "enchanted forest", "wizard", "dragon", "math", 8
            )
            self.assertIsInstance(story, str)
            self.assertEqual(story, "This is a mock story")  # Assert the mocked response

        # Test for invalid age
        with self.assertRaises(ValueError):
            self.generator.generate_story("Bob", "mountains", "knight", "ogre", "science", -1)

    def test_generate_exercise(self):
        # Provide a mock story for isolated testing
        story = "This is a mock story"
        exercise = self.generator.generate_exercise(story)
        self.assertIsInstance(exercise, str)

    def test_generate_options(self):
        # Provide a mock exercise for isolated testing
        exercise = "What was the name of the evil king in the story?"
        options = self.generator.generate_options(exercise)
        self.assertIsInstance(options, list)
        self.assertEqual(len(options), 3)  # Default number of options
        for option in options:
            self.assertIsInstance(option, str)

    def test_generate_answer(self):
        # Provide mock exercise and options for isolated testing
        exercise = "What color was the dragon's scales?"
        options = ["green", "red", "purple"]
        answer = self.generator.generate_answer(exercise, options)
        self.assertIn(answer, options)
