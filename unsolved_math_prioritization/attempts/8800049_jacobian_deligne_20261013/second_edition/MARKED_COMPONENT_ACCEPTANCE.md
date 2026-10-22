# Acceptance audit: marked polarized Deligne realization

## Verdict and exact object

**ACCEPTED at the stated theoretical scope**, relative to the established results cited in the manuscript. The entire manuscript was read, and the previously identified marking, orientation and whole-tuple descent obligations were checked after revision.

Reviewed manuscript: *A certificate-search inverse for a marked polarized Deligne ideal*.

Reviewed SHA-256: `6828c52bf1e49781a6e0c4fe5cc75699877dd76a3128bb5655650b1e7c6ed025`.

The accepted claim is a terminating, exact certificate-search realization of a specified principally polarized ordinary absolutely simple threefold Deligne ideal, under an explicitly fixed effective full comparison convention. Composition with the separately accepted geometric theorem attaches the finite-field Jacobian/descent answer to that marked object. It is not a new efficient algorithm, an implementation result, a numerical precision bound, a worldwide novelty result, or a historical closure claim.

This report supersedes the unresolved-status list in the earlier adversarial audit. No change to the independent first-pass aggregate theorem is required.

## Critical points verified

### Full Frobenius forces the canonical deformation

The certificate checks a base-linear lift of the original q-Frobenius and the exact relation h(F)=0. Ordinary unit-root/nonunit-root factors of h are coprime over Z_p; the resulting CRT projectors split the lifted p-divisible group. The special-fibre projectors are the étale and multiplicative projectors. At finite level, étaleness lifts by the vanishing of differentials and Nakayama; the dual argument gives multiplicative type. The split deformation is canonical by Serre–Tate. This proof retains torsion deformation parameters, so it is not invalidated by ramified quasi-canonical-lift concerns.

The residue extension does not change the marked Frobenius to q^m-Frobenius. The certificate explicitly uses the base change of A's original F_q-linear endomorphism and checks its reduction as a morphism of schemes.

### The comparison is globally fixed and effective

The chosen tower of algebraic number fields, compatible primes above p, and compatible residue embeddings provides effective arithmetic on every finite coefficient set. The unramified algebraic subfield and its valuation ring are the algebraic strict henselization used in Deligne's construction. The complex embedding is fixed globally, not selected to fit a candidate. The residue identification in the certificate uses the fixed embedding of the input F_q.

These requirements remove the real gap that would remain if a candidate were required only to have the correct CM type. CM type, characteristic polynomial and local Tate data do not by themselves identify the integral ideal class.

### The complete marked tuple descends

Deligne's §3 supplies descent of the underlying canonical abelian scheme to D. The revised manuscript then separately justifies descent of F and the polarization map: H=Frac(D) is relatively algebraically closed in the fraction field of its completion; finite coefficient subextensions are regular; generic homomorphisms descend by Milne's Corollary 15.4(b); and the Néron mapping property extends them to D.

For the polarization line bundle, the rigidified Pic^lambda torsor under the dual abelian scheme is smooth. A point on its geometric special fibre lifts over the strictly henselian base. Rigidification at zero realizes the point as an actual line bundle. Cohomology and base change for an ample principal line bundle gives a rank-one section module; a generator gives the relative effective Cartier theta divisor. The cube gives the projective embedding. The final finite-presentation descent therefore includes the endomorphism, polarization, theta, section, group law and special-fibre identifications, rather than only the underlying generic variety.

The original BLR Proposition 1.2/8 was independently inspected and provides the exact Néron-model fact used here. It can replace or supplement the manuscript's lecture-note reference without changing the argument.

### All topology is integral and functorial

The projective variety is represented by a compact semialgebraic set over real algebraic numbers. Finite semialgebraic homeomorphism graphs are verified by real quantifier elimination. The verified open-star condition supplies genuine simplicial approximations to each required map after subdivision. Therefore the method computes actual integral induced maps, not just Betti numbers or rational homology.

The group law, product triangulations, shuffle cross products, subdivision chain maps and integral Smith-normal-form calculations are all included. The positive projective hyperplane class is oriented by the explicit outward octahedron cycle and its radial map to the sphere, followed by the displayed CP^1 map. Division by three occurs in torsion-free characteristic-zero H^2 with a certified cube identity; it does not cancel a finite-field polarization morphism in characteristic three.

The pairing is evaluated on the Pontryagin product m_*(x cross y), so the marked matrix has the same meaning as the input alternating form.

### The sign was checked rather than guessed

The printed Marseglia form has conjugation over both t and a. The manuscript explicitly distinguishes this b from the positive topological pairing E_a=Tr(a s overline(t)), with b=-E_a. Its Hermitian-form/Chern-form calculation gives the correct sign for the oriented product torus. The test E_(i/2)(1,i)=1 agrees with the positive complex orientation. The conversion is a convention check, not an allegation of a source error.

### The enumeration has a real stopping proof

Every candidate includes all finite witnesses and its integer matching matrix. Every individual check terminates. The scheme checks over the number-field localization have standard-smooth-chart witnesses; the algorithm does not import the first-pass field-only tests without modification. The search does not become stuck indefinitely looking for an isomorphism to one wrong candidate.

Completeness starts from the particular Deligne object (I,a), descends its whole canonical tuple, obtains topology witnesses and its unimodular matching matrix, and observes that this finite successful certificate eventually occurs. The two exact matrix equalities prove the marked polarized identification by Deligne full faithfulness. This is stronger than arbitrarily labeling an unlabeled counted list.

## Bounded source inspection

- Deligne, *Variétés abéliennes ordinaires sur un corps fini* (1969), original retained PDF and text: §§1–3, 6–8 inspected for comparison, descent, Frobenius marking and equivalence. Source: https://publications.ias.edu/sites/default/files/Number6.pdf
- Katz, *Serre–Tate local moduli*: retained full PDF; Theorem 2.1(1),(4), printed pp.148–149, directly inspected for deformation parameters and lifting morphisms. Source: https://web.math.princeton.edu/~nmk/old/serretatelocmod.pdf
- Marseglia, *Computing square-free polarized abelian varieties over finite fields*, §8: the relevant rendered PDF page and enlarged formula were visually inspected for the bar placement and period convention. Source: https://arxiv.org/abs/1805.10223v3
- Schnell, Lecture 4: p.3 directly inspected for the Chern-form formula, with the elliptic normalization also checked. Source: https://www.math.stonybrook.edu/~cschnell/mat615/lectures/lecture4.pdf
- Milne, *Abelian Varieties*, AV110: Corollary 15.4(b) and its proof, printed pp.58–59, inspected for Hom descent over regular extensions. Source: https://www.jmilne.org/math/CourseNotes/AV110.pdf
- Bosch–Lütkebohmert–Raynaud, *Néron Models*, §1.2 Proposition 8 and proof, printed p.15, visually inspected in the retained Chapter 1 scan. It states that an abelian scheme is the Néron model of its generic fibre. Source: https://math.arizona.edu/~cais/scans/BLR-Neron_Models/neron1.pdf
- Basu–Karisani, *Efficient simplicial replacement of semialgebraic sets*, introduction, inspected for semialgebraic triangulation and quantifier-elimination context. The faster homology-functor result has rational-coefficient scope and is not substituted for the explicit integral witness argument. Sources: https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/efficient-simplicial-replacement-of-semialgebraic-sets/C32B4A3FA99FAF864D70274612ADA1C2 and https://arxiv.org/abs/2207.10497

This is a bounded proof/source audit. The original proofs of every standard dependency were not reproved. No nontrivial end-to-end geometric instance was executed, and no practical running-time claim was tested. Hashes establish reviewed byte identity only. No remote writes were performed.
