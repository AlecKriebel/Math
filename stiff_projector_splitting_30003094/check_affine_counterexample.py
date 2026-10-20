"""Independent exact-subflow evaluations; numerical evidence, not proof."""
import json
import mpmath as mp
mp.mp.dps = 100

def eval_step(lam,h,eta,dps=100):
    mp.mp.dps=dps
    l,h,e=map(mp.mpf,(lam,h,eta)); rt=mp.sqrt(2); E=mp.exp(-l*h/2)
    k=mp.matrix([(E+2*e*(1-E)/l)/rt,(E**3+2*e*(1-E**3)/(3*l))/rt])
    kh=mp.norm(k); u=k/kh; a=-l*u[1]**2; b=-l/2; q=a+b; d=e*(u[0]+u[1])/rt
    # Cancellation-free algebraic form of the three exact subflows.
    z=(u[0]*(-l/2+e)+u[1]*(-3*l/2+e)*E**2)/(2*q)
    Lv=mp.matrix([z,E**2*z])
    for j,r in enumerate([a,a-l]):
        Lv[j] += -d/q*mp.exp(r*h)/rt + e*u[j]*mp.expm1(r*h)/r
    Y=u*Lv.T
    X=mp.matrix([[mp.mpf('.5')+e*h,mp.mpf('.5')*mp.exp(-l*h)],
                 [mp.mpf('.5')*mp.exp(-l*h),mp.mpf('.5')*mp.exp(-2*l*h)+e*(-mp.expm1(-2*l*h))/(2*l)]])
    # Literal K, S, L formula, using enough precision to withstand cancellation.
    St=mp.exp(-q*h)*kh-d*mp.expm1(-q*h)/(-q)
    Ldirect=mp.matrix([mp.exp((a-l*j)*h)/rt*St+e*u[j]*mp.expm1((a-l*j)*h)/(a-l*j) for j in range(2)])
    Ydirect=u*Ldirect.T
    return {"lambda":str(l),"tau":str(h),"eta":str(e),"precision_digits":dps,
            "Y":[[float(Y[i,j]) for j in range(2)] for i in range(2)],
            "error":float(mp.norm(Y-X)),"literal_vs_stable":float(mp.norm(Y-Ydirect)),
            "normal_defect_bound":float(e),"k_norm":float(kh)}

if __name__=='__main__':
    cases=[]
    for l in [10,100,1000,10000]:
        cases.append(eval_step(l,'.1','.01',max(100,int(l*.1)+60)))
    for n in [10,30,100,300,1000]:
        # All tau, eta, and 1/lambda tend to zero. lambda*tau=n.
        cases.append(eval_step(n*n,mp.mpf(1)/n,mp.mpf(1)/n,max(100,n+60)))
    out={"description":"Rank-1 full-F KSL with exact affine subflows; A=B=diag(0,-lambda), C=eta I, Y0=vv^T.","limit_Y":[[.375,0],[.125,0]],"limit_error_at_eta_tau_zero":float(1/(4*mp.sqrt(2))),"cases":cases}
    print(json.dumps(out,indent=2))
