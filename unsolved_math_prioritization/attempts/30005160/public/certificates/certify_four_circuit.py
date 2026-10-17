"""Exact integer/rational certificate for Gamma={(0,0),(2,0),(0,1),(5,1)}.
P_plus=4+4z^2+w(5+2z^5), P_minus=4-4z^2+w(5+2z^5).
All acceptance checks use integers. Decimal approximations are display only.
"""
from math import comb
from fractions import Fraction as Q
from pathlib import Path
import argparse, json, time, hashlib

def moments(n,m=5):
    # T[h][r]=CT z^-r (29+10(z+z^-1))^h, r>=0.
    T=[[1]]
    for h in range(1,n+1):
        t=T[-1]
        T.append([29*(t[r] if r<len(t) else 0)+10*(t[abs(r-1)] if abs(r-1)<len(t) else 0)+10*(t[r+1] if r+1<len(t) else 0) for r in range(h+1)])
    plus=[]; minus=[]
    for k in range(n+1):
        pp=mm=0
        for j in range(k+1):
            h=k-j;factor=comb(k,j)**2*16**j
            zero=comb(2*j,j)*T[h][0]
            pos=neg=zero
            for ell in range(1,min(j//m,h//2)+1):
                v=2*comb(2*j,j+m*ell)*T[h][2*ell]
                pos+=v;neg+=(-1)**ell*v
            pp+=factor*pos;mm+=factor*neg
        plus.append(pp);minus.append(mm)
    return plus,minus

def complementary(raw,L2=225):
    out=[]
    for j in range(len(raw)):
        v=sum((-1)**k*comb(j,k)*L2**(j-k)*raw[k] for k in range(j+1))
        assert 0<=v<=L2**j
        if j:assert v<=L2*out[-1]
        out.append(v)
    return out

def exact_fixed(plus,minus,N):
    q=Q(5,2);c=Q(1);s=Q(0)
    for j in range(1,N+1):
        c*=-(q-j+1)/j
        s+=15**5*c*Q(plus[j]-minus[j],225**j)
    b=Q(1)
    for j in range(1,N+1):b*=(q-j)/j
    tail=15**5*abs(b)*Q(plus[N+1]+minus[N+1],225**(N+1))
    assert s+tail<Q(-1,4)
    return {'partial':str(s),'tail':str(tail),'upper_bound':str(s+tail),'upper_bound_float':float(s+tail)}

def uniform(plus,minus,N,bins=256,digits=70):
    scale=10**digits;lower=[];finite=[];tails=[]
    def ceildiv(a,b):return -((-a)//b)
    powers=[225**j for j in range(N+2)]
    for cell in range(bins):
        left=2*bins+cell;right=left+1
        wl=wr=1;den=24;finite_lower=0
        for j in range(4,N+1):
            if j>4:
                wl*=((j-1)*bins-left);wr*=((j-1)*bins-right);den*=j*bins
            delta=plus[j]-minus[j]
            weight=wr if delta>=0 else wl
            finite_lower+=(scale*weight*delta)//(den*powers[j])
        # Sum j>N w_j(q)=(N+1)w_(N+1)(q)/q, bounded at left.
        tail=ceildiv(scale*wl*(N*bins-left)*(plus[N+1]+minus[N+1]),den*left*powers[N+1])
        lower.append(finite_lower-tail);finite.append(finite_lower);tails.append(tail)
    assert min(lower)>0, (min(lower)/scale,lower.index(min(lower)), min(finite)/scale,max(tails)/scale)
    assert min(lower)*40000000>scale
    return {'N':N,'bins':bins,'decimal_grid':digits,'minimum_lower_numerator':str(min(lower)),'scale':str(scale),'minimum_lower_float':min(lower)/scale,'worst_cell':lower.index(min(lower)),'all_lower_numerators':[str(x) for x in lower], 'largest_tail_float':max(tails)/scale}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=128);parser.add_argument('--bins',type=int,default=256);a=parser.parse_args()
    start=time.monotonic();rawp,rawm=moments(a.n+1)
    assert rawp[:7]==rawm[:7]
    expected=4*comb(7,5)**2*4**10*5**2*2**2
    assert rawp[7]-rawm[7]==expected,(rawp[7]-rawm[7],expected)
    p=complementary(rawp);m=complementary(rawm)
    result={'configuration':[[0,0],[2,0],[0,1],[5,1]],'positive_amplitudes':[4,4,5,2], 'negative_amplitudes':[4,-4,5,2], 'N':a.n,'raw_first_difference':str(expected),'fixed_p5':exact_fixed(p,m,a.n)}
    print('Fixed p=5:',result['fixed_p5']['upper_bound_float'],flush=True)
    result['uniform_4_lt_p_lt_6']=uniform(p,m,a.n,a.bins)
    result['elapsed_seconds']=time.monotonic()-start
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print('Uniform certified:',result['uniform_4_lt_p_lt_6']['minimum_lower_float'],'in',result['elapsed_seconds'],'seconds',flush=True)
if __name__=='__main__':main()
