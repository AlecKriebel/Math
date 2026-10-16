#!/usr/bin/env python3
"""Independent coordinate exterior-calculus controls; no author import."""
import hashlib,itertools,json,pathlib
import sympy as S
counts={}
def check(name,condition):
    if not condition:raise AssertionError(name)
    counts[name]=counts.get(name,0)+1
def trim(form):return {k:S.simplify(v) for k,v in form.items() if S.simplify(v)!=0}
def add(*forms):
    result={}
    for form in forms:
        for k,v in form.items():result[k]=result.get(k,0)+v
    return trim(result)
def mul(f,form):return trim({k:f*v for k,v in form.items()})
def wedge(a,b):
    result={}
    for I,c in a.items():
        for J,d in b.items():
            if len(set(I+J))!=len(I)+len(J):continue
            sign=(-1)**sum(i>j for i in I for j in J)
            k=tuple(sorted(I+J));result[k]=result.get(k,0)+sign*c*d
    return trim(result)
def exterior(form,coords):
    terms=[]
    for I,c in form.items():
        for i,x in enumerate(coords):terms.append(wedge({(i,):S.diff(c,x)},{I:S.Integer(1)}))
    return add(*terms)
def differential(f,coords):return exterior({():f},coords)
def equal(a,b):return not add(a,mul(-1,b))

families=[]
for dimension in (3,4):
    coords=S.symbols('x y z t',real=True)[:dimension];x,y,z=coords[:3]
    t=coords[3] if dimension==4 else S.Integer(0)
    dz={(2,):S.Integer(1)}
    for j,q in enumerate((x,x*y+z,x*x+y*z+t)):
        h=y+x*z+j*t;f=x*z+y*y+(j+1)*t;g=x*y+z*z+j*y
        a=mul(S.exp(q),dz);w=add(mul(-1,differential(q,coords)),mul(h,dz))
        da=exterior(a,coords);dw=exterior(w,coords);df=differential(f,coords)
        af=mul(S.exp(f),a);b=add(w,mul(-1,df),mul(g,a));db=exterior(b,coords)
        gv=wedge(w,dw);new=wedge(b,db);delta=add(new,mul(-1,gv))
        primitive=add(mul(g,da),mul(-f,dw),mul(g,wedge(df,a)))
        alternate=add(wedge(df,w),mul(g,wedge(a,add(w,mul(-1,df)))))
        check('coordinate_defining_equation',equal(da,wedge(a,w)))
        check('coordinate_integrability_domega',not wedge(a,dw))
        check('coordinate_GV_closed_including_dimension4',not exterior(gv,coords))
        check('coordinate_new_defining_equation',equal(exterior(af,coords),wedge(af,b)))
        check('coordinate_transgression_full_primitive',equal(delta,exterior(primitive,coords)))
        check('coordinate_transgression_alternate_primitive',equal(delta,exterior(alternate,coords)))
        check('primitives_differ_by_exact_d_fomega',equal(add(alternate,mul(-1,primitive)),exterior(mul(f,w),coords)))
        normalized_h=g*S.exp(-f)
        author_primitive=add(mul(-f,dw),mul(normalized_h,exterior(af,coords)))
        check('author_h_alpha_f_normalization',equal(primitive,author_primitive))
        f2=x-y+t;g2=y*y+z
        b2=add(b,mul(-1,differential(f2,coords)),mul(g2,af))
        direct=add(w,mul(-1,differential(f+f2,coords)),mul(g+S.exp(f)*g2,a))
        check('semidirect_gauge_composition',equal(b2,direct))
        if dimension==3:
            vector=lambda form:S.Matrix([form.get((1,2),0),-form.get((0,2),0),form.get((0,1),0)])
            W=vector(da);Y=vector(dw);A=S.Matrix([a.get((i,),0) for i in range(3)])
            grad=lambda u:S.Matrix([S.diff(u,c) for c in coords])
            check('vector_W_tangent',S.simplify(A.dot(W))==0)
            check('vector_Y_tangent',S.simplify(A.dot(Y))==0)
            check('vector_W_divergence_free',S.simplify(sum(S.diff(W[i],coords[i]) for i in range(3)))==0)
            J=g*W-f*Y+g*grad(f).cross(A)
            density=delta.get((0,1,2),0)
            check('vector_flux_matches_exterior_primitive',all(S.simplify(v)==0 for v in J-vector(primitive)))
            check('vector_flux_divergence_matches_GV_change',S.simplify(sum(S.diff(J[i],coords[i]) for i in range(3))-density)==0)
        families.append({'dimension':dimension,'q':str(q),'h':str(h),'f':str(f),'g':str(g)})

x,y,z=S.symbols('x y z',real=True);coords=(x,y,z)
dx,dy,dz=[{(i,):S.Integer(1)} for i in range(3)]
volume={(0,1,2):S.Integer(1)}
b=add(mul(-1,dx),mul(y,dz))
check('actual_local_product_gauge_contact_negative',equal(wedge(b,exterior(b,coords)),mul(-1,volume)))
good=mul(y,wedge(dx,dz));bad=mul(-1,good)
check('wrong_mixed_primitive_sign_detected',equal(exterior(good,coords),mul(-1,volume)) and equal(exterior(bad,coords),volume))
check('arbitrary_boundary_integral_nonzero',S.integrate(S.Integer(-1),(x,0,1),(y,0,1),(z,0,1))==-1)
periodic=add(mul(-S.cos(x),dx),mul(S.sin(y),dz))
density=wedge(periodic,exterior(periodic,coords))[(0,1,2)]
check('global_torus_sign_negative',density.subs({x:0,y:0})==-1)
check('global_torus_sign_positive',density.subs({x:S.pi,y:0})==1)
check('global_torus_exact_integral_zero',S.integrate(density,(x,0,2*S.pi),(y,0,2*S.pi),(z,0,2*S.pi))==0)
contact=add(dz,mul(x,dy))
check('nonintegrable_input_detected',not equal(exterior(contact,coords),{}))
check('nonfoliation_cannot_use_transgression',equal(wedge(contact,exterior(contact,coords)),volume) and not exterior(exterior(contact,coords),coords))
af=mul(S.exp(x),dz)
wrong=dx
check('wrong_rescaling_sign_detected',not equal(exterior(af,coords),wedge(af,wrong)))

root=pathlib.Path(__file__).resolve().parent
result={'assertions_passed':sum(counts.values()),'counts':counts,'sympy_version':S.__version__,
        'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'coordinate_families':families,
        'scope':'Actual local smooth coordinate algebra, compact torus zero-GV gauge control, boundary/sign failures. No target manifold counterexample.'}
(root/'coordinate_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
