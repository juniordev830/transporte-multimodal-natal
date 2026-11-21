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

    def test_rejects_oversized_json_from_file_and_stdin(self):
        from tempfile import TemporaryDirectory
        payload = b" " * 1_000_001
        script = Path(__file__).with_name("app.py")
        with TemporaryDirectory() as directory:
            filename = Path(directory) / "large.json"
            filename.write_bytes(payload)
            for arguments, stdin in (([str(filename)], None), (["-"], payload)):
                with self.subTest(arguments=arguments):
                    result = subprocess.run([sys.executable, str(script), *arguments],
                                            input=stdin, capture_output=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn(b"1 MB", result.stderr)
                    self.assertNotIn(b"Traceback", result.stderr)
