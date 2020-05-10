import pytest
import os.path

from ...backlinker import Note, Link


def note_cats():
  with open(os.path.join(os.path.dirname(__file__), 'cats/Cats.md'), 'r') as f:
    file_contents = f.read().rstrip() + '\n'

  note = Note("test/path/Cats.md")
  note.title = "Cats"
  note.frontmatter = '''created: "2020-03-18T12:31:33.886Z"
modified: "2020-03-24T00:06:13.163Z"
tags: []
title: Cats'''
  note.other_titles = {
      "Cat",
      "Felis catus",
  }
  note.content = """tags [[Animals]]

Cats, also called domestic cats (Felis catus), are small, carnivorous (meat-eating) mammals, of the family Felidae. Domestic cats are often called house cats when kept as indoor pets.

A cat is sometimes called a kitty. A young cat is called a [[Kitten]]. A female cat that has not had its sex organs removed is called a queen. A male cat that has not had its sex organs removed is called a tom.

## Likes and Dislikes

The table below describes some of the common likes and dislikes of cats.

| Thing       | Like | Dislike |
| ----------- | :--: | :-----: |
| [[Kittens]] |  x   |         |
| Food        | xxx  |         |
| [[Dogs]]    |      |    x    |
| Attention   |  x   |         |
| Belly Rub   |  x   |    x    |
| Water       |      |    x    |

<!-- Drafts -->

## Cats with Jobs

Some cats have jobs, often catching [[Mice]]. A cat that does this on a ship is called a [[Ship's Cat]].

<!-- End Drafts -->"""

  link = Link(note.title)
  link.destination = note

  links = {
      "Animals",
      "Kitten",
      "Kittens",
      "Dogs",
      "Mice",
      "Ship's Cat"
  }

  return {
      "file_contents": file_contents,
      "note": note,
      "link": link,
      "links": links
  }


def note_drafts():
  with open(os.path.join(os.path.dirname(__file__), 'cats/Drafts.md'), 'r') as f:
    file_contents = f.read().rstrip() + '\n'

  note = Note("test/path/Drafts.md")
  note.title = "Drafts"
  note.frontmatter = """created: "2020-03-18T12:31:33.886Z"
modified: "2020-03-24T00:06:13.163Z"
tags: []
title: Drafts"""
  note.other_titles = {}
  note.content = """tags [[Categories]]

This page contains links to all the in-progress of draft pages."""

  link = Link(note.title)
  link.destination = note

  links = {
      "Categories"
  }

  return {
      "file_contents": file_contents,
      "note": note,
      "link": link,
      "links": links
  }


def note_kittens():
  with open(os.path.join(os.path.dirname(__file__), 'cats/Kittens.md'), 'r') as f:
    file_contents = f.read().rstrip() + '\n'

  note = Note("test/path/Kittens.md")
  note.title = "Kittens"
  note.frontmatter = """created: "2020-03-18T12:31:33.886Z"
modified: "2020-03-24T00:06:13.163Z"
tags: []
title: Kittens"""
  note.other_titles = {"Kitten"}
  note.content = """tags [[Animals]]

A kitten is a baby [[Cat]].

Kittens play endlessly. It is how they do their learning. They will play their favourite games, such as 'hide and pounce', with almost anyone or anything. Soft balls on strings are a standard toy; so is a scratching post."""

  link = Link(note.title)
  link.destination = note

  links = {
      "Animals",
      "Cat"
  }

  return {
      "file_contents": file_contents,
      "note": note,
      "link": link,
      "links": links
  }


def note_ships_cat():
  with open(os.path.join(os.path.dirname(__file__), 'cats/Ship\'s Cat.md'), 'r') as f:
    file_contents = f.read().rstrip() + '\n'

  note = Note("test/path/Ship\'s Cat.md")
  note.title = "Ship\'s Cat"
  note.frontmatter = """created: "2020-03-18T12:31:33.886Z"
modified: "2020-03-24T00:06:13.163Z"
tags: []
title: Ship\'s Cat"""
  note.other_titles = {}
  note.content = """tags [[Drafts]]

TODO: Write about cats on ships here."""

  link = Link(note.title)
  link.destination = note

  links = {
      "Drafts"
  }

  return {
      "file_contents": file_contents,
      "note": note,
      "link": link,
      "links": links
  }


def blank_note(title):
  note = Note(f"test/path/{title}.md")
  note.title = title

  link = Link(note.title)
  link.destination = note

  links = {}

  return {
      "file_contents": "",
      "note": note,
      "link": link,
      "links": links
  }


@pytest.fixture
def fixture_cats():
  '''Returns notes examples about Cats'''

  animals = blank_note("Animals")
  cats = note_cats()
  categories = blank_note("Categories")
  dogs = blank_note("Dogs")
  drafts = note_drafts()
  kittens = note_kittens()
  mice = blank_note("Mice")
  ships_cat = note_ships_cat()

  animals['link'].sources = {
      cats['note'],
      kittens['note']
  }

  dogs['link'].sources = {
      cats['note']
  }

  drafts['link'].sources = {
      ships_cat['note']
  }

  kittens['link'].sources = {
      cats['note']
  }

  mice['link'].sources = {
      cats['note']
  }

  ships_cat['link'].sources = {
      cats['note']
  }

  # alias links

  cat_link = Link("Cat")
  cat_link.destination = cats["note"]
  cat_link.sources = {
      kittens['note']
  }

  kitten_link = Link("Kitten")
  kitten_link.destination = kittens["note"]
  kitten_link.sources = {
      cats['note']
  }

  return {
      "Cats": cats,
      "Categories": categories,
      "Dogs": dogs,
      "Drafts": drafts,
      "Kittens": kittens,
      "Mice": mice,
      "Ship\'s Cat": ships_cat,
      "notes": {
          "Cats": cats["note"],
          "Categories": categories["note"],
          "Dogs": dogs["note"],
          "Drafts": drafts["note"],
          "Kittens": kittens["note"],
          "Mice": mice["note"],
          "Ship\'s Cat": ships_cat["note"],
      },
      "links": {
          "Animals": animals["link"],
          "Cat": cat_link,
          "Dogs": dogs["link"],
          "Drafts": drafts["link"],
          "Kitten": ships_cat["link"],
          "Kittens": kitten_link,
          "Mice": mice["link"],
          "Ship's Cat": ships_cat["link"]
      }
  }
