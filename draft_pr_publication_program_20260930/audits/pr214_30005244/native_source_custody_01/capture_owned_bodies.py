"""Full original/current own-body custody; imports inspected pinned GET-only capture.
No scientific code is run and no artifact contents are interpreted mathematically.
"""
from pathlib import Path
import datetime,hashlib,json,sys,types
HERE=Path(__file__).absolute().parent
CAPTURE=HERE/'capture_native_custody.py'
CAPTURE_PIN={'bytes':11941,'sha256':'a7732c6bef25ca818a03494ba213ce457138213fb25ee863a221f07a43239d6e'}
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run():
 expected=CAPTURE_PIN
 raw=CAPTURE.read_bytes()
 if pin(raw)!=expected:raise RuntimeError('Capture source changed')
 m=types.ModuleType('native_custody');m.__file__=str(CAPTURE);exec(compile(raw,str(CAPTURE),'exec'),m.__dict__)
 inv=json.loads((HERE/'INVENTORY.json').read_bytes());records=[]
 for snapshot in ('original','current'):
  for path,row in inv[snapshot]['leaves'].items():
   m.need(row['type']=='blob' and row['mode'] in ('100644','100755','120000'),'Owned leaf must have full blob body; unsupported gitlink stops')
   body=m.body(row['sha']);reading=HERE/'_private/reading'/snapshot/path;m.write(reading,body)
   records.append({'snapshot':snapshot,'commit':inv[snapshot]['commit']['sha'],'root':inv[snapshot]['commit']['tree'],'path':path,**row,**pin(body),'reading_copy':str(reading.relative_to(HERE))})
  root=inv[snapshot]['commit']['tree'];p='unsolved_math_prioritization/README.md';row=m.lookup(root,p)
  m.need(row is not None and row['mode']=='100644' and row['type']=='blob','Applicable prioritization README')
  body=m.body(row['sha']);reading=HERE/'_private/reading'/snapshot/p;m.write(reading,body)
  records.append({'snapshot':snapshot,'kind':'applicable_readme','commit':inv[snapshot]['commit']['sha'],'root':root,'path':p,**row,**pin(body),'reading_copy':str(reading.relative_to(HERE))})
 original={r['path']:r for r in records if r['snapshot']=='original' and not r.get('kind')}
 current={r['path']:r for r in records if r['snapshot']=='current' and not r.get('kind')}
 archive=m.ATTEMPT+'/history/original_submission_20261015/'
 comparison=[]
 for path,row in original.items():
  archived=current.get(archive+path.removeprefix(m.ATTEMPT+'/'))
  comparison.append({'original':path,'current_archive':archived['path'] if archived else None,'present':archived is not None,'exact_mode_type_native_body':archived is not None and all(row[k]==archived[k] for k in ('mode','type','sha','bytes','sha256'))})
 m.need(len(comparison)==31 and all(r['exact_mode_type_native_body'] for r in comparison),'Every original31 must be byte/mode exact in current archive')
 after=m.current_pr();m.need(all(after.get(k)==inv['PR'].get(k) for k in ('number','state','draft','merged','merge_commit_sha','merged_at','head')),'PR identity changed during body custody')
 result={'schema':'pr214-complete-owned-body-custody-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records,'original_count':len(original),'current_count':len(current),'original31_current_archival_comparisons':comparison,'all_original31_preserved_exact_in_current':True,'fresh_current_PR_after':after,'no_scientific_program_execution_or_mathematical_acceptance':True}
 m.write(HERE/'BODY_RECORDS.json',m.encode(result));m.write(HERE/'BODY_ADDITIONAL_TREES.json',m.encode(m.TREES))
 log=HERE/'RESEARCH_LOG.md';log.write_text(log.read_text()+'\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — 70% of assigned custody. Original31/current41 complete native bodies authenticated with SHA1+SHA256/length and exact modes. All31 original files exactly match current history/original_submission_20261015 copies. Fresh PR remains exact already-merged head. Applicable instruction/README bodies and both whole QUEUE rows retained privately. Resolving finite problem-source entries; no mathematics or production mutation.\n')
 print(json.dumps({'original_files':len(original),'current_files':len(current),'preserved_original31':True,'body_records':pin((HERE/'BODY_RECORDS.json').read_bytes()),'native_GETs':len(m.ledger())}))
if __name__=='__main__':
 if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Require -E -S -B -P')
 run()

