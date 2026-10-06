#!/usr/bin/env python3
"""Replay normal/optimized/relocation/adversarial controls in temporary directories.
Bootstrap this file and the external manifest from separately trusted hashes first.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(manifest):
    package=Path(__file__).absolute().parent
    manifest=manifest.absolute()
    manifest_hash=sha(manifest)
    seal=json.loads(manifest.read_bytes())
    verifier_hash=seal['files']['verify.py']['sha256']
    records=[]

    def execute(p,m,optimized=False):
        # A forged external manifest is not a new trust anchor.
        if sha(m)!=manifest_hash:
            return {'code':91,'reason':'external manifest bootstrap pin rejected'}
        if not stat.S_ISREG((p/'verify.py').lstat().st_mode) or sha(p/'verify.py')!=verifier_hash:
            return {'code':92,'reason':'verifier bootstrap pin rejected'}
        args=[sys.executable]+(['-O'] if optimized else [])+['-B',str(p/'verify.py'),str(m)]
        r=subprocess.run(args,cwd='/tmp',capture_output=True,text=True,timeout=45,check=False)
        return {'code':r.returncode,'reason':r.stderr.strip(),'stdout':r.stdout}

    base=execute(package,manifest,bool(sys.flags.optimize))
    need(base['code']==0, 'initial trusted-package verification failed')
    with tempfile.TemporaryDirectory(prefix='multiplicity-controls-') as tmp:
        tmp=Path(tmp)
        for label,opt in [('normal',False),('optimized',True),('relocated with spaces',False),('relocated optimized with spaces',True)]:
            p=tmp/label
            shutil.copytree(package,p)
            r=execute(p,manifest,opt)
            need(r['code']==0,label+' failed')
            records.append({'control':label,'outcome':'passed','result':json.loads(r['stdout'])})
        names=['extra_file','extra_directory','cache_directory','missing_file','tampered_report',
               'symlink_report','broken_symlink','symlink_directory','fifo_node','directory_in_place',
               'tampered_expected','tampered_certificate','tampered_verifier',
               'forged_manifest_missing_entry','forged_manifest_extra_entry','forged_manifest_duplicate_key',
               'forged_manifest_boolean_schema','rehashed_report_and_manifest','rehashed_certificate_and_manifest']
        for name in names:
            for opt in [False,True]:
                p=tmp/(name+('_optimized' if opt else ''))
                shutil.copytree(package,p)
                m=tmp/(p.name+'_external.json')
                shutil.copyfile(manifest,m)
                if name=='extra_file':(p/'extra.txt').write_text('unexpected')
                elif name=='extra_directory':(p/'extra').mkdir()
                elif name=='cache_directory':(p/'__pycache__').mkdir()
                elif name=='missing_file':(p/'RESULT.md').unlink()
                elif name=='tampered_report':(p/'RESULT.md').write_text('changed report')
                elif name=='symlink_report':
                    (p/'RESULT.md').unlink();(p/'RESULT.md').symlink_to(package/'RESULT.md')
                elif name=='broken_symlink':(p/'broken').symlink_to(tmp/'does-not-exist')
                elif name=='symlink_directory':(p/'linked').symlink_to(package,target_is_directory=True)
                elif name=='fifo_node':os.mkfifo(p/'pipe')
                elif name=='directory_in_place':(p/'EXPECTED.json').unlink();(p/'EXPECTED.json').mkdir()
                elif name=='tampered_expected':(p/'EXPECTED.json').write_text('{}\n')
                elif name in ['tampered_certificate','tampered_verifier']:
                    fn='certificate.py' if name=='tampered_certificate' else 'verify.py'
                    (p/fn).write_text('from pathlib import Path\nPath(__file__).with_name("EXECUTED_SENTINEL").write_text("unsafe")\n')
                elif name.startswith('forged_manifest'):
                    data=json.loads(m.read_bytes())
                    if name.endswith('missing_entry'):del data['files']['RESULT.md']
                    elif name.endswith('extra_entry'):data['files']['../escape.txt']={'bytes':0,'sha256':'0'*64}
                    elif name.endswith('boolean_schema'):data['schema']=True
                    if name.endswith('duplicate_key'):
                        m.write_text('{"schema":1,"schema":1,"problem_id":30001707,"files":{}}')
                    else:m.write_text(json.dumps(data))
                elif name.startswith('rehashed_'):
                    fn='RESULT.md' if name=='rehashed_report_and_manifest' else 'certificate.py'
                    if fn.endswith('.py'):
                        (p/fn).write_text('from pathlib import Path\nPath(__file__).with_name("EXECUTED_SENTINEL").write_text("unsafe")\n')
                    else:(p/fn).write_text('forged mathematical result')
                    data=json.loads(m.read_bytes());data['files'][fn]={'bytes':(p/fn).stat().st_size,'sha256':sha(p/fn)}
                    m.write_text(json.dumps(data))
                r=execute(p,m,opt)
                need(r['code']!=0,'adversarial package accepted: '+name)
                need(not (p/'EXECUTED_SENTINEL').exists(),'untrusted code executed')
                records.append({'control':name,'optimized':opt,'outcome':'rejected',
                                'reason':r['reason'],'execution_sentinel_absent':True})
    return {'schema':1,'positive_controls':4,'negative_controls':len(names)*2,
            'manifest_bootstrap_sha256':manifest_hash,'verifier_bootstrap_sha256':verifier_hash,
            'controls':records,
            'limit':'Checks test integrity and execution boundaries, not the prose mathematics.'}


if __name__=='__main__':
    need(len(sys.argv)==2,'usage: controls.py EXTERNAL_MANIFEST.json')
    print(json.dumps(main(Path(sys.argv[1])),sort_keys=True,indent=2))
