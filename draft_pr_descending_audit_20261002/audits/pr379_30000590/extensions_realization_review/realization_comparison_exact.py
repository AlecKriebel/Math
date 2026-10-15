#!/usr/bin/env python3
"""Post-seal exact Nielsen matrix comparison, plus genuine chain boundaries."""
import json
import independent_exact_checks as r

t=r.mul_g(r.a,r.inv_g(r.c))
u=r.mul_g(r.b,r.inv_g(r.a))
v=r.mul_g(r.d,r.inv_g(r.c))
x,y,z=r.x,r.y,r.z
assert x==r.inv_g(u) and y==r.inv_g(v)
assert z==r.mul_g(r.mul_g(u,t),r.inv_g(v))
assert t==r.mul_g(r.mul_g(x,z),r.inv_g(y))
O={}
def positive(g): return r.mono(g)
def negative(g): return r.neg(r.mono(g))
T=[[O,O,positive(r.inv_g(v))],
   [negative(r.inv_g(u)),O,positive(r.mul_g(t,r.inv_g(v)))],
   [O,negative(r.inv_g(v)),negative(r.inv_g(v))]]
U=[[positive(r.mul_g(z,r.inv_g(y))),negative(r.inv_g(x)),O],
   [negative(r.inv_g(y)),O,negative(r.inv_g(y))],
   [positive(r.inv_g(y)),O,O]]
I=[[r.E if i==j else {} for j in range(3)] for i in range(3)]
def mm(A,B):
    out=[]
    for row in A:
        outrow=[]
        for j in range(len(B[0])):
            entry={}
            for k in range(len(B)):
                entry=r.add(entry,r.mul(row[k],B[k][j]))
            outrow.append(entry)
        out.append(outrow)
    return out
def encode_matrix(A): return [[r.encode(x) for x in row] for row in A]
old=[[r.sub(positive(s),r.E) for s in [t,u,v]]]
new=[[r.sub(positive(s),r.E) for s in [x,y,z]]]
assert mm(old,T)==new
assert mm(new,U)==old
assert mm(T,U)==mm(U,T)==I

# Chain coordinates are LEFT free module coefficients. partial_1 maps
# row (q_s) to sum q_s(s-1), whereas delta_0 multiplies coefficients
# on the other side because Hom uses the commuting right action.
def partial1_left(vect):
    out={}
    for q,s in zip(vect,r.minus): out=r.add(out,r.mul(q,s))
    return out
boundaries=[]
for i in range(2):
    for j in range(2,4):
        column=[{}, {}, {}, {}]
        column[j]=r.minus[i]
        column[i]=r.neg(r.minus[j])
        residual=partial1_left(column)
        assert residual=={}
        boundaries.append({'cell':[r.g_name(r.G4[i]),r.g_name(r.G4[j])],
                           'partial2':r.encode_vec(column),'partial1_partial2':r.encode(residual)})
wrong=[r.neg(r.minus[1]),r.minus[0],{},{}]
wrongres=partial1_left(wrong)
assert wrongres
print(json.dumps({'scope':'Post-seal comparison; actual integral words, no abelianized substitution.',
    'T_old_to_independent':encode_matrix(T),'U_independent_to_old':encode_matrix(U),
    'T_U':encode_matrix(mm(T,U)),'U_T':encode_matrix(mm(U,T)),
    'M_old_T_equals_M_new':True,'M_new_U_equals_M_old':True,
    'actual_product_tree_chain_boundaries':boundaries,
    'negative_fake_same_factor_2cell_boundary':r.encode_vec(wrong),
    'negative_fake_same_factor_partial1_partial2':r.encode(wrongres)},indent=2,sort_keys=True))
