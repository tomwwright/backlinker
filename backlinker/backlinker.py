"""
A skeleton python script which reads from an input file,
writes to an output file and parses command line arguments
"""
from __future__ import print_function
import sys
import os
import glob
import yaml
import re


class Link(object):

  def __init__(self, title):
    self.title = title
    self.sources = []
    self.destination = None


class Note(object):

  def __init__(self, path):
    self.path = path
    self.other_titles = []
    self.content = ""
    self.content_lines = []
    self.frontmatter = ""

  def load(self):
    with open(self.path, 'r') as f:
      content = f.read()

    start_of_backlinking_block = content.find("<!-- begin backlinker content -->")
    if start_of_backlinking_block != -1:
      content = content[:start_of_backlinking_block]

    content = content.split('---', 2)

    self.content_lines = content[2].strip().split('\n')
    self.frontmatter = content[1].strip()

    self.parse_titles()

  def parse_titles(self):
    self.title = self.content_lines[0].replace('#', '').strip()
    self.content_lines = self.content_lines[1:]

    self.other_titles = []
    if len(self.content_lines) > 1 and self.content_lines[1].startswith('aka'):
      self.other_titles = parse_links(self.content_lines[1])
      self.content_lines = self.content_lines[2:]
    elif len(self.content_lines) > 2 and self.content_lines[2].startswith('aka'):
      self.other_titles = parse_links(self.content_lines[2])
      self.content_lines = self.content_lines[3:]

    self.content = "\n".join(self.content_lines).strip()

  def find_links(self):
    return parse_links(self.content)


def parse_links(text):
  links = re.findall(r'\[\[(.*?)(?:\|(.*?))?\]\]', text)
  return set(map(lambda link: link[0], links))


def backlink(input_dir):
  input_paths = glob.glob(os.path.join(input_dir, "*.md"))

  notes = dict()
  other_titles_mapping = dict()
  links = dict()
  for path in input_paths:
    print(f'Backlinking {path}')
    note = Note(path)
    note.load()
    if note.title in notes:
      raise ValueError(f'note title \'{note.title}\' occurs more than once')
    notes[note.title] = note

    for other_title in note.other_titles:
      if other_title in other_titles_mapping:
        raise ValueError(f'note other title \'{note.title}\' occurs more than once')
      other_titles_mapping[other_title] = note.title

    for link in note.find_links():
      if link not in links:
        links[link] = Link(link)
      links[link].sources.append(note)

  for title, note in notes.items():

    if note.title in links:
      links[note.title].destination = note

    for other_title in note.other_titles:
      if other_title in links:
        links[other_title].destination = note

  for title, link in links.items():
    if link.destination is None:
      note = Note(os.path.join(input_dir, f"{title}.md"))
      note.title = title

      link.destination = note
      notes[title] = note

  return notes, links


def output_notes(notes, links, output_dir):
  for title, note in notes.items():
    link = links.get(title, None)
    other_title_links = list(
        filter(lambda link: link.title in note.other_titles, list(links.values())))

    rendered = render_note(note, link, other_title_links)

    output_path = os.path.join(output_dir, os.path.basename(note.path))
    with open(output_path, 'w') as f:
      f.write(rendered)


def render_note(note, link, other_title_links):
  rendered = f"""---
{note.frontmatter}
---

# {note.title}
{render_note_other_titles(note)}
{note.content}
{render_note_backlinks(note, link, other_title_links)}
"""

  return rendered


def render_note_other_titles(note):
  if note.other_titles == []:
    return ""

  rendered = "\naka"
  for title in note.other_titles:
    rendered += f" [[{title}]]"

  return rendered


def render_note_backlinks(note, link, other_title_links):
  rendered = """
<!-- begin backlinker content -->

---
"""

  if link:
    link.sources.sort(key=lambda note: note.title)
    for source in link.sources:
      rendered += f"\n[[{source.title}]]"

  other_title_links.sort(key=lambda link: link.title)
  for link in other_title_links:
    rendered += f"\n\nas _{link.title}_\n"
    link.sources.sort(key=lambda note: note.title)
    for source in link.sources:
      rendered += f"\n[[{source.title}]]"

  rendered += "\n"

  return rendered


def update_link_in_content(link):
  is_alternate_title = link.title != link.destination.title
  for source in link.sources:
    pattern = re.compile(f'\[\[{re.escape(link.title)}(\|.*?)?\]\]')
    new_link_text = f"[[{link.title}|{link.destination.title}]]" if is_alternate_title else f"[[{link.title}]]"
    (updated_content, substitutions_count) = pattern.subn(new_link_text, source.content)
    source.content = updated_content


def run_backlinker(input_dir, output_dir):
  notes, links = backlink(input_dir)

  for link in links.values():
    update_link_in_content(link)

  output_notes(notes, links, output_dir)
