#!/usr/bin/env python3
"""Merge and cross-check the six source residual manifests."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-root',type=Path,required=True)
    args=parser.parse_args()
    rows=[];bindings=None;seen=set();totals={}
    for source in range(6):
        path=args.run_root/f'source_{source}'/'residual_manifest.json'
        if not path.exists():raise SystemExit(f'missing {path}')
        row=json.loads(path.read_text())
        if row['source_index']!=source:raise SystemExit(f'wrong source index in {path}')
        current={k:row[k] for k in ('compiler_sha256','canonicalizer_sha256','descriptor_pickle_sha256','rank_pickle_sha256','output_schema_sha256','input_lock_sha256')}
        if bindings is None:bindings=current
        elif current!=bindings:raise SystemExit(f'input binding disagreement in {path}')
        ids=[record['canonical_class_id'] for record in row['records']]
        if len(ids)!=len(set(ids)):raise SystemExit(f'duplicate class in {path}')
        for status in ('separated','isomorphic','triangle','restoration_parent','unresolved'):
            totals[status]=totals.get(status,0)+sum(record['status']==status for record in row['records'])
        rows.append({'source_index':source,'manifest_sha256':sha(path),'complete':row['complete'],
                     'canonical_class_count':row['canonical_class_count'],'record_count':row['record_count'],
                     'unresolved':row['unresolved'],'restoration_candidates':row['restoration_candidates']})
        seen.add(source)
    payload={'schema':'k2p-four-port-six-source-merge-v1','bindings':bindings,'sources':rows,
             'all_six_sources_present':seen==set(range(6)),
             'all_manifests_complete':all(row['complete'] for row in rows),
             'total_status_counts':totals,
             'unresolved_by_source':{str(row['source_index']):row['unresolved'] for row in rows if row['unresolved']},
             'restoration_candidate_counts':{str(row['source_index']):len(row['restoration_candidates']) for row in rows}}
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    payload['payload_sha256_without_hash']=hashlib.sha256(raw).hexdigest()
    out=args.run_root/'FOUR_PORT_SWEEP_MERGED_STATUS.json'
    out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(out),'complete':payload['all_manifests_complete'],'counts':totals,
                      'unresolved_by_source':payload['unresolved_by_source']},sort_keys=True))

if __name__=='__main__':main()
