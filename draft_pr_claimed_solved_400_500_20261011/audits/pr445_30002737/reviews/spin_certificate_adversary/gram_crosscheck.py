#!/usr/bin/env python3
"""Independent all-frequency Gram recurrence and exact producer comparison."""
import datetime,hashlib,importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
HERE=pathlib.Path(__file__).resolve().parent
CASE=HERE.parent.parent
SAVED=CASE/'private_sources/spin_certificate_adversary/sealed_validator/certify_integral.py'
EXPECTED='027dc38ea76f1a4e69d8976a4845caefc4429e48b551afa7c327dc243b3dac20'
Z=(0,0); ONE=(1,0); I=(0,1)

def need(x,s):
    if not x: raise RuntimeError(s)
def add(a,b): return a[0]+b[0],a[1]+b[1]
def mul(a,b): return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def conjugate(a): return a[0],-a[1]

def gram_coeffs(n):
    # G_n(x)=A_n(x) A_n(x)^*, A_n(x)=D(z) W A_(n-1)(2x).
    W=[[ONE,I],[ONE,(-1,0)]]
    G=[[{0:ONE},{}],[{},{0:ONE}]]
    for _ in range(n):
        H=[[{},{}],[{},{}]]
        for r in range(2):
            for c in range(2):
                for u in range(2):
                    for v in range(2):
                        m=mul(W[r][u],conjugate(W[c][v]))
                        for k,a in G[u][v].items():
                            kk=2*k+r-c
                            H[r][c][kk]=add(H[r][c].get(kk,Z),mul(m,a))
                H[r][c]={k:v for k,v in H[r][c].items() if v!=Z}
        G=H
    S={k:add(G[0][0].get(k,Z),G[1][1].get(k,Z)) for k in set(G[0][0])|set(G[1][1])}
    return {k:S.get(k,Z) for k in range(1-2**n,2**n)}

def load_producer():
    need(hashlib.sha256(SAVED.read_bytes()).hexdigest()==EXPECTED,'sealed code hash mismatch')
    spec=importlib.util.spec_from_file_location('sealed_certificate',SAVED)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def main():
    producer=load_producer()
    spec=importlib.util.spec_from_file_location('independent_reference',HERE/'independent_reference.py')
    reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
    checks=[]
    for n in range(1,7):
        c=gram_coeffs(n)
        d=reference.norm_coefficients(reference.direct_product(n))
        p=producer.matrix_polynomial(n)
        direct=reference.direct_product(n)
        need(all(list(zip(*p[2*r+c]))==direct[r][c] for r in range(2) for c in range(2)),'full polynomial source-order mismatch')
        need(c==d,'Gram vs generic direct matrix autocorrelation mismatch')
        nt,_=producer.exact_fourier_coefficients(p,n)
        need(nt==c,'Gram vs NTT mismatch')
        checks.append({'N':n,'full_polynomial_entries_match_generic_source_forward':True,'all_gram_coefficients_match_generic_quadratic_autocorrelation_and_NTT':True})
    c=gram_coeffs(13)
    nt,sanity=producer.exact_fourier_coefficients(producer.matrix_polynomial(13),13)
    need(c==nt,'N13 all-frequency independent Gram/NTT disagreement')
    digest=hashlib.sha256(json.dumps(sorted(c.items()),separators=(',',':')).encode()).hexdigest()
    need(digest==sanity['coefficient_sha256'],'coefficient digest mismatch')
    need(all(i==0 for r,i in c.values()),'imaginary coefficient found')
    need(all(c[-k]==conjugate(v) for k,v in c.items()),'negative frequency mismatch')
    print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sealed_code_sha256':EXPECTED,'checks':checks,'N13':{'all_frequency_coefficients_matched':len(c),'nonzero_coefficients':sum(v!=Z for v in c.values()),'all_coefficients_real':True,'negative_frequencies_correct':True,'coefficient_sha256':digest,'independent_coefficient_l1':sum(abs(r)+abs(i) for r,i in c.values())},'mechanism':'G_n=D(z) W G_(n-1)(2x) W* D(z)*, exact Gaussian Laurent polynomial dictionaries; no modular convolution'},indent=2))
if __name__=='__main__': main()
