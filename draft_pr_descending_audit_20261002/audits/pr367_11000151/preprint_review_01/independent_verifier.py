#!/usr/bin/env python3
"""Fresh review01: parity-derived strand orders, full records, standard library.

No candidate module is imported or executed. Candidate bytes are read-only.
Run python3 -B independent_verifier.py --package ../preprint
The program outputs its complete receipt to stdout and writes nothing.
"""
import argparse
import datetime
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parent.parent/'preprint')
args = parser.parse_args()
base = args.package.resolve()
checks = 0
def check(value, context):
    global checks
    if not value: raise AssertionError(context)
    checks += 1

def inverse(word): return tuple(-v for v in reversed(word))
def multiply_parts(parts):
    result = []
    for part in parts:
        for letter in part:
            if result and result[-1] == -letter: result.pop()
            else: result.append(letter)
    return tuple(result)
def apply(images, table):
    return tuple(multiply_parts(table[a-1] if a>0 else inverse(table[-a-1]) for a in word) for word in images)
def identity(n): return tuple((j,) for j in range(1,n+1))
def action(word, tables):
    result = identity(len(tables[0]))
    for letter in word:
        result = apply(result, tables[letter-1])
    return result

archive = base/'wajnryb-artin-a5-verification.zip'
member_receipts=[]
with zipfile.ZipFile(archive) as z:
    names = z.namelist()
    check(len(names)==len(set(names)), 'ZIP duplicate names')
    check(z.testzip() is None, 'ZIP CRC')
    for info in z.infolist():
        name=info.filename
        check(not name.startswith('/') and '..' not in Path(name).parts, ('ZIP path',name))
        check((info.external_attr>>16)&0o170000 != 0o120000, ('ZIP symlink',name))
        data=z.read(name)
        check(data==(base/name).read_bytes(), ('ZIP/disk literal equality',name))
        if name.endswith('.gz'):
            raw=gzip.decompress(data)
            text=raw.decode('utf-8')
            if name.endswith('.jsonl.gz'):
                for line in text.splitlines(): json.loads(line)
        else:
            text=data.decode('utf-8')
            if name.endswith('.json'): json.loads(text)
        member_receipts.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    manifest=json.loads(z.read('verification/MANIFEST.json'))
    expected={'verification/'+r['path'] for r in manifest['files']}
    check(set(names)==expected|{'verification/MANIFEST.json','fixed_generator_classification.tex'}, 'closed ZIP manifest')
    for row in manifest['files']:
        data=z.read('verification/'+row['path'])
        check(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'], ('package manifest',row['path']))

sealed=json.loads((base/'INITIAL_REVIEW_PACKAGE.json').read_bytes())
for row in sealed['sealed_files']:
    data=(base/row['path']).read_bytes()
    check(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'], ('initial package seal',row['path']))

f4=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),
    ((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),
    ((1,),(2,),(3,),(3,-2,1,4))]
f4inv=[((1,),(-1,2),(-1,3),(-1,4)),((2,),(2,-1,2),(3,),(4,)),
       ((1,),(3,),(3,-2,3),(4,)),((1,),(2,),(4,),(4,-3,4)),
       ((1,),(2,),(3,),(-1,2,-3,4))]
for i in range(5):
    check(apply(f4[i],f4inv[i])==identity(4), ('F4 inverse right',i))
    check(apply(f4inv[i],f4[i])==identity(4), ('F4 inverse left',i))
    for j in range(i+1,5):
        left=(i+1,j+1,i+1) if j==i+1 else (i+1,j+1)
        right=(j+1,i+1,j+1) if j==i+1 else (j+1,i+1)
        check(action(left,f4)==action(right,f4), ('F4 relation',i,j))
c=(1,2,3,4)*5
h=(5,4,3,2,1,1,2,3,4,5)
check(action(c,f4)==action(h,f4), 'F4 quotient relator')
target4=action(c+c,f4)
check(target4==action(h+h,f4), 'F4 target')
star_rows={}
counts=[]
kept=[]
for start in range(6):
    # Enumerate literal generator words while tracking actual labelled strands.
    # Other labels may never cross. Counts refer to labels, not walk edges.
    frontier=[(tuple(range(6)),(0,)*6,(),identity(4))]
    for depth in range(20):
        following=[]
        for order,count,word,images in frontier:
            for g in range(5):
                pair=order[g:g+2]
                if start not in pair: continue
                other=pair[0] if pair[1]==start else pair[1]
                if count[other]==4: continue
                neworder=list(order);neworder[g],neworder[g+1]=neworder[g+1],neworder[g]
                newcount=list(count);newcount[other]+=1
                following.append((tuple(neworder),tuple(newcount),word+(g+1,),apply(images,f4[g])))
        frontier=following
    census=accepted=0
    for order,count,word,images in frontier:
        if order!=tuple(range(6)): continue
        check(all(count[j]==4 for j in range(6) if j!=start), 'star full label count')
        census+=1;accepted+=images==target4
        check(word not in star_rows, 'star unique words')
        star_rows[word]=(start+1,images,images==target4)
    counts.append(census);kept.append(accepted)
check(counts==[81,162,162,162,162,81] and kept==[1,2,2,2,2,1], 'star census')
check(len(star_rows)==810, 'all810 enumerated')
with gzip.open(base/'verification/certificates/20_full_actions.jsonl.gz','rt') as f:
    records=[json.loads(line) for line in f]
check(len(records)==810 and len({tuple(r['word']) for r in records})==810,'810 stored distinct')
for r in records:
    expected=star_rows[tuple(r['word'])]
    check(expected==(r['center'],tuple(tuple(w) for w in r['images']),r['survives']), ('full F4 record',r['word']))
check({word for word,(_,_,survives) in star_rows.items() if survives}=={(h+h)[k:]+(h+h)[:k] for k in range(20)}, 'ten literal rotations')
bad=list(f4);bad[4]=((1,),(2,),(3,),(3,-2,4))
check(action(c,bad)!=action(h,bad),'negative F4 relator mutation')

pairs=list(itertools.combinations(range(6),2))
powers={pair:3**j for j,pair in enumerate(pairs)}
FULL=3**15-1
def order_from_parities(code):
    # Reconstruct the entire order independently; no stored swap permutation.
    predecessors=[0]*6
    for a,b in pairs:
        odd=((code//powers[a,b])%3)%2
        predecessors[a if odd else b]+=1
    check(sorted(predecessors)==list(range(6)), ('parity order consistency',code))
    order=[0]*6
    for label,pos in enumerate(predecessors): order[pos]=label
    return tuple(order)
def transitions(code,direction):
    order=order_from_parities(code)
    # Explore generators in reverse order to differ from original parent paths.
    for g in range(4,-1,-1):
        pair=tuple(sorted(order[g:g+2]));power=powers[pair];digit=code//power%3
        if (direction>0 and digit==2) or (direction<0 and digit==0):continue
        yield code+direction*power,g+1
def explore(start,direction):
    reached={start:None};queue=[start];edges=0
    for code in queue:
        for successor,g in transitions(code,direction):
            edges+=1
            if successor not in reached:
                reached[successor]=(code,g);queue.append(successor)
    return reached,queue,edges
forward,queue,forward_edges=explore(0,1)
backward,_,backward_edges=explore(FULL,-1)
co=set(forward)&set(backward)
check(co=={q for q in forward if FULL-q in forward}, 'complement/reverse coaccessibility')
check(len(forward)==len(backward)==234368 and forward_edges==backward_edges==711342,'full independent graph counts')
check(len(co)==90921, '90921 coaccessible')
f6=[]
for g in range(1,6):
    table=list(identity(6));table[g-1]=(g,g+1,-g);table[g]=(g,);f6.append(tuple(table))
for i in range(5):
    for j in range(i+1,5):
        left=(i+1,j+1,i+1) if j==i+1 else (i+1,j+1)
        right=(j+1,i+1,j+1) if j==i+1 else (j+1,i+1)
        check(action(left,f6)==action(right,f6), ('F6 braid/commutation',i,j))
check(action(c+h,f6)==action((1,2,3,4,5)*6,f6),'full twist decomposition')
f6inv=[]
for g in range(1,6):
    table=list(identity(6));table[g-1]=(g+1,);table[g]=(-g-1,g,g+1);f6inv.append(tuple(table))
def signed_action(word):
    result=identity(6)
    for letter in word: result=apply(result,(f6 if letter>0 else f6inv)[abs(letter)-1])
    return result
for g in range(1,6):
    check(signed_action((g,-g))==signed_action((-g,g))==identity(6),('F6 inverse',g))
    z=(1,2,3,4,5)*6
    check(signed_action(z+(g,))==signed_action((g,)+z),('F6 central full twist',g))
d=(1,2,3,4,5)
for g in range(1,5):check(signed_action(d+(g,)+inverse(d))==signed_action((g+1,)),('shift conjugation',g))
check(signed_action(d+c+c+inverse(d))==signed_action((2,3,4,5)*10),'second forty model')
def signed_linking(word):
    order=list(range(6));crossings={pair:0 for pair in pairs}
    for letter in word:
        g=abs(letter)-1;pair=tuple(sorted(order[g:g+2]));crossings[pair]+=1 if letter>0 else -1
        order[g],order[g+1]=order[g+1],order[g]
    check(order==list(range(6)) and all(v%2==0 for v in crossings.values()),'pure signed linking')
    return tuple(crossings[pair]//2 for pair in pairs)
relator=c+inverse(h)
check(signed_linking(c+c)==tuple(2 if b<5 else 0 for a,b in pairs),'target linking15')
expected_patterns={tuple(1-2*(k in pair) for pair in pairs) for k in range(6)}
conjugators=[(),(5,),(4,5),(3,4,5),(2,3,4,5),(1,2,3,4,5)]
check({signed_linking(b+relator+inverse(b)) for b in conjugators}==expected_patterns,'six relator conjugation patterns')
check(all(sum(pattern)==5 for pattern in expected_patterns),'linking T coefficient5')
def subgroup(generators):
    generated={tuple(range(6))};queue=list(generated)
    for p in queue:
        for g in generators:
            q=list(p);q[g-1],q[g]=q[g],q[g-1];q=tuple(q)
            if q not in generated:generated.add(q);queue.append(q)
    return generated
first=subgroup(range(1,5));second=subgroup(range(2,6))
check(len(first)==len(second)==120 and first!=second,'strict subgroups distinct')
check(all(p[5]==5 for p in first) and all(p[0]==0 for p in second),'strict subgroup fixed vertices')
images={0:identity(6)}
for code in queue:
    if code==0 or code not in co: continue
    parent,g=forward[code]
    check(parent in images,'coaccessible parent')
    images[code]=apply(images[parent],f6[g-1])
edge_comparisons=0
for code in queue:
    if code not in co:continue
    for successor,g in transitions(code,1):
        if successor not in co:continue
        check(apply(images[code],f6[g-1])==images[successor],('complete edge action',code,g,successor))
        edge_comparisons+=1
check(edge_comparisons==261810,'261810 full equalities')
check(images[FULL]==action((1,2,3,4,5)*6,f6),'terminal action equals full twist')
raw_bytes=0;digest=hashlib.sha256();record_count=0
with gzip.open(base/'verification/certificates/30_action_records.txt.gz','rb') as source:
    for code in sorted(co):
        packed=sum(label<<(3*pos) for pos,label in enumerate(order_from_parities(code)))
        actual=('S|'+str(code)+'|'+str(packed)+'|'+'|'.join(','.join(map(str,w)) for w in images[code])+'\n').encode()
        stored=source.readline()
        check(actual==stored,('full literal stored F6 record',code))
        raw_bytes+=len(actual);digest.update(actual);record_count+=1
    check(source.read()==b'','no extra stored records')
check(record_count==90921 and raw_bytes==15258431,'full raw stream count/bytes')
def count_word(word):
    code=0;order=list(range(6))
    for g in word:
        i=g-1;code+=powers[tuple(sorted(order[i:i+2]))];order[i],order[i+1]=order[i+1],order[i]
    return code,tuple(order)
collision=count_word((1,1,2,2))
check(collision==count_word((2,2,1,1)),'negative same count/order')
check(action((1,1,2,2),f6)!=action((2,2,1,1),f6),'negative unequal action')
check(collision[0] in forward and collision[0] not in co,'negative collision outside coaccessible')
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'PASS','mechanism':'Fresh parity-derived order, bidirectional graph, reversed generator order, full tuple substitutions; literal comparison of every stored record; no candidate imports',
    'checks':checks,'archive_members':len(member_receipts),'archive_member_receipts':member_receipts,
    'F4_presentation_equalities':22,'twenty_words':len(star_rows),'twenty_candidate_counts':counts,'twenty_survivor_counts':kept,
    'forward_states':len(forward),'forward_edges':forward_edges,'backward_states':len(backward),'backward_edges':backward_edges,
    'full_coaccessible_records':record_count,'full_edge_comparisons':edge_comparisons,'full_record_raw_bytes':raw_bytes,
    'full_record_sha256':digest.hexdigest(),'negative_controls':['mutated F4 quotient relator','unequal positive prefixes at identical count/permutation outside coaccessible graph']},indent=2))
