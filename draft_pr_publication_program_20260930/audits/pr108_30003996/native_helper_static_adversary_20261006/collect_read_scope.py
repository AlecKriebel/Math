#!/usr/bin/env python3
"""Bounded read-only source receipts. Writes only this review packet."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
O = Path(__file__).resolve().parent
A = O.parent
C = A.parents[2]
D = A / 'native_publication_integration_plan_20261006'
BASE = '1026e5ff3cc3ff5b39501bd1f7218e773730c51a'
P = 'unsolved_math_prioritization/'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
records = []
source_pins = []
def read(path, semantic_scope):
    b=path.read_bytes()
    source_pins.append({'path': str(path), **pin(b), 'read_scope': semantic_scope})
    return b
def git(args, save=None):
    started=utc()
    process=subprocess.Popen(['/usr/bin/git', *args], cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try: out, err=process.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        process.kill(); out,err=process.communicate()
        raise RuntimeError('Bounded read-only Git timed out')
    record={'argv':['/usr/bin/git',*args], 'cwd':str(C), 'PID':process.pid,
            'UTC_start':started, 'UTC_end':utc(), 'exit_code':process.returncode,
            'stdout':pin(out), 'stderr':pin(err), 'stdout_retained':save}
    records.append(record)
    if process.returncode: raise RuntimeError(err.decode(errors='replace'))
    if save:
        p=O/save; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(out)
    return out
head=git(['rev-parse','HEAD'],'read_receipts/HEAD.txt').decode().strip()
branch=git(['symbolic-ref','--short','HEAD'],'read_receipts/BRANCH.txt').decode().strip()
if branch!='main': raise RuntimeError('Source checkout branch changed; refresh scope')
native_parent_diff=git(['diff','--name-only',BASE,head,'--',P], 'read_receipts/NATIVE_PARENT_DIFF.txt')
if native_parent_diff: raise RuntimeError('Native source changed after frozen source parent; refresh scope')
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl',
       'assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
tree=git(['ls-tree','-l',BASE,'--',*[P+n for n in names]],'read_receipts/NATIVE_TREE.txt')
native={}
for name in names:
    b=git(['show',BASE+':'+P+name], 'read_receipts/queue.py' if name=='queue.py' else None)
    source_pins.append({'git_commit':BASE,'path':P+name,**pin(b),
                        'read_scope':'complete source semantics' if name=='queue.py' else
                        'complete byte hash; structured target/projection/sizing inspection only'})
    native[name]=b
rows=json.loads(native['catalog.json']); states=json.loads(native['state.json']); assessments=json.loads(native['assessments.json'])
K='30003996'
target=next(x for x in rows if x['id']==K)
stale=[{'id':x['id'],'catalog_status':x['local_status'],'state_status':states[x['id']].get('status'),
        'catalog_turns':x['turns_used'],'state_turns':states[x['id']].get('turns_used',0)}
       for x in rows if x['id']!=K and x['id'] in states and
       (x['local_status']!=states[x['id']].get('status') or x['turns_used']!=states[x['id']].get('turns_used',0))]
for name in ['PLAN.md','prepare_review_bundle.py','test_review_bundle.py','run_offline_checks.py',
             'CONFIG_TEMPLATE_DO_NOT_RUN.json','ROOT_GATE_TEMPLATE_DO_NOT_USE_AS_EVIDENCE.json',
             'AFFECTED_PATH_RULES.json','OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','TASK_COMPLETION.json',
             'CONTEXT_SNAPSHOT.json','CONTEXT_INPUT_MANIFEST.json','OFFLINE_FIXTURE_RESULTS.json']:
    read(D/name,'complete body or structured byte-binding check')
writer_manifest=json.loads((D/'OUTPUT_MANIFEST.json').read_bytes())
seal=json.loads((D/'SEAL_RECEIPT.json').read_bytes())
manifest_check=[]
for entry in writer_manifest['files']:
    actual=pin((D/entry['path']).read_bytes())
    if actual != {k:entry[k] for k in ['bytes','sha256']}:
        raise RuntimeError('Writer seal changed: '+entry['path'])
    manifest_check.append({'path':entry['path'], **actual})
if pin((D/'OUTPUT_MANIFEST.json').read_bytes()) != {k:seal['output_manifest_pin'][k] for k in ['bytes','sha256']}:
    raise RuntimeError('Writer output manifest seal binding changed')
math=json.loads(read(A/'ROOT_MATHEMATICAL_GATE_20261006.json','complete structured gate body'))
priority=json.loads(read(A/'ROOT_PRIORITY_GATE_20261006.json','complete structured gate body'))
authroot=A/'original_source_authentication_20261006'
auth=json.loads(read(authroot/'ORIGINAL_BLOB_MANIFEST.json','complete body and all original file pins'))
qauth=json.loads(read(authroot/'QUEUE_STATUS_PROJECTION.json','complete body and current original row pin'))
read(authroot/'SOURCEPAIR_AUTHENTICATION.json','complete body; historical receipt interpreted as dated')
prior=read(authroot/'SELECTED_IMPORTED_PRIOR_REPORT.json','complete bytes and JSON object')
read(authroot/'original_attempt/source_manifest.json','complete body')
read(authroot/'original_attempt/RESEARCH_LOG.md','complete historical prose effort')
original_bytes=[]
for entry in auth['files']:
    b=read(authroot/'original_attempt'/entry['relative_path'],'complete byte pin; not new mathematical proof review')
    if pin(b)!={k:entry[k] for k in ['bytes','sha256']} or entry['path']!=P+'attempts/'+K+'/'+entry['relative_path']:
        raise RuntimeError('Current original inventory byte/path map mismatch')
    blob=git(['show',auth['source_head']+':'+entry['path']])
    if blob!=b: raise RuntimeError('Original source-head byte mismatch')
    original_bytes.append(entry['relative_path'])
queue_orig=git(['show',auth['source_head']+':'+P+'QUEUE.md'])
if pin(queue_orig)!={'bytes':qauth['whole_QUEUE_bytes'],'sha256':qauth['whole_QUEUE_sha256']}:
    raise RuntimeError('Original queue full pin mismatch')
if hashlib.sha256(qauth['selected_row'].encode()).hexdigest()!=qauth['selected_row_sha256'] or queue_orig.decode().splitlines().count(qauth['selected_row'])!=1:
    raise RuntimeError('Current selected original row pin mismatch')
scope={'schema':'pr108-native-helper-static-source-read-scope/v1','UTC':utc(),'actual_operator_PID':os.getpid(),
       'frozen_native_source_parent':BASE,'isolated_main_parent_observed_during_collection':head,
       'native_source_parent_to_observed_head_diff_empty':not native_parent_diff,'branch':branch,
       'sealed_writer_manifest_file_count_verified':len(manifest_check),
       'writer_seal_verified':True,'writer_helper_pin':pin((D/'prepare_review_bundle.py').read_bytes()),
       'source_pins':source_pins,'original_native_inventory_verified':original_bytes,
       'original_imported_report_bytes':prior.decode(),'original_imported_report_is_empty_object':json.loads(prior)=={},
       'current_target_catalog':target,'current_target_state_present':K in states,
       'current_target_assessment':assessments[K], 'current_summary':json.loads(native['summary.json']),
       'current_stale_unrelated_projection_count':len(stale),'current_stale_unrelated_projections':stale,
       'current_csv_extra_splitlines_characters':{hex(ord(c)):native['ranking.csv'].decode().count(c)
         for c in '\v\f\x1c\x1d\x1e\x85\u2028\u2029' if c in native['ranking.csv'].decode()},
       'current_campaign_selected_row':[x for x in native['QUEUE.md'].decode().splitlines() if '| '+K+' / OWR-16633-013 |' in x],
       'current_shortlist_target_present':('## '+K+' —').encode() in native['SHORTLIST.md'],
       'capacity_native_baseline_total_bytes':sum(map(len,native.values())),
       'helper_minimum_capacity_without_package_bytes':3*sum(map(len,native.values()))+1024*1024,
       'filesystem_free_bytes_observed':os.statvfs(O).f_bavail*os.statvfs(O).f_frsize,
       'mathematical_gate_summary':{k:math.get(k) for k in ['UTC','mathematical_clearance','current_effective_proof_sha256','new_central_proof_search_turns']},
       'priority_gate_summary':{k:priority.get(k) for k in ['UTC','priority_audit_percent','priority_clearance_for_scoped_note_preparation',
          'substantive_novel_resolution_supported','proof_note_preparation_authorized','publication_package_ready',
          'whole_package_review_completed','publication_clearance','disposition']},
       'prohibited_real_native_prepare_assess_export_Git_mutation_service_or_cache_write_executed':False,
       'earlier_root_unscoped_status_excluded':True}
(O/'SOURCE_READ_SCOPE.json').write_text(json.dumps(scope,indent=2,ensure_ascii=False)+'\n')
(O/'READ_PROCESS_JOURNAL.json').write_text(json.dumps({'UTC':utc(),'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
(O/'WRITER_SEAL_VERIFICATION.json').write_text(json.dumps({'UTC':utc(),'actual_operator_PID':os.getpid(),'all_79_writer_files_verified':True,
       'writer_seal':seal,'verified_files':manifest_check},indent=2)+'\n')
print(json.dumps({'HEAD':head,'operator_PID':os.getpid(),'writer_file_count':len(manifest_check),
                   'stale_unrelated_rows':len(stale),'min_capacity_bytes':scope['helper_minimum_capacity_without_package_bytes'],
                   'filesystem_free_bytes':scope['filesystem_free_bytes_observed']}))
