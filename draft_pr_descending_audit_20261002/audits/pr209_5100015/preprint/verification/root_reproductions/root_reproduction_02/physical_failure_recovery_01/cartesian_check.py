#!/usr/bin/env python3
"""Independent direct geometry; does not import submitted proof/checker code.

High precision is NOT interval certification. Exact SymPy checks are separated.
"""
import argparse
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def det(x, y):
    return x[0]*y[1]-x[1]*y[0]


def add(x, y):
    return (x[0]+y[0], x[1]+y[1])


def mul(t, x):
    return (t*x[0], t*x[1])


def shoelace(vertices):
    return sum(det(p, q) for p, q in zip(vertices, vertices[1:]+vertices[:1]))/2


def init(a, b, lam, phase):
    q = (a*mp.cos(phase), b*mp.sin(phase))
    normal = (q[0]/a**2, q[1]/b**2)
    norm = mp.sqrt(dot(normal, normal))
    nhat = mul(1/norm, normal)
    tangent = (-nhat[1], nhat[0])
    D = (a*b*norm)**2
    s = mp.sqrt(lam/D)
    c = mp.sqrt(1-lam/D)
    return q, add(mul(c, tangent), mul(-s, nhat))


def advance(a, b, q, velocity):
    normal = (q[0]/a**2, q[1]/b**2)
    invv = velocity[0]**2/a**2+velocity[1]**2/b**2
    length = -2*dot(normal, velocity)/invv
    nxt = add(q, mul(length, velocity))
    nn = (nxt[0]/a**2, nxt[1]/b**2)
    reflected = add(velocity, mul(-2*dot(nn, velocity)/dot(nn, nn), nn))
    return nxt, reflected, length


def trace(a, b, lam, phase, N, diagnostics=True):
    q, v = init(a, b, lam, phase)
    q0, v0 = q, v
    vertices = []
    angle = mp.mpf('0')
    errors = {k: mp.mpf('0') for k in ['ellipse', 'caustic', 'reflection_speed', 'reflection_tangent', 'reflection_normal']}
    min_step = mp.inf
    for _ in range(N):
        vertices.append(q)
        nxt, w, length = advance(a, b, q, v)
        ux, uy = q[0]/a, q[1]/b
        vx, vy = nxt[0]/a, nxt[1]/b
        delta = mp.atan2(ux*vy-uy*vx, ux*vx+uy*vy)
        if delta < 0:
            delta += 2*mp.pi
        angle += delta
        if diagnostics:
            errors['ellipse'] = max(errors['ellipse'], abs(ux**2+uy**2-1))
            speed = dot(v, v)
            caustic = (a*a*v[1]**2+b*b*v[0]**2-det(q, v)**2)/speed
            errors['caustic'] = max(errors['caustic'], abs(caustic-lam))
            normal = (nxt[0]/a**2, nxt[1]/b**2)
            tangent = (-normal[1], normal[0])
            errors['reflection_speed'] = max(errors['reflection_speed'], abs(dot(w,w)-speed))
            errors['reflection_tangent'] = max(errors['reflection_tangent'], abs(dot(w,tangent)-dot(v,tangent)))
            errors['reflection_normal'] = max(errors['reflection_normal'], abs(dot(w,normal)+dot(v,normal)))
            min_step = min(min_step, length)
        q, v = nxt, w
    errors['position_closure'] = mp.sqrt(dot(add(q,mul(-1,q0)),add(q,mul(-1,q0))))
    errors['velocity_closure'] = mp.sqrt(dot(add(v,mul(-1,v0)),add(v,mul(-1,v0))))
    return vertices, angle, errors, min_step


def closure_caustic(a, b, N, winding):
    # Solve the geometric endpoint angle at a boundary-axis start. No elliptic
    # parametrization, complete integral, or author trace is used.
    lo, hi = mp.mpf('0'), b*b
    target = 2*mp.pi*winding
    for _ in range(int(mp.mp.dps*3.5)):
        mid = (lo+hi)/2
        _, angle, _, _ = trace(a,b,mid,mp.mpf('0'),N,False)
        if angle < target:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def geometry(a, b, vertices):
    normals = [(q[0]/a**2,q[1]/b**2) for q in vertices]
    outer, feet = [], []
    min_det = mp.inf
    incidence, foot_orthogonal = mp.mpf('0'), mp.mpf('0')
    for n, m in zip(normals,normals[1:]+normals[:1]):
        denominator = det(n,m)
        min_det = min(min_det, abs(denominator))
        outer.append(((m[1]-n[1])/denominator,(n[0]-m[0])/denominator))
        feet.append(mul(1/dot(n,n),n))
    for i, (n,h) in enumerate(zip(normals,feet)):
        prev, nxt = outer[i-1], outer[i]
        incidence=max(incidence,abs(dot(n,prev)-1),abs(dot(n,nxt)-1),abs(dot(n,h)-1))
        foot_orthogonal=max(foot_orthogonal,abs(dot(h,add(nxt,mul(-1,prev)))))
    A, B = shoelace(outer), shoelace(feet)
    angles=[mp.atan2(q[1]/b,q[0]/a) for q in vertices]
    directA=mp.mpf('0'); directB=mp.mpf('0')
    for t,s in zip(angles,angles[1:]+angles[:1]):
        directA+=a*b*mp.tan((s-t)/2)
        D=b*b*mp.cos(t)**2+a*a*mp.sin(t)**2
        E=b*b*mp.cos(s)**2+a*a*mp.sin(s)**2
        directB+=a**3*b**3*mp.sin(s-t)/(2*D*E)
    return A,B,{'line_incidence':incidence,'foot_orthogonality':foot_orthogonal,
                'outer_area_identity':abs(A-directA),'pedal_area_identity':abs(B-directB),
                'min_tangent_determinant':min_det}


def cartesian_transform(a,b,lam,vertices):
    plus=[];minus=[];T=mp.sqrt(lam)
    for x,y in vertices:
        c,s=x/a,y/b;D=b*b*c*c+a*a*s*s;R=mp.sqrt(D-lam)
        midpoint=(-a*a*s*R/D,b*b*c*R/D)
        plus.append(add(midpoint,mul(a*b*T/D,(c,s))))
        minus.append(add(midpoint,mul(-a*b*T/D,(c,s))))
    joins=max(mp.sqrt(dot(add(p,mul(-1,q)),add(p,mul(-1,q)))) for p,q in zip(minus,plus[1:]+plus[:1]))
    edges=[add(q,mul(-1,p)) for p,q in zip(plus,plus[1:]+plus[:1])]
    feet=[mul(1/(x*x/a**4+y*y/b**4),(x/a**2,y/b**2)) for x,y in vertices]
    area_error=abs(shoelace(feet)-a*b*shoelace(edges)/(4*lam))
    pointwise=mp.mpf('0');incidence=mp.mpf('0')
    for i,h in enumerate(feet):
        predicted=(-b*edges[i][0]/(2*T),-a*edges[i][1]/(2*T))
        pointwise=max(pointwise,mp.sqrt(dot(add(predicted,mul(-1,h)),add(predicted,mul(-1,h)))))
        for p in [plus[i],minus[i]]:
            incidence=max(incidence,abs(p[0]**2/a**2+p[1]**2/b**2-1))
    return {'transformed_chord_join':joins,'transformed_ellipse_incidence':incidence,
            'pointwise_center_foot_edge_map':pointwise,'transformed_edge_area_map':area_error}


def exact_geometry(vertices,a2,b2):
    normals=[(sp.cancel(x/a2),sp.cancel(y/b2)) for x,y in vertices]
    outer=[];feet=[]
    for n,m in zip(normals,normals[1:]+normals[:1]):
        denominator=det(n,m)
        outer.append(((m[1]-n[1])/denominator,(n[0]-m[0])/denominator))
        feet.append(mul(1/dot(n,n),n))
    A,B=sp.simplify(shoelace(outer)),sp.simplify(shoelace(feet))
    return A,B,sp.simplify(A*B)


def exact_orbit(vertices,a2,b2):
    residuals=[];orientations=[];lambdas=[]
    for i,q in enumerate(vertices):
        prev,nxt=vertices[i-1],vertices[(i+1)%len(vertices)]
        incoming=add(q,mul(-1,prev));outgoing=add(nxt,mul(-1,q))
        n=(q[0]/a2,q[1]/b2)
        reflected=add(incoming,mul(-2*dot(n,incoming)/dot(n,n),n))
        residuals.extend([sp.simplify(det(reflected,outgoing)),sp.simplify(q[0]**2/a2+q[1]**2/b2-1)])
        orientations.append(sp.simplify(dot(reflected,outgoing)))
        lambdas.append(sp.simplify((a2*outgoing[1]**2+b2*outgoing[0]**2-det(q,outgoing)**2)/dot(outgoing,outgoing)))
    allzero=all(x==0 for x in residuals)
    # SymPy proves positivity of these explicit real algebraic expressions.
    forward=all(x.is_positive is True for x in orientations)
    fixedcaustic=all(sp.simplify(x-lambdas[0])==0 for x in lambdas)
    pair_distances=[sp.simplify(dot(add(x,mul(-1,y)),add(x,mul(-1,y)))) for i,x in enumerate(vertices) for y in vertices[:i]]
    primitive=all(d.is_positive is True for d in pair_distances)
    return {'reflection_and_incidence_residuals':[str(x) for x in residuals],
            'reflected_outgoing_positive_dots':[str(x) for x in orientations],
            'reflection_incidence_and_forward_verified':allzero and forward,
            'caustic_lambda':str(lambdas[0]),'all_edges_same_caustic':fixedcaustic,
            'primitive_distinct_vertices_verified':primitive}


def exact_checks():
    a2,b2=sp.Integer(4),sp.Integer(1)
    # The two axis phases of the primitive triangle are derived by solving the
    # physical reflection at a vertical (respectively horizontal) opposite side.
    # Reflection reduces to (a2-b2)c^2-2*b2*c-a2=0 at a major-axis start.
    cx=(1-sp.sqrt(13))/3; sx=sp.sqrt(1-cx**2)
    cy=(sp.sqrt(13)-4)/3; sy=sp.sqrt(1-cy**2)
    tri_x=[(sp.Integer(2),sp.Integer(0)),(2*cx,sx),(2*cx,-sx)]
    tri_y=[(sp.Integer(0),sp.Integer(1)),(-2*sy,cy),(2*sy,cy)]
    # Primitive four-bounce same-caustic negative controls, independently
    # obtained by the axis diamond and the normal-bisected rectangle.
    diamond=[(sp.Integer(2),sp.Integer(0)),(sp.Integer(0),sp.Integer(1)),(-sp.Integer(2),sp.Integer(0)),(sp.Integer(0),-sp.Integer(1))]
    root5=sp.sqrt(5)
    rectangle=[(4/root5,1/root5),(-4/root5,1/root5),(-4/root5,-1/root5),(4/root5,-1/root5)]
    # 4/9 was recognized from the independently solved Cartesian closure root.
    # Generate both six-period witnesses by actual reflection, without hardcoded
    # vertices. These same witnesses also appear in the inherited author checker,
    # which was read before this exact six-period verification was added.
    sixes=[]
    for q,v in [((sp.Integer(2),sp.Integer(0)),(-sp.Rational(2,3),sp.sqrt(5)/3)),
                ((sp.Integer(0),sp.Integer(1)),(-2*sp.sqrt(2)/3,-sp.Rational(1,3)))]:
        vertices=[]
        for _ in range(6):
            vertices.append(q)
            q,v,_=advance(sp.Integer(2),sp.Integer(1),q,v)
            q=tuple(sp.simplify(x) for x in q);v=tuple(sp.simplify(x) for x in v)
        assert all(sp.simplify(x-y)==0 for x,y in zip(q,vertices[0]))
        sixes.append(vertices)
    rows=[]
    for name,vertices in [('triangle_x',tri_x),('triangle_y',tri_y),('four_diamond',diamond),('four_rectangle',rectangle),('six_x',sixes[0]),('six_y',sixes[1])]:
        row=exact_orbit(vertices,a2,b2);A,B,product=exact_geometry(vertices,a2,b2)
        row.update({'name':name,'vertices':[[str(x),str(y)] for x,y in vertices],
                    'A_outer':str(A),'B_pedal':str(B),'product':str(product)})
        rows.append(row)
    triangle_equal=sp.simplify(exact_geometry(tri_x,a2,b2)[2]-exact_geometry(tri_y,a2,b2)[2])==0
    tri_caustic_equal=sp.simplify(sp.sympify(rows[0]['caustic_lambda'])-sp.sympify(rows[1]['caustic_lambda']))==0
    four_lam=all(sp.simplify(sp.sympify(row['caustic_lambda'])-sp.Rational(4,5))==0 for row in rows[2:4])
    four_values=[exact_geometry(v,a2,b2)[2] for v in [diamond,rectangle]]
    six_values=[exact_geometry(v,a2,b2)[2] for v in sixes]
    passed=all(row['reflection_incidence_and_forward_verified'] and row['all_edges_same_caustic'] and row['primitive_distinct_vertices_verified'] for row in rows)
    passed=passed and triangle_equal and tri_caustic_equal and four_lam and four_values==[32,50] and six_values==[40,40]
    return {'status':'PASS' if passed else 'FAIL','cases':rows,
            'triangle_same_caustic':tri_caustic_equal,'triangle_equal_products':triangle_equal,
            'four_same_caustic_lambda_4_over_5':four_lam,'four_products_32_and_50':four_values==[32,50],
            'six_products_40_and_40':six_values==[40,40]}


def symbolic_cartesian_reduction():
    # Generic exact polynomial identities for the geometric construction in
    # CARTESIAN_REDUCTION.md. Positivity assumptions are proved there.
    a,b,c,s,T,R=sp.symbols('a b c s T R',nonzero=True,real=True)
    D=b*b*c*c+a*a*s*s
    e=(c,s)
    midpoint=(-a*a*s*R/D,b*b*c*R/D)
    plus=add(midpoint,mul(a*b*T/D,e))
    minus=add(midpoint,mul(-a*b*T/D,e))
    q=(a*c,b*s)
    foot=mul(1/(c*c/(a*a)+s*s/(b*b)),(c/a,s/b))
    velocity=((-a*s*R-b*c*T)/D,(b*c*R-a*s*T)/D)
    normal_minus=(minus[0]/a**2,minus[1]/b**2)
    relations=[]
    for p in [plus,minus]:
        relations.append(p[0]**2/a**2+p[1]**2/b**2-1)
        relations.append(-s*p[0]+c*p[1]-R)
    relations.extend([dot(velocity,velocity)-1,
                      dot((c/a,s/b),velocity)+T/(a*b),
                      dot(e,normal_minus)+T/(a*b),
                      a*normal_minus[0]-velocity[0],b*normal_minus[1]-velocity[1]])
    edge=add(plus,mul(-1,minus))
    relations.extend([foot[0]-b*edge[0]/(2*T),foot[1]-a*edge[1]/(2*T)])
    reductions=[]
    for expression in relations:
        numerator=sp.fraction(sp.cancel(expression))[0]
        numerator=sp.rem(sp.Poly(numerator,R),sp.Poly(R**2-D+T*T,R)).as_expr()
        numerator=sp.rem(sp.Poly(numerator,c),sp.Poly(c*c+s*s-1,c)).as_expr()
        reductions.append(sp.factor(numerator))
    return {'status':'PASS' if all(x==0 for x in reductions) else 'FAIL',
            'identities':len(reductions),'reduced_numerators':[str(x) for x in reductions]}


def strval(x):
    return mp.nstr(x,25)


def run():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True); parser.add_argument('--dps',type=int,default=80)
    args=parser.parse_args(); mp.mp.dps=args.dps
    cases=[('odd3',2,1,3,1),('odd5',2,1,5,1),('even6',2,1,6,1),
           ('odd_star5_2',2,1,5,2),('even_star10_3',2,1,10,3),
           ('odd_star7_3',3,1,7,3),('even14',2,1,14,1),
           ('boundary4',2,1,4,1),('boundary8',2,1,8,1),('boundary8star',2,1,8,3),
           ('near_circle',mp.mpf('1.000001'),1,5,2),('thin',10,1,7,1),('largeN',2,1,50,1)]
    phases=[mp.mpf('0'),mp.mpf('.173'),mp.mpf('.631'),mp.mpf('1.17')]
    out={'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'dps':args.dps,'numerics_certified':False,'construction':'Cartesian reflection, line intersections, orthogonal feet',
         'exact':exact_checks(),'symbolic_cartesian_reduction':symbolic_cartesian_reduction(),'cases':[]}
    for name,a,b,N,winding in cases:
        a,b=mp.mpf(a),mp.mpf(b); lam=closure_caustic(a,b,N,winding)
        products=[]; rows=[]; reference=None
        for phase in phases:
            vertices,angle,errors,minstep=trace(a,b,lam,phase,N)
            A,B,g=geometry(a,b,vertices); products.append(A*B)
            transform=cartesian_transform(a,b,lam,vertices)
            reversed_product=mp.fprod(geometry(a,b,list(reversed(vertices)))[:2])
            repeated_product=mp.fprod(geometry(a,b,vertices*3)[:2])
            primitive_dist=min(mp.sqrt(dot(add(vertices[i],mul(-1,vertices[0])),add(vertices[i],mul(-1,vertices[0])))) for i in range(1,N))
            rows.append({'phase':strval(phase),'A_outer':strval(A),'B_pedal':strval(B),'product':strval(A*B),
                         'orbit_residuals':{k:strval(v) for k,v in errors.items()},
                         'geometry_residuals':{k:strval(v) for k,v in g.items()},
                         'transform_residuals':{k:strval(v) for k,v in transform.items()},
                         'minimum_forward_step':strval(minstep),'min_primitive_vertex_separation':strval(primitive_dist),
                         'reversal_product_error':strval(abs(reversed_product-A*B)),
                         'triple_repetition_scaling_error':strval(abs(repeated_product-9*A*B))})
        variation=max(products)-min(products)
        out['cases'].append({'name':name,'a':strval(a),'b':strval(b),'N':N,'winding':winding,
                             'lambda':strval(lam),'relative_product_spread':strval(variation/max(abs(x) for x in products)),
                             'phases':rows})
        print(name,'lambda',strval(lam),'relative spread',strval(variation/max(abs(x) for x in products)),flush=True)
    target=[row for row in out['cases'] if not row['name'].startswith('boundary')]
    boundary=[row for row in out['cases'] if row['name'].startswith('boundary')]
    tolerance=mp.power(10,-args.dps+20)
    physical_residuals=[]
    for case in out['cases']:
        for row in case['phases']:
            physical_residuals.extend(mp.mpf(x) for x in row['orbit_residuals'].values())
            physical_residuals.extend(mp.mpf(v) for k,v in row['geometry_residuals'].items() if k!='min_tangent_determinant')
            physical_residuals.extend(mp.mpf(v) for v in row['transform_residuals'].values())
            physical_residuals.extend([mp.mpf(row['reversal_product_error']),mp.mpf(row['triple_repetition_scaling_error'])])
    target_spread=max(mp.mpf(row['relative_product_spread']) for row in target)
    min_boundary=min(mp.mpf(row['relative_product_spread']) for row in boundary)
    maxres=max(physical_residuals)
    checks={'exact_geometry':out['exact']['status']=='PASS',
            'symbolic_reduction':out['symbolic_cartesian_reduction']['status']=='PASS',
            'all_physical_residuals_small':maxres<tolerance,
            'target_products_phase_constant_at_working_precision':target_spread<tolerance,
            'excluded_periods_vary_at_same_caustic':min_boundary>mp.mpf('1e-4'),
            'all_sampled_vertices_distinct':all(mp.mpf(row['min_primitive_vertex_separation'])>mp.mpf('1e-5') for case in out['cases'] for row in case['phases'])}
    out.update({'status':'PASS' if all(checks.values()) else 'FAIL','finite_acceptance_checks':checks,
                'acceptance_tolerance':strval(tolerance),'maximum_physical_residual':strval(maxres),
                'maximum_target_relative_product_spread':strval(target_spread),
                'minimum_boundary_relative_product_spread':strval(min_boundary)})
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':
    run()
