import pytest
import os.path

from ...backlinker import Note, Link


@pytest.fixture
def example_note_one():
  '''Returns contents of 'fixtures/note_one.md' '''
  with open(os.path.join(os.path.dirname(__file__), 'note_one.md'), 'r') as f:
    file_contents = f.read()

  expected = Note("test/path/note_one.md")
  expected.title = "Note 1"
  expected.frontmatter = """created: "2020-03-18T12:31:33.886Z"
modified: "2020-03-24T00:06:13.163Z"
tags:
  - Notebooks/My Notes
title: Note 1"""
  expected.other_titles = {
      "Note 1 Alias"
  }
  expected.content = """tags [[Tag]]

This is some content.

It has two paragraphs, this one contains a link to [[Note 2]].

### Subheading

Some stuff after the subheading, containing another link, this time to [[Note -- complicated 'title']].

---

Adding some content after the horizontal rule to see how that goes.

> Quote content
> This should also be quoted"""

  return {
      "file_contents": file_contents,
      "expected": expected
  }


@pytest.fixture
def example_note_two():
  '''Returns contents of 'fixtures/note_two.md' and the expected Note'''
  with open(os.path.join(os.path.dirname(__file__), 'note_two.md'), 'r') as f:
    file_contents = f.read().rstrip() + '\n'

  expected = Note("test/path/note_two.md")
  expected.title = "Note 2"
  expected.frontmatter = '''tags: [Notebooks/My Notes]
title: Note 2
created: "2020-03-18T12:31:33.886Z"
modified: "2020-03-24T00:06:13.163Z"'''
  expected.other_titles = {
      "Note 2 Alias"
  }
  expected.content = """tags [[Tag]] [[Other Tag]]

This is some content.

It has two paragraphs, this one contains a link back to [[Note 1 Alias]].

### Subheading

Some stuff after the subheading.

---

Adding some content after the horizontal rule to see how that goes.

> Quote content
> This should also be quoted"""

  return {
      "file_contents": file_contents,
      "expected": expected
  }


@pytest.fixture
def example_note_three():
  '''Returns contents of 'fixtures/note_three.md' and the expected Note'''
  with open(os.path.join(os.path.dirname(__file__), 'note_three.md'), 'r') as f:
    file_contents = f.read().rstrip() + '\n'

  expected = Note("test/path/note_three.md")
  expected.title = "Note 3"
  expected.frontmatter = '''tags: [Notebooks/My Notes]
title: Note 3
created: "2020-03-18T12:35:33.886Z"
modified: "2020-03-27T00:06:13.163Z"'''
  expected.other_titles = {
      "Note 3 Alias"
  }
  expected.content = """tags [[Tag]] [[Notes]]

This is some content.

It has two paragraphs, this one contains a link back to [[Note 1]].

### Subheading

Some stuff after the subheading.

---

Adding some content after the horizontal rule to see how that goes.

> Quote content
> This should also be quoted

#### Another subheading

This is getting quite nested."""

  return {
      "file_contents": file_contents,
      "expected": expected
  }


@pytest.fixture
def example_notes(example_note_one, example_note_two, example_note_three):
  '''Returns three example note fixtures with links resolved'''

  # prepare links for one

  one_link = Link(example_note_one['expected'].title)
  one_link.destination = example_note_one['expected']
  one_link.sources = [example_note_three['expected']]

  one_alias_link = Link("Note 1 Alias")
  one_alias_link.destination = example_note_one['expected']
  one_alias_link.sources = [example_note_two['expected']]

  example_note_one['link'] = one_link
  example_note_one['other_title_links'] = [one_alias_link]

  # prepare link for two
  two_link = Link(example_note_two['expected'].title)
  two_link.destination = example_note_two['expected']
  two_link.sources = [example_note_one['expected']]

  example_note_two['link'] = two_link
  example_note_two['other_title_links'] = []

  return {
      "one": example_note_one,
      "two": example_note_two,
      "three": example_note_three
  }


__all__ = [
    "example_note_one",
    "example_note_two",
    "example_note_three",
    "example_notes"


]
