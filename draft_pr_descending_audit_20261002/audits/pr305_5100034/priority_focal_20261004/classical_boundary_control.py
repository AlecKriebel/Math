from fractions import Fraction as F
P=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(3,5),F(-4,5))]
def foot(M,U,V):
 d=(V[0]-U[0],V[1]-U[1]);t=((M[0]-U[0])*d[0]+(M[1]-U[1])*d[1])/(d[0]*d[0]+d[1]*d[1])
 return (U[0]+t*d[0],U[1]+t*d[1])
def area(Q):
 return sum(Q[i][0]*Q[(i+1)%len(Q)][1]-Q[i][1]*Q[(i+1)%len(Q)][0] for i in range(len(Q)))/2
def pedal(M):return area([foot(M,P[i],P[(i+1)%len(P)]) for i in range(len(P))])
print("fixed cyclic nonrectangular quadrilateral",P)
for M in [(F(0),F(0)),(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))]:print(M,pedal(M))
a=pedal((F(0),F(0)))
xx=(pedal((F(1),F(0)))+pedal((F(-1),F(0)))-2*a)/2
yy=(pedal((F(0),F(1)))+pedal((F(0),F(-1)))-2*a)/2
print("quadratic coefficients",xx,yy,"linear x",(pedal((F(1),F(0)))-pedal((F(-1),F(0))))/2)
assert xx==yy==0
assert pedal((F(1),F(0)))!=pedal((F(0),F(0)))

xy=pedal((F(1),F(1)))-pedal((F(1),F(0)))-pedal((F(0),F(1)))+a
print("mixed coefficient",xy)
assert xy==0
print("exact area polynomial: 9/10 - 3*x/10")
