from ..backlinker import render_note

from . import fixtures
from .fixtures import example_notes, example_note_one, example_note_two, example_note_three


def test_render_note_one(example_notes):

  note = example_notes['one']['expected']
  link = example_notes['links'][note.title]
  other_title_links = list(
      filter(lambda link: link.title in note.other_titles, example_notes['links'].values()))

  print(other_title_links)

  rendered = render_note(note, link, other_title_links, False, True)

  assert example_notes['one']['file_contents'] == rendered


def test_render_note_two(example_notes):

  note = example_notes['two']['expected']
  link = example_notes['links'][note.title]
  other_title_links = list(
      filter(lambda link: link.title in note.other_titles, example_notes['links'].values()))

  rendered = render_note(note, link, other_title_links, False, True)

  assert example_notes['two']['file_contents'] == rendered


def test_render_note_three(example_notes):

  note = example_notes['three']['expected']

  rendered = render_note(note, None, [], False, True)

  # backlinker content section in note_three.md is incorrect, assert on render before that

  original = example_notes['three']['file_contents']
  assert original != rendered
  assert original[:original.find('<!-- begin backlinker content -->')
                  ] == rendered[:rendered.find('<!-- begin backlinker content -->')]
