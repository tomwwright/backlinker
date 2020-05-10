"""
Backlinker
"""

import argparse
import os
from .backlinker import run_backlinker


def dir_path_arg_type(path):
  if os.path.isdir(path):
    return path
  else:
    raise argparse.ArgumentTypeError(f"readable_dir: {path} is not a valid path")


def parse_arguments():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--input', type=dir_path_arg_type)
  parser.add_argument('--output', type=dir_path_arg_type)

  parser.add_argument('--rewrite-as-links', dest='rewrite_as_links', action='store_true')
  parser.add_argument('--no-rewrite-as-links', dest='rewrite_as_links', action='store_false')

  parser.add_argument('--exclude', type=str, nargs='+',
                      help='the list of note tags or titles to exclude from the render')

  parser.add_argument('--render-frontmatter', dest='render_frontmatter', action='store_true')
  parser.add_argument('--no-render-frontmatter', dest='render_frontmatter', action='store_false')

  parser.add_argument('--render-index', dest='render_index', action='store_true')
  parser.add_argument('--no-render-index', dest='render_index', action='store_false')

  parser.set_defaults(rewrite_as_links=False, render_frontmatter=True,
                      exclude=[], render_index=False)

  return parser.parse_args()


def cli():
  args = parse_arguments()

  run_backlinker(args.input, args.output, args.rewrite_as_links,
                 args.render_frontmatter, args.exclude, args.render_index)
