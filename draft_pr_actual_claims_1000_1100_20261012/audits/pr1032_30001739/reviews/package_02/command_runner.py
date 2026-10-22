#!/usr/bin/env python3
"""Record real subprocess argv, status, stdout and stderr; never infer success."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys, time
ROOT = Path(__file__).resolve().parent

def run(name, argv, cwd=None, timeout=120, expected=0):
    begin = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start = time.monotonic()
    outcome = 'completed'
    try:
        p = subprocess.run(list(map(str, argv)), cwd=cwd, capture_output=True, timeout=timeout)
        code, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        outcome, code, out, err = 'timeout_incomplete', None, e.stdout or b'', e.stderr or b''
    except OSError as e:
        outcome, code, out, err = 'launch_failed_incomplete', None, b'', str(e).encode()
    (ROOT/'commands'/f'{name}.stdout').write_bytes(out)
    (ROOT/'commands'/f'{name}.stderr').write_bytes(err)
    row = dict(name=name, argv=list(map(str, argv)), cwd=str(cwd) if cwd else None,
               started_utc=begin, duration_s=time.monotonic()-start, outcome=outcome,
               returncode=code, expected_exit=expected, expectation_met=code==expected,
               stdout_bytes=len(out), stdout_sha256=hashlib.sha256(out).hexdigest(),
               stderr_bytes=len(err), stderr_sha256=hashlib.sha256(err).hexdigest())
    (ROOT/'commands'/f'{name}.json').write_text(json.dumps(row,indent=2)+'\n')
    print(json.dumps({k:row[k] for k in ('name','outcome','returncode','expectation_met','stdout_bytes','stderr_bytes')}))
    return row

if __name__ == '__main__':
    audit=ROOT.parents[1]; candidate=audit/'preprint_v1_1'
    run('pdfinfo', ['/opt/homebrew/bin/pdfinfo', candidate/'paper.pdf'])
    run('candidate_render', ['/opt/homebrew/bin/pdftoppm','-scale-to','1350','-png',candidate/'paper.pdf',ROOT/'source_renders'/'candidate'])
    run('candidate_text', ['/opt/homebrew/bin/pdftotext','-layout',candidate/'paper.pdf',ROOT/'source_renders'/'candidate.txt'])
    for flag, tag in (([], 'normal'), (['-O'],'O'), (['-OO'],'OO')):
        run('kit_'+tag,[sys.executable,'-I','-B',*flag,candidate/'kit/scripts/verify_kit.py','--archive',candidate/'pr1032_supportkit_v1.1.zip'])
    out=ROOT/'fixtures/compile';out.mkdir()
    run('tectonic_offline',['/opt/homebrew/bin/tectonic','--only-cached','--keep-logs','--outdir',out,candidate/'paper.tex'])
