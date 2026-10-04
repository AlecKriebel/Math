# Independent adversarial audit: problem 30006308

Audit date: 2026-10-04 UTC. Problem code: OWR-14299288-014. Rank: 555.

## Verdict

**PASS for publication as an unresolved research packet, with the stated scope limits.**
No blocking mathematical error was found in the frozen packet. The proposed
`unsolved`, `5/5` disposition is appropriate: five distinct mathematical approaches
are documented, but neither broad question is solved. This does not certify five
historical sessions, universal current-open status, or novelty.

The numerical non-determination result is valid. The published varieties
`A=X(3,-4,3)` and `B=X(4,-4,3)` have the same four specified first-order counts
`(1,2,3,7)` and tangent dimension seven, whereas their hull rings have respectively
one and two minimal primes. The comparison is a consequence of existing examples,
not a new pair of toric examples and not an answer to every possible relationship
in Question 5.

The seven-variable equation for A, including its free `t7`, is justified by an
invertible coordinate change. The resonant candidate `X(2,-4,4)` has the verified
quadratic coefficient `-2`, but its normalized higher residual series is still
unknown. Neither it nor the auxiliary formal countermodel is promoted to a
counterexample to the toric question.

## 1. Frozen input and audit boundary

The exact reviewed input is bound by `../public/FROZEN_MANIFEST.json`, SHA-256

`a4087c4f62929196749da8c9d1925792be34b714719c7cb4469fa32b997b0c2c`.

All six payload entries in that manifest matched both byte length and SHA-256;
with the manifest itself, the frozen directory contains seven files. The original
verification script ran successfully, and its new output was byte-for-byte equal
to the saved output. No frozen file was changed. No repository or remote state
was changed.

This audit adds its own exact replay and explanations. The replay imports none
of the original verification functions. In particular, it derives the complete
finite cohomology lists from the induced complexes and inequalities, instead of
assuming the four family formulas implemented by the original script.

The audit is deliberately bounded. It does not independently rerun all ancillary
Macaulay2 computations, prove every external foundational theorem, recertify the
repository-history search, certify a complete literature search, or calculate the
candidate's higher hull. Those limitations are not gaps in the specific count
collision proved below.

## 2. Primary-source scope and equation inspection

The primary problem is [Oberwolfach Report 19/2025, printed p. 914](https://ems.press/content/serial-article-files/51856).
Its fourth question concerns recovery of the deformation space from its tangent
cone. The fifth asks whether component counts and counts of first-order complexes
are related. It supplies neither a numerical formula nor an equivalence relation
for counting complexes. The page immediately preceding the questions supplies the
three illustrative hulls. The page image was inspected: the cubic displayed there
has the square of `t3`, and the rank-four quadratic hull has seven variables.

The current proof source used here is [Ilten–Robins, arXiv:2409.02824v5](https://arxiv.org/abs/2409.02824v5),
revised 13 May 2026. The public arXiv version page was checked independently. The
following proof chain was inspected in the full paper:

- §§3.2–3.3, Proposition 3.2.4, Theorem 3.3.1, and Appendix B: the iterative
  obstruction construction, its limit, and the versality argument;
- §§4.3–4.4, including the divisor-cohomology comparison and the vanishing when
  the distinguished ray pairing differs from `-1`;
- Theorems 5.1.2 and 5.1.4, including the bracket and deformation-functor
  comparison, and Proposition 5.2.1;
- Example 5.4.2, Theorem 5.4.4 and its proof, and the four-cone reduction;
- Lemmas 6.3.2–6.3.3 and their proofs; Lemma 6.4.1; the relevant complete
  equations, changes of variables, and tables in Examples 6.4.2, 6.4.5 and 6.4.6;
  and Remark 6.4.7.

This verifies the applicability of the obstruction-space presentation, rather
than inferring a hull from its tangent dimensions alone. Smoothness makes the
locally trivial deformation functor sufficient here. Completeness provides the
required positive-degree structure-sheaf cohomology vanishings. The graded
construction permits generators indexed by the obstruction basis, with monomials
of the corresponding lattice degrees. Positive scalar weights make the two
finite degree-support arguments genuinely all-order arguments.

The source PDFs inspected had SHA-256 values:

- OWR 19/2025: `0511e00aa5e3c1b778f66f0e5b8fb00ab02b1103550bbd7941e2bd0c1bb62442`
- Ilten–Robins v5: `dd193430943321bff78810f8ea07ffee03cd47f0154167275f5de3225ab6002f`

No source PDF, page image, extracted text, corpus, or tool transcript is part of
this audit's publication payload.

## 3. Independent fan and parameter check

The parameter convention is fixed by `H=O_{F_e}(1)`, with `H^2=e`, and by the
six explicit rays. This matters: replacing `H` by the negative section would
change the apparent parameters. The packet uses the same convention as the
source.

There is also a direct projectivity certificate that avoids relying only on the
projective-bundle identification. For `e,b >= 0`, put `A0=1+max(0,-a)` and consider

`0 <= z <= 1`,
`0 <= y <= 1+b z`,
`0 <= x <= A0+e y+a z`.

Every interval has strictly positive width, including its endpoints. This is a
bounded integral polytope with exactly eight vertices: choose an endpoint of z,
then an endpoint of y, then an endpoint of x. Its inward facet normals are the
six rays in the packet. At each vertex, exactly one facet from each opposite
pair is active. Thus its normal fan has exactly the stated eight maximal cones,
and is complete and projective. The exact replay verifies all active facets and
strictly positive remaining slacks for A, B and the candidate.

Each maximal-cone determinant is `+1` or `-1`, as independently checked. Hence
these are smooth projective toric threefolds. Smooth determinants alone would
not have established completeness or projectivity; the polytope does.

## 4. Exhaustive first- and second-order cohomology

The fan complex is the join of the three two-element discrete complexes. If one
of the fiber vertices 5 or 6 belongs to an induced complex and the other does
not, the induced complex is a cone. Both cannot occur together because their
pairings are opposites, including the distinguished-ray threshold. Therefore a
complex contributing reduced H0 or H1 contains neither fiber vertex.

The independent replay computes boundary ranks for every induced subcomplex on
vertices 1,2,3,4. Only these cases contribute:

- `{1,3}`: two isolated vertices, reduced H0 dimension one;
- `{2,4}`: two isolated vertices, reduced H0 dimension one;
- `{1,2,3,4}`: a four-cycle, H1 dimension one.

Only distinguished ray-degree pairs with pairing `-1` need be considered, by the
cohomology comparison. With no selected fiber vertex, `z` must be `0` for rays
1–4, `-1` for ray 5, or `1` for ray 6. For each of the six rays and each of the
three support patterns, the replay solves all remaining exact integer
inequalities using two-dimensional Fourier–Motzkin elimination. It does not
use a guessed coordinate cutoff. The elimination yields a bounded interval for
x and a bounded interval for y at each x, or proves infeasibility.

The finite lists thus follow without importing the packet's family formulas.
The general four-family classification can also be checked directly: support
`{1,3}` at ray 2 forces `y=-1,z=0` and `1-e<=x<=-1`; at ray 6 it forces
`z=1`, `0<=y<=b`, and `ey+a+1<=x<=-1`; at ray 5 it forces `z=-1`, `y=0`,
`b=0`, and `1-a<=x<=-1`. Support `{2,4}` can occur only at ray 5, with
`z=-1`, `1-b<=y<=-1`, and `0<=x<=ey-a`. The other choices contradict either
an opposite-pair inequality or exclusion of the distinguished ray. This also
checks the `b=0` exception, which is absent from the three numerical examples.
For those examples the replay yields:

- A: seven first-order pairs, with family sizes `2,3,2`; one second-order
  obstruction pair, at ray 5 and degree `(-1,-2,-1)`;
- B: seven first-order pairs, with family sizes `3,3,1`; three obstruction
  pairs, at ray 5 and degrees `(-k,-2,-1)`, `k=1,2,3`;
- C: nine first-order pairs; one obstruction pair, at ray 5 and degree
  `(-1,-3,-1)`.

For both A and B the abstract type is exactly two points, the embedded support
count is two, the distinguished-ray/support count is three, and the
ray/character count is seven. The complete lists agree with the frozen lists.
The support multiplicities differ (`5+2` versus `6+1`) and the character data
differ. The packet correctly does not claim either stronger equality.

## 5. Quadratic coefficients and the four-cone cover

The four cones are `(145),(125),(235),(345)`, in that cyclic order. On their nerve,
use cochains `c=(0,1,1,0)` for the selected ray-5 direction and
`d=(0,0,1,1)` for a ray-2 direction. They are the characteristic functions of the
specified connected components in the first-order complexes.

For two direction sections, the Euler-sheaf bracket is

`[chi^u f_r, chi^w f_s] = r(w) chi^(u+w) f_s - s(u) chi^(u+w) f_r`.

The second-order part of `BCH(-alpha_i,alpha_j)` is minus one half of this
bracket. Summing the resulting four oriented edge values kills coboundaries and
reads the single four-cycle cohomology class. The replay constructs these
six-component bracket vectors and edge values independently.

For each quadratic monomial required in A and B, the nonzero ray-5 edge values
are `-1/2,-1/2`, with sum `-1`. For C, the relevant evaluation is `-2`, so the
nonzero edge values are `-1,-1`, with sum `-2`. The entire second-order normal
form is not inferred from a nonzero raw edge: it is its nonzero cycle class that
certifies the obstruction. The source reduction theorem justifies using this
four-cone cover, and the original proof's signs match the selected conventions.

## 6. A: the omitted variable is retained by proof

For the ordered seven tangent degrees in the packet, the functional
`ell=(-2,-2,-1)` takes strictly positive values. Pairing with the obstruction
degree bounds every exponent. Independent exhaustive enumeration gives exactly
five compatible monomials: the two quadratics and three cubics displayed in the
packet. No unexamined higher-order monomial can occur in the homogeneous
obstruction generator.

The one-dimensional obstruction-space construction and the nonzero quadratic
class give the equation

`f=-t1 t4-t2 t6+c3 t1^2 t3+c4 t2^2 t7+c5 t1 t2 t5`.

Leave `t1,t2,t3,t5,t7` fixed and replace

`t4` by `-t4+c3 t1 t3+c5 t2 t5`,
`t6` by `-t6+c4 t2 t7`.

This is a triangular automorphism; applying it twice is the identity. Its
Jacobian determinant is one. Exact expansion gives the rank-four quadric
`t1 t4'+t2 t6'`. In particular, it cannot eliminate the independent variable
`t7`. There are three free variables and one equation in seven variables.

The v5 p. 49 image was inspected. Its last displayed ring omits `t7`, while its
preceding ring, coordinate change, and table include it. Reading that last ring
literally would give embedding dimension six and Krull dimension five, contrary
to the independently established embedding dimension seven and the page's
six-dimensional geometric description. The OWR display also retains seven
variables. The packet's correction is therefore supported by algebra, not merely
an assumption that an inconvenient display is a typo.

The quadratic has rank four. A reducible quadratic is a product of linear forms
and has rank at most two, so this polynomial is irreducible and its polynomial
quotient is a domain. The completed homogeneous quotient has that domain as its
associated graded ring; multiplication of nonzero initial forms proves the
completion is a domain as well. Thus A has one hull component, of dimension six.

## 7. B: components are not removed by saturation

For `X(e,-e,3)`, the y- and z-coordinate equations already force every monomial
of obstruction degree `(-k,-2,-1)` to be one of

`t1 t_(2k)` or `t1^2 t_(2k+1)`.

Indeed, the number of negative-y factors is two, while the z equation forces
either one ray-5 factor and one ray-2 factor, or two ray-5 factors and one ray-6
factor. The x equation fixes the index k. This proves exhaustiveness for every
`e>=2`; the replay additionally enumerates the three degrees needed for B.

The nonzero quadratic coefficients permit simultaneous triangular changes,
leaving the ideal

`I=(t1 t2,t1 t4,t1 t6)` for B.

In the power series ring S,

`I=(t1) intersection (t2,t4,t6)`.

For the reverse inclusion, write an element as `t1 h` and reduce modulo
`(t2,t4,t6)`. The quotient is a domain in which `t1` is nonzero, so the image of
h is zero. Both ideals are prime, incomparable, and minimal over I. The equality
also proves reducedness; there is no hidden embedded component contributing to
the count. Their dimensions are six and four.

The independent replay verifies the analogous polynomial intersection by an
elimination Gröbner basis, while the preceding argument establishes the formal
power-series equality. No saturation is used. In particular, saturating by `t1`
would discard a genuine component and would be an invalid replacement for this
calculation.

## 8. Equal weights and the auxiliary countermodel

The equal-positive-weight criterion is correct under its stated equivariant
presentation hypothesis. In finite jets a torus representation splits into
weight spaces. If all variables have a common positive scalar weight, ordinary
degrees are precisely these scalar weights. Each homogeneous piece of an
invariant ideal is therefore in the ideal modulo every jet. Closedness of ideals
in the complete Noetherian ring places the piece in the ideal itself. The ideal
is the completion of a homogeneous polynomial ideal, which proves the asserted
isomorphism with the completed tangent cone.

That argument is conditional: the packet neither proves that every toric hull
admits equal weights nor confuses arbitrary positive weights with equal weights.
The displayed lattice relation excludes equal positive weights in the chosen
four-variable example. The known equation nevertheless becomes homogeneous by
an invertible triangular change. Thus a mixed-degree presentation alone has no
force against Question 4.

The auxiliary ring factors into the three distinct prime elements

`t4`, `t3-t1 t2 t4`, `t3+t1 t2 t4`.

Each quotient is a power series domain. Unique factorization shows their product
ideal is the intersection of their principal prime ideals, hence radical. The
initial ideal is generated by `t3^2 t4`: for a principal ideal, orders add and
initial forms multiply. Its completed quotient is nonreduced, witnessed by the
nonzero nilpotent class of `t3 t4`. This correctly prevents a formal isomorphism.
Its three components versus the cone's two also distinguish them.

The torus weights are distinct, the equation is weight homogeneous, and each
coordinate axis gives a formal arc. Consequently the example does refute the
proposed implication from these formal properties alone. It does **not** supply
a smooth complete toric variety with that hull. Such a realization is neither
constructed nor supplied by a theorem in the packet.

## 9. C: verified finite data and an uncomputed residual

The independently recovered nine tangent directions agree exactly with the
packet. Enumeration of every unordered quadratic pair gives only `xy` in the
obstruction degree, and its cycle coefficient is `-2`. Since there is one
obstruction basis element, the hull is a hypersurface with that initial form.

The zero-weight pair `dq` and the allowed residual monomial `c^2 p^2 q` both pass
exact lattice-degree checks. The first permits infinitely many compatible terms;
it does not show that any of them is nonzero or essential. Terms proportional
to a hull generator, or removable by a coordinate change, carry no independent
nonconicality information.

The formal splitting argument is applicable: the x,y Hessian block is invertible
in characteristic zero. Solve the two derivative equations for the critical
point in x,y, translate, and eliminate remaining mixed terms in successively
higher adic orders. This yields `XY+G` in the other seven parameters. The process
is a formal argument, not a proof that the infinite residual is zero.

No raw coefficient of the permitted quintic, no normalized quintic coefficient,
and no all-order residual series were computed by this audit. A vanishing finite
jet would not settle the all-order question. The packet states this limitation
correctly and should retain it unchanged.

## 10. What the result does and does not establish

The pair A,B rules out a function of any one of the four counts, or their joint
tuple even with tangent dimension, that always returns the number of hull
components. It does not rule out inequalities or richer combinatorial relations.
Its two tangent cones are different: both rings are conical, and the cones
already have different component counts. It is therefore not a pair with the
same tangent cone and different hulls.

Question 4 also distinguishes two possible meanings: being isomorphic to one's
completed tangent cone, and being recoverable in some other sense from that
invariant. The packet identifies this distinction rather than silently treating
the meanings as equivalent. For component counts, the intended formal-germ
convention is the minimal-prime count of the hull ring, as in the cited source.

The five approaches and their gaps are substantive and adequately separated.
No change from the proposed unresolved status is justified. No blocking revision
to the frozen mathematical packet is requested.

## Reproduction

Run `python independent_replay.py` with Python 3 and SymPy. The saved
`independent_results.json` is an actual successful run. The original script's
separate replay is saved as `frozen_replay_results.json`.

The script checks frozen integrity, exact fan certificates, exhaustive finite
cohomology lists, finite monomial supports, quadratic cocycles, coordinate-change
inverses, and ideal-intersection identities. Its success is supporting exact
arithmetic, not a substitute for the mathematical arguments or an all-order
candidate computation. `AUDIT_MANIFEST.json` hashes these audit deliverables and
records the binding to the unchanged frozen input.
