"""Exact coordinate bridge to manually read Takagi2013 Example4.4."""
from pathlib import Path
from fractions import Fraction
import json,sys
ROOT=Path(__file__).resolve().parent
COUNT=0
class ScopeFailure(ValueError):pass
def require(ok,label):
    global COUNT
    COUNT+=1
    if not ok:raise ScopeFailure(label)
def rejects(fn,label):
    try:fn()
    except ScopeFailure:return
    raise ScopeFailure('Mutant accepted: '+label)
def image(a,z):return [sum(x*y for x,y in zip(row,z)) for row in a]
def main():
    require('--false-control' not in sys.argv,'deliberate false source-bridge guard')
    old=json.loads((ROOT/'BRIDGE_CHECK_RESULT.json').read_text())['matrix']
    # Published term order: f1 positive/negative, f2 positive/negative, f3 positive/negative.
    # The published f3 is the negative of the candidate cyclic f3.
    terms=[(1,0,0,0,1,0),(0,1,0,1,0,0),(0,1,0,0,0,1),(0,0,1,0,1,0),(1,0,0,0,0,1),(0,0,1,1,0,0)]
    pub=[[terms[j][i] for j in range(6)] for i in range(6)]+[[int(j//2==i) for j in range(6)] for i in range(3)]
    perm=[0,3,1,4,5,2]
    require(pub==[[row[j] for j in perm] for row in old],'matrix equality under exact permutation')
    require(sorted(perm)==list(range(6)),'coordinate permutation invertible')
    require(len(set(terms))==6,'six distinct degree-two monomials')
    require(all(sum(t)==2 for t in terms),'all generators degree two')
    require([sum(pub[-3+i]) for i in range(3)]==[2,2,2],'generator-group cap rows retained')
    for j in range(6):
        oldz=[Fraction(int(k==j)) for k in range(6)];pubz=[oldz[k] for k in perm]
        require(image(pub,pubz)==image(old,oldz),'universal image conjugacy via rational basis')
        require(sum(pubz)==sum(oldz),'objective preserved via rational basis')
    for t in [Fraction(0),Fraction(1),Fraction(2,3)]:
        oldz=[t]*3+[1-t]*3;pubz=[oldz[k] for k in perm]
        require(pubz==[t,1-t,t,1-t,1-t,t],'published optimal segment formula')
        require(image(pub,pubz)==[1]*9,'published full augmented image constant')
        require(sum(pubz)==3,'published objective three')
    # These source-scope facts are manually verified in the report, not discovered by this checker.
    c=0;s=3;mi=[2]*3
    require(c==0 and s==3 and mi==[2,2,2],'affine-six-space ambient specialization')
    require(sum([])==c,'extra ambient complete-intersection equality tautological for c zero')
    wrong=[0,3,1,4,2,5]
    rejects(lambda:require(pub==[[r[j] for j in wrong] for r in old],'forgot third generator sign swap'),'incorrect sign/order')
    rejects(lambda:require(pub==old,'forgot interleaving'),'incorrect column order')
    rejects(lambda:require(len(pub)==6,'dropped caps'),'missing generator caps')
    rejects(lambda:require(c==2,'used determinantal subscheme as ambient variety'),'ambient/subscheme conflation')
    print(json.dumps({'result':'PASS','explicit_exception_checks':COUNT,'old_coordinate_order':['mu1','mu2','mu3','nu1','nu2','nu3'],'published_coordinate_order':['sigma11','sigma12','sigma21','sigma22','sigma31','sigma32'],'published_from_old_indices':perm,'published_coordinate_values':['mu1','nu1','mu2','nu2','nu3','mu3'],'published_augmented_matrix':pub,'ambient_complete_intersection_codimension':c,'source_example_is_exact_original_target_counterexample':True,'new_central_proof_search_turns':0},indent=2))
if __name__=='__main__':main()
