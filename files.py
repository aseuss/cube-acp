#!/usr/bin/env python

#
# files.py
#
# Copyright 2015 Andreas Seuss
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
from pprint import pprint

# TODO: recurse through src dir
with open('src/config.json') as data_file:
    data = json.load(data_file)

#pprint(data)
files = data["files"]
for fil in files:
    # TODO: loop over targets
    rate = data["default_astc"]["rate"]
    options = data["default_astc"]["options"]
    if 'options' in fil:
        options = fil["options"]
    if 'rate' in fil:
        rate = fil["rate"]
    for target in data["convert_to"]:
        print "{0},src/{1},{2},{3}".format(target, fil["file"], options, rate)
