"""Independent finite acceptance controls; no theorem certification or network.
Run: python -I -S [-O] replay_acceptance.py PACKAGE_ROOT [OUTPUT_JSON]
PACKAGE_ROOT contains the original/corrected ZIPs, their manifests and corrected bootstrap.
CORRECTION.patch is read beside this script. All archive inputs are pinned first.
"""
import ast
import hashlib
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile

PINS = {
'BOUNDED_HOUSE_30003245_AUTHOR_SAFE_FREEZE.zip': (13207,'c1e5d102a785d8407b30f1f2aa04789c4047b90ee64b693a4b4197949f891c92'),
'BOUNDED_HOUSE_30003245_AUTHOR_EXTERNAL_MANIFEST.json': (1697,'e531b0589430725a2cfea393071a751ae5d2cafe24322c3632541f125c021f08'),
'BOUNDED_HOUSE_30003245_CORRECTED_SAFE.zip': (13956,'a09a0aea6ad9199401a6afb36e1cad67d8bc4dd70a5ed9b3838f6f8bbd209004'),
'BOUNDED_HOUSE_30003245_CORRECTED_EXTERNAL_MANIFEST.json': (2089,'b7023a117f2275a012e3c09f95ffe967742827b3ada7bff040598376b0bccd78'),
'BOUNDED_HOUSE_30003245_CORRECTED_BOOTSTRAP.py': (2819,'5a073b37774e8c02dc3abdac0953b21b1deb04824f29088049bf70d34687676d')}

def require(ok, label):
    if not ok:
        raise SystemExit('ACCEPTANCE FAILED: '+label)

root=pathlib.Path(sys.argv[1]).resolve()
inputs={}
for name,(size,digest) in PINS.items():
    data=(root/name).read_bytes()
    require(len(data)==size and hashlib.sha256(data).hexdigest()==digest,'input pin '+name)
    inputs[name]=data

def read_archive(zname,mname):
    manifest=json.loads(inputs[mname]); rows=manifest['members']
    expected={r['name']:r for r in rows}
    with zipfile.ZipFile(io.BytesIO(inputs[zname])) as z:
        require(len(z.namelist())==len(set(z.namelist()))==len(rows)==8,'exact member count')
        require(set(z.namelist())==set(expected),'exact member set')
        output={name:z.read(name) for name in z.namelist()}
    for name,data in output.items():
        r=expected[name]
        require(len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],'member pin '+name)
    return output
old=read_archive('BOUNDED_HOUSE_30003245_AUTHOR_SAFE_FREEZE.zip','BOUNDED_HOUSE_30003245_AUTHOR_EXTERNAL_MANIFEST.json')
new=read_archive('BOUNDED_HOUSE_30003245_CORRECTED_SAFE.zip','BOUNDED_HOUSE_30003245_CORRECTED_EXTERNAL_MANIFEST.json')
for label,data in [('original',old['verify_arithmetic.py']),('corrected',new['verify_arithmetic.py'])]:
    tree=ast.parse(data)
    require(not any(isinstance(n,(ast.Import,ast.ImportFrom)) for n in ast.walk(tree)),label+' import-free')
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
            require(n.func.id not in {'open','exec','eval','compile','__import__','input'},label+' prohibited call')
    if label=='corrected':
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'no removable assertions')
rows=[]
expected_result=json.loads(old['ARITHMETIC_RESULT.json'])

def run_case(label,path,optimized,cwd,args=(),expect_pass=True,gate=False,env=None):
    cmd=[sys.executable,'-I','-S']+(['-O'] if optimized else [])+[str(path)]+list(map(str,args))
    r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
    require((r.returncode==0)==expect_pass,label+' exit expectation')
    if expect_pass:
        require(json.loads(r.stdout.strip().splitlines()[-1])==expected_result,label+' exact result')
    else:
        require('"status":"passed"' not in r.stdout,label+' no false success')
        if gate:
            require('PINS VERIFIED' not in r.stdout,label+' reject before execution')
    row={'case':label,'optimized':optimized,'returncode':r.returncode,'expected_pass':expect_pass,'stdout':r.stdout.strip(),'stderr_tail':r.stderr.splitlines()[-1:]}
    rows.append(row)

with tempfile.TemporaryDirectory(prefix='bounded-house-audit-') as td:
    temp=pathlib.Path(td);run=temp/'runner';cwd=temp/'hostile cwd with spaces';run.mkdir();cwd.mkdir()
    poison='raise RuntimeError("HOSTILE IMPORT EXECUTED")\n'
    for name in ['sitecustomize.py','usercustomize.py','hashlib.py','json.py']:
        (cwd/name).write_text(poison)
    env=os.environ.copy();env['PYTHONPATH']=str(cwd);env['PYTHONSTARTUP']=str(cwd/'sitecustomize.py')
    original=run/'original.py';original.write_bytes(old['verify_arithmetic.py'])
    corrected=run/'corrected.py';corrected.write_bytes(new['verify_arithmetic.py'])
    for optimized in [False,True]:
        run_case('original clean',original,optimized,temp)
        run_case('corrected clean',corrected,optimized,temp)
        run_case('corrected relocated hostile environment',corrected,optimized,cwd,env=env)
    mutants=[
      ('false discriminant',b'== 229, "arithmetic check 01"',b'== 230, "arithmetic check 01"'),
      ('false norm',b'det3(matrix) == -229',b'det3(matrix) == -230'),
      ('bad modular factorization',b'(x-29)**2*(x-171)',b'(x-28)**2*(x-171)'),
      ('bad power of two conductor',b'valuation(m,2)+2',b'valuation(m,2)+1'),
      ('truncated residues',b'range(229)',b'range(228)'),
      ('truncated conductors',b'range(1,601)',b'range(1,600)'),
      ('bad necessary count',b'necessary_cases += 1',b'necessary_cases += 2'),
      ('omit all odd conductor factors',b'if prime(p) and m % (p-1) == 0:',b'if False:')]
    for label,a,b in mutants:
        require(new['verify_arithmetic.py'].count(a)==1,'unique mutant preimage '+label)
        path=run/'mutant.py';path.write_bytes(new['verify_arithmetic.py'].replace(a,b))
        for optimized in [False,True]:run_case('corrected mutant: '+label,path,optimized,cwd,expect_pass=False,env=env)
    # Demonstrate the original optimization bug separately; its false success is expected evidence.
    path=run/'original_false.py';path.write_bytes(old['verify_arithmetic.py'].replace(b'assert -4*(-4)**3-27 == 229',b'assert -4*(-4)**3-27 == 230'))
    run_case('original false discriminant normal rejection',path,False,cwd,expect_pass=False)
    run_case('original false discriminant optimized FALSE POSITIVE',path,True,cwd,expect_pass=True)
    archive=run/'input.zip';manifest=run/'external.json';bootstrap=run/'bootstrap.py'
    za=inputs['BOUNDED_HOUSE_30003245_CORRECTED_SAFE.zip'];ma=inputs['BOUNDED_HOUSE_30003245_CORRECTED_EXTERNAL_MANIFEST.json']
    bootstrap.write_bytes(inputs['BOUNDED_HOUSE_30003245_CORRECTED_BOOTSTRAP.py'])
    for optimized in [False,True]:
        archive.write_bytes(za);manifest.write_bytes(ma)
        run_case('bootstrap relocated hostile environment',bootstrap,optimized,cwd,[archive,manifest],env=env)
    for label,zd,md in [('archive same-size corruption',za[:-1]+bytes([za[-1]^1]),ma),('manifest same-size corruption',za,ma[:-1]+b' '),('archive truncation',za[:-1],ma),('manifest truncation',za,ma[:-1]),('swapped original archive',inputs['BOUNDED_HOUSE_30003245_AUTHOR_SAFE_FREEZE.zip'],ma)]:
        archive.write_bytes(zd);manifest.write_bytes(md)
        for optimized in [False,True]:run_case('bootstrap rejection: '+label,bootstrap,optimized,cwd,[archive,manifest],expect_pass=False,gate=True,env=env)
    # Apply the actual patch to the original eight members, then compare every derivative byte.
    patched=temp/'patch target';patched.mkdir()
    for name,data in old.items():(patched/name).write_bytes(data)
    patch=pathlib.Path(__file__).resolve().parent/'CORRECTION.patch'
    result=subprocess.run(['patch','--batch','--forward','-p1','-i',str(patch)],cwd=patched,capture_output=True,text=True,timeout=30)
    require(result.returncode==0,'patch applies')
    require({p.name:p.read_bytes() for p in patched.iterdir()}==new,'patch produces exact derivative')
receipt={'schema':'bounded-house-independent-acceptance-v1','problem_id':30003245,'verdict':'corrected derivative accepted as partial progress; full problem unresolved','counts':{'process_runs':len(rows),'corrected_mutant_failures':len(mutants)*2,'external_pin_rejections':10,'modular_residue_checks_per_valid_run':229,'conductor_samples_per_valid_run':4800,'necessary_conductor_samples_per_valid_run':1030},'pins_checked_before_supplied_execution':True,'patch_exact_reproduction':True,'normal_and_optimized':True,'relocation_and_hostile_python_environment':True,'finite_checks_are_not_universal_proof':True,'runs':rows}
encoded=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(encoded)
else:print(encoded)
