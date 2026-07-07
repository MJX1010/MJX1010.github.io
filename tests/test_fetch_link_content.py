import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import fetch_link_content as fetcher  # noqa: E402


class WechatFetchTests(unittest.TestCase):
    def test_wechat_verification_page_is_rejected(self):
        html = """
        <html>
          <head><title>微信公众平台安全验证</title></head>
          <body>验证码 请点击下方按钮继续访问</body>
        </html>
        """

        with patch.object(fetcher, "http_get", return_value=(True, html, "")):
            ok, content, error = fetcher.try_wechat_public_html("https://mp.weixin.qq.com/s/demo", 5)

        self.assertFalse(ok)
        self.assertEqual(content, "")
        self.assertEqual(error, "wechat page requires verification or client context")

    def test_wechat_deleted_article_is_rejected(self):
        html = """
        <html>
          <head><title>微信公众号文章</title></head>
          <body>该内容已被发布者删除</body>
        </html>
        """

        with patch.object(fetcher, "http_get", return_value=(True, html, "")):
            ok, content, error = fetcher.try_wechat_public_html("https://mp.weixin.qq.com/s/deleted", 5)

        self.assertFalse(ok)
        self.assertEqual(content, "")
        self.assertEqual(error, "wechat page requires verification or client context")


class BilibiliFetchTests(unittest.TestCase):
    def test_bilibili_api_error_is_reported(self):
        payload = '{"code": -404, "message": "啥都木有"}'

        with patch.object(fetcher, "http_get", return_value=(True, payload, "")):
            ok, content, error = fetcher.try_bilibili_api("https://www.bilibili.com/video/BV1GbkBBKEDo", 5)

        self.assertFalse(ok)
        self.assertEqual(content, "")
        self.assertEqual(error, "啥都木有")

    def test_b23_short_link_resolves_before_api_fetch(self):
        payload = """
        {
          "code": 0,
          "data": {
            "title": "短链视频",
            "owner": {"name": "UP 主"},
            "duration": 12,
            "desc": "公开视频简介"
          }
        }
        """

        with (
            patch.object(
                fetcher,
                "resolve_final_url",
                return_value="https://www.bilibili.com/video/BV1GbkBBKEDo/",
            ) as resolve_mock,
            patch.object(fetcher, "http_get", return_value=(True, payload, "")),
        ):
            ok, content, error = fetcher.try_bilibili_api("https://b23.tv/demo", 5)

        self.assertTrue(ok)
        self.assertEqual(error, "")
        self.assertIn("# 短链视频", content)
        resolve_mock.assert_called_once_with("https://b23.tv/demo", 5)

    def test_bilibili_kind_fetch_falls_back_to_ytdlp_when_api_fails(self):
        with (
            patch.object(fetcher, "try_bilibili_api", return_value=(False, "", "api blocked")),
            patch.object(fetcher, "try_ytdlp_metadata", return_value=(True, "# yt-dlp video", "")),
        ):
            ok, content, method, error = fetcher.try_kind_specific_fetch(
                "https://www.bilibili.com/video/BV1GbkBBKEDo", "bilibili", 5
            )

        self.assertTrue(ok)
        self.assertEqual(content, "# yt-dlp video")
        self.assertEqual(method, "yt-dlp")
        self.assertEqual(error, "api blocked")

    def test_bilibili_kind_fetch_keeps_api_content_when_ytdlp_fails(self):
        with (
            patch.object(fetcher, "try_bilibili_api", return_value=(True, "# api video", "")),
            patch.object(fetcher, "try_ytdlp_metadata", return_value=(False, "", "yt-dlp not installed")),
        ):
            ok, content, method, error = fetcher.try_kind_specific_fetch(
                "https://www.bilibili.com/video/BV1GbkBBKEDo", "bilibili", 5
            )

        self.assertTrue(ok)
        self.assertEqual(content, "# api video")
        self.assertEqual(method, "bilibili-api")
        self.assertEqual(error, "yt-dlp not installed")


if __name__ == "__main__":
    unittest.main()
