#!/usr/bin/env python3
"""Additional actual verifier/producer regressions; benign copied fixtures."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
from review_controls import AUDIT, PUB, HERE, CACHE, EXTRACTED, PROFILE, clone_tree, altered_copy, reseal_outer


def main():
    outcomes=[]
    for filename in ('source.pdf','imported_corpus.txt'):
        src=EXTRACTED/'original/unsolved_math_prioritization/attempts/30004404'
        target=CACHE/'historical_R1'/filename/'release'
        if target.exists():shutil.rmtree(target)
        shutil.copytree(src,target)
        extra=target/filename;extra.write_bytes(b'BENIGN SYNTHETIC FIXTURE, NO THIRD-PARTY CONTENT\n')
        m=target/'RELEASE_MANIFEST.json';d=json.loads(m.read_text())
        d['files'].append({'path':filename,'bytes':extra.stat().st_size,
                           'sha256':hashlib.sha256(extra.read_bytes()).hexdigest()})
        m.write_text(json.dumps(d,indent=2)+'\n')
        p=subprocess.run(['/usr/bin/sandbox-exec','-p',PROFILE,sys.executable,'-B',str(target/'verify_release.py'),'--self-test'],capture_output=True,text=True)
        assert p.returncode==0,p.stderr
        result=json.loads(p.stdout)
        assert result['source_files_included'] is False and result['release_files_verified']==22
        outcomes.append({'case':'historical_manifested_'+filename,'historical_acceptance_confirmed':True,
                         'full_output':result,'stderr':p.stderr})
    def seal(root):
        path=root/'reviews/priority02/SHA256SUMS';path.write_bytes(path.read_bytes()+b'\n')
        reseal_outer(root)
    outcomes.append(altered_copy('nested_seal_changed_outer_resealed',seal,'Seal binding differs'))
    def symlink(root):
        path=root/'README.md';data=path.read_bytes();path.unlink();target=root.parent/'benign_symlink_target.md';target.write_bytes(data);path.symlink_to(target)
    outcomes.append(altered_copy('actual_driver_symlink',symlink,'Unexpected symlink'))
    # Nonselected private/raw/cache fixtures must never enter the authored archive.
    root=CACHE/'producer_extra/audit';clone_tree(root)
    for name in ('.cache/raw.pdf','sources/raw.txt','scratch/sentinel.txt','qa/page.png','.secrets/benign.env','account.private.txt'):
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('BENIGN SYNTHETIC UNSELECTED FIXTURE\n')
    p=subprocess.run([sys.executable,'-B',str(root/'publication/make_package.py')],capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    assert (root/'publication/verification_package.zip').read_bytes()==(PUB/'verification_package.zip').read_bytes()
    outcomes.append({'case':'unselected_raw_cache_private_fixtures','exact_zip':True,'selected':False})
    (HERE/'EXTRA_CONTROLS_RESULT.json').write_text(json.dumps({'status':'PASS','controls':outcomes},indent=2)+'\n')
    print(json.dumps({'status':'PASS','historical_R1_full_replays':2,'more_driver_rejections':2,'unselected_raw_cache_private_fixtures_excluded':6}))


if __name__=='__main__':main()
