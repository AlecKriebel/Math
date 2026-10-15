import fractions, json, pathlib, math, random, datetime
F=fractions.Fraction
counts={"rational_local_cases":0,"focal_line_systems":0,"origin_opposite_pairs":0,"circle_rotation_actions":0}
def intersect(A,B,h):
    ax,ay=A; bx,by=B; dx=ax-h; ex=bx-h
    ra=dx*dx+ay*ay; rb=ex*ex+by*by
    det=dx*by-ay*ex
    if not det: raise RuntimeError("singular")
    qx=(ra*by-ay*rb)/det; qy=(dx*rb-ra*ex)/det
    if (qx-dx)*dx+(qy-ay)*ay or (qx-ex)*ex+(qy-by)*by: raise RuntimeError("line equation")
    return qx+h,qy
for t in range(2,9):
    a=F(t*t+1); b=F(t*t-1); c=F(2*t)
    for z in [F(-7,3),F(-2),F(-1),F(-1,3),F(0),F(2,5),F(1),F(7,4)]:
      C=(1-z*z)/(1+z*z); S=2*z/(1+z*z); D2=C*C/(a*a)+S*S/(b*b)
      for w in [F(1,100),F(1,15),F(1,5),F(1,3)]:
        U=(1-w*w)/(1+w*w); V=2*w/(1+w*w); lam=V*V/D2
        if not 0<lam<b*b: continue
        A=(a*(C*U+S*V),b*(S*U-C*V)); B=(a*(C*U-S*V),b*(S*U+C*V)); nA=tuple(-x for x in A); nB=tuple(-x for x in B)
        if A[0]*B[1]-A[1]*B[0]<=0: raise RuntimeError("direction")
        K=a*a*b*b-lam*c*c
        for h in [c,-c]:
          Q=intersect(A,B,h); R=intersect(nA,nB,h)
          pair=tuple(Q[i]+R[i] for i in [0,1]); expected=(-2*h+2*h*K*C*C/(a*a*(b*b-lam)),2*h*K*S*C/(a*b*(b*b-lam)))
          if pair!=expected: raise RuntimeError(("pair",t,z,w,h,pair,expected))
          if not (U*U-c*c*C*C/(a*a)==(b*b-lam)*D2>0): raise RuntimeError("denominator")
          counts["focal_line_systems"]+=2
        if tuple(sum(x) for x in zip(intersect(A,B,F(0)),intersect(nA,nB,F(0))))!=(0,0): raise RuntimeError("origin pair")
        counts["origin_opposite_pairs"]+=1
        counts["rational_local_cases"]+=1
for N in range(4,202,2):
  for k in range(1,N):
    if math.gcd(k,N)!=1: continue
    if (k*(N//2))%N != N//2: raise RuntimeError("central action")
    counts["circle_rotation_actions"]+=1
result={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","mechanism":"Independent exact rational line intersection with no imported package verification; Pythagorean axes, rational midpoint and half-angle parameters; rotation parity enumeration","counts":counts,"limitations":["Finite rational cases do not prove all-parameter identity","Parity enumeration supplements the circle-action deduction"]}
pathlib.Path(__file__).with_name("own_rational_attack_result.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result))
