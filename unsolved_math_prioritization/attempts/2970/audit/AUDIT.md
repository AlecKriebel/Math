# Independent acceptance audit: KP-4.94 / 2970

Date: 2026-10-08. Assessment: accept the frozen report as a carefully bounded partial/unresolved mathematical investigation, with a nonblocking executable-hardening recommendation below. No positive or negative answer to either requested equivalence has been established for any odd r >= 3. The approach count remains five; this audit adds no approach.

## 1. Exact frozen input and result

The audited candidate has nine public files totaling 67,843 bytes. Its `MANIFEST.sha256` has SHA-256:

`a8cd4866d04bba62d53083e3e3f353e90974d955f09218f59244687f6d9152e4`.

Every listed digest was recomputed. Every candidate file was rehashed after testing; all bytes remain unchanged. The audit independently inspected the complete authored report, accompanying source audit, executable, saved result, approach ledger, and bibliographic manifest. It did not modify the candidate, publish anything, or change a queue.

The following distinctions are indispensable to acceptance:

1. The pullback lattice is a marking. Its saturation index is not shown to be an invariant of the unmarked smooth manifold.
2. The characteristic-fiber argument excludes maps identifying the displayed fiber classes. It excludes no arbitrary diffeomorphism.
3. The Lagrangian-sphere span identification remains an explicit hypothesis.
4. The finite example is in PSL(2,F_3), using its SL(2,F_3) central extension. It is not a computed quotient of the Horikawa monodromy.
5. The sphere result is a smooth representability statement; it is not a canonical-symplectic representability theorem.
6. The even-r degeneration counterexample refutes a general inference but lies outside KP-4.94's homotopy-equivalent range.
7. The normal log-canonical bridge at r=3 does not supply the missing diffeomorphism or symplectomorphism.

## 2. Target and numerical identities

The normalization matches K3 Problem 4.94: X_r is the smooth double cover of F_0 with branch class 6s+4rf; Y_r is the double cover of F_(2r) with branch components Delta_infinity and a smooth member of |5Delta_0|. Here Delta_0=Delta_infinity+2rf. The relevant general-type pair has odd r >= 3. The case r=1 is not a minimal general-type pair of the required kind; even r has different intersection-form parity.

The double-cover formulas independently give

- K_X = U+(2r-2)V;
- K_Y = 2R+(3r-2)F;
- K^2=8r-8, chi(O)=4r-1, p_g=4r-2;
- e=40r-4, signature=-24r;
- b2+=8r-3 and b2-=32r-3.

For example, on F_(2r), using the negative-section/fiber basis, the half-branch class is (3,5r), the base canonical class is (-2,-2r-2), and their sum is (1,3r-2). Pulling back gives the displayed K_Y and square 8r-8. The Euler characteristics were also recomputed from the topology of a branched double cover, independently of Noether's formula. The branch genera are 20r-5 on X_r and 20r-4 for Y_r's positive component, in addition to its rational component.

The nonzero common signature rules out an orientation-reversing diffeomorphism. Canonical symplectic forms are compared with the same normalization [omega]=c1(K); independent rescaling or uniqueness of all forms in that class is not assumed. Catanese's deformation-invariance theorem supports this canonical comparison, with the singular-fiber qualifications discussed below.

## 3. Integral marking and characteristic fiber

The proof that Lambda_X is primitive is valid, rather than just a mod-two calculation. In the nodal-grid model, six horizontal sections and 4r vertical fibers give 24r transverse branch crossings. Blowing up these crossings makes the branch components disjoint. The smooth double cover of that blown-up base is the simultaneous-resolution model of the nodal cover.

The two chosen ramification curves have pairings b and a with aU+bV. Consequently, any rational combination of U,V lying in integral cohomology has integral coefficients. Simultaneous resolution identifies the underlying smooth manifolds and the pullback base classes with those on a smoothing. This identifies precisely the primitive U(2) summand claimed in the report; there is no inference that an arbitrary diffeomorphism must preserve it.

On Y_r, the negative section is a branch component, so its total pullback is 2R. Thus the unsaturated lattice has Gram matrix [[-4r,2],[2,0]], while the lattice on R,F has matrix [[-r,1],[1,0]]. The latter determinant is -1. The elementary integral orthogonal-projection argument proves that this unimodular sublattice is primitive and an integral direct summand. Therefore it is the saturation and has index two over Lambda_Y. Both unsaturated pullback lattices have determinant -4; substituting the unsaturated Y lattice in the discriminant argument would lose the obstruction.

Primitivity of Lambda_X makes K_X primitive. The direct-summand property makes the divisibility of K_Y exactly gcd(2,3r-2). Reduction modulo two then gives X_r non-spin for every r, and Y_r spin precisely for even r. For odd r, F is characteristic, whereas V is not: K_X is congruent to U and primitivity prevents U+V from vanishing modulo two. This is a valid obstruction to identifying V and F, without any assumption that an arbitrary map preserves a chosen genus-two fibration.

The deck-involution distinction is likewise correctly marked. The fixed loci have one versus two components. Equal Euler characteristics do not remove this distinction; conversely, nonconjugate covering involutions do not prove the underlying manifolds inequivalent.

## 4. Conditional Lagrangian-span obstruction

For an embedded Lagrangian sphere A, its normal orientation gives A^2=-2, and normalization [omega]=K gives K.A=0. Those two necessary numerical constraints do not characterize which integral classes occur as embedded Lagrangian spheres.

Let E be the rational span of all such sphere classes. If E(X)=N_X tensor Q and E(Y)=N_Y tensor Q, a symplectomorphism identifies the two rational subspaces and hence their intersections with integral cohomology. Orthogonal complements of integral sublattices are saturated, so these intersections are exactly N_X and N_Y.

For a primitive nondegenerate sublattice M of a unimodular lattice L, restriction of the pairing maps L onto M*: primitivity makes L/M free, so any integral functional on M extends to L, and unimodularity represents the extension. The kernel is M-perpendicular. Reducing by M shows that [L:M plus M-perpendicular]=|det M|. Applying the same reasoning to the primitive complement gives equality of absolute discriminants. Thus the required complements have discriminants 4 and 1 and cannot be integrally isometric.

This proves the conditional implication, not the antecedent. The report does not replace all Lagrangian spheres with algebraic vanishing cycles, immersed spheres, or relations among Dehn twists. Its geometric missing hypothesis remains genuinely open within this investigation.

## 5. Finite partial-conjugation example and pencil scope

The displayed matrices A,B generate all 24 elements of SL(2,F_3). Their projective actions on the four points of P^1(F_3) give the full alternating group A_4, with kernel {I,-I}. The quotient group therefore has order 12. The displayed P lies in the same generated group, and C=AB satisfies C^2=P^2=-I and PCP^(-1)=-C.

Both quotient tuples multiply to identity, have order-three entries, and generate the same A_4; the unchanged last two factors alone already generate it. Each order-three element downstairs has exactly one order-three lift upstairs. Hurwitz moves preserve the product of these distinguished lifts, and simultaneous conjugation fixes it when it is central. The two products are I and -I. This is a complete mathematical obstruction to Hurwitz-and-inner-conjugation equivalence for this finite example.

The independent executable uses permutations of P^1(F_3), rather than the candidate's canonical matrix representatives. It enumerates all determinant-one matrices, checks the projective homomorphism on every pair, and constructs the complete braid orbits using the two global-conjugation generators. It then verifies closure under every element of A_4 and both braid directions. The results are exactly 216 and 144, disjoint. Every tuple retains identity product, full generated group, order-three factors, and its prescribed central lift product. A separate exhaustive enumeration shows that the two orbits together exhaust all 360 generating identity quadruples with the relevant two-per-conjugacy-class multiset.

None of this realizes a quotient of the actual genus-17 canonical-pencil tuples. It refutes only the proposed group-theoretic cancellation shortcut. The pencil identities were independently recovered from adjunction, base-point intersections, and Euler characteristic: g_k=1+k(k+1)K^2/2, n_k=k^2K^2, and N_k=e+K^2(3k^2+2k). At r=3,k=1 the values are 17,16,196. Auroux's equivalence criterion involves a suitable pluricanonical degree and eventual high-degree equivalence; one low-degree obstruction alone does not settle canonical symplectomorphism.

## 6. Smooth sphere construction

The vertical component in the nodal-grid base is blown up six times, so its strict transform has square -6. Its ramification preimage S is a smooth rational curve and has square -3, because the square of its doubled class is twice -6. In the cover canonical formula, the exceptional contributions to the base canonical class and half-branch class cancel. Projection to the original vertical fiber then gives K.S=1.

The simultaneous-resolution family preserves the canonical class. Its canonical divisor is the pullback of the nef, big base class s+(2r-2)f; hence the resolution model is a minimal general-type surface in the required deformation component. This justifies transporting the smooth sphere and its canonical pairing to X_r. For r=3 it matches the square and canonical pairing of Y_3's ramification sphere, so the simple existence test fails.

The report correctly separates this smooth argument from canonical-symplectic representability. The resolution's exceptional -2 curves have canonical degree zero; a Kähler form on that complex model is not automatically the normalized canonical symplectic form. The formal odd-unimodular-lattice vector calculation is also correctly labeled formal: it proves compatible arithmetic and adjunction data, not the identification of a specific canonical marking or an embedded representative. No matching -r sphere for r>3 is established.

## 7. Degeneration hypotheses and source status

MNU v3, Theorems 5.12 and 5.8, applies to p_g>=10 with only T-singularities, not all Du Val, and the stated smoothing hypotheses. Here K^2=8(r-1), so the integer in Theorem 5.8 is r-1>1. Its precise conclusion is the component whose general canonical image is F_0. The shorthand about a non-spin component cannot distinguish the odd-r pair because both components are non-spin. The report uses the precise conclusion. It does not extend the theorem to arbitrary log-canonical or non-normal limits. Purely Du Val limits are separately controlled by simultaneous resolution.

AEHK's moduli space is explicitly the space of Q-Gorenstein smoothable normal stable Horikawa surfaces. Its Theorem 1.17 and Example 1.23 yield the exceptional common normal limit with an elliptic double-cone singularity at p_g=10. Since p_g=4r-2 and p_g-2 is divisible by four throughout this family, only r=3 survives within the odd-r target. The r>=5 odd pairs remain disconnected in that normal locus. The source's differential-topology discussion expressly does not complete a diffeomorphism argument. A current primary-page check still lists AEHK as arXiv v1, submitted 23 July 2025, and MNU as v3, revised 7 July 2025. These are inspected preprints, not a new solution or a guarantee of exhaustive literature coverage.

Rana--Rollenske's published statements support the semi-smooth common degeneration. The abstract, Theorem A, and later local-moduli statements use slightly different bounds. The chosen counterexample r=4 has K^2=24 and ell=3, safely inside all relevant bounds. X_4 is non-spin and Y_4 spin, so their intersection-form parities differ and they cannot be homotopy equivalent. This refutes an unrestricted common-semi-smooth-degeneration implication, while preserving the target restriction to odd r.

The remaining filling requirement is logically exact: exterior and filling diffeomorphisms must intertwine the attaching maps, up to collar-adjustable isotopy. The non-normal case may involve neighborhoods of a singular curve, not just a union of isolated Milnor fibers. Canonical-class equality under a proposed diffeomorphism does not give the cohomologous path of symplectic forms needed by Moser. Catanese's singular-gluing results retain hypotheses on normal singularities and smoothing components; they cannot be invoked solely from the existence of a common central fiber.

## 8. Reproduction, adversarial tests, and optional guard

The supplied independent checker verifies the finite example and arithmetic at r=2 through 101, with pencil degrees 1,2,4,8,16. The finite parameter range is an error check and not a substitute for the symbolic derivations above.

Both the candidate and independent programs were executed from genuine mode-0555 directories with mode-0444 scripts, at UID=EUID=1000. A subprocess file-creation probe received PermissionError and confirmed that its working directory was not writable. All normal, -O, and -OO runs succeeded. Candidate output exactly matched the frozen 23,969-byte JSON, SHA-256 `b85cb80dfd9a9b7b25b3257e04ca162c75964cd35d640adf174c899ab0a60b2a`. Independent outputs were also identical across modes. No local state was created.

The audit harness itself was rerun under normal, -O, and -OO, with byte-identical audit records. Neither mathematical checker uses Python assert. Fifteen meaningful mutation cases were each tested in all three modes; fourteen were rejected by always-active RuntimeError checks. They changed a generator, conjugator, saturation pairing, canonical coefficient, signature, pencil count, inverse Hurwitz operation, formal characteristic vector, expected orbit size, or partial conjugation.

The fifteenth mutation deliberately truncated each candidate orbit to its seed. The frozen candidate still emitted a passed status, because it reports rather than directly requires the two exact orbit cardinalities. The strict saved-output comparator rejected that output in all modes. This is a narrow hardening issue, not evidence that the unchanged algorithm or reported orbit sizes are wrong: independent exhaustive computation verifies both.

`OPTIONAL_ORBIT_GUARD.patch` adds one always-active require call, checking the ordered cardinalities (216,144). In a separate disposable copy, the patched program retained byte-identical valid output under every optimization mode and rejected the truncated-closure mutant in every mode. It has not been applied to the frozen candidate. If adopted in a later candidate, the modified executable and manifest must receive fresh pins; the audit does not silently substitute that new candidate for the original.

## 9. Source integrity and bounded conclusion

All seven cached scholarly PDF byte counts and SHA-256 digests were independently matched to the candidate's source manifest. Relevant theorem statements, hypotheses, and proof endpoints were inspected from those pinned files. Key K3, MNU, and AEHK pages were additionally inspected visually. Current primary landing pages were checked for version/status where available. The audit does not claim to have independently reproved all classification results in the cited papers or inspected every page of the 218-page AEHK preprint.

The public audit bundle contains original mathematical assessment, original executable tests, outputs, a patch to authored code, and public source verification metadata only. It contains no scholarly PDF, screenshot, copied source passage, external dataset, private source, or coordination record.

Final disposition: retain **partial/unresolved, five approaches**. The report's restricted and conditional conclusions pass this independent audit. No mathematical correction to the frozen report is required. The optional exact-orbit guard improves standalone fail-closed behavior without changing any mathematical result.

## Primary references

- K3, Problem 4.94, pp. 267--268: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- D. Auroux, *The canonical pencils on Horikawa surfaces*, published-version arXiv v2: https://arxiv.org/abs/math/0605692v2
- F. Catanese, *Canonical symplectic structures and deformations of algebraic surfaces*: https://arxiv.org/abs/math/0608110v2
- V. Monreal, J. Negrete, G. Urzua, *Classification of Horikawa surfaces with T-singularities*, v3: https://arxiv.org/abs/2410.02943v3
- J. Rana, S. Rollenske, *Standard stable Horikawa surfaces*, published 2024: https://doi.org/10.14231/AG-2024-017
- H. Akaike, M. Enokizono, M. Hattori, Y. Koto, *Normal stable degenerations of Noether-Horikawa surfaces*, v1: https://arxiv.org/abs/2507.17633v1
