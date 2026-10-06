#!/usr/bin/env python3
"""Fail-closed static handoff and isolated replay; authenticate this wrapper first."""
import argparse, hashlib, io, json, os, shutil, stat, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PINS={
'DEGENERATE_POLYTOPE_3800003_AUTHOR_SAFE_FREEZE.zip':(12004,'1d82820c9e37d3d8118a8ddc5b2aa55bea0d0744b78b5594b85e23bb80e81f34'),
'DEGENERATE_POLYTOPE_3800003_AUTHOR_EXTERNAL_MANIFEST.json':(3250,'0cdd8ad3ad85c08c3d5905f107d44627f6969a8a0e698feb65b873aa2758b9cb'),
'DEGENERATE_POLYTOPE_3800003_INDEPENDENT_AUDIT_SAFE.zip':(36710,'32b7ebb5fed5ad9964d465b0342af36345b2c01c40f14fa1b2629975f03e0a7e'),
'DEGENERATE_POLYTOPE_3800003_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(3574,'6ae6ccd33afa02a5babfce9642b6073c86dad26de18aaeeda11dff86495bf64e'),
'DEGENERATE_POLYTOPE_3800003_INDEPENDENT_AUDIT_RECEIPT.json':(1451,'2e38cd5e4ba333a3e148238a1308cca1a344fad21260471fb0c4a55d5a36b9d9')}
def need(v,s):
    if not v: raise ValueError(s)
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'duplicate JSON key'); d[k]=v
    return d
def load(b): return json.loads(b,object_pairs_hook=unique)
def safe(n):
    p=Path(n); need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==n and n not in ('','.'),'unsafe member path'); return p
def pin(b,p,s): need((len(b),sha(b))==tuple(p),s+': byte/hash mismatch')
def read(p):
    need(not p.is_symlink() and p.is_file(),'not a regular non-symlink file'); return p.read_bytes()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expect-manifest',required=True)
    for n in ('catalog','problems','reports','sources'): ap.add_argument('--'+n,type=Path)
    ap.add_argument('--integrity-only',action='store_true')
    a=ap.parse_args(); need(not ROOT.is_symlink(),'symlink root')
    mb=read(ROOT/'PUBLICATION_MANIFEST.json'); need(sha(mb)==a.expect_manifest,'external publication manifest mismatch')
    m=load(mb); need(m['schema']=='degenerate-facet-publication-v1' and m['problem_id']==3800003,'publication identity')
    files=m['files']; actual=set()
    for p in ROOT.rglob('*'):
        need(not p.is_symlink(),'publication symlink')
        if p.is_file(): actual.add(p.relative_to(ROOT).as_posix())
    need(actual==set(files)|{'PUBLICATION_MANIFEST.json'},'publication inventory mismatch')
    verified={}
    for n,p in files.items():
        b=read(ROOT/safe(n)); pin(b,(p['bytes'],p['sha256']),'publication member '+n); verified[n]=b
    for n,p in PINS.items(): pin(verified['archives/'+n],p,'frozen '+n)
    packets={}; external={}
    for stem,directory,zn in [('AUTHOR','author_original','DEGENERATE_POLYTOPE_3800003_AUTHOR_SAFE_FREEZE.zip'),('INDEPENDENT_AUDIT','independent_audit','DEGENERATE_POLYTOPE_3800003_INDEPENDENT_AUDIT_SAFE.zip')]:
        en='DEGENERATE_POLYTOPE_3800003_'+stem+'_EXTERNAL_MANIFEST.json'; e=load(verified['archives/'+en]); external[stem]=e
        need(e['archive']['filename']==zn and (e['archive']['bytes'],e['archive']['sha256'])==PINS[zn],'external archive binding')
        members={}
        with zipfile.ZipFile(io.BytesIO(verified['archives/'+zn])) as z:
            infos=z.infolist(); need(len(infos)==len({i.filename for i in infos})==11 and {i.filename for i in infos}==set(e['members']),'ZIP inventory')
            for i in infos:
                n=i.filename; safe(n); need(len(Path(n).parts)==1 and not i.is_dir() and stat.S_ISREG(i.external_attr>>16),'unsafe ZIP member')
                b=z.read(i); p=e['members'][n]; pin(b,(p['bytes'],p['sha256']),'ZIP member '+n)
                need(verified[directory+'/'+n]==b,'archive/loose mismatch'); members[n]=b
        mf=e['manifest']; pin(members[mf['filename']],(mf['bytes'],mf['sha256']),'inner manifest')
        inner=load(members[mf['filename']]); need(set(inner['files'])|{mf['filename']}==set(members),'inner manifest inventory')
        for n,p in inner['files'].items(): need(p==e['members'][n],'inner/external pin mismatch')
        packets[stem]=members
    au=packets['AUTHOR']; ad=packets['INDEPENDENT_AUDIT']
    for n in ('DEGENERATE_POLYTOPE_3800003_AUTHOR_SAFE_FREEZE.zip','DEGENERATE_POLYTOPE_3800003_AUTHOR_EXTERNAL_MANIFEST.json'): need(ad[n]==verified['archives/'+n],'nested author mismatch')
    acc=load(ad['EXACT_ACCEPTANCE.json']); need(acc['author_original_unchanged'] is True and acc['repair_required'] is False and acc['substantive_approaches_used']==2 and acc['approach_limit']==5,'acceptance identity')
    need(acc['full_extremal_problem_solved'] is False and acc['new_mathematical_discovery_claimed'] is False and acc['two_n_subquestion_previously_solved'] is True,'acceptance scope')
    for key,name in [('accepted_proof','PROOF.md'),('accepted_report','REPORT.md'),('accepted_author_member_manifest','MANIFEST.json')]:
        p=acc[key]; pin(au[name],(p['bytes'],p['sha256']),'acceptance '+key)
    result={'result':'PASS','problem_id':3800003,'rank':927,'queue_status':'unsolved','turns':'2/5','frozen_artifacts_verified':5,'author_members_verified':11,'audit_members_verified':11,'original_unchanged':True,'full_problem_solved':False,'formal_proof_certification':False}
    if a.integrity_only:
        result['replay_performed']=False; print(json.dumps(result,sort_keys=True,indent=2)); return
    need(all(getattr(a,n) is not None for n in ('catalog','problems','reports','sources')),'full replay requires all corpus and source inputs')
    meta=load(au['VERIFICATION_METADATA.json']); corpus=[]; sources={}
    for p,q in zip((a.catalog,a.problems,a.reports),meta['complete_corpora']):
        b=read(p); pin(b,(q['bytes'],q['sha256']),'complete corpus '+q['name']); corpus.append(b)
    need(len(meta['complete_corpora'])==len(corpus)==3,'corpus count')
    for q in meta['public_sources']:
        if 'sha256' in q:
            b=read(a.sources/safe(q['filename'])); pin(b,(q['bytes'],q['sha256']),'source '+q['filename']); sources[q['filename']]=b
    need(len(sources)==4,'source count')
    with tempfile.TemporaryDirectory(prefix='facet publication relocation ') as td:
        td=Path(td); audit=td/'renamed audit'; audit.mkdir(); foreign=td/'unrelated poisoned cwd'; foreign.mkdir()
        for n,b in ad.items(): (audit/n).write_bytes(b)
        for n in ('json','hashlib','fractions'): (foreign/(n+'.py')).write_text("raise RuntimeError('poisoned cwd')\n")
        inputs=td/'renamed complete inputs'; inputs.mkdir(); paths=[]
        for i,b in enumerate(corpus): p=inputs/(str(i)+'.json'); p.write_bytes(b); paths.append(p)
        src=inputs/'renamed sources'; src.mkdir()
        for n,b in sources.items(): (src/n).write_bytes(b)
        env=dict(os.environ,PYTHONPATH=str(foreign),PYTHONDONTWRITEBYTECODE='1')
        def run(script,tail,opt):
            return subprocess.run([sys.executable,'-I','-B',*(['-O'] if opt else []),str(script),*map(str,tail)],cwd=foreign,env=env,capture_output=True,text=True,timeout=300)
        checks=[]; anchor=external['INDEPENDENT_AUDIT']['manifest']['sha256']
        def positive(label,root):
            for opt in (False,True):
                r=run(audit/'verify_audit.py',['--root',root,'--manifest-sha256',anchor],opt)
                need(r.returncode==0 and r.stderr=='' and load(r.stdout)=={'result':'PASS','audit_members_verified':11,'external_anchor_verified':True,'scope':'Artifact integrity only; not theorem certification.'},label+' did not pass')
            checks.append({'case':label,'normal_and_optimized':'PASS'})
        def negative(label,script,args,reason):
            for opt in (False,True):
                r=run(script,args,opt); need(r.returncode==1 and r.stdout=='' and r.stderr.rstrip().splitlines()[-1]=='ValueError: '+reason,label+' exact rejection failed')
            checks.append({'case':label,'normal_and_optimized':'REJECTED','reason':reason})
        positive('authentic_audit_inventory',audit)
        for label in ('changed_audit_report','missing_audit_file','extra_audit_file','symlink_audit_file','rebound_audit_manifest'):
            bad=td/label; shutil.copytree(audit,bad)
            if label=='changed_audit_report': (bad/'AUDIT_REPORT.md').write_text('changed'); reason='audit member mismatch: AUDIT_REPORT.md'
            elif label=='missing_audit_file': (bad/'AUDIT_REPORT.md').unlink(); reason='unexpected or missing audit member'
            elif label=='extra_audit_file': (bad/'EXTRA.txt').write_text('extra'); reason='unexpected or missing audit member'
            elif label=='symlink_audit_file': (bad/'AUDIT_REPORT.md').unlink(); (bad/'AUDIT_REPORT.md').symlink_to(audit/'AUDIT_REPORT.md'); reason='symlink forbidden'
            else: (bad/'AUDIT_MANIFEST.json').write_text('{}'); reason='audit manifest differs from external anchor'
            negative(label,audit/'verify_audit.py',['--root',bad,'--manifest-sha256',anchor],reason)
        args=['--author-zip',audit/'DEGENERATE_POLYTOPE_3800003_AUTHOR_SAFE_FREEZE.zip','--author-external',audit/'DEGENERATE_POLYTOPE_3800003_AUTHOR_EXTERNAL_MANIFEST.json','--catalog',paths[0],'--problems',paths[1],'--reports',paths[2],'--sources',src]
        for label,index,reason in [('changed_outer_author_zip',1,'author ZIP: byte/hash mismatch'),('changed_outer_author_external',3,'author external manifest: byte/hash mismatch')]:
            bad=td/(label+'.bin'); bad.write_bytes(Path(args[index]).read_bytes()+b'\n'); tail=args[:]; tail[index]=bad
            negative(label,audit/'replay_audit.py',tail,reason)
        relocated=td/'another relocated frozen audit'; shutil.copytree(audit,relocated); positive('relocated_frozen_audit_inventory',relocated)
        need(checks==external['INDEPENDENT_AUDIT']['freeze_checks'],'freeze checks differ')
        outputs=[]
        for opt in (False,True):
            r=run(audit/'replay_audit.py',args,opt); need(r.returncode==0 and r.stderr=='','audit replay process failed')
            need(r.stdout.encode()==ad['AUDIT_REPLAY_RESULTS.json'],'audit replay bytes differ'); outputs.append(r.stdout)
        need(outputs[0]==outputs[1],'audit replay mode difference')
        replay=load(outputs[0]); need(replay['acceptance_cases']==4 and replay['rejection_cases']==22,'audit case counts')
        need(not list(audit.rglob('__pycache__')),'unexpected bytecode')
        result.update(replay_performed=True,complete_corpora_verified=meta['complete_corpora'],source_files_verified=[{'filename':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(sources.items())],freeze_case_families=checks,audit_positive_case_families=4,audit_negative_case_families=22,audit_replay_bytes=len(ad['AUDIT_REPLAY_RESULTS.json']),audit_replay_sha256=sha(ad['AUDIT_REPLAY_RESULTS.json']),audit_driver_normal_optimized_outputs_identical=True,relocated_all_inputs=True,isolated_python=True,poisoned_unrelated_cwd=True)
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    try: main()
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
