# Independent falsification audit: finite action locus and full Hecke tuples

Checkpoint: 2026-10-07 04:47 UTC. Completion toward this scoped audit: 100%.
This estimate concerns the present falsification assignment only, not the
Hodge-conjecture claim or the entire research program.

## Scope and verdict

Read the pinned `build/sections/05a-moduli.tex` and the relevant specialization
arguments in `05b-frobenius.tex`, without reading other audit notes. A separate
child audit independently checked the Hecke polarization, marking, and branch
identifications. No external person was contacted.

**No concrete counterexample or substantive gap was found in this scope.**
The strongest checked conclusion is that the stated construction has a coherent
finite-type/finiteness mechanism and that its positive Hecke quotient branches
preserve the entire tuple, including the polarization homomorphism and the
ordered torsion marking. This is a mathematical audit, not a formal-verification
claim. It does not assess the theta construction, Satake calculations, ensuing
CM-source extraction, or the ultimate rational Hodge-conjecture conclusion.

Terminology matters: the source does **not** assert that all CM points form a
finite set. Its finite morphism is the locus of integral `O_E` actions **over the
fixed polarized abelian moduli base** (05a:157–201). The selected CM points used
for ordinary density are isolated only after adding three projector
endomorphisms (05a:320–341).

## Exact claims and hypotheses checked

- `E` is a fixed Galois CM field, `s=[E^+:Q]>=2`, and the universal abelian
  varieties have dimension `3s` (05a:11–17, 95–101).
- The polarization has one fixed elementary-divisor type. The action of
  `O_E` is unital, and its Rosati adjoint is complex conjugation.
- The field of definition contains `E`, so its characteristic-zero action
  algebra splits and the Lie-rank conditions are locally constant
  (05a:114–125, 195–198).
- The principal level is sufficiently deep, and every ordered full
  `N`-torsion basis is allowed, without prescribing a pairing matrix
  (05a:103–110).
- The auxiliary prime is split in the final field and prime to the level,
  polarization degree, and excluded denominators (05a:358–365).

## Finite type and representability: attempts to falsify

### 1. Unbounded endomorphism graphs

The potential obstruction is that integral `O_E` actions on the universal
abelian scheme might have graph Hilbert polynomials of unbounded degree, so a
union of relative Hilbert schemes would not be finite type.

The explicit bound closes this obstruction (05a:157–182). For every chosen
ring generator `b`, let `alpha=1+c(b)b`, and choose a fixed positive integer `m`
with `m/alpha` integral. In each valid action,

`iota(alpha) iota(m/alpha)=[m]`.

Consequently both factors are isogenies, and
`deg(iota(alpha))<=m^(6s)`. The graph of `iota(b)` is isomorphic to the source
abelian variety. The product ample bundle restricts to a bundle inducing
`2 lambda iota(alpha)`, whose polarization degree is at most
`deg(2 lambda)m^(6s)`. Its Hilbert polynomial is
`chi(L)n^(3s)`, with `chi(L)^2=deg(phi_L)`, so only finitely many polynomials
occur. This uses fixed `E`, fixed ring generators, fixed dimension, and fixed
polarization degree; it does not assume the desired finite-type conclusion.

The standard graph-locus step is implicit but substantive enough to check:
within a relative Hilbert scheme, being the graph of a morphism is represented
by requiring the first projection to be an isomorphism; the homomorphism,
finitely presented ring, Rosati, and unital identities are equations between
universal morphisms. There are finitely many generators and relations. This
does not require enumerating infinitely many elements of `O_E`.

The Poincare-bundle identity needed for the bound is supported by Proposition
11.1 of [Edixhoven–van der Geer–Moonen, Chapter XI](https://www.math.ru.nl/~bmoonen/BookAV/PolWp.pdf):
pullback along `(id,lambda)` induces `lambda+lambda^t=2lambda`.

### 2. Failure of properness of the action locus over polarized moduli

The action-locus argument is over the fixed abelian scheme supplied by a DVR
point of the polarized base (05a:184–201), rather than a compactification of
the abelian moduli base. Each generic generator extends uniquely between the
two abelian schemes. Group, ring, and Rosati identities persist by uniqueness.
The graph is still a graph and has the same Hilbert polynomial because it is
the flat source family with the extended line bundle. In characteristic zero,
the `E`-idempotent Lie summands are direct summands of a vector bundle, hence
their ranks remain constant. Thus the extension satisfies the same moduli
conditions.

Infinitesimal rigidity supplies unramifiedness, which entails local
quasi-finiteness. Combined with properness and finite type, this gives a finite
morphism to polarized moduli. No claim that an arbitrary unbounded Hom functor
is proper or finite is being used here.

### 3. Noncompact components or a unitary determinant missed by principal level

The fixed matrices and positivity identify the entire compatible period domain
with one two-ball (05a:203–226). At the other real places, the prescribed
extreme ranks force definite Hermitian forms. A nonzero `E`-isotropic vector
would remain nonzero and isotropic at such a definite place; this is
impossible because `s>=2` (05a:229–235). The special-unitary group is
anisotropic over `E^+`, so the corresponding arithmetic quotient is compact.
The finiteness of the number of components comes from the established finite
type, not from an unproved finiteness of Hermitian forms.

For a possibly nonfree lattice, its top exterior power is a fractional ideal.
A lattice automorphism preserves this ideal, so its determinant is an
`O_E` unit. Unitarity gives `det(g)c(det(g))=1`; every complex conjugate has
absolute value one, and the determinant is a root of unity. A sufficiently
deep congruence level kills the finite group of these roots. This identifies
the reference stabilizer with the principal **special**-unitary level
(05a:243–250), including the nonfree-lattice case.

The compactness and congruence-level tools quoted in the source match
[Milne, Introduction to Shimura Varieties](https://www.jmilne.org/math/xnotes/svi.pdf),
Theorem 3.3 and Proposition 3.5. The arithmetic group here is restriction of
scalars of the indicated unitary group, with compact nonactive real factors.

## Selected CM points and ordinary density

The enhanced isolated-point mechanism (05a:320–341) also survived the scoped
attack. A negative rational `E`-line and an orthogonal diagonalization give
three rational `E`-linear projectors. Integral multiples are endomorphisms at
the selected period. After adding their graphs with the fixed Hilbert
polynomials, rigidity fixes their matrices locally. A line preserved by all
three projectors is a coordinate line, and exactly one coordinate line is
negative at the active place. Thus the selected enhanced point is isolated in
a finite-type scheme over a number field and has algebraic coordinates.

After excluding the projector denominators, these projectors and the split
`O_E tensor Z_q` idempotents cut the `q`-divisible group into height-one pieces
(05a:343–353). This is a finite list of selected points, one on each component;
it does not rely on a uniform assertion that every CM reduction is ordinary.

## Hecke branches, polarization, and marking: affirmative mapping

| Potential obstruction | Checkable mechanism | Source lines |
|---|---|---|
| Wrong opposite kernel or polarization type | If selected exponents are `a_k` and multiplier exponent is `h`, the opposite target exponents are `h-a_k`. Equivalently its lattice is `q^(-h)(L')^dual`. The scaled form is perfect at `q`; at other primes scaling and the isogeny are units, so the original elementary-divisor valuations remain unchanged. | 05a:407–446 |
| Fiberwise polarizations fail to descend over the parameter scheme | For the complementary isogeny `g`, `beta=g^dual lambda g` equals `q^h lambda'` on every geometric fiber. It therefore kills `B'[q^h]`. This torsion scheme is finite etale over the smooth reduced characteristic-zero correspondence base, so vanishing on geometric points is actual vanishing. The fppf quotient by this kernel factors `beta` through `[q^h]`, producing the relative homomorphism. | 05a:448–467 |
| A polarization line bundle has an additional descent obstruction | The tuple stores the polarization homomorphism. The proof descends that homomorphism, for which isotropic descent gives existence and uniqueness; it does not require descending a chosen line bundle. | 05a:444–467 |
| Quotient targets violate action or level conditions | `O_E` stability of the kernel gives a unique descended action. Its Rosati identity follows by cancellation. Since the isogeny has degree prime to `N`, `eta'=f eta` is a full basis. Its pairing matrix may scale by `q^h`, but every matrix is admitted. | 05a:103–110, 469–476 |
| Branch labels identify different kernels by accident | Representatives modulo the left integral subgroup give the same target lattice: `(kg)^(-1)L=g^(-1)L`. The actual subgroup-choice scheme counts kernels as separate branches even if targets are isomorphic. | 05a:403–405, 474–476, 508–519 |
| Negative exponents cannot act algebraically | The central position `(a_k=1,h=2)` is quotient by `B[q]`; identifying the quotient with `B` via `[q]` leaves the action and polarization fixed and sends `eta` to `q eta`. This is a finite-order marking automorphism. Adding its sufficiently large powers clears every exponent into the positive range, and positive convolution makes the extension independent of the clearing power. | 05a:521–533 |

For the polarization issue, Proposition 11.25 of
[Edixhoven–van der Geer–Moonen, Chapter XI](https://www.math.ru.nl/~bmoonen/BookAV/PolWp.pdf)
states the isotropic-kernel criterion for a symmetric isogeny to descend over
an isogeny, with uniqueness and preservation of positivity. This is the
appropriate homomorphism-level criterion.

## Specialization and full-tuple identity

The source's use of properness in 05b:143–161 extends each generic neighbor's
target to the already constructed proper full-tuple model. The isogeny then
extends between the abelian schemes. The polarization identity makes every
fiber map an isogeny. The fixed source and target polarization degrees give
the same degree `q^(3si)` on every fiber, and fiberwise flatness gives a finite
flat extension. Its kernel is the schematic closure of the generic kernel.

Cartier duality transports the annihilator condition under this specialization
(05b:163–172). For equal total kernels and the same multiplier, the quotient
abelian scheme is canonically identified; the action is forced by the quotient
map, the marking is forced by `f eta`, and the polarization is unique because
`f^dual delta f=0` implies `delta=0`. The retained graph coordinates give the
same action point, rather than only an unmarked isomorphism class
(05b:174–179).

The Frobenius marking identity is also consistent. With constant label group
`T=(Z/NZ)^(6s)`, naturality is
`F_B eta=eta^(q) F_T`, and relative Frobenius of the etale constant label group
is the identity on its labels. Hence the transported marking is the twisted
marking (05b:188–213). It acquires no extra multiplication-by-`q` factor. This
does not contradict the central `[q]` position, which uses a different
isogeny and a different identification of its quotient.

## Exact remaining limits of this audit

No route was marked blocked because no central difficulty was transferred to
an equivalent unsupported claim in the inspected construction. The source
could make the graph-locus representability step more explicit and cite the
relative version of the Hom-extension theorem directly; these are exposition
improvements, not identified mathematical defects. I have not independently
reconstructed every cited GIT theorem or its integral-base formulation.
The affirmative conclusion is restricted to the characteristic-zero moduli
construction and the full-tuple specialization mechanism mapped above.
