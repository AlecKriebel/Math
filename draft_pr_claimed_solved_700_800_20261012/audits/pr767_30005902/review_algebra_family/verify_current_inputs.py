#!/usr/bin/env python3
"""Separate read-only check of adjacent frozen/current inputs; no Git calls."""
import hashlib,json,os,stat
from pathlib import Path
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    root=Path(__file__).resolve().parent; a=root.parent
    expected=json.loads((root/'INPUT_BINDING.json').read_bytes())
    snapshot=json.loads((a/'SNAPSHOT.json').read_bytes())
    for name,entry in expected['adjacent_files'].items():
        p=a/name;need(stat.S_ISREG(p.lstat().st_mode),'input special file: '+name)
        data=p.read_bytes(); need(len(data)==entry['bytes'] and sha(data)==entry['sha256'],'adjacent binding changed: '+name)
    need(snapshot['head']==expected['head'],'snapshot head changed')
    files={}
    for parent,dirs,names in os.walk(a/'original',followlinks=False):
        for name in dirs+names:
            p=Path(parent)/name;mode=p.lstat().st_mode
            need(stat.S_ISDIR(mode) or stat.S_ISREG(mode),'original symlink or special node')
        for name in names:
            p=Path(parent)/name;files[p.relative_to(a/'original').as_posix()]=p
    need(set(files)=={e['path'] for e in snapshot['files']},'original exact inventory differs')
    total=0
    for e in snapshot['files']:
        p=files[e['path']];need(stat.S_ISREG(p.lstat().st_mode),'original special file')
        data=p.read_bytes();need(len(data)==e['bytes'] and sha(data)==e['sha256'],'original changed: '+e['path']);total+=len(data)
    record=json.loads((a/'private_sources/selected_record.json').read_bytes())
    need(record['statement_hash']==expected['statement_hash'] and record['review_hash']==expected['review_hash'],'record identity metadata changed')
    need(record['prior_research']=={},'prior value changed')
    return {'status':'PASS','scope':'adjacent inputs at replay time; not authored history closure',
      'head':snapshot['head'],'frozen_original_file_count':len(files),'frozen_original_bytes':total,
      'source_record_hashes_bound':True,'git_or_remote_mutations':False}
if __name__=='__main__': print(json.dumps(main(),sort_keys=True,indent=2))
