#!/usr/bin/env python3
"""Adversarial static-integrity controls, not mathematical validation."""
from pathlib import Path
from types import SimpleNamespace
import copy,io,json,runpy,shutil,sys,tempfile,warnings,zipfile
D=Path(__file__).resolve().parent
M=runpy.run_path(str(D/'verify_publication.py'));H=M['H'];need=M['need'];inspect=M['inspect'];PINS=M['PINS'];rejected=[]
def reject(label,fn):
    try:fn()
    except (ValueError,KeyError,zipfile.BadZipFile,UnicodeError,FileNotFoundError):rejected.append(label);return
    raise RuntimeError('Invalid control accepted: '+label)
p=PINS['packs'][0];ab=(D/'archives'/p['archive']['path']).read_bytes();mb=(D/'archives'/p['manifest']['path']).read_bytes();original=inspect(ab,mb,p)
reject('outer ZIP corruption',lambda:inspect(ab+b'x',mb,p));reject('external manifest corruption',lambda:inspect(ab,mb+b' ',p))
def mutant(label,change,rebind=False):
    es=[dict(path=n,data=b,mode=0o100644) for n,b in original.items()];change(es);buf=io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',UserWarning)
        with zipfile.ZipFile(buf,'w') as z:
            for e in es:i=zipfile.ZipInfo(e['path']);i.external_attr=e['mode']<<16;z.writestr(i,e['data'])
    b=buf.getvalue();q=copy.deepcopy(p);q['archive'].update(bytes=len(b),sha256=H(b));mm=json.loads(mb);mm['archive']=q['archive']
    if rebind:q['members']=[dict(path=e['path'],bytes=len(e['data']),sha256=H(e['data'])) for e in es];mm['members']=q['members'];mm['member_count']=len(es)
    bb=json.dumps(mm).encode();q['manifest'].update(bytes=len(bb),sha256=H(bb));reject(label,lambda:inspect(b,bb,q))
mutant('changed member',lambda es:es[0].update(data=es[0]['data']+b'x'))
mutant('missing member',lambda es:es.pop())
mutant('extra member',lambda es:es.append(dict(path='extra.md',data=b'x',mode=0o100644)))
mutant('duplicate member',lambda es:es.append(es[0].copy()),True)
for label,n in [('absolute path','/bad.md'),('parent traversal','../bad.md'),('dot segment','a/./bad.md'),('backslash','a\\bad.md'),('drive colon','C:bad.md'),('raw PDF format','bad.pdf')]:mutant(label,lambda es,n=n:es[0].update(path=n),True)
mutant('symlink ZIP member',lambda es:es[0].update(mode=0o120644),True)
mutant('executable ZIP member',lambda es:es[0].update(mode=0o100755),True)
mutant('invalid UTF-8',lambda es:es[0].update(data=b'\xff'),True)
mutant('invalid JSON',lambda es:es[0].update(path='bad.json',data=b'{'),True)
args=SimpleNamespace(catalog=None,problems=None,reports=None,sources_directory=None,queue_base=None,queue_current=None)
with tempfile.TemporaryDirectory() as td:
    t=Path(td)/'relocated'/'nested';shutil.copytree(D,t);r=M['verify'](t,args);need(r['status']=='PASS','relocation');need(not any(r[k]['performed'] for k in ('corpus_checks','source_checks','queue_checks')),'honest omissions')
    for n in ('author_original/PROOFS.md','independent_audit/author_original/PROOFS.md','exact_acceptance/EXACT_ACCEPTANCE.json','INDEPENDENT_AUDIT_RECEIPT.json','PUBLICATION_MANIFEST.json'):
        f=t/n;b=f.read_bytes();f.write_bytes(b+b'x');reject('changed '+n,lambda:M['verify'](t,args));f.write_bytes(b)
    f=t/'extra.md';f.write_text('extra');reject('extra loose file',lambda:M['verify'](t,args));f.unlink()
    f=t/'author_original/README.md';b=f.read_bytes();f.unlink();reject('missing loose member',lambda:M['verify'](t,args));f.write_bytes(b)
    f=t/'symbolic.md';f.symlink_to(t/'README.md');reject('publication symlink',lambda:M['verify'](t,args));f.unlink()
    f=t/'PUBLICATION_METADATA.json';b=f.read_bytes();o=json.loads(b)
    for key,value in [('queue_status','verified_solved'),('turns','6/5'),('palette_minimum_equality_certified',True),('full_solution',True),('novelty_claimed',True),('mathematical_executable_present',True)]:
        changed=dict(o);changed[key]=value;f.write_text(json.dumps(changed));reject('overbroad publication '+key,lambda:M['verify'](t,args));f.write_bytes(b)
    bad=Path(td)/'bad.json';bad.write_text('{}');meta=json.loads((D/'independent_audit/AUDIT_VERIFICATION_METADATA.json').read_bytes())
    def options(**kw):return SimpleNamespace(**dict(vars(args),**kw))
    reject('incomplete corpus arguments',lambda:M['inputs'](options(catalog=str(bad)),meta))
    reject('corrupt complete corpora',lambda:M['inputs'](options(catalog=str(bad),problems=str(bad),reports=str(bad)),meta))
    reject('missing source PDFs',lambda:M['inputs'](options(sources_directory=td),meta))
    reject('incomplete queue arguments',lambda:M['inputs'](options(queue_base=str(bad)),meta))
    reject('corrupt queue bytes',lambda:M['inputs'](options(queue_base=str(bad),queue_current=str(bad)),meta))
print(json.dumps(dict(status='PASS',optimization_level=sys.flags.optimize,relocated_package_passed=True,omitted_optional_inputs_explicitly_skipped=True,negative_controls_rejected=rejected,negative_control_count=len(rejected),mathematical_validation=False),indent=2))
