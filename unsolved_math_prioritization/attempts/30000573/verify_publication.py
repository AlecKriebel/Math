#!/usr/bin/env python3
"""Fail-closed byte inventory and scoped replay; not a mathematical proof checker.
Verify this program externally before trusting it. Never rebind unknown code.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import zipfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def regular(path):
    need(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'nonregular file: '+str(path))


def zip_match(path, root, prefix):
    expected = {prefix+'/'+p.name for p in root.iterdir()}
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)) and set(names) == expected, 'ZIP inventory mismatch')
        for info in archive.infolist():
            pp = PurePosixPath(info.filename)
            need(not pp.is_absolute() and '..' not in pp.parts and len(pp.parts) == 2, 'unsafe ZIP name')
            need(not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0,stat.S_IFREG), 'nonregular ZIP member')
            need(archive.read(info.filename) == (root/pp.name).read_bytes(), 'ZIP member bytes mismatch')
    return len(names)


def check_manifest(root, pin):
    need(not root.is_symlink(), 'symlink root')
    need(len(pin)==64 and all(c in '0123456789abcdef' for c in pin), 'invalid external pin')
    path=root/'PUBLICATION_MANIFEST.json';regular(path);raw=path.read_bytes()
    need(digest(raw)==pin, 'external manifest pin mismatch')
    manifest=json.loads(raw)
    need(set(manifest)=={'schema','problem_id','files'} and manifest['schema']==1 and manifest['problem_id']==30000573,'manifest schema')
    files=manifest['files'];dirs=set()
    for name in files:
        pp=PurePosixPath(name)
        need(str(pp)==name and not pp.is_absolute() and '..' not in pp.parts and '\\' not in name,'unsafe manifest path')
        need(name!='PUBLICATION_MANIFEST.json','self-listed manifest')
        dirs.update(str(x) for x in pp.parents if str(x)!='.')
    actual_files=set();actual_dirs=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink entry')
        rel=p.relative_to(root).as_posix()
        if p.is_dir(): actual_dirs.add(rel)
        else: regular(p);actual_files.add(rel)
    need(actual_files==set(files)|{'PUBLICATION_MANIFEST.json'},'file inventory mismatch')
    need(actual_dirs==dirs,'directory inventory mismatch')
    for name,spec in files.items():
        b=(root/name).read_bytes()
        need(set(spec)=={'bytes','sha256'} and type(spec['bytes']) is int,'member schema')
        need(len(b)==spec['bytes'] and digest(b)==spec['sha256'],'member mismatch: '+name)
    return len(actual_files)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected-manifest',required=True)
    args=parser.parse_args();invoked=Path(__file__).absolute();root=invoked.parent
    try:
        regular(invoked);count=check_manifest(root,args.expected_manifest)
        status=json.loads((root/'PUBLICATION_STATUS.json').read_bytes())
        need(status['problem_id']==30000573 and status['status']=='unsolved','target disposition')
        need(status['turns_used']==status['turn_limit']==5,'turn count')
        for name,spec in status['archives'].items():
            b=(root/'archives'/name).read_bytes();need(len(b)==spec['bytes'] and digest(b)==spec['sha256'],'archive external pin')
        author_name=status['author_archive'];audit_name=status['audit_archive']
        a_count=zip_match(root/'archives'/author_name,root/'author','release')
        u_count=zip_match(root/'archives'/audit_name,root/'independent_audit','audit')
        for folder,pin_key in [('author','author_manifest_sha256'),('independent_audit','audit_manifest_sha256')]:
            need(digest((root/folder/'MANIFEST.json').read_bytes())==status[pin_key],'inner manifest pin')
            m=json.loads((root/folder/'MANIFEST.json').read_bytes())
            need(set(m['files'])=={p.name for p in (root/folder).iterdir()}-{'MANIFEST.json'},'inner inventory')
            for name,spec in m['files'].items():
                b=(root/folder/name).read_bytes();need(spec=={'bytes':len(b),'sha256':digest(b)},'inner member')
        acceptance=json.loads((root/'independent_audit'/'ACCEPTANCE.json').read_bytes())
        need(acceptance['decision']=='ACCEPT_SCOPED_PARTIAL_RESULTS_UNSOLVED','audit disposition')
        need(acceptance['original_problem_disposition']=='unsolved' and acceptance['turns_used']==5,'audit status')
        need(acceptance['required_corrections']==[],'unexpected mathematical corrections')
        cmd=[sys.executable,'-I']+(['-O'] if sys.flags.optimize else [])+['-B',str(root/'independent_audit'/'audit_checks.py'),'--author-zip',str(root/'archives'/author_name)]
        run=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=180)
        need(run.returncode==0,'independent replay failed: '+run.stderr)
        got=json.loads(run.stdout);expected=json.loads((root/'independent_audit'/'AUDIT_CHECKS.json').read_bytes())
        need(got==expected,'independent replay output mismatch')
        need(got['negative_control_count']==36 and got['author_primary_cases_per_replay']==13722,'independent counts')
        need(len(got['baseline'])==4 and len(got['scope_diagnostics'])==2,'independent coverage')
        print(json.dumps({'status':'PASS_PUBLICATION_INTEGRITY_AND_REPLAY','problem_id':30000573,'target_status':'unsolved','turns_used':5,'publication_manifest_sha256':args.expected_manifest,'files_verified':count,'author_archive_members':a_count,'audit_archive_members':u_count,'independent_negative_controls':36,'finite_author_cases_per_replay':13722,'independent_baselines':4,'expected_pass_scope_diagnostics':2,'scope':'Bytes, inventory and finite diagnostics; mathematical acceptance is separate.'},sort_keys=True,indent=2))
        return 0
    except Exception as exc:
        print('REJECT: '+str(exc),file=sys.stderr);return 1


if __name__=='__main__':
    raise SystemExit(main())
