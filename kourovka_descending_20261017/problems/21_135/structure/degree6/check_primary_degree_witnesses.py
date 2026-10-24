#!/usr/bin/env python3
"""Read ordinary identity columns from primary CTblLib source, never execute it.

Reads MOT's first-column integer entries and GALOIS row references. For A7
covers reads ARC's projectives: these are projective characters of A7 that
lift to ordinary characters of the designated central cover (see ConstructProj).
"""
from pathlib import Path
from collections import Counter
from math import prod
import re,json,hashlib

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources'

def split_top(s):
    pieces=[];start=0;depth=0;quote=False;escape=False
    for i,ch in enumerate(s):
        if quote:
            if escape:escape=False
            elif ch=='\\':escape=True
            elif ch=='"':quote=False
        elif ch=='"':quote=True
        elif ch in '[({':depth+=1
        elif ch in '])}':depth-=1
        elif ch==',' and depth==0:
            pieces.append(s[start:i].strip());start=i+1
    pieces.append(s[start:].strip())
    return pieces

def function_args(text,prefix):
    loc=text.index(prefix);start=text.index('(',loc);depth=1;quote=False;escape=False
    for i in range(start+1,len(text)):
        ch=text[i]
        if quote:
            if escape:escape=False
            elif ch=='\\':escape=True
            elif ch=='"':quote=False
        elif ch=='"':quote=True
        elif ch=='(':depth+=1
        elif ch==')':
            depth-=1
            if depth==0:return split_top(text[start+1:i])
    raise ValueError('unbalanced call')

def list_items(s):
    assert s.startswith('[') and s.endswith(']')
    return [x for x in split_top(s[1:-1]) if x]

def row_degrees(s):
    out=[]
    for row in list_items(s):
        m=re.match(r'\[\s*(\d+)\s*[,\]]',row)
        if m:out.append(int(m.group(1)));continue
        m=re.match(r'\[GALOIS,\[\s*(\d+)\s*,',row)
        assert m, row[:60]
        i=int(m.group(1));assert 1<=i<=len(out)
        out.append(out[i-1])
    return out

def find_mot(group):
    prefix='MOT('+json.dumps(group)+','
    for file in SRC.glob('*.tbl'):
        text=file.read_text()
        if prefix in text:
            args=function_args(text,prefix)
            if args[4].startswith('['):
                deg=row_degrees(args[4]);order=int(list_items(args[2])[0])
                assert sum(d*d for d in deg)==order,(group,deg,order)
                return {'group':group,'source':file.name,'source_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
                    'degrees':deg,'order':order,'number_classes':len(list_items(args[2]))}
    raise ValueError(group)

def projective_a7():
    file=SRC/'ctoalter.tbl';text=file.read_text()
    args=function_args(text,'ARC("A7","projectives",')
    items=list_items(args[2]);out={}
    for i in range(0,len(items),2):
        name=json.loads(items[i]);deg=row_degrees(items[i+1])
        assert sum(d*d for d in deg)==2520
        out[name]=deg
    return out

def in_edge_monoid(d):
    # Necessary invariant only; failure certifies absence for every power.
    vals=[];rem=d
    for p in (2,3,5,7):
        a=0
        while rem%p==0:rem//=p;a+=1
        vals.append(a)
    return rem==1 and sum(vals)%2==0 and max(vals)<=sum(vals)-max(vals)

def main():
    groups=['A5','A6','A7','L2(7)','U4(2)','U3(3)','U4(3)','J2','L3(4)']
    tables={g:find_mot({'L2(7)':'L3(2)'}.get(g,g)) for g in groups}
    proj=projective_a7()
    witnesses={'A5':3,'A6':5,'L2(7)':3,'U4(2)':5,'U3(3)':7,'U4(3)':189,'J2':63,'L3(4)':20}
    for g,d in witnesses.items():
        assert d in tables[g]['degrees']
        assert not in_edge_monoid(d)
    assert 24 in proj['3.A7'] and not in_edge_monoid(24)
    assert 24 in proj['6.A7']
    assert 4 in proj['2.A7'] and not in_edge_monoid(4)
    assert Counter(tables['A7']['degrees'])==Counter({1:1,6:1,10:2,14:2,15:1,21:1,35:1})
    covers={}
    for m in [2,3,6]:
        a=list(tables['A7']['degrees'])
        for d in [2,3,6]:
            if m%d==0:
                multiplicity={2:1,3:2,6:2}[d]
                a+=proj[str(d)+'.A7']*multiplicity
        assert sum(z*z for z in a)==m*2520
        covers[str(m)+'.A7']={'degrees':a,'order':m*2520}
    data={'method':'Read primary ordinary MOT identity columns and projective ARC rows; resolve Galois references by degree; exact square sums.',
          'tables':tables,'A7_projective_rows':proj,'reconstructed_A7_covers':covers,
          'forbidden_witnesses':witnesses,'cover_witnesses':{'3.A7':24,'6.A7':24},
          'warning':'Character-table witness check only, not verification of Lindsey classification or a full Kourovka21.135 solution.'}
    path=ROOT/'primary_degree_witnesses.json';path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'simple_tables_checked':len(tables),'A7_cover_square_sums_checked':3,'forbidden_witnesses_checked':len(witnesses)+2,'output':str(path)},sort_keys=True))
if __name__=='__main__':main()
