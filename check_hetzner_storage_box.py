#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
check_hetzner_storage_box provides an icinga/nagios check command
to check for free space of your Hetzner Storage Boxes.
"""

import sys
import argparse
import requests

__author__ = 'Martin Seener'
__copyright__ = 'Copyright 2018-2025, viafintech GmbH'
__license__ = 'MIT'
__version__ = '2.0.0'
__maintainer__ = 'Martin Seener'
__email__ = 'martin.seener@viafintech.com'
__status__ = 'Production'

def get_storage_box_info(storage_box_id, token):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Accept': 'application/json'
    }

    try:
        r = requests.get('https://api.hetzner.com/v1/storage_boxes', headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('UNKNOWN - API request failed: {}'.format(e))
        sys.exit(3)

    resp = r.json()
    boxes = resp.get("storage_boxes", [])
    target_box = next((b for b in boxes if str(b.get("id")) == str(storage_box_id)), None)

    if not target_box:
        print('UNKNOWN - Storage Box #{} not found via API.'.format(storage_box_id))
        sys.exit(3)

    name = target_box.get("name", "unknown")

    # max quota from storage_box_type
    box_type = target_box.get("storage_box_type", {})
    max_size_bytes = box_type.get("size")

    # used size from stats (size_data)
    stats = target_box.get("stats", {})
    used_bytes = stats.get("size_data", stats.get("used", None))

    try:
        quota = float(max_size_bytes) / (1024 * 1024)
    except (TypeError, ValueError):
        quota = 0.0

    try:
        usage = float(used_bytes) / (1024 * 1024) if used_bytes is not None else 0.0
    except (TypeError, ValueError):
        usage = 0.0

    if quota <= 0:
        print('UNKNOWN - Storage Box max quota invalid or zero.')
        sys.exit(3)

    free = round(100 - (usage / quota * 100), 1)

    return name, quota, usage, free

def check_storage_box(storage_box_id, token, warning, critical):
    name, quota, usage, free = get_storage_box_info(storage_box_id, token)

    perf_warning = round(quota * (100 - warning) / 100, 1)
    perf_critical = round(quota * (100 - critical) / 100, 1)

    if free <= critical:
        print('CRITICAL - Free disk size of Storage Box #{} ({}) is less than {}% of the quota! '
              '|Usage={}MB;{};{};0;{}'
              .format(storage_box_id, name, critical, usage, perf_warning, perf_critical, quota))
        sys.exit(2)
    elif free <= warning:
        print('WARNING - Free disk size of Storage Box #{} ({}) is less than {}% of the quota! '
              '|Usage={}MB;{};{};0;{}'
              .format(storage_box_id, name, warning, usage, perf_warning, perf_critical, quota))
        sys.exit(1)
    else:
        print('OK - Free disk size of Storage Box #{} ({}) is currently {}% '
              '|Usage={}MB;{};{};0;{}'
              .format(storage_box_id, name, free, usage, perf_warning, perf_critical, quota))
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Nagios/Icinga check for Hetzner Storage Boxes using Console API.')
    parser.add_argument('-s', '--storage-box', dest='storage_box', required=True,
                        help='Enter the Storage Box ID (numeric).')
    parser.add_argument('-t', '--token', dest='token', required=True,
                        help='Hetzner Console API Token.')
    parser.add_argument('-w', '--warning', default=10.0, type=float,
                        help='WARNING threshold in percent (free space). Default 10%%.')
    parser.add_argument('-c', '--critical', default=5.0, type=float,
                        help='CRITICAL threshold in percent (free space). Default 5%%.')
    args = parser.parse_args()
    check_storage_box(args.storage_box, args.token, args.warning, args.critical)

if __name__ == '__main__':
    main()
