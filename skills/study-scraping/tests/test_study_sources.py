import argparse
import importlib.util
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error


SCRIPT = Path(__file__).parents[1] / "scripts" / "study_sources.py"
SPEC = importlib.util.spec_from_file_location("study_sources", SCRIPT)
study = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(study)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class StudySourcesTests(unittest.TestCase):
    def test_environment_status_is_boolean_only(self):
        with patch.dict(os.environ, {"TIKHUB_API_KEY": "secret-token"}, clear=True):
            self.assertEqual(
                study.environment_status(),
                {"TIKHUB_API_KEY": {"available": True}},
            )

    def test_parse_params_rejects_malformed_values(self):
        with self.assertRaises(ValueError):
            study.parse_params(["missing-separator"])

    def test_endpoint_validation_rejects_private_or_unknown_routes(self):
        for path in (
            "/api/v1/instagram/private/messages",
            "/api/v1/instagram/v3/login",
            "/api/v1/temp_mail/inbox",
        ):
            with self.subTest(path=path):
                with self.assertRaises(study.SafetyError):
                    study.validate_endpoint(path)

    def test_request_retries_server_errors_three_times(self):
        attempts = []

        def opener(request, timeout):
            attempts.append((request.full_url, timeout))
            if len(attempts) < 3:
                raise urllib.error.HTTPError(request.full_url, 500, "server", {}, None)
            return FakeResponse({"ok": True})

        result = study.request_json(
            "/api/v1/youtube/web_v2/get_video_info",
            {"video_id": "abc"},
            api_key="token",
            opener=opener,
            sleeper=lambda _: None,
        )

        self.assertEqual(result, {"ok": True})
        self.assertEqual(len(attempts), 3)

    def test_request_stops_immediately_on_403_or_429(self):
        for status in (403, 429):
            attempts = []

            def opener(request, timeout, status=status):
                attempts.append(status)
                raise urllib.error.HTTPError(
                    request.full_url, status, "blocked", {}, None
                )

            with self.subTest(status=status):
                with self.assertRaises(study.SafetyError):
                    study.request_json(
                        "/api/v1/instagram/v3/get_user_posts",
                        {"username": "creator"},
                        api_key="token",
                        opener=opener,
                        sleeper=lambda _: None,
                    )
                self.assertEqual(len(attempts), 1)

    def test_youtube_search_normalizes_to_contract(self):
        payload = {
            "data": {
                "items": [
                    {
                        "videoId": "abc123",
                        "title": "Agent tutorial",
                        "channelTitle": "AI Builder",
                        "publishedAt": "2026-07-09T10:00:00Z",
                        "viewCount": "4200",
                    }
                ]
            }
        }

        packet = study.build_packet("AI agents", "youtube", "search", payload, limit=5)

        self.assertEqual(packet["schema_version"], "research.v1")
        self.assertEqual(packet["source_cards"][0]["collector"], "tikhub")
        self.assertEqual(packet["source_cards"][0]["platform"], "youtube")
        self.assertEqual(packet["source_cards"][0]["metrics"]["views"], 4200)

    def test_youtube_nested_renderer_fields_normalize_cleanly(self):
        payload = {
            "data": {
                "contents": [
                    {
                        "videoId": "nested123",
                        "title": {"runs": [{"text": "AI Agents, Clearly Explained"}]},
                        "shortBylineText": {"runs": [{"text": "Jeff Su"}]},
                        "viewCountText": {"simpleText": "4,589,935 views"},
                        "publishedTimeText": {"simpleText": "1 year ago"},
                    }
                ]
            }
        }

        packet = study.build_packet("AI agents", "youtube", "search", payload, limit=1)
        card = packet["source_cards"][0]

        self.assertEqual(card["title_or_text"], "AI Agents, Clearly Explained")
        self.assertEqual(card["author"], "Jeff Su")
        self.assertEqual(card["metrics"]["views"], 4589935)

    def test_instagram_profile_and_posts_normalize(self):
        profile = {
            "data": {
                "user": {
                    "id": "77",
                    "username": "creator",
                    "full_name": "Creator",
                    "biography": "AI workflows",
                    "follower_count": 12000,
                }
            }
        }
        posts = {
            "data": {
                "items": [
                    {
                        "code": "POST1",
                        "username": "creator",
                        "caption": {"text": "Three agent lessons"},
                        "like_count": 300,
                        "comment_count": 20,
                        "play_count": 9000,
                    }
                ]
            }
        }

        profile_packet = study.build_packet(
            "Creator profile", "instagram", "profile", profile, limit=1
        )
        posts_packet = study.build_packet(
            "Creator posts", "instagram", "posts", posts, limit=5
        )

        self.assertEqual(
            profile_packet["source_cards"][0]["source_url"],
            "https://www.instagram.com/creator/",
        )
        self.assertEqual(posts_packet["source_cards"][0]["metrics"]["plays"], 9000)

    def test_reddit_search_normalizes_and_blocks_nsfw_default(self):
        payload = {
            "data": {
                "items": [
                    {
                        "id": "post1",
                        "title": "How founders use agents",
                        "permalink": "/r/ArtificialInteligence/comments/post1/example/",
                        "subreddit": "ArtificialInteligence",
                        "score": 90,
                        "num_comments": 12,
                    }
                ]
            }
        }

        packet = study.build_packet(
            "Founder agent objections", "reddit", "search", payload, limit=5
        )

        self.assertEqual(packet["source_cards"][0]["platform"], "reddit")
        self.assertTrue(
            packet["source_cards"][0]["source_url"].startswith(
                "https://www.reddit.com/"
            )
        )
        self.assertEqual(
            study.command_params("reddit-search", query="agents")["allow_nsfw"], 0
        )

    def test_limit_and_budgets_are_required_positive_values(self):
        with self.assertRaises(ValueError):
            study.validate_budgets(limit=0, page_budget=1, deep_fetch_limit=0)
        with self.assertRaises(ValueError):
            study.validate_budgets(limit=5, page_budget=0, deep_fetch_limit=0)
        self.assertEqual(
            study.validate_budgets(limit=5, page_budget=2, deep_fetch_limit=1),
            {"limit": 5, "page_budget": 2, "deep_fetch_limit": 1},
        )

    def test_collect_pages_stops_at_page_budget(self):
        responses = [
            {
                "data": {
                    "items": [{"code": "ONE", "caption": "One"}],
                    "after": "cursor-2",
                }
            },
            {
                "data": {
                    "items": [{"code": "TWO", "caption": "Two"}],
                    "after": "cursor-3",
                }
            },
            {"data": {"items": [{"code": "THREE", "caption": "Three"}]}},
        ]
        calls = []

        def requester(path, params, **_):
            calls.append(dict(params))
            return responses[len(calls) - 1]

        pages = study.collect_pages(
            "/api/v1/instagram/v3/get_user_posts",
            {"username": "creator"},
            platform="instagram",
            page_budget=2,
            api_key="token",
            requester=requester,
        )

        self.assertEqual(len(pages), 2)
        self.assertEqual(calls[1]["after"], "cursor-2")

    def test_generic_public_comment_route_normalizes_text_evidence(self):
        payload = {
            "data": {
                "comments": [
                    {
                        "id": "comment-1",
                        "text": "Setup is difficult for small teams",
                        "author": "operator",
                        "like_count": 18,
                    }
                ]
            }
        }

        packet = study.build_packet(
            "Audience objections",
            "youtube",
            "comments",
            payload,
            limit=5,
        )

        self.assertEqual(len(packet["source_cards"]), 1)
        self.assertEqual(
            packet["source_cards"][0]["title_or_text"],
            "Setup is difficult for small teams",
        )

    def test_execute_high_level_command_does_not_pass_command_twice(self):
        args = argparse.Namespace(
            command="youtube-search",
            query="AI agents",
            limit=1,
            page_budget=1,
            deep_fetch_limit=0,
        )
        with (
            patch.object(study, "require_api_key", return_value="token"),
            patch.object(
                study,
                "collect_pages",
                return_value={"data": {"items": []}},
            ) as collect_pages,
        ):
            packet = study.execute(args)

        self.assertEqual(packet["schema_version"], "research.v1")
        self.assertEqual(
            collect_pages.call_args.args[0],
            "/api/v1/youtube/web_v2/get_general_search",
        )


if __name__ == "__main__":
    unittest.main()
