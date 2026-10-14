#!/usr/bin/env python3
"""Independent frozen-package tests; mutations are confined to .cache copies.

This is finite rational/packaging verification, not an analytic formalization.
The frozen producer is replayed on a temporary audit subtree in .cache.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction as F
import copy
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
PUB = AUDIT / 'publication'
CACHE = HERE / '.cache'
EXPECTED = {
    'support_slit.pdf': '134c3e24a4a2d1db58a2f9744477491e05b0bc14297b3e23621138c00a22ecbc',
    'verification_package.zip': '1115899b96895d6e3a06eee1d42fd621450518b5e282f3d6898fdf76cac80be3',
    'make_package.py': '5e6a400191a77597e5a1858f26270c7e7960d9738fd651d76c4408012134519a',
}
CHECKS = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(name, condition, detail=None):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append({'name': name, 'passed': True, 'detail': detail})


def dump(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def archive_inventory(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in root.rglob('*') if p.is_file()
            and not {'.venv', '__pycache__'} & set(p.relative_to(root).parts)}


def run(root, *, args=None, env=None, python=None):
    return subprocess.run([str(python or PYTHON), *(args or []), str(root/'run_all.py')],
                          cwd=root, capture_output=True, text=True,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', **(env or {})))


def retarget_outer(root, names):
    path = root / 'MANIFEST.json'
    m = json.loads(path.read_text())
    for name in names:
        d = (root/name).read_bytes()
        m['files'][name] = {'bytes': len(d), 'sha256': sha(d)}
    dump(path, m)


def new_copy(name):
    root = CACHE / 'controls' / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(FRESH, root, ignore=shutil.ignore_patterns('.venv', '__pycache__'))
    return root


def rational_checks():
    e, h, T = F(1, 10**24), F(1, 10**12), F(7, 4)
    q = lambda t: t*t - F(2, 5)*t**4
    check('epsilon is exactly eta squared', e == h*h)
    check('uniform a2 proximity margin', F(52) < 8**2)
    check('uniform a3 tail bound', F(4*13, 3) < 5**2)
    check('uniform a3 total bound', F(5)+F(3,4)*8*4 == 29)
    check('uniform A and B bounds', 2*29+8*6 == 106 and 3*8 == 24)
    r = F(2,3)
    check('area-theorem H tail and derivative bounds',
          r**4/(3*(1-r*r)) == F(16,135) < F(1,4)
          and (1-r*r)**-2 - 1 == F(56,25) < F(9,4)
          and 4*r + 2 < 5 and 4 + 4*F(3,2) == 10)
    check('H denominator range at actual zstar',
          F(5,3)-5*h > F(3,2) and F(5,3)+5*h < F(11,6))
    check('reciprocal-square error below two eta after zstar multiplication',
          r*5*F(7,2)/(F(3,2)**2*F(5,3)**2) == F(28,15) < 2)
    check('derivative two component budgets',
          19/F(3,2)**3 < 6 and F(1,3)*5*11/F(125,8) < 2)
    check('actual tip upper radius gate',
          F(6,25)+F(5,9)*F(9,125)==F(7,25)
          and 2+F(5,9)*8 < 7 and F(7,25)+7*h < F(3,10))
    check('polynomial, inverse and strict tip separation',
          106+24*9 == 322 and 2+3*9+81 == 110
          and 110+322*h < 111 and T+333*e < F(9,5)
          and F(25,81)-F(3,10) == F(7,810) > 0)
    check('orientation for entire tail and segment',
          222*e/(1-111*e) < 223*e < 1)
    check('analytic remainder absorption margins',
          F(111**2,2)*h < 1 and 18315*h < 1 and 45621*h < 1
          and 3*162 == 486 and 55*333 == 18315
          and F(126*333,2) == 20979 and 2*111**2 == 24642)
    check('division remainder exact worst-case budget',
          2*(T*162+487) == 1541 and 2*7*333 == 4662
          and 1541+4662*h < 2000)
    check('opposite target signs with epsilon over two margins',
          q(F(1)) == F(3,5) and q(T) == -F(441,640)
          and q(F(1))-2000*h > F(1,2)
          and q(T)+2000*h < -F(1,2))
    check('zero epsilon negative control: no strict witness',
          0*q(F(1)) == 0*q(T) == 0)
    check('short-segment negative control: endpoint signs need not reverse',
          q(F(1)) > 0 and q(F(3,2)) > 0)
    check('tip-exclusion negative control: continuation nonzero is insufficient',
          not (F(25,81) > F(2,5)))


def main():
    global FRESH, PYTHON
    FRESH = CACHE/'fresh/support_slit_verification'
    PYTHON = FRESH/'.venv/bin/python'
    check('fresh virtual environment exists', PYTHON.exists())
    installed = subprocess.run([str(PYTHON), '-c',
        'import sys,mpmath,json;print(json.dumps({"python":sys.version,"mpmath":mpmath.__version__}))'],
        capture_output=True, text=True, check=True)
    environment = json.loads(installed.stdout)
    check('fresh installed pinned dependency and supported Python',
          environment['mpmath']=='1.4.1' and sys.version_info >= (3,10), environment)
    for name, expected in EXPECTED.items():
        check('frozen digest '+name, sha((PUB/name).read_bytes()) == expected, expected)
    with zipfile.ZipFile(PUB/'verification_package.zip') as z:
        names=z.namelist()
        check('archive 221 members, unique safe relative paths, no symlinks',
              len(names)==221 and len(set(names))==221
              and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
              and all((i.external_attr >> 16) & 0o170000 != 0o120000 for i in z.infolist()))
        check('no fulltext/cache/account files in archive names',
              not any(n.endswith('.pdf') or any(x in PurePosixPath(n).parts for x in ['.cache','.venv','__pycache__']) for n in names))
        outer = json.loads(z.read('support_slit_verification/MANIFEST.json'))
        check('all 220 outer payload bytes/digests match', len(outer['files'])==220 and all(
              len(z.read('support_slit_verification/'+n))==v['bytes'] and
              sha(z.read('support_slit_verification/'+n))==v['sha256'] for n,v in outer['files'].items()))
    spec=importlib.util.spec_from_file_location('preflight_integrity',PUB/'integrity.py')
    integrity=importlib.util.module_from_spec(spec);spec.loader.exec_module(integrity)
    payloads={n:(FRESH/n).read_bytes() for n in outer['files']}
    registry=json.loads(payloads['SEALS.json'])
    check('all fourteen nested seals including source06 authored_outputs schema',
          len(registry)==14 and integrity.verify_nested(payloads,registry)==140)
    check('hidden gitignore is actually included and inner sealed',
          all('reviews/'+f+'/.gitignore' in payloads for f in
              ['priority06_zemyan2003','priority09_commentary_citations','priority10_adversary']))
    source06=json.loads(payloads['reviews/priority06_zemyan2003/CHECKS.json'])
    summary=json.loads(payloads['root_reproduction/supplied_primary_controls.json'])
    check('source06 full mathematical fields equal wrapper record',
          all(source06[k]==summary['priority06_zemyan2003'][k] for k in ['exact_controls','interval_controls']))
    for family in ['priority07_zemyan_bounds','priority08_radial_extrema',
                   'priority09_commentary_citations','priority10_adversary']:
        record_name = 'EXACT_CHECKS.json' if family in ['priority08_radial_extrema','priority09_commentary_citations'] else 'CHECKS.json'
        check('full mathematical record correspondence '+family,
              json.loads(payloads['reviews/'+family+'/'+record_name])==summary[family])
    marker=b'\\section{Attribution, scope and verification}'
    current=payloads['support_slit.tex'];baseline=payloads['root_reproduction/PRIMARY_AUDIT_BASELINE.tex']
    check('archived baseline/current proof exact prefix mapping',
          current.count(marker)==baseline.count(marker)==1
          and current.split(marker)[0]==baseline.split(marker)[0],
          {'prefix_bytes':len(current.split(marker)[0]),'baseline_sha256':sha(baseline)})
    wrong_baseline=baseline.replace(b'\\eps=10^{-24}',b'\\eps=10^{-23}',1)
    check('independent mapping rejects mutated baseline proof',
          current.split(marker)[0]!=wrong_baseline.split(marker)[0])
    wrong_current=current.replace(b'\\section{Attribution, scope and verification}',b'\\section{Attribution}',1)
    check('independent mapping rejects incorrect attribution boundary',wrong_current.count(marker)!=1)
    before=archive_inventory(FRESH)
    replay=[]
    for attempt in [1,2]:
        p=run(FRESH)
        check('fresh complete replay '+str(attempt),p.returncode==0, p.stdout[-1100:])
        replay.append({'attempt':attempt,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        check('immutable extraction after replay '+str(attempt),archive_inventory(FRESH)==before)
    dump(HERE/'REPLAY_RECEIPTS.json',replay)
    # Rehashed expected mathematical record mutations deliberately preserve
    # counts: this tests comparison of data, rather than only output length.
    for family in summary:
        root=new_copy('record_'+family)
        target=root/'root_reproduction/supplied_primary_controls.json'
        data=json.loads(target.read_text())
        if family=='priority06_zemyan2003':
            data[family]['interval_controls']['B']['real']='MUTATED_INTERVAL_VALUE'
        else:
            if isinstance(data[family]['checks'][0], str):
                data[family]['checks'][0] += ' MUTATED_MATH_DETAIL'
            else:
                field = 'evidence' if 'evidence' in data[family]['checks'][0] else 'detail'
                data[family]['checks'][0][field]='MUTATED_MATH_DETAIL'
        dump(target,data);retarget_outer(root,['root_reproduction/supplied_primary_controls.json'])
        p=run(root)
        check('preserved-count changed math record rejected '+family,
              p.returncode!=0 and 'Replay mismatch: root_reproduction/check_supplied_primary_controls.py' in p.stderr,
              p.stderr[-400:])
    root=new_copy('incomplete_interval')
    target=root/'root_reproduction/supplied_primary_controls.json'
    data=json.loads(target.read_text());del data['priority06_zemyan2003']['interval_controls']['tip_phase_residual_enclosure']
    dump(target,data);retarget_outer(root,['root_reproduction/supplied_primary_controls.json'])
    p=run(root)
    check('incomplete new interval record rejected',p.returncode!=0 and 'Replay mismatch' in p.stderr,p.stderr[-400:])
    root=new_copy('missing_hidden_seal_payload')
    missing='reviews/priority06_zemyan2003/.gitignore'
    (root/missing).unlink()
    manifest=json.loads((root/'MANIFEST.json').read_text());del manifest['files'][missing];dump(root/'MANIFEST.json',manifest)
    p=run(root)
    check('missing source06 hidden inner-sealed payload rejected after outer removal',
          p.returncode!=0 and 'Nested payload omitted' in p.stderr,p.stderr[-400:])
    root=new_copy('missing_new_seal')
    missing='reviews/priority10_adversary/MANIFEST.json'
    (root/missing).unlink()
    manifest=json.loads((root/'MANIFEST.json').read_text());del manifest['files'][missing];dump(root/'MANIFEST.json',manifest)
    p=run(root)
    check('missing new registry seal rejected',p.returncode!=0 and 'Missing seal:' in p.stderr,p.stderr[-400:])
    for args,env,label in [(['-O'],{},'minus O'),([],{'PYTHONOPTIMIZE':'1'},'optimization environment')]:
        p=run(FRESH,args=args,env=env)
        check('optimization rejected '+label,p.returncode!=0 and 'Run without Python optimization' in p.stderr,p.stderr[-400:])
    nodeps=CACHE/'nodeps_venv'
    if not (nodeps/'bin/python').exists():
        subprocess.run([sys.executable,'-m','venv',str(nodeps)],check=True,capture_output=True,text=True)
    p=run(FRESH,python=nodeps/'bin/python')
    check('missing dependency rejected',p.returncode!=0 and 'mpmath' in p.stderr,p.stderr[-400:])
    site=CACHE/'bad_version';site.mkdir(exist_ok=True)
    (site/'sitecustomize.py').write_text("import mpmath\nmpmath.__version__='0.BAD_CONTROL'\n")
    p=run(FRESH,env={'PYTHONPATH':str(site)})
    check('incorrect dependency version rejected by full recorded output',
          p.returncode!=0 and 'Replay mismatch' in p.stderr,p.stderr[-400:])
    rational_checks()
    check('frozen original extraction still unchanged after controls',archive_inventory(FRESH)==before)
    # Producer writes only to a copied audit subtree. No canonical mutation.
    producer_root=CACHE/'producer_rebuild'
    if producer_root.exists():shutil.rmtree(producer_root)
    (producer_root/'publication').mkdir(parents=True)
    for name in ['original','reviews','root_reproduction']:
        if name=='reviews':
            for family in ['analytic01','quantitative01','source01','priority02','priority03','priority04_hib1996',
                           'priority05_friedland1977','priority06_zemyan2003','priority07_zemyan_bounds',
                           'priority08_radial_extrema','priority09_commentary_citations','priority10_adversary']:
                shutil.copytree(AUDIT/'reviews'/family,producer_root/'reviews'/family,
                                ignore=shutil.ignore_patterns('.cache','__pycache__'))
        else:
            shutil.copytree(AUDIT/name,producer_root/name,ignore=shutil.ignore_patterns('__pycache__'))
    for p in AUDIT.iterdir():
        if p.is_file() and p.suffix in ['.json','.md']:shutil.copy2(p,producer_root/p.name)
    for p in PUB.iterdir():
        if p.is_file():shutil.copy2(p,producer_root/'publication'/p.name)
    p=subprocess.run([str(PYTHON),str(producer_root/'publication/make_package.py')],
                     capture_output=True,text=True)
    check('nonmutating deterministic ZIP producer rebuild',p.returncode==0
          and sha((producer_root/'publication/verification_package.zip').read_bytes())==EXPECTED['verification_package.zip'],
          p.stdout if p.returncode==0 else p.stderr)
    result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'frozen_hashes':EXPECTED,'environment':environment,'check_count':len(CHECKS),
            'checks':CHECKS,'all_passed':True,
            'limits':'Finite controls and byte mapping do not formalize the analytic proof or certify source priority/authenticity.'}
    dump(HERE/'CHECKS.json',result)
    print(json.dumps({'check_count':len(CHECKS),'all_passed':True}))


if __name__=='__main__':
    main()
