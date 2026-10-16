"""Exact independent N4 boundary control and a discriminating source-fixture check.

No Jacobi phase coordinates, inherited verification code or external files.
All geometry is direct Cartesian algebra in a quadratic extension.
"""
from pathlib import Path
import json
import sympy as s


def simp(x):
    return s.simplify(s.expand(x))


def dot(x, y):
    return x[0]*y[0]+x[1]*y[1]


def det(x, y):
    return x[0]*y[1]-x[1]*y[0]


def sub(x, y):
    return (x[0]-y[0],x[1]-y[1])


def norm(x):
    return s.sqrt(simp(dot(x,x)))


def area(points):
    return simp(sum(det(p,points[(j+1)%len(points)]) for j,p in enumerate(points))/2)


def check_case(points):
    residuals={}
    for j,p in enumerate(points):
        prev=points[(j-1)%4];q=points[(j+1)%4]
        residuals[f'boundary_{j}']=simp(p[0]**2/4+p[1]**2-1)
        n=(p[0]/4,p[1]);incoming=sub(p,prev);outgoing=sub(q,p)
        incoming=tuple(x/norm(incoming) for x in incoming)
        outgoing=tuple(x/norm(outgoing) for x in outgoing)
        reflected=tuple(incoming[t]-2*dot(incoming,n)*n[t]/dot(n,n) for t in range(2))
        for t in range(2):residuals[f'unit_reflection_{j}_{t}']=simp(reflected[t]-outgoing[t])
        direction=sub(q,p);line=(direction[1],-direction[0]);w=dot(line,p)
        lam=simp((4*line[0]**2+line[1]**2-w**2)/dot(line,line))
        residuals[f'common_caustic_parameter_{j}']=simp(lam-s.Rational(4,5))
        # Exact actual adjacent boundary-tangent intersection.
        nn=(q[0]/4,q[1]);cross=det(n,nn)
        assert cross!=0
        vertex=((nn[1]-n[1])/cross,(n[0]-nn[0])/cross)
        residuals[f'actual_outer_tangent_{j}_0']=simp(dot(n,vertex)-1)
        residuals[f'actual_outer_tangent_{j}_1']=simp(dot(nn,vertex)-1)
    vertices=[]
    for j,p in enumerate(points):
        q=points[(j+1)%4];n=(p[0]/4,p[1]);nn=(q[0]/4,q[1]);cross=det(n,nn)
        vertices.append(((nn[1]-n[1])/cross,(n[0]-nn[0])/cross))
    areas={}
    for e in [-1,1]:
        f=(e*s.sqrt(3),s.Integer(0));feet=[]
        for j,p in enumerate(points):
            x=vertices[(j-1)%4];y=vertices[j];edge=sub(y,x)
            t=simp(dot(sub(f,x),edge)/dot(edge,edge))
            foot=tuple(simp(x[v]+t*edge[v]) for v in range(2));feet.append(foot)
            residuals[f'foot_on_actual_side_{e}_{j}']=simp(det(sub(foot,x),edge))
            residuals[f'foot_perpendicular_{e}_{j}']=simp(dot(sub(f,foot),edge))
            residuals[f'auxiliary_circle_{e}_{j}']=simp(dot(foot,foot)-4)
        areas[str(e)]=area(feet)
    assert all(v==0 for v in residuals.values()),residuals
    inverse={}
    for e in [-1,1]:
        f=(e*s.sqrt(3),s.Integer(0));inverted=[]
        for p in points:
            v=sub(p,f);squared=dot(v,v)
            inverted.append(tuple(simp(x/squared) for x in v))
        inverse[str(e)]=area(inverted)
    return {'points':[[str(x) for x in p] for p in points],
            'zero_residuals':{k:str(v) for k,v in residuals.items()},
            'exact_zero_count':len(residuals),'outer_pedal_areas':{k:str(v) for k,v in areas.items()},
            'outer_pedal_product':str(simp(areas['-1']*areas['1'])),
            'original_unit_inverse_areas':{k:str(v) for k,v in inverse.items()},
            'original_unit_inverse_product':str(simp(inverse['-1']*inverse['1']))}


def main():
    D=[(s.Integer(2),s.Integer(0)),(s.Integer(0),s.Integer(1)),(-s.Integer(2),s.Integer(0)),(s.Integer(0),-s.Integer(1))]
    rect=[(x/s.sqrt(5),y/s.sqrt(5)) for x,y in [(4,1),(-4,1),(-4,-1),(4,-1)]]
    cases=[check_case(D),check_case(rect)]
    assert [c['outer_pedal_product'] for c in cases]==['16','25']
    assert [c['original_unit_inverse_product'] for c in cases]==['1','25/16']
    # Literal printed source rectangle: on E, but its normal is not a reflection bisector.
    wrong=[(x/s.sqrt(5),y/s.sqrt(5)) for x,y in [(2,2),(-2,2),(-2,-2),(2,-2)]]
    p=wrong[0];n=(p[0]/4,p[1]);incoming=sub(p,wrong[-1]);outgoing=sub(wrong[1],p)
    incoming=tuple(x/norm(incoming) for x in incoming);outgoing=tuple(x/norm(outgoing) for x in outgoing)
    reflection=[simp(incoming[t]-2*dot(incoming,n)*n[t]/dot(n,n)-outgoing[t]) for t in range(2)]
    assert reflection==[s.Rational(9,17),-s.Rational(15,17)]
    wrong_lambdas=[]
    for j in range(2):
        p=wrong[j];q=wrong[j+1];direction=sub(q,p)
        line=(direction[1],-direction[0]);w=dot(line,p)
        wrong_lambdas.append(simp((4*line[0]**2+line[1]**2-w**2)/dot(line,line)))
    assert wrong_lambdas==[s.Rational(1,5),s.Rational(16,5)]
    out={'kind':'exact Cartesian parity boundary and printed-fixture discrimination',
         'ellipse_squared_axes':['4','1'],'caustic_lambda':'4/5','primitive_period':4,
         'cases':cases,'exact_zero_count':sum(c['exact_zero_count'] for c in cases),
         'even_product_constancy_counterexample':True,
         'literal_printed_Ferudun0062_p6_rectangle':{'coordinates':'(+-2/sqrt5,+-2/sqrt5)',
             'boundary_residual':'0','first_unit_reflection_residual':[str(v) for v in reflection],
             'alternating_confocal_parameters':[str(x) for x in wrong_lambdas],
             'genuine_billiard':False},
         'corrected_rectangle':'(+-4/sqrt5,+-1/sqrt5)',
         'interpretation':'Even primitive extension is false by exact genuine examples; the related paper printed a wrong rectangle, while its inverse-product numbers fit the corrected one. This does not refute its all-odd proof or the current odd outer-pedal theorem.'}
    raw=json.dumps(out,indent=2)+'\n'
    (Path(__file__).resolve().parent/'ROOT_EXACT_EVEN_CONTROL.json').write_text(raw)
    print(raw,end='')


if __name__=='__main__':
    main()
