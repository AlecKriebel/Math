"""Own text binding writer. Reads genuine closed evidence; no ROOT/code execution."""
from pathlib import Path
import argparse,datetime as dt,hashlib,json,stat
P=Path(__file__).absolute().parent;A=P.parent;R=A.parents[2];F=A/'corrective_source_adversary_v5_m5_addendum'
def need(v,s):
 if not v:raise ValueError(s)
def raw(p):need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Regular evidence');return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def triple(p):return {k:v for k,v in ref(p).items() if k!='full_mode'}
def clock(s):need(type(s) is str,'UTC literal');v=dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s);need(v.tzinfo is not None and v.utcoffset()==dt.timedelta(0),'Aware UTC');return v
def load(p):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'Duplicate key');d[k]=v
  return d
 return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def encode(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def cap(path):
 c=load(path);need(c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['status']=='PASS' and c['operator_unchanged'] is True and c['operator_sha256']=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec' and c['cwd']==str(R) and c['stdin_supplied'] is False,'Actual completed SOURCE evidence child');need({q.name for q in path.parent.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Complete CAP4');need(clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual UTC interval')
 for k in ['stdout','stderr']:
  z=c[k];b=raw(path.parent/z['path']);need(z['path']==k+'.bin' and type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256'],'Entire retained stream')
 need(raw(path.parent/'stderr.bin')==b'' and sha(raw(path.parent/'prelaunch_operator.py'))==c['operator_sha256'],'Clean complete source evidence operator/streams');return dict(capture=ref(path),complete_capture=c,complete_members=[ref(q) for q in sorted(path.parent.iterdir())])
def main():
 p=argparse.ArgumentParser();p.add_argument('--closed-M5-self-sha256',required=True);p.add_argument('--actual-M5-close-capture',required=True);p.add_argument('--actual-M5-readback-capture',required=True);a=p.parse_args();mf=F/'SELF_MANIFEST.json';need(sha(raw(mf))==a.closed_M5_self_sha256,'Actual ROOT closed adverse self');s=load(mf);need(s['schema']=='pr48-M5-adverse-evidence-closure/v1' and s['source_only'] is True and s['self_excluded']==['SELF_MANIFEST.json'] and type(s['files_count']) is int and s['files_count']==len(s['files'])==13 and s['verdict_status']=='REPAIR_REQUIRED_SOURCE','Closed13-only adverse evidence')
 for z in s['files']:
  need(type(z['bytes']) is int and raw(F/z['path']) and len(raw(F/z['path']))==z['bytes'] and sha(raw(F/z['path']))==z['sha256'] and stat.S_IMODE((F/z['path']).stat().st_mode)==0o444,'Every actual closed adverse body/mode')
 need(stat.S_IMODE(mf.stat().st_mode)==0o444 and {q.name for q in F.iterdir()}=={z['path'] for z in s['files']}|{'SELF_MANIFEST.json'},'Exact actual closed adverse family');verdict=load(F/'VERDICT.json');need(verdict['status']=='REPAIR_REQUIRED_SOURCE' and [z['id'] for z in verdict['mandatory_findings']]==['M5'] and verdict['production_executed'] is False and verdict['future_acceptance_approved'] is False,'M5 rejection only')
 close=cap(R/a.actual_M5_close_capture);reader=cap(R/a.actual_M5_readback_capture);c,d=close['complete_capture'],reader['complete_capture'];ready=sha(raw(F/'READY.json'));need(ready=='806048fc93a582b09396dc279c9e7dbb6888b1311b792960c0bb6eb8205cb7ba','Fully read M5 READY')
 need(c['argv']==['/usr/bin/python3','-B',str(F/'close_adverse_family.py'),'--execute','--personally-read-complete-source','--ready-sha256',ready] and d['argv']==['/usr/bin/python3','-B',str(F/'verify_closed_adverse_family.py'),'--self-manifest-sha256',a.closed_M5_self_sha256] and clock(c['finished_utc'])<=clock(d['started_utc']),'Actual close then separate reader argv/chronology')
 need(load((R/a.actual_M5_close_capture).parent/'stdout.bin')['candidate_approved'] is False and load((R/a.actual_M5_readback_capture).parent/'stdout.bin')['candidate_approved'] is False,'No candidate approval from adverse custody')
 history=P/'preliminary_unclosed_READY_history';history.mkdir()
 for n in ['SOURCE_READY.json','REPORT.md','RESEARCH_LOG.md','M5_AND_SUPERSEDED_V5_BINDINGS.json']:
  with (history/n).open('xb') as f:f.write(raw(P/n))
 old=load(P/'SOURCE_READY.json');need(sha(raw(history/'SOURCE_READY.json'))=='81540e51b5859a99deb8ecf3ff21e800b0f6b003e6c7a878325e487e1c9a1a1a','Exact preserved preliminary unclosed READY')
 failure=load(P/'M5_AND_SUPERSEDED_V5_BINDINGS.json');failure['independent_M5_review']=dict(status='GENUINELY_ROOT_CLOSED_ADVERSE_EVIDENCE_ONLY',observed_utc=dt.datetime.now(dt.timezone.utc).isoformat(),self_manifest=ref(mf),report=ref(F/'REPORT.md'),verdict=ref(F/'VERDICT.json'),control_source=ref(F/'private_clock_controls.py'),entire_control_result=load(F/'PRIVATE_CLOCK_CONTROL_RESULTS.json'),complete_actual_close=close,complete_actual_separate_readback=reader,candidate_V6_approved=False);(P/'M5_AND_SUPERSEDED_V5_BINDINGS.json').write_bytes(encode(failure))
 with (P/'REPORT.md').open('a') as f:f.write('\nThe genuine closed M5 adverse report/verdict and all ten independent control outcomes were fully read. The final M5 binding retains its actual SELF full0444 and both complete genuine ROOT CAP4s. This is rejected-V5 evidence custody; it does not approve V6. Preliminary READY81540e51 and its dated report/log/M5 record are preserved unchanged under preliminary_unclosed_READY_history, explicitly unclosed and superseded.\n')
 with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\nFinal source checkpoint100%, actual recovery0%, independent V6 review0%. Fully read M5 report/verdict/private source/results/ready; genuine ROOT adverse closure/separate reader are now bound as completed adverse evidence only. Preliminary unclosed READY81540e51 and its prior report/log/M5 record remain byte-preserved in the dedicated history folder. No V6 production or ROOT execution by preparer.\n')
 old['utc']=dt.datetime.now(dt.timezone.utc).isoformat();old['source_files']=[triple(R/z['path']) for z in old['source_files']];old['actual_M5_failure']=triple(P/'M5_AND_SUPERSEDED_V5_BINDINGS.json');old['genuine_closed_M5_adverse_SELF']=triple(mf);old['genuine_closed_M5_adverse_fullmode']=0o444;old['preliminary_unclosed_READY']=triple(history/'SOURCE_READY.json');old['preliminary_READY_was_ROOT_closed']=False;old['closure_payload_files']=sorted(q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file());old['closure_payload_count']=len(old['closure_payload_files']);old['closure_directory_count']=sum(q.is_dir() for q in P.rglob('*'));(P/'SOURCE_READY.json').write_bytes(encode(old))
 for q in P.rglob('*'):need(not q.is_symlink() and stat.S_IMODE(q.stat().st_mode)==(0o644 if q.is_file() else 0o755),'Final SOURCE raw fullmodes')
 print(json.dumps(dict(status='READY_FINAL_V6_SOURCE_ONLY_WAIT_ROOT',READY=ref(P/'SOURCE_READY.json'),report=ref(P/'REPORT.md'),payload_count=old['closure_payload_count'],relative_dirs=old['closure_directory_count'],actual_M5_adverse_SELF=ref(mf),production_executed=False)))
if __name__=='__main__':main()
