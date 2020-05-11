from unittest.mock import patch, mock_open

from ..backlinker import Note, exclude_sections_from_notes
from .fixtures.cats import fixture_cats


def test_none_present(fixture_cats):
  """
  Test with labels that are not present -- nothing should change
  """

  notes = fixture_cats['notes'].values()
  exclusions = ["Nothing", "Present"]

  original_contents = list(map(lambda n: n.content, notes))

  exclude_sections_from_notes(notes, exclusions)

  updated_contents = list(map(lambda n: n.content, notes))

  assert original_contents == updated_contents


def test_exclude_drafts_keep_todo(fixture_cats):
  """
  Test excluding Drafts but not TODO -- only that note should have its content changed
  """

  notes = fixture_cats['notes'].values()
  exclusions = ["Drafts", "Not Present"]

  original_contents = list(map(lambda n: n.content, filter(lambda n: n.title != "Cats", notes)))

  exclude_sections_from_notes(notes, exclusions)

  updated_contents = list(map(lambda n: n.content, filter(lambda n: n.title != "Cats", notes)))

  assert original_contents == updated_contents  # unchanged for everything that isn't 'Cats'
  assert fixture_cats['Cats']['note'].content == fixture_cats['Cats']['content_without_section']


def test_exclude_drafts_todo(fixture_cats):
  """
  Test excluding both Drafts and TODO -- two notes in question should be changed
  """

  notes = fixture_cats['notes'].values()
  exclusions = ["Drafts", "TODO"]

  original_contents = list(map(lambda n: n.content, filter(lambda n: n.title != "Cats" and n.title != "Ship's Cat", notes)))

  exclude_sections_from_notes(notes, exclusions)

  updated_contents = list(map(lambda n: n.content, filter(lambda n: n.title != "Cats" and n.title != "Ship's Cat", notes)))

  assert original_contents == updated_contents  # unchanged for everything that isn't 'Cats'
  assert fixture_cats['Cats']['note'].content == fixture_cats['Cats']['content_without_section']
  assert fixture_cats['Ship\'s Cat']['note'].content == fixture_cats['Ship\'s Cat']['content_without_section']


def test_exclude_section_appearing_twice():
  """
  Test excluding a section that appears twice in a Note
  """

  note = Note("test.md")
  note.title = "Testing"
  note.content = """
# Testing

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

  expected_content = """
# Testing

This has some content with a section in it.



Content after the section

<!-- DIFFERENT SECTION -->
this should not match
<!-- End DIFFERENT SECTION -->



Opening section line should not match
<!-- SECTION -->
"""

  exclude_sections_from_notes([note], ["SECTION"])

  assert note.content == expected_content
