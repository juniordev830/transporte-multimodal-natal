"""The piped CLI should match its existing file-based entry point."""
from pathlib import Path
import subprocess
import sys
import unittest


class StdinInputTest(unittest.TestCase):
    def test_piped_example_matches_file(self):
        example = Path(__file__).with_name("exemplo.json")
        command = [sys.executable, str(example.with_name("app.py"))]
        flags = [[], ['--csv']]
        for arguments in flags:
            with self.subTest(arguments=arguments):
                direct = subprocess.check_output([*command, str(example), *arguments])
                piped = subprocess.check_output([*command, "-", *arguments], input=example.read_bytes())
                self.assertEqual(piped, direct)

    def test_piped_json_preserves_existing_validation(self):
        for payload in [b'{"a": 1, "a": 2}', b"[" * 1500 + b"]" * 1500]:
            with self.subTest(length=len(payload)):
                app = Path(__file__).with_name("app.py")
                result = subprocess.run([sys.executable, str(app), "-"], input=payload, capture_output=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertNotIn(b"Traceback", result.stderr)
