from unittest.mock import patch, mock_open

from ..backlinker import parse_sections
from .fixtures.cats import fixture_cats


def test_section_not_present():

  text = """
# Testing Section Not Present

This has some content but there is not a complete section in here.

The word 'SECTION' should not trigger a match.

Out of order tags should not trigger a match, e.g.

<!-- End SECTION -->
out of order
<!-- SECTION -->

Wrong case shouldn't trigger a match, e.g.

<!-- section -->
wrong case
<!-- End section -->

None matching tags shouldn't trigger a match, e.g.

<!-- SECTION -->
out of order
<!-- End WRONG SECTION -->
"""

  sections = parse_sections(text, "SECTION")

  assert sections == []


def test_section_single_line():

  text = """
# Testing Section Present in Single Line

This has some content with a section in it.

<!-- SECTION -->section content here<!-- End SECTION -->

Content after the section

<!-- DIFFERENT SECTION -->
this should not match
<!-- End DIFFERENT SECTION -->
"""

  sections = parse_sections(text, "SECTION")

  assert len(sections) == 1
  assert sections[0]['content'] == "section content here"
  assert text[sections[0]['start']:sections[0]['end']] == "<!-- SECTION -->section content here<!-- End SECTION -->"


def test_section_multiline():

  text = """
# Testing Section Present Multiline

This has some content with a section in it.

<!-- SECTION -->
section content here
<!-- End SECTION -->

Content after the section

<!-- DIFFERENT SECTION -->
this should not match
<!-- End DIFFERENT SECTION -->
"""

  sections = parse_sections(text, "SECTION")

  expected_content = "\nsection content here\n"

  assert len(sections) == 1
  assert sections[0]['content'] == expected_content
  assert text[sections[0]['start']:sections[0]['end']] == f"<!-- SECTION -->{expected_content}<!-- End SECTION -->"


def test_section_appears_twice():

  text = """
# Testing Section Present

This has some content with a section in it.

<!-- SECTION -->
section content here
<!-- End SECTION -->

Content after the section

<!-- DIFFERENT SECTION -->
this should not match
<!-- End DIFFERENT SECTION -->

<!-- SECTION -->
second section of content here

<!-- another comment in the middle -->

multiline
<!-- End SECTION -->

Opening section line should not match
<!-- SECTION -->
"""

  sections = parse_sections(text, "SECTION")

  expected_content_first = "\nsection content here\n"
  expected_content_second = """
second section of content here

<!-- another comment in the middle -->

multiline
"""

  assert len(sections) == 2

  assert sections[0]['content'] == expected_content_first
  assert text[sections[0]['start']:sections[0]['end']] == f"<!-- SECTION -->{expected_content_first}<!-- End SECTION -->"

  assert sections[1]['content'] == expected_content_second
  assert text[sections[1]['start']:sections[1]['end']] == f"<!-- SECTION -->{expected_content_second}<!-- End SECTION -->"


def test_section_drafts_not_exists_kittens(fixture_cats):

  note = fixture_cats['Kittens']['note']

  sections = parse_sections(note.content, 'Drafts')

  assert sections == []


def test_section_drafts_exists_cats(fixture_cats):

  note = fixture_cats['Cats']['note']

  sections = parse_sections(note.content, 'Drafts')

  expected_content = """

## Cats with Jobs

Some cats have jobs, often catching [[Mice]]. A cat that does this on a ship is called a [[Ship's Cat]].

"""

  assert len(sections) == 1
  assert sections[0]['content'] == expected_content
  assert note.content[sections[0]['start']:sections[0]['end']] == f"<!-- Drafts -->{expected_content}<!-- End Drafts -->"
