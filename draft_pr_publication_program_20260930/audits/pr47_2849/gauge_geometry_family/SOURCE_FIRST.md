# Independent gauge/deformation baseline

Checkpoint UTC: 2026-10-03 04:23:29. Audit completion estimate: 20%; progress toward solving full KP-3.51: 0%. This file was written before reading the candidate OBSTRUCTION, helper code, results, or previous review. Scope: original PR 47 head `487327b2412c436ae69e8c52bf353a9a1fb7594e`.

## Source binding

The supplied AIM URL is a four-page workshop summary, not the numbered K3 list. The author-hosted [K3 list](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp.167–168, asks whether an SU(2)-abelian rational homology 3-sphere has complex framed instanton dimension equal to its finite first-homology order. Its stated Morse–Bott subcase is already known. Only source identity, locator, and first-party deductions are retained here; no foreign PDF, extracted text, pixels, or headers are saved.

[Baldwin–Sivek, Stein fillings and SU(2) representations](https://msp.org/gt/2018/22-7/gt-v22-n7-p13-s.pdf), DOI 10.2140/gt.2018.22.4307, §4.1, Propositions 4.4–4.5 and Theorem 4.6, supplies the exact conditional theorem. Under the no-irreducible hypothesis, vanishing of all adjoint H1 groups is equivalent to the framed critical set being Morse–Bott; cyclical finiteness suffices. The theorem's contrapositive then gives the L-space equality. This is conditional, not the full target.

Exact PDF identity freshly fetched in memory: author K3 6,578,041 bytes, SHA256 `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`; publisher full-paper `gt-v22-n7-p13-p.pdf` 811,743 bytes, SHA256 `8878155672962cf4fd6489b3f6f4e7d1dcf889108f3caf692319de3c42f85c15`. AIM direct fetch returned HTTP 403; browser inspection succeeded. Publisher full-paper browser parsing returned an internal error, whereas its publisher sibling `-s.pdf` was inspectable and contains the cited theorem and proof.

## Derivation without candidate input

Let Y be connected, closed, oriented, and a rational homology 3-sphere; A=H1(Y;Z) is finite. A reducible unitary two-dimensional representation preserves a complex line, so its orthogonal complement is also invariant. After conjugation it is diag(chi,chi^-1) for a character chi:A→U(1). Conversely such a diagonal representation is reducible and abelian. Because A is finite its image is finite cyclic. Two such representations are conjugate exactly for chi' in {chi,chi^-1}. The central cases have chi^2=1 and conjugacy orbit a point; every other orbit is SU(2)/U(1)=S2. If all representations are reducible, there are finitely many such disjoint compact orbits. Thus the underlying critical-set topology has total complex homology dimension

    #{chi:chi^2=1} + 2·(#{chi:chi^2≠1}/2) = |A|.

This counts the unquotiented Hom(pi1(Y),SU(2)) critical set after framing. Counting only conjugacy classes loses the two homology classes of each S2.

Conjugation on su(2) fixes the diagonal real axis and rotates the off-diagonal real plane by chi^2. Write C_(chi^2) for that plane with its natural complex structure. As real local systems,

    ad(rho)=R ⊕ (C_(chi^2))_R,
    dim_R H1(Y;ad rho)=b1(Y)+2 dim_C H1(Y;C_(chi^2)).

Here b1(Y)=0. If chi^2=1 the whole adjoint system is trivial and H1 vanishes. The factor 2 counts real dimensions; it does not appear if one instead complexifies the full adjoint system, whose splitting is C⊕C_(chi^2)⊕C_(chi^-2).

For a group presentation, linearizing its relations identifies the Zariski tangent space with Z1(pi1;ad rho). Infinitesimal conjugation gives B1, of dimension 3−dim(stabilizer). Therefore

    dim_R T_rho Hom = 3−dim(stabilizer) + dim_R H1(Y;ad rho).

At a central rho the stabilizer has dimension 3; at a noncentral reducible rho it has dimension 1. In the framed Hopf-link construction, fixing the two framing meridians to i and j makes the total stabilizer discrete, but the original representation's conjugacy directions remain as true critical directions. The framed Hessian kernel consequently has the same dimension as T_rho Hom. A noncentral reducible component is S2, so Morse–Bott means kernel dimension 2, not 0. Its excess is precisely the adjoint H1 above. Central representations are isolated and nondegenerate.

An orbit being the entire nearby set does not force its Zariski tangent space to be only its orbit tangent: obstructed first-order deformations may fail to integrate. H2 or higher-order relation terms must be controlled to convert an infinitesimal deformation into a nearby irreducible representation. A zero derivative of x² at the isolated zero x=0 gives the elementary logical model. This does not assert a 3-manifold counterexample.

For a finite abelian cover X→Y with deck group D, averaging over D decomposes the complex cochain complex into character summands. Up to the conventional inversion of character labels,

    H1(X;C)= ⊕_(lambda in D^) H1(Y;C_lambda).

Only the trivial-character summand is forced to vanish by b1(Y)=0. For the adjoint cover associated to chi², vanishing b1(X) implies the chosen twisted group vanishes. The converse for a single fixed rho is generally stronger than that one group's vanishing: other character summands can contribute. A statement quantified over all rho can use character powers/quotients to recover the converse. This distinction must be checked against the candidate.

## Exact remaining gap

The topology rank |A| does not alone bound Floer rank. A Morse–Bott spectral sequence gives that upper bound only after normal nondegeneracy is proved. Euler characteristic gives the lower bound |A| over C. The full target still needs a theorem excluding or managing all degenerate reducibles under the no-irreducible hypothesis. Simply assuming twisted H1 vanishes, assuming relevant cyclic covers are rational homology spheres, or treating every first-order direction as integrable transfers the central difficulty to an unsupported assertion.

No communication with outside individuals was attempted or prepared. No candidate or canonical/native state has been modified.
