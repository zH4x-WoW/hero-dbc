# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Aethys256
"""

import sys
import os
import csv

generatedDir = os.path.join('DBC', 'generated')
parsedDir = os.path.join('DBC', 'parsed')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), 'AethysDBC'))

## Mapping
# id_spell & id_misc from Spell
# id_misc & proj_speed from SpellMisc

# Get every misc id associated to every spell id
Spells = {}
with open(os.path.join(generatedDir, 'Spell.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        Spells[row['id_misc']] = row['id']
        
Durations = {}
with open(os.path.join(generatedDir, 'SpellDuration.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    for row in reader:
        if int(row['duration_1']) > 0:
            Durations[row['id']] = {}
            Durations[row['id']][1] = row['duration_1']
            Durations[row['id']][2] = row['duration_2']

with open(os.path.join(generatedDir, 'SpellMisc.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    ValidRows = []
    for row in reader:
        if int(row['id_duration']) > 0 and row['id'] in Spells and row['id_duration'] in Durations:
            ValidRows.append(row)
    with open(os.path.join(parsedDir, 'SpellDuration.lua'), 'w', encoding='utf-8') as file:
        file.write('AethysCore.Enum.SpellDuration = {\n')
        iMax = len(ValidRows)-1
        for i, row in enumerate(ValidRows):
            baseDuration = int(Durations[row['id_duration']][1])
            pandemic = int(float(Durations[row['id_duration']][1])*0.3)
            maxDuration = baseDuration + pandemic
            if i == iMax:
                file.write('  [' + Spells[row['id']] + '] = {' + Durations[row['id_duration']][1] + ', ' + str(int(maxDuration)) + '}\n')
            else:
                file.write('  [' + Spells[row['id']] + '] = {' + Durations[row['id_duration']][1] + ', ' + str(int(maxDuration)) + '},\n')
        file.write('}\n')

