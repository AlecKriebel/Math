"""Read-only integration of actual producer-generated/published synthetic bytes.
This never runs the producer CLI, consumer main(), native transport or an intake.
Inputs must be exact Root-provided owned test artifacts, never the real A214 file.
"""
from pathlib import Path
import argparse,hashlib,json,sys,types
HERE=Path(__file__).absolute().parent
P=HERE.parents[1]
CONSUMER=HERE/'status_only_intake_after_pr214.py'
CONSUMER_PIN={'bytes':24956,'sha256':'a5dd2b47e66dff21fff04a1a0efac9edace7c911c2fba951471bac1013e7b7c0'}
REAL_TERMINAL=P/'audits/pr214_30005244/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json'
def need(x,msg):
 if type(x)is not bool or not x:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def rows(value):
 if type(value)is dict:
  yield value
  for x in value.values():yield from rows(x)
 elif type(value)is list:
  for x in value:yield from rows(x)
def run(published,published_pin,producer_source,producer_pin,execution,execution_pin):
 raw=CONSUMER.read_bytes();need(pin(raw)==CONSUMER_PIN,'Frozen unchanged consumer')
 h=types.ModuleType('unchanged_after214_consumer');h.__file__=str(CONSUMER);exec(compile(raw,str(CONSUMER),'exec'),h.__dict__)
 need(published.is_absolute() and published!=REAL_TERMINAL and published.is_relative_to(P),'Only owned synthetic artifact, never actual terminal')
 artifact=h.regular(published);need(h.exact(pin(artifact),h.bytepin(published_pin)),'Exact published synthetic bytes pin')
 source=h.regular(producer_source);need(h.exact(pin(source),h.bytepin(producer_pin)),'Exact production generator source pin')
 execution_raw=h.regular(execution);need(h.exact(pin(execution_raw),h.bytepin(execution_pin)),'Exact actual synthetic execution evidence')
 evidence=h.decode(execution_raw);allrows=list(rows(evidence))
 publications=[r['terminal_receipt'] for r in allrows if type(r.get('terminal_receipt'))is dict
  and r['terminal_receipt'].get('bytes')==published_pin['bytes']
  and r['terminal_receipt'].get('sha256')==published_pin['sha256']
  and Path(r['terminal_receipt'].get('path','')).name=='ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json']
 need(bool(publications),'Producer execution must bind exact published terminal bytes/path')
 need(any(r.get('exclusive_atomic_publication')is True
  and r.get('post_publication_mutable_guard_performed')is False for r in allrows),'Executed exclusive production publisher evidence')
 proof=h.completion_proof(artifact,published_pin)
 need(h.exact(proof.get('terminal_source_pin'),producer_pin),'Published record must bind exact real generator source')
 checks=proof.get('source_gate_checks')
 need(type(checks)is dict and type(checks.get('refreshes_completed_before_record'))is int
  and checks['refreshes_completed_before_record']>=2
  and checks.get('all_exact_pins_and_gates_rechecked_successfully')is True
  and h.exact(checks.get('terminal_source_pin'),producer_pin),'Production source/gate refresh provenance')
 need(pin(CONSUMER.read_bytes())==CONSUMER_PIN,'Consumer changed during integration')
 return {'schema':'after214-actually-published-synthetic-consumer-integration-v1','status':'PASS',
  'consumer_pin':CONSUMER_PIN,'producer_source':{'path':str(producer_source),**producer_pin},
  'producer_execution_evidence':{'path':str(execution),**execution_pin},
  'published_record':{'reading_path':str(published),**published_pin},
  'original_synthetic_publication_paths':[r['path']for r in publications],
  'consumed_exact_actual_generator_published_bytes':True,'detached_fixture_substitution':False,
  'producer_refresh_count':checks['refreshes_completed_before_record'],
  'facts':{k:proof[k]for k in ('PR','workflow_percent','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor','goal_complete')},
  'membership_lengths':{k:len(proof[k])for k in ('fully_completed_eligible_PRs','published_PRs')},
  'actual_root_receipt_gate_or_intake_created':False,'native_or_provider_requests':0,
  'consumer_main_executed':False,'operational_authority_inferred_from_test':False}
if __name__=='__main__':
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize,'Use -E -S -B -P')
 p=argparse.ArgumentParser(description=__doc__)
 for n in ('published','producer-source','execution'):
  p.add_argument('--'+n,required=True);p.add_argument('--'+n+'-bytes',required=True,type=int);p.add_argument('--'+n+'-sha256',required=True)
 a=p.parse_args()
 def entry(n):
  n=n.replace('-','_');return Path(getattr(a,n)),{'bytes':getattr(a,n+'_bytes'),'sha256':getattr(a,n+'_sha256')}
 published,pp=entry('published');source,sp=entry('producer_source');execution,ep=entry('execution')
 print(json.dumps(run(published,pp,source,sp,execution,ep),sort_keys=True,indent=2))

