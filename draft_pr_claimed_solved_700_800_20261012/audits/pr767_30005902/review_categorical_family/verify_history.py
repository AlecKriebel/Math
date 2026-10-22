#!/usr/bin/env python3
"""Read-only recursive review closure; optional current-input bindings are separate."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def meta(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def inventory(root):
    need(stat.S_ISDIR(os.lstat(root).st_mode),'root must be a real directory')
    files, dirs = {}, []
    for path in sorted(root.rglob('*')):
        mode = os.lstat(path).st_mode
        name = path.relative_to(root).as_posix()
        need(not stat.S_ISLNK(mode),'symlink: '+name)
        if stat.S_ISDIR(mode):
            need(any(path.iterdir()),'empty directory: '+name)
            dirs.append(name)
        else:
            need(stat.S_ISREG(mode),'special file: '+name)
            if name != 'MANIFEST.json':
                files[name] = meta(path.read_bytes())
    return files, dirs


def check_inputs(root):
    binding = json.loads((root/'INPUT_BINDINGS.json').read_bytes())
    original = Path(binding['original_root'])
    got = {}
    for path in sorted(original.rglob('*')):
        mode=os.lstat(path).st_mode
        need(not stat.S_ISLNK(mode),'original symlink')
        if stat.S_ISREG(mode):
            got[path.relative_to(original).as_posix()]=meta(path.read_bytes())
        else:
            need(stat.S_ISDIR(mode),'original special file')
    need(got==binding['original_files'],'current original files differ')
    need(len(got)==binding['original_file_count'],'original count')
    need(sum(x['bytes'] for x in got.values())==binding['original_total_bytes'],'original bytes')
    selected=binding['selected_record']
    raw=Path(selected['path']).read_bytes()
    need(meta(raw)=={k:selected[k] for k in ['bytes','sha256']},'selected record bytes')
    record=json.loads(raw)
    need(hashlib.sha256(record['problem']['statement'].encode()).hexdigest()==binding['statement_sha256'],'statement digest')
    review=hashlib.sha256(json.dumps([record['problem'],record['prior_research']],sort_keys=True).encode()).hexdigest()
    need(review==binding['review_sha256'],'review digest')
    return {'status':'PASS','original_files':len(got),'original_bytes':sum(x['bytes'] for x in got.values()),'scope':'current locally supplied input bindings only'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest-sha256')
    ap.add_argument('--inputs',action='store_true')
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    raw=(root/'MANIFEST.json').read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if args.manifest_sha256:
        need(digest==args.manifest_sha256,'external manifest pin')
    manifest=json.loads(raw)
    need(manifest['format']==1 and manifest['problem_id']==30005902 and manifest['family']=='categorical_cochain_comparison','identity')
    files,dirs=inventory(root)
    need(files==manifest['files'],'recursive exact file inventory/hashes')
    need(dirs==manifest['directories'],'recursive directory inventory')
    need(len(files)==manifest['file_count_excluding_manifest'],'file count')
    need(sum(v['bytes'] for v in files.values())==manifest['total_bytes_excluding_manifest'],'total bytes')
    result=(root/'CONTROL_RESULTS.json').read_bytes()
    runs=[]
    for flags in [[],['-O']]:
        proc=subprocess.run([sys.executable,*flags,'-B',str(root/'check_comparison.py')],capture_output=True,check=True)
        need(proc.stdout==result,'comparison replay bytes')
        runs.append({'optimized':bool(flags),'exact_result_bytes_match':True})
    verdict=json.loads((root/'VERDICT.json').read_bytes())
    need(verdict['issue_count']==0 and verdict['required_repairs']==[] and verdict['remaining_central_gaps']==[],'bounded verdict')
    out={'status':'PASS','file_count_including_manifest':len(files)+1,'manifest_sha256':digest,'external_pin_checked':bool(args.manifest_sha256),'closed_utc':manifest['closed_utc'],'authored_history':'exact recursive regular-file inventory including hidden files; excludes only MANIFEST.json','math_replays':runs,'current_inputs':check_inputs(root) if args.inputs else 'NOT_RUN: separate optional binding','limits':'Internal consistency unless manifest externally pinned; no formal/human/priority certification'}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
