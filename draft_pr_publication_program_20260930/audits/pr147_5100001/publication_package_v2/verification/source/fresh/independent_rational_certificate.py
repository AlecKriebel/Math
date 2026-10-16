"""Independent PR147 certificate, constructed without reading author verifier.

Only the Python standard library is required. All geometric comparisons are
exact Fraction comparisons, and failures remain effective with Python -O.
This establishes the two finite examples, not historical priority.
"""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path

checks = 0

def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise ValueError(message)

def add(u, v): return tuple(x+y for x,y in zip(u,v))
def sub(u, v): return tuple(x-y for x,y in zip(u,v))
def mul(c, u): return tuple(c*x for x in u)
def dot(u, v): return sum(x*y for x,y in zip(u,v))
def det(u, v): return u[0]*v[1]-u[1]*v[0]
def sqrt_fraction(x):
    require(x >= 0, "negative squared length")
    p, q = isqrt(x.numerator), isqrt(x.denominator)
    require(p*p == x.numerator and q*q == x.denominator,
            "this finite certificate requires a rational square root")
    return F(p,q)
def area(vertices):
    return sum(det(vertices[i],vertices[(i+1)%len(vertices)])
               for i in range(len(vertices)))/2
def intersect(n1,h1,n2,h2):
    z=det(n1,n2)
    require(z != 0, "consecutive outer tangents are parallel")
    return ((h1*n2[1]-n1[1]*h2)/z,
            (n1[0]*h2-h1*n2[0])/z)
def serialize(obj):
    if isinstance(obj,F): return str(obj)
    if isinstance(obj,dict): return {k:serialize(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)): return [serialize(v) for v in obj]
    return obj

def certificate(vertices, A=F(16), B=F(9), Ac=F(256,25), Bc=F(81,25)):
    n=len(vertices)
    require(n == 4 and len(set(vertices)) == n, "not four distinct vertices")
    require(A > B > 0 and A-Ac == B-Bc > 0,
            "caustic is not confocal and strictly smaller")
    require(Ac > Bc > 0, "caustic is not an ellipse")
    for p in vertices:
        require(p[0]**2/A+p[1]**2/B == 1,"orbit vertex off ellipse")
    # Strict convexity and positive winding, with no reliance on a plot.
    for i in range(n):
        require(det(sub(vertices[(i+1)%n],vertices[i]),
                    sub(vertices[(i+2)%n],vertices[(i+1)%n])) > 0,
                "polygon is not strictly convex and counterclockwise")
    normals=[(p[0]/A,p[1]/B) for p in vertices]
    outer=[intersect(normals[i],F(1),normals[(i+1)%n],F(1))
           for i in range(n)]
    length=[]; contacts=[]; reflections=[]; cosines=[]; half_squares=[]
    incoming_states=[]
    for i,p in enumerate(vertices):
        q=vertices[(i+1)%n]
        edge=sub(q,p)
        ell=sqrt_fraction(dot(edge,edge))
        length.append(ell)
        vout=mul(1/ell,edge)
        previous=sub(p,vertices[(i-1)%n])
        vin=mul(1/sqrt_fraction(dot(previous,previous)),previous)
        normal=normals[i]
        reflected=sub(vin,mul(2*dot(vin,normal)/dot(normal,normal),normal))
        require(reflected == vout,"ordinary unit-speed reflection fails")
        require(dot(vin,normal) > 0 and dot(vout,normal) < 0,
                "directions are not physically incoming and outgoing")
        reflections.append({"vertex":p,"unit_in":vin,"unit_out":vout,
                            "outward_normal":normal,"reflected_unit_in":reflected})
        incoming_states.append((p,vin))
        # For n_line . X = h, tangency to the centered diagonal ellipse
        # is h^2 = Ac*n_x^2 + Bc*n_y^2. Its unique point is C*n/h.
        nline=(-edge[1],edge[0]); h=dot(nline,p)
        require(h != 0,"edge line through caustic center")
        require(h*h == Ac*nline[0]**2+Bc*nline[1]**2,
                "edge line not tangent to fixed caustic")
        touch=(Ac*nline[0]/h,Bc*nline[1]/h)
        require(touch[0]**2/Ac+touch[1]**2/Bc == 1,
                "alleged contact off caustic")
        require(det(sub(touch,p),edge) == 0,"contact not on edge line")
        coordinate=dot(sub(touch,p),edge)/dot(edge,edge)
        require(0 < coordinate < 1,"contact not in open edge segment")
        contacts.append({"point":touch,"edge_coordinate":coordinate})
        uleft=mul(-1,vin)
        cosine=dot(uleft,vout)
        require(-1 < cosine < 1,"degenerate polygon angle")
        cosines.append(cosine)
        half_squares.append((1-cosine)/2)
    require(len(set(incoming_states)) == 4,"earlier incoming oriented state returns")
    orbit_area=area(vertices); outer_area=area(outer)
    require(orbit_area > 0 and outer_area > 0,"signed area nonpositive")
    product_squared=F(1)
    supplement_squared=F(1)
    for h in half_squares: product_squared*=h
    for c in cosines: supplement_squared *= (1+c)/2
    product=sqrt_fraction(product_squared)
    supplement=sqrt_fraction(supplement_squared)
    ratio=outer_area/orbit_area
    return {"vertices":vertices,"outer_vertices":outer,
            "caustic_axes_squared":[Ac,Bc],"contacts":contacts,
            "physical_reflections":reflections,"edge_lengths":length,
            "perimeter":sum(length),"primitive_period":4,
            "signed_orbit_area":orbit_area,"signed_outer_area":outer_area,
            "area_ratio":ratio,"internal_angle_cosines":cosines,
            "half_angle_squares":half_squares,"half_angle_product":product,
            "k107":ratio*product,"supplement_half_angle_product":supplement,
            "supplementary_convention_k107":ratio*supplement,
            "quotient_k103_over_k105":ratio/product,
            "area_product":orbit_area*outer_area,
            "joachimsthal":dot(normals[0],reflections[0]["unit_in"])}

def main():
    diamond=[(F(4),F(0)),(F(0),F(3)),(F(-4),F(0)),(F(0),F(-3))]
    rectangle=[(F(16,5),F(9,5)),(F(-16,5),F(9,5)),
               (F(-16,5),F(-9,5)),(F(16,5),F(-9,5))]
    d=certificate(diamond); r=certificate(rectangle)
    require(d["k107"] == F(288,625),"wrong diamond value")
    require(r["k107"] == F(625,1152),"wrong rectangle value")
    require(r["k107"]-d["k107"] == F(58849,720000),"wrong strict difference")
    require(d["perimeter"] == r["perimeter"] == 20,"perimeters differ")
    require(d["joachimsthal"] == r["joachimsthal"] == F(1,5),
            "Joachimsthal constants differ")
    require(d["quotient_k103_over_k105"] == r["quotient_k103_over_k105"],
            "two-representative corrected quotient diagnostic differs")
    require(d["area_product"] == r["area_product"] == 1152,
            "known even-period area-product consistency fails")
    require(d["supplementary_convention_k107"] !=
            r["supplementary_convention_k107"],
            "supplementary angle convention removes counterexample")
    # Reverse orientation changes both signed areas, and consequently leaves
    # their ratio, positive half-angle product, and counterexample intact.
    # The certificate intentionally enforces counterclockwise orientation;
    # verify reversal directly by the exact signed shoelace identity instead.
    require(area(list(reversed(diamond))) == -d["signed_orbit_area"],
            "orientation reversal does not negate orbit area")
    require(area(list(reversed(d["outer_vertices"]))) == -d["signed_outer_area"],
            "orientation reversal does not negate outer area")
    negative_controls=[]
    cases=[("wrong caustic",diamond,F(10),F(3)),
           ("off-ellipse point",[(F(5),F(0))]+diamond[1:],F(256,25),F(81,25))]
    for label,vertices,ac,bc in cases:
        try: certificate(vertices,Ac=ac,Bc=bc)
        except ValueError as e: negative_controls.append({"name":label,"rejected":str(e)})
        else: raise ValueError("negative control falsely accepted: "+label)
    result={"status":"PASS_EXACT_FINITE_COUNTEREXAMPLE","checks":checks,
            "diamond":d,"rectangle":r,"negative_controls":negative_controls,
            "limitations":["No historical priority conclusion.",
                            "No proposed corrected all-period invariant is proved.",
                            "The continuous-family proof is recorded separately."]}
    output=Path(__file__).with_name("RATIONAL_CERTIFICATE.json")
    output.write_text(json.dumps(serialize(result),indent=2)+"\n")
    print(json.dumps({"status":result["status"],"checks":checks,
                      "k107_D":str(d["k107"]),"k107_R":str(r["k107"]),
                      "difference":str(r["k107"]-d["k107"])}))

if __name__ == "__main__": main()
