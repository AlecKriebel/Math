#!/usr/bin/env python3
"""Exact inventory/hash verification, with actual changed/missing/extra controls."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def verify(entries, data):
    if set(entries)!=set(data):raise ValueError('inventory mismatch')
    for name,blob in data.items():
        item=entries[name]
        if len(blob)!=item['bytes'] or hashlib.sha256(blob).hexdigest()!=item['sha256']:
            raise ValueError('content mismatch: '+name)

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    entries={x['path']:x for x in manifest['files']}
    if len(entries)!=len(manifest['files']):raise ValueError('duplicate manifest paths')
    data={str(p.relative_to(ROOT)):p.read_bytes() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
    verify(entries,data); rejected=[]
    key=next(iter(data))
    for name,changed in [('modified',dict(data,**{key:data[key]+b'\n'})),('missing',{k:v for k,v in data.items() if k!=key}),('extra',dict(data,**{'unexpected.txt':b'not authorized'}))]:
        try:verify(entries,changed)
        except ValueError:rejected.append(name)
        else:raise ValueError('manifest control accepted: '+name)
    print(json.dumps({'PASS':True,'files_verified':len(data),'manifest_negative_controls_rejected':rejected},indent=2))
if __name__=='__main__':main()
