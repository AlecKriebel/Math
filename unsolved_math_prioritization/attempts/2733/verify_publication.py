#!/usr/bin/env python3
"""Fail-closed static publication integrity checks. No archive code execution."""
import argparse,hashlib,io,json,re,stat,sys,zipfile
from pathlib import Path,PurePosixPath
STEM='CONNECTED_SUM_ROPELENGTH_2733_'
PINS={
'archives/'+STEM+'AUTHOR_SAFE_FREEZE.zip':(16395,'f05d1acd29f9366fa08facff81b97e561bcadd60072584dce6037a001e273953'),
'archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json':(3750,'c715974ed45a383eb56086518b506887b340671025d532f3a33cf36f62cdeb44'),
'archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip':(27807,'99aaac45d0f8bd732a53486fd17f01b2b10f1da6933fbdaf4878b7718faef1eb'),
'archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(7222,'b8b893d46e0f7ea2fdc7180d5b4f9d9f3aeb6f134e4ccf70045901e62e21827a')}
EXTRA={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','EXECUTABLE_REPLAY_RESULTS.json','verify_publication.py'}
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def bad(v):raise ValueError('nonfinite JSON')
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=bad)
def enc(x):return (json.dumps(x,indent=2)+'\n').encode()
def entry(e,b):
 need(type(e['bytes']) is int and e['bytes']>0 and isinstance(e['sha256'],str) and re.fullmatch('[a-f0-9]{64}',e['sha256']),'malformed pin');need((len(b),sha(b))==(e['bytes'],e['sha256']),'member hash/size mismatch')
def validate(files,manifest=True):
 for n,p in PINS.items():need(n in files and (len(files[n]),sha(files[n]))==p,'external pin: '+n)
 expected=set(PINS)|EXTRA;counts=[];external={}
 for tag,leaf,suffix,count in [('AUTHOR','original_author','_SAFE_FREEZE.zip',9),('INDEPENDENT_AUDIT','independent_audit','_SAFE.zip',15)]:
  zn='archives/'+STEM+tag+suffix;mn='archives/'+STEM+tag+'_EXTERNAL_MANIFEST.json';m=parse(files[mn]);external[tag]=m;need(m['archive']['name']==Path(zn).name and (m['archive']['bytes'],m['archive']['sha256'])==PINS[zn],'manifest archive binding')
  with zipfile.ZipFile(io.BytesIO(files[zn])) as z:
   infos=z.infolist();names=[i.filename for i in infos];need(len(names)==len(set(names))==len(m['members'])==count,'archive duplicate/count');need(set(names)=={e['name'] for e in m['members']},'archive coverage');data={}
   for e in m['members']:
    n=e['name'];p=PurePosixPath(n);need(len(p.parts)==1 and p.name==n and n not in ('.','..') and not p.is_absolute() and '\\' not in n,'unsafe archive path');info=z.getinfo(n);need(not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'nonregular archive member');b=z.read(n);entry(e,b);need(files.get(leaf+'/'+n)==b,'loose member differs from frozen ZIP');expected.add(leaf+'/'+n);data[n]=b
   im=parse(data['MANIFEST.json']);es=im['members'];need(len(es)==count-1 and {e['name'] for e in es}==set(names)-{'MANIFEST.json'},'internal exact coverage')
   for e in es:entry(e,data[e['name']])
  counts.append(count)
 need(set(files)==expected,'unexpected or missing public file')
 for n,b in files.items():
  p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts and '\\' not in n,'unsafe public path')
  if not n.endswith('.zip'):
   t=b.decode('utf-8');need(all(s not in t for s in ['/'+'workspace/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','agent_'+'notes/','private_'+'sources/']),'private/local path')
   if n.endswith('.json'):parse(b)
 a=parse(files['independent_audit/ACCEPTANCE.json']);em=external['AUTHOR'];need(a['accepted_members']==[dict(e,match=True) for e in em['members']],'accepted nine-member identity');need(a['accepted_archive']==dict(em['archive'],match=True),'accepted archive binding');need((a['accepted_external_manifest']['bytes'],a['accepted_external_manifest']['sha256'])==PINS['archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json'],'accepted manifest binding');need(a['verdict']=='ACCEPT_EXACT_AUTHOR_FREEZE_AS_PARTIAL_FORMULATION_AUDIT' and a['full_resolution'] is False and a['novelty_claim'] is False,'acceptance scope')
 m=parse(files['PUBLICATION_METADATA.json']);need(m['schema']=='partial-formulation-publication-v1' and type(m['problem_id']) is int and m['problem_id']==2733 and m['problem_number']=='KP-1.74' and m['rank']==907,'target identity');need(m['canonical_status']=='unsolved' and m['author_assessment']=='PARTIAL_FORMULATION_AUDIT_STALLED','canonical status');need(type(m['approaches_used']) is int and m['approaches_used']==2 and m['approach_limit']==5,'budget');need(m['literal_part_a_classification']=='formulation_issue_only_identity_summands','literal scope');need(m['intended_nontrivial_part_a']==m['part_b']=='unresolved','unresolved intended target')
 for k in ['full_resolution','novelty_claim','certified_global_splice','correction_required','derivative_created','formal_proof_verification','human_peer_review_claimed','fresh_source_downloads','source_or_corpus_contents_published','nature_fulltext_independently_inspected','pubmed_full_abstract_independently_reproduced','merge_authorized','auto_merge_authorized','release_authorized','doi_authorized','outreach_authorized']:need(m[k] is False,'forbidden claim: '+k)
 need(m['historical_freeze_fields_preserved'] is True and m['publication_type']=='draft_pull_request','preservation/draft');q=m['queue'];need(q['permitted_cells']==q['changed_cells']==['Status','Turns'] and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 for k in ['base_sha256','new_sha256']:need(re.fullmatch('[a-f0-9]{64}',q[k]),'queue digest syntax')
 for k in ['base_git_blob_sha','new_git_blob_sha']:need(re.fullmatch('[a-f0-9]{40}',q[k]),'queue blob syntax')
 s=parse(files['original_author/STATUS.json']);need(s['independent_audit']=='pending' and s['publication_performed'] is False,'historical author fields');need(a['publication_performed'] is False,'historical audit publication field')
 r=parse(files['EXECUTABLE_REPLAY_RESULTS.json']);need(r['schema']=='publication-executable-replay-v1' and r['geometry_proved_by_checks'] is False and r['source_downloads'] is False,'test scope');need(r['full_inputs_supplied'] is True and r['optimized_runner_outputs_byte_identical'] is True and r['full_corpus_pin_and_complete_pair_replay'] is True and r['five_pdf_pins_and_page_counts'] is True,'full input checks');need(len(r['runs'])==3 and [x['mode'] for x in r['runs']]==['normal','-O','-OO'],'runner modes')
 for x in r['runs']:need(x['result']['result']=='PASS' and x['result']['baseline_runs']==6 and x['result']['mutation_cases']==14 and x['result']['mutation_runs']==42 and x['result']['original_pins_unchanged'] is True,'runner result')
 need(r['total_author_mutation_rejections']==126 and len(r['author_baselines'])==len(r['audit_baselines'])==6,'baseline/rejection counts');need(all(x['result']['result']=='PASS' for x in r['author_baselines']+r['audit_baselines']),'relocated results');need(len(r['report_pins'])==4 and {e['name'] for e in r['report_pins']}=={'ARTIFACT_VERIFICATION.json','CORPUS_VERIFICATION.json','PDF_VERIFICATION.json','REPLAY_RESULTS.json'},'report coverage')
 for e in r['report_pins']:need(e['matches_frozen_report'] is True,'frozen replay match');entry(e,files['independent_audit/'+e['name']])
 if manifest:
  pm=parse(files['PUBLICATION_MANIFEST.json']);need(pm['schema']=='public-file-manifest-v1','manifest schema');es=pm['files'];need(len(es)==len(files)-1 and {e['path'] for e in es}==set(files)-{'PUBLICATION_MANIFEST.json'},'publication exact coverage')
  for e in es:entry(e,files[e['path']])
 return {'result':'PASS','public_files':len(files),'author_members':counts[0],'audit_members':counts[1],'acceptance_exactly_bound':True,'frozen_historical_bytes_preserved':True,'archive_code_executed':False,'geometry_proved':False}
def controls(files):
 done=[]
 def reject(label,alter,manifest=False):
  f=dict(files);alter(f)
  try:validate(f,manifest)
  except (ValueError,KeyError,TypeError,UnicodeError,zipfile.BadZipFile):done.append(label);return
  raise ValueError('negative accepted: '+label)
 for n in PINS:reject('external pin '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'bad'))
 for n in ['original_author/PROOF.md','original_author/STATUS.json','independent_audit/ACCEPTANCE.md','independent_audit/MATHEMATICAL_AUDIT.md','independent_audit/SOURCE_REVIEW.md']:reject('altered loose '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'bad'))
 reject('missing file',lambda f:f.pop('original_author/README.md'));reject('extra file',lambda f:f.__setitem__('extra.txt',b'extra'));reject('traversal path',lambda f:f.__setitem__('../extra',b'extra'))
 for k,v in [('canonical_status','already_solved'),('approaches_used',True),('approaches_used',3),('intended_nontrivial_part_a','proved'),('part_b','proved'),('full_resolution',True),('novelty_claim',True),('certified_global_splice',True),('nature_fulltext_independently_inspected',True),('pubmed_full_abstract_independently_reproduced',True),('historical_freeze_fields_preserved',False)]:
  def change(f,k=k,v=v):m=parse(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
  reject('metadata '+k+' '+str(v),change)
 def qchange(f):m=parse(f['PUBLICATION_METADATA.json']);m['queue']['changed_cells'].append('Findings');f['PUBLICATION_METADATA.json']=enc(m)
 reject('queue Findings change',qchange)
 reject('duplicate JSON key',lambda f:f.__setitem__('PUBLICATION_METADATA.json',f['PUBLICATION_METADATA.json'].replace(b'{',b'{"problem_id":2733,',1)))
 reject('nonfinite JSON',lambda f:f.__setitem__('PUBLICATION_METADATA.json',f['PUBLICATION_METADATA.json'].replace(b'"approaches_used": 2',b'"approaches_used": NaN')))
 reject('stale wrapper pin',lambda f:f.__setitem__('README.md',f['README.md']+b'bad'),True)
 def pmchange(f):m=parse(f['PUBLICATION_MANIFEST.json']);m['files'].pop();f['PUBLICATION_MANIFEST.json']=enc(m)
 reject('manifest omission',pmchange,True)
 return done
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');ap.add_argument('--base-queue',type=Path);a=ap.parse_args();root=Path(a.root).absolute();need(root.is_dir() and not root.is_symlink(),'root symlink/non-directory');paths=list(root.rglob('*'));need(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths),'symlink/nonregular path');files={p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()};result=validate(files);result['negative_controls_rejected']=controls(files);result['negative_control_count']=len(result['negative_controls_rejected']);q=parse(files['PUBLICATION_METADATA.json'])['queue'];qp=root.parent.parent/'QUEUE.md';result['queue_check']='NOT_RUN'
 if qp.is_file():
  b=qp.read_bytes();need(sha(b)==q['new_sha256'] and git(b)==q['new_git_blob_sha'],'published queue pin');result['queue_check']='PUBLISHED_PIN_PASS'
  if a.base_queue:
   old=a.base_queue.read_bytes();need(sha(old)==q['base_sha256'] and git(old)==q['base_git_blob_sha'],'base queue pin');ls=old.splitlines(keepends=True);ids=[i for i,l in enumerate(ls) if l.startswith(b'| 907 | 2733 / KP-1.74 |')];need(len(ids)==1,'unique queue target');i=ids[0];c=ls[i].split(b'|');need(c[8].strip()==b'queued' and c[9].strip()==b'0/5','base target state');c[8]=b' unsolved ';c[9]=b' 2/5 ';ls[i]=b'|'.join(c);need(b''.join(ls)==b,'only Status/Turns may change');result['queue_check']='ONLY_TARGET_STATUS_TURNS_PASS'
 elif a.base_queue:raise ValueError('base supplied but published queue unavailable')
 print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
