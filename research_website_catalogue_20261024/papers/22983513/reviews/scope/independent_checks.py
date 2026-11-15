"""Independent exact spectra via a monotone heap frontier, and Fourier tails.
No supplied imports, no finite matrix pretends to realize the infinite sum rules.
"""
from fractions import Fraction as F
from heapq import heappush,heappop
from math import isqrt
import json,hashlib
from datetime import datetime,timezone

def spectrum(components,count):
    heap=[];seen=set()
    def add(c,mode):
        key=(c,mode)
        if key not in seen:
            seen.add(key);heappush(heap,(sum((F(m,L)**2 for m,L in zip(mode,components[c])),F(0)),c,mode))
    for c,L in enumerate(components):add(c,(1,)*len(L))
    out=[]
    for _ in range(count):
        E,c,mode=heappop(heap);out.append(E)
        for i in range(len(mode)):
            nei=list(mode);nei[i]+=1;add(c,tuple(nei))
    return out,heap[0][0]

def run():
    cases=[('interval',[(F(1),)]),('three_equal_intervals',[(F(1),)]*3),('unequal_intervals',[(F(1),),(F(2),),(F(3,2),)]),('rectangle',[(F(1),F(3,2))]),('disconnected_unequal_rectangles',[(F(1),F(1)),(F(2),F(1))]),('cube',[(F(1),)*3])]
    reports=[];gapchecks=thresholdchecks=zerogaps=groundties=0;digest=hashlib.sha256()
    for name,components in cases:
        n=len(components[0]);E,nextlower=spectrum(components,161)
        assert E==sorted(E) and nextlower>=E[-1]
        smallest=None
        for J in range(1,161):
            A=sum(E[:J],F(0))/J;B=sum((e*e for e in E[:J]),F(0))/J
            M=F(n+2,n)*A;D=M*M-F(n+4,n)*B;g=E[J]-E[J-1];margin=D-g*g/4
            assert margin>0
            Q=lambda t:sum(((t-e)*(t-F(n+4,n)*e) for e in E[:J]),F(0))/J
            assert Q(E[J-1])<=0 and (Q(E[J])<0 if E[J]>E[0] else D==F(4,n*n)*E[0]**2)
            if name=='interval':assert margin==F((2*J+1)*(3*J*J+2*J+2),12)
            zerogaps+=g==0;groundties+=E[J]==E[0];gapchecks+=1
            if smallest is None or margin<smallest:smallest=margin
            digest.update(str((name,J,D,g,margin)).encode())
        levels=sorted(set(E))
        for z in [F(0),E[0]]+levels[1:]+[(a+b)/2 for a,b in zip(levels,levels[1:])]:
            low=[e for e in E if e<z]
            R=4*sum(((z-e)*e for e in low),F(0))-n*sum(((z-e)**2 for e in low),F(0))
            assert (R>0) if z>E[0] else (R==0)
            thresholdchecks+=1
        scale=F(7,3)
        scaled,_=spectrum([tuple(scale*L for L in C) for C in components],161)
        assert scaled==[e/scale**2 for e in E]
        reports.append({'name':name,'n':n,'components':[[str(L) for L in C] for C in components],'prefix_length':161,'frontier_lower_bound':str(nextlower),'last_energy':str(E[-1]),'smallest_absolute_gap_deficit':str(smallest),'geometric_scale_check':str(scale)})
    # Exact parity/rational Fourier coefficient pi*a_1k=-8k/(k²-1)².
    # For every finite z, an even k with k²>z supplies a nonzero positive tail.
    tails=[]
    for z in [F(3,2),F(4),F(9),F(101,7),F(10**6),F(10**20)]:
        k=2*((isqrt(z.numerator//z.denominator)//2)+1)
        assert k%2==0 and k*k>z
        c=F(-8*k,(k*k-1)**2)
        weighted=(z-1)*(k*k-1)*(k*k-z)*c*c
        assert c and weighted>0
        tails.append({'z':str(z),'even_mode_above_threshold':k,'pi_times_coordinate_coefficient':str(c),'pi_squared_times_positive_remainder_summand':str(weighted)})
    # Literal unsquared report display can even be negative under dilation.
    c=F(10);E1=1/c**2
    # In one dimension M1=3E1, M2=sqrt(5)E1; sqrt5>2.
    assert 9*E1*E1-2*E1<0
    return {'status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),'mechanism':'monotone heap frontier gives exact complete box/component prefixes, distinct from supplied Cartesian cutoff','gap_cases':gapchecks,'strict_real_threshold_cases':thresholdchecks,'zero_gap_cases':zerogaps,'repeated_ground_branch_cases':groundties,'case_digest_SHA256':digest.hexdigest(),'cases':reports,'infinite_support_fourier_witnesses':tails,'negative_controls':{'z_equals_E1_is_zero_not_strict':True,'literal_unsquared_M2_expression_fails_scale':True,'finite_matrix_not_claimed_to_realize_TRK':True},'limitations':['Exact selected-domain checks are not the universal rough-domain proof.','Fourier tail identity is proved analytically in the reconstruction; these controls check its rational coefficient/sign consequences.','No formal proof assistant or human peer review.']}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
