import os
import subprocess
import sys
from pathlib import Path

import pypandoc
from atlassian import Confluence


class ChangelogConfluence:
    def __init__(self, space, module_path):
        self._module_path = module_path
        self._confluence = Confluence(
            url=os.environ.get('CONFLUENCE_URL'),
            username=os.environ.get('CONFLUENCE_USER'),
            password=os.environ.get('CONFLUENCE_TOKEN'),
            cloud=True)
        self._space = space

    def create_path(self):
        self._path_ids = list()
        last_path = None
        for i, path in enumerate(self._module_path.split('/')):
            if i == 0:
                page_id = self._confluence.get_page_id(self._space, path)
            else:
                page_id = self._confluence.update_or_create(self._path_ids[i-1], path, "", representation='wiki').get('id')
            self._path_ids.append(page_id)
            last_path = path
        return self._path_ids[-1], last_path

    def update_page(self, page_id, title, body):
        return self._confluence.update_page(page_id, title, body, representation='wiki')


def main():
    if len(sys.argv) != 3:
        print("usage: changelog-confluence space page_path")
        return 1
    if not Path(".git").exists():
        print("this directory is not a working copy")
        return 1
    command = "git-chglog"
    chglog = subprocess.run([command], capture_output=True, text=True)
    if chglog.returncode != 0:
        print(f"git-chglog command failed (exit code {chglog.returncode})")
        print(f"{chglog.stderr}")
        return 1
    space = sys.argv[1]
    module_path = sys.argv[2]

    # get page id for changelog
    changelog = ChangelogConfluence(space, module_path)
    page_id, title = changelog.create_path()

    # convert chglog markdown output to jira wiki and update the target page
    output = pypandoc.convert_text(chglog.stdout, 'jira', format='markdown_strict')
    changelog.update_page(page_id, title, output)


if __name__ == "__main__":
    exit(main())