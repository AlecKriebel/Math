#!/usr/bin/env python3
"""Independent rational series bounds for constants, sinc and selected logarithms."""
from fractions import Fraction as Q
import datetime,json,sys
sys.dont_write_bytecode=True
from gram_crosscheck import load_producer,need,EXPECTED

def atan(q,K=60):
    s=sum(((-1)**j*Q(1,(2*j+1)*q**(2*j+1)) for j in range(K)),Q(0))
    t=Q(1,(2*K+1)*q**(2*K+1))
    return (s,s+t) if K%2==0 else (s-t,s)
def log_u(u,K=100):
    s=2*sum((u**(2*j+1)/(2*j+1) for j in range(K)),Q(0))
    tail=2*u**(2*K+1)/((2*K+1)*(1-u*u))
    return s,s+tail

def sinc(t,K=40):
    term=Q(1);s=term
    for j in range(1,K+1):
        term=term*t*t/((2*j)*(2*j+1));s+=(-1)**j*term
    nxt=term*t*t/((2*K+2)*(2*K+3))
    return (s-nxt,s) if K%2==0 else (s,s+nxt)

def main():
    p=load_producer();f=p.Fixed(100);R=f.R
    a,b=atan(5),atan(239); pi=(16*a[0]-4*b[1],16*a[1]-4*b[0])
    plo,phi=f.pi();need(Q(plo,R)<=pi[0] and Q(phi,R)>=pi[1],'pi enclosure does not contain independent rational bounds')
    scale=10**50
    pil=Q((pi[0]*scale).numerator//(pi[0]*scale).denominator,scale)
    z=pi[1]*scale;piu=Q(-(-z.numerator//z.denominator),scale)
    l2=log_u(Q(1,3));lo,hi=f.log2_bounds()
    need(Q(lo,R)<=l2[0] and Q(hi,R)>=l2[1],'log2 enclosure does not contain independent rational bounds')
    sinc_checks=[]
    for k in [0,1,2,4095,8190,8191]:
        sl,su=f.sinc(k,65536,(plo,phi))
        if k==0:need(sl==su==R,'sinc zero failure')
        else:
            # sinc is strictly decreasing on (0,π): integral cos(ts) over 0<=s<=1.
            low=sinc(piu*k/65536)[0];up=sinc(pil*k/65536)[1]
            need(Q(sl,R)<=low and Q(su,R)>=up,'sinc enclosure does not contain independent rational bounds')
        sinc_checks.append(k)
    values=[R,R+1,3*R//2,2*R-1,2*R,180*R,190*R+1,16384*R,2**40*R-1]
    for value in values:
        e=value.bit_length()-R.bit_length(); scale=R*2**e
        t=Q(value,scale); u=(t-1)/(t+1)
        ln=log_u(u)[1]+e*l2[1]
        need(Q(f.log_upper(value,hi),R)>=ln,'log upper misses independent rational upper')
    print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sealed_code_sha256':EXPECTED,'independent_method':'Exact Fraction alternating atan/Machin, alternating sinc and positive atanh log series with exact tail; no fixed-point helper reused','pi_enclosure_contains_independent_rational_bounds':True,'log2_enclosure_contains_independent_rational_bounds':True,'sinc_k_values_checked':sinc_checks,'rational_log_inputs_checked':len(values),'boundary_inputs':'1, 1+ulp, 2−ulp, 2, positive determinant-scale values, large exact power boundary','scope':'These finite cross-checks supplement the general interval derivation; they do not replace it'},indent=2))
if __name__=='__main__':main()
