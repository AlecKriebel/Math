"""Independently rehash and resolve every custody stage and omission."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,datetime,collections
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';R=A/'repairs/case_alias01';T=A/'finalization/terminal_admin_20261015'
def read(p):return json.loads(p.read_text())
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def check(p,r):
    need(p.is_file() and not p.is_symlink(),'Missing/nonregular '+str(p));b=p.read_bytes()
    need(len(b)==r.get('bytes',r.get('size')) and hashlib.sha256(b).hexdigest()==r['sha256'],'Identity mismatch '+str(p))
def dump(n,o):(D/n).write_text(json.dumps(o,indent=2)+'\n')
hist=read(R/'HISTORICAL_STAGE_RESOLUTION.json');old=read(T/'HISTORICAL_STAGE_RESOLUTION.json')['records']
need(len(hist['records'])==2788 and len(hist['additional_terminal_rows'])==1558,'Historical count changed')
need(len(old)==2788,'Old terminal source count')
verified=[]
for i,(new,previous) in enumerate(zip(hist['records'],old)):
    need(new['prior_row_index']==i and new['prior_resolution_path']==previous['resolved_path'],'Old-row position/locator changed')
    for k in ['stage','captured_path','bytes','sha256']:need(new[k]==previous[k],'Old-row value drift '+k)
    q=A/new['resolved_path'];check(q,new);verified.append({**new,'actual_rehashed':True})
# Compare each original stage to its actual immutable pin manifest as well as
# the old and new resolution rows. No counts or acceptance banners substitute.
sets=[('terminal_immediate_inputs',T/'BASELINE_INPUT_PINS.json','records'),('preparation_204',P/'FROZEN_INPUTS.json','records'),('preparation_92',P/'INPUT_OUTPUT_PINS.json','records'),('repair_492_before',A/'repairs/package01/BASELINE_INPUT_PINS.json','records'),('repair_34_outputs',A/'repairs/package01/OUTPUT_PINS.json','records'),('repair_270_current',A/'repairs/package01/CURRENT_OUTPUT_PINS.json','records'),('repair_480_unchanged',A/'repairs/package01/PROTECTED_UNCHANGED.json','unchanged_records'),('whole01_25_outputs',A/'reviews/package_01/OUTPUT_PINS.json','files'),('whole02_25_outputs',A/'reviews/package_02/OUTPUT_PINS.json','files'),('whole02_569_inputs',A/'reviews/package_02/INPUT_PINS.json','files')]
stagecounts={}
for name,path,key in sets:
    original=read(path)[key];resolved=[r for r in hist['records'] if r['stage']==name]
    need(len(original)==len(resolved),'Stage length '+name)
    for r,s in zip(original,resolved):need((r['path'],r['bytes'],r['sha256'])==(s['captured_path'],s['bytes'],s['sha256']),'Original captured row mismatch '+name)
    stagecounts[name]=len(original)
extra_sources={'OUTPUT_PINS.json':read(T/'OUTPUT_PINS.json')['records'],'CURRENT_AUDIT_PINS.json':read(T/'CURRENT_AUDIT_PINS.json')['records'],'CURRENT_CANDIDATE_PINS.json':read(T/'CURRENT_CANDIDATE_PINS.json')['records'],'PROTECTED_UNCHANGED.json':read(T/'PROTECTED_UNCHANGED.json')['records']}
for name,rows in extra_sources.items():
    rr=[r for r in hist['additional_terminal_rows'] if r['stage']==name];need(len(rr)==len(rows),'Additional length')
    for s,r in zip(rr,rows):
        need((r['path'],r['bytes'],r['sha256'])==(s['captured_path'],s['bytes'],s['sha256']),'Additional captured mismatch')
        check(A/s['resolved_path'],s);verified.append({**s,'actual_rehashed':True})
# Current repair baseline, its nine before/after edits, 659 protected inputs,
# 322 current candidate rows, 684 current audit rows, and 39 sealed outputs.
changes={r['path']:r for r in read(R/'CHANGE_INVENTORY.json')['authorized_existing_changes']};need(len(changes)==9,'Nine changes')
baseline=read(R/'BASELINE_INPUT_PINS.json')['records'];need(len(baseline)==668,'Baseline668')
for r in baseline:
    q=A/r['path']
    if r['path'] in changes:
        c=changes[r['path']];need(c['before']==r,'Before capture drift');check(A/c['before_bytes_path_relative_to_audit'],r);check(q,c['after'])
    else:check(q,r)
counts={'case_repair_baseline':668,'case_repair_existing_edits':9}
for file,base,num in [('PROTECTED_UNCHANGED.json',A,659),('CURRENT_CANDIDATE_PINS.json',P,322),('CURRENT_AUDIT_PINS.json',A,684),('OUTPUT_PINS.json',R,39),('CORE_PROTECTED_IDENTITIES.json',A,25)]:
    rr=read(R/file)['records'];need(len(rr)==num,'Current count '+file)
    for r in rr:check(base/r['path'],r)
    counts[file]=len(rr)
# Original 116 map rows and ordering; all 128 exact source/copy pairs.
oldmap=read(R/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies'];copies=read(P/'INPUT_COPY_MAP.json')['copies']
need(len(oldmap)==116 and len(copies)==128 and copies[:116]==oldmap,'Original copy order/values')
copyrows=[]
for r in copies:
    src=A/r.get('source_snapshot',r['original_path']);dst=P/r['package_copy'];check(src,r);check(dst,r);need(src.read_bytes()==dst.read_bytes(),'Source/copy bytes')
    copyrows.append({**r,'actual_source_resolved':str(src.relative_to(A)),'actual_byte_equality':True})
# All omissions individually rehashed, including the full program source pins
# that the distribution correctly calls excerpts, never a complete copy.
omissions=[]
for name in ['WHOLE01_COPY_EXCLUSIONS.json','WHOLE02_COPY_EXCLUSIONS.json','CASE_ALIAS_COPY_EXCLUSIONS.json']:
    for r in read(P/name)['records']:
        q=A/r['path']
        if not q.exists():q=A.parents[1]/r['path']
        check(q,r);omissions.append({'ledger':name,**r,'actual_resolved':str(q)})
evidence=read(P/'CASE_ALIAS_SOURCE_EVIDENCE.json');program=A.parents[1]
for r in evidence['sources']:check(program/r['path'],r)
fullroot=read(program/'ROOT_CASE_ALIAS_SCOPE_REVIEW.json')
report=(program/'reviews/case_alias_scope_20261016/REPORT.md').read_text()
need(evidence['exact_report_section'] in report,'Scoped exact excerpt changed')
need(evidence['root_status']==fullroot['status'],'Scoped root status')
# These are evidence of then-actual old commands; no fresh old-command replay.
need(evidence['kind']=='SCOPED_AUTHORED_EXCERPTS_WITH_FULL_SOURCE_PINS','Excerpt mislabeled')
submitted=read(A/'SUBMITTED_PINS.json');need(len(submitted['files'])==9 and submitted['head_oid']=='fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','Nine original identity')
for r in submitted['files']:check(A/r['snapshot_path'],r)
for r in read(P/'FROZEN_INPUTS.json')['records']:check(A/r['path'],r)
ag=read(P/'FROZEN_INPUTS.json')['workspace_AGENTS'];check(Path(ag['path']),ag)
native=read(A/'publication/zenodo-deposit.json');meta=read(P/'metadata.json')
need(set(native)=={'metadata','files'} and native['metadata']==meta==read(P/'metadata_wrapped.json')['metadata']==read(P/'deposit.json')['metadata'],'Native exact metadata object')
need(native['files']==[{'path':'../NEWpreprint_v1_0/paper.pdf','name':'paper.pdf'},{'path':'../NEWpreprint_v1_0/PR1071_preprint_v1_0_support.zip','name':'PR1071_preprint_v1_0_support.zip'}],'Native assets')
need(read(D/'INDEPENDENT_CHECKS_NORMAL.json')==read(D/'INDEPENDENT_CHECKS_OPTIMIZED.json'),'New exact math differs under -O')
dump('CUSTODY_RECHECK.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','counts':counts,'stage_counts':stagecounts,'historical_rows':verified,'all_historical_rows':len(verified),'source_copy_pairs':copyrows,'original_116_rows_exact_and_ordered':True,'individual_omissions':omissions,'native_metadata_exact_objects_equal':True,'native_assets_exact':True,'nine_originals_exact':True,'workspace_AGENTS_exact':True,'new_math_both_modes_exact_equal':True,'omitted_historical_program_replay_claim':False})
print(json.dumps({'status':'PASS','historical_rows':len(verified),'copies':len(copyrows),'individual_omissions':len(omissions),'counts':counts},indent=2))
