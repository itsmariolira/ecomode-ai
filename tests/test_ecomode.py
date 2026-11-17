import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ecomode import compact_lines, compact_text


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ecomode.py"


class CompactLinesTests(unittest.TestCase):
    def test_removes_repeated_normal_lines(self):
        result = compact_lines(["build ok", "build ok", "done"])

        self.assertEqual(result[:2], ["build ok", "done"])
        self.assertIn("1 linha(s) repetida(s)", result[-1])

    def test_preserves_important_messages_even_when_repeated_and_limited(self):
        result = compact_lines(
            ["normal 1", "normal 2", "WARNING: disk almost full", "ERROR: failed", "ERROR: failed"],
            max_lines=1,
        )

        self.assertIn("WARNING: disk almost full", result)
        self.assertEqual(result.count("ERROR: failed"), 2)
        self.assertNotIn("normal 2", result)

    def test_preserves_python_traceback_details(self):
        text = "Traceback (most recent call last):\n  File \"app.py\", line 7\nValueError: bad value\n"

        self.assertEqual(compact_text(text, max_lines=0).splitlines()[:3], text.splitlines())

    def test_empty_input_stays_empty(self):
        self.assertEqual(compact_text(""), "")


class CliTests(unittest.TestCase):
    def test_cli_reads_stdin(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--max-lines", "1"],
            input="one\ntwo\nERROR: important\n",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 0)
        self.assertIn("one", process.stdout)
        self.assertNotIn("\ntwo\n", process.stdout)
        self.assertIn("ERROR: important", process.stdout)

    def test_cli_reads_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "saída.txt"
            path.write_text("aviso: atenção\nnormal\n", encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(process.returncode, 0)
        self.assertIn("aviso: atenção", process.stdout)


if __name__ == "__main__":
    unittest.main()
