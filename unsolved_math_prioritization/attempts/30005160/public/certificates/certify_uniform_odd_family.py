"""Uniform (4,6) real-majorant counterexamples, via integer interval arithmetic.
Separate from the frozen exact-moment 027 certificate.
"""
import argparse,json,time
from pathlib import Path

def ceildiv(a,b):return -((-a)//b)

def moments(N,A,B,C,K,bits=160):
    M=(A+B+C)**2; workbits=bits+N+4; scale=1<<workbits; rescale=1<<(workbits-bits)
    out=[]
    for sign in [1,-1]:
        ker={0:M-A*A-B*B-C*C,2:-sign*A*B,K:-A*C,K-2:-sign*B*C}
        for e,c in list(ker.items()):
            if e:ker[-e]=c
        # L1(kernel) <=2M implies the error per coefficient after j rounded
        # normalized convolutions is <=(2^j-1)/2^workbits.
        if sum(map(abs,ker.values()))>2*M:raise ArithmeticError('L1 bound')
        v=[scale];seq=[(1<<bits,1<<bits)]
        for j in range(1,N+2):
            w=[0]*(len(v)+2*K)
            for e,c in ker.items():
                shift=e+K
                for i,x in enumerate(v):w[i+shift]+=c*x
            v=[x//M for x in w];err=(1<<j)-1
            mid=v[K*j]
            seq.append(((mid-err)//rescale,ceildiv(mid+err,rescale)))
        out.append(seq)
    return out,M

def verify(K,N,bins,bits=160):
    A=10*(K-2);B=10*K;C=63
    S=1<<bits;t=time.time();(u,v),M=moments(N,A,B,C,K,bits=bits)
    worst=None;wbin=None
    for k in range(bins):
        l=2*bins+k;r=l+1;lo=S//24;hi=ceildiv(S,24);partial_lo=0
        for j in range(4,N+1):
            if j>4:
                lo=(lo*((j-1)*bins-r))//(j*bins)
                hi=ceildiv(hi*((j-1)*bins-l),j*bins)
            dl=u[j][0]-v[j][1];du=u[j][1]-v[j][0]
            partial_lo+=min(lo*dl,lo*du,hi*dl,hi*du)//S
        hi_next=ceildiv(hi*(N*bins-l),(N+1)*bins)
        tail_weight=ceildiv(hi_next*(N+1)*bins,l)
        tail=ceildiv(tail_weight*(u[N+1][1]+v[N+1][1]),S)
        lower=partial_lo-tail
        if worst is None or lower<worst:worst=lower;wbin=k
    return {'status':'PASS' if worst>0 else 'FAIL','exponent_interval':'4 < p < 6','frequencies':[0,2,K],'majorant_coefficients':[A,B,C],'signed_coefficients':[A,-B,C],'normalization_M':M,'N':N,'q_bins':bins,'precision_bits':bits,'moment_work_bits':bits+N+4,'worst_bin_index':wbin,'minimum_normalized_lower_numerator':str(worst),'lower_denominator':str(S),'minimum_normalized_lower_display':worst/S,'elapsed_seconds':time.time()-t,'rounding':'Every arithmetic bound uses integer floor/ceiling; convolution errors explicitly bounded by (2^j-1)/2^workbits.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--K',type=int,required=True);p.add_argument('--N',type=int,default=512);p.add_argument('--bins',type=int,default=1024);a=p.parse_args()
 if a.K<7 or a.K%2==0:raise ValueError('Require odd K>=7')
 ans=verify(a.K,a.N,a.bins)
 path=Path(__file__).with_name('uniform_02'+str(a.K)+'.json');path.write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
 if ans['status']!='PASS':raise ArithmeticError('Certificate failed')
