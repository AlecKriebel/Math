#!/usr/bin/env python3
"""Read-only freeze authentication, with exact lexical component spelling."""
import datetime, hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
EXPECTED = '76db189f9a41ad8946b77d75657311dcce12f5e70bd0ec8cb1f2858c9c4d68c8'
def sha(data): return hashlib.sha256(data).hexdigest()
def exact_path(p):
    p = p.absolute()
    current = pathlib.Path(p.anchor)
    for part in p.parts[1:]:
        if part not in {x.name for x in current.iterdir()}:
            return False
        current /= part
    return True
def authenticate(label):
    freeze = HERE / 'INPUT_FREEZE.json'
    data = freeze.read_bytes()
    if sha(data) != EXPECTED: raise ValueError('Freeze hash mismatch')
    obj = json.loads(data)
    records = []
    errors = []
    for group in ('files','external_readonly_inputs'):
        for rec in obj[group]:
            p = pathlib.Path(rec['path'])
            if not p.is_absolute(): p = AUDIT / p
            lexical = exact_path(p)
            raw = p.read_bytes()
            actual = dict(path=rec['path'],bytes=len(raw),sha256=sha(raw),exact_lexical_path=lexical)
            records.append(actual)
            if not lexical or len(raw)!=rec['bytes'] or sha(raw)!=rec['sha256']:
                errors.append(actual)
    result = dict(schema='pr1262-round4-input-authentication-v1',phase=label,
        at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        input_freeze_sha256=EXPECTED,files=len(obj['files']),external_readonly_inputs=len(obj['external_readonly_inputs']),
        all_exact=True if not errors else False,errors=errors,authenticated=records)
    (HERE / ('INPUT_AUTHENTICATION_'+label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    if errors: raise ValueError(errors)
    print(json.dumps({k:v for k,v in result.items() if k!='authenticated'}))
if __name__ == '__main__': authenticate(sys.argv[1])
