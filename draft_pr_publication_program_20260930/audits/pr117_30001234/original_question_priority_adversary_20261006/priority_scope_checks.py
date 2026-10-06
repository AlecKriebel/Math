#!/usr/bin/env python3
"""Exact algebraic equivalence of Takagi's 2011 Example 4.4 and PR117.

No threshold computation is needed for the priority match. Private-source mode
also verifies the actual retrieved source bodies and immutable review inputs.
All guards remain active under Python -O. --force-false is a negative control.
"""
import argparse, ast, hashlib, json, pathlib
from fractions import Fraction as Q

D=pathlib.Path(__file__).resolve().parent
COUNT=0
def ck(b,m):
    global COUNT
    COUNT += 1
    if not b: raise ValueError(m)

parser=argparse.ArgumentParser()
parser.add_argument('--with-private-sources', action='store_true')
parser.add_argument('--force-false', action='store_true')
args=parser.parse_args()
if args.force_false: ck(False,'forced false priority guard')

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def image(A,z): return tuple(dot(row,z) for row in A)

# Coordinates in the polynomial ring are x1,x2,x3,y1,y2,y3.
# Candidate f3 is the negative of Takagi's third generator.
a=[(1,0,0,0,1,0),(0,1,0,0,0,1),(0,0,1,1,0,0)]
b=[(0,1,0,1,0,0),(0,0,1,0,1,0),(1,0,0,0,0,1)]
candidate_columns=a+b
A=tuple(tuple(col[j] for col in candidate_columns) for j in range(6))
A+=tuple(tuple(int(i==j%3) for j in range(6)) for i in range(3))
expected=((1,0,0,0,0,1),(0,1,0,1,0,0),(0,0,1,0,1,0),
          (0,0,1,1,0,0),(1,0,0,0,1,0),(0,1,0,0,0,1),
          (1,0,0,1,0,0),(0,1,0,0,1,0),(0,0,1,0,0,1))
ck(A==expected,'Exact immutable candidate matrix')

# Source interleaves each generator's two terms, with f3's sign reversed.
source_columns=(a[0],b[0],a[1],b[1],b[2],a[2])
B=tuple(tuple(col[j] for col in source_columns) for j in range(6))
B+=tuple(tuple(int(j//2==i) for j in range(6)) for i in range(3))
order=(0,3,1,4,5,2)
ck(sorted(order)==list(range(6)),'Coordinate map is a bijection')
def permute(z): return tuple(z[j] for j in order)

for j in range(6):
    e=tuple(int(k==j) for k in range(6))
    ck(image(B,permute(e))==image(A,e),'Source/candidate column identity '+str(j))
    ck(sum(permute(e))==sum(e),'Objective preserved on basis '+str(j))

# The matrix identity on a basis proves image equality for every rational z,
# not just for sampled points. Permutation preserves nonnegativity and hence
# feasible polytopes, objectives, distinct optimizers and image fibers exactly.
d=(1,1,1,-1,-1,-1)
ck(image(A,d)==(0,)*9,'Entire candidate segment lies in one image fiber')
ck(image(B,permute(d))==(0,)*9,'Entire prior segment lies in one image fiber')
endpoints=[]
for t in [Q(0),Q(1,3),Q(1,2),Q(1)]:
    z=(t,t,t,1-t,1-t,1-t)
    sig=permute(z)
    ck(all(x>=0 for x in sig),'Rational feasible nonnegativity')
    ck(image(B,sig)==(1,)*9,'Source exact augmented image')
    ck(sum(sig)==3,'Source optimal objective')
    ck(sig==(t,1-t,t,1-t,1-t,t),'Explicit sign-adjusted source optimal face')
    if t in [0,1]: endpoints.append(sig)
ck(endpoints[0]!=endpoints[1],'Prior image fiber is nontrivial')
ck(image(B,endpoints[0])==image(B,endpoints[1]),'Prior endpoint image equality')

# A wrong correspondence must fail: forgetting the f3 orientation changes
# columns5/6. The assertion being rejected is not accepted by the checker.
wrong=(0,3,1,4,2,5)
ck(any(image(B,tuple(e[j] for j in wrong))!=image(A,e)
       for e in [tuple(int(k==j) for k in range(6)) for j in range(6)]),
   'Negative control: wrong third-term correspondence is detected')

for name in ['acquire_sources.py','acquire_followups.py','acquire_decisive_source_versions.py','render_version_one.py']:
    tree=ast.parse((D/name).read_text())
    fs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ck']
    ck(len(fs)==1,'Exactly one acquisition/render exception guard '+name)
    ns={}
    exec(compile(ast.Module(body=fs,type_ignores=[]),str(D/name),'exec'),ns)
    rejected=False
    try: ns['ck'](False,'deliberate false acquisition guard')
    except ValueError: rejected=True
    ck(rejected,'False acquisition/render guard is rejected '+name)

private_count=0
if args.with_private_sources:
    sources=json.loads((D/'SOURCE_MANIFEST.json').read_text())
    for rec in sources['private_members']:
        path=D/rec['relative_path']; body=path.read_bytes()
        ck(len(body)==rec['bytes'],'Actual private-source byte count '+rec['relative_path'])
        ck(hashlib.sha256(body).hexdigest()==rec['sha256'],'Actual private-source digest '+rec['relative_path'])
        private_count+=1
    pins={
     '../original_head_authentication_20261006/original_attempt/CANDIDATE.md':(10573,'1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf'),
     '../original_head_authentication_20261006/original_attempt/source_record.json':(4949,'c815205b3bf1eeb3dd0d47ad93fcb1faedf360759d44bc605915ef4a66595ea5'),
     '../original_head_authentication_20261006/SOURCE_STATEMENT.json':(4949,'5afe57bf74b27a30ed1b38a757370379dfdcddee350e3d9d273330dcf922da7d'),
     '../original_head_authentication_20261006/PRIOR_REPORT.json':(3,'ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356'),
     '../MATHEMATICAL_SOURCE_GATE_20261006.json':(1539,'a7a9b25346ab832761e8c9da67b5e2fb946fc18cf83e81546d6a23bceb9acd56'),
    }
    for name,(length,digest) in pins.items():
        raw=(D/name).read_bytes()
        ck(len(raw)==length and hashlib.sha256(raw).hexdigest()==digest,'Immutable review-input pin '+name)
    original=json.loads((D/'../original_head_authentication_20261006/original_attempt/source_record.json').read_text())
    full=json.loads((D/'../original_head_authentication_20261006/SOURCE_STATEMENT.json').read_text())
    prior=json.loads((D/'../original_head_authentication_20261006/PRIOR_REPORT.json').read_text())
    ck(original==full,'Complete original/current source statement identical')
    ck(prior=={},'Complete retrieved prior report is empty')
    for name in ['takagi_1105.0072v1.txt','takagi_1105.0072v5.txt','takagi_adjoint2013.txt']:
        txt=(D/'private_sources'/name).read_text()
        ck('Example 4.4.' in txt and 'Remark 4.3.' in txt,'Primary counterexample/condition numbering '+name)
        ck('does not satisfy' in txt,'Explicit prior failure statement '+name)

print(json.dumps({'schema':'pr117-original-question-scope-checks/v1','status':'PASS',
                  'guards':COUNT,'private_sources_checked':private_count,
                  'exact_prior_counterexample':True,'originality_clearance':False,
                  'new_central_proof_turns':0,'source_to_candidate_order':list(order)},sort_keys=True))
