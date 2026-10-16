#!/usr/bin/env python3
"""Universal exact polynomial controls. Analytical topology is outside its scope."""
from fractions import Fraction as Q
from pathlib import Path
import argparse, hashlib, json, sys

NAMES = ('x','y','a1','a2','a0','b1','b2','b0','u','v')
DIM = len(NAMES)
CATEGORIES = {}

def require(value,label):
    if not value:
        raise ValueError(label)
    CATEGORIES[label]=CATEGORIES.get(label,0)+1

def clean(p):return {k:v for k,v in p.items() if v}
def constant(c):return {(0,)*DIM:Q(c)} if c else {}
def variable(name):
    exponent=[0]*DIM;exponent[NAMES.index(name)]=1
    return {tuple(exponent):Q(1)}
def add(p,q):
    out=p.copy()
    for k,v in q.items():out[k]=out.get(k,Q(0))+v
    return clean(out)
def scale(p,c):return clean({k:v*Q(c) for k,v in p.items()})
def multiply(p,q):
    out={}
    for a,av in p.items():
        for b,bv in q.items():
            k=tuple(x+y for x,y in zip(a,b));out[k]=out.get(k,Q(0))+av*bv
    return clean(out)
def derivative(p,name):
    j=NAMES.index(name);out={}
    for k,v in p.items():
        if k[j]:
            n=list(k);n[j]-=1;out[tuple(n)]=v*k[j]
    return clean(out)
def substitute(p,values):
    out={}
    for exponents,coefficient in p.items():
        term=constant(coefficient)
        for name,power in zip(NAMES,exponents):
            replacement=values.get(name,variable(name))
            for _ in range(power):term=multiply(term,replacement)
        out=add(out,term)
    return out
def display(p):
    terms=[]
    for powers,value in sorted(p.items()):
        monomial='*'.join(name+(f'^{power}' if power!=1 else '')
                          for name,power in zip(NAMES,powers) if power) or '1'
        terms.append({'monomial':monomial,'coefficient':str(value)})
    return terms

# Separate univariate polynomial implementation for interval certificates.
def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p
def uadd(p,q):
    out=[Q(0)]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)
def uscale(p,c):return trim([a*c for a in p])
def umul(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return trim(out)
def evaluate(p,t):
    out=Q(0)
    for c in reversed(p):out=out*t+c
    return out
def exact_quadratic_range(p,lo,hi):
    require(len(p)<=3,'supported_norm_degree_at_most_two')
    candidates=[lo,hi]
    if len(p)==3 and p[2]:
        vertex=-p[1]/(2*p[2])
        if lo<=vertex<=hi:candidates.append(vertex)
    values=[evaluate(p,t) for t in candidates]
    return min(values),max(values),[
        {'t':str(t),'value':str(v)} for t,v in zip(candidates,values)]

def certify(model):
    x,y,a1,a2,a0,b1,b2,b0,u,v=[variable(n) for n in NAMES]
    sqx=multiply(x,x);sqy=multiply(y,y);xy=multiply(x,y)
    first=add(add(add(add(sqx,scale(sqy,-1)),multiply(a1,x)),multiply(a2,y)),a0)
    second=add(add(add(scale(xy,Q(model['system_xy_multiplier'])),multiply(b1,x)),multiply(b2,y)),b0)
    substitutions={'a1':{},'a2':{},'a0':scale(u,-1),
        'b1':{},'b2':{},'b0':scale(v,Q(model['embedding_b0_multiplier']))}
    slice_first=substitute(first,substitutions)
    slice_second=substitute(second,substitutions)
    require(slice_first==add(add(sqx,scale(sqy,-1)),scale(u,-1)),
            'universal_first_slice_identity')
    require(scale(slice_second,2)==add(scale(xy,2),scale(v,-1)),
            'universal_second_slice_identity')
    coefficient_norm=add(multiply(u,u),scale(multiply(v,v),Q(model['embedding_b0_multiplier'])**2))
    coefficient_gap=add(add(multiply(u,u),multiply(v,v)),scale(coefficient_norm,-1))
    require(coefficient_gap==scale(multiply(v,v),Q(3,4)),
            'universal_coefficient_norm_sos')
    det=add(multiply(derivative(first,'x'),derivative(second,'y')),
            scale(multiply(derivative(first,'y'),derivative(second,'x')),-1))
    proposed={}
    for term in model['general_jacobian_terms']:
        mono=constant(Q(term['coefficient']))
        for name,power in term['powers'].items():
            require(name in NAMES,'supported_jacobian_variable')
            require(type(power) is int and power >= 0,'nonnegative_integer_jacobian_power')
            for _ in range(power):mono=multiply(mono,variable(name))
        proposed=add(proposed,mono)
    require(det==proposed,'universal_general_jacobian')
    sliced_det=substitute(det,substitutions)
    require(sliced_det==scale(add(sqx,sqy),2),'universal_slice_jacobian')
    require(len(model['path_pieces'])==2,'two_path_pieces')
    paths=[];bounds=[]
    for i,piece in enumerate(model['path_pieces']):
        lo,hi=map(Q,piece['interval'])
        require((lo,hi)==((Q(0),Q(1)) if i==0 else (Q(1),Q(2))),
                'full_interval_coverage')
        gx,gy=[trim(list(map(Q,piece[name]))) for name in ('real','imaginary')]
        norm=uadd(umul(gx,gx),umul(gy,gy))
        lower,upper,witnesses=exact_quadratic_range(norm,lo,hi)
        require(lower>=Q(1,2) and upper<=1,'universal_path_nonzero_and_bounded')
        zx=uadd(umul(gx,gx),uscale(umul(gy,gy),Q(-1)))
        zy=uscale(umul(gx,gy),Q(2))
        require(uadd(umul(zx,zx),umul(zy,zy))==umul(norm,norm),
                'universal_squared_loop_norm_identity')
        paths.append((gx,gy,zx,zy))
        bounds.append({'interval':[str(lo),str(hi)],'norm_coefficients':list(map(str,norm)),
                       'exact_minimum':str(lower),'exact_maximum':str(upper),
                       'extremum_certificate':witnesses})
    at=lambda path,t:(evaluate(path[0],t),evaluate(path[1],t))
    param=lambda path,t:(evaluate(path[2],t),evaluate(path[3],t))
    require(at(paths[0],Q(1))==at(paths[1],Q(1)),'polynomial_path_continuous_join')
    root0,root2=at(paths[0],Q(0)),at(paths[1],Q(2))
    require(root0==(1,0) and root2==(-1,0),'exact_path_endpoints')
    require(root0==tuple(-a for a in root2),'opposite_nonzero_root_endpoints')
    require(param(paths[0],Q(0))==param(paths[1],Q(2))==(1,0),
            'exact_closed_parameter_endpoints')
    c,r=Q(model['example_scale']),Q(model['example_disk_radius'])
    require(c>0,'positive_example_scale')
    require(c*c<r,'strict_example_disk_inclusion')
    return {'status':'PASS','guard':'explicit exceptions remain active with Python -O',
        'scope':'Universal polynomial identities and quadratic interval bounds only. Continuous-section nonexistence additionally uses openness, continuity of composition and quotient, and connectedness of the interval, as supplied by the written proof.',
        'categories':CATEGORIES,'general_jacobian':display(det),
        'coefficient_norm_gap_sos':display(coefficient_gap),'path_certificates':bounds,
        'arbitrary_radius_statement':'For every r>0 choose 0<c<sqrt(r). The checked universal bound |gamma|^2<=1 gives |c^2 gamma^2|<=c^2<r.',
        'topological_assumptions_verified_by_code':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('model',type=Path);args=parser.parse_args()
    data=args.model.read_bytes();model=json.loads(data)
    result=certify(model)
    result['model_sha256']=hashlib.sha256(data).hexdigest()
    result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError) as error:
        print(json.dumps({'status':'FAIL','reason':str(error)},sort_keys=True),file=sys.stderr)
        raise SystemExit(1)
