#!/usr/bin/env python3
"""Independent exact identities and release corruption tests; no live writes."""
import copy
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import types
import zipfile
import sympy as s

HERE = Path(__file__).absolute().parent
A = HERE.parents[1]
REPO = A.parents[2]
TMP = HERE / 'tmp'
TMP.mkdir(exist_ok=True)
RESULTS = []

def check(label, value):
    if not bool(value):
        raise ValueError('failed control: ' + label)
    RESULTS.append({'label': label, 'status': 'PASS'})

def rejects(label, function):
    try:
        function()
    except (ValueError, FileNotFoundError, OSError, KeyError):
        RESULTS.append({'label': label, 'status': 'REJECTED_AS_REQUIRED'})
    else:
        raise ValueError('corruption accepted: ' + label)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path, name):
    obj = types.ModuleType(name)
    obj.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), obj.__dict__)
    return obj

def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha(data)}

def exact():
    x, y, a, t = s.symbols('x y a t', real=True)
    z = x + s.I*y
    q = s.symbols('q')
    kp = q/(1-q)**2
    km = q/(1+q)**2
    h = q/(1-q**2)
    P = lambda f: s.cancel(s.diff(f,q,2)/s.diff(f,q))
    Af = lambda f: s.cancel((1-x*x-y*y)*P(f).subs(q,z)-2*s.conjugate(z))
    delta2 = y*y/((1-z*z)*(1-s.conjugate(z)**2))
    for label, f in [('plus',kp),('minus',km)]:
        B = Af(f)
        check(label+' Koebe full complex deficit', s.cancel(B*s.conjugate(B)-(16-48*delta2)) == 0)
    check('two opposite real endpoints', s.cancel(Af(kp).subs(y,0)-4) == 0 and s.cancel(Af(km).subs(y,0)+4) == 0)
    check('h value at imaginary point', s.cancel(Af(h).subs({x:0,y:t})-8*s.I*t/(1+t*t)) == 0)
    u, v = s.symbols('u v')
    check('h univalence factorization', s.cancel(h.subs(q,u)-h.subs(q,v)-(u-v)*(1+u*v)/((1-u*u)*(1-v*v))) == 0)
    check('delta denominator identity', s.expand((1-z*z)*(1-s.conjugate(z)**2)-(1-x*x-y*y)**2-4*y*y) == 0)
    phi = (z+a)/(1+a*z)
    phib = s.conjugate(phi)
    imphi = s.cancel((phi-phib)/(2*s.I))
    check('imaginary numerator covariance', s.cancel(imphi-y*(1-a*a)/((1+a*z)*(1+a*s.conjugate(z)))) == 0)
    check('delta squared invariance', s.cancel(imphi**2/((1-phi*phi)*(1-phib*phib))-delta2) == 0)
    check('automorphism inverse', s.cancel(((phi-a)/(1-a*phi))-z) == 0)
    phase = (1+a*s.conjugate(z))/(1+a*z)
    check('phase unimodularity', s.cancel(phase*s.conjugate(phase)-1) == 0)
    p0=s.symbols('p0')
    derivative=(1-a*a)/(1+a*z)**2
    Ptrans=p0*derivative-2*a/(1+a*z)
    left=(1-x*x-y*y)*Ptrans-2*s.conjugate(z)
    right=phase*((1-phi*phib)*p0-2*phib)
    check('covariance for arbitrary jet', s.cancel(left-right) == 0)
    check('growth integral derivative', s.cancel(s.diff(s.log((1+t)/(1-t)**3),t)-(4+2*t)/(1-t*t)) == 0)
    check('function growth integral', s.cancel(s.diff(t/(1-t)**2,t)-(1+t)/(1-t)**3) == 0)
    d=s.Rational(2,5)
    check('i/2 Koebe lower squared', 16*(1-3*d*d) == s.Rational(208,25))
    check('i/2 second lower squared', (8*d)**2 == s.Rational(256,25))
    check('crossing lower bounds', s.simplify(16*(1-3/s.Integer(7))-64/s.Integer(7)) == 0)
    av=(kp+km)/2
    critical=s.I*(s.sqrt(2)-1)
    check('convex average derivative simple zero', s.simplify(s.diff(av,q).subs(q,critical)) == 0 and s.simplify(s.diff(av,q,2).subs(q,critical)) != 0)
    ep=s.symbols('ep',positive=True)
    check('Euclidean near-endpoint counterlimit', s.limit(s.cancel(delta2.subs({x:1-ep,y:ep})),ep,0,dir='+') == s.Rational(1,8))
    # A wrong phase is a substantive mutation and is detected without asserts.
    wrong=1/phase*((1-phi*phib)*p0-2*phib)
    check('inverse covariance phase mutation detected', s.cancel(left-wrong).subs({x:s.Rational(1,5),y:s.Rational(1,4),a:s.Rational(1,3),p0:2}) != 0)
    check('radius squared optimum not falsely equated to lower envelope', s.Rational(256,25) > s.Rational(208,25))

def archive_and_native():
    archive_bytes=(A/'publication/real_schlicht_verification.zip').read_bytes()
    check('known exact accepted archive', len(archive_bytes)==307142 and sha(archive_bytes)=='945c5e52a136bd0187d51661140b617965c064c880628bdbeff3324516b9bc04')
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        entries=archive.infolist()
        check('101 unique sorted ZIP paths', len(entries)==101 and [e.filename for e in entries]==sorted({e.filename for e in entries}))
        check('ZIP regular modes dates and no encryption', all(e.external_attr>>16==0o100644 and e.date_time==(2026,10,15,0,0,0) and not(e.flag_bits&1) for e in entries))
        payload={e.filename:archive.read(e) for e in entries}
        check('ZIP CRC', archive.testzip() is None)
    # Inspect both nested authored archives, rather than accepting extensions alone.
    nested_inventory={}
    for name,data in payload.items():
        check('no source scans, page images, operational journals or caches: '+name,
              not name.endswith(('.png','.jpg','.jpeg','.pyc')) and '/tmp/' not in name and
              not any(token in name for token in ('ZENODO_', 'TRACKER_', 'INTEGRATION_', '__pycache__')))
        if name.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(data)) as nested:
                names=nested.namelist();nested_inventory[name]=names
                check('nested authored archive has no raw PDFs/images', all(not n.lower().endswith(('.pdf','.png','.jpg','.jpeg')) for n in names))
    snapshot=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_bytes())
    expected=snapshot['original_blobs']
    check('selected scope claimed_solved', snapshot['status']=='claimed_solved' and '| claimed_solved | 5/5 |' in snapshot['queue_row'])
    tree=subprocess.check_output(['git','ls-tree','-r','-z',snapshot['original_head'],'--','unsolved_math_prioritization/attempts/2306086'],cwd=REPO)
    actual={}
    for row in tree.split(b'\0'):
        if not row:continue
        fields,path=row.split(b'\t');mode,kind,oid=fields.decode().split()
        actual[path.decode()]={'git_mode':mode,'kind':kind,'git_blob':oid}
    check('Git original 24 exact paths', set(actual)==set(expected) and len(actual)==24)
    for name,record in expected.items():
        data=subprocess.check_output(['git','cat-file','blob',record['git_blob']],cwd=REPO)
        check('Git/native/archive bytes '+name, actual[name]=={'git_mode':record['git_mode'],'kind':'blob','git_blob':record['git_blob']} and
              len(data)==record['size'] and sha(data)==record['sha256'] and data==(A/'native'/name).read_bytes() and data==payload['native/'+name])
    (HERE/'NESTED_ARCHIVE_INVENTORIES.json').write_text(json.dumps(nested_inventory,indent=2)+'\n')
    return payload

def release_tests(payload, numerical=False):
    packet=TMP/'packet'
    if packet.exists():shutil.rmtree(packet)
    packet.mkdir()
    for name,data in payload.items():
        path=packet/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    V=load(packet/'verify_package.py','_round2_verifier')
    before={n:sha((packet/n).read_bytes()) for n in payload}
    check('standalone verifier actual archive', V.verify(packet)['status']=='PASS')
    replay=V.replay(packet,numerical=numerical)
    check('isolated full replay', replay['status']=='PASS' and replay['optimizer_executed'] is False)
    check('package unchanged after full replay', before=={n:sha((packet/n).read_bytes()) for n in payload})
    (HERE/('PACKAGE_REPLAY.numerical.json' if numerical else 'PACKAGE_REPLAY.exact.json')).write_text(json.dumps(replay,indent=2)+'\n')
    original_manifest=payload['PACKAGE_MANIFEST.json']
    def update_manifest(name,data):
        m=json.loads(original_manifest)
        for r in m['files']:
            if r['path']==name:r.update(bytes=len(data),sha256=sha(data))
        (packet/'PACKAGE_MANIFEST.json').write_text(json.dumps(m))
    changed_cases=[
        ('outer digest mismatch','README.md',payload['README.md']+b'corrupt',False),
        ('native corruption with recomputed manifest',V.NATIVE+'/README.md',payload[V.NATIVE+'/README.md']+b'changed',True),
        ('source scope corruption with recomputed manifest','SCOPE_AND_SNAPSHOT.json',payload['SCOPE_AND_SNAPSHOT.json']+b' ',True),
        ('sharp claim inflated with recomputed manifest','CLAIM_SCOPE.json',json.dumps(json.loads(payload['CLAIM_SCOPE.json'])|{'sharp_quantitative_radius':True}).encode(),True),
        ('numeric zero boolean substituted','CLAIM_SCOPE.json',json.dumps(json.loads(payload['CLAIM_SCOPE.json'])|{'source_expression_at_zero':False}).encode(),True),
        ('duplicate scope JSON key','CLAIM_SCOPE.json',payload['CLAIM_SCOPE.json'].rstrip()[:-1]+b',"claim":"wrong"}',True),
        ('QA PDF pin diverges','real_schlicht_preschwarzian.pdf',payload['real_schlicht_preschwarzian.pdf']+b'changed',True),
        ('deposit extra file','zenodo-deposit.json',json.dumps(json.loads(payload['zenodo-deposit.json'])|{'files':[{'path':'wrong'}]}).encode(),True),
    ]
    for label,name,data,rebase in changed_cases:
        (packet/name).write_bytes(data)
        if rebase:update_manifest(name,data)
        rejects(label,lambda:V.verify(packet))
        (packet/name).write_bytes(payload[name]);(packet/'PACKAGE_MANIFEST.json').write_bytes(original_manifest)
    for name in ['../escape','/absolute','x//y','x/./y','x/../y','x\\y','x:y','x\x00y']:
        rejects('unsafe manifest name '+repr(name),lambda name=name:V.safe_name(name))
    extra=packet/'UNMANIFESTED';extra.write_bytes(b'extra')
    rejects('unmanifested file',lambda:V.verify(packet));extra.unlink()
    empty=packet/'empty';empty.mkdir();rejects('empty directory',lambda:V.verify(packet));empty.rmdir()
    readme=packet/'README.md';readme.unlink();readme.symlink_to(packet/'CURRENT_PRIORITY_AND_STATUS.md')
    rejects('symlinked payload',lambda:V.verify(packet));readme.unlink();readme.write_bytes(payload['README.md'])
    m=json.loads(original_manifest);m['files'].append(copy.deepcopy(m['files'][0]));m['file_count']+=1
    (packet/'PACKAGE_MANIFEST.json').write_text(json.dumps(m));rejects('duplicate manifest record',lambda:V.verify(packet))
    (packet/'PACKAGE_MANIFEST.json').write_bytes(original_manifest)
    check('all tamper fixtures restored',V.verify(packet)['status']=='PASS')
    # Reconstruct the complete build layout under this review only.
    layout=TMP/'builder-layout'
    if layout.exists():shutil.rmtree(layout)
    pub=layout/'publication';pub.mkdir(parents=True)
    for name,data in payload.items():
        if name=='PACKAGE_MANIFEST.json':continue
        target=pub/('PACKAGE_README.md' if name=='README.md' else name) if name in V.PUBLICATION_FILES else layout/name
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    built=[]
    for i in range(2):
        result=subprocess.run([sys.executable,'-I','-B',str(pub/'build_package.py')],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=120)
        check('isolated deterministic builder success '+str(i),result.returncode==0)
        built.append((pub/'real_schlicht_verification.zip').read_bytes())
    check('rebuild matches exact original ZIP twice',built[0]==built[1]==(A/'publication/real_schlicht_verification.zip').read_bytes())

def main():
    exact();payload=archive_and_native();release_tests(payload,numerical='--numerical' in sys.argv)
    report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'checks':len(RESULTS),'optimized':sys.flags.optimize>0,'results':RESULTS,
            'no_live_service_or_remote_mutations':True,'temporary_copies_only':True,
            'numerical_certification':False,'formal_proof_certificate':False}
    output=HERE/('INDEPENDENT_CHECKS.optimized.json' if sys.flags.optimize else 'INDEPENDENT_CHECKS.normal.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','checks':len(RESULTS),'optimized':sys.flags.optimize>0}))

if __name__=='__main__':main()
