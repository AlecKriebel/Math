"""Physical self-controls for the review's own custody verifier."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, json, os, shutil
from verify_custody import snapshot, verify


def main():
    rows=[]
    # TMPDIR is deliberately supplied by the caller; no peer directory is used.
    with TemporaryDirectory(prefix='review03-custody-') as tmp:
        base=Path(tmp)
        root=base/'packet'
        def reset():
            if root.exists():shutil.rmtree(root)
            root.mkdir();(root/'.hidden').write_bytes(b'hidden')
            (root/'nested').mkdir();(root/'nested/evidence').write_bytes(b'evidence')
            manifest={'schema':'review-preprint03-exact-inventory-v1','files':snapshot(root)}
            raw=(json.dumps(manifest,sort_keys=True)+'\n').encode()
            (root/'MANIFEST.json').write_bytes(raw)
            return hashlib.sha256(raw).hexdigest()
        pin=reset();verify(root,pin);rows.append({'case':'baseline_hidden_nested','result':'PASS'})
        for p in root.rglob('*'):
            if p.is_file():os.utime(p,(1000000001,1000000001))
        moved=base/'relocated with spaces';shutil.copytree(root,moved)
        verify(moved,pin);rows.append({'case':'relocated_changed_mtimes','result':'PASS'})
        cases={
            'wrong_pin':lambda:None,
            'missing':lambda:(root/'nested/evidence').unlink(),
            'extra_hidden':lambda:(root/'.extra').write_bytes(b'extra'),
            'altered':lambda:(root/'nested/evidence').write_bytes(b'changed'),
            'rewritten_manifest':lambda:(root/'MANIFEST.json').write_bytes(b'{}'),
            'symlink':lambda:(root/'link').symlink_to(root/'nested/evidence'),
            'fifo':lambda:os.mkfifo(root/'fifo'),
            'empty_directory':lambda:(root/'empty').mkdir(),
        }
        for label,change in cases.items():
            pin=reset();change()
            try:verify(root,'0'*64 if label=='wrong_pin' else pin)
            except (ValueError,OSError):rows.append({'case':label,'result':'REJECTED'})
            else:raise RuntimeError('negative accepted: '+label)
        pin=reset();link=base/'root-link';link.symlink_to(root,target_is_directory=True)
        try:verify(link,pin)
        except (ValueError,OSError):rows.append({'case':'root_symlink','result':'REJECTED'})
        else:raise RuntimeError('root symlink accepted')
    print(json.dumps({'status':'PASS','controls':rows,'positive':2,'negative':9,
                      'owned_temporary_fixture_removed':True},sort_keys=True,indent=2))


if __name__=='__main__':
    main()
