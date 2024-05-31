import pytest
from unittest.mock import patch, MagicMock
from mkdocs_git_diff_highlighter.plugin import GitDiffHighlighterPlugin

@pytest.fixture
def plugin():
    plugin = GitDiffHighlighterPlugin()
    plugin.config['compare_with'] = 'HEAD'
    plugin.config['highlight_color'] = '#FF0000'
    return plugin

@pytest.fixture
def page_mock():
    page = MagicMock()
    page.file.src_path = 'path/to/file.md'
    return page

def test_git_diff_called_correctly(plugin, page_mock):
    with patch('subprocess.run') as mock_run:
        # Setup mock return value
        mock_run.return_value = MagicMock(returncode=0, stdout='''+added line\n''')

        # Execute
        output = plugin.on_post_page('<p>Original content</p>', page_mock)

        # Assert command was called correctly
        mock_run.assert_called_with(['git', 'diff', 'HEAD', '--', 'path/to/file.md'], capture_output=True, text=True)
        assert '<span style="color: #FF0000;">added line</span>' in output

def test_no_diffs_no_change(plugin, page_mock):
    with patch('subprocess.run') as mock_run:
        # Setup mock return value
        mock_run.return_value = MagicMock(returncode=0, stdout='')

        # Execute
        output = plugin.on_post_page('<p>Original content</p>', page_mock)

        # Assert no changes made to output content
        assert output == '<p>Original content</p>'

def test_error_in_git_command(plugin, page_mock):
    with patch('subprocess.run') as mock_run:
        # Setup mock return value
        mock_run.return_value = MagicMock(returncode=1, stdout='', stderr='error')

        # Execute
        output = plugin.on_post_page('<p>Original content</p>', page_mock)

        # Assert no changes made to output content and handle errors gracefully
        assert output == '<p>Original content</p>'
