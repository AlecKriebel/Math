#!/usr/bin/env python3
"""Static publication integrity checks and mutation controls; never a proof checker."""
from pathlib import Path, PurePosixPath
import copy, hashlib, io, json, stat, sys, zipfile
PINS={
 'archives/CHORDAL_CLIQUE_1917_AUTHOR_SAFE_FREEZE.zip':(16904,'5023ed1178ffada4f6c05ef80484bbf4ec6f0070a4f1554d0acef7147d3ae843'),
 'archives/CHORDAL_CLIQUE_1917_AUTHOR_EXTERNAL_MANIFEST.json':(2850,'175287bb667cc8a78c99cb2e7d5684d6c1eaf70d5c8ee490d5d7727515ab4a13'),
 'archives/CHORDAL_CLIQUE_1917_INDEPENDENT_AUDIT_SAFE.zip':(33671,'7af89a02b80f38d39e8bde063bded7ac7d6613a4003e0ece12c810de9995766f'),
 'archives/CHORDAL_CLIQUE_1917_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(3263,'a24fca9508042b221ed7fd8b8ddf834f7c4699e4f3f9445d2480720428b075b4'),
 'AUTHOR_FREEZE_RECEIPT.json':(640,'572c8366aad5a4bec5224b73b081f5cfd1d0b7f708e56d6c6eb6941a5bd52569'),
 'INDEPENDENT_AUDIT_RECEIPT.json':(1800,'1e9403fb86909ec2c582dd8929a6762f3753bc1eeb5e334c9b009173b4d6165c')}
EXTRA={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','EXECUTABLE_REPLAY_RESULTS.json','verify_publication.py'}
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def encode(j):return json.dumps(j,indent=2).encode()
def validate(files,check_manifest=True):
 for n,(nb,h) in PINS.items():need(n in files and (len(files[n]),sha(files[n]))==(nb,h),'external pin: '+n)
 expected=set(PINS)|EXTRA;member_counts=[]
 for tag,leaf,suffix in [('AUTHOR','original_author','_SAFE_FREEZE.zip'),('INDEPENDENT_AUDIT','independent_audit','_SAFE.zip')]:
  zn='archives/CHORDAL_CLIQUE_1917_'+tag+suffix;mn='archives/CHORDAL_CLIQUE_1917_'+tag+'_EXTERNAL_MANIFEST.json';m=json.loads(files[mn]);need((m['archive_bytes'],m['archive_sha256'])==PINS[zn],'archive manifest identity')
  with zipfile.ZipFile(io.BytesIO(files[zn])) as z:
   names=z.namelist();need(len(names)==len(set(names))==m['member_count'],'unique members/count');need(set(names)=={x['name'] for x in m['members']},'archive exact inventory')
   for x in m['members']:
    n=x['name'];p=PurePosixPath(n);need(len(p.parts)==1 and not p.is_absolute() and '..' not in p.parts and '\\' not in n,'safe archive name');info=z.getinfo(n);mode=info.external_attr>>16;need(stat.S_ISREG(mode) and mode==0o100444,'read-only regular member');b=z.read(n);need((len(b),sha(b))==(x['bytes'],x['sha256']),'member pin');path=leaf+'/'+n;need(files.get(path)==b,'loose member differs: '+path);expected.add(path)
  member_counts.append(m['member_count'])
 need(set(files)==expected,'exact public path allowlist')
 for n in files:
  p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts and '\\' not in n,'safe public path')
  if not n.endswith('.zip'):
   t=files[n].decode('utf-8');need(all(word not in t for word in ['/'+'work'+'space/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','agent_'+'notes/','private_'+'sources/']),'unexpected local/private path')
 meta=json.loads(files['PUBLICATION_METADATA.json']);need(meta['problem_id']==1917 and meta['problem_number']=='EP-81' and meta['rank']==883 and meta['status']=='already_solved','identity/disposition');need(type(meta['fresh_approaches_used'])is int and meta['fresh_approaches_used']==0 and meta['approach_limit']==5,'approach budget');need(meta['credited_author']=='Obinna Okechukwu' and meta['source']=='https://arxiv.org/abs/2609.20871v1' and meta['source_submission_date']=='2026-09-15','prior credit')
 for k in ['new_solution_claimed','correction_patch_needed','stronger_all_order_exact_conjecture_accepted','auxiliary_section_6_accepted','formal_verification_claimed','human_peer_review_claimed','source_downloads_during_publication','corpus_contents_published','mathematical_theorem_certified_by_finite_checks']:need(meta[k] is False,'forbidden claim: '+k)
 need(meta['eventual_exactness_accepted'] is True and meta['historical_freeze_fields_preserved'] is True,'accepted/historical scope')
 q=meta['queue'];need(q['permitted_cells']==['Status','Turns','Findings'] and q['actually_changed_cells']==['Status','Findings'] and q['turns_preserved']=='0/5' and q['unrelated_bytes_preserved'] is True,'queue scope')
 receipt=json.loads(files['INDEPENDENT_AUDIT_RECEIPT.json']);a=files['independent_audit/ACCEPTANCE.md'];need((len(a),sha(a))==(receipt['acceptance_report']['bytes'],receipt['acceptance_report']['sha256']),'exact acceptance binding');need(receipt['main_theorem_mathematically_accepted'] is True and receipt['exact_EP81_target_resolved_by_prior_result'] is True and receipt['correction_patch_needed'] is False,'audit verdict')
 er=json.loads(files['EXECUTABLE_REPLAY_RESULTS.json']);need(er['normal_optimized_equal'] is True and er['negative_controls_passed']==26 and len(er['runs'])==12,'actual executable replay summary');need(er['formal_proof_verification'] is False and er['finite_checks_prove_asymptotic_theorem'] is False,'finite proof limitation');need(er['runs']['author_full_normal']['complete_corpus_replay']=='PASS' and er['runs']['audit_full_normal']['corpus_replay']=='PASS','full corpus replay');need(er['runs']['author_relocated_normal']['complete_corpus_replay']=='NOT_RUN' and er['runs']['audit_relocated_normal']['corpus_replay']=='NOT_RUN','standalone honest omission')
 if check_manifest:
  m=json.loads(files['PUBLICATION_MANIFEST.json']);need(m['schema']=='public-file-manifest-v1','public manifest schema');need(len(m['files'])==len(files)-1 and {x['path'] for x in m['files']}==set(files)-{'PUBLICATION_MANIFEST.json'},'public manifest exact inventory')
  for x in m['files']:need((len(files[x['path']]),sha(files[x['path']]))==(x['bytes'],x['sha256']),'public manifest file pin')
 return {'status':'PASS','public_files_checked':len(files),'archive_members_checked':sum(member_counts),'original_author_members':member_counts[0],'audit_members':member_counts[1],'acceptance_bound':True,'historical_files_unchanged':True,'formal_proof_verification':False,'archive_code_executed_by_this_program':False}
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();paths=[p for p in root.rglob('*') if p.is_file()];need(not any(p.is_symlink() for p in root.rglob('*')),'no symlinks');files={str(p.relative_to(root)):p.read_bytes() for p in paths};result=validate(files);controls=[]
 def reject(label,alter,manifest=True):
  f=dict(files);alter(f)
  try:validate(f,manifest)
  except (ValueError,KeyError,UnicodeDecodeError,zipfile.BadZipFile,json.JSONDecodeError):controls.append(label);return
  raise ValueError('negative control accepted: '+label)
 for name in PINS:
  reject('changed external pin '+name,lambda f,n=name:f.__setitem__(n,f[n]+b'changed'),False)
 for name in ['original_author/MAIN_PROOF_ASSESSMENT.md','independent_audit/ACCEPTANCE.md','independent_audit/FRACTIONAL_AUDIT.md','independent_audit/INTEGRAL_AND_RIGIDITY_AUDIT.md']:
  reject('changed loose prose '+name,lambda f,n=name:f.__setitem__(n,f[n]+b'changed'),False)
 reject('missing member',lambda f:f.pop('original_author/README.md'),False)
 reject('extra path',lambda f:f.__setitem__('extra.txt',b'extra'),False)
 reject('traversal path',lambda f:f.__setitem__('../extra',b'extra'),False)
 for key,value in [('status','verified_solved'),('fresh_approaches_used',1),('credited_author','New author'),('stronger_all_order_exact_conjecture_accepted',True),('formal_verification_claimed',True),('human_peer_review_claimed',True),('correction_patch_needed',True),('new_solution_claimed',True)]:
  def alter(f,k=key,v=value):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=encode(m)
  reject('bad claim '+key,alter,False)
 reject('changed wrapper with stale manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'changed'))
 def manifest_attack(f):m=json.loads(f['PUBLICATION_MANIFEST.json']);m['files'].pop();f['PUBLICATION_MANIFEST.json']=encode(m)
 reject('missing public manifest entry',manifest_attack)
 result['negative_controls_rejected']=controls;result['negative_control_count']=len(controls);print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
