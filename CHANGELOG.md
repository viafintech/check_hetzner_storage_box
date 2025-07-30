# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [2.0.0] - 2025-07-30
- change API for new Hetzner Console API because Robots API is deprecated
  - this changes from user/password to API Token for authentication

## [1.1.5] - 2024-10-15
- fix performance data disk size unit from KB to MB

## [1.1.4] - 2021-09-23
- fix performance data output name to "Usage" to remove whitespaces and make it work again for check_mk

## [1.1.3] - 2020-12-29
- rename company name after rebranding

## [1.1.2] - 2018-12-20
- made another perfData adjustment so Icinga shows the green/grey usage cake icon

## [1.1.1] - 2018-12-20
- fixed performance data and made it compatible to Icinga2 (see https://www.monitoring-plugins.org/doc/guidelines.html#AEN201)

## [1.1.0] - 2018-12-14
- added some README improvements
- made some code refactoring
- improved error handling for requests module
- all changes from 1.1.0-pre1 (#2)

## [1.1.0-pre1] - 2018-12-14
- added perfData to command output (quota, used, warn, crit)

## [1.0.1] - 2018-12-14
- made some fixes in the formatting/long lines using pycodestyle/pyflakes
- added compatibility for python 2.7

## [1.0.0] - 2018-12-09
- Initial release
