from fractions import Fraction as F
import json
rows=[]
for m in [1,2,3,17,101]:
    direct=F(1,4)*sum(F(1,m**4) for j in range(m) for k in range(m))
    grouped=F(m+2*sum(m-r for r in range(1,m)),4*m**4)
    expected=F(1,4*m*m)
    if direct!=grouped or direct!=expected: raise RuntimeError('H=1 variance inconsistency')
    rows.append({'m':m,'T1_direct':str(direct),'T1_grouped':str(grouped),'expected':str(expected)})
print(json.dumps({'status':'CORRECTED_EXACT_CONTROL_PASS','general_formula':'T^4/(4m^2)','rows':rows,'supersedes':'FIRST_CONTROLS_SEAL-era statement H=1 Q variance=T^4/4; review-only error; reader correct'},indent=2))
