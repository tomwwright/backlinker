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
    raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def parse_arguments():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--input', type=dir_path_arg_type)
  parser.add_argument('--output', type=dir_path_arg_type)

  return parser.parse_args()


def cli():
  args = parse_arguments()

  run_backlinker(args.input, args.output)
