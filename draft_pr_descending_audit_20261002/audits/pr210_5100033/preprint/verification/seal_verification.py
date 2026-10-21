#!/usr/bin/env python3
"""Seal the assembled verification payload; no copying, replay or publication."""
from pathlib import Path
import argparse,hashlib,json
from integrity import BASE,inventory

def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--seal',action='store_true')
    g.add_argument('--candidate',type=Path,help='write an unsealed trial inventory outside this package')
    args=p.parse_args()
    out=BASE/'MANIFEST.json' if args.seal else args.candidate
    if args.candidate and (out.resolve()==BASE or BASE in out.resolve().parents):raise ValueError('Candidate must be outside package')
    rows=inventory()
    data={'schema':'portable-pr210-sha256-v1','source_head':'2180d64b648b81ac660a792f7823d0b715f9cf12','scope':'Portable verification payload; manuscript and final publication seal are separate.','self_excluded':True,'files':rows}
    raw=(json.dumps(data,indent=2)+'\n').encode();out.write_bytes(raw)
    print(json.dumps({'files':len(rows),'payload_bytes':sum(r['bytes'] for r in rows),'manifest_sha256':hashlib.sha256(raw).hexdigest(),'output':str(out)},indent=2))
if __name__=='__main__':main()
