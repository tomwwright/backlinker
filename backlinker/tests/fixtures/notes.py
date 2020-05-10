import pytest
import os.path

from ...backlinker import Note, Link


@pytest.fixture
def example_note_one():
  '''Returns contents of 'fixtures/note_one.md' '''
  with open(os.path.join(os.path.dirname(__file__), 'notes/note_one.md'), 'r') as f:
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
  with open(os.path.join(os.path.dirname(__file__), 'notes/note_two.md'), 'r') as f:
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
  with open(os.path.join(os.path.dirname(__file__), 'notes/note_three.md'), 'r') as f:
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
  expected.content = """tags [[Tag]] [[Notes]] [[Secret]]

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
def example_notes_index():
  note = Note("Index.md")
  note.title = "Index"

  note.content = """## N

- [[Note -- complicated 'title']]
- [[Note 1]]
- [[Note 1 Alias]] _Note 1_
- [[Note 2]]
- [[Note 2 Alias]] _Note 2_
- [[Note 3]]
- [[Note 3 Alias]] _Note 3_
- [[Notes]]

## O

- [[Other Tag]]

## S

- [[Secret]]

## T

- [[Tag]]

"""

  link = Link(note.title)
  link.destination = note

  links = {}  # index is generated after backlinking and so generates no Links

  return {
      "file_contents": "",
      "note": note,
      "link": link,
      "links": links
  }


@pytest.fixture
def example_notes(example_note_one, example_note_two, example_note_three):
  '''Returns three example note fixtures with links resolved'''

  # prepare links for one

  one_link = Link(example_note_one['expected'].title)
  one_link.destination = example_note_one['expected']
  one_link.sources = {example_note_three['expected']}

  one_alias_link = Link("Note 1 Alias")
  one_alias_link.destination = example_note_one['expected']
  one_alias_link.sources = {example_note_two['expected']}

  # prepare link for two
  two_link = Link(example_note_two['expected'].title)
  two_link.destination = example_note_two['expected']
  two_link.sources = {example_note_one['expected']}

  tag_note = Note("Tag.md")
  tag_note.title = "Tag"
  tag_link = Link("Tag")
  tag_link.destination = tag_note
  tag_link.sources = {example_note_one['expected'],
                      example_note_two['expected'], example_note_three['expected']}

  notes_note = Note("Notes.md")
  notes_note.title = "Notes"
  notes_link = Link("Notes")
  notes_link.destination = notes_note
  notes_link.sources = {example_note_three['expected']}

  other_tag_note = Note("Other Tag.md")
  other_tag_note.title = "Other Tag"
  other_tag_link = Link("Other Tag")
  other_tag_link.destination = other_tag_note
  other_tag_link.sources = {example_note_two['expected']}

  secret_note = Note("Secret.md")
  secret_note.title = "Secret"
  secret_link = Link("Secret")
  secret_link.destination = secret_note
  secret_link.sources = {example_note_three['expected']}

  complicated_name_note = Note("Note -- complicated 'title'")
  complicated_name_note.title = "Note -- complicated 'title'"
  complicated_name_link = Link("Note -- complicated 'title'")
  complicated_name_link.destination = complicated_name_note
  complicated_name_link.sources = {example_note_one['expected']}

  return {
      "one": example_note_one,
      "two": example_note_two,
      "three": example_note_three,
      "notes": {
          "Note 1": example_note_one['expected'],
          "Note 2": example_note_two['expected'],
          "Note 3": example_note_three['expected'],
          "Note -- complicated 'title'": complicated_name_note,
          "Notes": notes_note,
          "Other Tag": other_tag_note,
          "Secret": secret_note,
          "Tag": tag_note
      },
      "links": {
          "Note 1": one_link,
          "Note 1 Alias": one_alias_link,
          "Note 2": two_link,
          "Note -- complicated 'title'": complicated_name_link,
          "Notes": notes_link,
          "Other Tag": other_tag_link,
          "Secret": secret_link,
          "Tag": tag_link
      }
  }
