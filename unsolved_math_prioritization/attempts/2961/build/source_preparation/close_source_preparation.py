"""ROOT-only source-family closure. Wait for a real external actual capture."""
import argparse, datetime as dt, hashlib, json, os, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent
SELF='PREPARATION_MANIFEST.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise ValueError(m)
def regular(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink file');return p.read_bytes()
def scan():
    files=[];dirs=[]
    for p in sorted(F.rglob('*')):
        require(not p.is_symlink(),'Symlink member');n=p.relative_to(F).as_posix()
        if p.is_file():
            if n!=SELF:b=regular(p);files.append({'path':n,'bytes':len(b),'sha256':sha(b)})
        else:require(stat.S_ISDIR(p.stat().st_mode),'Special member');dirs.append(n)
    expected={p.as_posix() for r in files for p in PurePosixPath(r['path']).parents if p.as_posix()!='.'};require(set(dirs)==expected,'Extra/empty directory');return files,dirs
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected-report-sha256',required=True);args=parser.parse_args();require(__debug__ and not sys.flags.optimize,'Unoptimized closure');require(F.name=='current_preparation_family' and F.parent.name=='pr48_2961','Exact source family');require(not (F/SELF).exists() and not (F/SELF).is_symlink(),'Never overwrite closure')
    require(sha(regular(F/'SOURCE_REPORT.md'))==args.expected_report_sha256,'Complete read report changed');files,dirs=scan()
    for r in files:(F/r['path']).chmod(0o444)
    m={'schema':'pr48-current-source-only-closure/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),'self_excluded':[SELF],'files_count':len(files),'files':files,'directories':[{'path':n,'full_mode':stat.S_IMODE((F/n).stat().st_mode)} for n in ['.']+dirs],'status':'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','production_builder_imported_compiled_or_executed':False,'ROOT_prerequisites_authored':False,'candidate_frozen':False,'future_acceptance_approved':False,'new_whole_current_gate':'PENDING','status_recommendation':'unsolved','original_shared_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'source_preparation_completion_estimate_percent':100,'target_discovery_completion_estimate_percent':0,'outer_completed_closing_capture_outside_own_manifest_required':True,'ROOT_separate_postexit_readback_required':True,'foreign_raw_SQL_PDF_OCR_pixel_bodies_copied':False}
    with (F/SELF).open('xb') as h:h.write((json.dumps(m,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
    (F/SELF).chmod(0o444);after,afterdirs=scan();require(after==files and afterdirs==dirs,'Closed bodies/topology changed');require(all(stat.S_IMODE((F/r['path']).stat().st_mode)==0o444 for r in files) and stat.S_IMODE((F/SELF).stat().st_mode)==0o444,'Full0444 closure')
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY_WAIT_ROOT_POSTEXIT_READBACK','files_count':len(files),'files_including_manifest':len(files)+1,'manifest_sha256':sha(regular(F/SELF)),'actual_closing_pid':os.getpid(),'production_builder_executed':False,'future_acceptance_approved':False},indent=2))
if __name__=='__main__':main()
