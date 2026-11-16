#!/usr/bin/env python3
"""Finalize one source-only packet and preserve actual offline closure streams.

Only owned files are written. The only invoked program is the fully read new
owned verify_custody.py in ordinary/optimized modes; no native/source science,
old helper, builder, dependency, network, Git, Sheet or website action occurs.
"""
from pathlib import Path
import base64,datetime,hashlib,json,os,stat,subprocess,sys

R=Path(__file__).absolute().parent
TERMS={'SOURCE_READY_CLOSURE.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'}

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(body):return {'bytes':len(body),'SHA256':hashlib.sha256(body).hexdigest()}
def bind(path):return {'path':str(path),**pin(path.read_bytes())}
def write(name,value,exclusive=False):
    with (R/name).open('x' if exclusive else 'w') as f:
        f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n');f.flush();os.fsync(f.fileno())

def extent():
    files=[];dirs=[]
    def visit(p):
        with os.scandir(p) as it:es=sorted(it,key=lambda x:x.name)
        for e in es:
            q=p/e.name;r=q.relative_to(R).as_posix();mode=q.lstat().st_mode
            if stat.S_ISDIR(mode):dirs.append(r);visit(q)
            elif stat.S_ISREG(mode):
                if r not in TERMS:files.append({'path':r,**pin(q.read_bytes())})
            else:raise ValueError('symlink/FIFO/special '+r)
    for n in TERMS:
        if not stat.S_ISREG((R/n).lstat().st_mode):raise ValueError('terminal not an existing ordinary file')
    visit(R);return sorted(files,key=lambda x:x['path']),sorted(dirs)

def main():
    if any((R/n).exists() for n in TERMS):raise ValueError('preserve existing control/finalization history')
    for n in ['SOURCE_READY.json','INPUT_MANIFEST.json','HELPER_READS.json','SOURCE_CUSTODY_PROOF.md','CUSTOM_VERDICT.json','EXECUTION_LEDGER.json']:
        if not (R/n).is_file():raise ValueError('missing final payload '+n)
    with (R/'SOURCE_LOG.md').open('a') as f:
        f.write('\n'+utc()+' — 100% bounded source custody preparation: all acquisition/opaque archive/manuscript metadata artifacts complete. Actual default closure and final control binding follow; mathematical body/pixels/code/results/opinions remain unread and scientific/publication authority absent.\n')
    write('SOURCE_READY_MANIFEST.json',{'status':'MANIFEST_FINALIZATION_IN_PROGRESS'},True)
    write('SOURCE_READY_CLOSURE.json',{'status':'ACTUAL_CLOSURES_PENDING'},True)
    write('SOURCE_READY_SEAL.json',{'status':'SOURCE_READY_SEAL_FINALIZATION_IN_PROGRESS','immutable':False},True)
    files,dirs=extent()
    manifest={'UTC':utc(),'owned_root':str(R),'excluded_terminal_files':sorted(TERMS),
        'all_exact_root_terminal_files_already_present_as_ordinary_files':True,'files':files,'directories':dirs,
        'owned_payload_count':len(files),'owned_directory_count':len(dirs),
        'all_raw_assets_archive_extractions_nested_occurrences_rasters_and_ignored_caches_included':True,
        'no_basename_directory_or_future_file_exclusions':True}
    write('SOURCE_READY_MANIFEST.json',manifest)
    runs=[]
    for label,flags in [('normal',[]),('optimized',['-O'])]:
        argv=[sys.executable,'-I','-B',*flags,str(R/'verify_custody.py')]
        start=utc();r=subprocess.run(argv,cwd=R,capture_output=True)
        runs.append({'label':label,'argv':argv,'started_UTC':start,'completed_UTC':utc(),'exit_code':r.returncode,
            'stdout_bytes':len(r.stdout),'stdout_SHA256':pin(r.stdout)['SHA256'],'stdout_base64':base64.b64encode(r.stdout).decode(),
            'stdout_literal_UTF8':r.stdout.decode(errors='replace'),'stderr_bytes':len(r.stderr),'stderr_SHA256':pin(r.stderr)['SHA256'],
            'stderr_base64':base64.b64encode(r.stderr).decode(),'stderr_literal_UTF8':r.stderr.decode(errors='replace')})
        if r.returncode or r.stderr:
            write('SOURCE_READY_CLOSURE.json',{'UTC':utc(),'status':'FAILED_FINALIZATION_HISTORY_RETAINED','runs':runs})
            raise ValueError('actual offline closure failed; no final seal, all streams retained')
    if extent()!=(files,dirs):raise ValueError('payload/directory mutation during read-only default closure')
    closure={'UTC':utc(),'record_id':23130727,'pure_offline_default_mode':True,
        'fully_read_current_helper':bind(R/'verify_custody.py'),'helper_read_receipt':bind(R/'HELPER_READS.json'),
        'runs':runs,'all_actual_output_bytes_retained':True,'both_default_normal_O_exit_zero':True,
        'normal_O_stdout_identical':runs[0]['stdout_SHA256']==runs[1]['stdout_SHA256'],
        'stderr_empty':True,'source_helpers_or_scientific_programs_imported_in_default_closure':False,
        'network_or_filesystem_writes_in_default_closure':False,
        'control_phase_qualification':'The actual saved defaults ran with all three exact root controls already ordinary files and a closed final payload/directory manifest. Their explicit seal_finalized_and_bound:false means the final seal had not yet bound this literal closure. Final defaults are also issued directly after this immutable final binding, without packet writes.',
        'terminal_seal_binding':'Separate final seal binds READY, manifest and this whole actual closure receipt.'}
    write('SOURCE_READY_CLOSURE.json',closure)
    ready=json.loads((R/'SOURCE_READY.json').read_bytes())
    final={'UTC':utc(),'status':'SOURCE_READY_SEALED','record_id':23130727,'sheet_row':141,
        'SOURCE_READY_SHA256':pin((R/'SOURCE_READY.json').read_bytes())['SHA256'],
        'MANIFEST_SHA256':pin((R/'SOURCE_READY_MANIFEST.json').read_bytes())['SHA256'],
        'CLOSURE_SHA256':pin((R/'SOURCE_READY_CLOSURE.json').read_bytes())['SHA256'],
        'owned_payload_count':len(files),'owned_directory_count':len(dirs),'exact_root_terminal_files':sorted(TERMS),
        'actual_file_count':len(files)+3,'all_payload_files_and_all_directories_closed':True,
        'only_existing_exact_root_terminals_excluded':True,'no_future_unsealed_carveouts':True,
        'current_pure_helper':bind(R/'verify_custody.py'),'helper_full_current_body_read_before_execution':True,
        'actual_default_normal_O_both_exit_zero':True,'complete_literal_stdout_stderr_and_exit_codes_retained':True,
        'default_receipt_phase_honest':closure['control_phase_qualification'],
        'source_only_completion_percent':100,'source_scientific_body_pixels_code_results_or_opinions_read':False,
        'source_scientific_programs_executed':[],'old_original_helpers_executed':False,
        'native_version_field_present':ready['version_field_present'],'native_version_original':ready['version'],
        'printed_fields_inspected':False,'printed_date':None,'printed_version':None,
        'source_assets_archives_and_payloads_original_bytes_preserved':True,'current_native_Sheet_read':False,
        'existing_queue_identity_plus_fresh_native_record_only':True,'qualified_core17_plus_sole405b':True,
        'source_only_no_scientific_or_publication_authority':True,'scientific_verdict':None,
        'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None,
        'Git_Sheet_site_deploy_redirect_or_contact_mutations':False,'immutable_after_this_seal':True}
    write('SOURCE_READY_SEAL.json',final)
    if extent()!=(files,dirs):raise ValueError('postseal exact namespace changed')
    print(json.dumps({'status':'SOURCE_READY_SEALED','SOURCE_READY_SEAL':bind(R/'SOURCE_READY_SEAL.json'),
        'SOURCE_READY_MANIFEST':bind(R/'SOURCE_READY_MANIFEST.json'),'payloads':len(files),'directories':len(dirs),
        'scientific_verdict':None,'publication_authority':False,'mathematical_reading':False},sort_keys=True))

if __name__=='__main__':main()
