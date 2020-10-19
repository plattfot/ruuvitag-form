# Ruuvitag-bar

Simple program that fetches data from a server running
[ruuvitag-hark](https://github.com/plattfot/ruuvitag-hark) and
displays it so a bar program can understand. For example
[waybar](https://github.com/Alexays/Waybar).

Right now it only supports [waybar](https://github.com/Alexays/Waybar).

## Install

Clone this and run `pip install <clone> -U` where `<clone>` is the
path to where you cloned this.

## Usage

Setup a server running
[ruuvitag-hark](https://github.com/plattfot/ruuvitag-hark). Then depending on what bar you use:

### Waybar

Add this to your waybar config

```
"custom/ruuvitag": {
    "format": "{}",
    "exec": "$HOME/.local/bin/ruuvitag-bar <address>:<port>",
    "interval": 60,
    "return-type": "json"
}
```

Where `<address>` is the local address to the machine running
[ruuvitag-hark](https://github.com/plattfot/ruuvitag-hark) and
`<port>` is the port number it is listening to.
