# Deformation spaces of smooth complete toric varieties: partial results and a precise gap

Problem 30006308, OWR-14299288-014. Status: **unresolved**.

## 1. Scope and conventions

Robins and Ilten's contribution to *Toric Geometry*, Oberwolfach Report 19/2025,
p. 914, asks whether a smooth complete toric variety's deformation space is
recoverable from its tangent cone, and whether component numbers have a relation
to counts of the simplicial complexes encoding first-order deformations.
These are two questions, not a single conjecture with a stated formula.

Throughout, `k` is algebraically closed of characteristic zero. A deformation
space means the formal spectrum of a miniversal hull `R` of `Def_X` at the
undeformed point. Its tangent cone has ring `gr_m(R)`; comparison with the formal
deformation space means completion at the vertex. In particular, a formal
isomorphism `R ≅ completion(gr_m R)` is a sufficient, stronger interpretation of
“determined.” We do not claim that this interpretation is the only meaning of the
question. We settle neither the universal isomorphism assertion nor injectivity
of the tangent-cone invariant on the class of toric deformation hulls.

The main proved partial result is that four natural *numerical counts* of
first-order complexes, even jointly with tangent dimension, do not determine the
number of components. It follows from existing examples; no priority claim is
made. This is not a negative answer to the much broader phrase “any relation.”

Primary references:

- [OWR 19/2025, pp. 912–914](https://ems.press/content/serial-article-files/51856)
- [Ilten–Robins, arXiv:2409.02824v5](https://arxiv.org/abs/2409.02824v5), especially
  §§3.2–3.3, 4.3–4.4, 5.1–5.4, Lemmas 6.3.2–6.3.3, Examples 6.4.2, 6.4.5,
  6.4.6, and Remark 6.4.7.

The hulls below are Ilten–Robins examples. We give the degree, quadratic
obstruction, coordinate-change, and component arguments needed for the partial
result explicitly, instead of treating an abstract or catalogue status as proof.

## 2. An explicit count collision

### 2.1 The varieties and their complexes

Put

`X(e,a,b) = P_{F_e}(O ⊕ O(aF+bH))`,

where `F_e=P_{P^1}(O⊕O(e))`, `e,b≥0`, and `F,H` are the fiber and tautological
classes. These are smooth projective toric threefolds. Their rays are

`n1=(1,0,0), n2=(0,1,0), n3=(-1,e,a), n4=(0,-1,b), n5=(0,0,1), n6=(0,0,-1)`.

The eight maximal cones select one ray from each of `{1,3}`, `{2,4}`, `{5,6}`.
Each determinant is ±1. The projective-bundle construction provides completeness
and projectivity, not merely the determinant test.

For a ray `rho` and a character `u`, let `V_{rho,u}` be the induced subcomplex
on rays `j` satisfying

- `<n_j,u><0` for `j≠rho`;
- `<n_rho,u><-1` for `j=rho`.

The Euler sequence and toric divisor cohomology identify `H^1(T_X)` with the sum
of `reduced H^0(V_{rho,u};k)`. Only pairs with `<n_rho,u>=-1` contribute.
For these splitting fans, the complex is the join of its intersections with the
three opposite pairs. At most one of vertices 5,6 can be selected; a selected
one makes the complex a cone. If at least two opposite-pair intersections are
nonempty, their join is connected. Consequently a contributing complex is
exactly two isolated vertices, either `{1,3}` or `{2,4}`.

Solving the ray inequalities gives the following exhaustive list:

- I: `rho=2, u=(x,-1,0), 1-e≤x≤-1`, support `{1,3}`.
- II: `rho=6, u=(x,y,1), 0≤y≤b, ey+a+1≤x≤-1`, support `{1,3}`.
- III: `rho=5, u=(x,y,-1), 1-b≤y≤-1, 0≤x≤ey-a`, support `{2,4}`.
- IV: `rho=5, u=(x,0,-1), b=0, 1-a≤x≤-1`, support `{1,3}`.

For example, support `{1,3}` with distinguished ray 2 forces `y=-1,z=0`;
`x<0` and `-x-e<0` give I. With distinguished ray 6 it forces `z=1`,
`0≤y≤b`, `x<0`, and `-x+ey+a<0`, giving II. Support `{2,4}` forces
distinguished ray 5, `z=-1`, negative pairings with rays 2,4 and nonnegative
pairings with rays 1,3, giving III. The remaining support `{1,3}` case with
ray 5 gives IV. The opposite primitive relations exclude the other rays.
Every complex listed contributes dimension one.

Choose

`A=X(3,-4,3)` and `B=X(4,-4,3)`.

For A, types I, II, III occur respectively 2, 3, 2 times. For B they occur
3, 3, 1 times. Neither has IV. Thus both have exactly:

- seven contributing ray-character pairs, and `h^1(T)=7`;
- three distinct pairs `(distinguished ray, embedded support)`;
- two distinct embedded supports;
- one abstract isomorphism type of contributing complex, namely two points.

These definitions specify the otherwise ambiguous word “distinct.” We do not
assert that their complete labelled character data, or their support
multiplicities, agree: they do not.

### 2.2 The hull of A, with the necessary computations

Order its tangent degrees as

`u1=(0,-1,-1), u2=(1,-1,-1), u3=(-1,0,1), u4=(-1,-1,0),`
`u5=(-2,0,1), u6=(-2,-1,0), u7=(-3,0,1)`.

The obstruction space has dimension one, in degree `v=(-1,-2,-1)` at ray 5.
Indeed the only complex having first cohomology is the four-cycle on 1,2,3,4;
its ray inequalities are `1-b≤y≤-1`, `ey-a+1≤x≤-1`, `z=-1`.

The complete list of nonnegative expressions for `v` in the `u_i` is

`u1+u4, u2+u6, 2u1+u3, 2u2+u7, u1+u2+u5`.

Here is a finite, exhaustive justification, rather than a guessed cutoff:
`ell=(-2,-2,-1)` is positive on every `u_i`; pairing with `ell` bounds each
exponent by `ell(v)/ell(u_i)`. The script enumerates exactly that bounded box.
Alternatively, the y-coordinate forces exactly two factors from indices
1,2,4,6; the z-coordinate then leaves precisely the quadratic and cubic cases
listed above, and their x-coordinates finish the enumeration.

The graded hull construction of Ilten–Robins therefore gives a single equation

`f=c1 t1 t4+c2 t2 t6+c3 t1²t3+c4 t2²t7+c5 t1 t2 t5`.

The two quadratic coefficients are nonzero. They can be checked directly on the
four cones `(145),(125),(235),(345)`. For a ray-5 direction the chosen 0-cochain
is `c=(0,1,1,0)`; for a ray-2 direction it is `d=(0,0,1,1)`. The quadratic
BCH cochain on an oriented edge `ij` is

`(c_i d_j-c_j d_i)/2 · (rho2(u) f5-rho5(w) f2)`.

For `(u,w)=(u1,u4)` or `(u2,u6)`, the ray evaluations are `rho2(u)=-1`,
`rho5(w)=0`. Summing around the cycle gives `-1` in its one-dimensional first
cohomology. The four-cycle sum kills coboundaries. Thus `c1=c2=-1` with these
choices. No higher coefficient needs to be computed: set

`t4'=-t4+c3 t1 t3+c5 t2 t5`, `t6'=-t6+c4 t2 t7`.

This triangular change is an invertible formal coordinate change, and
`f=t1 t4'+t2 t6'`. Hence

`R_A ≅ k[[t1,t2,t3,t4',t5,t6',t7]]/(t1 t4'+t2 t6')`.

The degree-two form has rank four. A reducible degree-two polynomial is a product
of two linear forms and has rank at most two, so this form is irreducible.
Its polynomial quotient is a domain. Because the equation is homogeneous, the
associated graded ring of `R_A` is that domain. The initial forms of two nonzero
formal elements then have nonzero product, so `R_A` itself is a domain. It has
one irreducible component, of dimension six.

There is a typographical omission in the final hull display on p. 49 of v5:
`t7` is absent there. The preceding seven-variable equation, explicit coordinate
change, tangent dimension seven, dimension-six conclusion, and the OWR display
all retain the seventh variable. Our computation above establishes the required
seven-variable version without adopting that inconsistent display literally.

### 2.3 The hull of B

More generally take `X(e,-e,3)`, `e≥2`, and use degrees

`u1=(0,-1,-1)`, `u_{2k}=(-k,-1,0)`, `u_{2k+1}=(-k,0,1)`

for `1≤k≤e-1`. The obstruction degrees are `v_k=(-k,-2,-1)`.
The y- and z-coordinates force the only expressions

`v_k=u1+u_{2k}=2u1+u_{2k+1}`.

Thus the hull ideal has generators

`g_k=a_k t1 t_{2k}+b_k t1²t_{2k+1}`.

The same cycle computation gives `a_k=-1`. The simultaneous, triangular changes
`t_{2k}'=-t_{2k}+b_k t1 t_{2k+1}` give

`R ≅ k[[t1,...,t_{2e-1}]]/(t1 t2,t1 t4,...,t1 t_{2e-2})`.

With `S` the ambient power series ring,

`(t1 t2,...,t1 t_{2e-2})=(t1) ∩ (t2,t4,...,t_{2e-2})`.

To prove the equality, if `t1 h` belongs to the second ideal, reducing modulo that
ideal shows `h` also belongs to it, since its quotient is a power series domain
in which `t1` is nonzero. Both ideals are prime and neither contains the other.
They are exactly the minimal primes. Their dimensions are `2e-2` and `e`.
For B, `e=4`, giving two components of dimensions six and four.

### 2.4 Consequence and limit

A and B have the same quadruple of counts `(1,2,3,7)` and tangent dimension seven,
but component counts one and two. There is no function of any of these counts,
or of their joint tuple, that always equals the hull's component count.
This does not rule out inequalities, a relation using additional incidence or
character information, or any other suitably specified answer to OWR Question 5.
Both hulls are homogeneous and therefore give no counterexample to Question 4.

## 3. A sufficient equal-weight criterion, and why torus grading alone fails

**Lemma.** Suppose a hull has an equivariant presentation `R=k[[t1,...,tn]]/I`
with a torus grading, and some rational linear functional `ell` takes the same
positive value on every variable's weight. Then R is isomorphic to the completed
local ring of its tangent cone.

**Proof.** Clear denominators to obtain a one-parameter subgroup giving every
variable the same positive integer weight. The ideal is invariant. In every
finite jet, projection to weight spaces preserves its image (a torus is linearly
reductive). Passing to the inverse limit, each ordinary homogeneous component of
every element of I lies in I. Thus I is the closed ideal generated by homogeneous
polynomials. Let J be this homogeneous ideal in `k[t1,...,tn]`. Then
`R=k[[t]]/Jk[[t]]`, `gr_m R=k[t]/J`, and completing the latter gives R. ∎

The criterion need not apply even in a published example. For the four degrees

`u1=(0,-1,-1), u2=(1,-1,-1), u3=(0,-2,-1), u4=(-1,0,1)`,

one has `u3=u1+u2+u4`. Equal positive weights would imply `c=3c`, impossible.
The known hull is nevertheless conical: the identity

`t3²t4-2t1t2t3t4²+t1²t2²t4³ = t4(t3-t1t2t4)²`

provides the required coordinate change. A mixed-degree *presentation* is not a
counterexample. Conversely, unequal positive weights do not suffice.

## 4. A countermodel to the proposed shortcut, not to the toric question

Keep the four weights above. Let

`R_* = k[[t1,t2,t3,t4]] / ( t4(t3²-t1²t2²t4²) )`.

Both terms have weight `2u3+u4`, and `ell=(-2,-2,-1)` is strictly positive on all
four weights. The equation vanishes on each coordinate axis; hence each
one-dimensional weight tangent direction extends to a formal one-parameter arc.
Nevertheless R_* is not formally isomorphic to its tangent cone.

Indeed, its defining equation is the product of the three distinct prime
elements

`t4`, `t3-t1t2t4`, `t3+t1t2t4`.

Each quotient is a power series domain, and the factors are nonassociate in
characteristic zero. Since the ambient power series ring is a UFD, the ideal of
their product is the intersection of their prime ideals, hence is radical.
R_* is reduced and has three minimal primes.

The initial form of the equation is `t3²t4`. The initial ideal of a principal
ideal in a power series ring is generated by the initial form: orders add and
initial forms multiply. Thus

`gr_m R_* = k[t1,t2,t3,t4]/(t3²t4)`.

Its completion is nonreduced: the nonzero class of `t3t4` squares to zero.
Its two minimal primes are `(t3)` and `(t4)`. Reducedness already forbids the
claimed isomorphism.

This establishes a real limitation of the shortcut “torus action plus integration
of all weight directions implies conicality.” **No smooth complete toric variety
with hull R_* has been constructed here.** It is therefore not a counterexample
to Question 4. In the corresponding published example the actual coefficients
have the square relation that makes the ring conical, rather than the coefficients
chosen for this countermodel.

## 5. A genuine resonant toric candidate and the remaining computation

Consider `C=X(2,-4,4)`. The first-order variables, rays, and degrees can be labelled

- ray 2: `x=(-1,-1,0)`;
- ray 6: `a=(-3,0,1), b=(-2,0,1), c=(-1,0,1), d=(-1,1,1)`;
- ray 5: `y=(0,-2,-1), p=(0,-1,-1), q=(1,-1,-1), r=(2,-1,-1)`.

Thus `h^1(T_C)=9`. The obstruction space is one-dimensional of degree
`v=(-1,-3,-1)` at ray 5. The only degree-v quadratic monomial is `xy`.
The cycle formula from §2 gives coefficient `-2`, because now the ray-2
evaluation on the ray-5 degree y is `-2`. Consequently the hull is a hypersurface

`k[[x,a,b,c,d,y,p,q,r]]/(F)`, with `F=-2xy+terms of ordinary order ≥3`.

This assertion is an application of the one-dimensional obstruction-space hull
construction, not a claim that we computed the higher terms.

The degree relation `deg(d)+deg(q)=0` shows why no positive functional can bound
all weight-compatible monomials. For instance `xy(dq)^n` has degree v for every
n. Such multiples alone are not evidence of essential higher obstructions: unit
multiples of an equation can be removed. More relevantly, `c²p²q` has degree v
and involves neither x nor y. Its ordinary degree is five, so weight restrictions
permit a residual term surviving the first quadratic-pair elimination.

For precision, the formal splitting lemma with parameters transforms F, after
an invertible coordinate change, into `XY+G(a,b,c,d,p,q,r)` with `G` of order at
least three. One proof is to solve `F_x=F_y=0` for x,y as series in the other
variables by the formal implicit function theorem; the 2×2 Hessian block is
invertible. Shift to that critical point, then recursively remove all terms
involving X,Y of order at least three by changes of X,Y, using the nondegenerate
quadratic block. Completeness makes the recursive changes converge m-adically.
The constant part in X,Y is the residual series G.

**Exact gap:** no calculation here determines whether this G vanishes, or even
the coefficient of the permitted residual quintic after all required coordinate
changes. Computing a raw quintic coefficient before eliminating the quadratic
pair would not suffice. Vanishing at finitely many orders also does not prove
G=0 without a termination or structural argument. Conversely an actual nonzero
G, with a proved invariant distinguishing the hull from its tangent cone, could
supply a toric counterexample, but neither step is established here.

This concrete gap coexists with the broader gap: a universal result would require
an all-order elimination theorem for every smooth complete fan, or a certified
counterexample fan and its full relevant hull/invariant. The calculations and
partial count collision above do not fill it.
