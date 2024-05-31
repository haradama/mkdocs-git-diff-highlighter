import unittest
from mkdocs_git_diff_highlighter.plugin import GitDiffHighlighterPlugin

class TestGitDiffHighlighterPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = GitDiffHighlighterPlugin()
        self.plugin.load_config({'compare_with': 'HEAD'})

    def test_apply_patch_to_content(self):
        # テストデータ
        original_content = "今日は晴れです。\n"
        patch = """diff --git a/1.txt b/1.txt
index c712072..cee7a92 100644
--- a/1.txt
+++ b/1.txt
@@ -1 +1 @@
-今日は晴れです．
+今日は雨です．
"""

        # 期待される結果
        expected_content = "<span style=\"color: red;\">今日は雨です．</span>\n"

        # メソッドをテスト
        modified_content = self.plugin.apply_patch_to_content(original_content, patch)

        # 結果を検証
        self.assertEqual(modified_content, expected_content)

    def test_replace_line(self):
        original_content = "今日は晴れです。\n今日は良い天気です。\n"
        line_num = 1
        new_line = "<span style=\"color: red;\">今日は雨です。</span>"
        
        # 期待される結果
        expected_content = "<span style=\"color: red;\">今日は雨です。</span>\n今日は良い天気です。\n"

        # メソッドをテスト
        modified_content = self.plugin.replace_line(original_content, line_num, new_line)

        # 結果を検証
        self.assertEqual(modified_content, expected_content)

if __name__ == '__main__':
    unittest.main()
