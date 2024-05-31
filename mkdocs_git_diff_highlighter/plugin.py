import subprocess
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import re

class GitDiffHighlighterPlugin(BasePlugin):
    config_scheme = (
        ('compare_with', config_options.Type(str, default='HEAD')),
        ('highlight_color', config_options.Type(str, default='#FF0000')),  # RGB形式でカラーを指定
    )

    def on_post_page(self, output_content, page):
        # Git Diffコマンドを実行
        compare_with = self.config['compare_with']
        highlight_color = self.config['highlight_color']
        command = ["git", "diff", compare_with, "--", page.file.src_path]
        result = subprocess.run(command, capture_output=True, text=True)

        # 差分がある場合、HTMLに適用
        if result.returncode == 0 and result.stdout:
            diffs = self.extract_diffs(result.stdout)
            for diff in diffs:
                # HTMLコンテンツ内の対応するテキストを指定されたカラーでハイライト
                output_content = re.sub(re.escape(diff), f'<span style="color: {highlight_color};">{diff}</span>', output_content)

        return output_content

    def extract_diffs(self, git_output):
        # Gitの出力から差分のテキストを抽出
        diffs = []
        lines = git_output.split('\n')
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                # '+'で始まる行は追加された行
                diffs.append(line[1:])  # 先頭の'+'を削除
        return diffs
