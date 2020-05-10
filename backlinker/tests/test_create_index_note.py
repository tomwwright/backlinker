from ..backlinker import Note, create_index_note

import pytest

from . import fixtures
from .fixtures.notes import example_notes, example_notes_index, example_note_one, example_note_two, example_note_three
from .fixtures.cats import fixture_cats, fixture_cats_index


def test_exception_raised_when_index_exists(example_notes):

  index = Note("bogus/index.md")
  index.title = "Index"

  notes_with_index = dict(example_notes['notes'])
  notes_with_index["Index"] = index

  with pytest.raises(Exception):
    create_index_note(notes_with_index)


def test_create_notes_index(example_notes, example_notes_index):

  assert "Index" not in example_notes["notes"]

  index_links = create_index_note(example_notes["notes"])

  index = example_notes["notes"]["Index"]
  assert index.content == example_notes_index['note'].content

  assert len(list(filter(lambda link: link.sources != {index}, index_links))) == 0


def test_create_cats_index(fixture_cats, fixture_cats_index):

  assert "Index" not in fixture_cats["notes"]

  index_links = create_index_note(fixture_cats["notes"])

  index = fixture_cats["notes"]["Index"]
  assert index.content == fixture_cats_index["note"].content

  assert len(list(filter(lambda link: link.sources != {index}, index_links))) == 0
