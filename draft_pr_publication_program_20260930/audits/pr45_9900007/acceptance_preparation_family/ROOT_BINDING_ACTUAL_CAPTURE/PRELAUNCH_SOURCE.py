"""Read and bind the genuinely completed ROOT record; adapt exact actual query schema, no approval."""
from pathlib import Path
import datetime as dt,difflib,hashlib,json,os
H=Path(__file__).resolve().parent;A=H.parent;R=H.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(n,v):
 with (H/n).open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n')
def main():
 p=A/'ROOT_WHOLE_CURRENT_REVIEW.json';raw=p.read_bytes();root=load(p)
 if sha(raw)!='122fd1e3df7918cc32cbcccd75a94956e01cf1acbfc914c71f1547217beacc71' or root['schema']!='pr45-root-complete-closed-whole-inspection/v1' or root['future_execution_approved'] is not False or root['mandatory_corrections']!=[]:raise ValueError('Genuine scoped ROOT record required')
 put('EXPECTED_ROOT_WHOLE_REVIEW.json',root)
 inputs=load(H/'INPUT_BINDINGS_PENDING_ROOT.json');inputs['closed_root_whole_inspection']=pin(p)
 for n in ['ROOT_SOURCE_SAFETY_INSPECTION.json','ROOT_EVIDENCE_BINDINGS.json','ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md','ROOT_CLOSED_WHOLE_INSPECTION_PRELAUNCH_SOURCE_V2.py','inspect_closed_whole_ROOT_v2.py','inspect_closed_whole_ROOT.py']:
  inputs['pins'][n]=pin(A/n)
 for folder in ['root_closed_whole_inspection_actual_capture','root_closed_whole_inspection_v2_actual_capture','root_closed_whole_direct_git_v2']:
  for p in sorted((A/folder).rglob('*')):
   if p.is_file():inputs['pins'][p.relative_to(A).as_posix()]=pin(p)
 P=A.parent/'pr44_2912'
 inputs['pins']['actual44_post_inspector_prelaunch_source']=pin(P/'ROOT_POST_INSPECTION_PRELAUNCH_SOURCE_V2.py')
 put('INPUT_BINDINGS.json',inputs)
 source=H/'pr45_guards.py';before=source.read_text();(H/'BASIS_BEFORE_GENUINE_ROOT_QUERY_SCHEMA.py').write_text(before)
 st=before.index('    for n in sorted(historical):expected.extend',before.index('def basis('));en=before.index("    require(type(root['complete_actual_captures_checked'])",st)
 replacement=r'''    for n in sorted(historical):expected.extend([['git','show',dated_head+':'+n],['git','ls-tree',dated_head,'--',n]])
    require(equal([z['argv'] for z in commands],expected),'Exact ROOT full actual argv sequence')
    actual_source=inputs['pins']['inspect_closed_whole_ROOT_v2.py'];actual_operator=inputs['pins']['root_closed_whole_inspection_v2_actual_capture/prelaunch_operator.py']
    parent_capture=load(R/inputs['pins']['root_closed_whole_inspection_v2_actual_capture/CAPTURE.json']['path'])
    required(parent_capture,{'schema':'root-explicit-command-capture/v1','actual_execution':True,'completed':True,'exit_code':0,'stdin_supplied':False,'operator_unchanged':True,'status':'PASS','pid':root['actual_direct_four_operator_pid']},'Genuine ROOT whole checker parent capture')
    require(regular(R,actual_source['path']).read_bytes()==regular(R,inputs['pins']['ROOT_CLOSED_WHOLE_INSPECTION_PRELAUNCH_SOURCE_V2.py']['path']).read_bytes(),'Genuine ROOT prelaunch source exact')
    for i,z in enumerate(commands):
        keyset(z,{'schema','argv','cwd','operator_pid','started_utc','source_sha256','operator_sha256','pid','exit_code','finished_utc','stdout','stderr','source_unchanged','operator_unchanged'},'Exact actual known ROOT native4 query schema')
        required(z,{'schema':'pr45-root-independent-frozen-native-git/v1','cwd':str(R),'operator_pid':root['actual_direct_four_operator_pid'],'exit_code':0,'source_unchanged':True,'operator_unchanged':True,'source_sha256':actual_source['sha256'],'operator_sha256':actual_operator['sha256']},'Whole actual ROOT native4 query')
        require(type(z['pid']) is int and z['pid']>0 and utc_clock(parent_capture['started_utc'],'ROOT parent start')<=utc_clock(z['started_utc'],'Git start')<=utc_clock(z['finished_utc'],'Git finish')<=utc_clock(parent_capture['finished_utc'],'ROOT parent finish'),'Actual query PID/capture clocks')
        for channel in ['stdout','stderr']:exact_reference(z[channel]);check(R,[z[channel]])
        require(regular(R,z['stderr']['path']).read_bytes()==b'','Complete direct stderr');raw=regular(R,z['stdout']['path']).read_bytes();n=sorted(historical)[i//2]
        if not i%2:require(len(raw)==native[n]['bytes'] and sha(raw)==native[n]['sha256'],'Whole direct frozen show stdout')
        else:
            require(raw.endswith(b'\n') and raw.count(b'\n')==1,'One whole direct ls-tree line');fields,literal=raw.decode().rstrip('\n').split('\t');mode,kind,blob=fields.split();require(mode=='100644' and kind=='blob' and literal==n,'Direct ls-tree exact100644/path')
'''
 after=before[:st]+replacement+before[en:];source.write_text(after)
 (H/'GENUINE_ROOT_QUERY_SCHEMA_ADAPTATION.patch').write_text(''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='BASIS_BEFORE_GENUINE_ROOT_QUERY_SCHEMA.py',tofile='pr45_guards.py')))
 with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Genuine ROOT binding checkpoint:85% preparation,0% acceptance/discovery. Exact128346-byte Rootwhole122fd1... now read and pinned, along with successful59667 capture, every eight native4 full query stream/prelaunch source/operator and retained failed59202. Source query guard now requires actual known body-then-tree schema with full typed object equality; no invented actual_execution fields appended. Independent controls remain, future approval staysfalse/null.\n')
 print(json.dumps({'status':'GENUINE_ROOT_WHOLE_BOUND_SOURCE_ONLY','actual_child_pid':os.getpid(),'ROOT_ref':pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),'future_ROOT_acceptance_approved':False,'production_executed':False,'individual_input_pins':len(inputs['pins'])},sort_keys=True))
if __name__=='__main__':main()
