#!/usr/bin/env python3
"""Exercise the exact-file-set and byte verification interface in private copies."""
import datetime, hashlib, json, shutil, subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
def run():
    manifest=HERE/'FIRST_PARTY_MANIFEST.json'
    frozen=json.loads(manifest.read_text())
    root=HERE/'ignoredtmp/manifest_controls'; root.mkdir(parents=True,exist_ok=True)
    cases=[]
    for label in ['pristine','tampered_bytes','missing_file','unlisted_file','nested_same_basename','ignored_foreign_file']:
        dest=root/label
        if dest.exists():shutil.rmtree(dest)
        dest.mkdir()
        for row in frozen['files']:
            target=dest/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(HERE/row['path'],target)
        shutil.copy2(manifest,dest/manifest.name)
        if label=='tampered_bytes':(dest/'REPORT.md').write_text('Corrupted content\n')
        if label=='missing_file':(dest/'.gitignore').unlink()
        if label=='unlisted_file':(dest/'unlisted.txt').write_text('Unlisted authored content\n')
        if label=='nested_same_basename':
            (dest/'nested').mkdir();(dest/'nested/FIRST_PARTY_MANIFEST.json').write_text('{}\n')
        if label=='ignored_foreign_file':
            (dest/'ignoredtmp').mkdir();(dest/'ignoredtmp/foreign.txt').write_text('Foreign content stays excluded\n')
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        argv=['/usr/bin/python3',str(dest/'replay_audit.py'),'--verify-manifest']
        r=subprocess.run(argv,capture_output=True)
        expect=label in ['pristine','ignored_foreign_file']
        assert (r.returncode==0)==expect, label
        cases.append({'case':label,'at_utc':start,'argv':argv,'returncode':r.returncode,
                      'expected_pass':expect,'actual_pass':r.returncode==0,
                      'stdout':r.stdout.decode(),'stderr_tail':r.stderr.decode()[-500:]})
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'tested_manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
             'all_expected_outcomes':True,'cases':cases,
             'note':'Receipt creation changes the live authored set; regenerate its self-excluding manifest afterward.'}
    (HERE/'MANIFEST_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'controls':len(cases),'all_expected_outcomes':True}))

if __name__=='__main__':run()
