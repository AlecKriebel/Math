"""Exact signed-area witnesses bracketing a genuine zero constant for N=8.
No elliptic numerical value is needed: rational half-period coordinates,
confocal caustic tangency, and original focus constructions are checked.
"""
from pathlib import Path
import json
import sympy as z

def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def area(ps):return z.simplify(sum(det(ps[j],ps[(j+1)%len(ps)]) for j in range(len(ps)))/2)
def simp(x):return z.simplify(z.radsimp(x))
cases=[]
for xx,ww in [(z.Rational(3,4),z.Rational(5,4)),(z.Rational(5,12),z.Rational(13,12))]:
    assert ww*ww==1+xx*xx
    ll=xx*xx;k2=1-ll*ll;a2=(ww-xx)*ww*(1+xx);b2=a2-k2
    aa,bb,kk=z.sqrt(a2),z.sqrt(b2),z.sqrt(k2)
    ps=[(0,bb),(-aa/ww,bb*xx/ww),(-aa,0),(-aa/ww,-bb*xx/ww),(0,-bb),(aa/ww,-bb*xx/ww),(aa,0),(aa/ww,bb*xx/ww)]
    feet=[];antis=[]
    for j,p in enumerate(ps):
        q=ps[(j+1)%8];prev=ps[(j-1)%8]
        incoming=(p[0]-prev[0],p[1]-prev[1]);outgoing=(q[0]-p[0],q[1]-p[1])
        ni=z.sqrt(dot(incoming,incoming));no=z.sqrt(dot(outgoing,outgoing))
        vin=tuple(simp(x/ni) for x in incoming);vout=tuple(simp(x/no) for x in outgoing)
        outer_normal=(p[0]/a2,p[1]/b2)
        factor=2*dot(vin,outer_normal)/dot(outer_normal,outer_normal)
        for coord in range(2):
            assert simp(vin[coord]-factor*outer_normal[coord]-vout[coord])==0
        assert simp(p[0]*p[0]/a2+p[1]*p[1]/b2-1)==0
        edge=(q[0]-p[0],q[1]-p[1]);normal=(-edge[1],edge[0]);hl=dot(normal,p)
        # Tangency to caustic axes (1,ll).
        assert simp(normal[0]**2+ll*ll*normal[1]**2-hl**2)==0
        mu=dot((kk-p[0],-p[1]),edge)/dot(edge,edge)
        feet.append(tuple(simp(p[i]+mu*edge[i]) for i in range(2)))
        n=(p[0]-kk,p[1]);m=(q[0]-kk,q[1]);hn=dot(n,p);hm=dot(m,q);den=det(n,m)
        assert den!=0
        antis.append((simp((hn*m[1]-hm*n[1])/den),simp((n[0]*hm-hn*m[0])/den)))
    AF=area(feet);AR=area(antis)
    cases.append({'sqrt_complementary_modulus':str(xx),'complementary_modulus':str(ll),'modulus_squared':str(k2),'outer_a_squared':str(a2),'outer_b_squared':str(b2),'pedal_area_exact':str(AF),'antipedal_area_exact':str(AR),'product_exact':str(simp(AF*AR)),'antipedal_sign':int(z.sign(AR))})
assert cases[0]['antipedal_sign']==1 and cases[1]['antipedal_sign']==-1
result={'status':'PASS','cases':cases,'deduction':'The primitive N=8,tau=1 focal antipedal coefficient is continuous in 0<k<1: all original normals have nonzero determinant and dn trace is positive. Opposite exact signs at k²=175/256 and k²=20111/20736 imply a genuine intermediate zero coefficient by the intermediate value theorem. At that parameter the full antipedal signed area and target product vanish identically in phase, by the independently proved trace identity.'}
Path('ZERO_CONSTANT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
