"""Render the unchanged original once; no scientific/support program execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess
import time

R = Path(__file__).resolve().parent
assert R.name == 'root-initial-20261117' and R.parent.parent.name == '23411227'
S = R.parent.parent / 'sources'
sha = lambda b: hashlib.sha256(b).hexdigest()
pins = {'SOURCE_FINAL.json':'46a1f71e118fff3101c7f0af2158658847ad338172d7bd6d119ba041c8613886',
        'SOURCE_MANIFEST.json':'3bd41786837658193a0258d1f1a70dc719f0e321647ed885294e9947f64a1e7b',
        'assets/rank-two-fano-note.pdf':'38b4897c731fe9916a7ae8eaf3cb6c62352631f24776b9b93f9af61807ab0060',
        'published-source/container-001/tree/note.tex':'58fc08b947c20e4d00fb6a379a109e8489aa6a22b1f2161587980ada95c318bc',
        'record.response.body':'f2e9d52d8cd6a35328dfcab864b3b1dff00f9bf9b60967ac6072d2dd0d4b92a1'}
def inventory():
    rows = []
    for path in [S] + sorted(S.rglob('*')):
        info = path.lstat()
        assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
        row = {'path':path.relative_to(S).as_posix(),'mode':oct(stat.S_IMODE(info.st_mode)),
               'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns}
        if path.is_dir():
            row.update(kind='directory', empty=not any(path.iterdir()))
        else:
            raw = path.read_bytes()
            row.update(kind='file', bytes=len(raw), SHA256=sha(raw), empty=not raw)
        rows.append(row)
    assert sum(x['kind']=='file' for x in rows)==196
    assert sum(x['kind']=='directory' for x in rows)==22
    for path, digest in pins.items():
        assert sha((S/path).read_bytes()) == digest, path
    return rows
def save(name, value):
    with (R/name).open('x') as f:
        f.write(json.dumps(value,indent=2)+'\n')
assert not (R/'png').exists() and not (R/'RENDER_EXECUTION.json').exists()
before = inventory()
save('SOURCE_BEFORE.json',before)
(R/'png').mkdir()
argv=['/opt/homebrew/bin/pdftoppm','-png','-scale-to','1500',str(S/'assets/rank-two-fano-note.pdf'),str(R/'png/page')]
start=datetime.now(timezone.utc).isoformat()
clock=time.monotonic()
run=subprocess.run(argv,capture_output=True)
elapsed=time.monotonic()-clock
(R/'render.stdout').write_bytes(run.stdout)
(R/'render.stderr').write_bytes(run.stderr)
after=inventory()
save('SOURCE_AFTER.json',after)
save('RENDER_EXECUTION.json',{'argv':argv,'UTC_start':start,'UTC_end':datetime.now(timezone.utc).isoformat(),
     'elapsed_seconds':elapsed,'exit':run.returncode,'stdout_bytes':len(run.stdout),'stderr_bytes':len(run.stderr),
     'stdout_SHA256':sha(run.stdout),'stderr_SHA256':sha(run.stderr),'source196_21_before_after_exact':before==after,
     'scientific_program_executions':0,'attempts':1,'retries':0})
assert run.returncode==0 and before==after
assert sorted(x.name for x in (R/'png').iterdir())==['page-1.png','page-2.png','page-3.png','page-4.png','page-5.png']
print(json.dumps({'render_exit':0,'pages':5,'source196_21_exact':True,'scientific_program_executions':0}))
