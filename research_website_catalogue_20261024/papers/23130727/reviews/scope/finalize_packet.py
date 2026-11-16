#!/usr/bin/env python3
"""Explicit new local metadata freeze. Default inert; no scientific programme.
Runs only the fully read new pure custody helper, never native/source campaigns.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

A = Path(__file__).resolve().parent
T = ['FINAL_CLOSURE.json','FINAL_MANIFEST.json','FINAL_SEAL.json']

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(p):
    b = p.read_bytes()
    return {'path':p.relative_to(A).as_posix(),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def put(name, obj):
    (A/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
    if sys.argv[1:] != ['--freeze']:
        print('Inert default; explicit --freeze required for new local terminal controls.')
        return
    if any((A/n).exists() for n in T):
        raise ValueError('refuse existing terminals; preserve any failed first attempt')
    start = utc()
    with (A/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+start+' —95%: substantive review and exact histories complete; current full pure-helper/finalizer bodies read before execution. Final metadata runs and100% terminal checkpoint follow. Root141 CLOSED; no findings sent.\n')
    for name in T:
        put(name,{'status':'EXISTING_EXACT_ROOT_PRESEAL_CONTROL','UTC':start})
    files,dirs = [],[]
    for p in A.rglob('*'):
        if p.is_symlink():
            raise ValueError('symlink in owned namespace')
        if p.is_dir():
            dirs.append(p.relative_to(A).as_posix())
        elif p.is_file():
            if p.relative_to(A).as_posix() not in T:
                files.append(pin(p))
        else:
            raise ValueError('nonregular owned item')
    files.sort(key=lambda r:r['path'])
    dirs.sort()
    put('FINAL_MANIFEST.json',{'schema':'row141-scope-finite-manifest-v1','UTC':start,'owned_root':str(A),
        'exact_root_terminal_exclusions':T,'files':files,'directories':dirs,
        'payload_count':len(files),'directory_count':len(dirs),'no_basename_cache_or_future_carveouts':True})
    runs=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for optimize in (False,True):
        argv=[sys.executable,'-B']+(['-O'] if optimize else [])+[str(A/'verify_custody.py'),'--preseal']
        begin=utc()
        r=subprocess.run(argv,cwd=A,env=env,capture_output=True)
        runs.append({'started_UTC':begin,'completed_UTC':utc(),'argv':argv,'exit':r.returncode,
            'stdout':r.stdout.decode('utf-8'),'stderr':r.stderr.decode('utf-8'),
            'stdout_bytes':len(r.stdout),'stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),
            'stderr_bytes':len(r.stderr),'stderr_SHA256':hashlib.sha256(r.stderr).hexdigest()})
        put('FINAL_CLOSURE.json',{'status':'ACTUAL_PRESEAL_ATTEMPT_HISTORY','UTC':utc(),'runs':runs})
        if r.returncode or r.stderr:
            raise RuntimeError('exact first failure preserved; stop without automatic replay')
    put('FINAL_CLOSURE.json',{'schema':'row141-scope-actual-custody-closure-v1','UTC':utc(),
        'status':'ACTUAL_NORMAL_O_PRESEAL_CUSTODY_BOTH_PASS','runs':runs,
        'whole_current_helper':pin(A/'verify_custody.py'),'whole_current_finalizer':pin(A/'finalize_packet.py'),
        'entire_actual_current_bodies_read_before_execution':True,'native_or_scientific_programmes_executed':[],
        'default_custody_network_subprocess_writes_scientific_execution':False,
        'actual_preseal_not_misrepresented_as_postseal_default':True,
        'postseal_defaults_observed_separately_without_writing_immutable_namespace':True,
        'research_checkpoint':{'UTC':utc(),'completion_percent':100,'root141_gate':'CLOSED','findings_shared':False}})
    put('FINAL_SEAL.json',{'schema':'row141-scope-final-seal-v1','UTC':utc(),'status':'FINAL_SEALED',
        'record_id':23130727,'sheet_row':141,'MANIFEST_SHA256':pin(A/'FINAL_MANIFEST.json')['SHA256'],
        'CLOSURE_SHA256':pin(A/'FINAL_CLOSURE.json')['SHA256'],'owned_payload_count':len(files),
        'actual_file_count':len(files)+3,'owned_directory_count':len(dirs),'exact_root_terminal_exclusions':T,
        'only_existing_exact_root_terminals_excluded':True,'all_owned_files_and_directories_closed':True,
        'whole_original_source_files':128,'whole_original_source_directories':18,'PDF_pages':3,'controlling_TeX_lines':229,
        'whole_ZIP_regular_occurrences':69,'external_raw_bodies_byreference':6,'fresh_primary_GETs':0,
        'INITIAL_SHA256':'fdc72cc386c1024956de533e3de5b0247de96ec9e129c3d722f584407bc51365',
        'OWN_RESULTS_SHA256':'e6de783d93556cfb08579f69338a0a85983a4c0f1d0a9ac9d74c40965b6d5fac',
        'PRIMARY_PROOF_SHA256':'3d33f32ba107f3800ab48720603b3fca5df5a431caff983e0b1c5ce41a64cde6',
        'qualified_original_core_files':17,'sole_authorized405b_checkpoint':True,'generated_caches_opaque_no_immutability_claim':True,
        'current_helper_full_body_read_before_execution':True,'actual_preseal_normal_O_exit0_empty_stderr':True,
        'source_or_native_scientific_programmes_imported_or_executed':[],'completion_percent':100,'immutable_after_this_seal':True,
        'root141_gate':'CLOSED','scientific_findings_sent_to_root_or_peer':False,'followup':None,
        'publication_authority':False,'canonical_url':None,'AA':None,
        'by_this_lane_source_core_prior_packets_site_Git_Sheet_deploy_redirect_contact_mutations':False})
    for name in T:
        print(json.dumps(pin(A/name)))

if __name__ == '__main__':
    main()
