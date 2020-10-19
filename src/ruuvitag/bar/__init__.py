# Copyright (C) 2020  Fredrik Salomonsson

# This file is part of ruuvitag-bar.

# Ruuvitag-bar is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Ruuvitag-bar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ruuvitag-bar. If not, see
# <https://www.gnu.org/licenses/>.

"""Display information from a ruuvitag-hark server
"""

import getopt
import os
import sys
import pycurl
import json
from io import BytesIO

class ArgparseFaux:
    """Get the same interface as argparse's error."""
    def __init__(self, prog=os.path.basename(sys.argv[0])):
        self.prog=prog

    def error(self, message, errno=2):
        print(f"{self.prog}: {message}\nTry `{self.prog} --help' for more information.",
              file=sys.stderr)
        sys.exit(errno)

class Arguments:
    def __init__(self):
        self.format = None
        self.mac = None

def parse_arguments(argv):
    parser = ArgparseFaux(prog=os.path.basename(argv[0]))
    helpstring=f"""usage: {parser.prog} [OPTIONS]... ADDRESS
Display information from a ruuvitag-hark server

Options:
  -F, --format FORMAT  Specify what FORMAT to use for the output. See FORMAT
      --show MAC       Show ruuvitag with MAC address
  -h, --help           Print this message then exits

FORMAT:
  Supported formats waybar.
"""
    args = Arguments()
    try:
        opts, address = getopt.gnu_getopt(
            argv[1:],
            "hF:",
            ["help",
             "format=",
             "show=",
             ])
        if address:
            # Pick the last one
            args.address = address[-1]
        else:
            parser.error("Need to specify an url to a ruuvitag-hark server.")

    except getopt.GetoptError as err:
        parser.error(err)

    for option, argument in opts:
        if option in ("-h", "--help"):
            print(helpstring)
            sys.exit(0)
        elif option == '--show':
            args.mac = argument.upper()
        elif option in ("-F", "--format"):
            args.format = argument.lower()

    return parser, args

class Acceleration:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Tag:
    def __init__(self,
                 mac='--:--:--:--:--:--',
                 name='Unknown',
                 humidity='-',
                 temperature='-',
                 pressure='-',
                 acceleration=Acceleration(),
                 battery='?',
                 time='?'):
        self.mac = mac
        self.name = name
        self.humidity = humidity
        self.temperature = temperature
        self.pressure = pressure
        self.acceleration = acceleration
        self.battery = battery
        self.time = time
    def __repr__(self):
        return f"{self.temperature}C {self.humidity}% {self.pressure}hPa"

def fetch_tags(address):

    tags = {}
    try:
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, f'{address}/data')
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        tags_json = json.loads(body.decode('UTF-8'))
        for mac,data in tags_json.items():
            tags[mac] = Tag(
                mac=data['mac'],
                name=data['name'],
                humidity=data['humidity'],
                temperature=data['temperature'],
                pressure=data['pressure'],
                acceleration=Acceleration(
                    data['acceleration_x'],
                    data['acceleration_y'],
                    data['acceleration_z'],
                ),
                battery=data['battery'],
                time=data['time']   )
    except pycurl.error as err:
        print(err, file=sys.stderr)

    return tags

def run(argv):
    parser, args = parse_arguments(argv)

    tags = fetch_tags(args.address)

    if tags and not args.mac:
        args.mac = next(iter(tags))

    try:
        if args.format == 'waybar' or args.format == None:
            if tags:
                json.dump({'text': str(tags[args.mac]),
                           'tooltip': '\n'.join([f'{tag.name}: {tag}' for mac,tag in tags.items()]),
                           'class': 'ruuvitag',
                           'percentage': tags[args.mac].humidity},
                          sys.stdout)
            else:
                json.dump({'text': str(Tag()), 'class': 'ruuvitag', 'percentage': 0}, sys.stdout)

        else:
            parser.error(f'{args.format} is currently not supported')
    except KeyError:
        parser.error(f'Tag "{args.mac}" does not exist')

def main():
    run(sys.argv)
