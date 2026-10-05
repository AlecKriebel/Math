#!/usr/bin/env python3
"""Read-only full-gzip/semantic validator, independent of live API calls.
Use --run runs/clean_live_20261003_01 or another unique completed run.
No writes, no Git/service changes, and no permission to merge is inferred.
"""
from pathlib import Path
import argparse,datetime,gzip,hashlib,json,subprocess
F=Path(__file__).resolve().parent;OWN=F.parent;A=OWN.parent;R=A.parents[2]
p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args();D=(F/a.run).resolve();assert D.is_relative_to(F.resolve())
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def ck(name,b):
 checks.append({'check':name,'pass':bool(b)})
 if not b:raise AssertionError(name)
j=json.loads((D/'RECEIPT.json').read_bytes());ck('complete primary success',j['status']=='PASS exact live acceptance as unsolved5/5; actual merge pending' and len(j['checks'])==j['check_count']==8268 and all(r['pass'] for r in j['checks']))
ck('executed whole verifier identity',j['program_sha256']==sha((F/'audit_exact_live.py').read_bytes()))
seen=set();by_id={}
def unpack(row):
 safe=(D/row['path']).resolve();ck('owned complete gzip '+row['path'],safe.is_relative_to(D) and not safe.is_symlink());b=safe.read_bytes();ck('full compressed stream identity '+row['path'],len(b)==row['gzip_bytes'] and sha(b)==row['gzip_sha256']);raw=gzip.decompress(b);ck('full uncompressed stream identity '+row['path'],len(raw)==row['bytes'] and sha(raw)==row['sha256']);seen.add(row['path']);return raw
for cap in j['complete_captures']:
 ck('unique command capture ID '+str(cap['id']),cap['id'] not in by_id);by_id[cap['id']]=cap
 ck('successful captured Git/API/program command '+str(cap['id']),cap['exit_code']==0)
 for channel in ['stdout','stderr']:
  row=cap[channel]
  if 'path' in row:unpack(row)
  else:ck('explicit large Git listing nonretention '+str(cap['id']),channel=='stdout' and row['retained'] is False and cap['command'][:5]==['git','ls-tree','-r','-z','--full-tree'])
stdout={}
for row in j['complete_program_replays']:
 ck('full replay actual command capture '+row['label'],row['capture_id'] in by_id and row['command']==by_id[row['capture_id']]['command'] and row['stdout']==by_id[row['capture_id']]['stdout'] and row['stderr']==by_id[row['capture_id']]['stderr'])
 stdout[row['label']]=unpack(row['stdout']);ck('full replay empty stderr '+row['label'],unpack(row['stderr'])==b'')
C=A/'snapshot/problems/30004320_laurent_descent';author={}
for n in range(1,6):
 b=(C/f'TURN_{n}_CHECKS.json').read_bytes();ck('whole author output '+str(n),stdout['author'+str(n)]==b);author[n]=json.loads(b)['exact_assertions']
ck('actual128694 author assertions',sum(author.values())==128694)
ck('historical8664 exact output',stdout['historical_review']==(C/'review/INDEPENDENT_CHECKS.json').read_bytes() and json.loads(stdout['historical_review'])['exact_assertions']==8664)
s=(C/'review/AUTHOR_REPLAY.json').read_bytes();n=json.loads(s);n.update(source_check='not requested; raw sources are not distributed',source_pdfs_checked=0);n=(json.dumps(n,indent=2,sort_keys=True)+'\n').encode();rv=b'PASS: review hashes, frozen author/remote binding, and independent replay\n';end=b'PASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n'
for label,expected in [('packet_with_sources',s),('packet_without_sources',n),('review_wrapper',rv),('publication_with_sources',s+rv+end),('publication_without_sources',n+rv+end)]:ck('entire source/portable contract '+label,stdout[label]==expected)
rootorig=json.loads((A/'root_original_reproduction_receipt.json').read_bytes());rootfam=json.loads((A/'root_family_control_reproduction.json').read_bytes());ck('all root original complete check records',rootorig['status']=='PASS' and len(rootorig['checks'])==rootorig['check_count']==501 and all(r['pass'] for r in rootorig['checks']));ck('all root family complete check records',rootfam['status']=='PASS' and len(rootfam['checks'])==rootfam['check_count']==3310 and all(r['pass'] for r in rootfam['checks']))
for fam in rootfam['families']:
 name=fam['family'];control=stdout['controls_'+name];manifest=stdout['manifest_'+name]
 ck('whole root control stdout '+name,control==(A/'root_family_control_streams'/(name+'.stdout')).read_bytes() and (A/'root_family_control_streams'/(name+'.stderr')).read_bytes()==b'')
 ck('root complete control receipt matches stdout '+name,json.loads(control)==fam['complete_control_output'] and len(control)==fam['control_stdout_bytes'] and sha(control)==fam['control_stdout_sha256'])
 ck('whole root stored manifest stream '+name,manifest==(A/'root_family_control_streams'/(name+'_manifest.stdout')).read_bytes() and (A/'root_family_control_streams'/(name+'_manifest.stderr')).read_bytes()==b'' and json.loads(manifest)==fam['manifest_verifier_output'])
ck('all13339 fresh distinct controls',sum(json.loads(stdout['controls_'+f])['exact_assertions'] for f in ['descent_cohomology_review','residue_valuation_review','clean_final_adversary'])==13339)
rootneg=(A/'root_family_control_streams/drift.stdout').read_bytes();ck('whole root14 stored negative output',json.loads(rootneg)==rootfam['full_negative_output'] and rootneg==(json.dumps(rootfam['full_negative_output'],indent=2)+'\n').encode() and (A/'root_family_control_streams/drift.stderr').read_bytes()==b'')
oldneg=json.loads((OWN/'DRIFT_NEGATIVES.json').read_bytes());newneg=json.loads(stdout['drift14_private']);ck('all14 newly replayed complete negative records',newneg==j['old_drift_negative_controls'] and newneg['negative_controls']==14 and len(newneg['results'])==14 and all(r['rejected'] for r in newneg['results']))
for old,root,new in zip(oldneg['results'],rootfam['full_negative_output']['results'],newneg['results']):
 ck('entire original/root/new negative record shape '+old['control'],old.keys()==root.keys()==new.keys())
 for k in old:
  if k not in ['stderr_bytes','stderr_sha256']:ck('all negative metadata '+old['control']+'/'+k,old[k]==root[k]==new[k])
 if 'exit_code' in old:
  label=old['control'];ob=(OWN/(label+'.stderr')).read_bytes();rb=(A/'tmp/root_drift02'/(label+'.stderr')).read_bytes();nb=gzip.decompress((D/'streams'/('negative_'+label+'_stderr.gz')).read_bytes());seen.add('streams/negative_'+label+'_stderr.gz');sb=gzip.decompress((D/'streams'/('negative_'+label+'_stdout.gz')).read_bytes());seen.add('streams/negative_'+label+'_stdout.gz')
  ck('actual whole root negative traceback '+label,len(rb)==root['stderr_bytes'] and sha(rb)==root['stderr_sha256'] and ob.replace(str(OWN/'private_controls').encode(),b'OWN_PRIVATE')==rb.replace(str(A/'tmp/root_drift02/private_controls').encode(),b'OWN_PRIVATE'))
  ck('actual whole new negative traceback '+label,len(nb)==new['stderr_bytes'] and sha(nb)==new['stderr_sha256'] and ob.replace(str(OWN/'private_controls').encode(),b'OWN_PRIVATE')==nb.replace(str(D/'private/private_controls').encode(),b'OWN_PRIVATE') and sb==b'')
failed=json.loads((A/'ROOT_CONTROL_REPLAY_FAILURES.json').read_bytes());ck('root failed route count',len(failed)==1)
fb=(A/'root_family_control_streams/drift_failed_01.stderr').read_bytes();ck('whole root failed route hash and no success output',sha(fb)==failed[0]['stderr_sha256'] and (A/'root_family_control_streams/drift_failed_01.stdout').read_bytes()==b'' and b'FileNotFoundError' in fb and b'tmp/snapshot/unsolved_math_prioritization/QUEUE.md' in fb and failed[0]['candidate_mathematical_failure'] is False)
for f in (D/'private/candidate').rglob('*'):
 if f.is_file():ck('entire replay candidate still immutable '+f.relative_to(D/'private/candidate').as_posix(),f.read_bytes()==(C/f.relative_to(D/'private/candidate')).read_bytes())
actual={p.relative_to(D).as_posix() for p in (D/'streams').iterdir() if p.is_file()};ck('complete gzip stream closed scope',actual==seen and len(actual)==1626)
for phase in ['before','after']:
 p=j[phase]['pull'];pins=j['pins'];ck('retained whole live metadata pins '+phase,p['state']=='open' and p['draft'] is False and p['head']['sha']==pins['head'] and p['base']['sha']==pins['base'] and sha(p['body'].encode())==pins['accepted_body_sha256'] and j[phase]['actual_commit']['tree']['sha']==pins['tree'])
ck('all6 literal live negatives',len(j['live_metadata_negative_controls'])==6 and all(r['rejected'] for r in j['live_metadata_negative_controls']))
# Original parent manifest/read-only utility remains unchanged despite additive live evidence.
r=subprocess.run([str(R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'),'-B',str(OWN/'verify_manifest.py')],capture_output=True,cwd=F);ck('original47 public/seal verifier still passes',not r.returncode and not r.stderr and json.loads(r.stdout)['status']=='PASS' and json.loads(r.stdout)['public_files_bound']==47)
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'complete_evidence_checks':len(checks),'complete_gzip_streams':len(actual),'command_captures':len(j['complete_captures']),'primary_live_checks':j['check_count'],'checks':checks,'original47_and_all_source_math_final_seals_unchanged':True,'no_new_live_api_call_in_this_validator':True,'actual_merge_pending':True},indent=2))
