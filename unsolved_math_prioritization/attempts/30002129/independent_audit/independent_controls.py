#!/usr/bin/env python3
"""Independent exact audit. No author-code imports; all checks survive python -O.
The oracle uses gap compositions and X-index block maps, rather than the
release's XY-site tables and letterwise composition. Finite evidence only.
"""
from fractions import Fraction as Q
from itertools import product
from math import gcd,lcm,comb
from bisect import bisect_right
from collections import Counter
import hashlib,json

COUNTS=Counter()
def require(value,label):
    COUNTS[label]+=1
    if not value: raise RuntimeError(label)

def compositions(total,n):
    if n==1:
        yield (total,)
    else:
        for x in range(total+1):
            for tail in compositions(total-x,n-1): yield (x,)+tail

def phases(word):
    runs=[]
    for char in word[::-1]:
        if runs and runs[-1][0]==char:runs[-1][1]+=1
        else:runs.append([char,1])
    require(all(runs[j][0]==('b' if j%2==0 else 'a') for j in range(len(runs))),'word_phase_convention')
    return [(runs[j][1],runs[j+1][1]) for j in range(0,len(runs),2)]

def orbit_data(gaps,P,U,steps,deep=True):
    N=len(gaps);V=sum(gaps);S=[0]
    for t in gaps:S.append(S[-1]+t)
    def prefix(i):
        d,k=divmod(i,N);return d*V+S[k]
    def hop(i,beta,alpha):
        y=prefix(i)+beta*U
        turn,rank=divmod(y,V)
        gap=turn*N+bisect_right(S,rank)-1
        return gap+1+alpha*P,gap-i
    def advance(i):
        for beta,alpha in steps:i,_=hop(i,beta,alpha)
        return i
    table=[advance(i) for i in range(N+1)]
    require(table[-1]==table[0]+N,'degree_one')
    require(all(x<=y for x,y in zip(table,table[1:])),'monotone')
    def fast(i):
        d,k=divmod(i,N);return d*N+table[k]
    cycles=[];rotations=[]
    for initial in range(N):
        seen={};x=initial;k=0
        while x%N not in seen:
            seen[x%N]=(k,x);x=fast(x);k+=1
        before,start=seen[x%N];period=k-before;delta=x-start
        require(delta%N==0,'integer_lift_closure')
        value=Q(delta,N*period)
        require(value.denominator==period,'reduced_denominator_is_cycle_period')
        rotations.append(value);cycles.append((start,period,value.numerator))
    require(len(set(rotations))==1,'all_initial_orbits_same_translation')
    val=rotations[0]
    if deep:
        start,q,c=cycles[0];x=start;suml=0;rows=[[] for _ in steps]
        for _ in range(q):
            for phase,(beta,alpha) in enumerate(steps):
                previous=x;x,skip=hop(x,beta,alpha);gap=previous+skip
                require(skip>=0,'nonnegative_gap_skip')
                require(prefix(gap)-prefix(previous)<=beta*U,'weighted_gap_inequality')
                require(prefix(gap+1)-prefix(previous)>beta*U,'endpoint_gap_exact')
                suml+=skip;rows[phase].append((previous%N,gap%N,skip))
        A=sum(a for _,a in steps);B=sum(b for b,_ in steps);m=len(steps)
        require(x==start+c*N,'full_word_cycle_closure')
        require(c*N==q*A*P+m*q+suml,'reduction_identity_5_1')
        defect=val-Q(A*P,N)-Q(B*U,V)
        reduced_rhs=Q(q*N*B*U,V)+m*(N-q)
        require((suml<=reduced_rhs)==(defect<=Q(m,q)),'reduction_equivalence_5_2')
        for row,(beta,alpha) in zip(rows,steps):
            require(len({z[0] for z in row})==q,'phase_start_injectivity')
            require(len({z[1] for z in row})==q,'phase_endpoint_gap_injectivity')
            if q==N:
                require(len({z[2] for z in row})==1,'full_period_constant_shift')
                ell=row[0][2]
                require(ell*V<=N*beta*U,'full_period_average')
        if q==N: require(defect<=Q(m,N),'full_period_bound')
    return val

def jn(r,s):
    cutoff=lcm(r.denominator,s.denominator)
    return max(Q((r*k).__floor__()+(s*k).__floor__()+1,k) for k in range(1,cutoff+1))

def pl_f(x):
    k=x.__floor__();x-=k
    return k+(5*x if x<=Q(1,6) else Q(5,6)+(x-Q(1,6))/5)
def pl_inverse(x):
    k=x.__floor__();x-=k
    return k+(x/5 if x<=Q(5,6) else Q(1,6)+5*(x-Q(5,6)))

def main():
    words=['ab','aab','abb','aabb','abab','abaab','abbab','aaabbb','abaabb','aababab','abaababb','abaabbabbbababaab']
    rats=sorted({Q(p,n) for n in range(1,6) for p in range(n)})
    collected=[];configurations=0;fullperiod=0;proper_both=0;maxscaled=Q(0);witness=None
    uneven_fullperiod=None;output_denominators=Counter()
    for r,s in product(rats,repeat=2):
        N=r.denominator;V=s.denominator;arrangements=list(compositions(V,N))
        require(len(arrangements)==comb(N+V-1,N-1),'gap_inventory_count')
        maxima={}
        for word in words:
            steps=phases(word);vals=[]
            for gaps in arrangements:
                val=orbit_data(gaps,r.numerator,s.numerator,steps)
                vals.append(val);configurations+=1
                if val.denominator==N:
                    fullperiod+=1
                    if len(set(gaps))>1 and uneven_fullperiod is None:
                        uneven_fullperiod={'word':word,'r':str(r),'s':str(s),'gaps':gaps,'value':str(val)}
                if val.denominator<min(N,V):proper_both+=1
            R=max(vals);A=word.count('a');B=word.count('b');m=len(steps);q=R.denominator
            defect=R-A*r-B*s;maxima[word]=R
            require(defect>=0,'maximal_rigid_translation_lower_bound')
            require(defect<=m,'maximal_global_m_bound')
            require(defect<=Q(m,q),'maximal_refined_bound_finite_only')
            require(q<=min(N,V),'maximal_rationality_bound')
            output_denominators[str(q)]+=1
            if defect*q>maxscaled:
                maxscaled=defect*q;witness={'word':word,'r':str(r),'s':str(s),'R':str(R),'m':m,'q_times_defect':str(maxscaled)}
            collected.append({'word':word,'r':str(r),'s':str(s),'R':str(R),'configurations':len(vals)})
        require(maxima['ab']==jn(r,s),'independent_jn_formula')
        require(maxima['abab']==2*maxima['ab'],'independent_power_identity')
    # Exact false phase bound, reconstructed directly from cumulative gap counts.
    gaps=(1,1,1,1,96);S=[0]
    for t in gaps:S.append(S[-1]+t)
    skips=[];ends=[]
    for i in range(4):
        rank=S[i]+1;turn,y=divmod(rank,100);j=5*turn+bisect_right(S,y)-1
        skips.append(j-i);ends.append(j)
    require(skips==[1]*4 and len(set(ends))==4,'false_phase_configuration')
    false_rhs=Q(4*5,100)+1
    require(sum(skips)>false_rhs,'phase_shortcut_rejected')
    image=sorted({(j+2)%5 for j in ends})
    require(image==[0,1,3,4] and image!=list(range(4)),'phase_not_a_closed_four_cycle')
    # Fixed-point / supremum separation, with every PL breakpoint and all
    # affine pieces checked by endpoint plus midpoint tests on a full period.
    require(pl_f(0)==0,'pl_f_fixed_point')
    require(pl_inverse(Q(1,6)+Q(2,3))==Q(1,6),'pl_g_fixed_point')
    cuts=sorted({Q(0),Q(1),Q(1,6),Q(5,6),Q(1,3)})
    tests=set(cuts)|{(a+b)/2 for a,b in zip(cuts,cuts[1:])}
    for period in range(-3,4):
        for z in tests:
            x=z+period;g=pl_inverse(x+Q(2,3))
            require(pl_f(pl_inverse(x))==x and pl_inverse(pl_f(x))==x,'pl_inverse_identity')
            require(pl_f(g)==x+Q(2,3),'pl_product_is_translation')
            require(pl_f(x+1)==pl_f(x)+1,'pl_lift_periodicity')
    require(jn(Q(0),Q(0))==1,'nonextremal_supremum_control')
    require(Q(2,3)>Q(1,3),'nonextremal_false_bound_rejected')
    require(jn(Q(1,5),Q(1,5))==1,'wrong_input_denominator_exact_value')
    require(Q(3,5)>Q(1,5),'wrong_input_denominator_rejected')
    # Lower-left half-rotation versus the point value, using exact ab formula.
    require(jn(Q(1,2),Q(1,2))==Q(3,2),'pointwise_half_rotation_ab')
    lower_left=[]
    for n in [3,5,8,13,21,34,55]:
        x=Q(1,2)-Q(1,2*n);v=jn(x,x)
        require(v==1,'half_rotation_lower_left_ab_sequence')
        lower_left.append({'r_equals_s':str(x),'R_ab':str(v)})
    # Integer lifts are never reduced modulo one in the target.
    shifted=[]
    for r,s in [(Q(-7,5),Q(12,5)),(Q(7,3),Q(-4,7)),(Q(-2),Q(3))]:
        j=r.__floor__();k=s.__floor__();R=jn(r-j,s-k)+j+k
        require(R-r-s==jn(r-j,s-k)-(r-j)-(s-k),'integer_shift_defect')
        require(R.denominator==jn(r-j,s-k).denominator,'integer_shift_denominator')
        shifted.append({'r':str(r),'s':str(s),'R_ab':str(R)})
    # Denominator reduction for powers, independently on a larger finite range.
    for d in range(1,51):
        for c in range(-50,51):
            if gcd(c,d)!=1:continue
            for m in range(1,21):
                require(Q(m*c,d).denominator==d//gcd(m,d),'power_denominator_reduction')
    raw=(json.dumps(collected,sort_keys=True,separators=(',',':'))+'\n').encode()
    out={'status':'PASS_INDEPENDENT_BOUNDED_CONTROLS','method':'gap compositions, blockwise X-index maps, every X initial orbit, phase identities; no author-code imports','rational_inputs':len(rats),'words':words,'word_parameter_cases':len(collected),'configurations':configurations,'all_control_assertions':sum(COUNTS.values()),'checks_by_label':dict(sorted(COUNTS.items())),'output_denominators':dict(sorted(output_denominators.items())),'full_input_X_period_configurations':fullperiod,'proper_subset_of_both_input_orbits_configurations':proper_both,'nonuniform_gap_full_period_example':uneven_fullperiod,'largest_q_times_defect':witness,'oracle_case_stream_sha256':hashlib.sha256(raw).hexdigest(),'oracle_case_stream_bytes':len(raw),'false_phase_control':{'gaps':gaps,'skips':skips,'sum':sum(skips),'false_rhs':str(false_rhs),'next_a_image':image,'closed_four_cycle':False},'supremum_control':{'tau_f':'0','tau_g':'0','tau_fg':'2/3','R_ab_0_0':'1','false_upper':'1/3'},'wrong_denominator_control':{'r':'1/5','s':'1/5','R':'1','defect':'3/5','false_upper':'1/5'},'lower_left_vs_pointwise':{'word':'ab','target_r_equals_s':'1/2','lower_left':'1','pointwise':'3/2','sequence':lower_left},'integer_shift_controls':shifted,'scope':'Bounded arithmetic and combinatorial checks; no infinite theorem, formal verification, novelty, or global openness claim.'}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
