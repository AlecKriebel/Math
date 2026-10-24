#!/usr/bin/env python3
"""Exhaustive bounded rainbow Hamilton-cycle search; never a universal proof.

Group coordinates use mixed radix with the first coordinate least significant.
Certificate masks enumerate every subset containing zero with >=3 vertices.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time
from datetime import datetime, timezone

GROUPS = [(3,), (5,), (7,), (9,), (3,3), (11,), (13,), (15,)]

def utc():
    return datetime.now(timezone.utc).isoformat()

def coordinates(index, moduli):
    out = []
    for m in moduli:
        out.append(index % m)
        index //= m
    assert index == 0
    return out

def addition_table(moduli):
    q = 1
    for m in moduli: q *= m
    coords = [coordinates(i, moduli) for i in range(q)]
    table = []
    for u in coords:
        row = []
        for v in coords:
            index, stride = 0, 1
            for a,b,m in zip(u,v,moduli):
                index += ((a+b) % m) * stride
                stride *= m
            row.append(index)
        table.append(row)
    return table

def find_cycle(vertices, plus):
    """Complete DFS, vertex zero fixed; return witness and search statistics.

    Sum colors are bits. Every recursive choice has a new vertex and color.
    At closure require a new color and discard reversed duplicates by demanding
    cycle[1] < cycle[-1]. No heuristic pruning that could remove a valid cycle.
    """
    assert vertices[0] == 0 and len(vertices) > 2
    path = [0]
    calls = 0
    candidates = 0
    leaves = 0
    remaining_mask = sum(1 << v for v in vertices[1:])
    def visit(last, remaining, colors):
        nonlocal calls,candidates,leaves
        calls += 1
        if remaining == 0:
            leaves += 1
            closing_bit = 1 << plus[last][0]
            if path[1] < last and not (colors & closing_bit):
                return list(path)
            return None
        pending = remaining
        while pending:
            bit = pending & -pending
            pending -= bit
            v = bit.bit_length() - 1
            color = 1 << plus[last][v]
            if colors & color: continue
            candidates += 1
            path.append(v)
            result = visit(v, remaining ^ bit, colors | color)
            if result is not None: return result
            path.pop()
        return None
    cycle = visit(0, remaining_mask, 0)
    return cycle, {"calls":calls,"accepted_extensions":candidates,"closure_tests":leaves}

def group_label(moduli):
    return 'x'.join('C'+str(x) for x in moduli)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--max-order', type=int, default=15)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    summary = {"started_utc":utc(),"domain":"All subsets A containing 0 with |A|>2 in every listed odd-order abelian group. Translation covers all subsets in these groups.","groups":[],"complete":False}
    started = time.perf_counter()
    for moduli in GROUPS:
        plus = addition_table(moduli)
        q = len(plus)
        if q > args.max_order: continue
        label = group_label(moduli)
        path = args.output / (label + '.jsonl')
        group_started = time.perf_counter()
        counts = {}
        total_calls = 0
        worst = None
        failed = []
        expected = 2**(q-1)-q
        with path.open('w') as out:
            out.write(json.dumps({"format":"odd-rainbow-cycle-v1","moduli":moduli,"order":q,"fixed_start":0,"covered_subsets":expected},sort_keys=True)+'\n')
            for tail in range(1 << (q-1)):
                mask = (tail << 1) | 1
                n = mask.bit_count()
                if n < 3: continue
                vertices = [v for v in range(q) if mask & (1 << v)]
                cycle, stats = find_cycle(vertices,plus)
                total_calls += stats['calls']
                counts[str(n)] = counts.get(str(n),0)+1
                record = {"mask":mask,"cycle":cycle,"calls":stats['calls']}
                out.write(json.dumps(record,separators=(',',':'))+'\n')
                if worst is None or stats['calls']>worst['calls']:
                    worst = {**record,"vertices":vertices,**stats}
                if cycle is None: failed.append(record)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        result = {"group":label,"moduli":moduli,"order":q,"subsets":sum(counts.values()),"expected_subsets":expected,"counts_by_size":counts,"failures":failed,"total_dfs_calls":total_calls,"hardest":worst,"elapsed_seconds":time.perf_counter()-group_started,"certificate_file":path.name,"sha256":digest}
        summary['groups'].append(result)
        print(json.dumps(result),flush=True)
        if failed: break
    summary.update({"finished_utc":utc(),"elapsed_seconds":time.perf_counter()-started,"complete":not any(g['failures'] for g in summary['groups']),"total_subsets":sum(g['subsets'] for g in summary['groups'])})
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')

if __name__=='__main__': main()
