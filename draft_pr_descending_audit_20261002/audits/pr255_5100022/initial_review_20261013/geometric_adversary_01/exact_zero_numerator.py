"""Exact permitted least-six billiard with zero signed antipedal numerator."""
from pathlib import Path
import sympy as s
import json
a=3*s.sqrt(2)/4;b=3*s.sqrt(2)/8;focus=3*s.sqrt(6)/8
b0sq=s.Rational(5,32)
P=[s.Matrix(x) for x in [(0,b),(-1,b/3),(-1,-b/3),(0,-b),(1,-b/3),(1,b/3)]]
dot=lambda x,y:(x.T*y)[0]
det=lambda x,y:s.det(s.Matrix.hstack(x,y))
area=lambda Z:s.simplify(sum(det(Z[j],Z[(j+1)%6]) for j in range(6))/2)
assert a*a-b*b==focus*focus
assert a*a-1==b*b-b0sq==s.Rational(1,8)
assert len({tuple(p) for p in P})==6
records=[];areas={}
for fi in [1,-1]:
    F=s.Matrix([fi*focus,0]);Q=[];U=[]
    for j,p in enumerate(P):
        pp=P[(j+1)%6];pm=P[(j-1)%6];e=pp-p
        n=s.Matrix([-e[1],e[0]]);gamma=dot(n,p)
        assert s.simplify(n[0]**2+b0sq*n[1]**2-gamma**2)==0
        assert s.simplify(p[0]**2/a**2+p[1]**2/b**2-1)==0
        contact=s.Matrix([n[0]/gamma,b0sq*n[1]/gamma])
        fraction=s.simplify(dot(contact-p,e)/dot(e,e))
        assert bool(fraction>0) and bool(fraction<1)
        incoming=(p-pm)/s.sqrt(dot(p-pm,p-pm))
        outgoing=e/s.sqrt(dot(e,e));no=s.Matrix([p[0]/a**2,p[1]/b**2])
        reflected=incoming-2*dot(incoming,no)/dot(no,no)*no
        assert all(s.simplify(x)==0 for x in outgoing-reflected)
        ray=p-F;ray2=pp-F;D=det(ray,ray2)
        assert bool(s.simplify(D)>0)
        mat=s.Matrix.vstack(ray.T,ray2.T)
        u=s.simplify(mat.inv()*s.Matrix([dot(ray,p),dot(ray2,pp)]))
        assert s.simplify(dot(ray,u-p))==s.simplify(dot(ray2,u-pp))==0
        q=s.simplify(p+dot(F-p,e)/dot(e,e)*e)
        assert s.simplify(dot(q-F,e))==s.simplify(det(q-p,e))==0
        Q.append(q);U.append(u)
        records.append({'focus_sign':fi,'edge':j,'focal_normals_determinant':str(s.simplify(D)),'caustic_contact_segment_fraction':str(fraction),'specular_reflection':'exact PASS'})
    pedal_edges=[s.simplify(det(Q[j]-F,Q[(j+1)%6]-F)) for j in range(6)]
    assert all(bool(v>0) for v in pedal_edges)
    assert area(U)==0 and area(Q)==10*s.sqrt(2)/9
    areas[str(fi)]={'antipedal_signed_area':str(area(U)),'pedal_signed_area':str(area(Q)),'pedal_edge_determinants':[str(v) for v in pedal_edges],'antipedal_vertices':[[str(x) for x in u] for u in U]}
assert area(P)==s.sqrt(2)
result={'status':'PASS','outer_semiaxis_squares':['9/8','9/32'],'caustic_semiaxis_squares':['1','5/32'],'focal_distance_squared':'27/32','least_period':6,'winding':1,'original_signed_area':str(area(P)),'zero_numerator_is_allowed':True,'exact_edge_certificates':records,'both_focal_areas':areas,'claim_limit':'This exact Cartesian orbit checks a permitted zero numerator. All-phase zero follows from the separately audited universal theorem, not from this one orbit alone.'}
Path(__file__).with_name('EXACT_ZERO_NUMERATOR.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','least_period':6,'antipedal_area':0,'pedal_area':'10*sqrt(2)/9'}))
