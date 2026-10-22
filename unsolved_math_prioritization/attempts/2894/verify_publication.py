#!/usr/bin/env python3
"""Fail-closed publication replay for ID 2894; no theorem certification."""
import argparse,hashlib,io,json,re,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
STEM='FOUR_MANIFOLD_SIMPLE_2894_'
PINS={'archives/FOUR_MANIFOLD_SIMPLE_2894_AUTHOR_EXTERNAL_MANIFEST.json': [1650, '224df160047e5e01f24127fcf2bccee3add613fa1b0dee08235b1664f7983e7a'], 'archives/FOUR_MANIFOLD_SIMPLE_2894_AUTHOR_SAFE_FREEZE.zip': [10990, '2a89bece1a2e10133910bc3fcde5a604e9e41de2ea50620d290be71ad864a9d4'], 'archives/FOUR_MANIFOLD_SIMPLE_2894_CORRECTED_EXTERNAL_MANIFEST.json': [2072, '2aefce4fc9c27e800a14249e8c1ff132f8bff1bc0c65ec1f480fa2a31fe2bd26'], 'archives/FOUR_MANIFOLD_SIMPLE_2894_CORRECTED_SAFE.zip': [11662, '407d0d67f37d548eaa55e1cf85455ad218e123d56a4880791a78c5bd8ca912de'], 'archives/FOUR_MANIFOLD_SIMPLE_2894_INDEPENDENT_AUDIT_BOOTSTRAP.py': [3029, '16cb24da2a29d11334c8ff63551678c97a2873f0e1af4000b09e4746d68d8515'], 'archives/FOUR_MANIFOLD_SIMPLE_2894_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': [4285, '3e3f1b1b18b82726222749ca66c8d49739adfbd8b9f8bd4ac6ec4d61c23b2cfa'], 'archives/FOUR_MANIFOLD_SIMPLE_2894_INDEPENDENT_AUDIT_RECEIPT.json': [2877, 'bbee500f556d8412f68c7fbbe2f2ceb06c795225427b5224e7d30cb8f31d24df'], 'archives/FOUR_MANIFOLD_SIMPLE_2894_INDEPENDENT_AUDIT_SAFE.zip': [53146, '0f80d3891fcb60409ffcd6e43dc262a3c0ef2df2beaa8a2702d8c88a73681f1d']}
TOP={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_MANIFEST.json','verify_publication.py'}
FALSE=['full_problem_solved','new_solution_claimed','independent_full_L_theory_reproduction','independent_GAP_group_identification','finite_tests_are_theorem_certification']
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def enc(o):return (json.dumps(o,sort_keys=True,indent=2)+'\n').encode()
def pairs(rows):
 d={}
 for k,v in rows:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=pairs)
def safe(n):return isinstance(n,str) and n and not n.startswith('/') and '\\' not in n and n==str(PurePosixPath(n)) and all(p not in ('.','..','') for p in n.split('/'))
def pin(b,size,digest):need(len(b)==size and sha(b)==digest,'size/hash mismatch')
def unpack(b,manifest,count):
 rows=manifest['files'];names=[r['path'] for r in rows];need(len(names)==len(set(names))==count and all(safe(n) and '/' not in n for n in names),'unsafe archive manifest')
 zmeta=manifest['zip'];pin(b,zmeta['bytes'],zmeta['sha256'])
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  entries=z.infolist();actual=[e.filename for e in entries];need(len(actual)==len(set(actual))==count and set(actual)==set(names),'archive inventory')
  need(all(not e.is_dir() and stat.S_IFMT(e.external_attr>>16) in (0,stat.S_IFREG) for e in entries),'archive member type');out={e.filename:z.read(e) for e in entries}
 for r in rows:pin(out[r['path']],r['bytes'],r['sha256'])
 return out
def bundles(files):
 out={}
 for label,folder,count,zn in [('AUTHOR','original_author',8,'AUTHOR_SAFE_FREEZE.zip'),('CORRECTED','corrected_author',8,'CORRECTED_SAFE.zip'),('INDEPENDENT_AUDIT','independent_audit',22,'INDEPENDENT_AUDIT_SAFE.zip')]:
  out[folder]=unpack(files['archives/'+STEM+zn],js(files['archives/'+STEM+label+'_EXTERNAL_MANIFEST.json']),count)
 return out
def validate(files,manifest_pin=None):
 need(all(safe(n) for n in files),'unsafe published path')
 for name,(size,digest) in PINS.items():pin(files[name],size,digest)
 packs=bundles(files);expected=TOP|set(PINS)|{folder+'/'+n for folder,pack in packs.items() for n in pack};need(set(files)==expected,'exact public inventory')
 for folder,pack in packs.items():
  for name,b in pack.items():need(files[folder+'/'+name]==b,'expanded frozen member mismatch')
 for label in ['AUTHOR','CORRECTED']:
  for suffix in ['_EXTERNAL_MANIFEST.json','_SAFE_FREEZE.zip' if label=='AUTHOR' else '_SAFE.zip']:
   name=STEM+label+suffix;need(files['archives/'+name]==packs['independent_audit'][name],'nested artifact mismatch')
 old=js(packs['original_author']['status.json']);new=js(packs['corrected_author']['status.json']);audit=js(packs['independent_audit']['audit_status.json']);meta=js(files['PUBLICATION_METADATA.json'])
 need(old['disposition']=='partially_solved','historical author status');need(new['disposition']==new['queue_status']==audit['canonical_status']==meta['canonical_status']=='unsolved','canonical status')
 need(meta['schema']=='four-manifold-publication-v1' and type(meta['problem_id']) is int and meta['problem_id']==2894 and meta['problem_number']=='KP-4.18' and type(meta['rank']) is int and meta['rank']==917,'identity')
 need(type(meta['turns_used']) is int and meta['turns_used']==1 and type(meta['turn_limit']) is int and meta['turn_limit']==5,'turns')
 need(all(meta[k] is False for k in FALSE),'unsupported full/novel/certification claim')
 need(meta['part_a']=='accepted_HU_KNV_theorem_dependent_prior_affirmative_result' and meta['part_b']=='unresolved_in_inspected_primary_literature','split status')
 need(meta['original_freeze_preserved'] is True and meta['historical_publication_false_fields_preserved'] is True,'historical preservation')
 need(meta['manifold_fundamental_group']=='G*G' and meta['HU_status']=='public_preprint_v1_2026-02-04' and meta['KNV_status']=='published_PLMS_131_2025_e70101_v2' and meta['KP_status']=='v2_2026-07-22_part_b_open','dependency scope')
 need(meta['publication_mode']=='draft_PR_only' and meta['no_merge_release_DOI_outreach'] is True,'publication scope')
 q=meta['queue'];need(q['changed_cells']==['Status','Turns','Findings'] and q['unrelated_bytes_preserved'] is True and q['notes_and_chat_links_preserved'] is True,'queue scope')
 need(meta['author_validation_receipt']['bundled'] is False and meta['author_validation_receipt']['sha256']==audit['author_validation_receipt_sha256'],'private receipt exclusion')
 if manifest_pin is not None:
  need(re.fullmatch('[0-9a-f]{64}',manifest_pin) is not None and sha(files['PUBLICATION_MANIFEST.json'])==manifest_pin,'publication manifest pin');m=js(files['PUBLICATION_MANIFEST.json']);rows=m['files'];need(m['schema']=='public-file-manifest-v1' and m['problem_id']==2894,'manifest identity');need(len(rows)==len(files)-1 and len({r['path'] for r in rows})==len(rows) and {r['path'] for r in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'manifest inventory')
  for r in rows:need(set(r)=={'path','bytes','sha256'},'manifest row');pin(files[r['path']],r['bytes'],r['sha256'])
 return {'result':'PASS','public_files':len(files),'original_members':8,'corrected_members':8,'audit_members':22,'canonical_status':'unsolved','turns':'1/5','mathematical_theorems_certified':False}
def check_queue(base,new,meta):
 q=meta['queue'];need(sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'] and git(base)==q['base_git_blob_sha'] and git(new)==q['new_git_blob_sha'],'queue byte pins');a=base.splitlines(keepends=True);b=new.splitlines(keepends=True);need(len(a)==len(b),'queue line count');ix=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(ix)==1 and a[ix[0]].startswith(b'| 917 | 2894 / KP-4.18 |'),'unique target row');x=a[ix[0]].split(b'|');y=b[ix[0]].split(b'|');need(len(x)==len(y)==14 and [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]==[8,9,11],'only Status/Turns/Findings');need(y[8:10]==[b' unsolved ',b' 1/5 '] and y[11]==(' '+q['findings']+' ').encode(),'exact changed cells');return {'result':'PASS','changed_cells':['Status','Turns','Findings'],'all_unrelated_bytes_preserved':True}
def controls(files):
 rejected=[]
 def reject(label,mutate,bound=False):
  f=dict(files);mutate(f)
  try:validate(f,sha(files['PUBLICATION_MANIFEST.json']) if bound else None)
  except Exception:rejected.append(label);return
  raise RuntimeError('negative accepted: '+label)
 for n in PINS:reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 for n in ['original_author/status.json','corrected_author/status.json','independent_audit/audit_status.json','independent_audit/correction.patch']:
  reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 reject('missing member',lambda f:f.pop('corrected_author/README.md'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('traversal',lambda f:f.__setitem__('../x',b'x'))
 for k,v in [('canonical_status','partially_solved'),('canonical_status','verified_solved'),('turns_used',2),('turns_used',True),('turn_limit',True),('part_a','independently_proved'),('part_b','solved'),('manifold_fundamental_group','G'),('HU_status','peer_reviewed'),('publication_mode','merged'),('original_freeze_preserved',False)]+[(k,True) for k in FALSE]:
  def alter(f,k=k,v=v):m=js(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
  reject('claim '+k+'='+str(v),alter)
 reject('stale manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'x'),True);reject('corrupt manifest',lambda f:f.__setitem__('PUBLICATION_MANIFEST.json',b'{}'),True)
 try:need(False,'explicit guard')
 except ValueError:rejected.append('explicit false guard')
 else:raise RuntimeError('guard disabled')
 return {'all_rejected':True,'count':len(rejected),'cases':rejected}
def run(argv,cwd):
 p=subprocess.run(argv,cwd=cwd,capture_output=True,timeout=180);need(p.returncode==0,'subprocess failed: '+p.stderr.decode(errors='replace')[:1000]);return p

def replay(files):
 packs=bundles(files);checks=[]
 with tempfile.TemporaryDirectory(prefix='four manifold publication replay ') as td:
  t=Path(td);other=t/'unrelated';other.mkdir()
  for folder,pack in packs.items():
   (t/folder).mkdir()
   for name,b in pack.items():(t/folder/name).write_bytes(b)
  (t/'archives').mkdir()
  for n in PINS:(t/n).write_bytes(files[n])
  audit=t/'independent_audit'
  for opt in [False,True]:
   py=[sys.executable,'-B']+(['-O'] if opt else [])
   for name,args in [('verify_acceptance.py',[]),('check_hu_parity.py',['--check',str(audit/'HU_PARITY_RESULTS.json')])]:
    p=run(py+[str(audit/name)]+args,other);checks.append({'check':name,'optimized':opt,'exit_code':0,'output_sha256':sha(p.stdout)})
   p=run(py+[str(t/'archives'/(STEM+'INDEPENDENT_AUDIT_BOOTSTRAP.py'))],other);need(js(p.stdout)['result']=='pass','bootstrap result');checks.append({'check':'pinned_bootstrap','optimized':opt,'exit_code':0,'output_sha256':sha(p.stdout)})
   for label,folder,zn in [('original','original_author','AUTHOR_SAFE_FREEZE.zip'),('corrected','corrected_author','CORRECTED_SAFE.zip')]:
    mn='AUTHOR' if label=='original' else 'CORRECTED';out=t/(label+str(opt)+'.json');p=run(py+[str(audit/'replay_integrity.py'),str(t/folder),str(t/'archives'/(STEM+mn+'_EXTERNAL_MANIFEST.json')),str(t/'archives'/(STEM+zn)),label,str(out)],other);r=js(out.read_bytes());need(len(r['positive'])==4 and all(x['exit_code']==0 for x in r['positive']) and len(r['negative'])==12 and len(r['adversarial'])==30 and all(x['rejected'] and x['exit_code']!=0 for x in r['negative']+r['adversarial']),'integrity replay counts');need(r==js(files['independent_audit/'+label.upper()+'_REPLAY_RESULTS.json']),'saved replay mismatch');checks.append({'check':label+'_integrity','optimized':opt,'positive':4,'baseline_rejected':12,'additional_rejected':30,'exact_saved_result_match':True})
  patched=t/'patched';patched.mkdir()
  for name,b in packs['original_author'].items():(patched/name).write_bytes(b)
  p=run(['patch','--batch','--fuzz=0','-p1','-i',str(audit/'correction.patch')],patched);need(b'fuzz' not in p.stdout.lower() and b'offset' not in p.stdout.lower(),'patch used fuzz/offset');need({p.name:p.read_bytes() for p in patched.iterdir()}==packs['corrected_author'],'actual patch output mismatch')
 return {'result':'PASS','fresh_authenticated_extraction':True,'unrelated_working_directory':True,'patch_zero_fuzz_exact_eight_members':True,'checks':checks,'mathematical_theorems_certified':False}
def inputs(files,paths):
 out=[]
 with tempfile.TemporaryDirectory(prefix='four manifold inputs ') as td:
  t=Path(td)
  for name in ['validate_inputs.py','INPUT_SOURCE_CHECKS.json']:(t/name).write_bytes(files['independent_audit/'+name])
  for opt in [False,True]:
   cmd=[sys.executable,'-B']+(['-O'] if opt else [])+[str(t/'validate_inputs.py')]
   for flag,path in zip(['--catalog','--problems','--reports','--pdf-dir'],paths):cmd.extend([flag,str(path.resolve())])
   p=run(cmd,t);r=js(p.stdout);need(r['result']=='pass' and r['raw_content_emitted'] is False and r['mathematical_theorems_certified'] is False,'external inputs result');out.append({'optimized':opt,'exit_code':0,'output':r})
 need(out==js(files['independent_audit/INPUT_REPLAY_RESULTS.json']),'exact saved input replay');return {'result':'PASS','runs':out,'new_source_retrieval_or_inspection':False}
def load_files(root):
 need(root.is_dir() and not root.is_symlink(),'regular root');ps=list(root.rglob('*'));need(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in ps),'regular files/directories only');files={p.relative_to(root).as_posix():p.read_bytes() for p in ps if p.is_file()};dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need({p.relative_to(root).as_posix() for p in ps if p.is_dir()}==dirs,'no extra empty directories');return files

def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('directory',type=Path);a.add_argument('--manifest-sha256',required=True);a.add_argument('--replay',action='store_true');a.add_argument('--base-queue',type=Path);a.add_argument('--queue',type=Path)
 for name in ['catalog','problems','reports','pdf-dir']:a.add_argument('--'+name,type=Path)
 x=a.parse_args();f=load_files(x.directory);r=validate(f,x.manifest_sha256);r['wrapper_controls']=controls(f);need(bool(x.base_queue)==bool(x.queue),'both queue arguments required');r['queue']=check_queue(x.base_queue.read_bytes(),x.queue.read_bytes(),js(f['PUBLICATION_METADATA.json'])) if x.queue else {'result':'NOT_RUN'};r['replay']=replay(f) if x.replay else {'result':'NOT_RUN'};paths=[x.catalog,x.problems,x.reports,x.pdf_dir];need(all(paths) or not any(paths),'all source inputs required');r['inputs']=inputs(f,paths) if all(paths) else {'result':'NOT_RUN'};print(enc(r).decode(),end='')
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
