#!/usr/bin/env python3
"""Prepare PR263 only; private objects/index; no provider calls or ref writes."""
import argparse,base64,datetime as dt,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path,PurePosixPath
R=Path('/Users/alec/Documents/Math')
W=R/'draft_pr_descending_audit_20261002/audits/pr263_30000170/initial_review_20261011'
ROOT=W/'integration_preparation'
B=R/'draft_pr_descending_audit_20261002/audits/pr278_30005468/resume_20261011'
H=B/'checkpoint_resume/prepare_checkpoint.py'
AUTHOR='c4eff3253932a504f8e558c8b5f5b1b5e155de0f'
TARGET='attempts/30000170'
QUEUE='unsolved_math_prioritization/QUEUE.md'
BRANCH='refs/heads/dot/math-30000170'
REPO='R_kgDOTfIvPw'
def need(x,s):
 if not x: raise ValueError(s)
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def row(body):
 lines=body.splitlines(keepends=True)
 indexes=[i for i,l in enumerate(lines) if len(l.split(b'|'))>3 and l.split(b'|')[2].strip()==b'30000170 / OWR-783-002']
 need(len(indexes)==1,'Exact QUEUE row census differs')
 i=indexes[0];return lines,i,lines[i]
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--main',required=True);p.add_argument('--selection',required=True);p.add_argument('--date',required=True);p.add_argument('--output',required=True)
 a=p.parse_args();need(re.fullmatch('[0-9a-f]{40}',a.main),'Literal MAIN required')
 t=dt.datetime.strptime(a.date,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc);need(t<=dt.datetime.now(dt.timezone.utc),'Future date rejected')
 out=Path(a.output).resolve();need(out.parent==ROOT and not out.exists(),'New owned output required');out.mkdir()
 need(pin(H)['sha256']=='e5399e719a2a93a0e7d34670ff503a897a18cb2c8632a766248d21d50b3dd298','Checked helper changed')
 sys.dont_write_bytecode=True
 spec=importlib.util.spec_from_file_location('checked_private_reader',H);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.DRIVER=ROOT/'driver.git';m.OBJECTS=ROOT/'private_objects'
 m.ALTERNATES=[B/'checkpoint_resume/private_objects',B/'reconciliation/private_objects',B/'objects.git/objects']
 control=Path(a.selection).resolve();need(control.parent==ROOT,'Root selection control outside owned folder')
 s=m.load_json_no_duplicates(control);need(s['main']==a.main and s['author']==AUTHOR,'Selection literal bindings differ')
 accepted=Path(s['candidate_acceptance']['path']);need(pin(accepted)==s['candidate_acceptance'],'Candidate acceptance drift')
 acceptance=m.load_json_no_duplicates(accepted);need(acceptance['schema']=='pr263-root-final-publication-candidate-acceptance-v1' and acceptance['accepted_for_native_preparation'] is True,'Candidate not accepted')
 candidate=Path(acceptance['candidate_root']);need(candidate==W/'publication_candidate/attempts/30000170' and candidate.resolve()==candidate,'Unowned candidate root')
 need(pin(candidate/'CANDIDATE_MANIFEST.json')==acceptance['candidate_manifest'],'Candidate manifest drift')
 selection=s['files'];need(len(selection)>1 and len({e['path'] for e in selection})==len(selection),'Selection census/uniqueness')
 selected={}; binary=[]
 for e in selection:
  path=e['path'];parts=PurePosixPath(path).parts
  need(PurePosixPath(path).as_posix()==path and not path.startswith('/') and all(x not in ('.','..','') for x in parts) and not any(x in path for x in ('\\','\n','\r','\0')),'Noncanonical path')
  need(path==QUEUE or path.startswith(TARGET+'/'),'Unowned destination')
  f=Path(e['source']);need(f.is_absolute() and f.resolve()==f and f.is_file() and not f.is_symlink() and f.is_relative_to(W),'Nonregular/foreign source')
  if path!=QUEUE:need(f==candidate/path[len(TARGET)+1:],'Source/destination candidate path differs')
  body=f.read_bytes();need(len(body)==e['bytes'] and hashlib.sha256(body).hexdigest()==e['sha256'],'Full source drift: '+path)
  oid=m.git_oid('blob',body);rec={'body':body,'git_blob':oid,'source':e}
  if path.endswith(('.pdf','.zip')):
   expected={'preprint/output/pdf/nonunique_nearest_stable_complex_quadratics.pdf':('6439bda84f32d9a5ac1680e184975df159f51f8c7e44e609fa873dfa8ae78e1f',76336),'preprint/output/nonunique_nearest_stable_complex_quadratics_verification.zip':('2fc6b62d67ab6681c36f7d3806db549073a3f0b2e0d039817f997fab9eb96dee',37068)}
   rel=path[len(TARGET)+1:];need(rel in expected and (e['sha256'],len(body))==expected[rel],'Unknown binary body')
   binary.append({'path':path,'expected_sha':oid,'payload':{'content':base64.b64encode(body).decode(),'encoding':'base64'}})
  else:
   rec['content']=body.decode('utf8');need(b'\0' not in body,'Binary pretending to be UTF8')
  selected[path]=rec
 need(len(binary)==2,'Exact two published binary bodies required')
 selected_targets=[{'path':x[len(TARGET)+1:],'bytes':len(e['body']),'sha256':hashlib.sha256(e['body']).hexdigest()} for x,e in sorted(selected.items()) if x!=QUEUE]
 need(selected_targets==acceptance['target_bodies'],'Root acceptance and complete target selection differ')
 need({e['path'] for e in acceptance['target_bodies']}=={str(f.relative_to(candidate)) for f in candidate.rglob('*') if f.is_file()},'Candidate/accepted full inventory differs')
 original_path=W/'original_submission/MANIFEST_WITH_MODES.json';binding_path=W/'original_submission/BINDING.json'
 need(pin(original_path)==s['original_manifest'] and pin(binding_path)==s['original_binding'],'Original binding/manifest drift')
 binding=m.load_json_no_duplicates(binding_path);need(binding['commit']==AUTHOR and binding['root_tree']=='1603b2bbd482f196b97e8237ecfa206282f44914' and binding['target_tree']=='14c0617b4dbb7d4d064d527df85a2ab6c212f028' and binding['target_leaves']==17,'Original immutable identities differ')
 original=m.load_json_no_duplicates(original_path)
 originals=[e for e in original if e['path'].startswith(TARGET+'/')];need(len(originals)==17 and all(e['path'] in selected for e in originals),'Original17 retained')
 historical=['REVIEW_REQUEST.md','checks/verify.py','checks/CHECKS.json',*[e['path'][len(TARGET)+1:] for e in originals if e['path'].startswith(TARGET+'/independent_review/')]]
 need(len(historical)==9,'Historical9 census')
 for rel in historical:
  e=next(e for e in originals if e['path']==TARGET+'/'+rel);need(selected[e['path']]['git_blob']==e['git_blob'] and selected[e['path']]['source']['sha256']==e['sha256'],'Historical original body changed')
 for private in [m.DRIVER,m.OBJECTS]:need(private.resolve()==private and not private.is_symlink() and private.is_relative_to(ROOT),'Private metadata path is unsafe')
 for alternate in m.ALTERNATES:need(alternate.resolve()==alternate and not alternate.is_symlink() and alternate.is_relative_to(B),'Read-only alternate path is unsafe')
 m.OBJECTS.mkdir(exist_ok=True)
 env=m.private_environment(out)
 if not m.DRIVER.exists():
  subprocess.run(['git','--no-replace-objects','init','--bare','--initial-branch=main',str(m.DRIVER)],env=env,capture_output=True,check=True,timeout=45)
 remotes=subprocess.run(['git','--no-replace-objects','--git-dir',str(m.DRIVER),'config','--local','--get-regexp','^remote\\.'],env=env,capture_output=True,timeout=10)
 need(remotes.returncode==1 and remotes.stdout==b'','Private driver must have no remotes')
 need(m.run_git(env,'cat-file','-t',a.main).decode().strip()=='commit','Literal MAIN must be a commit')
 before_tree=m.run_git(env,'rev-parse',a.main+'^{tree}').decode().strip();before=m.inventory(env,a.main)
 need(not any(x==TARGET or x.startswith(TARGET+'/') or x=='unsolved_math_prioritization/attempts/30000170' or x.startswith('unsolved_math_prioritization/attempts/30000170/') for x in before),'Existing independent target cannot be overwritten')
 need(before[QUEUE]['mode']=='100644' and before[QUEUE]['type']=='blob','QUEUE mode/type changed')
 base=Path(s['base_queue']['path']);need(pin(base)==s['base_queue'],'Whole baseline QUEUE source changed');basebody=base.read_bytes();need(m.git_oid('blob',basebody)==before[QUEUE]['sha'],'Whole QUEUE not explicit MAIN body')
 oldlines,i,oldrow=row(basebody);newbody=selected[QUEUE]['body'];newlines,j,newrow=row(newbody)
 need(i==j and oldlines[:i]==newlines[:i] and oldlines[i+1:]==newlines[i+1:] and oldrow!=newrow,'QUEUE change must be exactly one row')
 need(oldrow==base64.b64decode(s['queue_before_base64']) and newrow==base64.b64decode(s['queue_after_base64']),'Root exact row controls differ')
 cols=newrow.split(b'|');need(cols[8].strip()==b'claimed_solved' and cols[9].strip()==b'1/5' and b'10.5281/zenodo.23306332' in newrow and b'../attempts/30000170/PROOF.md' in newrow,'QUEUE status/budget/link/DOI differ')
 leaves={x:e for x,e in before.items() if e['type']!='tree'};nonempty=set()
 for path in leaves:
  parts=path.split('/');nonempty.update('/'.join(parts[:i]) for i in range(1,len(parts)))
 need(all(x in nonempty for x,e in before.items() if e['type']=='tree'),'Empty trees cannot be preserved by index')
 for path in selected:
  parts=path.split('/');need(all('/'.join(parts[:i]) not in before or before['/'.join(parts[:i])]['type']=='tree' for i in range(1,len(parts))),'Selected ancestor collision')
 m.run_git(env,'read-tree','--empty')
 m.run_git(env,'update-index','--info-only','-z','--index-info',data=b''.join((e['mode']+' '+e['sha']+'\t'+path).encode()+b'\0' for path,e in sorted(leaves.items())))
 for e in selected.values():need(m.run_git(env,'hash-object','-w','--stdin',data=e['body']).decode().strip()==e['git_blob'],'Private selected blob differs')
 m.run_git(env,'update-index','-z','--index-info',data=b''.join(('100644 '+e['git_blob']+'\t'+path).encode()+b'\0' for path,e in sorted(selected.items())))
 tree=m.run_git(env,'write-tree','--missing-ok').decode().strip();after=m.inventory(env,tree);expected=dict(leaves);expected.update({path:{'mode':'100644','type':'blob','sha':e['git_blob']} for path,e in selected.items()})
 need({x:e for x,e in after.items() if e['type']!='tree'}==expected,'Complete leaf/path/mode/OID conservation differs')
 raw=m.RawReader(env);main_kind,main_raw=raw.get(a.main);need(main_kind=='commit' and main_raw.split(b'\n',1)[0]==b'tree '+before_tree.encode(),'Raw literal MAIN/first tree header differs')
 before_raw=raw.walk(before_tree);after_raw=raw.walk(tree);raw.close()
 raw_leaves={x:e for x,e in before_raw.items() if e[0]!=b'40000'};rawexpected=dict(raw_leaves);rawexpected.update({x.encode():(b'100644',e['git_blob']) for x,e in selected.items()})
 need({x:e for x,e in after_raw.items() if e[0]!=b'40000'}==rawexpected,'Raw Merkle whole-leaf conservation differs')
 identity='Alec Kriebel <me@aleckriebel.com> '+str(int(t.timestamp()))+' +0000';message='PR263: publish audited complex-quadratic nearest-stability note\n'
 commitbody=('tree '+tree+'\nparent '+AUTHOR+'\nparent '+a.main+'\nauthor '+identity+'\ncommitter '+identity+'\n\n'+message).encode();commit=m.git_oid('commit',commitbody)
 need(m.run_git(env,'hash-object','-t','commit','-w','--stdin',data=commitbody).decode().strip()==commit,'Private commit differs')
 treepayload={'base_tree':before_tree,'tree':[dict(path=path,mode='100644',type='blob',**({'content':e['content']} if 'content' in e else {'sha':e['git_blob']})) for path,e in sorted(selected.items())]}
 commitpayload={'tree':tree,'parents':[AUTHOR,a.main],'message':message,'author':{'name':'Alec Kriebel','email':'me@aleckriebel.com','date':a.date},'committer':{'name':'Alec Kriebel','email':'me@aleckriebel.com','date':a.date}}
 cas={'query':'mutation PR263ScopedAuthorCAS($input:UpdateRefsInput!){updateRefs(input:$input){clientMutationId}}','variables':{'input':{'repositoryId':REPO,'refUpdates':[{'name':BRANCH,'beforeOid':AUTHOR,'afterOid':commit,'force':False}],'clientMutationId':'pr263-'+commit}}}
 manifest=[{'path':path,'mode':'100644','git_blob':e['git_blob'],'bytes':len(e['body']),'sha256':hashlib.sha256(e['body']).hexdigest(),'source':e['source']['source']} for path,e in sorted(selected.items())]
 result={'schema':'pr263-private-native-reconciliation-v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'main':a.main,'main_tree':before_tree,'original_author':AUTHOR,'tree':tree,'commit':commit,'ordered_parents':[AUTHOR,a.main],'selected_count':len(selected),'target_count':len(selected)-1,'before_leaf_count':len(leaves),'after_leaf_count':len(expected),'unselected_leaves_preserved':len(set(leaves)-set(selected)),'queue_before':oldrow.decode(),'queue_after':newrow.decode(),'selected_full_body_manifest':manifest,'root_selection':pin(control),'candidate_acceptance':s['candidate_acceptance'],'checked_private_helper':pin(H),'provider_mutations':0,'primary_local_Git_mutations':0,'prepared_only_not_execution_authority':True}
 for name,obj in [('PREPARATION.json',result),('TREE_PAYLOAD.json',treepayload),('COMMIT_PAYLOAD.json',commitpayload),('AUTHOR_CAS_PAYLOAD.json',cas),('BINARY_BLOB_PAYLOADS.json',binary)]:
  (out/name).write_text(json.dumps(obj,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['main','main_tree','tree','commit','ordered_parents','selected_count','unselected_leaves_preserved','provider_mutations','primary_local_Git_mutations']},indent=2))
if __name__=='__main__':main()
