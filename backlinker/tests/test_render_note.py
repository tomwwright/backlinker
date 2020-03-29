from ..backlinker import render_note

from . import fixtures
from .fixtures import example_notes, example_note_one, example_note_two, example_note_three


def test_render_note_one(example_notes):

  rendered = render_note(example_notes['one']['expected'], example_notes['one']
                         ['link'], example_notes['one']['other_title_links'], False, True)

  assert example_notes['one']['file_contents'] == rendered


def test_render_note_two(example_notes):

  rendered = render_note(example_notes['two']['expected'], example_notes['two']
                         ['link'], example_notes['two']['other_title_links'], False, True)

  assert example_notes['two']['file_contents'] == rendered


def test_render_note_three(example_notes):

  rendered = render_note(example_notes['three']['expected'], None, [], False, True)

  # backlinker content section in note_three.md is incorrect, assert on render before that

  original = example_notes['three']['file_contents']
  assert original != rendered
  assert original[:original.find('<!-- begin backlinker content -->')
                  ] == rendered[:rendered.find('<!-- begin backlinker content -->')]
