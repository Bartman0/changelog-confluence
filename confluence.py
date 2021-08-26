import os

from atlassian import Confluence

confluence = Confluence(
    url=os.environ.get('CONFLUENCE_URL'),
    username=os.environ.get('CONFLUENCE_USER'),
    password=os.environ.get('CONFLUENCE_TOKEN'),
    cloud=True)

space = os.environ.get('CONFLUENCE_SPACE')

spaces = confluence.get_all_spaces()

pages = confluence.get_all_pages_from_space(space, start=0)

id_data_warehouse = confluence.get_page_id(space, "Data warehouse")

release_notes = confluence.update_or_create(id_data_warehouse, "Release notes", "Release notes")

led_etl = confluence.update_or_create(release_notes.get('id'), "led-etl", "hier komt dan changelog output")
