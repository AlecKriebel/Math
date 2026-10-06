#!/usr/bin/env python3
"""Exact-byte publication replay with explicit fail-closed guards; not a theorem prover.
Authenticate this executable independently before running it against untrusted data.
"""
import argparse,hashlib,io,json,pathlib,re,stat,subprocess,sys,tempfile,zipfile
PINS={'archives/LARGE_SLOPE_CONTACT_SURGERY_2839_AUTHOR_EXTERNAL_MANIFEST.json': [1322, 'be3be60e6fe3d89f6642a36f479160e783a5a0d062e450e47e2a3b8072ec8213'], 'archives/LARGE_SLOPE_CONTACT_SURGERY_2839_AUTHOR_SAFE_FREEZE.zip': [11598, 'c19623ac22f119bf828875af3cb961e04c2d5679ddd7aa8dcdfdd135416e446a'], 'archives/LARGE_SLOPE_CONTACT_SURGERY_2839_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': [2188, '1a048d00904d14f5dd053bd2f0e8fdb7c98961baa1afa53fb83657a936d10002'], 'archives/LARGE_SLOPE_CONTACT_SURGERY_2839_INDEPENDENT_AUDIT_RECEIPT.json': [29602, '6dbbcad6fd8c711f83fae63cdf96cd34da2fee0191fca99d5168d81fe60b140f'], 'archives/LARGE_SLOPE_CONTACT_SURGERY_2839_INDEPENDENT_AUDIT_SAFE.zip': [28932, '9defc09d8f288c2bb0351a192806503b8ad7f148485fae1748fe044535d95edb']}
STEM='LARGE_SLOPE_CONTACT_SURGERY_2839_'
EXTRAS={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_MANIFEST.json','verify_publication.py'}
FALSE_CLAIMS=['full_solution','counterexample','novelty_claim','formal_proof_claim','source_contents_included','dataset_contents_included','new_proof_search_performed','new_source_retrieval_or_visual_inspection_claimed','external_theorem_proofs_certified','correction_required']
def need(x,s):
 if not x:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(b):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 def invalid(v):raise ValueError('nonfinite JSON value')
 return json.loads(b.decode('utf8'),object_pairs_hook=pairs,parse_constant=invalid)
def safe(n):
 need(type(n) is str and bool(n),'path type');p=pathlib.PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts and str(p)==n and '\\' not in n,'safe relative path')
def pin(b,size,digest):
 need(type(size) is int and size>=0 and type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest) is not None,'pin types');need((len(b),sha(b))==(size,digest),'byte/hash mismatch')
def load_files(root):
 need(not root.is_symlink() and root.is_dir(),'root type');paths=list(root.rglob('*'));need(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths),'regular nonsymlink tree');return {p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()}
def archive(raw,ext,count):
 need(type(ext['problem_id']) is int and ext['problem_id']==2839 and ext['schema']==1,'archive identity');pin(raw,ext['archive']['bytes'],ext['archive']['sha256']);rows=ext['members'];need(type(rows) is list and len(rows)==count and len({r['path'] for r in rows})==count,'manifest inventory');out={}
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist();need(len(names)==len(set(names))==count and set(names)=={r['path'] for r in rows},'ZIP inventory');need(z.testzip() is None,'ZIP CRC')
  for row in rows:
   n=row['path'];safe(n);i=z.getinfo(n);need(stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1 and not i.is_dir(),'regular unencrypted ZIP');b=z.read(n);pin(b,row['bytes'],row['sha256']);out[n]=b
 return out
def validate(f,mp):
 for n in f:safe(n)
 need(type(mp) is str and re.fullmatch('[0-9a-f]{64}',mp) is not None and sha(f['PUBLICATION_MANIFEST.json'])==mp,'trusted publication manifest digest')
 m=load(f['PUBLICATION_MANIFEST.json']);need(type(m['problem_id']) is int and m['problem_id']==2839,'publication manifest identity');rows=m['files'];need(type(rows) is list and len(rows)==len(f)-1 and len({r['path'] for r in rows})==len(rows) and {r['path'] for r in rows}==set(f)-{'PUBLICATION_MANIFEST.json'},'publication manifest inventory')
 for r in rows:safe(r['path']);pin(f[r['path']],r['bytes'],r['sha256'])
 for n,(size,digest) in PINS.items():pin(f[n],size,digest)
 expected=set(PINS)|EXTRAS;packs={}
 for tag,suffix,count,leaf in [('AUTHOR','SAFE_FREEZE',6,'author_original'),('INDEPENDENT_AUDIT','SAFE',9,'independent_audit')]:
  ext=load(f['archives/'+STEM+tag+'_EXTERNAL_MANIFEST.json']);pack=archive(f['archives/'+STEM+tag+'_'+suffix+'.zip'],ext,count);packs[tag]=pack
  for n,b in pack.items():need(f[leaf+'/'+n]==b,'extracted archive/member identity');expected.add(leaf+'/'+n)
 need(set(f)==expected,'exact public inventory');audit=packs['INDEPENDENT_AUDIT'];need(audit['AUTHOR_SAFE_FREEZE.zip']==f['archives/'+STEM+'AUTHOR_SAFE_FREEZE.zip'] and audit['AUTHOR_EXTERNAL_MANIFEST.json']==f['archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json'],'nested original equality')
 a=load(audit['ACCEPTANCE.json']);need(a['decision']=='accepted_as_stalled_partial' and type(a['problem_id']) is int and a['problem_id']==2839 and a['problem_number']=='KP-3.41' and a['rank']==913 and a['approaches_used']==a['approach_limit']==5,'exact acceptance')
 for k in ['general_problem_solved','general_problem_refuted','novelty_certified','external_theorem_proofs_certified','correction_patch_required']:need(a[k] is False,'acceptance scope')
 need(a['original_preserved'] is True and len(a['accepted_mathematical_outputs'])==4,'accepted unchanged outputs')
 for key,suffix in [('original_author_archive','AUTHOR_SAFE_FREEZE.zip'),('original_author_external_manifest','AUTHOR_EXTERNAL_MANIFEST.json')]:e=a[key];pin(f['archives/'+STEM+suffix],e['bytes'],e['sha256'])
 receipt=load(f['archives/'+STEM+'INDEPENDENT_AUDIT_RECEIPT.json']);need(receipt['positive_acceptance_runs']==9 and receipt['negative_acceptance_runs']==79 and receipt['all_final_expected_results'] is True and all(r['matches_expected'] is True for r in receipt['results']),'historical audit receipt')
 meta=load(f['PUBLICATION_METADATA.json']);need(type(meta['problem_id']) is int and meta['problem_id']==2839 and meta['problem_number']=='KP-3.41' and meta['rank']==913 and meta['status']=='unsolved' and type(meta['approaches_used']) is int and meta['approaches_used']==meta['approach_limit']==5 and meta['accepted_verdict']==a['decision'],'publication disposition')
 for k in FALSE_CLAIMS:need(meta[k] is False,'publication limit '+k)
 need(meta['original_preserved'] is True and meta['historical_freeze_fields_preserved'] is True,'preserved history');need(meta['mandatory_interpretation']==a['mandatory_interpretation'] and meta['conditional_input']==a['conditional_input'],'mandatory qualifications')
 q=meta['queue'];need(q['actually_changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='5/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 return packs,meta

def check_queue(base,new,meta):
 q=meta['queue'];need(sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'],'queue digest');a=base.splitlines(keepends=True);b=new.splitlines(keepends=True);need(len(a)==len(b),'queue lines');ix=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(ix)==1 and a[ix[0]].startswith(b'| 913 | 2839 / KP-3.41 |'),'one target row');x=a[ix[0]].split(b'|');y=b[ix[0]].split(b'|');need(len(x)==len(y) and [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]==[8,9] and y[8:10]==[b' unsolved ',b' 5/5 '],'only Status and Turns');return {'status':'PASS','changed_cells':['Status','Turns'],'findings_and_unrelated_bytes_preserved':True}

def replay(f,packs,args):
 runs=[]
 with tempfile.TemporaryDirectory(prefix='contact-publication-') as td:
  base=pathlib.Path(td);root=base/'audit';root.mkdir();author=base/'author';author.mkdir();manifest=base/'audit-manifest.json';manifest.write_bytes(f['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'])
  for n,b in packs['INDEPENDENT_AUDIT'].items():(root/n).write_bytes(b)
  for n,b in packs['AUTHOR'].items():(author/n).write_bytes(b)
  for opt in ([],['-O'],['-OO']):
   cmd=[sys.executable,'-B',*opt,str(root/'verify_acceptance.py'),'--root',str(root),'--manifest',str(manifest),'--manifest-sha256',PINS['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'][1],'--author-root',str(author)]
   for attr,flag in [('catalog','--catalog'),('problems','--problems'),('reports','--reports'),('source_dir','--source-dir')]:
    value=getattr(args,attr,None)
    if value is not None:cmd.extend([flag,str(value.resolve())])
   p=subprocess.run(cmd,cwd=base,capture_output=True,timeout=120);need(p.returncode==0 and not p.stderr,'authenticated acceptance replay failed: '+p.stderr.decode());r=load(p.stdout);need(r['ok'] is True,'acceptance result');runs.append(r)
 return runs

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=pathlib.Path,nargs='?',default=pathlib.Path('.'));p.add_argument('--manifest-sha256',required=True)
 for n in ['base-queue','queue','catalog','problems','reports','source-dir']:p.add_argument('--'+n,type=pathlib.Path)
 args=p.parse_args();need(bool(args.base_queue)==bool(args.queue),'paired queue inputs');corpus=[args.catalog,args.problems,args.reports];need(all(corpus) or not any(corpus),'complete corpus argument set');f=load_files(args.directory);packs,meta=validate(f,args.manifest_sha256);queue=check_queue(args.base_queue.read_bytes(),args.queue.read_bytes(),meta) if args.queue else {'status':'NOT_RUN'}
 result={'status':'PASS','problem_id':2839,'optimization':sys.flags.optimize,'public_files_checked':len(f),'archive_member_counts':{k:len(v) for k,v in packs.items()},'exact_acceptance':'accepted_as_stalled_partial','canonical_status':'unsolved','turns':'5/5','queue_check':queue,'acceptance_replay':replay(f,packs,args),'mathematical_proof_checked':False};print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as exc:print(json.dumps({'status':'FAIL','error':str(exc)},sort_keys=True),file=sys.stderr);sys.exit(1)
