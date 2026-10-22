#!/usr/bin/env python3
"""Fresh exact and high precision controls; no inherited checker is imported.

Run with the prescribed ALWAYS-B runtime and -B. Controls support the proof
audit, and are not interval certificates or proofs of universal identities.
"""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import sys
import sympy as sp
import mpmath as mp


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'submitted/unsolved_math_prioritization/attempts/5100033'
PDFS = HERE.parents[2] / 'pr211_5100063/initial_review_20261015/private_reading'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_controls():
    a, b, c, s, t = sp.symbols('a b c s t', nonzero=True)
    rel = sp.groebner([b*b-a*a+c*c, t*t+s*s-1], t, b, a, c, s)
    def ident(expr):
        num = sp.together(expr).as_numer_denom()[0]
        return sp.expand(rel.reduce(sp.expand(num))[1]) == 0
    norm = s*s/(a*a)+t*t/(b*b)
    direct = [c-(1+c*s/a)*s/(a*norm), (1+c*s/a)*t/(b*norm)]
    q = [a*(c-a*s)/(a-c*s), a*b*t/(a-c*s)]
    minus = [-c-(1-c*s/a)*s/(a*norm), (1-c*s/a)*t/(b*norm)]
    checks = {
        'projection_x': ident(direct[0]-q[0]),
        'projection_y': ident(direct[1]-q[1]),
        'bilinear_circle': ident(q[0]**2+q[1]**2-a*a),
        'minus_focus_x': ident(minus[0]+q[0].subs({s:-s,t:-t}, simultaneous=True)),
        'minus_focus_y': ident(minus[1]+q[1].subs({s:-s,t:-t}, simultaneous=True)),
        'root_numerator_x': ident(a*(c-a*a/c)+a*b*b/c),
        'root_numerator_y': sp.simplify(a*b*(-sp.I*b/c)+sp.I*a*b*b/c)==0,
    }
    alpha,k,kp,S,C,D = sp.symbols('alpha k kp S C D', nonzero=True)
    av = alpha*D/C
    bv = alpha*kp/C
    cv = alpha*k
    numerator = -av*bv*bv/cv
    derivminus = alpha*kp*kp*S/(C*C)
    rm = sp.simplify(numerator/derivminus)
    checks['explicit_residue'] = sp.simplify(rm + av/(k*S)) == 0
    R = sp.Matrix([rm, sp.I*rm])
    det = lambda u,v: sp.det(sp.Matrix.hstack(u,v))
    checks['opposite_residue_determinant'] = sp.simplify(det(R,-R)) == 0
    checks['isotropic_residue'] = sp.simplify((R.T*R)[0]) == 0
    mutant = sp.simplify(det(R,sp.Matrix([-rm,sp.I*rm])))
    checks['wrong_residue_direction_mutant_nonzero'] = mutant != 0
    assert all(checks.values()), checks
    return {'checks':checks, 'residue_minus':str(R), 'mutant_double_pole':str(mutant)}


def collision_controls(max_n=151):
    cases=phases=0
    records=[]
    for n in range(3,max_n+1):
        for tau in range(1,(n+1)//2):
            if math.gcd(n,tau)!=1:
                continue
            step=Fraction(tau,n)
            rootminus=Fraction(1,4)-Fraction(tau,2*n)
            rootplus=Fraction(1,4)+Fraction(tau,2*n)
            orbit={(rootminus-j*step)%1 for j in range(n)}
            assert len(orbit)==n
            assert orbit=={(rootplus-j*step)%1 for j in range(n)}
            # At each possible pole phase the precise pair is adjacent.
            for basej in range(n):
                # Common denominator 4N, using exact modular integers.
                modulus=4*n
                phase_num=n-2*tau-4*tau*basej
                singular=[]
                for j in range(n):
                    val=(phase_num+4*tau*j)%modulus
                    if val==(n-2*tau)%modulus:
                        singular.append((j,'minus'))
                    if val==(n+2*tau)%modulus:
                        singular.append((j,'plus'))
                assert sorted(singular)==sorted([(basej,'minus'),((basej+1)%n,'plus')])
                phases+=1
            L=Fraction(1,n)
            assert (rootplus-rootminus)%L==0
            assert (L/2)%L!=0
            assert Fraction(1,2)%L==(L/2 if n%2 else 0)
            # An explicit Bezout certificate for the real period.
            inv=pow(tau,-1,n)
            quot=(inv*tau-1)//n
            assert inv*step-quot==L
            cases+=1
            if n<=9 or n==max_n:
                records.append({'N':n,'tau':tau,'orbit_size':n,'adjacent_pairs':n,
                                'bezout':[inv,-quot]})
    return {'N_range':[3,max_n],'primitive_cases':cases,'pole_phase_checks':phases,
            'imaginary_copy_multiplicity':2,'selected_certificates':records,
            'all_exact_fraction_assertions_pass':True}


def det(u,v):
    return u[0]*v[1]-u[1]*v[0]


def relerr(x,y,scale=1):
    return abs(x-y)/max(mp.mpf(scale),abs(x),abs(y))


class Family:
    def __init__(self,k,n,tau):
        self.k=mp.mpf(k); self.m=self.k*self.k
        self.kp=mp.sqrt(1-self.m)
        self.K=mp.ellipk(self.m); self.Kp=mp.ellipk(1-self.m)
        self.N=n;self.tau=tau
        self.v=2*self.K*tau/n; self.delta=2*self.v;self.L=4*self.K/n
        self.b0=self.K-self.v; self.p=mp.j*self.Kp; self.r=self.K+self.p
        self.a=self.jac('dn',self.v)/self.jac('cn',self.v)
        self.b=self.kp/self.jac('cn',self.v);self.c=self.k
    def jac(self,kind,z):
        return mp.ellipfun(kind,z,self.m)
    def q(self,z):
        s=self.jac('sn',z);t=self.jac('cn',z)
        d=self.a-self.c*s
        return (self.a*(self.c-self.a*s)/d,self.a*self.b*t/d)
    def T(self,z):
        qs=[self.q(z+j*self.delta) for j in range(self.N)]
        return sum(det(qs[j],qs[(j+1)%self.N]) for j in range(self.N))/2
    def geometry(self,w,focus_sign):
        points=[(-self.a*self.jac('sn',w+j*self.delta),
                 self.b*self.jac('cn',w+j*self.delta)) for j in range(self.N)]
        normals=[(x/(self.a*self.a),y/(self.b*self.b)) for x,y in points]
        outer=[]
        for j in range(self.N):
            u=normals[j];v=normals[(j+1)%self.N]; d=det(u,v)
            assert abs(d)>mp.mpf('1e-120')
            outer.append(((v[1]-u[1])/d,(u[0]-v[0])/d))
        f=(focus_sign*self.c,mp.mpf(0)); feet=[]
        for j in range(self.N):
            x=outer[j]; y=outer[(j+1)%self.N]
            d=(y[0]-x[0],y[1]-x[1]); dd=d[0]*d[0]+d[1]*d[1]
            assert dd>0
            lam=((f[0]-x[0])*d[0]+(f[1]-x[1])*d[1])/dd
            feet.append((x[0]+lam*d[0],x[1]+lam*d[1]))
        return sum(det(feet[j],feet[(j+1)%self.N]) for j in range(self.N))/2


def numstr(x):
    return mp.nstr(x,32)


def numeric_controls():
    mp.mp.dps=140
    families=[('0.00000001',3,1),('0.2',5,2),('0.67',9,4),('0.93',15,2),
              ('0.999999999999',5,1),('0.67',31,1),('0.67',31,15),
              ('0.67',101,1),('0.67',101,50),('0.67',8,1),('0.93',8,3)]
    rows=[]
    for ks,n,tau in families:
        f=Family(ks,n,tau)
        w=mp.mpf('0.137')*f.K+mp.mpf('0.083')*f.p
        q=f.q(w);qp=f.q(w+2*f.p)
        sw=f.jac('sn',w);cw=f.jac('cn',w);dw=f.jac('dn',w)
        char={
            'quarter_shift_sn':relerr(f.jac('sn',f.r+w),dw/(f.k*cw)),
            'quarter_shift_cn':relerr(f.jac('cn',f.r+w),-mp.j*f.kp/(f.k*cw)),
            'quarter_shift_dn':relerr(f.jac('dn',f.r+w),mp.j*f.kp*sw/cw),
            'real_shift_dn_correct_sign':relerr(f.jac('dn',w+2*f.K),dw),
            'Q_imaginary_reflection':max(relerr(qp[0],q[0],f.a),relerr(qp[1],-q[1],f.a)),
            'T_antiperiod':relerr(f.T(w+2*f.p),-f.T(w),f.a*f.a),
            'T_reduced_period':relerr(f.T(w+f.L),f.T(w),f.a*f.a),
            'F_even':relerr(f.T(f.b0+w),f.T(f.b0-w),f.a*f.a),
            'forced_zero_1':abs(f.T(f.b0+f.p+f.L/2))/(f.a*f.a),
            'forced_zero_2':abs(f.T(f.b0+3*f.p+f.L/2))/(f.a*f.a),
        }
        halfproducts=[f.T(w+u*f.L)*f.T(w+(u+mp.mpf('.5'))*f.L)/(f.a**4)
                      for u in map(mp.mpf,['0','.173','.391'])]
        char['complex_halfperiod_product']=max(relerr(x,halfproducts[0]) for x in halfproducts)
        if n%2:
            char['odd_focus_halfperiod_match']=relerr(f.T(w+2*f.K),f.T(w+f.L/2),f.a*f.a)
        else:
            char['even_focus_equality']=relerr(f.T(w+2*f.K),f.T(w),f.a*f.a)
        realphases=[mp.mpf(x)*f.K for x in ['.071','.419','.883']]
        gp=[];geometry_error=mp.mpf(0)
        for phase in realphases:
            ap=f.geometry(phase,1);am=f.geometry(phase,-1)
            geometry_error=max(geometry_error,relerr(ap,f.T(phase),f.a*f.a),
                               relerr(am,f.T(phase+2*f.K),f.a*f.a))
            gp.append(ap*am/(f.a**4))
        product_spread=max(abs(x-gp[0]) for x in gp)
        if n%2:
            char['real_outer_geometry_product']=product_spread
        char['actual_outer_projection_agreement']=geometry_error
        # Wrong small-torus hypothesis for cn must fail away from zeros.
        cn=f.jac('cn',w);cnshift=f.jac('cn',w+2*f.p)
        wrong_cn_period=abs(cnshift-cn)/max(abs(cnshift),abs(cn))
        assert wrong_cn_period>mp.mpf('1.99')
        wrong_dn_sign=abs(f.jac('dn',w+2*f.K)+dw)/max(abs(dw),abs(f.jac('dn',w+2*f.K)))
        assert wrong_dn_sign>mp.mpf('1.99')
        # Removable common Jacobi poles: all four representatives on the large torus.
        common_errors=[]
        eps=mp.mpf('1e-32')*(1+mp.j)/mp.sqrt(2)
        for xpart in [0,2*f.K]:
            for ipart in [1,3]:
                val=f.q(xpart+ipart*f.p+eps)
                target=(f.a*f.a/f.c,(1 if ipart==1 else -1)*mp.j*f.a*f.b/f.c)
                common_errors.append(max(relerr(val[j],target[j],f.a) for j in [0,1]))
        char['common_Jacobi_poles_removable_limit']=max(common_errors)
        for name,error in char.items():
            tol=mp.mpf('1e-24') if 'removable' in name else mp.mpf('1e-90')
            assert error<tol,(ks,n,tau,name,numstr(error))
        # Explicit residues, local order, and deliberately wrong residue direction.
        rm=-f.a/(f.k*f.jac('sn',f.v));R=(rm,mp.j*rm)
        A=f.q(f.r-3*f.v);B=f.q(f.r+3*f.v)
        pred_res=(det(A,R)+det((-R[0],-R[1]),B))/2
        local=[]
        mutant_target=2*mp.j*rm*rm
        for exp in [12,24,36]:
            eps=mp.power(10,-exp)*(mp.mpf('.6')+mp.mpf('.8')*mp.j)
            qm=f.q(f.r-f.v+eps);qq=f.q(f.r+f.v+eps)
            actual_res=eps*f.T(f.r-f.v+eps)
            wrong_endpoint=(qq[0],-qq[1])
            local.append({'epsilon_power':exp,
                          'Q_minus_residue_error':numstr(max(relerr(eps*qm[j],R[j],f.a) for j in [0,1])),
                          'Q_plus_residue_error':numstr(max(relerr(eps*qq[j],-R[j],f.a) for j in [0,1])),
                          'T_residue_error':numstr(relerr(actual_res,pred_res,f.a*f.a)),
                          'epsilon_squared_T':numstr(abs(eps*eps*f.T(f.r-f.v+eps))/(f.a*f.a)),
                          'adjacent_determinant_scaled':numstr(abs(det(qm,qq))/(f.a*f.a)),
                          'mutant_double_pole_error':numstr(relerr(eps*eps*det(qm,wrong_endpoint),mutant_target,f.a*f.a))})
        assert mp.mpf(local[-1]['T_residue_error'])<mp.mpf('1e-26'),(ks,n,tau,local[-1])
        assert mp.mpf(local[-1]['mutant_double_pole_error'])<mp.mpf('1e-25')
        if not n%2:
            assert product_spread>mp.mpf('1e-12'),(ks,n,tau,numstr(product_spread))
        rows.append({'k':ks,'N':n,'tau':tau,'v_over_K':numstr(f.v/f.K),
                     'character_and_geometry_errors':{k:numstr(v) for k,v in char.items()},
                     'normalized_product_samples':[numstr(x) for x in gp],
                     'normalized_product_spread':numstr(product_spread),
                     'wrong_cn_period_residual':numstr(wrong_cn_period),
                     'wrong_dn_real_shift_sign_residual':numstr(wrong_dn_sign),
                     'predicted_T_residue_normalized':numstr(pred_res/(f.a*f.a)),
                     'complex_pole_controls':local})
        print('completed',ks,n,tau,flush=True)
    return {'decimal_precision':mp.mp.dps,'interval_certification':False,'families':rows,
            'all_numeric_assertions_pass':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=HERE/'results.json')
    parser.add_argument('--max-n',type=int,default=151)
    args=parser.parse_args()
    source_manifest=json.loads((SOURCE/'source_manifest.json').read_text())
    hashes={}
    for rec in source_manifest['sources']:
        actual=digest(PDFS/rec['file'])
        assert actual==rec['sha256']
        hashes[rec['file']]=actual
    intake=json.loads((HERE.parent/'INTAKE.json').read_text())
    native_hashes={}
    for rec in intake['original_source_files']:
        if Path(rec['native_path']).name in ['PROOF.md','SOURCES.md','source_manifest.json']:
            path=HERE.parent/'submitted'/rec['native_path']
            actual=digest(path);assert actual==rec['sha256']
            native_hashes[str(path.relative_to(HERE.parent))]=actual
    result={'utc_start':datetime.now(timezone.utc).isoformat(),'head':intake['head'],
            'runtime':sys.executable,'python':sys.version,'sympy':sp.__version__,'mpmath':mp.__version__,
            'source_pdf_hashes':hashes,'immutable_input_hashes':native_hashes,
            'exact_symbolic':exact_controls(),'lattice_enumeration':collision_controls(args.max_n),
            'high_precision':numeric_controls()}
    result['utc_end']=datetime.now(timezone.utc).isoformat()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',args.output,flush=True)


if __name__=='__main__':
    main()
