#!/usr/bin/env python3
"""Optional fresh corpus-identity replay. Emits metadata only, never record text."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

PINS = {
    'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566', 15458,
                'fbc13b152f7e156a8e995042bbb81bec776e17a013abb0a28b03afd5123061a7'),
    'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf', 15458,
                 '742b73aef0b9855f679b4e2c7979d8548a414e63d3ec8af40a1e069f84f6f724'),
    'research_results': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b', 6701,
                         '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a')
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalog',type=Path,required=True)
    p.add_argument('--problems',type=Path,required=True)
    p.add_argument('--research-results',type=Path,required=True)
    p.add_argument('--output',type=Path)
    a = p.parse_args()
    receipts = []
    for kind in PINS:
        data = getattr(a,kind).read_bytes()
        size, digest, count, row_digest = PINS[kind]
        actual = hashlib.sha256(data).hexdigest()
        require(len(data) == size and actual == digest, kind+': full bytes mismatch')
        obj = json.loads(data)
        require(len(obj) == count, kind+': count mismatch')
        if kind != 'research_results':
            require(type(obj) is list,kind+': expected array')
            rows = [r for r in obj if isinstance(r,dict) and str(r.get('id')) == '30001066']
            require(len(rows) == 1,kind+': target is missing or duplicated')
            target = rows[0]
            require(target.get('problem_number') == 'OWR-2090-019',kind+': wrong problem binding')
            if kind == 'catalog':require(target.get('rank') == 819,'wrong catalog rank')
            present = True
        else:
            require(type(obj) is dict,'reports: expected map')
            require('OWR-2090-019' not in obj and '30001066' not in obj,'target report unexpectedly present')
            # Also check structured identifiers, where present, rather than
            # relying on the map key alone.
            for report in obj.values():
                if not isinstance(report,dict):continue
                candidates=[report]
                if isinstance(report.get('problem'),dict):candidates.append(report['problem'])
                for item in candidates:
                    require(str(item.get('id')) != '30001066' and str(item.get('problem_id')) != '30001066'
                            and item.get('problem_number') != 'OWR-2090-019',
                            'target report found under another key')
            target={};present=False
        actual_row = hashlib.sha256(json.dumps(target,sort_keys=True).encode()).hexdigest()
        require(actual_row == row_digest,kind+': full record hash mismatch')
        receipts.append({'dataset':kind+'.json','bytes':len(data),'sha256':actual,'entry_count':len(obj),
                         'target_record_present':present,'complete_target_record_sha256':actual_row,
                         'complete_record_match':True,'fresh_replay':'PASS'})
    result={'schema':'isolated-transversal-independent-corpus-replay-v1','status':'PASS',
            'checked_at':datetime.now(timezone.utc).isoformat(),'problem_id':30001066,
            'problem_number':'OWR-2090-019','rank':819,
            'hash_rule':'sha256(json.dumps(record, sort_keys=True).encode()) with Python defaults; absent report = {}',
            'datasets':receipts,'scope':'Entire restored file bytes and complete target records checked. No source content included.'}
    if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError) as exc:raise SystemExit('FAIL: '+str(exc))
