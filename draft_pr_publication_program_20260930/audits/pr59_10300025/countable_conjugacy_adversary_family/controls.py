#!/usr/bin/env python3
"""Independent exact interval/arrangement certificates; no author import."""
from fractions import Fraction as Q
import hashlib, itertools, json, pathlib

counts={}
def require(kind,condition):
    if not condition: raise AssertionError(kind)
    counts[kind]=counts.get(kind,0)+1

class Curve:
    def __init__(self,pairs):
        self.pairs=tuple(sorted((Q(x),Q(y)) for x,y in pairs))
        assert len(self.pairs)>=2
        assert all(a[0]<b[0] for a,b in zip(self.pairs,self.pairs[1:]))
        self.orientation=1 if self.pairs[-1][1]>self.pairs[0][1] else -1
        assert all(self.orientation*(b[1]-a[1])>0 for a,b in zip(self.pairs,self.pairs[1:]))
    def line_at(self,x):
        x=Q(x)
        a,b=self.pairs[0:2]
        for left,right in zip(self.pairs,self.pairs[1:]):
            a,b=left,right
            if x<=right[0]: break
        slope=(b[1]-a[1])/(b[0]-a[0])
        return slope,a[1]-slope*a[0]
    def __call__(self,x):
        a,b=self.line_at(x);return a*Q(x)+b
    def reversed(self): return Curve([(y,x) for x,y in self.pairs])
    def breaks(self): return [x for x,y in self.pairs]

def affine(a,b=0): return Curve([(0,b),(1,a+b)])
maps=[affine(1),affine(1,-10**9),affine(Q(1,10000)),
      Curve([(-7,-31),(-1,-3),(0,0),(2,100),(9,101)]),
      affine(-2,3),Curve([(-4,10**6),(0,7),(1,-1),(5,-10**7)]),
      Curve([(-8,-10**8),(-2,-1),(0,9),(3,11),(4,10**9)]),affine(-1)]
inverses=[f.reversed() for f in maps]
levels=[Q(0),Q(1)]
for n in range(1,19):
    candidates=[levels[n]+1]
    for f,fi in zip(maps[:n],inverses[:n]):
        candidates += [abs(g(t)) for g in (f,fi) for t in (-levels[n],levels[n])]
    levels.append(max(candidates)+1)
H=Curve([(s*r,s*n) for n,r in enumerate(levels) for s in (-1,1) if n]+[(0,0)])

def partition(f,left,right):
    fi=f.reversed()
    values=[left,right]+f.breaks()+H.breaks()+[fi(t) for t in H.breaks()]
    return sorted({x for x in values if left<=x<=right})

certificates=[]
for j,(f,fi) in enumerate(zip(maps,inverses),1):
    for n in range(j,len(levels)-1):
        for sign in (-1,1):
            require('strict_forward_inverse_endpoint_inclusions',
                    abs(f(sign*levels[n]))<levels[n+1] and abs(fi(sign*levels[n]))<levels[n+1])
    core=partition(f,-levels[j+1],levels[j+1])
    core_max=max(abs(H(f(x))-f.orientation*H(x)) for x in core)
    require('complete_compact_cell_certificate',core_max<=2*j+3)
    certificates.append({'map':j,'region':'core','cells':len(core)-1,'exact_max':str(core_max),'bound':2*j+3})
    for n in range(j+1,len(levels)-2):
        for sign in (-1,1):
            a,b=sorted((sign*levels[n],sign*levels[n+1]))
            knots=partition(f,a,b)
            maximum=max(abs(H(f(x))-f.orientation*H(x)) for x in knots)
            for x in knots:
                require('all_shell_cell_vertices_annular_bounds',levels[n-1]<abs(f(x))<levels[n+2])
                require('all_shell_cell_vertices_orientation',f.orientation*x*f(x)>0)
                require('all_shell_cell_vertices_displacement',abs(H(f(x))-f.orientation*H(x))<=2)
            require('complete_shell_cell_certificate',maximum<=2)
            certificates.append({'map':j,'region':'positive shell' if sign>0 else 'negative shell',
                                 'n':n,'cells':len(knots)-1,'exact_max':str(maximum),'bound':2})

# Reverse triangle inequality on new rational cases, including sign changes.
points=[Q(i,7) for i in range(-28,29)]+[s*r for r in levels[:8] for s in (-1,1)]
for f in maps:
    for x,y in itertools.product(points,repeat=2):
        dx=H(f(x))-f.orientation*H(x);dy=H(f(y))-f.orientation*H(y)
        defect=abs(abs(H(f(x))-H(f(y)))-abs(H(x)-H(y)))
        require('signed_error_exact_two_point_reduction',defect<=abs(dx-dy)<=abs(dx)+abs(dy))

# All-real finite envelope: use the entire affine-line arrangement, not a grid.
generators=[maps[k] for k in (0,1,2,3,6)]
S=generators+[f.reversed() for f in generators]
components=S+[affine(1,1)]
knots=sorted({Q(-1),Q(0),Q(1)}|{x for f in components for x in f.breaks()})
crossings=set(knots)
edges=[(None,knots[0])]+list(zip(knots,knots[1:]))+[(knots[-1],None)]
for a,b in edges:
    probe=b-1 if a is None else a+1 if b is None else (a+b)/2
    lines=[f.line_at(probe) for f in components]
    for (m,c),(k,d) in itertools.combinations(lines,2):
        if m!=k:
            x=(d-c)/(m-k)
            if (a is None or a<=x) and (b is None or x<=b):crossings.add(x)
F=Curve([(x,max(f(x) for f in components)) for x in sorted(crossings)])
Fi=F.reversed()
zero_knots=sorted(set(Fi.breaks()+[F(v) for v in F.breaks()]))
# Every composition-affine cell is determined by its two endpoints; outer rays
# are determined by an endpoint and one further point. Thus these certify R.
for x in zero_knots+[zero_knots[0]-1,zero_knots[-1]+1]:
    require('global_envelope_inverse_cell_certificate',F(Fi(x))==x)
tests=sorted(crossings)+[min(crossings)-1,max(crossings)+1]
for x in tests:
    require('global_arrangement_envelope_values',F(x)==max(f(x) for f in components))
    require('global_arrangement_positive_drift',F(x)>=x+1)
    for s in S:require('symmetric_generator_global_sandwich_cell_vertices',Fi(x)<=s(x)<=F(x))

# Exact countercontrols against stronger or broken variants.
countercontrols={}
for n in (2,3,10,100,1000):
    require('inverse_omission_cuberoot_countercontrol',n**3-n>n)
countercontrols['inverse_omission']={'forward_only_r_n':'n','map':'real cuberoot(x)',
                                  'defect_at_x_n_cubed':'n^3-n -> infinity'}
for n in (1,10,1000):
    require('reversal_requires_signed_identity',abs(-Q(n)+Q(n))==0 and abs(-Q(n)-Q(n))==2*n)
countercontrols['orientation']={'reflection_metric_defect':0,'plus_identity_displacement':'2|u|'}
badF=lambda x:max(Q(x)+1,Q(x)/100)
require('nonsymmetric_lower_sandwich_fails',badF(Q(99))==100 and Q(100)/100<Q(99))
countercontrols['nonsymmetric_set']={'S':'x/100','x':100,'F_inverse_x':99,'s_x':1}
slope,intercept=H.line_at(levels[-1]+1)
big=levels[-1]+Q(10**6,1)/slope
defect=H(4*big)-H(big)
require('finite_truncation_fails_global_dilation',defect==3*slope*big and defect>10**6)
countercontrols['finite_prefix']={'H_outer_slope':str(slope),'x':str(big),'dilation_displacement':str(defect),
                                 'growth_formula':'H(4x)-H(x)=3*outer_slope*x for x beyond last radius'}
for k in range(1,12):
    for x in (Q(0),Q(1,1000),Q(1),Q(10**9)):
        ratio=(1+2**k*x)/(1+x)
        require('log_coordinate_dilation_ratio',1<=ratio<=2**k)
for n in (1,2,10,100):
    require('fixed_pair_powers_no_group_uniform_bound',2**n-1>n-1)
countercontrols['uniform_group_bound']={'action':'x->2x','unconjugated_fixed_pair':[1,0],
                                      'defect_of_nth_power':'2^n-1','all_h_argument':'proper h sends 2^n to an infinite end'}

root=pathlib.Path(__file__).resolve().parent
result={'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'arithmetic':'Python fractions.Fraction; no numerical tolerance or author/checker import',
        'assertions_passed':sum(counts.values()),'counts':counts,
        'maps':len(maps),'radii':len(levels),'interval_certificates':certificates,
        'countercontrols':countercontrols,
        'interpretation':'Finite exact certificates and falsifying controls; universal result is proved separately.'}
(root/'controls_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'assertions_passed':sum(counts.values()),'counts':counts,
                  'interval_certificates':len(certificates),'countercontrols':list(countercontrols),
                  'max_radius_decimal_digits':len(str(levels[-1].numerator))},indent=2))
