#!/usr/bin/env python3
"""Finite split-quotient diagnostic. Not a mapping-class-group proof checker."""
import itertools,json,os,stat,sys
from pathlib import Path
class Reject(Exception):pass
def need(ok,message):
    if not ok:raise Reject(message)
def pairs(items):
    out={}
    for k,v in items:
        need(k not in out,'duplicate JSON key');out[k]=v
    return out
def bad_constant(value):raise Reject('nonfinite JSON value')
def read_json(path):
    p=Path(path); st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'input must be a regular nonlinked file')
    need(st.st_size<=1000000,'oversized JSON');return json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=bad_constant)
def exact(value,want):
    need(type(value) is type(want),'value type')
    if type(want) is dict:
        need(set(value)==set(want),'object keys')
        for k in want:exact(value[k],want[k])
    elif type(want) is list:
        need(len(value)==len(want),'list length')
        for a,b in zip(value,want):exact(a,b)
    else:need(value==want,'value mismatch')
def mat(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def transpose(a):return [list(x) for x in zip(*a)]
def det(a):
    # Exact fraction-free recursion is small here (6 x 6).
    if len(a)==1:return a[0][0]
    return sum((-1)**j*x*det([row[:j]+row[j+1:] for row in a[1:]]) for j,x in enumerate(a[0]) if x)
def shape(a,r,c):
    need(type(a) is list and len(a)==r,'matrix row shape')
    need(all(type(row) is list and len(row)==c and all(type(x) is int and abs(x)<=1000 for x in row) for row in a),'matrix scalar/column shape')
def check_claims(c):
    exact(c,{'schema':'positive-twist-claims-v1','problem_id':11000112,'rank':1012,'status':'prior-negative','approaches':0,'genus':3,'positive_factors':12,'quotient_rank':4,'torsion_free':True,'target_answer':'no','geometric_identity_dependency':'Baykur-2022-equation-47','novelty_claimed':False,'independent_review_performed':False,'formal_verification':False,'sharp_all_genera_bound_claimed':False,'finite_checks_certify_mapping_class_identity':False})
def check_certificate(c):
    need(type(c) is dict and set(c)=={'schema','basis','lattice_basis','quotient_map','section','rank','genus','factor_count'},'certificate keys')
    exact(c['schema'],'positive-twist-certificate-v1');exact(c['basis'],['a1','b1','a2','b2','a3','b3'])
    for key,want in [('rank',4),('genus',3),('factor_count',12)]:exact(c[key],want)
    l,q,s=c['lattice_basis'],c['quotient_map'],c['section'];shape(l,2,6);shape(q,4,6);shape(s,6,4)
    exact(l,[[1,0,0,0,1,0],[0,1,0,-1,0,1]])
    need(mat(q,transpose(l))==[[0,0] for _ in range(4)],'q does not kill lattice')
    need(mat(q,s)==ident(4),'q section not identity')
    residual=[[int(i==j)-mat(s,q)[i][j] for j in range(6)] for i in range(6)]
    coefficient=[[int(i==j) for j in range(6)] for i in range(2)]
    need(residual==mat(transpose(l),coefficient),'kernel decomposition fails')
    full=[list(row) for row in zip(l[0],l[1],*transpose(s))]
    need(abs(det(full))==1,'lattice not direct integral summand')
    grid=0
    for x in itertools.product((-1,0,1),repeat=6):
        col=[[v] for v in x];left=mat(s,mat(q,col));right=[[x[0]*l[0][i]+x[1]*l[1][i]] for i in range(6)]
        need([left[i][0]+right[i][0] for i in range(6)]==list(x),'finite decomposition control');grid+=1
    changes=0
    for k in range(-5,6):
        for sign1,sign2,swap in itertools.product((-1,1),(-1,1),(False,True)):
            ll=[[sign1*(l[0][i]+k*l[1][i]) for i in range(6)],[sign2*l[1][i] for i in range(6)]]
            if swap:ll.reverse()
            full2=[list(row) for row in zip(ll[0],ll[1],*transpose(s))]
            need(abs(det(full2))==1 and mat(q,transpose(ll))==[[0,0] for _ in range(4)],'unimodular basis control');changes+=1
    return {'schema':'positive-twist-diagnostics-v1','status':'PASS','problem_id':11000112,'genus':3,'positive_factors':12,'integral_quotient_rank':4,'torsion_free':True,'matrix_identities':4,'finite_integer_grid_controls':grid,'unimodular_basis_controls':changes,'geometric_identity':'IMPORTED_PUBLISHED_RESULT_NOT_MACHINE_CHECKED','source_rehash':'NOT_RUN','corpus_rehash':'NOT_RUN','independent_review':'NOT_PERFORMED','formal_verification':False}
def main():
    here=Path(__file__).resolve().parent;paths={'--claims':here/'CLAIMS.json','--certificate':here/'CERTIFICATE.json'}
    args=sys.argv[1:];need(len(args)%2==0,'arguments must be option/path pairs');seen=set()
    for i in range(0,len(args),2):
        need(args[i] in paths and args[i] not in seen,'unknown or repeated option');seen.add(args[i]);paths[args[i]]=Path(args[i+1])
    check_claims(read_json(paths['--claims']));return check_certificate(read_json(paths['--certificate']))
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (Reject,OSError,ValueError,TypeError,KeyError,RecursionError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
