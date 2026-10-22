#!/usr/bin/env python3
"""Bounded, journaled priority correction; no native operation is retried."""
from pathlib import Path
import argparse,base64,datetime,hashlib,json,os,subprocess
C=Path(__file__).resolve().parents[1];H='e3f8838a8eac68bbd186fc0234ac2e2a49194626';BR='wip/signed-adjacency-30003813';REPO='AlecKriebel/Math';PREFIX='signed_adjacency_polytopes_30003813';QUEUE='unsolved_math_prioritization/QUEUE.md'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(k,b):return hashlib.sha1((k+' '+str(len(b))+'\0').encode()+b).hexdigest()
def dump(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
def node(es):
 items=sorted(es.values(),key=lambda e:e['path'].encode()+(b'/' if e['type']=='tree' else b''))
 return git('tree',b''.join((('40000' if e['type']=='tree' else e['mode'])+' ').encode()+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in items))
def main():
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','apply']);p.add_argument('--plan-sha256',required=True);p.add_argument('--candidate-sha256');a=p.parse_args();private=C/'private_sources'/('status_repair_native_'+a.phase+'_20261013');private.mkdir(exist_ok=False);counter=0;writes=[]
 def api(method,route,body=None):
  nonlocal counter
  label=f'{counter:04}';counter+=1;dump(private/(label+'_intent.json'),{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':method,'route':route,'payload':body,'no_retry':True})
  if method!='GET':writes.append({'method':method,'route':route})
  cmd=['gh','api','--method',method,'-H','Cache-Control: no-cache','repos/'+REPO+'/'+route]
  if body is not None:cmd+=['--input','-']
  r=subprocess.run(cmd,input=None if body is None else json.dumps(body),capture_output=True,text=True,timeout=55);dump(private/(label+'_native.json'),{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});need(r.returncode==0,'Native response unconfirmed; STOP and GET-only reconciliation, no replay');d=json.loads(r.stdout);dump(private/(label+'_response.json'),d);return d
 def gate():
  m=api('GET','pulls/407');need(m['head']['sha']==H and m['head']['ref']==BR and m['head']['repo']['full_name']==REPO and m['state']=='open' and m['draft'] is True and m['merged'] is False,'Current PR no longer matches original claimed draft; skip')
  ref=api('GET','git/ref/heads/'+BR);need(ref['object']['sha']==H,'Native branch drift; skip');d=api('GET','contents/'+QUEUE+'?ref='+H);q=base64.b64decode(d['content']);need(git('blob',q)==d['sha'],'QUEUE identity');rows=[l for l in q.decode().splitlines() if l.startswith('|') and '30003813 /' in l];need(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='1/5','Nonclaimed status; immediate skip before local scientific input');return m,q
 try:
  meta,queue=gate();raw=(C/'status_repair_preparation/PLAN.json').read_bytes();need(sha(raw)==a.plan_sha256,'Prepared plan drift');plan=json.loads(raw);need(plan['expected_head']==H and sha(queue)==plan['expected_queue_sha256'],'Source gate differs');old=json.loads((C/'pr_metadata.json').read_bytes());need(meta['body']==old['body'] and meta['title']==old['title'],'Original PR metadata changed; no overwrite')
  if a.phase=='prepare':
   allowed={PREFIX+'/'+n for n in ['PROOF.md','README.md','SOURCE_GATE.md','RESEARCH_LOG.md','RELEASE_CHANGES.md','MANIFEST.sha256','status.json','PRIORITY_CORRECTION.md']}|{QUEUE};need(set(plan['changed_repository_files'])==allowed,'Positive repair footprint differs');data={}
   for rel,e in plan['changed_repository_files'].items():
    path=C/e['local'];need(path.is_file() and not path.is_symlink() and path.absolute().is_relative_to(C),'Nonregular/outside positive input');b=path.read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'] and git('blob',b)==e['git_blob_sha'],'Prepared bytes changed');data[rel]=b
   need(data[QUEUE]==queue.replace(plan['selected_old_row'].encode(),plan['selected_new_row'].encode(),1) and queue.count(plan['selected_old_row'].encode())==1,'QUEUE edit exceeds exact selected status cell')
   cache={}
   for f in (C/'private_sources/source_native_20261013').glob('*_NATIVE.json'):
    d=json.loads(f.read_bytes())
    if d['route'].startswith('git/trees/'):
     t=json.loads(d['stdout']);es={e['path']:e for e in t['tree']};need(t['truncated'] is False and node(es)==t['sha'],'Original tree identity');cache[t['sha']]=es
   base=api('GET','git/commits/'+H);need(base['tree']['sha']==plan['expected_source_root_tree'],'Original root differs');root={k:dict(v) for k,v in cache[base['tree']['sha']].items()};changed_nodes={}
   for dirname in [PREFIX,'unsolved_math_prioritization']:
    es={k:dict(v) for k,v in cache[root[dirname]['sha']].items()}
    for rel,e in plan['changed_repository_files'].items():
     if rel.startswith(dirname+'/'):
      name=rel[len(dirname)+1:];need('/' not in name,'Unexpected nested repair');es[name]={'path':name,'mode':'100644','type':'blob','sha':e['git_blob_sha']}
    ns=node(es);root[dirname]['sha']=ns;changed_nodes[dirname]=ns
   expected_tree=node(root)
   for rel,b in data.items():
    e=plan['changed_repository_files'][rel];d=api('POST','git/blobs',{'content':base64.b64encode(b).decode(),'encoding':'base64'});need(d['sha']==e['git_blob_sha'],'Blob ACK differs');d=api('GET','git/blobs/'+d['sha']);need(base64.b64decode(d['content'])==b,'Native blob bytes differ')
   tree=api('POST','git/trees',{'base_tree':base['tree']['sha'],'tree':[{'path':rel,'mode':'100644','type':'blob','sha':e['git_blob_sha']} for rel,e in plan['changed_repository_files'].items()]});need(tree['sha']==expected_tree,'Whole repository tree exceeds expected two-subtree edit');back=api('GET','git/trees/'+expected_tree);need(node({e['path']:e for e in back['tree']})==expected_tree,'Native prepared tree identity')
   date=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ');person={'name':'Alec Kriebel','email':'me@aleckriebel.com','date':date};message='Priority correction: 30003813 already covered by prior alcoved coefficient theorem'
   commit=api('POST','git/commits',{'message':message,'tree':expected_tree,'parents':[H],'author':person,'committer':person});native=api('GET','git/commits/'+commit['sha']);need(native['tree']['sha']==expected_tree and [x['sha'] for x in native['parents']]==[H] and native['message'].rstrip('\n')==message,'Prepared commit scope/parent/message differs')
   candidate={'format':'pr407-priority-status-repair-candidate-v1','commit_sha':commit['sha'],'parent_head':H,'tree':expected_tree,'plan_sha256':a.plan_sha256,'exact_changed_paths':sorted(data),'expected_new_queue_sha256':sha(data[QUEUE]),'prepared_at_utc':date,'branch_ref_or_metadata_writes':0,'scope':'Unreachable verified Git-data candidate; exact current claimed-solved gate still required before one title/body and one nonforce branch update'};dump(C/'STATUS_REPAIR_CANDIDATE.json',candidate);result={'result':'VERIFIED_REPAIR_CANDIDATE_PREPARED','candidate_sha256':sha((C/'STATUS_REPAIR_CANDIDATE.json').read_bytes()),'candidate':candidate,'native_writes':writes}
  else:
   need(a.candidate_sha256,'Exact prepared candidate pin required');b=(C/'STATUS_REPAIR_CANDIDATE.json').read_bytes();need(sha(b)==a.candidate_sha256,'Candidate changed');candidate=json.loads(b);need(candidate['parent_head']==H and candidate['plan_sha256']==a.plan_sha256,'Candidate plan/head mismatch');native=api('GET','git/commits/'+candidate['commit_sha']);need(native['tree']['sha']==candidate['tree'] and [x['sha'] for x in native['parents']]==[H],'Actual candidate drift');b=(C/'status_repair_preparation/PR_METADATA_UPDATE.json').read_bytes();need(sha(b)==plan['metadata_update_sha256'],'Reviewed metadata drift');update=json.loads(b)
   meta,queue=gate();need(meta['body']==old['body'] and meta['title']==old['title'],'Metadata drift immediately before PATCH');d=api('PATCH','pulls/407',update);need(d['body']==update['body'] and d['title']==update['title'] and d['head']['sha']==H and d['draft'] is True,'Metadata ACK unconfirmed; no next mutation')
   gate();d=api('PATCH','git/refs/heads/'+BR,{'sha':candidate['commit_sha'],'force':False});need(d['object']['sha']==candidate['commit_sha'],'Priority ref ACK unconfirmed; GET-only reconciliation required')
   # Status is now already_solved. Administrative acknowledgement only; no science opens.
   d=api('GET','git/ref/heads/'+BR);need(d['object']['sha']==candidate['commit_sha'],'Ref readback lag/drift; no replay');d=api('GET','contents/'+QUEUE+'?ref='+candidate['commit_sha']);q=base64.b64decode(d['content']);need(sha(q)==candidate['expected_new_queue_sha256'] and plan['selected_new_row'].encode() in q,'Exact changed-status acknowledgement differs')
   result={'result':'STATUS_REPAIR_CONFIRMED_IMMEDIATE_EXCLUSION','pr':407,'source_head':H,'new_head':candidate['commit_sha'],'status':'already_solved','turns':'1/5','priority_basis':'Verified prior general full-family theorem coverage; classification inference, no named historical closure','metadata_patch_count':1,'branch_ref_patch_count':1,'force':False,'merge_close_comment_Zenodo_GWS_actions':0,'native_writes':writes,'case_completion_estimate_percent':100,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};dump(C/'STATUS_REPAIR_RECEIPT.json',result)
  dump(private/'RESULT.json',result);print(json.dumps({k:result[k] for k in ['result','candidate_sha256','new_head'] if k in result}))
 except Exception as e:
  dump(private/'STOP.json',{'result':'STOP_NO_REPLAY','error':str(e),'native_writes':writes,'resume_mutation_permitted':False});raise
if __name__=='__main__':main()
