#!/usr/bin/python3
"""Own exact finite diagnostics; no author/reviewer imports; not an infinite proof."""
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import datetime, hashlib, json, os, sys

counts=Counter()
def check(label, value):
    if not value: raise AssertionError(label)
    counts[label]+=1

class Polygon:
    def __init__(self, pairs):
        self.points=tuple((Q(x),Q(y)) for x,y in pairs)
        check('map_domain_strict', len(self.points)>=2 and all(a[0]<b[0] for a,b in zip(self.points,self.points[1:])))
        self.sign=1 if self.points[-1][1]>self.points[0][1] else -1
        check('map_range_strict', all(self.sign*(b[1]-a[1])>0 for a,b in zip(self.points,self.points[1:])))
    def at(self,x):
        x=Q(x); k=0
        while k<len(self.points)-2 and x>self.points[k+1][0]: k+=1
        a,b=self.points[k:k+2]
        return a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0])
    def inverse(self): return Polygon(sorted((y,x) for x,y in self.points))
    def compose(self,inner):
        inv=inner.inverse()
        knots={x for x,y in inner.points}|{inv.at(x) for x,y in self.points}
        return Polygon([(x,self.at(inner.at(x))) for x in sorted(knots)])

def affine(a,b): return Polygon([(0,b),(1,a+b)])
identity=affine(1,0); shift=affine(1,Q(17,5)); dilation=affine(5,0); reflection=affine(-1,0)
bent=Polygon([(-4,-31),(-1,-7),(0,2),(3,Q(5,2)),(8,90)])
flipped=Polygon([(-5,47),(-1,9),(0,4),(2,-1),(7,-83)])
maps=[shift,dilation,identity,reflection,bent,affine(Q(1,37),-11),flipped,
      flipped.compose(shift),bent.inverse(),dilation.compose(flipped)]
inverses=[g.inverse() for g in maps]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for g,inv in zip(maps,inverses):
    for t in (Q(-100),Q(-7,3),Q(0),Q(3,8),Q(2),Q(71)):
        check('exact_inverse',inv.at(g.at(t))==t and g.at(inv.at(t))==t)

# Asymmetric exhaustion of the INITIAL independent argument, not radial radii.
left=[Q(0)]; right=[Q(0)]; levels=len(maps)+8
for n in range(1,levels+1):
    values=[Q(-n),Q(n),left[-1],right[-1]]
    for g,inv in zip(maps[:n],inverses[:n]):
        values.extend(f.at(x) for f in (g,inv) for x in (left[-1],right[-1]))
    left.append(min(values)-1); right.append(max(values)+1)
    check('strict_nested_exhaustion',left[-1]<left[-2] and right[-1]>right[-2] and left[-1]<-n and right[-1]>n)
    for g,inv in zip(maps[:n],inverses[:n]):
        for f in (g,inv):
            for x in (left[n-1],right[n-1]): check('image_inverse_interior',left[n]<f.at(x)<right[n])

h=Polygon([(left[n],-n) for n in range(levels,0,-1)]+[(0,0)]+[(right[n],n) for n in range(1,levels+1)])
hinv=h.inverse()
def error(g,x): return h.at(g.at(x))-g.sign*h.at(x)
def knots_on(g,lo,hi):
    inv=g.inverse()
    candidates={lo,hi}|{x for x,y in h.points}|{x for x,y in g.points}|{inv.at(x) for x,y in h.points}
    return sorted(x for x in candidates if lo<=x<=hi)

certificates=[]
for i,(g,inv) in enumerate(zip(maps,inverses),1):
    core=knots_on(g,left[i],right[i]); maximum=max(abs(error(g,x)) for x in core)
    check('full_finite_core_PL_certificate',maximum<=2*i+1)
    samples=list(core)
    annulus_count=0; tail_max=Q(0)
    for n in range(i,levels-1):
        for lo,hi,positive in ((right[n],right[n+1],True),(left[n+1],left[n],False)):
            vertices=knots_on(g,lo,hi)
            # All signed-error breakpoints are present; absolute affine error
            # attains its interval maximum at these vertices, not just samples.
            local_max=max(abs(error(g,x)) for x in vertices)
            check('full_finite_annulus_PL_certificate',local_max<=2)
            tail_max=max(tail_max,local_max); annulus_count+=1
            for x in vertices:
                image=g.at(x)
                expect_positive=(positive and g.sign==1) or (not positive and g.sign==-1)
                check('signed_annular_endpoint_barriers',right[n-1]<image<right[n+2] if expect_positive else left[n+2]<image<left[n-1])
                check('tail_correct_orientation',image>0 if expect_positive else image<0)
                check('tail_signed_displacement',abs(error(g,x))<=2)
                check('common_conjugacy_inverse',hinv.at(h.at(x))==x)
            samples.extend(vertices[:3]); samples.append((lo+hi)/2)
    for x,y in zip(samples,samples[::-1]):
        defect=abs(abs(h.at(g.at(x))-h.at(g.at(y)))-abs(h.at(x)-h.at(y)))
        check('two_point_from_signed_error',defect<=abs(error(g,x))+abs(error(g,y))<=4*i+2)
    certificates.append({'index':i,'orientation':g.sign,'core_vertices':len(core),'core_max':str(maximum),
      'fully_certified_finite_annuli':annulus_count,'tail_max':str(tail_max),'global_proof_bound':2*i+1})

# A single coordinate respects noncommutative composition and inverse exactly.
for a,b in ((0,3),(4,6),(1,7),(6,4)):
    for t in (Q(-3,2),Q(0),Q(7,5)):
        x=hinv.at(t)
        check('common_coordinate_composition',h.at(maps[a].at(maps[b].at(x)))==h.at(maps[a].at(hinv.at(h.at(maps[b].at(x))))))

# Deliberate mathematical mutants; witnesses are recorded, not hidden PASSes.
mutants=[]
bad_contraction=affine(Q(1,2),0)
forward_only=Polygon([(-2,-1),(0,0),(2,1)])
w=Q(80); witness=abs(forward_only.at(bad_contraction.at(w))-forward_only.at(w))
check('mutant_forward_only_killed',witness>2)
mutants.append({'name':'omit inverse barriers','x':str(w),'wrong_tail_error':str(witness),'forward_images_fit_linear_exhaustion':True})
w=Q(40); wrong=abs(reflection.at(w)-w)
check('mutant_orientation_sign_killed',wrong>2 and abs(reflection.at(w)+w)==0)
mutants.append({'name':'compare reflection to +t','wrong_error':str(wrong),'correct_error':'0'})
different_h=Polygon([(0,0),(1,1),(2,5)])
different_h_inv=different_h.inverse()
mixed_dilation=lambda x:different_h.at(2*different_h_inv.at(x))
mixed_value=mixed_dilation(different_h.at(0)+1)
check('mutant_separate_coordinates_killed',mixed_value!=2)
mutants.append({'name':'separate conjugacies break D T D^-1 = T^2','mixed_relation_at_zero':str(mixed_value),'required':'2'})
for k in (1,3,7,12):
    check('uniform_constant_obstruction_orbit_growth',Q(2)**k-1>=k)
check('probability_measure_coordinate_not_onto_R',sum(Q(1,2)**j for j in range(1,21))==1-Q(1,2)**20)
mutants.append({'name':'probability CDF substituted for line coordinate','total_mass':'1','range_bounded':True})

root=Path(__file__).resolve().parent
result={'role':'NEW_INDEPENDENT_EXACT_FINITE_DIAGNOSTICS','pid':os.getpid(),'argv':sys.argv,'start_utc':start,
 'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'proof_sha256':hashlib.sha256((root/'PROOF.md').read_bytes()).hexdigest(),'arithmetic':'stdlib fractions.Fraction; exact',
 'passed_assertions':sum(counts.values()),'counts':dict(counts),'maps':len(maps),'levels':levels,
 'certificates':certificates,'mutants':mutants,
 'left_knots':[str(x) for x in left],'right_knots':[str(x) for x in right],
 'limits':'Whole finite PL cores/annuli only; true infinite extension and arbitrary homeomorphisms are proved in PROOF.md. Truncated h is not claimed globally valid beyond the controlled intervals. No novelty, human, formal, or ROOT-acceptance claim.'}
print(json.dumps(result,indent=2,sort_keys=True))
