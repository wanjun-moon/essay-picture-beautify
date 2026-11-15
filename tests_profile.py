import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "scripts" / "learn_style_profile.py"

class ProfileTests(unittest.TestCase):
    def test_acceptance_learns_only_after_support_threshold(self):
        from importlib.machinery import SourceFileLoader
        module = SourceFileLoader("profile", str(SCRIPT)).load_module()
        records = [
            {"figure_type": "plot", "rating": "accept", "attributes": {"palette": "safe"}},
            {"figure_type": "plot", "rating": "accept", "attributes": {"palette": "safe"}},
            {"figure_type": "plot", "rating": "reject", "attributes": {"palette": "rainbow"}},
        ]
        result = module.build_profile(records, min_support=2)
        self.assertEqual(result["preferences_by_figure_type"]["plot"]["palette"], "safe")
        self.assertFalse(result["privacy"]["contains_raw_manuscript_or_image_data"])

    def test_cli_writes_valid_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            feedback = tmp / "feedback.jsonl"
            output = tmp / "profile.json"
            feedback.write_text(
                '{"figure_type":"plot","rating":"accept","attributes":{"font_family":"Arial"}}\n'
                '{"figure_type":"plot","rating":"accept","attributes":{"font_family":"Arial"}}\n',
                encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPT), str(feedback), "--output", str(output)], check=True)
            profile = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(profile["preferences_by_figure_type"]["plot"]["font_family"], "Arial")

if __name__ == "__main__":
    unittest.main()
