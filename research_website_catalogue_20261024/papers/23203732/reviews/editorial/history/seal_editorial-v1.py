#!/usr/bin/env python3
"""Close this owned editorial packet; invoke only the new read-only guard.
No native/scientific/build/network/Git/Sheet/website action or outside writes.
"""
from pathlib import Path
import base64,datetime,hashlib,json,os,stat,subprocess,sys
R=Path(__file__).absolute().parent
TERMS={'OWNED_MANIFEST.json','CLOSURE.json','FINAL_SEAL.json'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def bind(p):return {'path':str(p),**pin(p.read_bytes())}
def write(n,v,exclusive=False):
    with (R/n).open('x' if exclusive else 'w') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n');f.flush();os.fsync(f.fileno())
def extent():
    files=[];dirs=[]
    def visit(d):
        for p in sorted(d.iterdir()):
            mode=p.lstat().st_mode;rel=p.relative_to(R).as_posix()
            if stat.S_ISDIR(mode):dirs.append(rel);visit(p)
            elif stat.S_ISREG(mode):
                if rel not in TERMS:files.append({'path':rel,**pin(p.read_bytes())})
            else:raise ValueError('symlink/FIFO/special '+rel)
    for n in TERMS:
        if not stat.S_ISREG((R/n).lstat().st_mode):raise ValueError('terminal must already be ordinary')
    visit(R);return sorted(files,key=lambda x:x['path']),sorted(dirs)
def main():
    if any((R/n).exists() for n in TERMS):raise ValueError('retain earlier finalization/failure history')
    for n in ['REPORT.md','VERDICT.json','CURRENT_CODE_READS.json','EXECUTION_RECEIPTS.json']:
        if not (R/n).is_file():raise ValueError('missing required final payload '+n)
    with (R/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — 100% editorial preparation: full source-faithful copy/config/readers/head/Bib ready; actual strict default normal/O finalization follows. Root copy adoption, independent fact audit, production installation and live verification remain separate.\n')
    write('OWNED_MANIFEST.json',{'status':'MANIFEST_IN_PROGRESS'},True)
    write('CLOSURE.json',{'status':'ACTUAL_DEFAULTS_PENDING'},True)
    write('FINAL_SEAL.json',{'status':'FINALIZATION_IN_PROGRESS','immutable':False},True)
    files,dirs=extent();manifest={'UTC':utc(),'owned_root':str(R),'files':files,'directories':dirs,'payload_count':len(files),'directory_count':len(dirs),'exact_root_terminal_exclusions':sorted(TERMS),'all_terminals_already_ordinary_files':True,'no_directory_basename_future_run_or_cache_exclusions':True}
    write('OWNED_MANIFEST.json',manifest)
    runs=[]
    for label,flags in [('normal',[]),('optimized',['-O'])]:
        argv=[sys.executable,'-I','-B',*flags,str(R/'verify_editorial.py')];start=utc();r=subprocess.run(argv,cwd=R,capture_output=True)
        runs.append({'label':label,'argv':argv,'started_UTC':start,'completed_UTC':utc(),'exit_code':r.returncode,'stdout':{**pin(r.stdout),'base64':base64.b64encode(r.stdout).decode(),'literal_UTF8':r.stdout.decode(errors='replace')},'stderr':{**pin(r.stderr),'base64':base64.b64encode(r.stderr).decode(),'literal_UTF8':r.stderr.decode(errors='replace')}})
        if r.returncode or r.stderr:
            write('CLOSURE.json',{'status':'FAILED_FINALIZATION_HISTORY_RETAINED','runs':runs});raise ValueError('read-only guard failed; no final seal')
    if extent()!=(files,dirs):raise ValueError('payload mutation during closure')
    write('CLOSURE.json',{'UTC':utc(),'status':'ACTUAL_NORMAL_O_DEFAULTS_PASS','runs':runs,'whole_actual_streams_retained':True,'phase_qualification':'These saved actual defaults closed the final payload/declared directory namespace while all three root controls already existed, before final seal binding. Their final_seal_bound:false is literal. Direct final defaults follow final binding without packet writes.','normal_O_stdout_identical':runs[0]['stdout']['SHA256']==runs[1]['stdout']['SHA256'],'scientific_execution':False,'production_authority':False})
    write('FINAL_SEAL.json',{'UTC':utc(),'status':'EDITORIAL_PREPARATION_FINAL','record_id':23203732,'sheet_row':137,'manifest_SHA256':pin((R/'OWNED_MANIFEST.json').read_bytes())['SHA256'],'closure_SHA256':pin((R/'CLOSURE.json').read_bytes())['SHA256'],'payload_count':len(files),'actual_file_count':len(files)+3,'directory_count':len(dirs),'exact_root_terminals':sorted(TERMS),'all_files_and_directories_closed':True,'no_future_or_subtree_exclusions':True,'INITIAL':bind(R/'INITIAL.json'),'config':bind(R/'EDITORIAL_CONFIG.json'),'whole_copy':bind(R/'normal/COPY.md'),'whole_MAIN':bind(R/'normal/PUBLIC_MAIN.html'),'current_code_reads':bind(R/'CURRENT_CODE_READS.json'),'actual_saved_default_normal_O_exit_zero':True,'complete_original_source_peer_root_and_namedcore_preserved':True,'root_science_clearance_reference_only':True,'new_independent_scientific_verdict':None,'root_copy_adopted':False,'production_authority':False,'canonical_url':None,'AA':None,'follow_up':None,'immutable':True})
    if extent()!=(files,dirs):raise ValueError('postseal payload mutation')
    print(json.dumps({'status':'EDITORIAL_PREPARATION_FINAL','seal':bind(R/'FINAL_SEAL.json'),'manifest':bind(R/'OWNED_MANIFEST.json'),'payloads':len(files),'directories':len(dirs),'production_authority':False},sort_keys=True))
if __name__=='__main__':main()
