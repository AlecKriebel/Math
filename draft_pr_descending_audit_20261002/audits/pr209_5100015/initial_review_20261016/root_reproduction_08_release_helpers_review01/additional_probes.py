"""Additional exact-caller lifecycle and native-concurrency controls."""
from pathlib import Path
import json,types
import probes as p

RESULTS=[]
def run(label,fn):
 try:RESULTS.append(dict(label=label,status='PASS',detail=fn()))
 except Exception as e:RESULTS.append(dict(label=label,status='PROBE_ERROR',error=type(e).__name__+': '+str(e)))
 p.dump(p.HERE/'ADDITIONAL_PROBE_RESULTS.json',RESULTS);print(json.dumps(RESULTS[-1]))
def unpublish(f):
 for n in ['ZENODO_VERIFIED_PUBLICATION.json','TRACKER_VERIFIED_APPEND.json']:(f.pub/n).unlink()

def publish_baseline():
 f=p.Fixture('publish_baseline');unpublish(f);f.execute('publish_preprint.py');f.save()
 ops=[c['operation'] for c in f.calls if c['provider']=='zenodo-kit']
 assert ops==['check','stage','inspect','publish','inspect'];z=f.rb.publication(f.r,f.pub,f.ctx)
 return dict(operations=ops,verified=z['metadata_and_files_verified'],stage_intent=(f.pub/'STAGE_ATTEMPT.json').exists(),publish_intent=(f.pub/'PUBLISH_ATTEMPT.json').exists())

def lost_stage():
 f=p.Fixture('lost_stage');unpublish(f);real=f.run
 def call(args,**kw):
  r=real(args,**kw)
  if len(args)>3 and args[3]=='stage':raise TimeoutError('synthetic lost stage outcome')
  return r
 f.run=call;first=p.rejection(lambda:f.execute('publish_preprint.py'));before=len(f.calls);second=p.rejection(lambda:f.execute('publish_preprint.py'));f.save()
 assert len(f.calls)==before and (f.pub/'STAGE_ATTEMPT.json').exists()
 return dict(first=first,retry=second,retry_provider_calls=0)

def lost_publish():
 f=p.Fixture('lost_publish');unpublish(f);real=f.run
 def call(args,**kw):
  r=real(args,**kw)
  if len(args)>3 and args[3]=='publish':raise TimeoutError('synthetic lost publish outcome')
  return r
 f.run=call;first=p.rejection(lambda:f.execute('publish_preprint.py'));f.run=real;before=len(f.calls);retry=p.rejection(lambda:f.execute('publish_preprint.py'));assert len(f.calls)==before
 f.execute('verify_published_readonly.py');f.save();assert f.rb.publication(f.r,f.pub,f.ctx)
 return dict(first=first,retry=retry,operations=[c['operation'] for c in f.calls if c['provider']=='zenodo-kit'],read_only_recovery_verified=True)

def absent_clearance():
 f=p.Fixture('absent_clearance');unpublish(f);(f.r/'FINAL_CLEARANCE.json').unlink();error=p.rejection(lambda:f.execute('publish_preprint.py'));assert not f.calls
 return dict(error=error,provider_calls=0)

def lost_append():
 f=p.Fixture('lost_append');(f.pub/'TRACKER_VERIFIED_APPEND.json').unlink();real=f.run
 def call(args,**kw):
  r=real(args,**kw)
  if args[0].endswith('/gws') and args[1:5]==['sheets','spreadsheets','values','append']:raise TimeoutError('synthetic lost append outcome')
  return r
 f.run=call;first=p.rejection(lambda:f.execute('append_verified_tracker.py'));f.run=real;f.execute('append_verified_tracker.py');f.save()
 t=json.loads((f.pub/'TRACKER_VERIFIED_APPEND.json').read_text());assert t['append_count']==0 and t['reconciled_existing_attempt'] and sum(c.get('operation')=='append' for c in f.calls)==1
 return dict(first=first,actual_append_calls=1,reconciled_receipt_append_count=t['append_count'])

def wrong_fourth_cell():
 f=p.Fixture('wrong_fourth_cell');(f.pub/'TRACKER_VERIFIED_APPEND.json').unlink();real=f.run
 def call(args,**kw):
  r=real(args,**kw)
  if args[0].endswith('/gws') and args[1:5]==['sheets','spreadsheets','values','get'] and not json.loads(args[args.index('--params')+1])['range'].endswith('A:D'):
   values=json.loads(r.stdout);values['values'][0][3]='corrupted fourth cell';r.stdout=json.dumps(values)
  return r
 f.run=call;error=p.rejection(lambda:f.execute('append_verified_tracker.py'));f.save();assert not (f.pub/'TRACKER_VERIFIED_APPEND.json').exists() and (f.pub/'private_transport/tracker/APPEND_ATTEMPT.json').exists()
 return dict(error=error,verified_receipt_exists=False,attempt_retained=True)

def queued_placeholder():
 f=p.Fixture('queued_placeholder');fields=p.ROW.split('|');fields[8]=' queued ';fields[9]=' 0/5 '
 for k in [10,11,12]:fields[k]='  '
 f.mainfiles['unsolved_math_prioritization/QUEUE.md']=('|'.join(fields)+'\n| foreign | preserved |\n').encode();f.commits[f.main]['tree']['sha']=f.tree(f.mainfiles);f.execute('integrate_reviewed_pr.py');f.save()
 files=f.files_by_tree[f.commits[f.pr['head']['sha']]['tree']['sha']];assert files['foreign-preserved.txt']==f.mainfiles['foreign-preserved.txt'] and b'| foreign | preserved |' in files['unsolved_math_prioritization/QUEUE.md']
 return dict(exact_placeholder_accepted=True,foreign_path_and_row_preserved=True,source_year_2021_retained=b'| 2021 | claimed_solved | 1/5 |' in files['unsolved_math_prioritization/QUEUE.md'])

def main_boundaries():
 out={}
 for label,change in [('existing_subtree',lambda f:f.mainfiles.update({p.PREFIX+'foreign-proof.md':b'foreign existing science'})),('changed_source_year',lambda f:f.mainfiles.update({'unsolved_math_prioritization/QUEUE.md':f.queue.replace(b'| 2021 |',b'| 2020 |')}))]:
  f=p.Fixture(label);change(f);f.commits[f.main]['tree']['sha']=f.tree(f.mainfiles);error=p.rejection(lambda:f.execute('integrate_reviewed_pr.py'));f.save();assert not f.mutations
  out[label]=dict(error=error,provider_mutations=0)
 return out

def current_main_race():
 f=p.Fixture('current_main_race');f.execute('integrate_reviewed_pr.py');prepared=json.loads((f.pub/'PR_PREPARED.json').read_text());before=len(f.calls)
 current=dict(f.mainfiles);current[p.PREFIX+'UNREVIEWED_CONCURRENT_PROOF.md']=b'unreviewed concurrent science\n';current['foreign-new-row.txt']=b'concurrent preserved data\n';f.main='main-concurrent';f.commits[f.main]=dict(tree={'sha':f.tree(current)},parents=[{'sha':prepared['main_parent']}]);f.execute('verify_and_merge.py');f.save();assert f.pr['merged']
 merge_calls=f.calls[before:];assert not any(c.get('path')=='git/ref/heads/main' for c in merge_calls)
 # Distinct-path additions merge cleanly: current main plus the candidate's
 # delta relative to its main parent retains this unreviewed proof path.
 merged=dict(current);base=f.files_by_tree[f.commits[prepared['main_parent']]['tree']['sha']];head=f.files_by_tree[f.commits[prepared['prepared_head']]['tree']['sha']]
 for name,raw in head.items():
  if base.get(name)!=raw:merged[name]=raw
 p.dump(f.base/'EXPECTED_CLEAN_MERGE_PATHS.json',sorted(merged))
 receipt=json.loads((f.pub/'PR_MERGED.json').read_text())
 return dict(merged_receipt=True,current_main_reads=0,concurrent_unreviewed_scientific_path_in_clean_merge=p.PREFIX+'UNREVIEWED_CONCURRENT_PROOF.md',hardcoded_program_counts=receipt['program_counts'])

if __name__=='__main__':
 for label,fn in [('publish_baseline',publish_baseline),('lost_stage',lost_stage),('lost_publish',lost_publish),('absent_clearance',absent_clearance),('lost_append',lost_append),('wrong_fourth_cell',wrong_fourth_cell),('queued_placeholder',queued_placeholder),('main_boundaries',main_boundaries),('current_main_race',current_main_race)]:run(label,fn)
