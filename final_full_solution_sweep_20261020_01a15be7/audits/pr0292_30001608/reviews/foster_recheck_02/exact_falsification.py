"""Fresh exact boundary/negative diagnostics; no author/checker imports.
Poisson potential is solved from a killed tridiagonal linear system.
Finite tests supplement the separate all-state analytic review.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, random, sys
sys.set_int_max_str_digits(0)
C=Counter()
def ck(ok,label):
    if not ok: raise AssertionError(label)
    C[label]+=1
def ceil(v): return -((-v.numerator)//v.denominator)
def floor(v): return v.numerator//v.denominator

def build(lam):
    beta=F(17,8)*lam; c=2*beta+8; m=4*c; theta=beta+c+4
    gamma=1-F(1)/(theta+2); eta=1-F(1)/(2*(theta+2)); ell=2*(theta+2)
    weights=[F(1)]; R=0
    while True:
        R+=1; weights.append(weights[-1]*gamma)
        mu=sum(k*w for k,w in enumerate(weights))/sum(weights)
        if mu>theta and F(7,8)*(R+1)>beta+c+2: break
    # Solve Qg=k-mu for k<R with g(R)=0, using tridiagonal elimination.
    lo=[F(k) for k in range(R)]; up=[gamma*(k+1) for k in range(R)]
    diag=[-lo[k]-up[k] for k in range(R)]; rhs=[F(k)-mu for k in range(R)]
    for k in range(1,R):
        scale=lo[k]/diag[k-1]
        diag[k]-=scale*up[k-1]; rhs[k]-=scale*rhs[k-1]
    gs=[F(0)]*(R+1)
    for k in range(R-1,-1,-1): gs[k]=(rhs[k]-up[k]*gs[k+1])/diag[k]
    G=gs[0]
    N=ceil(max(F(R+2),F(3*(R+1)),(m+(1+eta)*R+eta)/(1-eta),ell*G*(lam+4*(2*R+1))))
    B=(N+R+1)*(beta+c+G*(lam+2*(N+R))+1)
    return locals()
def g(k,p):
    assert k>=0
    return p['gs'][k] if k<p['R'] else F(0)
def f(t,p): return max(F(0),min(F(1),(t-p['gamma'])*p['ell']))
def h(z,p): return abs(z) if abs(z)>=p['m'] else z*z/(2*p['m'])+p['m']/2
def hp(z,p): return min(F(1),max(F(-1),z/p['m']))
def field(s,p):
    a,b,x,y=s; D=x+y+1; Z=a+x-b-y; W=2*a+2*b+x+y
    fs=(f(F(b,D),p),f(F(a,D),p)); gs=(g(y,p),g(x,p)); js=tuple(v*w for v,w in zip(fs,gs))
    return {'D':D,'Z':Z,'W':W,'fs':fs,'gs':gs,'js':js,'J':sum(js),'V':W+p['c']*h(F(Z),p)+sum(js)}
def events(s,p):
    a,b,x,y=s; D=x+y+1; out=[]
    for tag,j in (('arrival_a',0),('arrival_b',1)):
        t=list(s); t[j]+=1; out.append((tag,tuple(t),p['lam']/2))
    for tag,i,j,rate in (('first_a',0,2,F(a*(x+1),D)),('first_b',1,3,F(b*(y+1),D))):
        if rate:
            t=list(s); t[i]-=1; t[j]+=1; out.append((tag,tuple(t),rate))
    for tag,j,rate in (('departure_x',2,F(x*(y+1),D)),('departure_y',3,F(y*(x+1),D))):
        if rate:
            t=list(s); t[j]-=1; out.append((tag,tuple(t),rate))
    return out

def inspect(s,p):
    a,b,x,y=s; old=field(s,p); D=old['D']; u=F(a*(x+1)+b*(y+1),D); d=F(2*x*y+x+y,D)
    LW=LZ=LH=LJ=LV=err=base=F(0); prim=[F(0),F(0)]
    for tag,t,rate in events(s,p):
        ck(min(t)>=0,'valid_successor'); new=field(t,p)
        LW+=rate*(new['W']-old['W']); LZ+=rate*(new['Z']-old['Z'])
        LH+=rate*(h(F(new['Z']),p)-h(F(old['Z']),p))
        LJ+=rate*(new['J']-old['J']); LV+=rate*(new['V']-old['V'])
        e=sum(gv*(fn-fo) for gv,fn,fo in zip(new['gs'],new['fs'],old['fs']))
        b0=sum(fv*(gn-go) for fv,gn,go in zip(old['fs'],new['gs'],old['gs']))
        for k in range(2): prim[k]+=rate*old['fs'][k]*(new['gs'][k]-old['gs'][k])
        err+=rate*e; base+=rate*b0
        ck(new['J']-old['J']==e+b0,'postjump_product_identity')
        if tag.startswith('first'):
            ck(e<=0,'signed_first_interface')
            ck(all(n<=o for n,o in zip(new['js'],old['js'])),'first_products_nonincreasing')
        if tag.startswith('departure'):
            ck(all(0<=n-o<=2*p['ell']/D for n,o in zip(new['fs'],old['fs'])),'departure_ratio_bound')
    ck(LW==2*p['lam']-u-d,'workload_generator'); ck(LZ==F(y-x,D),'imbalance_generator')
    ck(LH<=hp(F(old['Z']),p)*LZ+(p['lam']+d)/(2*p['m']),'rounded_generator')
    ck(err<=p['ell']*p['G']*(p['lam']+4*d)/D,'global_interface')
    ck(LJ==base+err,'summed_product_identity'); ck(LJ<=p['G']*(p['lam']+2*d),'coarse_correction_bound')
    ck(LV<=p['beta']-u-F(7,8)*d+p['c']*hp(F(old['Z']),p)*F(y-x,D)+LJ,'combined_generator_bound')
    for k,visible in enumerate((y,x)):
        if visible<=p['R']: ck(prim[k]<=old['fs'][k]*(visible-p['mu']),'cutoff_poisson_actual_generator')
    ck(old['V']>=sum(s),'coercivity')
    ck(old['V']<=(2+p['c'])*sum(s)+p['c']*p['m']/2+2*p['G'],'linear_growth')
    if min(x,y)>=p['R']+1:
        ck(LJ==0,'region_I_zero_successors'); ck(LV<-2,'region_I_negative')
    elif max(x,y)>=p['N']: ck(LV<=-3,'region_II_negative')
    else:
        ck(x+y<=p['N']+p['R'],'region_III_coverage')
        if a+b>p['B']: ck(LV<=-1,'region_III_negative')
    if x+y>p['N']+p['R'] or a+b>p['B']: ck(LV<=-1,'outside_F_negative')

def scalar(p):
    for sign in (-1,1):
        for offset in (F(-3,2),F(-1),F(-1,7),F(0),F(1,7),F(1),F(3,2)):
            z=sign*p['m']+offset
            for v in (F(-3),F(-1),F(-1,3),F(0),F(1,3),F(1),F(3)):
                ck(h(z+v,p)-h(z,p)<=hp(z,p)*v+v*v/(2*p['m']),'scalar_rounded_crossings')
    for D in (2,3,p['R']+1,p['N']):
        for z in (p['gamma'],p['eta']):
            for w in {0,floor(z*D),ceil(z*D),max(0,floor(z*D)-1),ceil(z*D)+1}:
                ck(0<=f(F(w,D-1),p)-f(F(w,D),p)<=2*p['ell']/D,'scalar_departure_contacts')
def poisson(p):
    R=p['R']; ck(0<p['gamma']<p['eta']<1,'parameter_order')
    ck(p['ell']==1/(p['eta']-p['gamma']),'cutoff_lipschitz_constant')
    ck(p['mu']>p['theta'] and p['mu']<R,'poisson_mean_margin')
    for k in range(R+2):
        value=p['gamma']*(k+1)*(g(k+1,p)-g(k,p)) if k<R else F(0)
        if k: value+=k*(g(k-1,p)-g(k,p))
        ck(value==k-p['mu'] if k<=R else value==0,'poisson_including_R_and_extension')
        ck(g(k,p)>=0,'potential_nonnegative')
        if k<R: ck(g(k+1,p)<g(k,p),'potential_strictly_decreasing')
    ck(p['N']>=R+2 and p['N']>=3*(R+1),'N_integer_constraints')
    ck((1-p['eta'])*p['N']-(1+p['eta'])*R-p['eta']>=p['m'],'N_imbalance_constraint')
    ck(p['ell']*p['G']*(p['lam']+4*(2*R+1))/p['N']<=1,'N_interface_constraint')

def states(p):
    R,N,B=p['R'],p['N'],p['B']; out={(a,b,x,y) for a in range(3) for b in range(3) for x in range(3) for y in range(3)}
    rng=random.Random(21032026+R)
    for _ in range(120): out.add(tuple(rng.randrange(2*R+3) for _ in range(4)))
    for x in (R,R+1,R+2,N-1,N,N+1):
        for y in (0,1,R-1,R,R+1):
            D=x+y+1
            bs={0,D*D,floor(p['gamma']*D),ceil(p['gamma']*D),floor(p['eta']*D),ceil(p['eta']*D),max(0,floor(p['gamma']*D)-1),ceil(p['eta']*D)+1}
            for b in bs:
                aa={0,D*D}
                for target in (floor(p['m']),ceil(p['m']),-floor(p['m']),-ceil(p['m'])):
                    for delta in (-1,0,1): aa.add(max(0,target-x+b+y+delta))
                for a in aa:
                    out.add((a,b,x,y)); out.add((b,a,y,x))
    huge=ceil(B)+1
    for x,y in ((0,0),(0,R),(R,R),(N-1,0),(N-1,R)):
        for total in (max(0,floor(B)),ceil(B),huge,2*huge):
            for a,b in ((total,0),(0,total),(total//2,total-total//2)):
                out.add((a,b,x,y)); out.add((b,a,y,x))
    return out

def negatives(p):
    out=[]
    lhs=p['lam']; rhs=p['lam']/(2*p['m'])
    ck(lhs>rhs,'negative_unsmoothed_absolute_detected')
    out.append({'mutation':'replace h by absolute value at Z=0','state':[0,0,0,0],'lhs':str(lhs),'claimed_upper':str(rhs)})
    ck(F(0)!=p['R']-p['mu'],'negative_absorbing_terminal_detected')
    out.append({'mutation':'omit death equation at terminal R','residual':str(-(p['R']-p['mu']))})
    slope=-g(p['R']-1,p); ck(slope<0,'negative_untruncated_corrector_detected')
    out.append({'mutation':'continue last negative slope past R','g_R_plus_1':str(slope)})
    D=max(4,ceil(1/(p['eta']-p['gamma']))); witness=None
    for n in range(1,4*D):
        delta=f(F(n,D-1),p)-f(F(n,D),p)
        if delta>0: witness=(n,D,delta); break
    ck(witness is not None,'negative_drop_departure_interface_detected')
    state=(0,witness[0],witness[1]-1,0)
    successor=(0,witness[0],witness[1]-2,0)
    delta_J=field(successor,p)['J']-field(state,p)['J']
    ck(delta_J>0,'negative_actual_departure_correction_detected')
    out.append({'mutation':'declare every interface error nonpositive','state':state,'successor':successor,'departure_rate':str(F(witness[1]-1,witness[1])),'positive_departure_cutoff_increment':str(witness[2]),'actual_delta_J':str(delta_J)})
    s=(2*p['R']+1,2*p['R']+1,p['R'],p['R']); old=field(s,p); witness=None
    for tag,t,rate in events(s,p):
        if tag.startswith('departure') and field(t,p)['J']>old['J']:
            witness={'tag':tag,'successor':t,'delta_J':str(field(t,p)['J']-old['J'])}; break
    ck(witness is not None,'negative_region_I_at_R_detected')
    out.append({'mutation':'claim J vanishes on every successor already at min(x,y)=R','state':s,'witness':witness})
    return out

def run():
    rows=[]; negative=[]
    for lam in (F(1,10**6),F(3,17),F(11,4),F(55,8)):
        p=build(lam); poisson(p); scalar(p); ss=states(p)
        for s in sorted(ss): inspect(s,p)
        for ratio in (p['gamma'],p['eta']):
            D=ratio.denominator
            for y in (0,min(p['R'],D-1)):
                s=(0,ratio.numerator,D-1-y,y); inspect(s,p); inspect((s[1],s[0],s[3],s[2]),p)
        negative.extend({'lambda':str(lam),**v} for v in negatives(p))
        rows.append({'lambda':str(lam),'R':p['R'],'N':p['N'],'B_floor':floor(p['B']),'B_ceiling':ceil(p['B']),'states':len(ss)+8,'mu_minus_theta_exact':str(p['mu']-p['theta']),'construction':'killed tridiagonal linear system with g(R)=0'})
        print('completed exact independent lambda='+str(lam)+' states='+str(len(ss)+8),file=sys.stderr,flush=True)
    original=Path(__file__).resolve().parents[2]/'original'
    hashes={str(v.relative_to(original)):hashlib.sha256(v.read_bytes()).hexdigest() for v in sorted(original.rglob('*')) if v.is_file()}
    return {'status':'PASS_NEW_EXACT_BOUNDARY_AND_NEGATIVE_DIAGNOSTICS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'loads':rows,'negative_controls':negative,'source_sha256':hashes,'limitations':'Finite exact falsification tests only. All-state/all-real-load deductions reviewed separately. No source-priority or publication clearance.'}
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
