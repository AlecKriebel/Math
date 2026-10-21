"""Independent rational conjugacy and invalid-inference controls; no PDE computation."""
from fractions import Fraction as Q
import json
def need(c,m):
    if not c:raise RuntimeError(m)
def dual(T,k0,gap,L,M,k):
    beta=k0-gap
    def value(t):
        x=t-T
        return k+(k0*x+L*x*x/2 if x<=0 else beta*x+M*x*x/2)-k*t
    candidates={Q(0),T,Q(1),max(Q(0),min(T,T+(k-k0)/L))}
    if M<0:candidates.add(max(T,min(Q(1),T+(k-beta)/M)))
    v={t:value(t) for t in candidates};best=max(v.values())
    return best,{t for t in v if v[t]==best}
def main():
    cases=0;checks=0
    for T in map(Q,['1/7','2/5','9/10']):
      for k0 in map(Q,['-1/17','-2','-31/2']):
       for gap in map(Q,['1/29','3/2','11']):
        for L in map(Q,['-1/97','-7/3','-100','-2']):
         for M in map(Q,['0','-1/19','-8']):
          for divisor in [3,8,31]:
            h=min(gap,T*(-L),-k0)/divisor
            for sign in [-1,0,1]:
                k=k0+sign*h
                best,optimizers=dual(T,k0,gap,L,M,k)
                extra=-h*h/(2*L) if sign>0 else Q(0)
                tstar=T+h/L if sign>0 else T
                need(best==(1-T)*k+extra,'quadratic residual');checks+=1
                need(optimizers=={tstar},'unique global optimum');checks+=1
            cases+=1
    # Without a slope gap, the same smooth quadratic on both sides has the
    # same nonzero quadratic conjugate coefficient on both sides: no defect.
    T=Q(2,5);k0=Q(-2);L=Q(-7,3);h=Q(1,100)
    residual=[]
    for k in [k0-h,k0+h]:
        val,opt=dual(T,k0,Q(0),L,L,k)
        need(val-(1-T)*k==-(k-k0)**2/(2*L),'no-gap smooth control')
        residual.append(str((val-(1-T)*k)/(k-k0)**2))
    # Infinite left curvature can leave a second Taylor coefficient zero.
    # a(T+x)=k0*x-(-x)^(3/2) for x<0 gives gain 4*h^3/27 for h>0.
    for h in [Q(1,10),Q(1,100),Q(1,1000)]:
        y=(2*h/3)**2
        gain=h*y-y*(2*h/3)
        need(gain==4*h**3/27,'infinite-curvature exact gain')
        need(gain/h**2==4*h/27,'vanishing quadratic coefficient')
    print(json.dumps({'verdict':'PASS_INDEPENDENT_SCALAR_CONTROLS',
          'parameter_h_cases':cases,'exact_residual_and_optimizer_checks':checks,
          'no_gap_two_sided_quadratic_coefficients':residual,
          'infinite_curvature_gain':'4*h^3/27; gain/h^2 -> 0',
          'scope':'Exact scalar normal forms and invalid-inference controls only; no geometric or PDE computation.'},indent=2))
if __name__=='__main__':main()
