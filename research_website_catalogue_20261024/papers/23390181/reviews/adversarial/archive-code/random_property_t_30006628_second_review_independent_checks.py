#!/usr/bin/env python3
"""Independent finite diagnostics. These do not certify an asymptotic theorem."""
import collections, hashlib, itertools, json, pathlib, zipfile

def check(test, label):
    if not test:
        raise RuntimeError(label)

def all_words(colors, length):
    def visit(prefix):
        if len(prefix) == length:
            yield prefix
        else:
            for a, color in enumerate(colors):
                if not prefix or color != colors[prefix[-1]]:
                    yield from visit(prefix + (a,))
    yield from visit(())

def inspect(sizes, ell, inversion_mode):
    colors = tuple(i for i, size in enumerate(sizes) for j in range(size))
    inv = list(range(len(colors)))
    if inversion_mode == 'paired':
        start = 0
        for size in sizes:
            for j in range(0, size-1, 2):
                inv[start+j], inv[start+j+1] = start+j+1, start+j
            start += size
    def reverse(w):
        return tuple(inv[a] for a in w[::-1])
    L, e = divmod(ell, 3)
    lengths = [L] * (3-e) + [L+1] * e
    types = sorted(set(lengths))
    good = {t: [w for w in all_words(colors,t) if w != reverse(w)] for t in types}
    vertices = tuple(w for t in types for w in good[t])
    vset = set(vertices)
    actual = collections.Counter()
    cyclic = retained = 0
    max_sample_degree = 0
    repeated_edge_samples = 0
    for rel in all_words(colors,ell):
        if colors[rel[0]] == colors[rel[-1]]:
            continue
        cyclic += 1
        blocks = []; i = 0
        for t in lengths:
            blocks.append(rel[i:i+t]); i += t
        if any(w not in vset for w in blocks):
            continue
        retained += 1
        incidence = collections.Counter()
        edges = []
        for j in range(3):
            x,y = reverse(blocks[j]), blocks[(j+1)%3]
            check(x != y, 'link loop')
            edges.append(tuple(sorted((x,y))))
            actual[x,y] += 1
            actual[y,x] += 1
            incidence[x] += 1; incidence[y] += 1
        max_sample_degree = max(max_sample_degree, max(incidence.values()))
        repeated_edge_samples += len(set(edges)) < 3
    check(max_sample_degree <= 3, 'degree bound')
    coef = collections.Counter()
    for i in range(3):
        t,u = lengths[i], lengths[(i+1)%3]
        coef[t,u] += 1; coef[u,t] += 1
    completion = {}
    for h in types:
        for a,b in itertools.product(range(len(colors)),repeat=2):
            completion[h,a,b] = sum(colors[a] != colors[w[0]] and colors[w[-1]] != colors[b] for w in good[h])
    mismatches = 0
    pair_count = 0
    for x,y in itertools.product(vertices,repeat=2):
        t,u = len(x),len(y)
        c = coef[t,u]
        expected = c * (colors[x[0]] != colors[y[0]]) * completion[ell-t-u,x[-1],y[-1]] if c else 0
        pair_count += 1
        mismatches += actual[x,y] != expected
    check(mismatches == 0, 'individual-vertex expected kernel')
    check(sum(actual.values()) == retained * 6, 'oriented mass')
    for h in types:
        check(all(completion[h,a,b] == completion[h,b,a] for a,b in itertools.product(range(len(colors)),repeat=2)), 'completion reversal')
    return {'sizes':sizes,'ell':ell,'inversion_mode':inversion_mode,'cyclic_words':cyclic,'retained_words':retained,'vertices':len(vertices),'individual_entries_verified':pair_count,'max_degree_per_sample':max_sample_degree,'samples_with_parallel_edges':repeated_edge_samples,'kernel_mismatches':mismatches}

def check_pins(root):
    frozen = root/'RANDOM_PROPERTY_T_30006628_AUTHOR_SAFE_FREEZE.zip'
    external = root/'RANDOM_PROPERTY_T_30006628_AUTHOR_EXTERNAL_MANIFEST.json'
    expected = [('archive',frozen,20225,'f5c4e06b7c535a98aa37520ff616b4b63b4bdd7eb100e461de733f7fd7192134'),('external_manifest',external,3285,'46011dfd09c59dc52c561886c31b0e8ed0c823f5d5f446baf2c5aa35448fdaf0')]
    for label,path,size,digest in expected:
        raw=path.read_bytes();check(len(raw)==size and hashlib.sha256(raw).hexdigest()==digest,label+' mismatch')
    metadata=json.loads(external.read_text())
    with zipfile.ZipFile(frozen) as z:
        check(set(z.namelist())=={x['path'] for x in metadata['members']},'archive member set')
        for x in metadata['members']:
            raw=z.read(x['path']);check(len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256'],'member mismatch '+x['path'])
        proof=z.read(metadata['proof_pin']['path'])
        check(proof==(root/'random_property_t_30006628/safe/PROOF.md').read_bytes(),'local proof mismatch')
    return {'archive_members_verified':len(metadata['members']),'archive_bytes':20225,'proof_bytes':len(proof),'proof_sha256':hashlib.sha256(proof).hexdigest()}

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--workspace',default=str(pathlib.Path(__file__).resolve().parents[2]));args=parser.parse_args()
    rows=[]
    for sizes,ells in [((1,1,1),range(6,13)),((2,1,1),range(6,10)),((3,2,1),range(6,10))]:
        for mode in ['self_inverse','paired']:
            if sizes==(1,1,1) and mode=='paired':continue
            for ell in ells:
                rows.append(inspect(sizes,ell,mode))
    print(json.dumps({'status':'PASS','scope':'Finite exact tests only; mathematical review is separate.','pins':check_pins(pathlib.Path(args.workspace)),'cases':rows,'total_cases':len(rows),'total_entries_verified':sum(x['individual_entries_verified'] for x in rows)},sort_keys=True,indent=2))
