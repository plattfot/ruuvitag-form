# Ruuvitag-form

Simple program that fetches data from a server running
[ruuvitag-hark](https://github.com/plattfot/ruuvitag-hark) and output
that to stdout in a format that other programs then can then consume.

Right now it supports:

- [waybar](https://github.com/Alexays/Waybar): Will show temperature,
  humidity and air pressure.
- [influxdb](https://www.influxdata.com/products/influxdb-overview/):
  Output the data in the
  [line-protocol](https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/),
  which then can be imported to influxdb.

## Install

### From source

Clone this repository to you machine. In the following subsections
`CLONE` will reference the path you cloned this to.

After you have cloned it, follow the instructions in the subsection
matching the tool you want to use to install this.

#### Guix

Install it with [guix](https://guix.gnu.org).

```
guix install -f CLONE/build-aux/guix.scm
```

#### Pip

Install it with [pip](https://pip.pypa.io/en/stable/)

```
pip install CLONE -U
```

## Usage

Setup a server running
[ruuvitag-hark](https://github.com/plattfot/ruuvitag-hark). Then
depending on what program you use.

### Waybar

Add this to your waybar config

```
"custom/ruuvitag": {
    "format": "{}",
    "exec": "$HOME/.local/bin/ruuvitag-form ADDRESS:PORT",
    "interval": 60,
    "return-type": "json"
}
```

Where `ADDRESS` is the local address to the machine running
[ruuvitag-hark](https://github.com/plattfot/ruuvitag-hark) and
`PORT` is the port number it is listening to.

### InfluxDB

If you're using the
[CLI](https://docs.influxdata.com/influxdb/v2.0/reference/cli/influx/write/)
and using a [bash](https://www.gnu.org/software/bash/) compatible
shell you can import data by running:

```bash
influx write -b BUCKET -f <(ruuvitag-form ADDRESS:PORT --format=influxdb)
```

Where `ADDRESS` is the local address to the machine running
[ruuvitag-hark](https://github.com/plattfot/ruuvitag-hark) and `PORT`
is the port number it is listening to. `BUCKET` is the bucket it
should import the data to.

Reason for using `<(…)` instead of `$(…)` to fetch the data is to
avoid escaping special characters if there are any in the data. As
`<(…)` will present itself as a file from which `influx` can read
from.
