#!/usr/bin/env python3
"""Independent finite-law audit. Python standard library only, offline.

Core enumeration and counterevaluations do not import author code. BFS tree
portraits, direct point actions, full fixed alphabets, and a deterministic
SHA-256-derived assignment bank differ from the author's recursive witnesses.
Author code is imported only in explicitly identified cross-checks.
"""
import argparse
import hashlib
import types
import itertools
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
import subprocess
import sys
import zipfile

MANIFEST_SHA = '7945b043809987bd5e6af09ee2bd279aaca7855698d9d556cd17a0c081b85aa5'
ZIP_SHA = '6a4403908dcf263fe30c005e94078c116cbb4a6e14db6009b3ac865576a68fb0'
COUNTS = {4: 1, 6: 3, 8: 27, 10: 190, 12: 1510, 14: 11851}

def require(test, message):
    if not test:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def normalize(w):
    seen = []
    out = []
    for letter in w:
        same = next((j for j, a in enumerate(seen) if abs(a) == abs(letter)), None)
        if same is None:
            seen.append(letter)
            same = len(seen) - 1
        out.append((same + 1) if seen[same] == letter else -(same + 1))
    return tuple(out)

def fixed_words(rank, length, start=None):
    alphabet = tuple(range(-rank, 0)) + tuple(range(1, rank + 1))
    layer = [()] if start is None else [(start,)]
    def visit(w):
        if len(w) == length:
            yield w
        else:
            for a in alphabet:
                if not w or a != -w[-1]:
                    yield from visit(w + (a,))
    for w in layer:
        yield from visit(w)

def balanced(w):
    counts = Counter(w)
    return all(counts[a] == counts[-a] for a in counts)

def candidates(rank, length):
    # Do not prune by running exponent sums, rank, or normal-form properties.
    # Enumerate fixed-alphabet reduced strings first, then filter/canonicalize.
    return {normalize(w) for w in fixed_words(rank, length, 1)
            if w[-1] != -1 and balanced(w)}

def full_dp_count(length):
    states = {(a, a, int(a == 1)-int(a == -1), int(a == 2)-int(a == -2)): 1
              for a in (-2, -1, 1, 2)}
    for _ in range(length-1):
        nxt = defaultdict(int)
        for (first,last,ex,ey),number in states.items():
            for a in (-2,-1,1,2):
                if a != -last:
                    key = (first,a,ex+int(a==1)-int(a==-1),ey+int(a==2)-int(a==-2))
                    nxt[key] += number
        states = nxt
    return sum(v for (first,last,ex,ey),v in states.items()
               if last != -first and ex == 0 and ey == 0)

@lru_cache(None)
def bfs_permutation(depth, code):
    require(0 <= code < 1 << ((1 << depth)-1), 'Portrait out of range')
    result = []
    for leaf in range(1 << depth):
        node = 0
        image = 0
        for shift in range(depth-1,-1,-1):
            bit = (leaf >> shift) & 1
            image = (image << 1) | (bit ^ ((code >> node) & 1))
            node = 2*node+1+bit
        result.append(image)
    return tuple(result)

def inv(p):
    q = [0]*len(p)
    for x,y in enumerate(p):
        q[y] = x
    return tuple(q)

def is_tree(p):
    if sorted(p) != list(range(len(p))):
        return False
    depth = len(p).bit_length()-1
    return all(len({p[x] >> shift for x in range(block,block+(1<<shift))}) == 1
               for shift in range(depth+1)
               for block in range(0,len(p),1<<shift))

def signed_perms(depth, codes):
    result = {}
    for i,c in enumerate(codes,1):
        result[i] = bfs_permutation(depth,c)
        result[-i] = inv(result[i])
    return result

def moved(w, perms):
    for leaf in range(len(next(iter(perms.values())))):
        image = leaf
        for letter in w:
            image = perms[letter][image]
        if image != leaf:
            return leaf,image
    return None

def value(w,perms):
    out = list(range(len(next(iter(perms.values())))))
    for a in w:
        out = [perms[a][x] for x in out]
    return tuple(out)

@lru_cache(None)
def bank(depth, rank, trial):
    bits = (1 << depth)-1
    codes = tuple(int.from_bytes(hashlib.sha256(
        ('binary-wreath-independent/%d/%d/%d' % (depth,trial,i)).encode()).digest(), 'big')
        & ((1 << bits)-1) for i in range(rank))
    return codes,signed_perms(depth,codes)

def own_certificate(depth, w):
    rank = max(map(abs,w))
    for trial in range(4096):
        codes,perms = bank(depth,rank,trial)
        point = moved(w,perms)
        if point is not None:
            require(all(is_tree(perms[i]) for i in range(1,rank+1)), 'Invalid tree action')
            return [list(w),list(codes),list(point)],trial
    raise RuntimeError('Assignment bank exhausted; no conclusion for ' + repr(w))

def preorder_to_bfs(depth, code):
    index = 0
    result = 0
    def walk(node, remaining):
        nonlocal index,result
        if remaining == 0:
            return
        result |= ((code >> index)&1) << node
        index += 1
        walk(node*2+1,remaining-1)
        walk(node*2+2,remaining-1)
    walk(0,depth)
    return result

def jsonline(row):
    return json.dumps(row,separators=(',',':')).encode()+b'\n'

def main(author):
    out = {'status':'PASS','problem_id':1200005,'scope':'Scoped partial claims only; full target remains unsolved'}
    manifest_bytes = (author/'MANIFEST.json').read_bytes()
    require(sha(manifest_bytes) == MANIFEST_SHA, 'Wrong author manifest')
    manifest = json.loads(manifest_bytes)
    allowed = set(manifest['files']) | {'MANIFEST.json'}
    require({p.name for p in author.iterdir() if p.is_file()} == allowed,'Author allowlist mismatch')
    for name,metadata in manifest['files'].items():
        raw = (author/name).read_bytes()
        require(not (author/name).is_symlink(),'Author symlink')
        require(len(raw)==metadata['bytes'] and sha(raw)==metadata['sha256'],'Author binding mismatch '+name)
    archive = author.parent/'QUESTIONS_1200005_AUTHOR_SAFE_FREEZE.zip'
    if archive.exists():
        raw=archive.read_bytes()
        require(len(raw)==21562 and sha(raw)==ZIP_SHA,'Wrong freeze archive')
        with zipfile.ZipFile(archive) as z:
            names=z.namelist()
            require(len(names)==10 and len(set(names))==10,'Wrong archive count')
            for name in names:
                require(Path(name).name in allowed,'Unexpected archive member')
                require(z.read(name)==(author/Path(name).name).read_bytes(),'Archive differs '+name)
        out['freeze_archive_verified']=True
    out['author_binding']={'files':10,'manifest_sha256':MANIFEST_SHA}
    print('Author freeze verified.',file=sys.stderr)

    low = {m:candidates(3,m) for m in (4,6)}
    # Additional unoptimized F3 Cartesian-product check, including every first letter.
    full_f3 = {}
    for m in (4,6):
        full_f3[m] = {normalize(w) for w in itertools.product((-3,-2,-1,1,2,3),repeat=m)
                      if all(w[j]!=-w[(j+1)%m] for j in range(m)) and balanced(w)}
        require(low[m] == full_f3[m], 'F3 full alphabet mismatch')
    require([len(low[m]) for m in (4,6)] == [1,7],'Wrong F3 counts')
    high = {m:candidates(2,m) for m in range(4,16,2)}
    for m,s in high.items():
        require(len(s) == COUNTS[m],'Wrong F2 count')
        require(full_dp_count(m) == 8*len(s),'Full-alphabet DP count mismatch')
    own_hash = hashlib.sha256()
    own_trials=Counter()
    for depth, collection in ((3,low),(4,high)):
        for m in sorted(collection):
            for w in sorted(collection[m]):
                cert,trial=own_certificate(depth,w)
                own_hash.update(jsonline([depth,cert]))
                own_trials[depth]=max(own_trials[depth],trial+1)
    out['independent_core']={
        'depth3_all_rank_candidate_counts':{str(m):len(s) for m,s in low.items()},
        'depth4_rank_two_candidate_counts':{str(m):len(s) for m,s in high.items()},
        'full_fixed_alphabet_dp_counts':{str(m):full_dp_count(m) for m in high},
        'explicit_counterevaluations':sum(map(len,low.values()))+sum(map(len,high.values())),
        'certificate_stream_sha256':own_hash.hexdigest(),
        'maximum_bank_trials_per_candidate':dict(own_trials),
        'independent_of_author_enumerator_witness_and_law_routines':True}
    print('Independent full coverage and all counterevaluations passed.',file=sys.stderr)

    # Exhaustive BFS portrait membership, orders, and central half-powers.
    orders={}
    for depth in range(1,5):
        distribution=Counter()
        ident=tuple(range(1<<depth))
        central=tuple(x^1 for x in ident)
        for code in range(1 << ((1 << depth)-1)):
            p=bfs_permutation(depth,code)
            require(is_tree(p),'Invalid BFS portrait')
            power=p
            exponent=1
            while power != ident:
                power=tuple(power[x] for x in power)
                exponent *= 2
                require(exponent <= 1 << depth,'Exponent failure')
            distribution[exponent]+=1
            half=ident
            for _ in range(1 << (depth-1)):
                half=tuple(p[x] for x in half)
            require(half in (ident,central),'Central half-power failure')
        require(max(distribution)==1 << depth,'Exact exponent not attained')
        orders[str(depth)]={str(k):v for k,v in sorted(distribution.items())}
    out['independent_order_and_halfpower_distributions']=orders

    sys.dont_write_bytecode=True
    ac=types.ModuleType('author_controls')
    # Compile the bound source explicitly; never trust an unbound local .pyc.
    exec(compile((author/'controls.py').read_bytes(),str(author/'controls.py'),'exec'),ac.__dict__)
    expected=json.loads((author/'CONTROL_RESULTS.json').read_text())
    cross={}
    for depth, collection,key in ((3,low,'depth3'),(4,high,'depth4')):
        stream=hashlib.sha256()
        total=0
        for m,words in collection.items():
            generated=list(ac.balanced_cyclic_words(m,m//2 if depth==3 else 2))
            require(len(generated)==len(set(generated)) and set(generated)==words,'Author coverage mismatch')
            for w in generated:
                v=ac.witness(depth,w)
                require(v is not None,'Missing author certificate')
                pp={}
                for variable,code in v.items():
                    pp[variable]=bfs_permutation(depth,preorder_to_bfs(depth,code))
                    pp[-variable]=inv(pp[variable])
                p=value(w,pp)
                require(p!=tuple(range(1<<depth)),'Invalid author certificate')
                require(p==ac.evaluate(depth,w,v),'Author evaluation mismatch')
                stream.update(jsonline([w,sorted(v.items()),p]))
                total+=1
        require(stream.hexdigest()==expected['checks'][key+'_witness_stream_sha256'],'Wrong author witness-stream hash')
        cross[key]={'coverage_and_certificate_count':total,'stream_sha256':stream.hexdigest()}
    # Every author portrait through depth four agrees with independent BFS encoding.
    portrait_total=0
    for depth in range(1,5):
        for code in range(1 << ((1 << depth)-1)):
            p=bfs_permutation(depth,preorder_to_bfs(depth,code))
            require(ac.permutation(depth,code)==p,'Portrait action mismatch')
            require(ac.permutation(depth,ac.inverse(depth,code))==inv(p),'Portrait inverse mismatch')
            portrait_total+=1
    cross['all_author_portraits_depth1_to4']=portrait_total
    # Check the eight explicitly printed depth-three certificates, not only code output.
    proof_rows=[((1,2,-1,-2),(8,2)),((1,1,2,-1,-1,-2),(48,1)),
        ((1,2,-1,-1,-2,1),(48,1)),((1,2,-1,3,-2,-3),(0,8,2)),
        ((1,2,2,-1,-2,-2),(8,17)),((1,2,3,-1,-2,-3),(0,8,2)),
        ((1,2,3,-1,-3,-2),(8,0,2)),((1,2,3,-2,-1,-3),(8,0,2))]
    require({w for w,c in proof_rows}==low[4]|low[6],'Printed proof table incomplete')
    for w,c in proof_rows:
        pp=signed_perms(3,tuple(preorder_to_bfs(3,x) for x in c))
        require(value(w,pp)[0]==1,'Printed proof-table witness fails')
    cross['explicit_proof_table_rows']=len(proof_rows)
    brute_count=0
    words=[]
    for m in range(1,7):
        for w in fixed_words(2,m):
            words.append(w)
            direct=all(moved(w,signed_perms(2,c)) is None for c in itertools.product(range(8),repeat=2))
            require(direct==ac.law(2,w),'Recursive criterion disagreement')
            brute_count+=1
    cross['independent_direct_W2_vs_author_criterion']=brute_count
    # Check the constructive linear bound on F2 up to length six independently.
    for w in words:
        depth=len(w)
        v=ac.prefix_witness(w)
        pp={}
        for variable,code in v.items():
            pp[variable]=bfs_permutation(depth,preorder_to_bfs(depth,code))
            pp[-variable]=inv(pp[variable])
            require(is_tree(pp[variable]),'Prefix certificate not tree action')
        path=[0]
        for a in w:
            path.append(pp[a][path[-1]])
        require(len(set(path))==len(w)+1,'Prefix separation failure')
    cross['independently_checked_prefix_certificates']=len(words)
    # Deliberate malformed certificate negative controls and normalization controls.
    require(moved((1,2,-1,-2),signed_perms(4,(0,0))) is None,'Bad negative control')
    symmetries=0
    for m,ws in high.items():
        for w in ws:
            # Variable inversion, swapping variables, cyclic conjugacy, word inverse.
            for transformed in (tuple(-x for x in reversed(w)),w[1:]+w[:1],
                tuple(-x if abs(x)==1 else x for x in w),
                tuple((3-abs(x))*(1 if x>0 else -1) for x in w)):
                require(normalize(transformed) in ws,'Symmetry coverage missing')
                symmetries+=1
    cross['depth4_symmetry_membership_checks']=symmetries
    out['author_cross_checks']=cross
    replay=subprocess.run([sys.executable,'-B',str(author/'verify.py')],capture_output=True,text=True,check=True)
    out['author_offline_replay']=json.loads(replay.stdout)
    out['checks_use_explicit_exceptions_not_assert_statements']=True
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--author',type=Path,default=Path(__file__).resolve().parent.parent/'questions_1200005'/'safe_output')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=main(args.author.resolve())
    rendered=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end='')
