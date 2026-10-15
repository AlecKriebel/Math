#!/usr/bin/env python3
import ctypes, datetime as dt, hashlib, json, math, os, re, stat
from pathlib import Path
R=Path('/Users/alec/Documents/Math'); A=R/'draft_pr_publication_program_20260930/audits/pr47_2849'; F=A/'current_source_adversary_family_v2'; S=A/'current_preparation_family_v2'; B=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'
assert __debug__
checks=[]; rows=[]
def ck(x,label): assert x,label; checks.append(label)
def sha(x): return hashlib.sha256(x).hexdigest()
def read(p):
 ck(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular nonsymlink read')
 b=p.read_bytes(); rows.append({'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}); return b
def timestamp(v):
 assert type(v) is str
 x=dt.datetime.fromisoformat(v.replace('Z','+00:00')); assert x.tzinfo is not None and x.utcoffset()==dt.timedelta(0)
 return x
mf=json.loads(read(S/'PREPARATION_MANIFEST.json')); caps=[]
for n in ['root_pr47_source_v2_closure_actual_capture','root_pr47_source_v2_closed_readback_actual_capture']:
 D=B/n; ck({p.name for p in D.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'exact external4')
 c=json.loads(read(D/'CAPTURE.json')); ck(c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and c['operator_unchanged'] is True and c['status']=='PASS','genuine ROOT actual child')
 for k in ['stdout','stderr']:
  b=read(D/c[k]['path']); ck(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'full external stream')
 ck(read(D/'stderr.bin')==b'','empty successful stderr'); ck(sha(read(D/'prelaunch_operator.py'))==c['operator_sha256'],'prelaunch operator exact')
 ck(all(stat.S_IMODE(p.stat().st_mode)==0o644 for p in D.iterdir()),'external exact full0644')
 ck(timestamp(c['started_utc'])<=timestamp(c['finished_utc'])<dt.datetime.now(dt.timezone.utc),'actual external child chronology'); caps.append(c)
ck(caps[0]['pid']==mf['actual_closure_pid']==32176,'actual closer PID')
ck(timestamp(caps[0]['started_utc'])<=timestamp(mf['utc'])<=timestamp(caps[0]['finished_utc'])<timestamp(caps[1]['started_utc'])<=timestamp(caps[1]['finished_utc']),'closer and separate AFTER-exit readback')
ck(caps[1]['argv'][-1]==sha(read(S/'PREPARATION_MANIFEST.json')),'readonly verified exact closed manifest')
ck(read(S/'close_source_preparation_v2.py')==read(A/'ROOT_SOURCE_V2_CLOSURE_PRELAUNCH_SOURCE.py')==read(S/'CLOSURE_PRELAUNCH_SOURCE.py'),'closer full prelaunch source identities')
patch=json.loads(read(S/'CURRENT_QUEUE_PATCH.json')); before=read(S/'native4_proposal/preimage/unsolved_math_prioritization__QUEUE.md'); after=read(S/'native4_proposal/prospective/unsolved_math_prioritization__QUEUE.md')
ck(sha(before)==patch['queue_preimage_sha256'] and sha(after)==patch['queue_prospective_sha256'],'queue proposal full body pins')
ck(before.count(patch['row_before'].encode())==1 and after==before.replace(patch['row_before'].encode(),patch['row_prospective'].encode()),'exact one target-row substitution')
b=patch['row_before'].split('|'); a=patch['row_prospective'].split('|'); ck(len(a)==len(b)==14 and all(x==y for i,(x,y) in enumerate(zip(a,b)) if i not in [8,9,11]),'all other cells exact')
ck(a[8].strip()=='unsolved' and a[9].strip()=='1/5' and 'PENDING' in a[11],'scoped proposed status and accounting')
for n in ['unsolved_math_prioritization__state.json','unsolved_math_prioritization__history.jsonl','draft_pr_publication_program_20260930__inventory.json']: ck(read(S/'native4_proposal/preimage'/n)==read(S/'native4_proposal/prospective'/n),'othernative3 exact unchanged')
for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:
 o=json.loads(read(S/'operative_proposal'/n)); ck(o['status']=='unsolved' and o['full_problem_solved'] is False,'scoped unresolved record')
 for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']: ck(o.get(k) is None,'no invented runtime/current verdict')
ck(read(S/'presentations/README.md')==read(S/'presentations/PR_DRAFT.md')==read(S/'presentations/pr_body.md')==read(S/'presentations/CURRENT_CONTEXT.md')==read(S/'presentations/CURRENT_REVIEW_CONTEXT.md'),'all presentation bodies exact identical')
for n in ['operative_proposal/OBSTRUCTION.md','operative_proposal/README.md','operative_proposal/REALIZED_DEGENERACY_PROOF.md','operative_proposal/RESEARCH_LOG.md','operative_proposal/review/REVIEW.md','presentations/README.md']:
 text=read(S/n).decode(); ck('The universal-vanishing route stays blocked' in text and 'I# rank of this example is not computed' in text and 'Original turns.json is one JSON OBJECT' in text and 'The older review is not the current verdict' in text,'global qualified route/math/history')
 for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
  if 'current_source_adversary_family/REPORT.md' in link: ck(((S/n).parent/link).resolve()==A/'current_source_adversary_family/REPORT.md','actual ADVERSE link resolves')
builder=read(S/'prepare_current_packet.py').decode(); operator=read(S/'capture_root_builder_operation.py').decode()
for phrase in ["not sys.flags.optimize", "PYTHONOPTIMIZE", "nativecheck()", "recheck()", "publish_absent(stage,dest)", "need(not dest.exists() and not dest.is_symlink()", "source_preparation_version':2", "clock(prep['utc'])", "all36 real"]:
 if phrase=='all36 real': continue
 ck(phrase in builder,'reviewed source guard '+phrase)
ck(operator.index("rec['exit_code']=child.wait")<operator.index("write(capture/'CAPTURE.json',rec)"),'outer completion written after actual child wait')
ck("GIT_COMMANDS.json').write_bytes(enc(commands))" in builder and 'inner_GIT_COMMANDS_written_incrementally_while_builder_alive' in builder and 'frozen_inner_copy_is_prepublication_prefix' in builder and 'outer_operator_does_not_write_inner_commands' in builder,'honest inner/outer chronology source')
ck('ROOT_personally_reads_original_final_inner_full_records_streams_AFTER_child_exit' in builder and 'ROOT_full_final_outer_capture_and_original_inner_full_records_streams_read_AFTER_child_exit_required' in operator,'ROOT actual original final readback gate')
ck("current_verdict':None" in builder and "native_mirror_disposition':'PENDING'" in builder and "paper_created':False" in builder,'generated output future flags')
# Actual exclusive creation and case-insensitive absent-only publication controls.
X=F/'PRIVATE_ADDITIONAL'; X.mkdir(); p=X/'xb'; p.write_bytes(b'original')
try:
 with p.open('xb') as h: h.write(b'replace')
except FileExistsError: ck(p.read_bytes()==b'original','exclusive creation retains original')
else: raise AssertionError('exclusive creation replaced')
src=X/'source'; src.mkdir(); (src/'member').write_bytes(b'own'); dst=X/'MixedCase'; dst.mkdir(); (dst/'member').write_bytes(b'original')
alias=X/'mixedcase'; ck(alias.exists() and alias.samefile(dst),'actual filesystem case alias')
lib=ctypes.CDLL(None,use_errno=True); rename=lib.renamex_np; rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
ck(rename(os.fsencode(src),os.fsencode(alias),4)==-1 and (src/'member').read_bytes()==b'own' and (dst/'member').read_bytes()==b'original','actual RENAME_EXCL alias rejection')
def strict(b):
 def pairs(items):
  o={}
  for k,v in items: assert k not in o; o[k]=v
  return o
 def constant(v): raise ValueError(v)
 def floating(v):
  f=float(v); assert math.isfinite(f); return f
 return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
for b in [b'{"a":1,"a":2}',b'NaN',b'Infinity',b'-Infinity',b'1e1000']:
 try: strict(b)
 except (AssertionError,ValueError): ck(True,'duplicate/nonfinite rejected')
 else: raise AssertionError('invalid JSON accepted')
for v in ['2026-10-03T00:00:00','2026-10-03T00:00:00+01:00',False,None]:
 try: timestamp(v)
 except (AssertionError,ValueError,TypeError): ck(True,'invalid awareUTC rejected')
 else: raise AssertionError('invalid time accepted')
out={'schema':'pr47-source-v2-independent-supplemental-controls/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'assertions':len(checks),'checks':checks,'full_read_rows':rows,'entire_ROOT_external_closing_and_after_exit_readback':caps,'native4_dated_proposal_only':True,'production_import_compile_execution':False,'full_problem_solved':False,'future_acceptance_approved':False}
(F/'SUPPLEMENTAL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps({k:v for k,v in out.items() if k not in ['checks','full_read_rows','entire_ROOT_external_closing_and_after_exit_readback']},indent=2))
