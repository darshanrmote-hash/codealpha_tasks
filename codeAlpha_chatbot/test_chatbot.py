import unittest
from chatbot import get_bot_response, clean_input, GREETING_RESPONSES, STATUS_RESPONSES, JOKES, HELP_MESSAGE

class TestChatbot(unittest.TestCase):

    def test_clean_input(self):
        self.assertEqual(clean_input("  Hello!  "), "hello")
        self.assertEqual(clean_input("How are you?"), "how are you")
        self.assertEqual(clean_input("BYE..."), "bye")

    def test_greetings(self):
        response = get_bot_response("Hello")
        self.assertIn(response, GREETING_RESPONSES)
        
        response = get_bot_response("hey!")
        self.assertIn(response, GREETING_RESPONSES)

    def test_status(self):
        response = get_bot_response("How are you?")
        self.assertIn(response, STATUS_RESPONSES)

    def test_identity(self):
        response = get_bot_response("what is your name?")
        self.assertIn("AlphaBot", response)

    def test_help(self):
        response = get_bot_response("help")
        self.assertEqual(response, HELP_MESSAGE.strip())

    def test_joke(self):
        response = get_bot_response("tell me a joke")
        self.assertTrue(any(joke in response for joke in JOKES))

    def test_farewell(self):
        response = get_bot_response("bye")
        self.assertIn("Goodbye", response)

    def test_fallback(self):
        response = get_bot_response("unknown query 12345")
        self.assertIn("I'm sorry, I didn't quite catch that", response)

if __name__ == "__main__":
    unittest.main()
