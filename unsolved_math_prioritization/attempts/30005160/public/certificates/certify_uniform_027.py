"""Exact interval certificate of D_p<0 for 4<p<6 on {0,2,7}.
Only integer arithmetic affects the verdict; displayed floats are diagnostics.
"""
import argparse,json,time
from pathlib import Path

def ceildiv(a,b):return -((-a)//b)

def moments(N,A=8,B=11,C=10,K=7,bits=160):
    M=(A+B+C)**2; scale=1<<bits
    out=[]
    for sign in [1,-1]:
        ker={0:M-A*A-B*B-C*C,2:-sign*A*B,K:-A*C,K-2:-sign*B*C}
        for e,c in list(ker.items()):
            if e:ker[-e]=c
        # Indexed dense integer Laurent coefficients: index i represents i-K*j.
        v=[1]; seq=[(scale,scale)]; den=1
        for j in range(1,N+2):
            w=[0]*(len(v)+2*K)
            for e,c in ker.items():
                shift=e+K
                for i,x in enumerate(v):w[i+shift]+=c*x
            v=w;den*=M
            num=v[K*j]*scale
            seq.append((num//den,ceildiv(num,den)))
        out.append(seq)
    return out,M

def verify(N=256,bins=256,bits=160):
    S=1<<bits;t=time.time();(u,v),M=moments(N,bits=bits)
    # Primitive mass 7 implies these exact moments agree; rounded intervals
    # themselves retain sufficient precision for the certificate below.
    worst=None;wbin=None; bounds=[]
    for k in range(bins):
        # q lies in [l/bins,r/bins], covering the CLOSED interval [2,3].
        l=2*bins+k;r=l+1
        wl=wu=S//24 # floor for lower; upper is separately rounded upward.
        lo=S//24; hi=ceildiv(S,24)
        partial_lo=0;partial_hi=0
        for j in range(4,N+1):
            if j>4:
                # Lower weight at right endpoint; upper at left endpoint.
                lo=(lo*((j-1)*bins-r))//(j*bins)
                hi=ceildiv(hi*((j-1)*bins-l),j*bins)
            dl=u[j][0]-v[j][1];du=u[j][1]-v[j][0]
            prods=[lo*dl,lo*du,hi*dl,hi*du]
            partial_lo+=min(prods)//S
            partial_hi+=ceildiv(max(prods),S)
        # Sum_{j>N} w_j(q) = (N+1)w_{N+1}(q)/q.
        hi_next=ceildiv(hi*(N*bins-l),(N+1)*bins)
        tail_weight=ceildiv(hi_next*(N+1)*bins,l)
        tail_moment=u[N+1][1]+v[N+1][1]
        tail=ceildiv(tail_weight*tail_moment,S)
        lower=partial_lo-tail
        bounds.append(lower)
        if worst is None or lower<worst:worst=lower;wbin=k
    result={'status':'PASS' if worst>0 else 'FAIL','exponent_interval':'4 < p < 6','frequencies':[0,2,7],'majorant_coefficients':[8,11,10],'signed_coefficients':[8,-11,10],'normalization_M':M,'N':N,'q_bins':bins,'precision_bits':bits,'worst_bin_index':wbin,'minimum_normalized_lower_numerator':worst,'lower_denominator':str(S),'minimum_normalized_lower_display':worst/S,'elapsed_seconds':time.time()-t,'rounding':'Integer floor/ceiling outward rounding; all acceptance tests exact.'}
    if worst<=0:raise ArithmeticError(json.dumps(result))
    return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--N',type=int,default=256);p.add_argument('--bins',type=int,default=256);a=p.parse_args()
 ans=verify(a.N,a.bins)
 Path(__file__).with_suffix('.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
