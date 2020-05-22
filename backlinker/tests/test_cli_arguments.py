
import argparse
import pytest

from ..cli import argument_parser, validate_arguments


def test_minimal_arguments():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--output',
          'backlinker/tests/fixtures/notes/']

  parser = argument_parser()
  args = parser.parse_args(argv)

  parameters = validate_arguments(args)

  assert parameters == {
      'exclude': [],
      'input': 'backlinker/tests/fixtures/cats/',
      'output': 'backlinker/tests/fixtures/notes/',
      'render_frontmatter': True,
      'render_index': False,
      'rewrite_as_links': False
  }


def test_normal_arguments():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--output',
          'backlinker/tests/fixtures/notes/', '--no-render-frontmatter', '--render-index', '--rewrite-as-links']

  parser = argument_parser()
  args = parser.parse_args(argv)

  parameters = validate_arguments(args)

  assert parameters == {
      'exclude': [],
      'input': 'backlinker/tests/fixtures/cats/',
      'output': 'backlinker/tests/fixtures/notes/',
      'render_frontmatter': False,
      'render_index': True,
      'rewrite_as_links': True
  }


def test_unknown_arguments():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--in-place', '--this-is-a-bad-argument']

  with pytest.raises(SystemExit) as e:
    parser = argument_parser()
    args = parser.parse_args(argv)


def test_missing_required_arguments():
  argv = ['--input', 'backlinker/tests/fixtures/cats/']

  with pytest.raises(SystemExit) as e:
    parser = argument_parser()
    args = parser.parse_args(argv)


def test_in_place_with_output():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--in-place', '--output', 'backlinker/tests/fixtures/notes/']

  with pytest.raises(SystemExit) as e:
    parser = argument_parser()
    args = parser.parse_args(argv)


def test_in_place():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--in-place']

  parser = argument_parser()
  args = parser.parse_args(argv)

  parameters = validate_arguments(args)

  assert parameters == {
      'exclude': [],
      'input': 'backlinker/tests/fixtures/cats/',
      'output': 'backlinker/tests/fixtures/cats/',
      'render_frontmatter': True,
      'render_index': False,
      'rewrite_as_links': False
  }


def test_in_place_with_index():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--in-place', '--render-index']

  parser = argument_parser()
  args = parser.parse_args(argv)

  parameters = validate_arguments(args)

  assert parameters == {
      'exclude': [],
      'input': 'backlinker/tests/fixtures/cats/',
      'output': 'backlinker/tests/fixtures/cats/',
      'render_frontmatter': True,
      'render_index': True,
      'rewrite_as_links': False
  }


def test_in_place_with_rewrite_as_links():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--in-place', '--rewrite-as-links']

  with pytest.raises(ValueError) as e:
    parser = argument_parser()
    args = parser.parse_args(argv)
    parameters = validate_arguments(args)

  assert '--in-place' in str(e.value) and '--rewrite-as-links' in str(e.value)


def test_in_place_with_no_render_frontmatter():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--in-place', '--no-render-frontmatter']

  with pytest.raises(ValueError) as e:
    parser = argument_parser()
    args = parser.parse_args(argv)
    parameters = validate_arguments(args)

  assert '--in-place' in str(e.value) and '--rewrite-as-links' in str(e.value)


def test_same_input_and_output():
  argv = ['--input', 'backlinker/tests/fixtures/cats/', '--output', 'backlinker/tests/fixtures/cats/']

  with pytest.raises(ValueError) as e:
    parser = argument_parser()
    args = parser.parse_args(argv)
    parameters = validate_arguments(args)

  assert '--in-place' in str(e.value) and '--input' in str(e.value) and '--output' in str(e.value)
