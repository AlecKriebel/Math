#!/usr/bin/env python3
"""Read-only checker of exact submitted namespace, manifests and native binding."""
import argparse, base64, hashlib, json, stat
from pathlib import Path

H = '6be98eac0ba508368218179ecf80020c037dbece'
B = 'efd29c05204703acca9a0860812f54b94fae54b1'
PREFIX = 'problems/30001370_basin_boundaries/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--snapshot', type=Path, required=True)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--capture-dir', type=Path)
    a = p.parse_args()
    m = json.loads(a.manifest.read_bytes())
    assert m['head'] == H and m['base'] == B and m['pr'] == 359
    expected = {f['path']:f for f in m['files']}
    assert len(expected) == len(m['files']) == 38
    assert all(s == QUEUE or s.startswith(PREFIX) for s in expected)
    actual = {str(f.relative_to(a.snapshot)) for f in a.snapshot.rglob('*') if f.is_file()}
    assert actual == set(expected)
    byte_map = {}
    for rel, f in expected.items():
        path = a.snapshot / rel
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) and stat.S_IMODE(mode) == 0o644 and f['mode'] == '100644'
        b = path.read_bytes()
        assert len(b) == f['bytes'] and digest(b) == f['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == f['git_blob_sha']
        byte_map[f['git_blob_sha']] = b
    folder = a.snapshot / PREFIX
    declarations = 0
    semantics = []
    for rel in ['TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','TURN_3_MANIFEST.json',
                'FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
        f = folder / rel
        j = json.loads(f.read_bytes())
        for row in j['files']:
            target = (f.parent / row['path']).resolve()
            assert target.is_relative_to(folder.resolve())
            b = target.read_bytes()
            assert len(b) == row['bytes'] and digest(b) == row['sha256']
            declarations += 1
        semantics.append(dict(manifest=rel, declarations=len(j['files']),
                              nonfile_declarations={k:v for k,v in j.items() if k!='files'}))
    for current, previous in [('TURN_2_MANIFEST.json','TURN_1_MANIFEST.json'),
                              ('TURN_3_MANIFEST.json','TURN_2_MANIFEST.json')]:
        j=json.loads((folder/current).read_bytes())
        assert j['previous_manifest_sha256']==digest((folder/previous).read_bytes())
    r=json.loads((folder/'review/REVIEW_MANIFEST.json').read_bytes())
    assert r['author_manifest_sha256']==digest((folder/'FINAL_AUTHOR_MANIFEST.json').read_bytes())
    publication=json.loads((folder/'PUBLICATION_MANIFEST.json').read_bytes())
    binding=json.loads((folder/'review/REMOTE_BINDING.json').read_bytes())
    assert publication['fresh_main_parent']==B and publication['author_head']==binding['commit']
    historical = 0
    for row in binding['files']:
        b=(folder/row['name']).read_bytes()
        assert len(b)==row['size']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['sha']
        historical += 1
    capture_receipts = api_bindings = tree_bindings = blob_bindings = 0
    captured_stderr=[]
    captured_heads=[]
    captured_indices=[]
    captured_branch=None
    if a.capture_dir:
        for f in sorted(a.capture_dir.glob('*.receipt.json')):
            row=json.loads(f.read_bytes());stem=f.name.split('.')[0]
            out=(a.capture_dir/(stem+'.stdout')).read_bytes()
            err=(a.capture_dir/(stem+'.stderr')).read_bytes()
            assert len(out)==row['stdout_bytes'] and digest(out)==row['stdout_sha256']
            assert len(err)==row['stderr_bytes'] and digest(err)==row['stderr_sha256']
            assert row['exit_code']==0
            if err: captured_stderr.append(dict(capture=stem,argv=row['argv'],bytes=len(err),sha256=digest(err)))
            args=row['argv']
            if args==['git','branch','--show-current']:
                captured_branch=out.strip().decode()
            if args==['git','rev-parse','HEAD']:
                captured_heads.append(out.strip().decode())
            if args==['git','ls-files','-s','-z']:
                captured_indices.append(digest(out))
            if args==['git','diff','--name-only',B,H]:
                assert set(out.decode().splitlines())==set(expected)
            if args[:3]==['git','cat-file','blob']:
                assert byte_map[args[3]]==out;blob_bindings+=1
            if args[:2]==['git','ls-tree']:
                assert args[2]==H
                meta,rel=out.decode().strip().split('\t');mode,kind,sha=meta.split()
                assert kind=='blob' and mode==expected[rel]['mode'] and sha==expected[rel]['git_blob_sha']
                tree_bindings+=1
            if args[:2]==['gh','api']:
                body=json.loads(out);sha=args[-1].rsplit('/',1)[-1]
                assert args[-1]=='repos/AlecKriebel/Math/git/blobs/'+sha
                assert body['sha']==sha and body['encoding']=='base64'
                b=base64.b64decode(body['content'])
                assert b==byte_map[sha] and body['size']==len(b);api_bindings+=1
            if args[:4]==['gh','pr','view','359']:
                body=json.loads(out)
                assert body['headRefOid']==H and body['state']=='OPEN' and body['isDraft']
                if 'baseRefOid' in body: assert body['baseRefOid']==B
                if 'files' in body: assert {v['path'] for v in body['files']}==set(expected)
            capture_receipts += 1
        assert (capture_receipts,api_bindings,tree_bindings,blob_bindings)==(123,38,38,38)
        assert captured_branch=='main'
        assert captured_heads==[m['original_main'],m['original_main']]
        assert len(captured_indices)==2 and captured_indices[0]==captured_indices[1]
    print(json.dumps(dict(status='PASS',head=H,base=B,files=len(expected),mode='100644',
                         nested_file_declarations=declarations,manifest_semantics=semantics,
                         historical_author_blob_bindings=historical,
                         native_capture_receipts=capture_receipts,api_bindings=api_bindings,
                         tree_bindings=tree_bindings,blob_bindings=blob_bindings,
                         frozen_main_and_index_unchanged=bool(a.capture_dir),
                         captured_stderr=captured_stderr,
                         semantics_warning='Historical author head is not the final PR head. Claimed-solved/PASS labels and assertion counts are declarations, not proof.'),indent=2))

if __name__ == '__main__':
    main()
