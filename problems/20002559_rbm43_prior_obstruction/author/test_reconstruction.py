#!/usr/bin/env python3
"""Adversarial semantic controls; all explicit gates also run under python -O."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location('reconstruction', Path(__file__).with_name('verify_reconstruction.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

def rejected(name, function):
    try:
        function()
    except (ValueError, KeyError, IndexError):
        return name
    raise RuntimeError('Mutation was accepted: '+name)

def main():
    certificate, appendix = map(Path, sys.argv[1:3])
    data = json.loads(certificate.read_bytes())
    text = appendix.read_text()
    rows = v.from_printed_appendix(text)
    checks = []
    altered = copy.deepcopy(data)
    altered['support'][0] = 3
    checks.append(rejected('different support', lambda: v.compare_json(altered, rows)))
    altered = copy.deepcopy(data)
    altered['cuts'][0]['left'][0][1] += 1
    checks.append(rejected('wrong multiplicity', lambda: v.compare_json(altered, rows)))
    altered = copy.deepcopy(data)
    altered['cuts'][0]['left'][0][1] = -1
    checks.append(rejected('negative multiplicity', lambda: v.compare_json(altered, rows)))
    altered = copy.deepcopy(data)
    altered['cuts'].pop()
    checks.append(rejected('missing JSON identity', lambda: v.compare_json(altered, rows)))
    altered_text = text.replace('| 1 | 25,65 |', '| 1 | 26,65 |')
    checks.append(rejected('wrong printable identity', lambda: v.from_printed_appendix(altered_text)))
    checks.append(rejected('identity without forbidden state', lambda: v.validate_identity([0,8],[0,8])))
    checks.append(rejected('empty identity collection', lambda: v.reconstruct([])))
    checks.append(rejected('insufficient valid cover', lambda: v.reconstruct(rows[:1])))
    print(json.dumps({'status':'PASS_ADVERSARIAL_CONTROLS','rejected_cases':checks,'python_optimized':sys.flags.optimize},indent=2))

if __name__ == '__main__':
    main()
