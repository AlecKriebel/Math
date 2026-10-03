#!/usr/bin/env python3
"""Read-only independent full post-merge stream/map/semantic validator.
Checks EVERY saved private/public gzip, then reassembles complete API maps.
Writes nothing; stdout is the complete check receipt.
"""
from pathlib import Path
import argparse,datetime,gzip,hashlib,json,subprocess
F=Path(__file__).resolve().parent;OWN=F.parent;A=OWN.parent;R=A.parents[2]
p=argparse.ArgumentParser();p.add_argument('--run',required=True);arg=p.parse_args();D=(F/arg.run).resolve();assert D.is_relative_to(F.resolve())
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode();checks=[]
def ck(n,v):
 checks.append({'check':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
j=json.loads((D/'RECEIPT.json').read_bytes());ck('whole post receipt success',j['status']=='PASS_ACTUAL_POST_MERGE_UNSOLVED5' and j['check_count']==len(j['checks']) and all(r['pass'] for r in j['checks']));ck('executed full program identity',j['program_sha256']==sha((F/'audit_actual_post_merge.py').read_bytes()))
ref=j['EVERY_saved_gzip_inventory'];ib=(D/ref['path']).read_bytes();ck('complete EVERY gzip inventory receipt binding',len(ib)==ref['bytes'] and sha(ib)==ref['sha256']);inv=json.loads(ib);listed={r['path']:r for r in inv['all_files']};actual={p.relative_to(D).as_posix() for p in D.rglob('*.gz') if p.is_file()};ck('EVERY saved gzip scope',len(listed)==len(inv['all_files'])==inv['saved_gzip_streams']==ref['saved_gzip_streams'] and set(listed)==actual)
streams={}
for path,r in listed.items():
 f=(D/path).resolve();ck('owned gzip '+path,f.is_relative_to(D) and not f.is_symlink());z=f.read_bytes();b=gzip.decompress(z);ck('complete compressed and uncompressed identity '+path,len(z)==r['gzip_bytes'] and sha(z)==r['gzip_sha256'] and len(b)==r['bytes'] and sha(b)==r['sha256']);streams[path]=b;ck('private raw/public program placement '+path,(path.startswith('private/raw_streams/') and not r['public']) or (path.startswith('program_streams/') and r['public']))
ck('private/public inventory counts',sum(not r['public'] for r in listed.values())==inv['private_raw_streams']==ref['private_raw_streams'] and sum(r['public'] for r in listed.values())==inv['public_complete_program_streams']==ref['public_program_streams'])
byid={};referenced=set();api_responses={};api_parses=[];programs={};t0=datetime.datetime.fromisoformat(j['start_utc']);t1=datetime.datetime.fromisoformat(j['end_utc'])
for c in j['all_complete_command_captures']:
 ck('unique captured command '+str(c['id']),c['id'] not in byid);byid[c['id']]=c;ct0=datetime.datetime.fromisoformat(c['start_utc']);ct1=datetime.datetime.fromisoformat(c['end_utc']);ck('actual captured command interval '+str(c['id']),t0<=ct0<=ct1<=t1)
 ck('successful or explicitly unavailable local commit probe '+str(c['id']),c['exit_code']==0 or c['command'][:3]==['git','cat-file','-e'])
 for channel in ['stdout','stderr']:
  r=c[channel]
  if 'path' in r:
   ck('full command inventory reference '+str(c['id'])+'/'+channel,r==listed[r['path']]);referenced.add(r['path'])
  else:ck('huge Git map explicit nonretention '+str(c['id']),channel=='stdout' and r['retained'] is False and c['command'][:5]==['git','ls-tree','-r','-z','--full-tree'])
 if c['command'][:2]==['gh','api']:
  ck('complete API raw stays private '+str(c['id']),not c['stdout']['public'] and c['exit_code']==0);b=streams[c['stdout']['path']];obj=json.loads(b);endpoint=c['command'][-1].removeprefix('repos/AlecKriebel/Math/');api_responses[endpoint]=obj;api_parses.append((endpoint,b,obj))
for row in j['all_complete_program_replays']:
 c=byid[row['capture_id']];ck('whole program capture linkage '+row['label'],row['command']==c['command'] and row['stdout']==c['stdout'] and row['stderr']==c['stderr'] and row['exit_code']==c['exit_code']==0 and streams[row['stderr']['path']]==b'');programs[row['label']]=streams[row['stdout']['path']]
for row in j['all_complete_JSON_parse_identity_records']:
 if row['reference'].startswith('API '):
  endpoint=row['reference'][4:];found=[(b,o) for ep,b,o in api_parses if ep==endpoint and sha(b)==row['sha256']];ck('complete API parse reference '+endpoint,bool(found));b,obj=found[0];leaves=[]
  def walk(v,path):
   if isinstance(v,dict):
    for k,x in sorted(v.items()):walk(x,path+[k])
   elif isinstance(v,list):
    for i,x in enumerate(v):walk(x,path+[i])
   else:leaves.append([path,type(v).__name__,v])
  walk(obj,[]);ck('complete API every-leaf identity '+endpoint,len(b)==row['bytes'] and len(leaves)==row['scalar_leaves'] and sha(canon(leaves))==row['complete_leaf_digest'])
# Complete maps are reconstructed from all retained untruncated API chunks.
maps={}
def api_map(oid):
 if oid in maps:return maps[oid]
 rec=api_responses.get('git/trees/'+oid+'?recursive=1')
 if rec is not None and not rec['truncated']:
  ck('complete recursive actual tree identity '+oid,rec['sha']==oid);out={r['path']:{k:r[k] for k in ['mode','type','sha']} for r in rec['tree'] if r['type']!='tree'}
 else:
  rec=api_responses['git/trees/'+oid];ck('complete nonrecursive actual tree identity '+oid,rec['sha']==oid and rec['truncated'] is False);out={}
  for r in rec['tree']:
   if r['type']=='tree':out.update({r['path']+'/'+p:v for p,v in api_map(r['sha']).items()})
   else:out[r['path']]={k:r[k] for k in ['mode','type','sha']}
 maps[oid]=out;return out
for r in j['all_current_main_versions']:
 m=api_map(r['tree']);ck('entire reconstructed current map '+r['commit'],len(m)==r['full_leaf_entries'] and sha(canon(m))==r['canonical_leaf_map_sha256'])
 if r['actual_current_Git_map_available']:
  g=subprocess.check_output(['git','ls-tree','-r','-z','--full-tree',r['commit']],cwd=R);gm={}
  for line in g.split(b'\0'):
   if line:
    meta,path=line.split(b'\t',1);mode,typ,oid=meta.decode().split();gm[path.decode()]={'mode':mode,'type':typ,'sha':oid}
  ck('entire reconstructed actual Git/API current map '+r['commit'],gm==m)
 ck('current own row accepted only',r['own_row']==j['literal_queue']['accepted_row'])
 for mut in r['four_mutable_root_files']:ck('literal/current full mutable text identity '+mut['path'],sha(mut['literal_checkpoint_complete_text'].encode())==mut['literal_checkpoint_sha256'] and sha(mut['current_complete_text'].encode())==mut['current_sha256'] and mut['changed']==(mut['literal_checkpoint_complete_text']!=mut['current_complete_text']))
C=A/'snapshot/problems/30004320_laurent_descent';allauthor=[]
for i in range(1,6):
 b=(C/f'TURN_{i}_CHECKS.json').read_bytes();ck('whole actual author output '+str(i),programs['author'+str(i)]==b);allauthor.append(json.loads(b)['exact_assertions'])
ck('author128694 exact total',sum(allauthor)==128694);ck('whole historical8664 exact',programs['historical_review']==(C/'review/INDEPENDENT_CHECKS.json').read_bytes() and json.loads(programs['historical_review'])['exact_assertions']==8664)
s=(C/'review/AUTHOR_REPLAY.json').read_bytes();n=json.loads(s);n.update(source_check='not requested; raw sources are not distributed',source_pdfs_checked=0);n=(json.dumps(n,indent=2,sort_keys=True)+'\n').encode();rv=b'PASS: review hashes, frozen author/remote binding, and independent replay\n';end=b'PASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n'
for name,want in [('packet_with_sources',s),('packet_without_sources',n),('review_wrapper',rv),('publication_with_sources',s+rv+end),('publication_without_sources',n+rv+end)]:ck('entire source/portable semantic contract '+name,programs[name]==want)
for r in j['complete_controls']:
 ck('whole distinct control output '+r['family'],json.loads(programs['controls_'+r['family']])==r['complete_output'] and r['complete_output']['status']=='PASS' and r['complete_output']['exact_assertions']==r['exact_assertions']);ck('whole original manifest program '+r['family'],json.loads(programs['manifest_'+r['family']])['status']=='PASS')
ck('all13339 new finite controls',sum(r['exact_assertions'] for r in j['complete_controls'])==13339);ck('whole sealed live manifest program',json.loads(programs['final_live_manifest'])['status']=='PASS' and json.loads(programs['final_live_manifest'])['additive_public_files']==1635)
negative=json.loads(programs['drift14_private']);ck('all14 full negative record semantics',negative==j['full14_drift_negative_output'] and negative['negative_controls']==len(negative['results'])==14 and all(r['rejected'] for r in negative['results']));cap=next(r for r in j['all_complete_program_replays'] if r['label']=='drift14_private');ck('negative UTC inside actual command interval',cap['start_utc']<=negative['utc']<=cap['end_utc'])
for r in negative['results']:
 if 'exit_code' in r:
  label=r['control'];ep='program_streams/negative_'+label+'_stderr.gz';op='program_streams/negative_'+label+'_stdout.gz';referenced|={ep,op};b=streams[ep];ck('entire rejected original verifier traceback '+label,len(b)==r['stderr_bytes'] and sha(b)==r['stderr_sha256'] and streams[op]==b'');old=(OWN/(label+'.stderr')).read_bytes();ck('whole rejection only exact private root differs '+label,old.replace(str(OWN/'private_controls').encode(),b'OWN_PRIVATE')==b.replace(str(D/'private/private_controls').encode(),b'OWN_PRIVATE'))
ck('EVERY inventory stream referenced by command or actual negative',referenced==set(listed));ck('all7 literal actual-merge negatives',len(j['literal_postmerge_negative_controls'])==7 and all(r['rejected'] for r in j['literal_postmerge_negative_controls']))
for r in j['all11_fresh_postmerge_sources']:
 b=(D/'private/sources'/r['name']).read_bytes();ck('fresh postmerge whole PDF '+r['name'],len(b)==r['bytes']==r['actual_bytes'] and sha(b)==r['sha256']==r['actual_sha256']);ck('fresh postmerge UTC chronology '+r['name'],j['start_utc']<=r['download_started_utc']<=r['download_finished_utc']<=j['end_utc'])
ck('all11 unique fresh postmerge PDFs',len(j['all11_fresh_postmerge_sources'])==len({r['name'] for r in j['all11_fresh_postmerge_sources']})==11)
for phase in ['before','after']:
 b=j[phase];m=j['literal_merge'];r=b['actual_PR_semantics'];ck('actual literal merged semantics '+phase,r['state']=='closed' and r['merged'] is True and r['draft'] is False and r['merge_commit_sha']==m['commit'] and r['merged_at']==m['merged_at'] and b['body_sha256']==m['body_sha256'] and sha(b['body_complete_text'].encode())==m['body_sha256'] and b['actual_PR_literal_base']==m['ordered_parents'][0] and b['actual_PR_head']==m['ordered_parents'][1] and b['actual_merge_API_identity']['tree']==m['tree'] and b['actual_merge_API_identity']['ordered_parents']==m['ordered_parents']);ck('all observed main merge ancestry '+phase,all(r['older']==m['commit'] and r['merge_base']==m['commit'] and r['behind_by']==0 for r in b['proved_merge_ancestry']))
print(json.dumps({'status':'PASS_ALL_POST_MERGE_EVIDENCE','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'full_semantic_checks':len(checks),'every_saved_gzip_streams':inv['saved_gzip_streams'],'private_raw_gzip_streams':inv['private_raw_streams'],'public_complete_program_gzip_streams':inv['public_complete_program_streams'],'actual_merged_problem_status':'unsolved5/5','no_new_live_observation_by_this_validator':True,'checks':checks},indent=2))
