#!/usr/bin/env python3
"""Historical audit harness; scratch is confined to this review's tmp/.

To replay this harness, use a disposable review-directory copy and first extract
frozen/source-and-verification.zip to tmp/source. It regenerates review receipts.
The closed review itself should be checked read-only with verify_review.py.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction as F
import datetime, hashlib, json, os, shutil, stat, subprocess, sys, zipfile
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'tmp/source'
TMP=ROOT/'tmp/runtime'; TMP.mkdir(exist_ok=True)
PYTHON=sys.executable

def require(x,message):
    if not x: raise RuntimeError(message)
def ident(raw): return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def run(cmd,env=None):
    e=os.environ.copy(); e.pop('PYTHONOPTIMIZE',None); e['PYTHONDONTWRITEBYTECODE']='1'; e['TMPDIR']=str(TMP)
    if env:e.update(env)
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(cmd,cwd=ROOT,env=e,capture_output=True,text=True,timeout=900)
    return {'started_utc':t,'command':cmd,'environment_overrides':env or {},'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def json_nodup(raw):
    def hook(pairs):
        out={}
        for k,v in pairs:
            require(k not in out,'Duplicate JSON key '+str(k)); out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=hook)
def read_source():
    out={}
    for p in SOURCE.rglob('*'):
        require(not p.is_symlink(),'symlink source')
        if p.is_file():out[p.relative_to(SOURCE).as_posix()]=p.read_bytes()
    return out

def closure_check():
    data=read_source(); m=json_nodup(data['MANIFEST.json']); listed={}
    for row in m['files']:
        name=row['path']; p=PurePosixPath(name)
        require(not p.is_absolute() and '\\' not in name and all(t not in ('','.','..') for t in name.split('/')),'unsafe manifest')
        require(name not in listed,'duplicate manifest'); listed[name]={k:row[k] for k in ('bytes','sha256')}
    require(set(data)==set(listed)|{'MANIFEST.json'},'source closure')
    for n,row in listed.items():require(ident(data[n])==row,'source hash '+n)
    for n,raw in data.items():
        if n.endswith('.json'):json_nodup(raw)
    snap=json_nodup(data['audit/SNAPSHOT.json']); prefix='unsolved_math_prioritization/attempts/30005453/'
    require(len(snap['files'])==63,'candidate size')
    historical=set()
    for row in snap['files']:
        require(row['path'].startswith(prefix),'wrong target'); n='historical_candidate/'+row['path'][len(prefix):]
        require(n not in historical,'candidate duplicate'); historical.add(n)
        require(ident(data[n])=={k:row[k] for k in ('bytes','sha256')},'candidate identity')
    require(historical=={n for n in data if n.startswith('historical_candidate/')},'candidate closure')
    pins={
      'review_deterministic_family':'51f60e1946a252cb1191636469d790cf8bfcf9af6e4f01b8f5a64bb686153a8c',
      'review_stochastic_family':'83d5f8bd9af8ce445b31d3f079ddd262a88895c4d69e4c5fce1ad0321a4528ee',
      'priority_audit':'c28066bda4655ad4688cf1e680e0ec63618e496028d42c7c810fcc22adfdf775',
      'priority_adversary01':'a6426b805a4493d39a28a77e5df7390c8ab4879bfb5fe78b459dc195dbd3e064'}
    for family,pin in pins.items():
        pre='audit/'+family+'/'; raw=data[pre+'MANIFEST.json']; require(ident(raw)['sha256']==pin,'review pin')
        entries=json_nodup(raw)['authored_files']; entries=[{'path':n,**x} for n,x in entries.items()] if isinstance(entries,dict) else entries
        names=[]
        for row in entries:
            n=pre+row['path']; names.append(n); require(ident(data[n])=={k:row[k] for k in ('bytes','sha256')},'review identity')
        require(len(names)==len(set(names)),'review duplicate')
        require(set(names)|{pre+'MANIFEST.json'}=={n for n in data if n.startswith(pre)},'review closure')
    require(ident(data['historical_candidate/PUBLICATION_MANIFEST.json'])['sha256']=='2603a5ef378dbc3e83a3a2862aa5517d63b0a0f0d90dcf7b2ffc4433b7c7b25f','candidate pin')
    return data,{'source_files':len(data),'historical_candidate_files':len(historical),'closed_review_pins':pins,'all_json_duplicate_key_check':'PASS'}

def package_checks():
    frozen=ROOT/'frozen'
    metadata=json_nodup((frozen/'zenodo-metadata.json').read_bytes())['metadata']
    deposit=json_nodup((frozen/'zenodo-deposit.json').read_bytes())
    require(metadata==deposit['metadata'],'standalone metadata')
    require((SOURCE/'paper.tex').read_bytes()==(frozen/'paper.tex').read_bytes(),'archived source')
    require(json_nodup((SOURCE/'zenodo-metadata.json').read_bytes())['metadata']==metadata,'source metadata')
    require(deposit['files']==[{'path':'output/pdf/paper.pdf','name':'paper.pdf'},{'path':'source-and-verification.zip','name':'source-and-verification.zip'}],'deposit paths')
    with zipfile.ZipFile(frozen/'zenodo-upload-kit.zip') as z:
        require(set(z.namelist())=={'paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','README.md'},'outer inventory')
        require(z.read('paper.pdf')==(frozen/'output/pdf/paper.pdf').read_bytes(),'outer pdf')
        require(z.read('source-and-verification.zip')==(frozen/'source-and-verification.zip').read_bytes(),'outer source archive')
        require(json_nodup(z.read('zenodo-metadata.json'))['metadata']==metadata,'outer metadata')
        flat=json_nodup(z.read('zenodo-deposit.json'))
        require(flat['metadata']==metadata and flat['files']==[{'path':'paper.pdf'},{'path':'source-and-verification.zip'}],'flat descriptor')
    for name in ['source-and-verification.zip','zenodo-upload-kit.zip']:
        with zipfile.ZipFile(frozen/name) as z:
            require(z.testzip() is None,'CRC')
            for i in z.infolist():require(stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG) and not i.is_dir() and not i.flag_bits&1,'nonregular or encrypted ZIP')
    return {'result':'PASS','metadata_objects_equal':5,'source_tex_equal':True,'outer_payloads_equal':True,'zip_crc_and_regular_modes':'PASS','title':metadata['title'],'date':metadata['publication_date'],'version':metadata['version'],'license':metadata['license'],'creators':metadata['creators']}

def mutate_rehash(fixture,rel,raw):
    p=fixture/rel; p.write_bytes(raw)
    mf=fixture/'MANIFEST.json'; m=json.loads(mf.read_bytes())
    for row in m['files']:
        if row['path']==rel:row.update(ident(raw));break
    else:raise RuntimeError('no manifest mutation row')
    mf.write_text(json.dumps(m,indent=2)+'\n')

def negatives():
    cases=['changed_paper','extra_file','extra_empty_directory','symlink','metadata_rehashed','historical_manifest_rehashed','review_manifest_rehashed','priority_scope_rehashed']
    rows=[]; fixture=ROOT/'tmp/mutant'
    for label in cases:
        if fixture.exists():shutil.rmtree(fixture)
        shutil.copytree(SOURCE,fixture)
        if label=='changed_paper':
            p=fixture/'paper.tex'; p.write_bytes(p.read_bytes()+b'changed\n')
        elif label=='extra_file':(fixture/'foreign.pdf').write_bytes(b'%PDF-')
        elif label=='extra_empty_directory':(fixture/'unlisted-empty-directory').mkdir()
        elif label=='symlink':
            p=fixture/'README.md';p.unlink();p.symlink_to('paper.tex')
        elif label=='metadata_rehashed':
            m=json.loads((fixture/'zenodo-metadata.json').read_bytes());m['metadata']['title']='UNAUTHORIZED TITLE';mutate_rehash(fixture,'zenodo-metadata.json',(json.dumps(m)+'\n').encode())
        elif label=='historical_manifest_rehashed':
            rel='historical_candidate/PUBLICATION_MANIFEST.json';mutate_rehash(fixture,rel,(fixture/rel).read_bytes()+b'\n')
        elif label=='review_manifest_rehashed':
            rel='audit/review_stochastic_family/MANIFEST.json';mutate_rehash(fixture,rel,(fixture/rel).read_bytes()+b'\n')
        else:
            rel='audit/PRIORITY_GATE.json';m=json.loads((fixture/rel).read_bytes());m['first_sole_new_theorem_claim_allowed']=True;mutate_rehash(fixture,rel,(json.dumps(m)+'\n').encode())
        for optimized in [False,True]:
            cmd=[PYTHON]+(['-O'] if optimized else [])+['-B',str(fixture/'verify_bundle.py'),'--integrity-only']
            receipt=run(cmd); require(receipt['returncode']!=0,'mutant accepted '+label)
            rows.append({'case':label,'optimized':optimized,**receipt})
    shutil.rmtree(fixture)
    return {'negative_cases':len(cases),'rejections':len(rows),'normal_and_optimized':True,'records':rows,'single_fixture_storage':True}

def fresh_finite_controls():
    # Exact arithmetic independently challenges extreme-strip algebra at beta=1,2.
    strips=0; minimum=None
    for beta in [1,2]:
      c=F(1,beta+1)
      for degree in [1,2,4]:
       for tiny in [F(1,10),F(1,10**12),F(1,10**60)]:
        for sign in [1,-1]:
         z=F(1,2); neighbors=[tiny*(j+1) for j in range(degree)];B=max([z]+neighbors);M=F(1,10);K=B+1;eps=M/8
         def omega(e):return beta*(2*K)**(beta-1)*e
         while B*degree*omega(eps)/(M/2)**beta>=M/4:eps/=2
         d=sign*(M-eps/2);b=z+d
         other=[a-min(M,a/2) if sign>0 else a+M for a in neighbors]
         Tz=sum(((z+a)**beta for a in neighbors),F());Tb=sum(((b+a)**beta for a in other),F())
         p=z*Tz;derivative=c*(p/Tb-z-d)
         margin=-c*M/2-derivative if sign>0 else derivative-c*M/2
         require(margin>0,'fresh exact strip failure');minimum=margin if minimum is None else min(minimum,margin);strips+=1
    jumps=0
    for num,den in [(1,2),(1,3),(2,3),(3,4),(19,20)]:
      for root in [1,2,7]:
       power=F(root**num);n=root**den;q=F(1,10**60)+F(7,11);intensity=power*q;jump=1/power
       require(jump*intensity==q and jump*jump*intensity==jump*q and jump*q<=q,'fresh jump failure');require(n>=1,'bad integer fixture');jumps+=3
    return {'result':'PASS','exact_extreme_strip_cases':strips,'exact_drift_bracket_domination_checks':jumps,'minimum_exact_damping_margin':str(minimum),'scope':'Finite rational falsification controls, not an infinite stochastic proof.'}

result={'review_started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Independent whole-package read-only reproduction; no network in portable replay.'}
before,closure=closure_check();result['independent_closure']=closure;result['package_checks']=package_checks()
result['full_replays']=[]
for flags,env in [([],{}),(['-O'],{}),([] ,{'PYTHONOPTIMIZE':'2'})]:
    rec=run([PYTHON,*flags,'-B',str(SOURCE/'verify_bundle.py')],env)
    result['full_replays'].append(rec)
    (ROOT/'REPRODUCTION_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
    require(rec['returncode']==0,'full replay failed')
result['negative_controls']=negatives()
rec=run([PYTHON,'-B',str(SOURCE/'build_package.py'),'--output-dir',str(ROOT/'tmp/rebuild'),'--pdf',str(ROOT/'frozen/output/pdf/paper.pdf')])
require(rec['returncode']==0,'portable rebuild failed'); result['portable_rebuild']=rec
result['six_rebuild_identities']=[]
for row in json.loads((ROOT/'INPUT_BINDING.json').read_bytes())['frozen_publication_files']:
    raw=(ROOT/'tmp/rebuild'/row['path']).read_bytes();ok=ident(raw)=={k:row[k] for k in ('bytes','sha256')};require(ok,'rebuild mismatch '+row['path']);result['six_rebuild_identities'].append({'path':row['path'],**ident(raw),'match':ok})
result['fresh_finite_controls']=fresh_finite_controls()
after,_=closure_check();require(before==after,'closed source changed');result['closed_inputs_unchanged']=True
result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();result['result']='PASS'
(ROOT/'REPRODUCTION_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'result':result['result'],'full_replays':len(result['full_replays']),'negative_rejections':result['negative_controls']['rejections'],'six_rebuilt_pins_match':True,'fresh_finite_controls':result['fresh_finite_controls']},indent=2))
