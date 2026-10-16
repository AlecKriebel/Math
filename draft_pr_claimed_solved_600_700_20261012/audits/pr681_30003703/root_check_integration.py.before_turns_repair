#!/usr/bin/env python3
"""Independent exact-byte and scoped-tree checks of the accepted/published result."""
import argparse,datetime,hashlib,json,os,re,subprocess
from pathlib import Path
A=Path(__file__).absolute().parent;REPO=A.parents[2];N='unsolved_math_prioritization/attempts/30003703/';P='unsolved_math_prioritization/publications/30003703/';Q='unsolved_math_prioritization/QUEUE.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(c,m):
 if not c:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--merge',action='store_true');args=ap.parse_args()
 r=load(A/'INTEGRATION_PUSHED_RECEIPT.json');head=r['integration_commit'];base=r['main_base'];original=r['existing_pr_head']
 need(r['pushed'] is True and original=='e92320ea5979c812089780a982fbd88136a26522','integration identity')
 env={k:v for k,v in os.environ.items()if not k.startswith('GIT_')};env.update(GIT_OBJECT_DIRECTORY=r['object_directory'],GIT_ALTERNATE_OBJECT_DIRECTORIES=str(REPO/'.git/objects'),GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_COUNT='6',GIT_CONFIG_KEY_0='gc.auto',GIT_CONFIG_VALUE_0='0',GIT_CONFIG_KEY_1='maintenance.auto',GIT_CONFIG_VALUE_1='false',GIT_CONFIG_KEY_2='core.hooksPath',GIT_CONFIG_VALUE_2='/dev/null',GIT_CONFIG_KEY_3='fetch.writeCommitGraph',GIT_CONFIG_VALUE_3='false',GIT_CONFIG_KEY_4='submodule.recurse',GIT_CONFIG_VALUE_4='false',GIT_CONFIG_KEY_5='core.logAllRefUpdates',GIT_CONFIG_VALUE_5='false')
 def git(*a):return subprocess.run(['git',*a],cwd=REPO,env=env,capture_output=True,check=True).stdout
 def tree(h,prefix):
  output={}
  for row in git('ls-tree','-r','-z',h,'--',prefix).split(b'\0'):
   if not row:continue
   details,name=row.split(b'\t',1);mode,kind,oid=details.decode().split();output[name.decode()]={'mode':mode,'kind':kind,'oid':oid}
  return output
 actual=head;live=json.loads(subprocess.run(['gh','pr','view','681','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,mergeCommit,mergedAt'],capture_output=True,text=True,check=True).stdout)
 need(live['number']==681 and live['headRefOid']==head,'actual PR accepted head')
 if args.merge:
  need(live['state']=='MERGED' and not live['isDraft'] and live['mergedAt'],'not actually merged');actual=live['mergeCommit']['oid'];need(re.fullmatch('[a-f0-9]{40}',actual),'merge oid')
  git('fetch','--no-write-fetch-head','--no-tags','--no-recurse-submodules','--refmap=','https://github.com/AlecKriebel/Math.git',actual)
  parents=git('rev-list','--parents','-n','1',actual).decode().split()[1:];need(head in parents,'actual merge parent lacks accepted head')
 else:
  need(live['state']=='OPEN' and live['isDraft'],'unexpected PR state before edit/merge')
  remote=git('ls-remote','--heads','https://github.com/AlecKriebel/Math.git','refs/heads/research/30003703-andreadakis-counterexamples').decode().split();need(remote[0]==head,'branch readback')
 need(git('rev-parse',head+'^{tree}').decode().strip()==r['tree'],'accepted tree identity')
 need(git('rev-list','--parents','-n','1',head).decode().split()[1:]==[base,original],'accepted two-parent ancestry')
 allowed={Q}|{N+n for n in r['attempt_sha256']}|{P+n for n in r['publication_sha256']}
 changed={x.decode() for x in git('diff','--no-ext-diff','--no-textconv','--name-only','-z',base,head).split(b'\0') if x}
 need(changed==allowed,'accepted changes escaped target allowlist')
 expected_native=load(A/'SCOPE_AND_SNAPSHOT.json')['original_blobs'];native=tree(actual,N);need(set(native)==set(expected_native) and len(native)==23,'actual native inventory')
 for path,record in expected_native.items():
  entry=native[path];data=git('show',actual+':'+path)
  need(entry['mode']==record['git_mode']=='100644' and entry['kind']=='blob' and entry['oid']==record['git_blob'] and sha(data)==record['sha256'],'native bytes/blob/mode '+path)
 pub=tree(actual,P);need(set(pub)=={P+n for n in r['publication_sha256']},'actual publication inventory')
 for name,pin in r['publication_sha256'].items():
  entry=pub[P+name];need(entry['mode']=='100644' and entry['kind']=='blob' and sha(git('show',actual+':'+P+name))==pin,'publication bytes/mode '+name)
 for prefix in [N,P]:need(tree(head,prefix)==tree(actual,prefix),'accepted/actual scoped inventory differs')
 def selected(data):
  rows=[x for x in data.splitlines(keepends=True)if b'| 30003703 /' in x];need(len(rows)==1,'selected queue row uniqueness');return rows[0]
 bq=git('show',base+':'+Q);hq=git('show',head+':'+Q);aq=git('show',actual+':'+Q);before=selected(bq);after=selected(hq)
 need(bq.replace(before,b'__SELECTED_ROW__')==hq.replace(after,b'__SELECTED_ROW__'),'other accepted queue bytes changed')
 bc,ac=before.rstrip(b'\r\n').split(b'|'),after.rstrip(b'\r\n').split(b'|');need(len(bc)==len(ac) and [i for i,(x,y)in enumerate(zip(bc,ac))if x!=y]==[8,9,11],'queue exact three cells')
 need(bc[8].strip()==b'queued' and bc[9].strip()==b'0/5' and ac[8].strip()==b'claimed_solved' and ac[9].strip()==b'5/5' and r['doi'].encode() in ac[11],'queue status/turn/DOI')
 need(selected(aq)==after,'actual merge selected row differs')
 report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','pr':681,'problem_id':'30003703','accepted_head':head,'actual_commit':actual,'main_base':base,'original_head':original,'all_23_native_bytes_blobs_modes_exact':True,'publication_files':len(pub),'all_publication_bytes_and_modes_exact':True,'accepted_changed_paths':len(changed),'accepted_target_queue_changed_cells':['Status','Turns','Findings'],'selected_actual_queue_row':after.decode().rstrip(),'whole_actual_tree_equals_accepted':git('rev-parse',actual+'^{tree}')==git('rev-parse',head+'^{tree}'),'live_pr':live,'no_shared_index_checkout_refs_or_objects_written':True,'isolated_fetch_for_actual_merge_only':args.merge}
 output=A/('ROOT_ACTUAL_MERGE_TREE_CHECK.json'if args.merge else'ROOT_PUSHED_TREE_CHECK.json')
 with output.open('x')as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
