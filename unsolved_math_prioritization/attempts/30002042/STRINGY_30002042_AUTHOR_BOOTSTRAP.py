#!/usr/bin/env python3
"""Trusted external bootstrap: run only with Python -I -S, optionally -O."""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    raise SystemExit('REFUSED: invoke python -I -S -B [ -O ] BOOTSTRAP.py ZIP MANIFEST')
# No filesystem-dependent imports occur before the isolation check.
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import subprocess
import tempfile
import zipfile

MANIFEST_SHA256='7ed84eb3615eba0c2a413e3a7653e7a826312171aff1f61666c67d614b06503f'
ZIP_SHA256='3e77fa2a11514444ea34bbee9ebd9096cbf313749d22dd4c7afc21060ef4218b'
NAMES={'README.md','RESULT.md','APPROACHES.md','STATUS.json','INPUT_BINDING.json','SOURCES.json','checks.py','EXPECTED.json'}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate JSON key')
        out[k]=v
    return out


def parse(b):
    return json.loads(b,object_pairs_hook=unique)


def regular_read(p):
    need(stat.S_ISREG(p.lstat().st_mode),'input is not a regular non-symlink file')
    need(p.stat().st_size<4_000_000,'input exceeds fixed size ceiling')
    return p.read_bytes()


def verify(zpath, mpath):
    zb,mb=regular_read(zpath),regular_read(mpath)
    need(sha(zb)==ZIP_SHA256,'ZIP trust-anchor mismatch')
    need(sha(mb)==MANIFEST_SHA256,'manifest trust-anchor mismatch')
    m=parse(mb)
    need(type(m) is dict and set(m)=={'schema','problem_id','files'},'manifest schema')
    need(type(m['schema']) is int and m['schema']==1,'manifest version')
    need(type(m['problem_id']) is int and m['problem_id']==30002042,'problem identifier')
    need(type(m['files']) is dict and set(m['files'])==NAMES,'manifest inventory')
    payload={}
    with zipfile.ZipFile(io.BytesIO(zb)) as z:
        entries=z.infolist()
        need(len(entries)==len(NAMES) and {x.filename for x in entries}==NAMES,'ZIP strict inventory')
        for item in entries:
            need(item.create_system==3 and stat.S_ISREG(item.external_attr>>16),'nonregular ZIP member')
            need(not item.is_dir() and not item.flag_bits&1,'directory or encrypted ZIP member')
            entry=m['files'][item.filename]
            need(type(entry) is dict and set(entry)=={'bytes','sha256'},'member record schema')
            need(type(entry['bytes']) is int and 0<=entry['bytes']<1_000_000,'member byte size')
            need(type(entry['sha256']) is str and re.fullmatch('[0-9a-f]{64}',entry['sha256']) is not None,'member hash format')
            need(item.file_size==entry['bytes'],'ZIP member declared size')
            data=z.read(item)
            need(len(data)==entry['bytes'] and sha(data)==entry['sha256'],'ZIP member content mismatch')
            payload[item.filename]=data
    # Execution consumes verified bytes, never an extracted or possibly replaced file.
    code=payload['checks.py'].decode('utf-8')
    expected=parse(payload['EXPECTED.json'])
    with tempfile.TemporaryDirectory(prefix='stringy-isolated-') as tmp:
        command=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+['-c',code]
        run=subprocess.run(command,cwd=tmp,check=False,capture_output=True,text=True,timeout=30)
        need(run.returncode==0 and run.stderr=='','mathematical check process failed')
        need(parse(run.stdout)==expected,'exact result mismatch')
    need(regular_read(zpath)==zb and regular_read(mpath)==mb,'input changed during verification')
    return {'verified':True,'schema':1,'problem_id':30002042,'members':len(NAMES),
            'archive_sha256':ZIP_SHA256,'manifest_sha256':MANIFEST_SHA256,
            'isolated_pre_execution_bootstrap':True,'optimized':bool(sys.flags.optimize),
            'checks_passed':expected['checks_passed'],
            'false_shortcut_controls':len(expected['false_shortcut_controls']),
            'scope':'sealed authored packet and exact arithmetic only; general finiteness unresolved'}


if __name__=='__main__':
    try:
        need(len(sys.argv)==3,'usage: BOOTSTRAP.py ZIP MANIFEST')
        print(json.dumps(verify(Path(sys.argv[1]),Path(sys.argv[2])),sort_keys=True,indent=2))
    except (OSError,ValueError,TypeError,KeyError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:
        print('VERIFICATION FAILED: '+str(e),file=sys.stderr)
        sys.exit(1)
