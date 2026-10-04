#!/usr/bin/env python3
"""Lossless command capture; no shell expansion or index mutation."""
import datetime, gzip, hashlib, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
PRIVATE = ROOT / 'private'
PRIVATE.mkdir(exist_ok=True)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run(name, argv, cwd=None):
    started = now()
    p = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for stream, data in [('stdout',p.stdout),('stderr',p.stderr)]:
        with gzip.open(PRIVATE / (name + '.' + stream + '.gz'),'wb') as f: f.write(data)
    info = dict(name=name, argv=argv, cwd=str(cwd or pathlib.Path.cwd()), started_utc=started,
                finished_utc=now(), exit_code=p.returncode, stdout_bytes=len(p.stdout), stderr_bytes=len(p.stderr),
                stdout_sha256=hashlib.sha256(p.stdout).hexdigest(), stderr_sha256=hashlib.sha256(p.stderr).hexdigest(),
                stdout_stored='private/'+name+'.stdout.gz',stderr_stored='private/'+name+'.stderr.gz')
    (PRIVATE/(name+'.json')).write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info))
    return p

if __name__ == '__main__':
    if len(sys.argv) < 4: raise SystemExit('usage: capture.py name cwd command [args]')
    p=run(sys.argv[1],sys.argv[3:],sys.argv[2])
    raise SystemExit(p.returncode)
