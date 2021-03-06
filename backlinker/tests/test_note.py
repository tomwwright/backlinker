from unittest.mock import patch, mock_open
import pytest
import os.path

from ..backlinker import Note
from .fixtures.notes import example_note_one, example_note_two, example_note_three
from .fixtures.cats import fixture_cats


def test_note_one_load(example_note_one):

  with patch("builtins.open", new_callable=mock_open, read_data=example_note_one['file_contents']):
    note = Note("note_one.md")
    note.load("test/path/")

  assert note.title == example_note_one['expected'].title
  assert note.frontmatter == example_note_one['expected'].frontmatter
  assert note.content == example_note_one['expected'].content
  assert note.other_titles == example_note_one['expected'].other_titles
  assert note.find_links() == {
      "Tag",
      "Note 2",
      "Note -- complicated 'title'"
  }


def test_note_two_load(example_note_two):

  with patch("builtins.open", new_callable=mock_open, read_data=example_note_two['file_contents']):
    note = Note("note_two.md")
    note.load("test/path/")

  assert note.title == example_note_two['expected'].title
  assert note.frontmatter == example_note_two['expected'].frontmatter
  assert note.content == example_note_two['expected'].content
  assert note.other_titles == example_note_two['expected'].other_titles
  assert note.find_links() == {
      "Tag",
      "Other Tag",
      "Note 1 Alias"
  }


def test_note_three_load(example_note_three):

  with patch("builtins.open", new_callable=mock_open, read_data=example_note_three['file_contents']):
    note = Note("note_three.md")
    note.load("test/path/")

  assert note.title == example_note_three['expected'].title
  assert note.frontmatter == example_note_three['expected'].frontmatter
  assert note.content == example_note_three['expected'].content
  assert note.other_titles == example_note_three['expected'].other_titles
  assert note.find_links() == {
      "Tag",
      "Notes",
      "Secret",
      "Note 1"
  }


def _load_test(title, fixture):

  with patch("builtins.open", new_callable=mock_open, read_data=fixture['file_contents']):
    note = Note(f"{title}.md")
    note.load("test/path/")

  assert note.title == fixture['note'].title
  assert note.frontmatter == fixture['note'].frontmatter
  assert note.content == fixture['note'].content
  assert note.other_titles == fixture['note'].other_titles
  assert note.find_links() == fixture['links']


def test_note_cats(fixture_cats):
  _load_test("Cats", fixture_cats["Cats"])


def test_note_drafts(fixture_cats):
  _load_test("Drafts", fixture_cats["Drafts"])


def test_note_kittens(fixture_cats):
  _load_test("Kittens", fixture_cats["Kittens"])


def test_note_ships_cat(fixture_cats):
  _load_test("Ship\'s Cat", fixture_cats["Ship\'s Cat"])
