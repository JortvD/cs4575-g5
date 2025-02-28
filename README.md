# Investigating how using uBlock Origin affects energy consumption

This is an experiment repository for testing energy efficiency of browsers with and without ad blocker extensions. 

It makes use of [EnergiBridge](https://github.com/tdurieux/EnergiBridge) to measure the energy consumption of Chromium with and without Ublock Origin enabled.

## Usage

This experiment can be run both on Windows and on Linux.

### Windows

1. Run `python main.py -e $ENERGIBRIDGEPATH -n 30` where `-e $ENERGIBRIDGEPATH` is the relative path to the energibridge executable, and `-n` is the number of times each set is repeated. The outputs by default are stored in the `output` directory.  

### Linux

Running on Linux requires a bit of extra setup.

1. Running `main.py` for the first time will install Chromium in the `data` directory. Navigate to `data/chrome-linux` and manually add a file with the name `master_preferences`, with the following content:
```json
{
   "extensions": {
      "ui": {
         "developer_mode": true
      }
   }
}
```
This automatically enables developer mode on startup, which is required in order to activate UBlock Origin on Chromium. 

2. Make sure to give the necessary permissions to EnergiBridge:
```bash
sudo chgrp -R msr /dev/cpu/*/msr;
sudo chmod g+r /dev/cpu/*/msr;
sudo setcap cap_sys_rawio=ep target/release/energibridge;
```
It also might be necessary to add the current user to the `msr` group.

3. Run `python main.py -e $ENERGIBRIDGEPATH -n 30` where `-e $ENERGIBRIDGEPATH` is the relative path to the energibridge executable, and `-n` is the number of times each set is repeated. The outputs by default are stored in the `output` directory.  