#!/usr/bin/env python3
"""Read-only authentication of the selected immutable program against copied disk."""
import argparse, hashlib, json, pathlib, subprocess, datetime
p=argparse.ArgumentParser(); p.add_argument('--output',required=True); a=p.parse_args()
root=pathlib.Path('/Users/alec/Documents/Math')
audit=root/'draft_pr_claimed_solved_900_1000_20261012/audits/pr932_30003471'
head='c09ef9df8b1f4642be0396ba6343344be8fa25b0'
prefix='unsolved_math_prioritization/attempts/30003471'
raw=subprocess.check_output(['git','-C',str(root),'ls-tree','-r','-z',head,'--',prefix])
rows=[]
for record in raw.split(b'\0'):
 if not record: continue
 meta, name=record.split(b'\t',1); mode,kind,oid=meta.decode().split(); path=name.decode()
 if kind!='blob': raise RuntimeError((path,kind))
 data=subprocess.check_output(['git','-C',str(root),'cat-file','blob',oid])
 disk=(audit/'original'/path).read_bytes()
 rows.append(dict(path=path,git_blob=oid,git_bytes=len(data),disk_bytes=len(disk),git_sha256=hashlib.sha256(data).hexdigest(),disk_sha256=hashlib.sha256(disk).hexdigest(),match=data==disk))
out=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),original_head=head,selected_prefix=prefix,file_count=len(rows),all_match=all(r['match'] for r in rows),files=rows)
pathlib.Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='files'}))
