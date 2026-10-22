#!/usr/bin/env python3
"""Authenticate only the two literal freeze lists, including path spelling."""
import datetime, hashlib, json, pathlib, sys
F=pathlib.Path(__file__).resolve().parent
A=F.parents[1]
EXPECTED='7520928e1b97250902a17474992bb84a298c5db257a0527f463158bc9ec69960'
def exact_case(p):
    if not p.is_absolute():
        raise ValueError('expected absolute path')
    q=pathlib.Path(p.anchor)
    for part in p.parts[1:]:
        if part not in {x.name for x in q.iterdir()}:
            return False
        q=q/part
    return True
def main():
    f=F/'INPUT_FREEZE.json'; data=f.read_bytes(); freeze=json.loads(data)
    errors=[]; counts={}
    if hashlib.sha256(data).hexdigest()!=EXPECTED:
        errors.append('freeze SHA mismatch')
    for key in ('files','external_readonly_inputs'):
        rows=freeze[key]; seen=set()
        for r in rows:
            rel=r['path']; p=pathlib.Path(rel); p=p if p.is_absolute() else A/p
            if rel in seen: errors.append('duplicate '+rel)
            seen.add(rel)
            try:
                b=p.read_bytes()
                if not exact_case(p): errors.append('case '+rel)
                if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']: errors.append('content '+rel)
            except Exception as e: errors.append(rel+': '+str(e))
        counts[key]=len(rows)
    out={'schema':'math-pr1280-package-round2-input-authentication-v1','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_freeze_sha256':EXPECTED,'counts':counts,'status':'PASS' if not errors else 'FAIL','errors':errors,'membership_policy':'Only literal files and external_readonly_inputs records were authenticated; no receipt paths traversed as membership.'}
    target=F/(sys.argv[1] if len(sys.argv)>1 else 'INPUT_AUTH_START.json')
    target.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
    return bool(errors)
if __name__=='__main__': sys.exit(main())
