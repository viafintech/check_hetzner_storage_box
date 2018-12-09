# check_hetzner_storage_box Icinga/Nagios check command

This check can be used with Icinga and Nagios and will check the free space of your Hetzner Storage Box and alerts you if it is below certain thresholds.

## Requirements

`check_hetzner_storage_box` requires Python 3.x to run and has been successfully tested with Python 3.4 on Debian and Python 3.7 on macOS.

This check command depends on the following python modules:
 * requests
 * argparse

**Installation on Debian / Ubuntu**
```
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
usage: check_hetzner_storage_box.py [-h] [-s STORAGE_BOX] [-u USER]
                                    [-p PASSWORD] [-w WARNING] [-c CRITICAL]

check_hetzner_storage_box is an Icinga/Nagios-compatible check that checks for
the free space of a storage box in your Hetzner Robot account and alerts upon
reasonable thresholds.

optional arguments:
  -h, --help            show this help message and exit
  -s STORAGE_BOX, --storage-box STORAGE_BOX
                        Enter the Storage Box ID. You can see this in your
                        Robot WebUI Storage Box overview (for ex. BX40 #<ID>).
  -u USER, --user USER  Enter the Hetzner Robot Webservice username.
  -p PASSWORD, --password PASSWORD
                        Enter the Hetzner Robot Webservice password.
  -w WARNING, --warning WARNING
                        Enter the WARNING threshold in percent (free).
  -c CRITICAL, --critical CRITICAL
                        Enter the CRITICAL threshold in percent (free).
```

With a WARNING treshold of 10.0% and CRITICAL treshold of 5.0% (default).
```
./check_hetzner_storage_box.py -s <STORAGE_BOX_ID> -u '<HETZNER_WS_USER>' -p '<HETZNER_WS_PASSWORD>'
OK - Free disk size of Storage Box #123456 (Backup-Box-1) is currently 59.6%
```

With own WARNING and CRITICAL tresholds.

```
./check_hetzner_storage_box.py -s <STORAGE_BOX_ID> -u '<HETZNER_WS_USER>' -p '<HETZNER_WS_PASSWORD>' -w 25 -c 15
CRITICAL - Free disk size of Storage Box #123457 (Backup-Box-2) is less than 15.0% of the quota!
```

## Contribution and License

Feel free to contribute. It's licensed under the [MIT LICENSE](LICENSE).
