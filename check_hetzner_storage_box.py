#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

"""
check_hetzner_storage_box provides an icinga/nagios check command
to check for free space of your Hetzner Storage Boxes.
"""

from __future__ import print_function
import sys
import argparse
import requests


__author__ = 'Martin Seener'
__copyright__ = 'Copyright 2018, Martin Seener'
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Martin Seener'
__email__ = 'martin@sysorchestra.com'
__status__ = 'Production'


def validate_storage_box(storage_box, user, password):
    r = requests.get('https://robot-ws.your-server.de/storagebox/'
                     + storage_box,
                     auth=(user, password))
    if r.status_code == 401:
        print('UNKNOWN - Webservice is not enabled or user/password is wrong')
        sys.exit(3)
    elif r.status_code == 403:
        print('UNKNOWN - Rate limit exeeded. Please don\'t check too often!.')
        sys.exit(3)
    elif r.status_code == 404:
        print('UNKNOWN - Can\'t find the storage box with ID ' + storage_box)
        sys.exit(3)
    elif r.status_code == 200:
        return True
    else:
        print('UNKOWN - An unknown error occured!')
        sys.exit(3)


def check_storage_box(storage_box, user, password, warning, critical):
    r = requests.get('https://robot-ws.your-server.de/storagebox/'
                     + storage_box,
                     auth=(user, password))

    disk_name = r.json()['storagebox']['name']
    disk_quota = r.json()['storagebox']['disk_quota']
    disk_usage = r.json()['storagebox']['disk_usage']
    disk_free_percent = round(100 - (disk_usage / disk_quota) * 100, 1)

    if disk_free_percent <= critical:
        print('CRITICAL - Free disk size of Storage Box #{} ({}) is less than {}% of the quota!'.format(
            storage_box,
            disk_name,
            critical
        ))
        sys.exit(2)
    elif disk_free_percent <= warning:
        print('WARNING - Free disk size of Storage Box #{} ({}) is less than {}% of the quota!'.format(
            storage_box,
            disk_name,
            warning
        ))
        sys.exit(1)
    elif warning < disk_free_percent:
        print('OK - Free disk size of Storage Box #{} ({}) is currently {}%'.format(
            storage_box,
            disk_name,
            disk_free_percent
        ))
        sys.exit()
    else:
        print('UNKNOWN - Unknown error occured!')
        sys.exit(3)


def main(args):
    parser = argparse.ArgumentParser(
        description='\
        check_hetzner_storage_box is an Icinga/Nagios-compatible\
        check that checks for the free space of a storage\
        box in your Hetzner Robot account and alerts\
        upon reasonable thresholds.',
    )

    parser.add_argument(
        '-s',
        '--storage-box',
        dest='storage_box',
        type=str,
        help='Enter the Storage Box ID. You can see this in your Robot WebUI\
        Storage Box overview (for ex. BX40 #<ID>).',
    )
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        help='Enter the Hetzner Robot Webservice username.',
    )
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        help='Enter the Hetzner Robot Webservice password.',
    )
    parser.add_argument(
        '-w',
        '--warning',
        default=10.0,
        type=float,
        help='Enter the WARNING threshold in percent (free).',
    )
    parser.add_argument(
        '-c',
        '--critical',
        default=5.0,
        type=float,
        help='Enter the CRITICAL threshold in percent (free).',
    )

    args = parser.parse_args()
    if args.storage_box and validate_storage_box(args.storage_box,
                                                 args.user,
                                                 args.password):
        check_storage_box(args.storage_box,
                          args.user,
                          args.password,
                          args.warning,
                          args.critical)
    else:
        parser.print_help()


if __name__ == '__main__':
    main(sys.argv[1:])
