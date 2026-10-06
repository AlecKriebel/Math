#!/usr/bin/env python3
"""Integrity and diagnostic checks only. Does not verify contact-topology theorems."""
import argparse
import hashlib
import json
import pathlib
import sys

NAMES = {'REPORT.md', 'APPROACHES.md', 'STATUS.json', 'VERIFICATION_METADATA.json', 'verify_bundle.py', 'VALIDATION_RESULTS.json'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def strict_json(path):
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)

def check(root, manifest):
    m = strict_json(manifest)
    require(type(m) is dict, 'manifest must be an object')
    require(m.get('schema') == 1 and m.get('problem_id') == 2839, 'wrong manifest identity')
    members = m.get('members')
    require(type(members) is list and len(members) == len(NAMES), 'wrong member count')
    names = [item.get('path') for item in members if type(item) is dict]
    require(len(names) == len(members) and set(names) == NAMES and len(set(names)) == len(names), 'invalid member set')
    require({p.name for p in root.iterdir()} == NAMES, 'unexpected or missing package file')
    for item in members:
        require(set(item) == {'path', 'bytes', 'sha256'}, 'unknown member fields')
        path = root / item['path']
        require(not path.is_symlink() and path.is_file(), 'nonregular member')
        blob = path.read_bytes()
        require(type(item['bytes']) is int and len(blob) == item['bytes'], 'byte-count mismatch: '+item['path'])
        require(hashlib.sha256(blob).hexdigest() == item['sha256'], 'hash mismatch: '+item['path'])
    s = strict_json(root/'STATUS.json')
    require(s.get('schema') == 1 and s.get('problem_id') == 2839, 'wrong status identity')
    require(s.get('status') == 'stalled_partial', 'incorrect classification')
    require(type(s.get('approaches_used')) is int and s['approaches_used'] == 5 and s.get('approach_limit') == 5, 'approach count mismatch')
    for key in ('general_problem_solved','general_problem_refuted','novelty_claim','publication_performed'):
        require(s.get(key) is False, 'unsupported outcome claim: '+key)
    require(s.get('inherited_gate') == 'pass_literature_triage_only', 'wrong gate')
    v = strict_json(root/'VERIFICATION_METADATA.json')
    require(v.get('problem_id') == 2839 and v.get('schema') == 1, 'wrong metadata identity')
    expected = [(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')]
    datasets = v['exact_input_verification']['datasets']
    require([(d['byte_count'],d['sha256']) for d in datasets] == expected, 'dataset identity mismatch')
    require(v['exact_input_verification']['statement_sha256']=='749b71051566bb470bb377e46477858e1f6506f8468ecea0fa5ba9fc46ea3e1f','statement identity mismatch')
    require(v['exact_input_verification']['complete_record_report_pair_sha256']=='4a4a4a2b98291ca38bfa7104b2da6bd6c979a4362baea22ebc1cb4bfbb3c156d','record identity mismatch')
    # These are arithmetic regression examples. Universal proofs are in REPORT.md.
    examples = 0
    for t in range(-5,6):
        for rho in range(-5,6):
            for a in range(6):
                for b in range(6):
                    require((t-a-b)-(rho+a-b)==t-rho-2*a,'stabilization identity failed')
                    examples += 1
    for s0 in range(1,21):
        for t in range(s0+1,s0+21):
            k=t-s0-1
            require(k>=0 and t-k-1==s0 and t-k>=2,'barrier endpoint failed')
    for m0 in range(1,101):
        bad=2*m0-1; threshold=2*m0
        require(bad<threshold and bad>=threshold-1,'threshold arithmetic failed')
    return {'ok':True,'scope':'integrity and finite arithmetic diagnostics only; no theorem certification','optimization':sys.flags.optimize,'stabilization_examples':examples}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=pathlib.Path,required=True)
    parser.add_argument('--manifest',type=pathlib.Path,required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(check(args.root,args.manifest),sort_keys=True))
    except Exception as error:
        print(json.dumps({'ok':False,'error':str(error)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
