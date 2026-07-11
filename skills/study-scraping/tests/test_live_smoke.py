import importlib.util
import os
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "study_sources.py"
SPEC = importlib.util.spec_from_file_location("study_sources_live", SCRIPT)
study = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(study)
study.load_env()


@unittest.skipUnless(os.environ.get("TIKHUB_API_KEY"), "TIKHUB_API_KEY not configured")
class TikHubLiveSmokeTests(unittest.TestCase):
    def test_youtube_search_returns_a_contract(self):
        payload = study.request_json(
            study.COMMANDS["youtube-search"][0],
            study.command_params("youtube-search", query="AI agents"),
            api_key=os.environ["TIKHUB_API_KEY"],
        )
        packet = study.build_packet(
            "TikHub live smoke: AI agents",
            "youtube",
            "search",
            payload,
            limit=1,
        )
        self.assertEqual(packet["schema_version"], "research.v1")


if __name__ == "__main__":
    unittest.main()
