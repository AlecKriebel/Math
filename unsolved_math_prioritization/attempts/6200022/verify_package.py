#!/usr/bin/env python3
"""Strict portable immutable-package verifier; explicit checks survive Python -O."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, re, subprocess, sys, zipfile
ROOT=Path(__file__).absolute().parent
ARCHIVES={'author':('KLEINIAN_BOUNDARY_6200022_AUTHOR_SAFE_FREEZE.zip','6200022/',16021,'2ed1cf89f1d8e3ea19184fa5bd14b840a2e12183b0ab4c1f0b690c9eea4f1e62','57bc684bc0e13d003f983210af89dc26b3ba71214f1c3a6e2921339ce1309cc4'),'audit':('KLEINIAN_BOUNDARY_6200022_INDEPENDENT_AUDIT_SAFE.zip','6200022_audit/',16755,'8921a5898f44d36b27fee9fff5d11df195da4ebd11be86d50b5778fbab367c5a','06c0b5c1e3a3b63a37ff73838a851652fea0b0b7c6e179285a12f175af5141a2')}
def need(v,m):
    if not v:raise RuntimeError('PACKAGE FAILURE: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
    return d
def read(p):return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=unique)
def safe(n):
    need(isinstance(n,str) and n and '\\' not in n,'path type');p=PurePosixPath(n)
    need(not p.is_absolute() and '..' not in p.parts and p.as_posix()==n and n!='.','unsafe or noncanonical path')
def inventory(root):
    for p in [root,*root.parents]:need(not p.is_symlink(),'linked package ancestor')
    fs=set();ds=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'linked member');n=p.relative_to(root).as_posix()
        if p.is_file():fs.add(n)
        elif p.is_dir():ds.add(n)
        else:need(False,'nonregular member')
    return fs,ds
def manifest(pin=None):
    fs,ds=inventory(ROOT);raw=(ROOT/'PUBLICATION_MANIFEST.json').read_bytes();need(pin is None or sha(raw)==pin,'external manifest pin');m=read(ROOT/'PUBLICATION_MANIFEST.json')
    need(set(m)=={'problem_id','schema','files'} and type(m['schema']) is int and m['schema']==1 and type(m['problem_id']) is int and m['problem_id']==6200022,'manifest schema')
    need(isinstance(m['files'],list) and m['files'],'manifest entries');expected={};derived=set()
    for row in m['files']:
        need(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'manifest entry shape');n=row['path'];safe(n);need(n!='PUBLICATION_MANIFEST.json' and n not in expected,'duplicate or self inventory')
        need(type(row['bytes']) is int and row['bytes']>=0 and isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'identity shape');expected[n]=row
        derived.update(p.as_posix() for p in PurePosixPath(n).parents if p!=PurePosixPath('.'))
    need(fs==set(expected)|{'PUBLICATION_MANIFEST.json'},'exact file inventory');need(ds==derived,'exact directory inventory')
    for n,row in expected.items():need(ident((ROOT/n).read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'file identity '+n)
    return sha(raw)
def queue_check(a,b):
    before=Path(a).read_bytes();after=Path(b).read_bytes();d=read(ROOT/'QUEUE_DELTA.json');need(ident(before)==d['before'] and ident(after)==d['after'],'queue byte binding')
    ls=before.splitlines(keepends=True);hits=[i for i,l in enumerate(ls) if b'| 6200022 / AMR-061-0022 |' in l];need(len(hits)==1,'queue target');i=hits[0];c=ls[i].split(b'|');need(c[1].strip()==b'809' and c[8]==b' queued ' and c[9]==b' 0/5 ' and c[11]==b'  ','queue cells');c[8]=b' already_solved ';c[9]=b' 1/5 ';c[11]=(' '+d['findings']+' ').encode();ls[i]=b'|'.join(c);need(b''.join(ls)==after,'exact three-cell queue delta');return {'all_other_bytes_preserved':True,'changed_cells':['Status','Turns','Findings']}
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest');p.add_argument('--queue-base');p.add_argument('--queue-updated');a=p.parse_args();need(bool(a.queue_base)==bool(a.queue_updated),'both queue paths required');outer=manifest(a.expected_manifest)
    for d,(n,prefix,size,pin,mpin) in ARCHIVES.items():
        need(ident((ROOT/'archives'/n).read_bytes())=={'bytes':size,'sha256':pin},'archive pin');need(sha((ROOT/d/'MANIFEST.json').read_bytes())==mpin,'inner manifest pin')
        with zipfile.ZipFile(ROOT/'archives'/n) as z:
            ns=z.namelist();need(len(ns)==len(set(ns))==9 and z.testzip() is None,'ZIP inventory or CRC');need(set(ns)=={prefix+x for x in inventory(ROOT/d)[0]},'ZIP exact members')
            for name in ns:safe(name);need(z.read(name)==(ROOT/d/name.removeprefix(prefix)).read_bytes(),'ZIP member binding')
    v=read(ROOT/'VERDICT.json');need(v['problem_id']==6200022 and v['classification']=='already_solved' and v['turns_used']==1 and v['turn_limit']==5 and v['independent_agent_audit']=='accepted','current disposition')
    for k in ['correction_required','universal_core_existence','neighboring_problem_21_resolved','novelty_claimed','human_peer_review','formal_proof_certification']:need(v[k] is False,'scope: '+k)
    need(v['full_universal_existence_question_resolved'] is True and v['credited_prior_resolution']['doi']=='10.4171/GGD/908' and v['credited_prior_resolution']['journal_subscription_pdf_inspected'] is False,'credited scope')
    counts={}
    for d,key,count in [('author','exact_checks',77142),('audit','audit_checks',27534)]:
        r=subprocess.run([sys.executable,'-I']+(['-O'] if sys.flags.optimize else [])+[str(ROOT/d/'verify.py')],capture_output=True,text=True,cwd='/',timeout=180)
        need(r.returncode==0,d+' replay: '+r.stderr);result=json.loads(r.stdout,object_pairs_hook=unique);need(result['status']=='pass' and result[key]==count,d+' replay result');counts[d]=count
    out={'status':'PASS','problem_id':6200022,'classification':'already_solved','turns':'1/5','publication_manifest_sha256':outer,'package_files':len(inventory(ROOT)[0]),'optimized':bool(sys.flags.optimize),'checks':counts,'immutable_author_and_audit':True,'strict_inventory':True,'neighboring_problem_21_resolved':False,'novelty_claimed':False,'formal_proof_certification':False}
    if a.queue_base:out['queue']=queue_check(a.queue_base,a.queue_updated)
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
