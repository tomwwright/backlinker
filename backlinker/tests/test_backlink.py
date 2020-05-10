from ..backlinker import backlink

from . import fixtures
from .fixtures.notes import example_notes, example_note_one, example_note_two, example_note_three
from .fixtures.cats import fixture_cats


def _test_backlink(fixture):
  notes_list = list(fixture["notes"].values())

  notes, links = backlink(notes_list)

  assert notes == fixture["notes"]
  assert links.keys() == fixture["links"].keys()
  for key in links:
    link = links[key]
    fixture_link = fixture["links"][key]

    assert link.title == fixture_link.title
    assert link.sources == fixture_link.sources
    assert link.destination == fixture_link.destination


def test_backlink_notes(example_notes):
  _test_backlink(example_notes)


def test_backlink_cats(fixture_cats):
  _test_backlink(fixture_cats)
