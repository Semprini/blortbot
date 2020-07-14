import unittest

import os

from blortbot import BlortBot
from commands import COMMANDS


class TestJSONOutput(unittest.TestCase):
    def setUp(self):
        # Get the value for this here: https://twitchapps.com/tmi/
        TOKEN = os.environ["TWITCH_OAUTH_TOKEN"]
        self.bb = BlortBot("blortbot", TOKEN, "blortbot", COMMANDS)

    def test_object_serialise(self):
        self.bb.process_base_msg("1user 2 3 -!blortbot")
        self.bb.process_base_msg("1user 2 3 -!cookie")
        self.bb.process_base_msg("1user 2 3 -!learn kung fu")
        self.bb.process_base_msg("1user 2 3 -@blortbot who was bruce lee's teacher")
        self.bb.process_base_msg("1user 2 3 -@blortbot what are the origins")
