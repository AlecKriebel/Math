#!/usr/bin/env python3
"""Run only disposable local package controls; preserve current/frozen bytes."""
import sys
sys.dont_write_bytecode=True
import datetime,hashlib,json,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent/'preprint_v1_0'
DEST=HERE/'tmp/controls'
def sha(data):return hashlib.sha256(data).hexdigest()
def execute(folder,name):
    r=subprocess.run([sys.executable,'-B','verify_package.py'],cwd=folder,capture_output=True)
    (HERE/(name+'_stdout.txt')).write_bytes(r.stdout);(HERE/(name+'_stderr.txt')).write_bytes(r.stderr)
    return r
def main():
    if DEST.exists():shutil.rmtree(DEST)
    controls=[]
    for name in ['altered_content','unmanifested_content','altered_archive','altered_wrapper','premature_readiness','fullsource_outside_raw']:
        folder=DEST/name
        shutil.copytree(ROOT,folder,ignore=shutil.ignore_patterns('tmp'))
        if name=='altered_content':
            with (folder/'paper.tex').open('a') as f:f.write('\n% deliberate integrity control\n')
        elif name=='unmanifested_content':(folder/'UNMANIFESTED.md').write_text('deliberate integrity control\n')
        elif name=='altered_archive':
            p=folder/'supportkit-v1.0.tar.gz';data=bytearray(p.read_bytes());data[-16]^=1;p.write_bytes(data)
        elif name=='altered_wrapper':
            p=folder/'zenodo-deposit.json';data=json.loads(p.read_text());data['metadata']['title']='deliberate metadata control';p.write_text(json.dumps(data)+'\n')
        elif name=='premature_readiness':
            p=folder/'STATUS.json';data=json.loads(p.read_text());data['publication_ready']=True;data['all_issues_resolved']=True;p.write_text(json.dumps(data,indent=2)+'\n')
            r=subprocess.run([sys.executable,'-B','build_archive.py'],cwd=folder,capture_output=True)
            if r.returncode:raise RuntimeError('control build failed')
        elif name=='fullsource_outside_raw':
            (folder/'fullsource.txt').write_text('deliberate excluded source-extract placeholder\n')
            before=(folder/'supportkit-v1.0.tar.gz').read_bytes()
            r=subprocess.run([sys.executable,'-B','build_archive.py'],cwd=folder,capture_output=True)
            if r.returncode or before!=(folder/'supportkit-v1.0.tar.gz').read_bytes():raise RuntimeError('excluded fullsource changed archive')
        r=execute(folder,'control_'+name)
        if name=='fullsource_outside_raw':
            if r.returncode:raise RuntimeError('intentional source exclusion check failed')
            controls.append({'control':name,'source_extract_excluded_even_outside_raw':True,'archive_unchanged':True,'verifier_returncode':0})
        else:
            if r.returncode==0:raise RuntimeError('negative control was not rejected: '+name)
            controls.append({'control':name,'rejected':True,'returncode':r.returncode})
    (HERE/'NEGATIVE_CONTROLS.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'disposable_copies_only':True,'controls':controls},indent=2)+'\n')
    print(json.dumps(controls))
if __name__=='__main__':main()
