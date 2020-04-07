from ..backlinker import exclude_notes

from . import fixtures
from .fixtures import example_notes, example_note_one, example_note_two, example_note_three


def test_exclude_nonexistent_title(example_notes):
  notes, links = exclude_notes(
      example_notes['notes'], example_notes['links'], {"This does not exist"})

  assert len(notes.values()) == len(example_notes['notes'].values())
  assert "REDACTED" not in notes


def test_exclude_unlinked_title(example_notes):
  notes, links = exclude_notes(
      example_notes['notes'], example_notes['links'], {"Note 3"})

  assert len(notes.values()) == len(example_notes['notes'].values()) - 1
  assert "Note 1" in notes
  assert "Note 2" in notes
  assert "Note 3" not in notes
  assert "REDACTED" not in notes


def test_exclude_linked_title(example_notes):

  notes, links = exclude_notes(example_notes['notes'], example_notes['links'], {"Note 2"})

  links_to_redacted = list(
      filter(lambda link: link.destination.title == "REDACTED", links.values()))

  assert len(notes.values()) == len(example_notes['notes'].values()) - 1
  assert "Note 1" not in notes  # deleted for referencing Note 2
  assert "Note 2" not in notes  # deleted for excluded title
  assert "Note 3" in notes  # redacted for referencing Note 1
  assert "REDACTED" in notes
  assert len(links_to_redacted) == 1


def test_exclude_existing_tag(example_notes):

  notes, links = exclude_notes(example_notes['notes'], example_notes['links'], {"Secret"})

  assert len(notes.values()) == len(example_notes['notes'].values()) - 2
  assert "Note 1" in notes
  assert "Note 2" in notes
  assert "Note 3" not in notes
  assert "Secret" not in notes
  assert "REDACTED" not in notes


def test_exclude_existing_tag_for_referenced_note(example_notes):

  notes, links = exclude_notes(example_notes['notes'], example_notes['links'], {"Other Tag"})

  links_to_redacted = list(
      filter(lambda link: link.destination.title == "REDACTED", links.values()))

  assert len(notes.values()) == len(example_notes['notes'].values()) - 1

  assert len(links_to_redacted) == 1  # just Note 1
  assert links_to_redacted[0].sources == {notes['Note 1']}
  assert "Note 1" in notes  # exists, with link to Note 2 redacted

  assert "Note 2" not in notes  # deleted for referencing Other Tag
  assert "Note 3" in notes
  assert "Other Tag" not in notes  # deleted as an excluded title
  assert "REDACTED" in notes
