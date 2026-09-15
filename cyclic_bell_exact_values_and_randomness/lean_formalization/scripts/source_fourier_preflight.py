#!/usr/bin/env python3
"""Exact source-Z coefficient/DFT/qutrit checks. NOT Lean theorem evidence.
Uses retained cyclotomic Fraction arithmetic, not floating-point sines.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json
import general_exact_preflight as E


def run(ds):
    C=E.Checks()
    for d in ds:
        if d<1:raise ValueError('positive dimension required')
        N=4*d;one=E.elt(N,[1]);z=one*0;ii=E.root(N,d);omega=E.root(N,4)
        sine=lambda k:(E.root(N,2*k+1)-E.root(N,-2*k-1))/(2*ii)
        base=[((-1)**k)*omega**(k*(k+1)//2)/(d*sine(k)) for k in range(d)]
        coeff=[[base[k]*omega**(-y*(k+1)) for k in range(d)] for y in range(d)]
        for k in range(d):
            C.equal(f'd{d}: integer triangular exponent {k}',2*(k*(k+1)//2),k*(k+1))
            C.equal(f'd{d}: triangular exponential bridge {k}',omega**(k*(k+1)//2),E.root(N,2*k*(k+1)))
            for m in range(d):
                got=sum((omega**(m*y)*coeff[y][k] for y in range(d)),z)
                C.equal(f'd{d}: source coefficient DFT {m}/{k}',got,d*base[k] if k==(m-1)%d else z)
        C.equal(f'd{d}: last coefficient sign',base[-1],base[0])
        X=E.shift([one]*d);Z=[[omega**i if i==j else z for j in range(d)] for i in range(d)]
        Id=E.ident(d,N);zero=E.ms(z,Id)
        mode=[E.mm(E.mpow(X,k+1),E.mpow(Z,k)) for k in range(d)]
        B=[]
        for y in range(d):
            T=zero
            for k in range(d):T=E.ma(T,E.ms(coeff[y][k],mode[k]))
            B.append(T)
            C.equal(f'd{d}: source Bob unitary {y}',E.mm(E.adj(T),T),Id)
            C.equal(f'd{d}: source Bob order {y}',E.mpow(T,d),Id)
        for m in range(d):
            got=zero
            for y in range(d):got=E.ma(got,E.ms(omega**(m*y),B[y]))
            C.equal(f'd{d}: source operator DFT {m}',got,E.ms(d*base[(m-1)%d],mode[(m-1)%d]))
        sum0=zero;sum1=zero
        for y in range(d):
            sum0=E.ma(sum0,B[y]);sum1=E.ma(sum1,E.ms(omega**y,B[y]))
        C.equal(f'd{d}: source Fourier sum zero',sum0,E.ms(1/sine(0),E.adj(Z)))
        C.equal(f'd{d}: source Fourier sum one',sum1,E.ms(1/sine(0),X))
        C.equal(f'd{d}: reduced source physical expectation',sum((E.phi_expect(E.ma(Z,E.ms(omega**y,X)),B[y]) for y in range(d)),z),2/sine(0))
        if d>1:
            wrong=zero
            for y in range(d):wrong=E.ma(wrong,E.ms(omega**(-y),B[y]))
            if wrong!=sum1:C.negative(f'd{d}: Fourier sign mutation',wrong,sum1)
            C.negative(f'd{d}: wrong extra dimension normalization',E.ms(F(1,d),sum0),sum0)
        if d==3:
            for y in range(d):
                explicit=E.ms(F(1,3),E.ma(E.ma(E.ms(2,E.mpow(Z,2)),E.ms(2*omega**(2*y),X)),
                                              E.ms(-omega**(y+1),E.mm(E.mpow(X,2),Z))))
                C.equal(f'd3: literal qutrit formula {y}',B[y],explicit)
                wrong=E.ms(F(1,3),E.ma(E.ma(E.ms(2,E.mpow(Z,2)),E.ms(2*omega**(2*y),X)),
                                              E.ms(omega**(y+1),E.mm(E.mpow(X,2),Z))))
                C.negative(f'd3: missing minus qutrit term {y}',wrong,B[y])
    return {'status':'exact_source_coefficient_tests_passed_NOT_LEAN','kernel_checked':False,
            'dimensions':ds,'checks':len(C.rows),'negative_controls':len(C.controls),
            'check_labels':C.rows,'negative_control_labels':C.controls,
            'scope':'Finite exact coefficients, DFTs, source matrices and qutrit expression. Does not prove the general polar identification or any Lean source.'}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--dimensions',nargs='+',type=int,default=list(range(1,9)))
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();t=datetime.now(timezone.utc)
    result=run(args.dimensions);result['started_utc']=t.isoformat();result['finished_utc']=datetime.now(timezone.utc).isoformat()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['shared_arithmetic_sha256']=hashlib.sha256(Path(__file__).with_name('general_exact_preflight.py').read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['check_labels','negative_control_labels']},indent=2))
