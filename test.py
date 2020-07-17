import unittest

import os

from blortbot import BlortBot


class TestJSONOutput(unittest.TestCase):
    def setUp(self):
        # Get the value for this here: https://twitchapps.com/tmi/
        TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]
        self.bb = BlortBot("blortbot", TOKEN, "blortbot")

    def test_blortbot(self):
        output = self.bb.process_base_msg("1user 2 3 -!blortbot")
        self.assertIsNotNone(output)

    def test_cookie(self):
        output = self.bb.process_base_msg("1user 2 3 -!cookie")
        self.assertIsNotNone(output)

    def test_ai(self):
        self.bb.process_base_msg("1user 2 3 -!learn kung fu")
        self.bb.process_base_msg("1user 2 3 -@blortbot who was bruce lee's teacher")
        output = self.bb.process_base_msg("1user 2 3 -@blortbot what are kung fu's origins")
        self.assertIsNotNone(output)
