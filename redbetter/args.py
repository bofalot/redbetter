import argparse
import sys
from multiprocessing import cpu_count

def parse_args(args=None):
  args = sys.argv[1:] if args is None else args

  name = sys.argv[0]
  description = "Redbetter: Transcoding utility for RED and OPS"
  parser = argparse.ArgumentParser(
    prog=name,
    description=description,
    add_help=False,
  )

  parser.add_argument(
    "-h",
    "--help",
    action="help",
    default=argparse.SUPPRESS,
    help="show this help message and exit",
  )

  options = parser.add_argument_group(title="options")
  options.add_argument(
    '-t',
    '--threads',
    type=int,
    help='number of threads to use when transcoding',
    default=max(cpu_count() - 1, 1)
  )

  options.add_argument(
    '-c',
    '--config',
    help='the location of the configuration file',
    default='./config.ini'
  )

  options.add_argument(
    '-k',
    '--cache',
    help='the location of the cache',
    default='./redbetter_cache'
  )

  parsed = parser.parse_args(args)
  return parsed
