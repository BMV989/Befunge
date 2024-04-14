from io import StringIO
from unittest.mock import patch

from src.befunge_interpreter import befunge_interpreter, parse_befunge_file
import unittest


class TestBefunge(unittest.TestCase):

    def test_parse_befunge_file_hello_world(self):
        self.assertEqual(parse_befunge_file("../examples/hello.bf"), [
            ['>', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'v'],
            ['v', ' ', ' ', ',', ',', ',', ',', ',', '"', 'H', 'e', 'l', 'l', 'o', '"', '<'],
            ['>', '4', '8', '*', ',', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'v'],
            ['v', ',', ',', ',', ',', ',', ',', '"', 'W', 'o', 'r', 'l', 'd', '!', '"', '<'],
            ['>', '2', '5', '*', ',', '@']
        ])

    def test_parse_befunge_file_another_hello_world(self):
        self.assertEqual(parse_befunge_file("../examples/another_hello.bf"), [
            [' ', '>', '2', '5', '*', '"', '!', 'd', 'l', 'r', 'o', 'w', ' ', ',', 'o', 'l', 'l', 'e', 'H', '"', ':',
             'v'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'v', ':', ',',
             '_', '@'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '>', ' ', ' ',
             '^']
        ])

    def test_hello_world(self):
        with patch("sys.stdout", new=StringIO()) as stdout:
            befunge_interpreter(parse_befunge_file("../examples/hello.bf"))
            self.assertEqual(stdout.getvalue(), "Hello World!\n")

    def test_another_hello_world(self):
        with patch("sys.stdout", new=StringIO()) as stdout:
            befunge_interpreter(parse_befunge_file("../examples/another_hello.bf"))
            self.assertEqual(stdout.getvalue(), "Hello, world!\n")

    def test_yet_another_hello_world(self):
        with patch("sys.stdout", new=StringIO()) as stdout:
            befunge_interpreter(parse_befunge_file("../examples/yet_another_hello.bf"))
            self.assertEqual(stdout.getvalue(), "Hello World!")
