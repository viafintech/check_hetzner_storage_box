# check_hetzner_storage_box Icinga/Nagios check command

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This check can be used with Icinga and Nagios and will check the free space of your Hetzner Storage Box and alerts you if it is below certain thresholds.

## Requirements

`check_hetzner_storage_box` requires Python 2.7 or Python 3.x to run and has been successfully tested with Python 2.7/3.4 on Debian and Python 3.7 on macOS.

This check command depends on the following python modules:
 * requests
 * argparse

**Installation on Debian / Ubuntu**
```
# Python 2.x
apt install python-requests

# Python 3.x
apt install python3-requests
```

**Installation on Redhat 6 / CentOS 6 (not tested!)**
```
yum install python-argparse python34-requests
```

**Installation on Redhat 7 / CentOS 7 (not tested!)**
```
yum install python-requests
```

**Installation using the requirements file with pip**
```
pip install -r requirements.txt
```

## Usage

```
usage: check_hetzner_storage_boxes.py [-h] -s STORAGE_BOX -t TOKEN
                                      [-w WARNING] [-c CRITICAL]

Nagios/Icinga check for Hetzner Storage Boxes using Console API.

optional arguments:
  -h, --help            show this help message and exit
  -s STORAGE_BOX, --storage-box STORAGE_BOX
                        Enter the Storage Box ID (numeric).
  -t TOKEN, --token TOKEN
                        Hetzner Console API Token.
  -w WARNING, --warning WARNING
                        WARNING threshold in percent (free space). Default
                        10%.
  -c CRITICAL, --critical CRITICAL
                        CRITICAL threshold in percent (free space). Default
                        5%.
```

With a WARNING treshold of 10.0% and CRITICAL treshold of 5.0% (default).
```
./check_hetzner_storage_box.py -s <STORAGE_BOX_ID> -t '<API_TOKEN>'
OK - Free disk size of Storage Box #123456 (Backup-Box-1) is currently 59.6%
```

With own WARNING and CRITICAL tresholds.

```
./check_hetzner_storage_box.py -s <STORAGE_BOX_ID> -t '<API_TOKEN>' -w 25 -c 15
CRITICAL - Free disk size of Storage Box #123457 (Backup-Box-2) is less than 15.0% of the quota!
```

#### Performance Data

The check also prints out performance data that can be used to generate some nice graphs in Icinga2 or any other tool. Here is what it looks like (exmaple):

```
OK -  The ... |Usage=3882418.0MB;4718592.0;4980736.0;0;5242880.0
```

## Contribution and License

Feel free to contribute. It's licensed under the [MIT LICENSE](LICENSE).
