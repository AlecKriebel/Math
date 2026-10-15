#!/usr/bin/env python3
"""Read-only closed-scope integrity/replay verifier for this audit.

The default verifies only public artifacts. --with-private checks source/raw
capture scope too. --snapshot checks the submitted candidate externally.
No output files, caches, Git operations, network calls, or installations.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def mode(path):
    return '100755' if path.stat().st_mode & 0o111 else '100644'


def ck(test, context):
    if not test:
        raise AssertionError(context)


def manifest(scope):
    directory = ROOT / scope
    name = scope.upper() + '_MANIFEST.json'
    data = (directory / name).read_bytes()
    obj = json.loads(data)
    expected = {entry['path'] for entry in obj['files']}
    discovered=list(directory.rglob('*'))
    ck(all(not p.is_symlink() for p in discovered), 'no hidden or broken symlinks in '+scope)
    actual = {str(p.relative_to(ROOT)) for p in discovered if p.is_file()}
    ck(actual == expected | {scope+'/'+name}, 'exact closed '+scope+' file set')
    ck(len(expected) == len(obj['files']), 'duplicate manifest paths')
    for entry in obj['files']:
        p = ROOT / entry['path']
        ck(not p.is_symlink() and p.is_file(), entry['path']+' regular file')
        b = p.read_bytes()
        ck(len(b) == entry['bytes'] and digest(b) == entry['sha256'], entry['path']+' bytes')
        ck(mode(p) == entry['mode'], entry['path']+' mode')
    return len(expected), digest(data)


def candidate(snapshot, binding):
    snapshot = snapshot.resolve()
    expected = {entry['path'] for entry in binding['files']}
    actual = {str(p.relative_to(snapshot)) for p in snapshot.rglob('*') if p.is_file()}
    ck(expected == actual, 'exact all38 snapshot file set')
    for entry in binding['files']:
        p = snapshot / entry['path']
        ck(p.is_file() and not p.is_symlink(), entry['path']+' regular')
        b=p.read_bytes()
        ck(len(b)==entry['bytes'] and digest(b)==entry['sha256'], entry['path'])
        ck(mode(p)==entry['mode'], entry['path']+' mode')
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        ck(blob==entry['git_blob_sha'], entry['path']+' Git blob')
    folder = snapshot/'problems/30001370_basin_boundaries'
    for item in binding['nested_manifests']:
        p = folder/item['manifest']; obj=json.loads(p.read_bytes())
        for entry in obj['files']:
            b=(p.parent/entry['path']).read_bytes()
            ck(len(b)==entry['bytes'] and digest(b)==entry['sha256'], item['manifest'])
        if 'previous_manifest_sha256' in obj:
            depth=int(p.name.split('_')[1])
            ck(obj['previous_manifest_sha256']==digest((folder/('TURN_'+str(depth-1)+'_MANIFEST.json')).read_bytes()), 'historical edge')
    for script, target in [('check_turn_1.py','TURN_1_CHECKS.json'),
                            ('check_turn_2.py','TURN_2_CHECKS.json'),
                            ('check_turn_3.py','TURN_3_CHECKS.json'),
                            ('review/check_independent.py','review/INDEPENDENT_CHECKS.json')]:
        p=subprocess.run([sys.executable,str(folder/script)],cwd=folder,capture_output=True)
        ck(p.returncode==0 and not p.stderr, script+' successful native replay')
        ck(p.stdout==(folder/target).read_bytes(), script+' complete byte-exact replay')
    return len(expected)


def private_captures(binding):
    cap=ROOT/'private/captures/root_freeze_import'
    apis={};blobs={};trees={}
    for item in binding['native_provenance']:
        stem=item['stem']; raw=(cap/(stem+'.receipt.json')).read_bytes()
        ck(digest(raw)==item['receipt_sha256'], stem+' imported provenance')
        rec=json.loads(raw);argv=rec['argv']
        ck(argv==item['argv'] and rec['exit_code']==0, stem+' imported command')
        out=(cap/(stem+'.stdout')).read_bytes();err=(cap/(stem+'.stderr')).read_bytes()
        ck(len(out)==rec['stdout_bytes'] and digest(out)==rec['stdout_sha256'], stem+' whole stdout')
        ck(len(err)==rec['stderr_bytes'] and digest(err)==rec['stderr_sha256'], stem+' whole stderr')
        if argv[:2]==['git','cat-file']:
            blobs[argv[-1]]=out
        elif argv[:2]==['gh','api'] and '/git/blobs/' in argv[-1]:
            obj=json.loads(out)
            b=base64.b64decode(obj['content'].replace('\\n','\n'))
            ck(len(b)==obj['size'], stem+' API decoded size')
            apis[obj['sha']]=b
        elif argv[:2]==['git','ls-tree']:
            trees[argv[-1]]=out.decode().split()[:3]
    for entry in binding['files']:
        b=blobs[entry['git_blob_sha']]
        ck(b==apis[entry['git_blob_sha']], entry['path']+' exact Git/API')
        ck(digest(b)==entry['sha256'] and len(b)==entry['bytes'], entry['path']+' complete raw bindings')
        ck(trees[entry['path']]==[entry['mode'],'blob',entry['git_blob_sha']], entry['path']+' tree mode')
    for entry in json.loads((ROOT/'public/source_identity_receipt.json').read_text())['sources']:
        b=(ROOT/'private/sources'/entry['file']).read_bytes()
        ck(len(b)==entry['bytes'] and digest(b)==entry['sha256'], entry['file']+' exact primary source')
    return len(binding['native_provenance'])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--with-private',action='store_true')
    ap.add_argument('--snapshot',type=Path)
    ap.add_argument('--unsealed-checks',action='store_true',help='content checks only; explicitly no closure PASS')
    args=ap.parse_args()
    seal=json.loads((ROOT/'public/independence_seal.json').read_text())
    ck(seal['candidate_access_before_seal'] is False, 'independence metadata')
    for item in seal['files']:
        b=(ROOT/item['path']).read_bytes()
        ck(len(b)==item['bytes'] and digest(b)==item['sha256'], 'pre-candidate reconstruction unchanged')
    binding=json.loads((ROOT/'public/immutable_binding_receipt.json').read_text())
    ck(binding['head']=='6be98eac0ba508368218179ecf80020c037dbece', 'head')
    ck(binding['base']=='efd29c05204703acca9a0860812f54b94fae54b1', 'base')
    ck(binding['all_submitted_files_count']==38, 'all submitted scope')
    ck(all(binding[k] for k in ['pr_head_base_match','pr_file_set_match','git_diff_set_match']), 'immutable path sets')
    ck(all(x['git_api_disk_match'] and x['tree_match'] for x in binding['files']), 'frozen identities')
    ck(all(x['size_match'] and x['hash_match'] and x['mode']=='100644'
           for m in binding['nested_manifests'] for x in m['entries']), 'all nested entries')
    result=subprocess.run([sys.executable,str(ROOT/'public/check_topology.py')],capture_output=True)
    ck(result.returncode==0 and not result.stderr, 'independent checker exit/stderr')
    ck(result.stdout==(ROOT/'public/topology_checks.json').read_bytes(), 'independent whole-output replay')
    public_count=private_count=None
    if not args.unsealed_checks:
        closure=json.loads((ROOT/'FINAL_CLOSURE.json').read_text())
        public_count,public_hash=manifest('public')
        ck(public_hash==closure['public_manifest_sha256'], 'public manifest closure binding')
        root_names={p.name for p in ROOT.iterdir()}
        ck(root_names <= {'public','private','FINAL_CLOSURE.json'} and
           {'public','FINAL_CLOSURE.json'} <= root_names, 'closed public root set')
        if args.with_private:
            ck(root_names=={'public','private','FINAL_CLOSURE.json'}, 'closed full root set')
            private_count,private_hash=manifest('private')
            ck(private_hash==closure['private_manifest_sha256'], 'private closure binding')
    snapshot_files=candidate(args.snapshot,binding) if args.snapshot else None
    captures=private_captures(binding) if args.with_private else None
    print(json.dumps({'status':'UNSEALED_CONTENT_CHECKS_PASS' if args.unsealed_checks else 'CLOSED_SCOPE_PASS',
                      'public_manifest_entries':public_count,'private_manifest_entries':private_count,
                      'external_snapshot_files_verified':snapshot_files,
                      'imported_whole_native_capture_commands':captures,
                      'independent_exact_controls':json.loads(result.stdout)['exact_assertions'],
                      'scope':'Read-only byte/mode/closed-set and whole-output verification; mathematics is established by the analytic report, not by these finite controls.'},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
