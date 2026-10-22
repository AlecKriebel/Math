#!/usr/bin/env python3
"""Second-audit controls; imports only the independent reviewer checker, never author code."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import sympy as S

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_reviewer_checker', HERE / 'independent_check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

def need(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def run(packet):
    packet = packet.resolve()
    need(digest((packet/'MANIFEST.json').read_bytes()) == 'd1e1467c6d36b6c62283af2ec50ddff8864020ad8a7c9e0ba9a6704dacb4246a', 'wrong author manifest')
    manifest = json.loads((packet/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        data = (packet/entry['path']).read_bytes()
        need(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'author file mismatch: '+entry['path'])
    check.PACKET = packet
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        check.run()
    original = (HERE/'INDEPENDENT_RESULTS.json').read_bytes()
    need(out.getvalue().encode() == original, 'independent replay differs from preserved output')
    w = check.target()
    matrix_controls = [([], [0,0,0]), ([[0]], [0,0,1]), ([[0,1],[1,0]], [1,1,0]), ([[2,0],[0,-3]], [1,1,0]), ([[0,0],[0,0]], [0,0,2]), ([[1,1],[1,1]], [1,0,1])]
    for matrix, expected in matrix_controls:
        need(check.inertia(S.Matrix(matrix))[0] == expected, 'matrix control failed')
    grid = []
    for powers in itertools.product((-4,-2,2,4), repeat=4):
        word = [x for i,p in enumerate(powers) for x in [(i%2+1)*(1 if p>0 else -1)]*abs(p)]
        G,mu = check.block_goeritz(word)
        P,pmu,pdata = check.planar_goeritz(word)
        need(P.extract(pdata['cycle_order'],pdata['cycle_order']) == G, 'control planar matrix mismatch')
        need(mu == pmu, 'control correction mismatch')
        inertia = check.inertia(P)[0]
        signature = inertia[0]-inertia[1]-pmu
        need(signature == check.braid_signature(word)[0], 'control independent signatures disagree')
        grid.append({'powers':powers,'signature':signature})
    transformations = []
    for name, word, expected in [('inverse',check.inverse(w),2), ('mirror',[-x for x in w],2), ('reverse',w[::-1],-2), ('double',w+w,-4)]+[('rotation_'+str(k),w[k:]+w[:k],-2) for k in (0,1,13,52,103)]:
        P,mu,_ = check.planar_goeritz(word)
        it = check.inertia(P)[0]
        signature = it[0]-it[1]-mu
        need(signature == expected == check.braid_signature(word)[0], 'transformation control failed: '+name)
        transformations.append({'name':name,'length':len(word),'signature':signature})
    relation_count = 0
    for prefix in [[],[1],[-2,1],[1,2,-1,-2]]:
        for suffix in [[],[-1],[2,1]]:
            left = check.braid_signature(prefix+[1,2,1]+suffix)
            right = check.braid_signature(prefix+[2,1,2]+suffix)
            need(left[:2] == right[:2], 'Artin relation failure')
            relation_count += 1
    cancellation_count = 0
    for k in (0,13,52,104):
        for x in (1,-1,2,-2):
            word=w[:k]+[x,-x]+w[k:]
            need(check.braid_signature(word)[:2] == check.braid_signature(w)[:2], 'inverse-pair failure')
            cancellation_count += 1
    conjugation_count=0
    for p in ([1],[-2],[1,2],[-1,2,-1]):
        need(check.braid_signature(list(p)+w+check.inverse(list(p)))[0] == -2, 'conjugation failure')
        conjugation_count += 1
    a=[1,1]; b=[2,2]; c=check.comm(a,b)
    d=check.reduce_word(check.inverse(a)+c+a)
    e=check.reduce_word(check.inverse(b)+c+b)
    u=check.comm(c,d); v=check.comm(d,e)
    nested={name:check.braid_signature(word)[0] for name,word in [('a',a),('b',b),('c',c),('d',d),('e',e),('u',u),('v',v),('beta',check.comm(u,v))]}
    need(nested == {'a':-1,'b':-1,'c':0,'d':0,'e':0,'u':2,'v':0,'beta':-2}, 'nested values differ')
    G,_=check.block_goeritz(w)
    wrong=G.copy(); bs=check.blocks(w); B=[e for g,e in bs[1::2]]; start=0
    for j,b in enumerate(B):
        previous=1 if B[j-1]>0 else -1
        for k in range(abs(b)):
            i=(start+k)%G.rows; h=(i+1)%G.rows
            wrong[i,h]=wrong[h,i]=previous
        start+=abs(b)
    wrong_entries=sum(G[i,j]!=wrong[i,j] for i in range(G.rows) for j in range(G.cols))
    need(wrong_entries>0, 'printed-index negative control failed')
    return {'status':'PASS_SECOND_AUDIT_RECOVERY_CONTROLS','author_manifest_sha256':digest((packet/'MANIFEST.json').read_bytes()),'author_entries_verified':len(manifest['files']),'preserved_independent_output_sha256':digest(original),'preserved_output_reproduced_byte_for_byte':True,'sympy_version':S.__version__,'matrix_controls':len(matrix_controls),'four_syllable_three_method_controls':len(grid),'four_syllable_results_sha256':digest(json.dumps(grid,sort_keys=True,separators=(',',':')).encode()),'diagram_meyer_transformations':transformations,'artin_relation_controls':relation_count,'inverse_pair_controls':cancellation_count,'conjugation_controls':conjugation_count,'nested_expression_signatures':nested,'non_homomorphism_explicitly_preserved':True,'printed_previous_block_index_negative_control':{'entry_mismatches':wrong_entries,'incorrect_inertia':check.inertia(wrong)[0],'rejected_by_diagram_matrix_comparison':True}}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-packet',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.author_packet),sort_keys=True,indent=2))
