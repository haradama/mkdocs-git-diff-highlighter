import mkdocs.plugins
import git
from unidiff import PatchSet
import os

class GitDiffHighlighterPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('highlight_color', mkdocs.config.config_options.Type(str, default='red')),
        ('comparison_base', mkdocs.config.config_options.Type(str, default='HEAD~1')),
    )

    def on_page_markdown(self, markdown, page, config, files):
        repo_path = config['docs_dir']
        repo = git.Repo(repo_path)
        diff = repo.git.diff(self.config['comparison_base'], os.path.join(repo_path, page.file.src_path), unified=1)
        patch = PatchSet(diff)

        lines_to_highlight = []
        for patched_file in patch:
            for hunk in patched_file:
                for line in hunk:
                    if line.is_added:
                        line_number = line.target_line_no
                        lines_to_highlight.append(line_number)

        # Markdownを更新し、指定された行をハイライト
        new_markdown_lines = []
        for i, markdown_line in enumerate(markdown.split('\n'), 1):
            if i in lines_to_highlight:
                # 追加された行に赤色のスタイルを適用
                highlighted_line = f'<span style="color: {self.config["highlight_color"]};">{markdown_line}</span>'
                new_markdown_lines.append(highlighted_line)
            else:
                new_markdown_lines.append(markdown_line)

        return '\n'.join(new_markdown_lines)  # 更新されたMarkdownを返します

