"""Complete immutable packet/history binding and private mathematical replay."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];M=json.loads((A/'snapshot_manifest.json').read_bytes());T=M['target_prefix'];D=A/'snapshot'/T
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
tmp=A/'tmp/root_original';streams=A/'root_original_streams';tmp.mkdir(parents=True,exist_ok=True);streams.mkdir(exist_ok=True)
assert not (tmp/'FINAL_AUTHOR_MANIFEST.json').exists();shutil.copytree(D,tmp,dirs_exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
checks=[];bindings=[];replays=[];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def ck(ok,label):
    checks.append({'label':label,'pass':bool(ok)});assert ok,label
ck(set(git('diff','--name-only',M['base'],M['head']).decode().splitlines())=={e['path'] for e in M['files']},'all47 actual changed paths')
for e in M['files']:
    b=(A/'snapshot'/e['path']).read_bytes();g=git('show',M['head']+':'+e['path']);ck(b==g and len(b)==e['bytes'] and sha(b)==e['sha256'] and blob(b)==e['git_blob_sha'],'immutable API/Git/snapshot '+e['path'])
manifests=[D/('TURN_'+str(i)+'_MANIFEST.json') for i in range(1,6)]+[D/'FINAL_AUTHOR_MANIFEST.json',D/'independent_review/REVIEW_MANIFEST.json',D/'PUBLICATION_MANIFEST.json']
for mp in manifests:
    m=json.loads(mp.read_bytes())
    for e in m['files']:
        f=mp.parent/e['path'];b=f.read_bytes();ok=len(b)==e['bytes'] and sha(b)==e['sha256'] and ('git_blob_sha1' not in e or blob(b)==e['git_blob_sha1']);ck(ok,'manifest '+mp.name+':'+e['path']);bindings.append({'manifest':str(mp.relative_to(D)),'path':e['path'],'bytes':len(b),'sha256':sha(b)})
for i in range(2,6):
    mp=D/('TURN_'+str(i)+'_MANIFEST.json');prev=D/('TURN_'+str(i-1)+'_MANIFEST.json');ck(json.loads(mp.read_bytes())['previous_manifest_sha256']==sha(prev.read_bytes()),'turn manifest chain '+str(i))
author=json.loads((D/'FINAL_PUBLIC_SCOPE.json').read_bytes())['files'];ck(len(author)==37 and len(set(author))==37,'unique37 final author scope')
review=json.loads((D/'independent_review/REMOTE_BINDING.json').read_bytes());wip=review['head'];ck(wip=='308b3ee53312800cfe6a82a2cdcc9763e1f90422','actual final WIP identity')
for e in review['files']:
    b=git('show',wip+':'+T+'/'+e['path']);ck(b==(D/e['path']).read_bytes() and len(b)==e['size'] and blob(b)==e['sha'],'actual37 final WIP raw '+e['path'])
history=['6fb965118ce87d6a25afa60f92cc21c78605eb4b','649acde2cf13c0a89ba7433b5cf4214e45cb8901','96158499a002790d1e82a62b8d43ee47836a312b','67c1e19c1c56f757896f509fab402441e99a58ea',wip];prev=M['base']
for i,h in enumerate(history,1):
    ck(git('show','-s','--format=%P',h).decode().strip()==prev,'actual author checkpoint parent '+str(i));state=json.loads(git('show',h+':'+T+'/TURN_'+str(i)+'_STATE.json'));ck(state['author_turns_completed']==i and state['budget']==5,'actual checkpoint turn state '+str(i))
    mf=json.loads(git('show',h+':'+T+'/TURN_'+str(i)+'_MANIFEST.json'))
    for e in mf['files']:ck(git('show',h+':'+T+'/'+e['path'])==(D/e['path']).read_bytes(),'actual checkpoint preserved '+str(i)+':'+e['path'])
    prev=h
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
commands=[(['verify_turn'+str(i)+'.py'],'TURN_'+str(i)+'_CHECKS.json','author_turn_'+str(i)) for i in range(1,6)]+[(['independent_review/independent_checks.py'],'independent_review/INDEPENDENT_CHECKS.json','historical_independent'),(['independent_review/verify_review.py','--author-dir',str(tmp)],None,'historical_wrapper')]
for args,expected,label in commands:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run([str(PY),*args],cwd=tmp,env=env,capture_output=True);(streams/(label+'.stdout')).write_bytes(r.stdout);(streams/(label+'.stderr')).write_bytes(r.stderr)
    ck(r.returncode==0 and not r.stderr,'complete private replay '+label)
    if expected:ck(r.stdout==(D/expected).read_bytes() and json.loads(r.stdout)==json.loads((D/expected).read_bytes()),'whole stdout/JSON exact '+label)
    replays.append({'label':label,'command':[str(PY),*args],'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'result':json.loads(r.stdout) if expected else r.stdout.decode()})
ck(sum(x['result']['assertions'] for x in replays[:5])==15618,'all15618 author assertions');ck(replays[5]['result']['assertions']==24692,'all24692 historical independent assertions')
result={'utc':now,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ROOT_COMPLETE_FROZEN_BINDINGS_HISTORY_AND_REPLAYS','checks':checks,'manifest_binding_instances':bindings,'binding_instance_count':len(bindings),'replays':replays,'actual_author_history':history,'actual_head':M['head'],'all47_changed_paths_all46_target_files_verified':True,'all37_actual_final_WIP_files_verified':True,'source_historical27_assets_not_independently_byte_reproduced':True,'source_scope':'Fresh primary mathematical statements checked separately; do not infer historical raw PDF/extract/render hashes from new fetches.','general_original_status':'unsolved5/5','paper_doi_tracker_release':False}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'manifest_instances':len(bindings),'replays':len(replays),'author_assertions':15618,'historical_assertions':24692,'historical_sources':'27 raw asset checks attributed to prior review; fresh byte recheck not asserted'}))
