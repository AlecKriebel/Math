#!/usr/bin/env python3
"""Reviewer-authored read-only diagnostics, not author code or a theorem prover."""
from fractions import Fraction as F
from pathlib import Path
import cmath
import hashlib
import json
import math
import sys

ROOT=Path(__file__).resolve().parent


def need(ok,msg):
    if not ok:
        raise ValueError(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load(n):
    return json.loads((ROOT/n).read_text())


def verify_entry(e,prefix=''):
    n=prefix+e['file']
    need(not Path(n).is_absolute() and '..' not in Path(n).parts,'unsafe member')
    f=ROOT/n
    need(f.is_file() and not f.is_symlink(),'missing/linked member')
    b=f.read_bytes()
    need(len(b)==e['bytes'] and sha(b)==e['sha256'],'member identity '+n)


def lgamma(z):
    # Conventional g=7 Lanczos approximation; double-precision diagnostic only.
    z=complex(z)
    if z.real<0.5:
        return cmath.log(math.pi)-cmath.log(cmath.sin(math.pi*z))-lgamma(1-z)
    coeff=[676.5203681218851,-1259.1392167224028,771.32342877765313,
           -176.61502916214059,12.507343278686905,-0.13857109526572012,
           9.9843695780195716e-6,1.5056327351493116e-7]
    zz=z-1
    x=0.99999999999980993+0j
    for k,c in enumerate(coeff,1):
        x+=c/(zz+k)
    t=zz+7.5
    return .5*math.log(2*math.pi)+(zz+.5)*cmath.log(t)-t+cmath.log(x)


def gamma(z):
    return cmath.exp(lgamma(z))


def simpson(fn,a,b,n):
    need(n>0 and n%2==0,'quadrature grid')
    h=(b-a)/n
    total=fn(a)+fn(b)
    for i in range(1,n):
        total+=(4 if i%2 else 2)*fn(a+i*h)
    return total*h/3


def prod(v):
    out=1
    for x in v:
        out*=x
    return out


def pvalue(lam,s,tau):
    return cmath.exp(-3*s*math.log(math.pi)+sum(lgamma((s+eps*1j*tau-x)/2) for x in lam for eps in [-1,1]))


def barnes(lam,s,tau,T,n):
    contour=s.real/4
    def fun(y):
        w=contour+1j*y
        return cmath.exp(lgamma(w+1j*tau/2)+lgamma(w-1j*tau/2)
                         +sum(lgamma((s-x)/2-w) for x in lam)-lgamma(3*s/2-w))
    before=cmath.exp(-3*s*math.log(math.pi)+sum(lgamma(s+x/2) for x in lam))/8
    return before*simpson(fun,-T,T,n)/(2*math.pi)


def reject(action,name):
    try:
        action()
    except ValueError:
        return name
    raise ValueError('accepted negative control '+name)


def main():
    binding=load('PR_BINDING.json')
    need(binding['head']=='a6e7e6f25f9ede706c80d6f7246a065011df501f','head')
    need(binding['base']=='4b27092a448d53b61408355ce44ec38d103a1ce4','base')
    need(binding['state']=='open' and binding['draft'] is True,'PR state')
    pr=load('private/pr.json');files=load('private/files.json')
    need(pr['head']['sha']==binding['head'] and pr['base']['sha']==binding['base'],'raw pins')
    need(sha((pr.get('body')or'').encode())==binding['body_sha256'],'body hash')
    need(len(files)==len(binding['files'])==8,'eight blobs')
    bypath={x['filename']:x['sha'] for x in files}
    for e in binding['files']:
        verify_entry(e)
        b=(ROOT/e['file']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        need(blob==e['git_blob']==bypath[e['path']],'Git blob')
        need(e['path'].startswith('unsolved_math_prioritization/attempts/30001876/') and e['status']=='added','exact paths')
    manifest=load('private/prfiles/MANIFEST.json')
    need(set(manifest['members'])=={Path(e['file']).name for e in binding['files']},'nested membership')
    for e in manifest['entries']:
        verify_entry(e,'private/prfiles/')
    goodreceipts=0
    for e in load('PRIMARY_RECEIPTS.json'):
        if 'file' in e:
            verify_entry(e)
            goodreceipts+=1
    g=load('GWS_CLEARANCE.json')
    need(g['numeric_gid']==1254632077 and g['requested_columns']==43 and g['rows_including_header']==191,'fresh numeric tracker')
    need(sha((ROOT/'private/GWS_FULL43.json').read_bytes())==g['sha256']=='fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1','ledger bytes')
    need(g['unresolved_duplicate_leads']==[],'semantic clearance')
    arxiv=(ROOT/'private/primary/liyoung_landing.html').read_text()
    need('citation_arxiv_id" content="1102.0195' in arxiv and '10.1112/S0010437X11007366' in arxiv,'same-paper primary alias')
    wrong=(ROOT/'private/primary/wrong_arxiv_landing.html').read_text()
    need('Observation of Zone-Folded Acoustic Phonons' in wrong,'rejected false alias')
    cr=load('private/primary/liyoung_crossref.json')['message']
    need(cr['DOI'].lower()=='10.1112/s0010437x11007366' and cr['volume']=='148' and cr['page']=='675-717','journal registry')
    cells=load('ROW_PROPOSAL.json')['cells']
    need(len(cells)==4 and all(isinstance(x,str) for x in cells),'four literal strings')
    need(cells[1]=='' and cells[2]=='https://doi.org/10.1112/S0010437X11007366','blank B and exact existing DOI')
    # Exact row-lattice, wedge and factorization identities: original Jacquet bridge.
    matrices=0
    for i in range(1,17):
        a,b=F(i+1,7),F(2*i+3,11)
        x,y,z=F(i-8,5),F(7-2*i,9),F(3*i-5,13)
        row2=[0,-a,-x];row3=[a*b,a*y,z]
        R=sum(t*t for t in row3)
        wedge=[row2[1]*row3[2]-row2[2]*row3[1],row2[2]*row3[0]-row2[0]*row3[2],row2[0]*row3[1]-row2[1]*row3[0]]
        S=sum(t*t for t in wedge)
        Q=a*a*b*b+b*b*x*x+(z-x*y)**2
        need(R==a*a*b*b+a*a*y*y+z*z and S==a*a*Q,'row/wedge quadratics')
        v=F(i,17)
        need(a*a*b*b+(1-v)*b*b*x*x+v*a*a*y*y+v*(1-v)*x*x*y*y==(a*a+(1-v)*x*x)*(b*b+v*y*y),'Gaussian factorization')
        n1,n2=F(i+2,5),F(i+1,7)
        p,q=3*n1/2,3*n2/2;k=p+q-F(1,2)
        need(n1+2*n2+F(1,2)-k==1+(n2-n1)/2,'a exponent')
        need(2*n1+n2+F(1,2)-k==1+(n1-n2)/2,'b exponent')
        need(F(1,2)-3*n1-3*n2==-2*k-F(1,2),'pi completion')
        need(q-k/2-F(1,4)==(q-p)/2 and p-k/2-F(1,4)==(p-q)/2,'beta exponents')
        A,B,C=1-n1-2*n2,-n1+n2,2*n1+n2-1
        e1,e2=n2-F(1,3),n1-F(1,3)
        lam=[2*e1+e2,-e1+e2,-e1-2*e2]
        need(lam==[-A,-B,-C] and sum(lam)==0,'literal parameter map')
        need(F(8)*F(1,4)*F(1,4)*F(1,2)==F(1,4),'double Mellin constant')
        need(F(1,4)*F(1,4)*2==F(1,8),'Barnes Jacobian')
        matrices+=1
    # Gamma implementation checks independent of the automorphic result.
    need(abs(gamma(1)-1)<1e-13 and abs(gamma(.5)-math.sqrt(math.pi))<1e-13,'gamma known values')
    for z in [.3+.2j,1.7-.4j,2.1+1.3j]:
        need(abs(gamma(z+1)/(z*gamma(z))-1)<1e-12,'gamma recurrence')
    s,tau=1.4+.19j,.31
    lam=[.2j,.7j,-.9j]
    num=[]
    for triple in [lam,[-x for x in lam]]:
        target=pvalue(triple,s,tau)/8
        for T,n in [(10,1600),(14,2800)]:
            answer=barnes(triple,s,tau,T,n)
            error=abs(answer/target-1)
            need(error<1e-9,'Barnes numerical transcription')
            num.append(error)
    signgap=abs(pvalue(lam,s,tau)/pvalue([-x for x in lam],s,tau)-1)
    need(signgap>1e-4,'sign-sensitive test is not degenerate')
    # Ordinary Fourier inversion with frequency2t: test x=.7 and Plancherel.
    x=.7
    gaussian=simpson(lambda t:math.sqrt(math.pi)*math.exp(-t*t)*cmath.exp(-2j*t*x),-8,8,2048)/math.pi
    need(abs(gaussian-math.exp(-x*x))<1e-11,'Mellin inversion factor')
    norm=simpson(lambda t:math.exp(-2*t*t),-8,8,2048)
    need(abs(norm-math.sqrt(math.pi/2))<1e-11,'Mellin norm')
    n1,n2=F(1,3)+.17j,F(1,3)+.29j
    D=cmath.exp((.5-3*n1-3*n2)*math.log(math.pi)+lgamma(1.5*n1)+lgamma(1.5*n2)+lgamma((3*n1+3*n2-1)/2))
    need(abs(D-1)>.01,'generic completion control')
    rho=2+3j;phase=cmath.exp(.4j)
    need(abs((rho*phase).conjugate()/rho.conjugate()-phase.conjugate())<1e-14,'inner-product phase conjugation')
    negative=[
        reject(lambda:need(abs(D-1)<1e-12,'four-equation discrepancy'),'four printed equations all literal'),
        reject(lambda:need(abs(gaussian/2-math.exp(-x*x))<1e-10,'inverse factor2'),'wrong Mellin factor'),
        reject(lambda:need(signgap<1e-10,'wrong sign'),'silently reverse spectral triple'),
        reject(lambda:need(F(1,4)*F(1,4)==F(1,8),'lost dz Jacobian'),'omit z=2w Jacobian'),
        reject(lambda:need(2*2==8,'lost stabilizer'),'omit U2 stabilizer'),
        reject(lambda:need('citation_arxiv_id" content="1012.1356' in arxiv,'wrong alias'),'unrelated arXiv alias'),
        reject(lambda:need(F(4)*F(1,4)*F(1,4)*F(1,2)==F(1,4),'wrong Bessel prefactor'),'Bessel prefactor4'),
        reject(lambda:need(abs((rho*phase)/rho-phase.conjugate())<1e-12,'unconjugated Fourier phase'),'omit Fourier coefficient conjugation'),
    ]
    closure=None
    if (ROOT/'REVIEW_SEAL.json').exists():
        seal=load('REVIEW_SEAL.json');names={e['file'] for e in seal['entries']}
        actual={str(x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file() and str(x.relative_to(ROOT))!='REVIEW_SEAL.json'}
        need(len(names)==len(seal['entries']) and names==actual,'complete actual closure')
        for e in seal['entries']:
            verify_entry(e)
        pm=load('PRIVATE_BODY_SEAL.json')
        need({e['file'] for e in pm['entries']}=={str(x.relative_to(ROOT/'private')) for x in (ROOT/'private').rglob('*') if x.is_file()},'private actual closure')
        for e in pm['entries']:
            verify_entry(e,'private/')
        closure=len(names)
    else:
        need('--require-seal' not in sys.argv,'missing seal')
    print(json.dumps({'status':'PASS','exact_matrix_and_exponent_cases':matrices,'Barnes_complex_relative_errors':num,'opposite_triple_relative_gap':signgap,'gaussian_inverse_error':abs(gaussian-math.exp(-x*x)),'negative_controls':negative,'bound_PR_blobs':8,'primary_receipts':goodreceipts,'recursive_closure_members':closure,'numeric_scope':'double-precision independent diagnostics; no validated interval or automorphic proof certificate'},sort_keys=True))


if __name__=='__main__':
    main()
