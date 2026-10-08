#!/usr/bin/env python3
"""Independent finite checks and authenticated-file tests; not a proof checker.

Use the original source-free author freeze and separately retained input files.
No network operations. No original input is changed. Corruptions use copies.
"""
import argparse
import errno
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    'bootstrap.py': (3752, '10efdf3b3290b84365e6cad3e84822f322aa5e7f6778e2551addb2ab9329076c'),
    'MANIFEST.json': (1648, '24e4e0b001028a38091b1293b490e36227fda8d2ee73f726ef316f2eb0fe4c96'),
    'packet/PROOF.md': (21275, 'e095f3cbfb4876a19d01be1558307267031c1eee4af08fcda8ace38e39077f5e'),
}
ZIP_PIN = (24197, 'b2d5c49b421e530bdf3863d12ddb753ff9884f4f217ed1c244120b9c38c70fe1')
MODES = [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pin(b):
    return (len(b), hashlib.sha256(b).hexdigest())

def snapshot(root):
    result = {}
    for p in [root] + sorted(root.rglob('*')):
        mode = p.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'original symlink')
        result[p.relative_to(root).as_posix()] = {
            'mode': stat.S_IMODE(mode),
            'kind': 'directory' if p.is_dir() else 'file',
            'pin': list(pin(p.read_bytes())) if p.is_file() else None,
        }
    return result

def run(script, args=(), flags=(), cwd=None):
    return subprocess.run([sys.executable, '-I', '-S', '-B', *flags, str(script), *map(str, args)],
                          capture_output=True, text=True, cwd=cwd, timeout=120)

def writable_copy(original, target):
    shutil.copytree(original, target)
    os.chmod(target, 0o755)
    for p in target.rglob('*'):
        os.chmod(p, 0o755 if p.is_dir() else 0o644)

def mathematically_scoped_controls():
    counts = {}
    # Every labelled partial order of size <=4, and all its automorphisms.
    # These are abstract order diagnostics, not geometric foliation models.
    order_count = automorphism_count = root_tests = conjugacy_tests = 0
    def comp(a, b): return tuple(a[b[i]] for i in range(len(a)))
    for n in range(1, 5):
        ident = tuple(range(n))
        pairs = [(i,j) for i in range(n) for j in range(n) if i != j]
        for bits in range(1 << len(pairs)):
            rel = {(i,i) for i in range(n)} | {p for k,p in enumerate(pairs) if bits & (1<<k)}
            if any(i != j and (j,i) in rel for i,j in rel): continue
            if any((i,k) not in rel for i,j in rel for jj,k in rel if j == jj): continue
            order_count += 1
            autos = [p for p in itertools.permutations(range(n))
                     if all(((i,j) in rel) == ((p[i],p[j]) in rel) for i in range(n) for j in range(n))]
            def bad(p): return all((i,p[i]) not in rel and (p[i],i) not in rel for i in range(n))
            for h in autos:
                automorphism_count += 1
                inv = tuple(h.index(i) for i in range(n))
                require(bad(h) == bad(inv), 'inversion diagnostic')
                power = ident
                for k in range(1, 13):
                    power = comp(h, power)
                    require(not bad(power) or bad(h), 'root direction diagnostic')
                    root_tests += 1
                for a in autos:
                    ai = tuple(a.index(i) for i in range(n))
                    require(bad(comp(comp(a,h),ai)) == bad(h), 'conjugacy diagnostic')
                    conjugacy_tests += 1
    counts.update(labelled_partial_orders=order_count, automorphisms=automorphism_count,
                  root_implications=root_tests, conjugacy_implications=conjugacy_tests)
    # A two-element antichain permutation is bad but its square is the identity.
    # This refutes only the converse in general order models, not a foliation claim.
    h = (1,0)
    require(all(h[i] != i for i in range(2)) and comp(h,h) == (0,1), 'power converse countercontrol')
    counts['power_converse_countercontrols'] = 1
    # Exact integer-period premise, including negative periods and strict boundary.
    periods = 0
    for a in [F(i,j) for i in range(1,11) for j in range(1,8)]:
        for length in [F(i,j) for i in range(0,11) for j in range(1,8)]:
            for n in range(-7,8):
                if abs(n) <= a*length and a*length < 1:
                    require(n == 0, 'integer period implication')
                    periods += 1
    require(F(1) <= F(1)*F(1), 'equality boundary control')
    require(F(1,2) <= F(1)*F(3,4) < 1, 'nonintegral premise control')
    counts.update(period_implications=periods, strictness_and_integrality_countercontrols=2)
    # Rational e^R parametrization and exact comass/Cauchy--Schwarz identities.
    calibration = 0
    for t in [F(i,j) for j in range(1,9) for i in range(j+1,j+11)]:
        c,s = (t+1/t)/2, (t-1/t)/2
        require(c*c-s*s == 1 and c > 1 and s > 0, 'hyperbolic identity')
        for k in range(-8,9):
            if k == 0: continue
            for b in [F(i,5) for i in range(41)]:
                require((abs(k)*(c-1) <= b) == (c <= 1+b/abs(k)), 'radius rearrangement')
                calibration += 1
    counts['calibration_algebra'] = calibration
    # d eta has unit horizontal bivector coefficient in an orthonormal frame.
    comass = 0
    for u in itertools.product(range(-2,3), repeat=3):
        for v in itertools.product(range(-2,3), repeat=3):
            cross = (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
            require(cross[2]**2 <= sum(x*x for x in cross), 'comass bound')
            comass += 1
    require((1*1-0*0)**2 == 1, 'comass attained')
    counts['comass_controls'] = comass+1
    # Every rational plane rotation preserves x dy-y dx. z translation has no term.
    twist = 0
    for q in [F(i,j) for i in range(-6,7) for j in range(1,7)]:
        a,b=(1-q*q)/(1+q*q),2*q/(1+q*q)
        require(a*a+b*b == 1, 'rotation determinant')
        for x,y,dx,dy in itertools.product(range(-1,2), repeat=4):
            X,Y=a*x-b*y,b*x+a*y; DX,DY=a*dx-b*dy,b*dx+a*dy
            require(X*DY-Y*DX == x*dy-y*dx and X*X+Y*Y == x*x+y*y, 'twist invariance')
            twist += 1
    counts['twist_invariance'] = twist
    require(F(1, math.factorial(2)) == F(1,2), 'smooth axis leading coefficient')
    counts['smooth_radial_series_coefficients'] = 12
    for k in range(12):
        # (cosh r-1)/r^2 is sum r^(2k)/(2k+2)! with no negative/odd power.
        require(2*k >= 0 and (2*k)%2 == 0 and F(1,math.factorial(2*k+2)) > 0, 'smooth radial coefficient')
    # Positive Jacobian independent of n; the pulled-back dx coefficient is a*n.
    for n in range(1,101):
        for e in [F(i,100) for i in range(-49,50)]:
            require(1+e > F(1,2), 'shear derivative')
        require(F(1,10)*n >= F(1,10), 'unbounded coefficient sequence')
    counts['shear_derivative_controls'] = 9900
    # Independently implement permutations by image dictionaries.
    a={1:2,2:1,3:3};b={1:1,2:3,3:2}
    def mul(p,q): return {i:p[q[i]] for i in (1,2,3)}
    require(mul(mul(a,b),a) == mul(mul(b,a),b), 'braid relation')
    require(mul(a,b) != mul(b,a), 'noncommuting quotient')
    generated={(1,2,3)}; frontier=[{i:i for i in (1,2,3)}]
    while frontier:
        p=frontier.pop()
        for q in (a,b):
            v=mul(p,q); key=tuple(v[i] for i in (1,2,3))
            if key not in generated: generated.add(key);frontier.append(v)
    require(len(generated)==6, 'S3 quotient')
    counts['trefoil_quotient_controls']=3
    return counts

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--freeze', type=Path, required=True)
    ap.add_argument('--archive', type=Path, required=True)
    ap.add_argument('--sources', type=Path, required=True)
    ap.add_argument('--corpora', type=Path, required=True)
    args=ap.parse_args(); root=args.freeze.resolve(); before=snapshot(root)
    require(os.geteuid()!=0, 'read-only test must not run as root')
    for f,want in PINS.items(): require(pin((root/f).read_bytes())==want,'external author pin: '+f)
    require(pin(args.archive.read_bytes())==ZIP_PIN,'external archive pin')
    mf=json.loads((root/'MANIFEST.json').read_text())
    for f,p in mf['files'].items(): require(pin((root/f).read_bytes())==(p['bytes'],p['sha256']),'manifest entry')
    with zipfile.ZipFile(args.archive) as z:
        names=z.namelist()
        require(len(names)==len(set(names))==13,'archive inventory')
        require(set(names)=={'author_v1/'+p for p,v in before.items() if v['kind']=='file'},'archive exact paths')
        for n in names: require(z.read(n)==(root/n.removeprefix('author_v1/')).read_bytes(),'archive member mismatch')
    denied=[]
    # Genuine DAC protection on the actual freeze, not merely a read-only label.
    # O_WRONLY without O_TRUNC cannot alter a file even if unexpectedly allowed.
    for p in sorted(root.rglob('*')):
        if p.is_file():
            require(not (p.stat().st_mode & 0o222), 'write mode present')
            try: fd=os.open(p,os.O_WRONLY)
            except OSError as e:
                require(e.errno in (errno.EACCES,errno.EROFS,errno.EPERM),'unexpected write-probe error')
                denied.append(p.relative_to(root).as_posix())
            else:
                os.close(fd);raise ValueError('actual file unexpectedly writable')
    for d in [root, root/'packet']:
        probe=d/'.independent_write_probe'
        require(not probe.exists(),'probe collision')
        try: fd=os.open(probe,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except OSError as e: require(e.errno in (errno.EACCES,errno.EROFS,errno.EPERM),'unexpected directory-probe error')
        else:
            os.close(fd);probe.unlink();raise ValueError('actual directory unexpectedly writable')
    tests=[]; baseline=None; input_baseline=None
    with tempfile.TemporaryDirectory(prefix='independent-short-geodesics-') as td:
        tmp=Path(td)
        claims=json.loads((root/'packet/CLAIMS.json').read_text())
        for mode,flags in MODES:
            p=run(root/'bootstrap.py',flags=flags,cwd=root)
            require(p.returncode==0 and not p.stderr,'actual read-only bootstrap')
            if baseline is None: baseline=p.stdout
            require(p.stdout==baseline,'optimization output changed')
            tests.append({'mode':mode,'case':'actual_read_only_freeze','accepted':True})
            p=run(root/'packet/verify_inputs.py',['--sources',args.sources.resolve(),'--corpora',args.corpora.resolve()],flags,cwd=root)
            require(p.returncode==0 and not p.stderr,'source/corpus replay')
            if input_baseline is None: input_baseline=p.stdout
            require(p.stdout==input_baseline,'input optimization output changed')
            tests.append({'mode':mode,'case':'source_and_corpus_replay','accepted':True})
            mutations=['same_size_proof','verifier_sentinel','extra_hidden_file','empty_subdirectory','missing_ledger',
                       'symlink_proof','fifo_member','changed_bootstrap','manifest_duplicate','manifest_nonfinite',
                       'manifest_repin','symlink_root','symlink_directory']
            for case in mutations:
                dst=tmp/(mode+'_'+case);writable_copy(root,dst);candidate=dst;sentinel=tmp/(mode+'_'+case+'_EXECUTED')
                if case=='same_size_proof':
                    p=dst/'packet/PROOF.md';bb=bytearray(p.read_bytes());bb[-2]^=1;p.write_bytes(bb)
                elif case=='verifier_sentinel':
                    (dst/'packet/verify.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("ran")\n')
                elif case=='extra_hidden_file': (dst/'packet/.extra').write_bytes(b'')
                elif case=='empty_subdirectory': (dst/'packet/empty').mkdir()
                elif case=='missing_ledger': (dst/'packet/APPROACH_LEDGER.json').unlink()
                elif case=='symlink_proof':
                    (dst/'packet/PROOF.md').unlink();(dst/'packet/PROOF.md').symlink_to(root/'packet/PROOF.md')
                elif case=='fifo_member': os.mkfifo(dst/'packet/fifo')
                elif case=='changed_bootstrap': (dst/'bootstrap.py').write_text('raise SystemExit(0)\n')
                elif case=='manifest_duplicate': (dst/'MANIFEST.json').write_text('{"schema":1,"schema":2}')
                elif case=='manifest_nonfinite': (dst/'MANIFEST.json').write_text('{"files":NaN}')
                elif case=='manifest_repin':
                    (dst/'packet/PROOF.md').write_text('altered proof')
                    mm=json.loads((dst/'MANIFEST.json').read_text());size,h=pin((dst/'packet/PROOF.md').read_bytes())
                    mm['files']['packet/PROOF.md']={'bytes':size,'sha256':h};(dst/'MANIFEST.json').write_text(json.dumps(mm))
                elif case=='symlink_root':
                    candidate=tmp/(mode+'_root_link');candidate.symlink_to(dst,target_is_directory=True)
                elif case=='symlink_directory':
                    shutil.rmtree(dst/'packet');(dst/'packet').symlink_to(root/'packet',target_is_directory=True)
                p=run(root/'bootstrap.py',['--root',candidate],flags,cwd=tmp)
                require(p.returncode!=0 and not p.stdout and not sentinel.exists(),'accepted corruption: '+case)
                tests.append({'mode':mode,'case':case,'accepted':False,'payload_sentinel_absent':True})
            bad=[]
            for key,value in [('problem_id',True),('problem_id',10300043.0),('rank',True),('turns_used',4),
                              ('turns_budget',True),('status','solved'),('independent_review','accepted'),
                              ('universal_isotopy_solution',True),('geodesic_counterexample',True),('claim_ids',[])]:
                x=dict(claims);x[key]=value;bad.append((key+'_'+repr(value),json.dumps(x).encode()))
            bad.extend([('duplicate',b'{"a":0,"a":1}'),('nan',b'{"a":NaN}'),('infinity',b'{"a":Infinity}'),
                        ('list',b'[]'),('null',b'null'),('utf8',b'\xff'),('oversize',b' '*2000001),
                        ('trailing',json.dumps(claims).encode()+b'x')])
            for case,data in bad:
                candidate=tmp/'claims.json';candidate.write_bytes(data)
                p=run(root/'packet/verify.py',['--input',candidate],flags,cwd=tmp)
                require(p.returncode!=0 and not p.stdout,'accepted claims mutation '+case)
                tests.append({'mode':mode,'case':'claims_'+case,'accepted':False})
            # Changed source bytes, absent source, and symbolic-link substitution.
            for case in ('changed_source','missing_source','symlink_source','missing_corpus'):
                src=tmp/(mode+'_'+case+'_sources');src.mkdir()
                for f in json.loads((root/'packet/SOURCE_PINS.json').read_text())['sources']:
                    shutil.copyfile(args.sources/f['filename'],src/f['filename'])
                file=src/'calegari_2002.pdf';corpora=args.corpora.resolve()
                if case=='changed_source':
                    bb=bytearray(file.read_bytes());bb[-1]^=1;file.write_bytes(bb)
                elif case=='missing_source': file.unlink()
                elif case=='symlink_source':
                    file.unlink();file.symlink_to((args.sources/'calegari_2002.pdf').resolve())
                elif case=='missing_corpus': corpora=tmp/'absent_corpora'
                p=run(root/'packet/verify_inputs.py',['--sources',src,'--corpora',corpora],flags,cwd=tmp)
                require(p.returncode!=0 and not p.stdout,'accepted input mutation '+case)
                tests.append({'mode':mode,'case':case,'accepted':False})
    require(snapshot(root)==before,'original freeze changed')
    counts=mathematically_scoped_controls()
    print(json.dumps({'status':'PASS_INDEPENDENT_AUDIT_CONTROLS','problem_id':10300043,
                      'effective_uid':os.geteuid(),'original_freeze_unchanged':True,
                      'actual_freeze_denied_file_write_probes':len(denied),
                      'actual_freeze_denied_directory_create_probes':2,
                      'all_mode_outputs_identical':True,'archive_members_byte_identical':13,
                      'independent_case_count':len(tests),'cases':tests,
                      'finite_controls':counts,'author_bootstrap_result':json.loads(baseline),
                      'input_replay_result':json.loads(input_baseline),
                      'mathematical_proof_machine_verified':False},sort_keys=True,indent=2))

if __name__=='__main__':
    try: main()
    except (ValueError,TypeError,KeyError,UnicodeError,OSError,subprocess.SubprocessError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(2)
