"""Independent exact reconstruction from current manuscript, before helper code.

Uses mass-action expansion, rational linear algebra, explicit ideal products,
modular irreducibility, Sturm signs and a separated integer search.
"""
from pathlib import Path
from fractions import Fraction
from math import gcd
from functools import reduce
import datetime, hashlib, json
import sympy as S

HERE=Path(__file__).resolve().parent
x,y,z,t,a,b,c,d,h,slack=S.symbols('x y z t a b c d h slack')
Q=S.Rational
checks=[]
def check(label,condition):
    if not bool(condition):raise RuntimeError(label)
    checks.append(label)
def zero(expr):return S.cancel(expr)==0
def record(name,data):
    (HERE/name).write_text(json.dumps(data,indent=2)+'\n')

complexes=[(0,0,0),(0,0,1),(0,0,3),(0,1,1),(0,3,0),(1,0,1),(1,1,0),(1,1,1),(2,1,0),(3,0,0)]
edges=[(0,1),(0,4),(0,6),(1,7),(2,4),(2,7),(2,9),(3,4),(5,9),(8,9)]
directed=[pair for i,j in edges for pair in [(i,j),(j,i)]]
ks=[(62*d-15*c)/48,33*(58*d-45*c)/160,16*d/15,(c-b)/3,(154*d-221*c)/224,(9856*d-3315*c)/1470,45*(154*d-221*c)/3136,5*c/14,(15*a+16*d)/15,(62*d-15*b-15*c)/45,(154*d-192*a-221*c)/64,11*(58*d-45*c)/60,a,2*(31*d-15*c)/45,88*d/15,b,88*d/15,c,33*d/5,d]
mons=[x**u*y**v*z**w for u,v,w in complexes]
N=S.Matrix.hstack(*[S.Matrix(complexes[j])-S.Matrix(complexes[i]) for i,j in directed])
unit=[S.Matrix([mons[i]*v for v in N[:,k]]) for k,(i,j) in enumerate(directed)]
L=z-x-y+1;conic=7*x*x-2*x*y-16*x+7*y*y-16*y+16
P=S.groebner([L,conic],z,y,x,order='lex',domain=S.QQ)
basis=[1,x,y,x*x,x*y,x**3,x*x*y]
M=S.Matrix(21,20,lambda row,col:S.Poly(P.reduce(unit[col][row//7])[1],x,y).coeff_monomial(basis[row%7]))
minor_rows=[0,1,2,4,5,6,7,8,9,12,13,14,15,16,18,19]
minor_cols=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,16,18]
check('rank_minor',M.extract(minor_rows,minor_cols).det()==Q(7255941120,823543))
computed=S.Matrix.hstack(*M.nullspace());free=[12,15,17,19]
computed=computed*computed.extract(free,list(range(4))).inv()
declared=S.Matrix(ks).jacobian([a,b,c,d])
check('family_recovered_independently',computed==declared and M*computed==S.zeros(21,4))
check('rank_and_nullity',M.rank()==16 and len(M.nullspace())==4)
check('positive_cone_parameterization',all(all(v>=0 for v in S.Poly(S.expand(k.subs({c:b+h,d:(192*a+221*(b+h)+slack)/154})),a,b,h,slack).coeffs()) and k!=0 for k in ks))
check('stoichiometric_rank',N.rank()==3 and N[:,[0,2,4]].det()==-3)
reached={0}
while True:
    new=reached|{j for i,j in directed if i in reached}
    if new==reached:break
    reached=new
check('connected_reversible',len(reached)==10 and all((j,i) in directed for i,j in directed))
check('nonsingular_projective_conic',S.Matrix([[7,-1,-8],[-1,7,-8],[-8,-8,16]]).det()==-256)
den=t*t-t+1;param={x:(t*t+3)/(2*den),y:(3*t*t+1)/(2*den),z:(t*t+t+1)/den}
check('parametrization_exact',zero(L.subs(param)) and zero(conic.subs(param)))
check('ellipse_identity',zero(conic.subs({x:(z+1+h)/2,y:(z+1-h)/2})-(4*(h*h+(z-1)**2)-(z+1)**2)))
check('rational_inverse',zero((2*(z-1)/(3*x-y)).subs(param)-t))
check('unique_omitted_point',S.factor(conic.subs({y:3*x}))==16*(2*x-1)**2)
check('nonzero_parametric_tangent',zero(S.diff(param[z],t)-2*(1-t*t)/den**2) and all(S.diff(param[x],t).subs(t,v)!=0 for v in [-1,1]))
record('independent-matrix.json',{'shape':list(M.shape),'rows':[[str(q) for q in row] for row in M.tolist()],'kernel':[[str(q) for q in row] for row in computed.tolist()]})
print('family and conic checked',flush=True)

clean_rates=[1160,10296,976,23,560,5977,1800,25,1629,1237,1,9152,653,1214,5368,1,5368,70,6039,915]
old_rates=[845740,7732494,702464,3920,437290,4380128,1405575,5600,706384,900816,1518755,6873328,3920,896896,3863552,3920,3863552,15680,4346496,658560]
clean_expected=[-4697*x**3+6039*x*x*y-9177*x*y*z-5977*x*y+10736*x*z+1960*z**3+1800*z+560,915*x**3-6039*x*x*y-9177*x*y*z-5977*x*y-3782*y**3+10736*y*z+4888*z**3+1800*z+3488,3712*x**3+18304*x*y*z-5368*x*z+3712*y**3-5368*y*z-6848*z**3-10296*z+1160]
old_expected=[-3380608*x**3+4346496*x*x*y-6878928*x*y*z-4380128*x*y+7727104*x*z+1530515*z**3+1405575*z+437290,658560*x**3-4346496*x*x*y-6878928*x*y*z-4380128*x*y-2722048*y**3+7727104*y*z+3637907*z**3+1405575*z+2544682,2706368*x**3+13746656*x*y*z-3863552*x*z+2706368*y**3-3863552*y*z-5168422*z**3-7732494*z+845740]

def modular_irreducibility(poly):
    pp=S.Poly(poly,z,domain=S.QQ).clear_denoms()[1].primitive()[1]
    n=pp.degree()
    for prime in list(S.primerange(2,200)):
        f=S.Poly(pp.as_expr(),z,modulus=prime)
        if f.degree()!=n:continue
        f=f.monic();base=S.Poly(z,z,modulus=prime)
        def powmod(p,exponent):
            result=S.Poly(1,z,modulus=prime)
            while exponent:
                if exponent&1:result=(result*p).rem(f)
                p=(p*p).rem(f);exponent//=2
            return result
        tests={str(n//q):S.gcd(f,powmod(base,int(prime)**(n//q))-base).degree() for q in S.factorint(n)}
        end=(powmod(base,int(prime)**n)-base).rem(f)
        if all(v==0 for v in tests.values()) and end.is_zero:
            return {'prime':int(prime),'degree':n,'gcd_degrees':tests,'frobenius_final_zero':True,'primitive_coefficients':[str(v) for v in pp.all_coeffs()]}
    raise RuntimeError('no modular irreducibility certificate below 200')

def specialize(label,params,rates,expected):
    check(label+'_rates_exact',[k.subs(dict(zip([a,b,c,d],params))) for k in ks]==rates)
    F=[S.expand(sum(rates[j]*unit[j][i] for j in range(20))) for i in range(3)]
    check(label+'_field_exact',F==expected)
    check(label+'_conic_membership',all(P.reduce(f)[1]==0 for f in F))
    check(label+'_pairwise_gcd',all(S.gcd(F[i],F[j])==1 for i in range(3) for j in range(i)))
    w=S.Symbol('w');hom=[S.Poly(f,x,y,z).homogenize(w).as_expr() for f in F]
    check(label+'_homogeneous_gcd',reduce(S.gcd,hom)==1)
    check(label+'_rank_two_on_conic',S.Matrix(F).jacobian([x,y,z]).subs({x:Q(3,2),y:Q(1,2),z:1}).rank()==2)
    G=S.groebner(F,x,y,z,order='lex',domain=S.QQ)
    check(label+'_three_basis_elements',len(G.polys)==3)
    D=y*y-y*z-y+Q(7,16)*z*z-Q(1,8)*z+Q(7,16)
    g0,g1,g2=[p.as_expr() for p in G.polys]
    H,rem1=S.div(g1,D,x,y,z);R,rem2=S.div(g2,D,x,y,z)
    check(label+'_triangular_factorization',rem1==rem2==0 and S.Poly(g0,x).degree()==1 and S.diff(g0,x)==1 and S.Poly(H,y).degree()==1 and not S.diff(H,y).free_symbols and R.free_symbols<={z})
    certificate=modular_irreducibility(R)
    check(label+'_degree_fifteen_irreducible',certificate['degree']==15)
    pp=S.groebner([L,D],x,y,z,domain=S.QQ);qq=S.groebner([g0,H,R],x,y,z,domain=S.QQ)
    check(label+'_q_triangular',len(qq.polys)==3 and S.diff(qq.polys[0].as_expr(),x)==1 and S.diff(qq.polys[1].as_expr(),y)==1 and qq.polys[2].as_expr().free_symbols<={z})
    check(label+'_D_nonzero_in_residue_field',qq.reduce(D)[1]!=0)
    check(label+'_primes_comaximal',list(S.groebner([L,D,g0,H,R],x,y,z,domain=S.QQ))==[S.Integer(1)])
    check(label+'_K_in_both_primes',all(pp.reduce(f)[1]==0 and qq.reduce(f)[1]==0 for f in F))
    check(label+'_prime_product_in_K',all(G.reduce(S.expand(u*v))[1]==0 for u in [L,D] for v in [g0,H,R]))
    check(label+'_not_detailed_balance_at_conic_point',rates[0]!=rates[1])
    record(label+'-ideal-certificate.json',{'parameters':params,'rates':rates,'field':[str(f) for f in F],'groebner_basis':[str(p.as_expr()) for p in G.polys],'H':str(H),'R':str(R),'q_basis':[str(p.as_expr()) for p in qq.polys],'D_residue':str(qq.reduce(D)[1]),'modular_irreducibility':certificate,'gcd':reduce(gcd,rates),'largest_rate':max(rates),'rate_sum':sum(rates)})
    print(label+' radical decomposition checked',flush=True)
    return F

Fc=specialize('clean',[653,1,70,915],clean_rates,clean_expected)
F0=specialize('frozen',[3920,3920,15680,658560],old_rates,old_expected)
check('clean_primitive_and_totals',reduce(gcd,clean_rates)==1 and max(clean_rates)==10296 and sum(clean_rates)==52464)

# Closed-form separation replaces a four-dimensional brute-force search.
# At fixed c,d, all a/b-dependent rates are below 88*d/15, already a fixed rate.
# Sum is affine with slope -1 in a and +1/3 in b, so its minimizer is the
# largest admissible integral a and least admissible positive b respectively.
linear_sum=S.expand(sum(ks))
check('integer_objective_slopes',S.diff(linear_sum,a)==-1 and S.diff(linear_sum,b)==Q(1,3))
bestmax=None;bestsum=None;maxparams=[];sumparams=[];feasible_cd=0
for dd in range(15,2714,15):
    for cc in range(14,dd,14):
        bb=cc%3 or 3
        if bb>=cc:continue
        C27=Fraction(154*dd-221*cc,64)
        if C27.denominator!=1:continue
        aa=(C27.numerator-1)//3
        if aa<1:continue
        vals=[Fraction(v) for v in [Fraction(62*dd-15*cc,48),Fraction(33*(58*dd-45*cc),160),Fraction(16*dd,15),Fraction(cc-bb,3),Fraction(154*dd-221*cc,224),Fraction(9856*dd-3315*cc,1470),Fraction(45*(154*dd-221*cc),3136),Fraction(5*cc,14),Fraction(15*aa+16*dd,15),Fraction(62*dd-15*bb-15*cc,45),Fraction(154*dd-192*aa-221*cc,64),Fraction(11*(58*dd-45*cc),60),aa,Fraction(2*(31*dd-15*cc),45),Fraction(88*dd,15),bb,Fraction(88*dd,15),cc,Fraction(33*dd,5),dd]]
        if any(v.denominator!=1 or v<=0 for v in vals):continue
        feasible_cd+=1;vals=[int(v) for v in vals];mx=max(vals);sm=sum(vals)
        if dd<1755:
            if bestmax is None or mx<bestmax:bestmax=mx;maxparams=[]
            if mx==bestmax:maxparams.append([aa,bb,cc,dd])
        if bestsum is None or sm<bestsum:bestsum=sm;sumparams=[]
        if sm==bestsum:sumparams.append([aa,bb,cc,dd])
check('exact_two_integer_optima',bestmax==10296 and bestsum==52464 and [653,1,70,915] in maxparams and [653,1,70,915] in sumparams)
record('integer-optimality.json',{'method':'Complete c,d search after exact integrality and monotone-separation argument in report','d_upper_strict':2714,'max_search_d_upper_strict':1755,'feasible_cd':feasible_cd,'minimum_max':bestmax,'minimum_sum':bestsum,'representative_max_parameters':maxparams,'sum_parameters':sumparams})
print('integer optima checked',flush=True)

J=S.Matrix(F0).jacobian([x,y,z]);Jt=J.subs(param)
tau=S.cancel(S.trace(Jt));product_transverse=S.cancel((S.trace(Jt)**2-S.trace(Jt*Jt))/2)
check('tangent_eigenvalue_zero',zero(Jt.det()))
T=5399367*t**4+1602005*t**3+11579010*t*t+1602005*t+6979911
Npoly=5730530769*t**8+20026244073*t**7+29613209084*t**6+118245415239*t**5-38238695578*t**4+127692520263*t**3-127590858244*t*t+10579139049*t-79465564719
E=31399532062137*t**8+25149913538286*t**7+139213446954293*t**6+100751092465458*t**5+199590946186248*t**4+109518436416306*t**3+114191722124597*t*t+26510727150318*t+17568656198073
check('trace_formula',zero(tau+8*T/den**2));check('product_formula',zero(product_transverse+6272*Npoly/den**4));check('discriminant_formula',zero(tau*tau-4*product_transverse-64*E/den**4))
def sign_at(poly,where):
    p=S.Poly(poly,t)
    if where in ('minus_infinity','plus_infinity'):
        return int(S.sign(p.LC()))*((-1)**p.degree() if where=='minus_infinity' else 1)
    return int(S.sign(p.eval(where)))
def variations(seq,where):
    signs=[sign_at(p,where) for p in seq];nonzero=[v for v in signs if v]
    return sum(u!=v for u,v in zip(nonzero,nonzero[1:])),signs
sturm={}
for name,poly in [('T',T),('E',E),('N',Npoly)]:
    seq=S.sturm(poly,t)
    locations=['minus_infinity',-4,-3,Q(9,10),1,'plus_infinity']
    vv={str(loc):variations(seq,loc) for loc in locations}
    total=vv['minus_infinity'][0]-vv['plus_infinity'][0]
    check(name+'_real_root_count',total==(2 if name=='N' else 0))
    if name!='N':check(name+'_positive',poly.subs(t,0)>0)
    else:
        check('N_root_isolation',vv['-4'][0]-vv['-3'][0]==1 and vv['9/10'][0]-vv['1'][0]==1)
        check('N_interval_signs',[sign_at(poly,q) for q in [-4,-3,Q(9,10),1]]==[1,-1,-1,1])
    sturm[name]={'polynomial':str(poly),'chain':[str(p) for p in seq],'variations_and_signs':vv,'total_real_roots':total}
check('infinity_saddle',S.limit(product_transverse,t,S.oo)<0 and J.subs({x:Q(1,2),y:Q(3,2),z:1}).det()==0)
check('gcd_negative_control',S.gcd(L*Fc[0],L*Fc[1]) not in [1,-1])
check('single_rate_perturbation_leaves_family',any(P.reduce(unit[0][i])[1]!=0 for i in range(3)))
check('strict_cone_boundary_rejected',ks[10].subs({d:(192*a+221*c)/154})==0)
record('sturm-and-spectrum.json',{'sturm':sturm,'tau':str(tau),'transverse_product':str(product_transverse),'infinity_product':str(S.limit(product_transverse,t,S.oo))})
record('independent-controls.json',{'status':'PASS_INDEPENDENT_EXACT_RECONSTRUCTION','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sympy_version':S.__version__,'checks_passed':len(checks),'checks':checks,'helper_code_read_before_authoring':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
print('all independent algebra checks passed: '+str(len(checks)),flush=True)
