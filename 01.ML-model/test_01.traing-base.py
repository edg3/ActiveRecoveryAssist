import unittest

from 01.training-base import formatting_prompt

class TestFormattingPrompt(unittest.TestCase):

    def setUp(self):
        self.examples = [
            {
                'context': 'I am feeling sad.',
                'response': 'I am here to help you.'
            },
            {
                'context': 'I am feeling anxious.',
                'response': 'Take a deep breath.'
            }
        ]
        self.data_prompt = """
        You are a super friendly mental health assistant. Your goal is to help victims feel comfortable in any situation with calm and reassuring responses. Always be empathetic, understanding, and supportive.
        """

    def test_return_type(self):
        result = formatting_prompt(self.examples)
        self.assertIsInstance(result, dict)

    def test_keys_in_dictionary(self):
        result = formatting_prompt(self.examples)
        for example in self.examples:
            self.assertIn(example['context'], result)

    def test_values_are_lists(self):
        result = formatting_prompt(self.examples)
        for value in result.values():
            self.assertIsInstance(value, list)

    def test_formatted_strings(self):
        result = formatting_prompt(self.examples)
        for example in self.examples:
            context = example['context']
            response = example['response']
            expected_prompt = f"{self.data_prompt}\n\nContext: {context}\n\nResponse: {response}\n\n"
            self.assertIn(expected_prompt, result[context])

    def test_empty_examples(self):
        result = formatting_prompt([])
        self.assertEqual(result, {})

    def test_single_example(self):
        single_example = [{'context': 'I am feeling happy.', 'response': 'That is great to hear!'}]
        result = formatting_prompt(single_example)
        expected_prompt = f"{self.data_prompt}\n\nContext: I am feeling happy.\n\nResponse: That is great to hear!\n\n"
        self.assertIn(expected_prompt, result['I am feeling happy.'])

    def test_duplicate_contexts(self):
        duplicate_examples = [
            {'context': 'I am feeling sad.', 'response': 'I am here to help you.'},
            {'context': 'I am feeling sad.', 'response': 'It is okay to feel sad sometimes.'}
        ]
        result = formatting_prompt(duplicate_examples)
        self.assertEqual(len(result['I am feeling sad.']), 2)

if __name__ == '__main__':
    unittest.main()