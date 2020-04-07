"""
A skeleton python script which reads from an input file,
writes to an output file and parses command line arguments
"""
from __future__ import print_function
import sys
import os
import glob
import re
import urllib.parse


class Link(object):

  def __init__(self, title):
    self.title = title
    self.sources = set()
    self.destination = None

  def as_soft_link(self):
    is_alternate_title = self.title != self.destination.title
    return f"[[{self.title}|{self.destination.title}]]" if is_alternate_title else f"[[{self.title}]]"

  def as_link(self):
    return f"[{self.title}]({urllib.parse.quote(os.path.basename(self.destination.path))})"

  def as_regex(self):
    return re.compile(f'\\[\\[{re.escape(self.title)}(\\|.*?)?\\]\\]')

  def update_aliases_in_notes(self):
    for source in self.sources:
      pattern = self.as_regex()
      (updated_content, _) = pattern.subn(self.as_soft_link(), source.content)
      source.content = updated_content

  def rewrite_in_notes(self):
    for source in self.sources:
      pattern = self.as_regex()
      (updated_content, _) = pattern.subn(self.as_link(), source.content)
      source.content = updated_content


class Note(object):

  def __init__(self, path):
    self.path = path
    self.other_titles = []
    self.content = ""
    self.content_lines = []
    self.frontmatter = ""

  def load(self, from_dir):
    with open(os.path.join(from_dir, self.path), 'r') as f:
      content = f.read()

    start_of_backlinking_block = content.find("<!-- begin backlinker content -->")
    if start_of_backlinking_block != -1:
      content = content[:start_of_backlinking_block]

    content = content.split('---', 2)

    self.content_lines = content[2].strip().split('\n')
    self.frontmatter = content[1].strip()

    self.parse_titles()

  def as_link(self):
    return f"[{self.title}]({urllib.parse.quote(os.path.basename(self.path))})"

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


def backlink(notes_list):

  notes = dict()
  other_titles_mapping = dict()
  links = dict()
  for note in notes_list:
    print(f'Backlinking {note.path}')

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
      links[link].sources.add(note)

  for title, note in notes.items():

    if note.title in links:
      links[note.title].destination = note

    for other_title in note.other_titles:
      if other_title in links:
        links[other_title].destination = note

  for title, link in links.items():
    if link.destination is None:
      note = Note(f"{title}.md")
      note.title = title

      link.destination = note
      notes[title] = note

  return notes, links


def _remove_note_from_links(note, links):
  # remove the note from the sources of its links
  for link_title in note.find_links():
    if link_title in links:
      link = links[link_title]
      link.sources.remove(note)

      if len(link.sources) == 0:
        del links[link_title]


def _exclude_note_and_referencing_notes_by_title(notes, links, title):

  excluded_referencing_note_titles = set()

  # delete any notes with excluded titles
  if title in notes:
    _remove_note_from_links(notes[title], links)
    del notes[title]

  # handle any link to excluded title
  if title in links:

    # remove the link itself
    link_to_excluded_note = links[title]
    del links[title]

    # exclude any referencing notes and record the titles of the referencing note
    for note in link_to_excluded_note.sources:
      if note.title in notes:
        del notes[note.title]

      excluded_referencing_note_titles.add(note.title)
      for other_title in note.other_titles:
        excluded_referencing_note_titles.add(other_title)

      _remove_note_from_links(note, links)

  return excluded_referencing_note_titles


def _redact_links_to_excluded_notes(notes, links, link_titles_to_redact):
  redacted = Note("REDACTED.md")
  redacted.title = "REDACTED"
  redacted.content = "This content has been removed. Maybe it's a secret?"

  did_redact_links = False
  for title in link_titles_to_redact:
    if title in links:
      links[title].destination = redacted
      did_redact_links = True

  if did_redact_links:
    notes['REDACTED'] = redacted


def exclude_notes(notes, links, titles_to_exclude):
  """
  Excludes items from `notes` dict that have a link to any of the given `titles_to_exclude`.
  Does not consider aliases during exclusion, primary title must be passed.
  Links to excluded notes are redirected to a REDACTED note.
  """

  filtered_notes = dict(notes)
  filtered_links = dict(links)

  excluded_referencing_note_titles = set()

  # iterate exclusion titles and remove directly referencing notes and links
  for title in titles_to_exclude:
    excluded_referencing_note_titles.update(_exclude_note_and_referencing_notes_by_title(
        filtered_notes, filtered_links,  title))

  # now replace links to deleted notes with link to REDACTED note
  _redact_links_to_excluded_notes(filtered_notes, filtered_links, excluded_referencing_note_titles)

  return filtered_notes, filtered_links


def load_notes(input_dir):
  input_paths = glob.glob(os.path.join(input_dir, "*.md"))

  notes = list()

  for path in input_paths:
    print(f'Loading {path}')
    note = Note(os.path.basename(path))
    note.load(input_dir)

    notes.append(note)

  return notes


def render_notes(notes, links, rewrite_as_links, render_frontmatter):

  rendered_notes = dict()
  for title, note in notes.items():
    link = links.get(title, None)
    other_title_links = list(
        filter(lambda link: link.title in note.other_titles, list(links.values())))

    rendered = render_note(note, link, other_title_links, rewrite_as_links, render_frontmatter)
    rendered_notes[note.path] = rendered

  return rendered_notes


def output_notes(rendered_notes, output_dir):

  for path, rendered in rendered_notes.items():

    output_path = os.path.join(output_dir, path)

    with open(output_path, 'w') as f:
      f.write(rendered)


def render_note(note, link, other_title_links, rewrite_as_links, render_frontmatter):
  rendered = ""

  if render_frontmatter:
    rendered += f"""---
{note.frontmatter}
---

"""

  rendered += f"""# {note.title}
{render_note_other_titles(note, rewrite_as_links)}
{note.content}
{render_note_backlinks(note, link, other_title_links, rewrite_as_links)}
"""

  return rendered.rstrip() + "\n"


def render_note_other_titles(note, rewrite_as_links):
  if note.other_titles == []:
    return ""

  rendered = "\naka"
  for title in note.other_titles:
    rendered += " "
    rendered += f"[{title}]({urllib.parse.quote(os.path.basename(note.path))})" if rewrite_as_links else f"[[{title}]]"

  return rendered


def render_note_backlinks(note, link, other_title_links, rewrite_as_links):
  rendered = """
<!-- begin backlinker content -->

---
"""

  if link:
    sorted_sources = list(link.sources)
    sorted_sources.sort(key=lambda note: note.title)
    for source in sorted_sources:
      rendered += "\n"
      rendered += ("- " + source.as_link()) if rewrite_as_links else f"[[{source.title}]]"

  other_title_links.sort(key=lambda link: link.title)
  for link in other_title_links:
    rendered += f"\n\nas _{link.title}_\n"
    sorted_sources = list(link.sources)
    sorted_sources.sort(key=lambda note: note.title)
    for source in sorted_sources:
      rendered += "\n"
      rendered += ("- " + source.as_link()) if rewrite_as_links else f"[[{source.title}]]"

  rendered += "\n"

  return rendered


def run_backlinker(input_dir, output_dir, rewrite_as_links=False, render_frontmatter=True, exclude_links_to=[]):

  notes_list = load_notes(input_dir)

  notes, links = backlink(notes_list)

  if len(exclude_links_to) > 0:
    number_of_notes_before_excluding = len(notes)
    number_of_links_before_excluding = len(links)
    notes, links = exclude_notes(notes, links, exclude_links_to)
    print(
        f'Excluded {number_of_notes_before_excluding - len(notes)} notes ({number_of_links_before_excluding - len(links)} links)')

  for link in links.values():
    if rewrite_as_links:
      link.rewrite_in_notes()
    else:
      link.update_aliases_in_notes()

  rendered_notes = render_notes(notes, links, rewrite_as_links, render_frontmatter)

  output_notes(rendered_notes, output_dir)
