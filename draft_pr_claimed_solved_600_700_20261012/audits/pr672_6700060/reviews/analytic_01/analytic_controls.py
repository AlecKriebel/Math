#!/usr/bin/env python3
"""Independent finite diagnostics; not a certificate of PDE/index theory."""
import json
from itertools import combinations, product
import sympy as s

checks = []

def require(label, condition, details=None):
    if not bool(condition):
        raise ValueError(label)
    checks.append({'label': label, 'passed': True, 'details': details})

I = s.I
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -I], [I, 0]])
Z = s.diag(1, -1)
eye = s.eye
kron = s.kronecker_product

def gamma(n):
    if n == 3:
        return [-I * X, -I * Y, -I * Z]
    gs = [kron(X, eye(2)), kron(Y, eye(2)), kron(Z, X), kron(Z, Y)]
    if n == 5:
        gs.append(kron(Z, Z))
    return [-I * a for a in gs]

def hom_matrix(left, right):
    """A -> left A right, using column-major vectorization."""
    return kron(right.T, left)

for n in [3, 4, 5]:
    cs = gamma(n)
    m = cs[0].rows
    zero = s.zeros(m)
    for j, c in enumerate(cs):
        require(f'n{n}_skew_{j}', c.conjugate().T == -c)
        for k, d in enumerate(cs):
            require(f'n{n}_clifford_{j}_{k}', c*d+d*c == (-2*eye(m) if j == k else zero))
    anti = s.Matrix.vstack(*[hom_matrix(c, eye(m)) + hom_matrix(eye(m), c) for c in cs])
    expected_nullity = 0 if n % 2 else 1
    require(f'n{n}_anticommutant_nullity', m*m-anti.rank() == expected_nullity,
            {'nullity': m*m-anti.rank()})
    comm = s.Matrix.vstack(*[hom_matrix(c, eye(m)) - hom_matrix(eye(m), c) for c in cs])
    require(f'n{n}_commutant_scalars', m*m-comm.rank() == 1)
    bivectors = s.Matrix.hstack(*[s.Matrix(cs[a]*cs[b]).reshape(m*m,1) for a,b in combinations(range(n),2)])
    require(f'n{n}_spin_bivectors_independent', bivectors.rank() == n*(n-1)//2)
    if n % 2:
        volume = eye(m)
        for c in cs:
            volume *= c
        require(f'n{n}_volume_scalar_nonzero', volume != zero and volume == volume[0,0]*eye(m))

cs = gamma(3)
nu = cs[2]
xi = cs[0]
L = hom_matrix(I*nu*xi, eye(2))
for j, eta in enumerate([s.Matrix([0,0,1]), s.Matrix([s.Rational(3,5),0,s.Rational(4,5)]),
                          s.Matrix([s.Rational(2,3),s.Rational(2,3),s.Rational(1,3)])]):
    omega_eta = sum((eta[k]*cs[k] for k in range(3)), s.zeros(2))
    chi = (-hom_matrix(nu, omega_eta)).applyfunc(s.expand)
    require(f'boundary{j}_chi_involution', (chi*chi-eye(4)).applyfunc(s.simplify) == s.zeros(4))
    require(f'boundary{j}_chi_selfadjoint', chi.conjugate().T == chi)
    require(f'boundary{j}_symbol_involution', L*L == eye(4))
    require(f'boundary{j}_symbol_anticommutes', (L*chi+chi*L).applyfunc(s.simplify) == s.zeros(4))
    require(f'boundary{j}_half_target', (eye(4)-chi).rank() == 2)
    require(f'boundary{j}_no_decaying_plus_intersection',
            s.Matrix.vstack(L-eye(4), chi-eye(4)).rank() == 4)
flat_chi = -hom_matrix(cs[2],cs[2])
identity_vec = s.Matrix([1,0,0,1])
require('flat_identity_plus_convention', flat_chi*identity_vec == identity_vec)
require('normal_commutes_chi_for_adjoint_boundary',
        hom_matrix(cs[2],eye(2))*flat_chi == flat_chi*hom_matrix(cs[2],eye(2)))

# Exact transverse integrals for delta=2^{-k}, including adverse controls.
for k in [2,3,5,10,20]:
    delta = s.Rational(1,2)**k
    length = k*s.log(2)
    logarithmic_squared_L2 = 2*s.pi*s.log(delta/delta**2)/length**2
    require(f'log_weight_k{k}', s.simplify(logarithmic_squared_L2-2*s.pi/length) == 0)
    ordinary_squared_L2 = s.pi*(delta**2-(delta/2)**2)/delta**2
    require(f'ordinary_cutoff_nonvanishing_k{k}', ordinary_squared_L2 == 3*s.pi/4)
    codim_two_squared_L2 = 2*(1/delta**2-1/delta)/length**2
    require(f'codim_two_wrong_dimension_k{k}', codim_two_squared_L2 > 0,
            {'exact_integral': str(codim_two_squared_L2)})
    require(f'rounding_displacement_separation_k{k}', delta**4/delta**2 == delta**2)

# Irredundant nonsimple octahedron: four facets incident at each vertex,
# yet no three contain a ridge. Its six vertices supply exact face tests.
normals = [s.Matrix(v) for v in product([-1,1],repeat=3)]
vertices = [sign*eye(3)[:,j] for sign in [-1,1] for j in range(3)]
for j,v in enumerate(vertices):
    active = [q for q,N in enumerate(normals) if (N.dot(v)) == 1]
    require(f'octahedron_vertex{j}_nonsimple',len(active)==4)
    for tri in combinations(active,3):
        rank = s.Matrix.vstack(*[normals[q].T for q in tri]).rank()
        require(f'octahedron_vertex{j}_triple{tri}_codim3',rank==3)

# Redundant inequalities destroy the codimension-three assertion: the
# cube's x<=1, y<=1 and x+y<=2 all contain the same codimension-two ridge.
redundant_normals = s.Matrix([[1,0,0],[0,1,0],[1,1,0]])
require('irredundancy_is_essential', redundant_normals.rank()==2)

# Absorption coefficient and the exact strong-L2 mass estimate algebra.
eps=s.symbols('eps',positive=True)
E=s.symbols('E',nonnegative=True)
require('energy_absorption_algebra', s.simplify((1-eps/2)*(eps/(2-eps))-eps/2)==0)
for denominator in [4,8,16,32]:
    e=s.Rational(1,denominator)
    require(f'energy_bound_epsilon_{denominator}',0 < e/(2-e) < e)

print(json.dumps({'schema':'pr672-analytic-controls-v1','scope':'finite exact diagnostics only; no PDE/index certification',
                  'count':len(checks),'passed':True,'checks':checks},indent=2,sort_keys=True))
