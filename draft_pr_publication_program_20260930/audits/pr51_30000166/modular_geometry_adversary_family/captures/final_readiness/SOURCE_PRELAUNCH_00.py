#!/usr/bin/env python3
"""Readonly preclosure family check; no approval, chmod or manifest creation."""
from pathlib import Path
import json
import family_custody as c

external = c.external_check()
verdict = c.load(c.ROOT/'VERDICT.json')
if verdict['mandatory_corrections'] != [] or verdict['recommended_status'] != 'already_solved':
    raise ValueError('verdict')
for name,expected_count in (('geometry_exact',138800),('geometry_exact_v2',140708)):
    cap = c.ROOT/'captures'/name
    start = c.load(cap/'STARTED.json')
    complete = c.load(cap/'COMPLETE.json')
    launch = c.load(cap/'PRELAUNCH.json')
    if complete['exit_code'] != 0 or type(complete['child_pid']) is not int:
        raise ValueError('actual completion')
    if start['child_pid'] != complete['child_pid'] or start['argv'] != complete['argv']:
        raise ValueError('started completion linkage')
    if launch['argv'] != complete['argv'] or start['cwd'] != complete['cwd']:
        raise ValueError('literal command')
    for label in ('prelaunch','started','stdout','stderr'):
        row = complete[label]
        identity = c.identity(Path(row['path']))
        if identity['bytes'] != row['bytes'] or identity['sha256'] != row['sha256']:
            raise ValueError('complete stream/member binding')
    if c.identity(cap/'STDERR.bin')['bytes'] != 0:
        raise ValueError('stderr')
    result = c.load(cap/'STDOUT.bin')
    if result['status'] != 'PASS' or type(result['assertions']) is not int or result['assertions'] != expected_count:
        raise ValueError('literal diagnostic result')
    for source in launch['sources']:
        saved = c.identity(Path(source['saved']['path']))
        if saved['bytes'] != source['saved']['bytes'] or saved['sha256'] != source['saved']['sha256']:
            raise ValueError('saved source digest')
        if source['saved']['sha256'] != source['original']['sha256']:
            raise ValueError('prelaunch source identity')
        if name == 'geometry_exact_v2' and c.identity(Path(source['original']['path']))['sha256'] != saved['sha256']:
            raise ValueError('final unchanged source')
    if c.identity(cap/'OPERATOR_PRELAUNCH.py')['sha256'] != c.identity(c.ROOT/'capture_private.py')['sha256']:
        raise ValueError('capture operator unchanged')
print(json.dumps({'status':'PASS_PREPARATION_ONLY','external_science_files':15,
                  'external_science_bytes':53495,'actual_diagnostic_children':[38813,39624],
                  'final_assertions':140708,'future_ROOT_closure_or_acceptance_authority':False},sort_keys=True,indent=2))
