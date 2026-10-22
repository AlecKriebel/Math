#!/usr/bin/env python3
"""Fail-closed finite consistency checks. These do not recognize PL spaces or prove the theorem."""
import argparse,itertools,json,math,sys
from fractions import Fraction
from pathlib import Path
class CheckFailure(Exception): pass
def need(condition, code):
    if not condition: raise CheckFailure(code)
def rank(matrix):
    if not matrix:return 0
    a=[[Fraction(x) for x in row] for row in matrix]
    n=len(a[0]);need(all(len(row)==n for row in a),'MATRIX_SHAPE_INVALID')
    r=0
    for j in range(n):
        pivot=next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        d=a[r][j];a[r]=[x/d for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                d=a[i][j];a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def check(f):
    need(f['schema']==1,'SCHEMA_MISMATCH')
    need(f['original_target']=='UNRESOLVED','ORIGINAL_TARGET_PROMOTION')
    need(f['research_turns']==5 and f['new_research_turns']==0,'RESEARCH_BUDGET_MISMATCH')
    c=f['cone'];need(c['m_values']==list(range(2,202)),'CONE_CASE_RANGE_MISMATCH')
    for m in c['m_values']:
        n=2*m;p=(n-2)//2
        need((n-1)-p==m+c['expected_offset'],'CONE_CUTOFF_MISMATCH')
        need(m-n+p==c['cycle_apex_allowability'],'CYCLE_ALLOWABILITY_MISMATCH')
        need(m+1-n+p==c['bounding_cone_apex_allowability'],'BOUNDING_ALLOWABILITY_MISMATCH')
        need((n+1)%2==1 and n%2==0,'EVENT_PARITY_MISMATCH')
    q=f['quotient'];w=q['weights'];need(w==[1,1,2,2,2],'WEIGHT_VECTOR_MISMATCH')
    coords=q['independent_sign_coordinates'];need(coords==[2,3,4],'SIGN_COORDINATES_MISMATCH')
    orbit=set()
    for signs in itertools.product((-1,1),repeat=len(coords)):
        z=[1,2,3,5,7]
        for i,sgn in zip(coords,signs):z[i]*=sgn
        need([z[i]**w[i] for i in range(5)]==[1,2,9,25,49],'POWER_MAP_ORBIT_MISMATCH')
        orbit.add(tuple(z))
    need(len(orbit)==q['degree'],'QUOTIENT_DEGREE_MISMATCH')
    ls=[1]
    for i in range(1,len(w)):
        terms=[math.prod(a)//math.gcd(*a) for a in itertools.combinations(w,i+1)]
        ls.append(math.lcm(*terms))
    need(ls==q['kawasaki_l'],'KAWASAKI_COEFFICIENT_MISMATCH')
    integral=Fraction(ls[2]**2,ls[4]);need(integral==Fraction(q['integral_square']),'INTEGRAL_SQUARE_MISMATCH')
    rational=Fraction(1,len(orbit));need(rational==Fraction(q['rational_square']),'RATIONAL_SQUARE_MISMATCH')
    need(integral/Fraction(ls[2]**2)==rational,'PAIRING_RESCALING_MISMATCH')
    s=f['sphere_bundle'];need(s['base_degrees']==[0,2] and s['fiber_degrees']==[0,5],'SPHERE_BUNDLE_BIDEGREES_MISMATCH')
    e2={(a,b) for a in s['base_degrees'] for b in s['fiber_degrees']}
    need(sorted(a+b for a,b in e2)==s['expected_total_degrees'],'SPHERE_BUNDLE_TOTAL_DEGREES_MISMATCH')
    need(not any((a+r,b-r+1) in e2 for a,b in e2 for r in range(2,10)),'SPHERE_BUNDLE_DIFFERENTIAL_PRESENT')
    need(all(a+b not in (3,4) for a,b in e2),'SPHERE_BUNDLE_MIDDLE_NOT_ZERO')
    v=f['mv'];need(v['boundary_rank']==0 and v['neighborhood_rank']==1 and v['map_matrix']==[[]],'MV_INPUT_MISMATCH')
    need(v['neighborhood_rank']-rank(v['map_matrix'])==v['cokernel_rank'],'MV_COKERNEL_MISMATCH')
    need(v['regular_middle_rank']==0,'REGULAR_MIDDLE_RANK_MISMATCH')
    need(v['signature_X']==1 and v['signature_cap']==0,'SIGNATURE_OBSTRUCTION_MISMATCH')
    for d in range(17):
        identity=[[int(i==j) for j in range(d)] for i in range(d)]
        diagonal=identity+[[-x for x in row] for row in identity]
        need(rank(diagonal)==d,'SUSPENSION_MV_INJECTIVITY_MISMATCH')
    z=f['normalization'];k=z['boundary_components'];need(k==3,'NORMALIZATION_TEST_COMPONENTS_MISMATCH')
    need(z['pinch_normalized_components']==k,'PINCH_NORMALIZATION_COMPONENTS_MISMATCH')
    need(z['separation_normalized_components']==2*k,'SEPARATION_NORMALIZATION_COMPONENTS_MISMATCH')
    need(z['same_normalization_not_literal'] is True,'DISCONNECTED_NORMALIZATION_ERROR')
    s=f['scope']
    for key,value in [('partial_only',True),('classify_is_not_construct',True),('bc_dimension_modulus',4),('bc_equivariant_required',True),('bc_local_duality_required_for_10_1',False),('zero_dimensional_cone_separate_case',True)]:
        need(s[key]==value,'SCOPE_'+key.upper()+'_MISMATCH')
    need(f['limitations']=='Finite arithmetic and source/claim consistency only; no automated PL recognition or proof of the universal problem.','LIMITATIONS_REMOVED')
    return {'status':'PASS_FINITE_CONSISTENCY_ONLY','cone_cases':len(c['m_values']),'generic_orbit_samples':len(orbit),'kawasaki_l':ls,'rational_pairing':str(rational),'sphere_bundle_degrees':f['sphere_bundle']['expected_total_degrees'],'mv_cokernel_rank':v['cokernel_rank'],'matrix_injectivity_cases':17,'original_target':'UNRESOLVED','scope':'Finite checks support the written audit; they do not prove local PL models, all inputs, or novelty.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('CHECK_FIXTURES.json'));args=parser.parse_args()
    try:
        f=json.loads(args.fixture.read_text());result=check(f)
    except CheckFailure as e:
        print(json.dumps({'status':'FAIL','diagnostic':str(e)},sort_keys=True));return 1
    except (OSError,ValueError,KeyError,TypeError,ZeroDivisionError) as e:
        print(json.dumps({'status':'FAIL','diagnostic':'INVALID_INPUT','error_type':type(e).__name__},sort_keys=True));return 2
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())
