"""Review02 independent integrity and adversarial harness controls, own extracted copy only."""
from pathlib import Path
from datetime import datetime,timezone
import sys,hashlib,json,zipfile,stat,subprocess,copy
D=Path(__file__).resolve().parent;R=D.parent.parent;B=R/'preprint'; X=D/'isolated_archive/k605a_outer_focal_pedal_product'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def validate_manifest(base,name):
    m=load(base/name);rows=m['files']
    for r in rows:
        p=base/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
    assert len({r['path'] for r in rows})==len(rows)
    return {'manifest':str((base/name).relative_to(D)) if (base/name).is_relative_to(D) else str(base/name),'rows':len(rows),'sha256':sha(base/name)}
start=datetime.now(timezone.utc).isoformat();result={'utc_start':start}
# Compare every extracted entry to actual current input and check independent ZIP policy.
with zipfile.ZipFile(B/'k605a-source-verification.zip') as z:
    names=z.namelist();assert len(names)==len(set(names))==180
    rows=[]
    for q in z.infolist():
        assert not q.is_dir() and not q.flag_bits&1
        assert not Path(q.filename).is_absolute() and '..' not in Path(q.filename).parts
        assert not stat.S_ISLNK(q.external_attr>>16)
        prefix='k605a_outer_focal_pedal_product/';assert q.filename.startswith(prefix)
        rel=q.filename.removeprefix(prefix);raw=z.read(q)
        assert raw==(B/rel).read_bytes()==(X/rel).read_bytes()
        assert not any(t.startswith('private') or t in {'__pycache__','.git'} for t in Path(rel).parts)
        assert Path(rel).suffix.lower() not in {'.html','.htm','.png','.jpg','.jpeg','.pyc'}
        if Path(rel).suffix.lower()=='.pdf':assert rel=='manuscript.pdf'
        rows.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'CRC32':q.CRC})
    result['zip']={'sha256':sha(B/'k605a-source-verification.zip'),'entries':rows,'testzip':z.testzip()}
result['manifests']=[validate_manifest(X,'SOURCE_MANIFEST.json'),validate_manifest(X/'verification','MANIFEST.json'),validate_manifest(X/'pr_update/5100033','CURRENT_PACKET_MANIFEST.json'),validate_manifest(X/'pr_update/5100033','MANIFEST.json'),validate_manifest(X/'pr_update/5100033','PUBLICATION_MANIFEST.json')]
assert set(r['path'] for r in load(X/'SOURCE_MANIFEST.json')['files'])|{'SOURCE_MANIFEST.json'}=={r['path'] for r in rows}
for base,manifest in [(X/'verification','MANIFEST.json'),(X/'pr_update/5100033','CURRENT_PACKET_MANIFEST.json')]:
    assert {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}==set(r['path'] for r in load(base/manifest)['files'])|{manifest}
intake=load(D.parent/'INTAKE.json');originals=[]
for r in intake['original_source_files']:
    rel=r['native_path'].split('attempts/5100033/')[1]
    paths=[D.parent/'submitted'/r['native_path'],X/'verification/original_submission'/rel,X/'pr_update/5100033/history/original_submission_20261015'/rel]
    raw=paths[0].read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert blob==r['native_blob']
    assert all(p.read_bytes()==raw for p in paths)
    originals.append({'path':rel,'bytes':len(raw),'sha256':r['sha256'],'git_blob_sha1':blob,'three_copy_match':True})
assert len(originals)==20;result['originals']=originals
metadata=load(X/'metadata.json');assert load(B/'deposit.json')['metadata']==metadata==load(B/'metadata.json')
assert metadata['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}]
result['metadata_exact']=True
# Read functions from our extracted package and attack them without executing scientific programs.
sys.path.insert(0,str(X/'verification'))
import run_verification as rv
import integrity as integ
import validate_payloads as vp
mutants=[]
def rejected(label,action):
    try: action()
    except Exception as e:mutants.append({'control':label,'rejected':True,'exception':type(e).__name__,'message':str(e)[:200]})
    else:raise AssertionError('Accepted mutant: '+label)
for label,a,b in [('bool versus integer',True,1),('integer versus float',1,1.0),('nested interpreter-looking science field',{'data':{'python':1}},{'data':{'python':2}}),('list order',[1,2],[2,1]),('added dictionary key',{'a':1},{'a':1,'extra':0}),('tiny residual change',{'residual':'1e-89'},{'residual':'2e-89'})]:
    assert rv.differences(a,b);mutants.append({'control':label,'difference_detected':True})
assert rv.normalize({'python':'old','data':{'python':17}},'source_domain')=={'data':{'python':17}}
rejected('missing explicitly excluded top-level metadata',lambda:rv.normalize({},'source_domain'))
for label,value in [('NaN','NaN'),('positive infinity','Infinity'),('large residual','1e-20')]:rejected(label,lambda value=value:vp.small(value,'1e-57'))
base=integ.BASE;before=integ.verify()
p=base/'requirements.txt';raw=p.read_bytes()
try:
 p.write_bytes(raw+b'\n');rejected('one-byte sealed payload addition',integ.verify)
finally:p.write_bytes(raw)
p=base/'unexpected-review02.txt'
try:
 p.write_text('extra');rejected('extra unmanifested payload',integ.verify)
finally:p.unlink()
p=base/'private';p.mkdir()
try:rejected('forbidden private directory even if empty',integ.verify)
finally:p.rmdir()
p=base/'review02-symlink'
try:
 p.symlink_to(base/'requirements.txt');rejected('symlink payload',integ.verify)
finally:p.unlink()
assert integ.verify()==before
for flags in [['-O'],['-OO']]:
 p=subprocess.run([sys.executable,*flags,'-B',str(base/'run_verification.py'),'--integrity-only'],capture_output=True,text=True)
 assert p.returncode!=0 and 'Refusing -O/-OO' in p.stderr
 mutants.append({'control':' '.join(flags),'rejected':True})
p=subprocess.run([sys.executable,'-B',str(base/'run_verification.py'),'--integrity-only','--receipt',str(base/'unsafe.json')],capture_output=True,text=True)
assert p.returncode!=0 and 'Receipt must be outside sealed package' in p.stderr and not (base/'unsafe.json').exists();mutants.append({'control':'receipt into sealed package','rejected':True})
result['harness_mutants']=mutants;result['harness_integrity_unchanged']=before==integ.verify()
result['archive_checks_independently_invoked']=vp.archive_checks()
helpers=sorted((R/'publication').glob('*.py'));result['read_only_external_helper_versions']=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in helpers]
result['utc_end']=datetime.now(timezone.utc).isoformat();result['all_pass']=True
(D/'INDEPENDENT_PACKAGE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'zip_entries':len(rows),'originals':len(originals),'manifests':[x['rows'] for x in result['manifests']],'harness_mutants':len(mutants),'all_pass':True},indent=2))
