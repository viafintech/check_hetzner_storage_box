#!/usr/bin/env python
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
__copyright__ = 'Copyright 2018-2021, viafintech GmbH'
__license__ = 'MIT'
__version__ = '1.1.4'
__maintainer__ = 'Martin Seener'
__email__ = 'martin.seener@viafintech.com'
__status__ = 'Production'


def validate_robot_ws(user, password):
    try:
        r = requests.get('https://robot-ws.your-server.de/storagebox',
                         auth=(user, password))
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('UNKNOWN - The following error occured: {}'.format(err))
        sys.exit(3)

    return True


def get_storage_box_info(storage_box, user, password):
    try:
        r = requests.get('https://robot-ws.your-server.de/storagebox/' +
                         storage_box,
                         auth=(user, password))
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print('UNKNOWN - Can\'t find storage box (#{})'
              .format(storage_box))

    name = r.json()['storagebox']['name']
    quota = float(r.json()['storagebox']['disk_quota'])
    usage = float(r.json()['storagebox']['disk_usage'])
    free = round(100 - (usage / quota) * 100, 1)

    return name, quota, usage, free


def check_storage_box(storage_box, user, password, warning, critical):
    name, quota, usage, free = get_storage_box_info(storage_box,
                                                    user,
                                                    password)

    # PerfData
    perf_warning = round(quota * (100 - warning) / 100, 1)
    perf_critical = round(quota * (100 - critical) / 100, 1)

    if free <= critical:
        print('CRITICAL - Free disk size of Storage Box #{} ({}) '
              'is less than {}% of the quota!'
              '|Usage={}KB;{};{};0;{}'
              .format(storage_box,
                      name,
                      critical,
                      usage,
                      perf_warning,
                      perf_critical,
                      quota)
              )
        sys.exit(2)
    elif free <= warning:
        print('WARNING - Free disk size of Storage Box #{} ({}) '
              'is less than {}% of the quota!'
              '|Usage={}KB;{};{};0;{}'
              .format(storage_box,
                      name,
                      warning,
                      usage,
                      perf_warning,
                      perf_critical,
                      quota)
              )
        sys.exit(1)
    elif warning < free:
        print('OK - Free disk size of Storage Box #{} ({}) '
              'is currently {}%'
              '|Usage={}KB;{};{};0;{}'
              .format(storage_box,
                      name,
                      free,
                      usage,
                      perf_warning,
                      perf_critical,
                      quota)
              )
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
    if args.storage_box and validate_robot_ws(args.user,
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
