"""
Backlinker
"""

import argparse
import os
import sys
from .backlinker import run_backlinker


def dir_path_arg_type(path):
  if os.path.isdir(path):
    return path
  else:
    raise argparse.ArgumentTypeError(f"readable_dir: {path} is not a valid path")


def argument_parser():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--input', type=dir_path_arg_type, required=True)

  output_group = parser.add_mutually_exclusive_group(required=True)
  output_group.add_argument('--output', type=dir_path_arg_type)
  output_group.add_argument('--in-place', action='store_true')

  rewrite_group = parser.add_mutually_exclusive_group()
  rewrite_group.add_argument('--rewrite-as-links', dest='rewrite_as_links', action='store_true')
  rewrite_group.add_argument('--no-rewrite-as-links', dest='rewrite_as_links', action='store_false')

  parser.add_argument('--exclude', type=str, nargs='+',
                      help='the list of note tags or titles to exclude from the render')

  frontmatter_group = parser.add_mutually_exclusive_group()
  frontmatter_group.add_argument('--render-frontmatter', dest='render_frontmatter', action='store_true')
  frontmatter_group.add_argument('--no-render-frontmatter', dest='render_frontmatter', action='store_false')

  index_group = parser.add_mutually_exclusive_group()
  index_group.add_argument('--render-index', dest='render_index', action='store_true')
  index_group.add_argument('--no-render-index', dest='render_index', action='store_false')

  parser.set_defaults(in_place=False, rewrite_as_links=False, render_frontmatter=True,
                      exclude=[], render_index=False)

  return parser


def validate_arguments(args):
  if args.in_place and args.output:
    raise ValueError('Cannot specify both --in-place and --output')

  if args.output == args.input:
    raise ValueError('Cannot specify same directory for --input and --output, use --in-place instead')

  if args.in_place and (not args.render_frontmatter or args.rewrite_as_links):
    raise ValueError('Cannot specify --no-render-frontmatter or --rewrite-as-links when --in-place set (too destructive)')

  if args.in_place and (not args.render_frontmatter or args.rewrite_as_links):
    raise ValueError('Cannot specify --no-render-frontmatter or --rewrite-as-links when --in-place set (too destructive)')

  return {
      'exclude': args.exclude,
      'input': args.input,
      'output': args.output if not args.in_place else args.input,
      'render_index': args.render_index,
      'render_frontmatter': args.render_frontmatter,
      'rewrite_as_links': args.rewrite_as_links
  }


def cli():
  parser = argument_parser()

  args = parser.parse_args()
  parameters = validate_arguments(args)

  run_backlinker(parameters)
