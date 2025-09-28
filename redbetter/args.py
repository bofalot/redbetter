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

  script = parser.add_argument_group(title="Script Mode")
  script.add_argument(
    "--script",
    action='store_true',
    help="run in one-time script mode. By default, find all possible torrents to transcode"
  )

  script.add_argument(
    '-s',
    '--single',
    action='store_true',
    help='only add one format per release (useful for getting unique groups)'
  )

  script.add_argument(
    '-U',
    '--upload',
    action='store_true',
    help="upload new torrents (dry-run mode is by default if not specified)"
  )

  script.add_argument(
    "--release-urls",
    nargs='*',
    help="list of specific torrents to transcode"
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
