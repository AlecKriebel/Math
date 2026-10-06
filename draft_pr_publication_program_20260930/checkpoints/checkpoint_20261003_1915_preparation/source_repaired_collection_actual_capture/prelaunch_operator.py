"""Collect exact completed files in place; no Git, copies of corpora, or native writes."""
import os, stat
from pathlib import Path
from common import *
from selection import *
P = R / 'draft_pr_publication_program_20260930'
fixed, directories = {}, {}
def addfile(q):
    row=plain_ref(q)
    need(row['path'] not in fixed or fixed[row['path']]==row,'Different duplicate')
    fixed[row['path']]=row;return row
def complete(q):
    need(q.is_dir() and not q.is_symlink(),'Whole regular selected directory')
    rows=[]
    for v in [q]+sorted(q.rglob('*')):
        need(not v.is_symlink(),'No selected symlink')
        s=v.lstat()
        if stat.S_ISDIR(s.st_mode):
            name=str(v.relative_to(R));directories[name]=dict(path=name,full_mode=stat.S_IMODE(s.st_mode))
        else:rows.append(addfile(v))
    return rows
def mode(v):return int(v,8) if isinstance(v,str) else v
def indexed(q,marker,sha,extras):
    m=q/marker;need(digest(m.read_bytes())==sha,'Exact existing family index')
    j=load(m);declared=set()
    for z in j['files']:
        rel=Path(z['path']);need(not rel.is_absolute() and '..' not in rel.parts,'Family-relative indexed member')
        f=q/rel;declared.add(f);a=plain_ref(f)
        need(a['bytes']==z['bytes'] and a['sha256']==z['sha256'],'Indexed complete body')
        v=z.get('full_mode_07777',z.get('full_mode',z.get('mode')))
        if v is None:
            modes=j.get('file_modes',{})
            if isinstance(modes,list):modes={r['path']:r['full_mode'] for r in modes}
            v=modes.get(z['path'])
        need(v is not None and a['full_mode']==mode(v),'Indexed full07777 mode')
    actual={f for f in q.rglob('*') if f.is_file()}
    need(actual-declared=={m}|{q/v for v in extras},'Literal index/self/READY/ROOT closure exclusions only')
    return plain_ref(m)
def streams(q,j):
    for key in ['stdout','stderr']:
        a=plain_ref(q/(key+'.bin'));need(a['bytes']==j[key]['bytes'] and a['sha256']==j[key]['sha256'],'Whole actual retained stream')
def ownpaths():
    rows={str(q.relative_to(R)) for q in N.rglob('*') if q.is_file() and q.name!='RESEARCH_LOG.md'
          and EXCLUDED_READBACK_ROOT not in q.relative_to(N).parts}
    # The current administrative collector's controller writes these actual
    # stream/metadata files only after the child returns. READY later requires
    # every one to exist and validates their real bodies and exit status.
    for q in N.glob('source_*_actual_capture'):
        if q.name=='source_derivation_actual_capture':continue
        rows|={str((q/n).relative_to(R)) for n in ['CAPTURE.json','prelaunch_operator.py','prelaunch_common.py','stdout.bin','stderr.bin']}
    rows|={str((N/n).relative_to(R)) for n in ['SCOPE_PREVERIFICATION.json','SCOPE.json','SOURCE_READY.json','SOURCE_VERIFICATION.json']}
    return sorted(rows)
def main():
    start=now();final=(N/'SOURCE_VERIFICATION.json').exists()
    if final:need(load(N/'SOURCE_VERIFICATION.json')['status']=='PASS_READONLY_SOURCE_CHECKS','Actual earlier administrative consistency required')
    families=[]
    for rel,count,marker,sha,extras in FAMILIES:
        q=P/rel;idx=indexed(q,marker,sha,extras);rows=complete(q)
        need(len(rows)==count,'Exact completed family count')
        families.append(dict(root=str(q.relative_to(R)),files=count,bytes=sum(z['bytes'] for z in rows),exact_existing_index=idx,
                             custody='Existing completed ROOT closure/readback retained; this collector supplies no new ROOT review or math credit'))
    outside=[addfile(P/n) for n in ROOT_FILES]
    extra=[]
    for rel,count,role in EXTRA_DIRECTORIES:
        q=P/rel;rows=complete(q);need(len(rows)==count,'Exact observed runtime/readback topology')
        extra.append(dict(root=str(q.relative_to(R)),files=count,bytes=sum(z['bytes'] for z in rows),role=role))
    caps=[]
    for rel,pid,exit_code in CAPS:
        q=P/rel;j=load(q/'CAPTURE.json');rows=complete(q)
        need({Path(z['path']).name for z in rows}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Whole CAP4')
        need(j['pid']==pid and j['exit_code']==exit_code and j['actual_execution'] and j['completed'] and j['operator_unchanged'],'Actual completed historical operation')
        need(j['status']==('PASS' if exit_code==0 else 'FAIL'),'Retain actual success/failure')
        need(digest((q/'prelaunch_operator.py').read_bytes())==j['operator_sha256'],'Full prelaunch operator body')
        streams(q,j);caps.append(dict(root=str(q.relative_to(R)),actual_pid=pid,exit_code=exit_code,status=j['status'],
              started_utc=j['started_utc'],finished_utc=j['finished_utc'],metadata=plain_ref(q/'CAPTURE.json'),new_checkpoint_ROOT_authority=False))
    inner=P/'audits/pr48_2961/root_finalize_actual_capture';j=load(inner/'CAPTURE.json')
    need(j['pid']==80480 and j['exit_code']==1 and j['status']=='FAIL' and j['completed'] and j['actual_execution'],'Actual failed inner operation')
    streams(inner,j)
    need(digest((inner/'PRELAUNCH_OPERATOR.py').read_bytes())==j['operator_sha256'],'Inner prelaunch wrapper body')
    need(digest((inner/'PRELAUNCH_SOURCE.py').read_bytes())==j['source_sha256'],'Inner prelaunch source body')
    install=load(P/'audits/pr45_9900007/root_pr48_v6_exact_source_install_actual_capture/stdout.bin')
    need(install['actual_pid']==79256 and len(install['files'])==5 and install['status']=='PASS_EXACT_ROOT_V6_SOURCE_INSTALL_ONLY','Actual five-file source installation')
    for z in install['files']:need(plain_ref(path(z['path']))==z and z['path'] in fixed,'All exact installed bodies/current full modes')
    pins={
      'audits/pr61_2725/ROOT_SCIENTIFIC_ADJUDICATION_20261003.json':'99a48b3c7236057a4abddc3112fd0e257d71e73e8d8d0d08c5dd39c0be39fdff',
      'audits/pr60_10300054/ROOT_CURRENT_PREPARATION_CLOSE_20261003.json':'5f9049da0c7447eafa56a8361c35c61a6dfb794dce95537a4db1b20789a19d40',
      'audits/pr48_2961/ROOT_POST_PUSH_V6_FINALIZE_FOREIGN_EPOCH.json':'6113e350091c2e408157425a2257f9947b0007c80b33ea642e31f19d92858c34',
      'storage_compression_20261003/ROOT_CHECKPOINT_20261003_READBACK_AND_PREVIEW_CLEANUP.json':'3e948708e3d2ba2161c5ad2a6e5c6aae356b91e81702d372070faa6f1e996722',
      'audits/pr61_2725/ROOT_RESEARCH_LOG.md':'69bc1b71d399e1adfa6f086751bdd36daf9639adad39a419ebd2e8f021091ef9'}
    for n,sha in pins.items():need(digest((P/n).read_bytes())==sha,'Exact authorized outside record/log body')
    forbidden=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/catalog.json','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.json']
    forbidden += [str((P/n).relative_to(R)) for n in ['inventory.json','review_state.json','review_history.json','RESEARCH_LOG.md','audits/pr48_2961/ROOT_RESEARCH_LOG.md']]
    need(not set(fixed)&set(forbidden),'No live shared/native path')
    scope=dict(schema='ROOT-exact-owned-research-checkpoint-scope/v1',source_only=True,prepared_utc=now(),started_utc=start,actual_collector_pid=os.getpid(),
      fixed_files=[fixed[k] for k in sorted(fixed)],fixed_directories=[directories[k] for k in sorted(directories)],completed_fixed_families=families,
      outside_actual_ROOT_records_and_installed_sources=outside,completed_extra_directories=extra,actual_ROOT_CAP4_sets=caps,
      actual_failed_inner_capture=dict(actual_pid=80480,files=11,exit_code=1,status='FAIL',metadata=plain_ref(inner/'CAPTURE.json')),
      ROOT_log_marker_suffix=ROOT_LOG_MARKER_SUFFIX,runtime_stamped_log_paths=[str((N/'RESEARCH_LOG.md').relative_to(R))],
      new_preparation_source_paths=ownpaths(),forbidden_native_paths=forbidden,
      excluded_future_output_roots=[str((N/EXCLUDED_READBACK_ROOT).relative_to(R)),'Own future actual_run_* directories; no completed run is claimed'],
      exclusions=['active PR48 rollback/preparer/reviewer','active PR49 and PR61 current SOURCE','live A48 remote_merge/integration_finalization/acceptance and selected native canonical PR48','program inventory/QUEUE/state/history/shared logs','raw corpus/private primary PDFs/cache/index/reconciled-index bodies'],
      formal_completed_acceptance=FORMAL_INVENTORY,formal_completed_percent=20.5556,partial_inventory38_is_not_completed_acceptance=True,
      mathematical_discovery_changed=False,ROOT_review_of_this_SOURCE_not_claimed=True,stage_commit_push_executed=False,native_acceptance_changed=False,
      qualification='Current literal full07777 modes are pinned without altering dated historical mode fields. Stored primary/theorem/ROOT claims retain their original limits; this is administrative custody, not fresh mathematical validation.')
    target=N/('SCOPE.json' if final else 'SCOPE_PREVERIFICATION.json');exclusive(target,encoded(scope))
    print(encoded(dict(status='PREPARED_EXACT_SOURCE_SCOPE_ONLY',scope=plain_ref(target),actual_pid=os.getpid(),final_scope=final,
      fixed_files=len(fixed),fixed_directories=len(directories),selected_bytes=sum(z['bytes'] for z in fixed.values()),
      whole_families=len(families),CAP4_sets=len(caps),inner_failed_capture_files=11,storage_readback_files=12)).decode(),end='')
if __name__=='__main__':main()
