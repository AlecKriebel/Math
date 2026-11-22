import sympy as s
from math import comb
x,z=s.symbols('t z')

def lift_delta(a,d):
    return s.expand(sum(v*(2*x)**i*(1+x)**(d-2*i) for i,v in enumerate(a)))

def bary_basis(d):
    p=[s.Integer(1)]
    for n in range(1,d+1):
        p=[s.expand(x*sum(p[:k])+sum(p[k:])) for k in range(n+1)]
    return p

def bary_transform(a):
    return s.expand(sum(v*p for v,p in zip(a,bary_basis(len(a)-1))))

def pyr(h,d): return s.expand((1+(d+1)*x)*h+x*(1-x)*s.diff(h,x))
def prism(h,d): return s.expand((1+(2*d+1)*x)*h+2*x*(1-x)*s.diff(h,x))

def rr_exact(p):
    pp=s.Poly(p,x)
    return sum(m for interval,m in s.polys.polytools.intervals(pp,eps=s.Rational(1,10000)))==pp.degree()

records={}
records['formal_balanced_delta']=1+6*z+6*z*z+2*z**3
records['formal_balanced_discriminant']=s.discriminant(records['formal_balanced_delta'],z)
assert records['formal_balanced_discriminant']==-108
records['formal_balanced_lift']=lift_delta([1,6,6,2],6)
assert records['formal_balanced_lift']==1+18*x+87*x*x+156*x**3+87*x**4+18*x**5+x**6
assert not rr_exact(records['formal_balanced_lift'])
records['local_sum']=s.expand((1+x)**4+(1+4*x+x*x)**2)
assert records['local_sum']==2+12*x+24*x*x+12*x**3+2*x**4
assert not rr_exact(records['local_sum'])
records['local_sum_gamma_discriminant']=s.discriminant(2+4*z+4*z*z,z)
assert records['local_sum_gamma_discriminant']==-16
H_cube=1+23*x+23*x*x+x**3
records['cube_from_faces']=s.expand((1-x)**3+x*(8*(1-x)**2+12*(1-x)*(1+x)+6*(1+6*x+x*x)))
assert records['cube_from_faces']==H_cube
records['cube_interval_identity']=s.expand(3*H_cube+(1-x)*s.diff(H_cube,x))
assert records['cube_interval_identity']==26+92*x+26*x*x
records['cube_wrong_boolean_transform']=bary_transform([1,5,-1,1])
assert records['cube_wrong_boolean_transform']==1+23*x+11*x*x+x**3
records['cube_two_subdivisions']=bary_transform([1,23,23,1])
assert records['cube_two_subdivisions']==1+143*x+143*x*x+x**3
H24=s.expand((1-x)**4+x*(24*(1-x)**3+96*(1-x)**2*(1+x)+96*(1-x)*(1+4*x+x*x)+24*H_cube))
records['24_cell']=H24
assert H24==1+236*x+678*x*x+236*x**3+x**4
assert H24==lift_delta([1,116,52],4)
records['24_cell_delta_discriminant']=s.discriminant(1+116*z+52*z*z,z)
assert records['24_cell_delta_discriminant']==13248
assert pyr(s.Integer(1),0)==1+x
assert prism(s.Integer(1),0)==1+x
records['square_pyramid']=pyr(1+6*x+x*x,2)
assert records['square_pyramid']==1+15*x+15*x*x+x**3
records['cube_pyramid']=pyr(H_cube,3)
assert records['cube_pyramid']==1+50*x+138*x*x+50*x**3+x**4
records['cube_pyramid_prism']=prism(records['cube_pyramid'],4)
assert records['cube_pyramid_prism']==1+159*x+1040*x*x+1040*x**3+159*x**4+x**5
for key in ['cube_from_faces','cube_two_subdivisions','24_cell','square_pyramid','cube_pyramid','cube_pyramid_prism']:
    assert rr_exact(records[key]),key
for key,value in records.items(): print(f'{key}: {value}')
print('PASS: symbolic identities, exact discriminants and rational root-isolation counts.')
