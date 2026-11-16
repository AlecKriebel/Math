#!/usr/bin/env python3
"""Explicit local metadata freeze; default is inert. No native/science execution."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

A = Path(__file__).resolve().parent
TERMINALS = ['FINAL_CLOSURE.json', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json']

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(path):
    body = path.read_bytes()
    return {'path': str(path.relative_to(A)), 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def put(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    if sys.argv[1:] != ['--freeze']:
        print('Inert default. Explicit --freeze required for new local terminal controls.')
        return
    for name in TERMINALS:
        if (A/name).exists():
            raise ValueError('refuse a prior terminal; preserve failed first attempt without overwrite')
    started = utc()
    with (A/'RESEARCH_LOG.md').open('a') as log:
        log.write('\n'+started+' — 95%: all science/copy artifacts complete, current standalone custody and finalizer bodies fully read; only finite metadata closure and terminal seal remain. Final100% checkpoint will be literal in FINAL_CLOSURE/FINAL_SEAL. Root140 CLOSED, findings withheld.\n')
    for name in TERMINALS:
        put(A/name, {'status':'PRESEAL_EXISTING_EXACT_ROOT_TERMINAL', 'UTC':started})
    files = []
    dirs = []
    for path in sorted(A.rglob('*')):
        if path.is_symlink():
            raise ValueError('symlink in owned namespace')
        if path.is_dir():
            dirs.append(path.relative_to(A).as_posix())
        elif path.is_file() and path.relative_to(A).as_posix() not in TERMINALS:
            files.append(pin(path))
        elif not path.is_file():
            raise ValueError('nonregular owned item')
    put(A/'FINAL_MANIFEST.json', {'schema':'row140-scope-finite-namespace-manifest-v1', 'UTC':started,
        'owned_root':str(A), 'exact_root_terminal_exclusions':TERMINALS,
        'files':files, 'directories':dirs, 'payload_count':len(files), 'directory_count':len(dirs),
        'no_basename_cache_directory_or_future_file_exclusions':True})
    runs = []
    for optimization in (False, True):
        argv = [sys.executable, '-B'] + (['-O'] if optimization else []) + [str(A/'verify_custody.py'),'--preseal']
        begin = utc()
        process = subprocess.run(argv, cwd=A, capture_output=True)
        runs.append({'started_UTC':begin, 'completed_UTC':utc(), 'argv':argv,
            'exit':process.returncode, 'stdout':process.stdout.decode('utf-8'),
            'stderr':process.stderr.decode('utf-8'), 'stdout_bytes':len(process.stdout),
            'stdout_SHA256':hashlib.sha256(process.stdout).hexdigest(),
            'stderr_bytes':len(process.stderr), 'stderr_SHA256':hashlib.sha256(process.stderr).hexdigest()})
        put(A/'FINAL_CLOSURE.json', {'status':'PRESEAL_EXECUTION_HISTORY', 'UTC':utc(), 'runs':runs})
        if process.returncode or process.stderr:
            raise RuntimeError('first exact closure failure preserved in terminal; no automatic repair or rerun')
    closure = {'schema':'row140-scope-actual-preseal-custody-closure-v1', 'UTC':utc(),
        'status':'BOTH_ACTUAL_PRESEAL_CUSTODY_RUNS_PASS', 'runs':runs,
        'whole_current_helper':pin(A/'verify_custody.py'), 'whole_finalizer':pin(A/'finalize_packet.py'),
        'entire_actual_current_bodies_read_before_execution':True,
        'scientific_programmes_imported_or_executed':[], 'source_or_core_programmes_executed':[],
        'network_subprocess_writes_on_custody_default':False,
        'preseal_flag_not_misrepresented_as_postseal_default':True,
        'postseal_default_normal_O_must_be_run_readonly_and_recorded_by_observer_outside_immutable_namespace':True,
        'research_checkpoint':{'UTC':utc(), 'completion_percent':100, 'root140_gate':'CLOSED','scientific_findings_shared':False}}
    put(A/'FINAL_CLOSURE.json', closure)
    seal = {'schema':'row140-scope-final-seal-v1', 'UTC':utc(), 'status':'FINAL_SEALED',
        'record_id':23133607, 'sheet_row':140,
        'MANIFEST_SHA256':pin(A/'FINAL_MANIFEST.json')['SHA256'],
        'CLOSURE_SHA256':pin(A/'FINAL_CLOSURE.json')['SHA256'],
        'owned_payload_count':len(files), 'actual_file_count':len(files)+3,
        'owned_directory_count':len(dirs), 'exact_root_terminal_exclusions':TERMINALS,
        'only_existing_exact_root_terminals_excluded':True, 'all_owned_files_and_directories_closed':True,
        'whole_original_source_files':97, 'whole_original_source_directories':9,
        'PDF_pages':4, 'controlling_TeX_lines':267, 'whole_ZIP_regular_occurrences':33,
        'INITIAL_SHA256':'92959fdf51fa0d58b9b782d00d9a38ab12ec7c3a106902d05210bd40712ec73b',
        'OWN_RESULTS_SHA256':'c734a8a17fcee7452fef17cb62ccd8e35bff81f97eff7dd16c0fe036465eeecd',
        'PRIMARY_PROOF_SHA256':'8f99749866e048aec957810a6d11cd5fcc43970d44a06fa82731917d10ced620',
        'qualified_core_originals':17, 'separately_authorized405b_checkpoint':True,
        'generated_caches_opaque_no_immutability_claim':True,
        'source_native_scientific_programmes_imported_or_executed':[],
        'actual_preseal_normal_O_both_exit_zero_empty_stderr':True,
        'current_helper_full_body_read_before_execution':True,
        'immutable_after_this_seal':True, 'completion_percent':100,
        'root140_gate':'CLOSED', 'scientific_findings_sent_to_root_or_peer':False,
        'followup':None, 'publication_authority':False, 'canonical_url':None, 'AA':None,
        'source_core_prior_packets_site_Git_Sheet_deploy_redirect_contact_mutations':False}
    put(A/'FINAL_SEAL.json', seal)
    for name in TERMINALS:
        print(json.dumps(pin(A/name)))

if __name__ == '__main__':
    main()
