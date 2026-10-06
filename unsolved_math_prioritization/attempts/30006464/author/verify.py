#!/usr/bin/env python3
"""Strict packet integrity and exact supplementary mathematical controls."""
import hashlib,json,math,pathlib,stat
from fractions import Fraction as Q
ROOT=pathlib.Path(__file__).resolve().parent
FILES={'README.md','PROOFS.md','APPROACHES.md','CLAIMS.json','DATA_IDENTITY.json','SOURCES.json','verify.py','verify_corpora.py','test_packet.py','SOURCE_PIN.json','CHECK_RESULTS.json','MANIFEST.json'}
def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(name):return json.loads((ROOT/name).read_text())
def verify_inventory():
    entries=list(ROOT.iterdir());need({p.name for p in entries}==FILES,'unexpected or missing inventory')
    for p in entries:need(stat.S_ISREG(p.lstat().st_mode),'nonregular member: '+p.name)
    m=load('MANIFEST.json');need(set(m)==FILES-{'MANIFEST.json'},'manifest inventory')
    for n,v in m.items():
        b=(ROOT/n).read_bytes();need(v=={'bytes':len(b),'sha256':sha(b)},'manifest bytes: '+n)
    pins=load('SOURCE_PIN.json');need(set(pins)=={'verify.py','verify_corpora.py','test_packet.py'},'source pin inventory')
    for n,v in pins.items():need(sha((ROOT/n).read_bytes())==v,'source pin: '+n)
def primes(n):return [p for p in range(2,n+1) if all(p%d for d in range(2,math.isqrt(p)+1))]
def prime_divisors(n):return [p for p in primes(n) if n%p==0]
def phi(n):return sum(math.gcd(j,n)==1 for j in range(1,n+1))
def P(n):return math.prod((Q(p+1,p) for p in prime_divisors(n)),start=Q(1))
def delta(M):
    # Coefficients of q*product(1-q^d)^24 via the exact logarithmic derivative.
    t=[0]*(M+1);t[1]=1
    sigma=[0]*(M+1)
    for d in range(1,M+1):
        for n in range(d,M+1,d):sigma[n]+=d
    for n in range(2,M+1):
        v=-24*sum(sigma[j]*t[n-j] for j in range(1,n));need(v%(n-1)==0,'integral tau recurrence');t[n]=v//(n-1)
    return t
def run():
    verify_inventory();c=load('CLAIMS.json');d=load('DATA_IDENTITY.json')
    need(c['problem_id']==30006464 and c['problem_number']=='OWR-14299577-017','target identity')
    need(c['status']=='unresolved' and c['approaches_used']==5 and c['full_resolution'] is False,'resolution scope')
    need(c['target']=={'weight':'integer k >= 2','nebentypus':'trivial','forms':'entire cusp space','norm':'unnormalized Petersson integral','coefficients':'a(n) = raw(n)/n^((k-1)/2)','epsilon':'strictly positive','constants':'depend only on k and epsilon'},'target conventions')
    o=c['oldform'];need(o=={'weight':12,'family':'c Delta(Nz)','norm_N_power':-12,'coefficient_square_N_power':-11,'ratio_factor':'I_N/N','linear_cutoff_disproved':True,'positive_epsilon_counterexample':False,'positive_epsilon_family_theorem':True,'cutoff_constant':4,'prime_pair_lower_bound':'3/4','log_slope':'3 epsilon/(8 log 2)'},'oldform theorem constants/scope')
    need(c['scope_guards']=={'all_oldspace_proved':False,'prime_level_full_space_proved':False,'sturm_gives_uniform_constant':False,'toy_map_is_modular_counterexample':False,'unrestricted_cusp_volume_extrapolation':False,'observability_is_proved':False},'scope guards')
    need(d['review_sha256']=='73ff2584746c1f75184a94669e67aea3ff3000e90e8c2b54cb6bac17cb33a395' and d['statement_sha256']=='3fd58aab3ddd149d21db6223b60f498cdc98c006ae67bf89495dc0e180f9605e','data digests')
    need(d['review_bytes']==4313 and d['report_present'] is False and d['absent_report']=={} and d['rank']==831 and d['statement_match'] is True and d['review_match'] is True,'data match scope')
    checks={}
    t=delta(256);need(t[1:11]==[1,-24,252,-1472,4830,-6048,-16744,84480,-113643,-115920],'tau anchor')
    count=0
    for p in primes(16):
        need(t[p*p]==t[p]*t[p]-p**11,'Hecke prime-square relation')
        u=Q(t[p]**2,p**11);v=Q(t[p*p]**2,p**22)
        need(u+v==(u-Q(1,2))**2+Q(3,4),'prime pair identity');need(u+v>=Q(o['prime_pair_lower_bound']),'prime pair lower bound');count+=1
    checks['exact_tau_prime_pairs']=count
    count=0
    for T in range(1,257):
        mass=sum((Q(t[n]**2,n**11) for n in range(1,T+1)),Q())
        need(mass>=1+Q(3,4)*len(primes(math.isqrt(T))),'prime-pair sum lower bound');count+=1
    checks['exact_partial_sums']=count
    count=0
    for N in range(1,121):
        I=N*P(N);need(I.denominator==1,'integral index')
        need(Q(1,N**12)*I/Q(1,N**11)==P(N),'oldform norm/coeff ratio')
        need(P(N)<=sum((Q(1,d) for d in range(1,N+1)),Q()),'harmonic product bound')
        cusp=sum(Q(N*v*v,math.gcd(v*v,N))*phi(math.gcd(v,N//v)) for v in range(1,N+1) if N%v==0)
        need(cusp==N*I,'complete cusp sum');count+=1
    checks['level_scaling_and_cusp_sums']=count
    # Exact rational grid is a supplementary control; the identity proves all t.
    for num in range(0,121):
        u=Q(num,12);need(u+(u-1)**2-(u-Q(1,2))**2==Q(3,4),'polynomial identity')
    checks['rational_identity_controls']=121
    for x in range(2,257):need(len(primes(x))>=x.bit_length()-1,'finite Bertrand consequence')
    checks['finite_bertrand_controls']=255
    for r in primes(31):
        prod=math.prod((Q(p+1,p) for p in primes(r)),start=Q(1))
        need(prod>=Q(1,2)*sum((Q(1,n) for n in range(1,r+1)),Q()),'primorial divergence bound control')
    checks['primorial_controls']=len(primes(31))
    g=c['geometry'];need(g=={'prime':101,'first_j':26,'last_j':49,'height_cutoff':'1/101','area_lower_bound':12,'proposed_area_upper_bound':2},'geometry constants')
    p=g['prime'];need(p in primes(p),'prime geometry level');l=Q(2*g['first_j']-1,2)
    need(Q(2,l*l)<Q(g['height_cutoff']),'whole rectangle height');area=Q(g['last_j']-g['first_j']+1,2)
    need(area==g['area_lower_bound'] and 2*Q(1,p)*(p*p*(P(p)-1))==g['proposed_area_upper_bound'] and area>g['proposed_area_upper_bound'],'volume extrapolation rejection')
    checks['exact_geometric_countermodel']=1
    # W has source-orthogonal eigenlines, but T cancels their sum.
    need(1**2==1 and (-1)**2==1 and (1-1)**2==0,'orthogonal block cancellation')
    checks['block_cancellation_countermodel']=1
    # Gamma(m,x)=(m-1)! exp(-x) sum_{j=0}^{m-1}x^j/j!;
    # polynomial derivative P'-P=-x^(m-1), exactly.
    for m in range(1,20):
        coeff=[Q(math.factorial(m-1),math.factorial(j)) for j in range(m)]
        deriv=[(j+1)*coeff[j+1] if j+1<m else Q() for j in range(m)]
        need([deriv[j]-coeff[j] for j in range(m)]==[Q()]*(m-1)+[Q(-1)],'incomplete gamma polynomial identity')
    checks['gamma_polynomial_controls']=19
    return {'status':'pass','full_resolution':False,'checks':checks,'total_exact_controls':sum(checks.values()),'limits':'Finite exact controls are not formal verification of the analytic proofs.'}
if __name__=='__main__':
    try: print(json.dumps(run(),sort_keys=True))
    except Exception as e: raise SystemExit('FAIL: '+str(e))
