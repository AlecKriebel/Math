# Audit of the finite group representation sphere result

Audit date: 11 October 2026. Target: AIM Problem 2.5, problem 20000157, row 1700. This is an AI-assisted mathematical audit, with no independent human referee review or proof-assistant formal certification.

## Verdict

**Accepted as a partial result, with scope made explicit.** The supplied equality criterion and rational classification admit complete proofs under the finite-group, complete-universe, genuine-equivariant, ordinary-thick interpretation. `PROOF.md` gives an independently reconstructed derivation. This audit does not establish novelty, priority, or a full integral answer to the AIM question.

The principal conclusions are:

1. Both the actual-sphere closure and the RO(G)-sphere closure equal all compact genuine spectra exactly for elementary abelian 2-groups, including the trivial group.
2. In the compact rational category, the closure has precisely the shifted Weyl orientation lines `det(alpha^H)` in each subgroup-conjugacy factor.
3. Orbit membership is also exact: G/H-plus is in the integral closure precisely when H is normal and G/H is elementary abelian of exponent two. This holds for both actual and virtual generators.
4. A rational-only integral membership criterion is false: for any other finite group, the free orbit smashed with a mod-ell Moore spectrum is rationally zero but remains excluded when ell is odd and does not divide the group order.

The last two points are direct audit consequences of the same arguments, not a claim of a newly discovered theorem.

## Proof obligations checked

| Obligation | Check and disposition |
| --- | --- |
| Original target | Fresh AIM HTML confirms attribution to J. Greenlees and a question whose body contains no finite-group hypothesis. The present finite-group interpretation is explicit, not silently substituted for the full original scope. |
| Ambient category | Genuine spectra indexed on a complete universe throughout. The obstruction passes to an underlying spectrum with G-action but does not replace the ambient category by naive spectra. |
| Compact and finite | Compact means retract of a finite orbit-cell construction. The proof obtains all orbit generators and uses the retract closure in the final step. It does not assert that every compact object is literally a chosen finite cell object. |
| RO(G) grading | Virtual spheres are legitimate compact invertible genuine spectra. Thick suspension itself means integer suspension, not automatic closure under all virtual representation shifts. |
| Actual versus virtual | The positive integral proof uses actual sign representations. The negative proof applies even when every virtual sphere is allowed. This proves the equality criterion for both choices. It does not establish equality of the two integral closures for every other group. |
| Euler triangle | Derived from the equivariant disk/sphere cofiber sequence and contraction of the disk to its origin. All terms and maps belong to the genuine category after suspension. |
| Genuine cells | The square-coordinate parametrization identifies each closed sign face with a simplex. Its stabilizer fixes the whole parameter disk pointwise. This verifies a genuine G-CW filtration rather than just counting strata. |
| Stabilizers | For a face with support I, the stabilizer is the intersection of the kernels of characters in I. Independence gives quotient rank exactly cardinality of I, with strict increase of stabilizer on every proper-support face. |
| Unique top orbit | The only top support set is all coordinates. Its 2^d sign chambers form exactly one E/K orbit. The group action preserves simplex parameters, so the top quotient is an ordinary integer suspension of E/K-plus without a representation twist. |
| Induction order | Induction is on quotient rank, simultaneously for all K. Every lower cell uses strictly smaller rank. The proof does not assume closure under an induction functor. |
| Attaching maps | Skeletal cofiber sequences suffice; no attaching map must be zero or split. The lower skeleton is built before taking the top cofiber. |
| Boundary cases | Quotient rank zero gives the unit. At rank one the preceding skeleton is empty, its based suspension spectrum is zero, and the Euler triangle directly produces the desired orbit. |
| Regular obstruction | Underlying rational homology retains its G-action. Sphere homology is a determinant line; the free orbit is the faithful regular module. Forgetting the action would invalidate the obstruction. |
| Semisimplicity | Maschke is applied only to a field with characteristic not dividing the finite group order. Long exact homology sequences yield kernels, cokernels and extensions with no new allowed-simple types. |
| Non-split group algebra | Q need not be a splitting field. The argument concerns actual rational simple constituents. If they are all sign lines, the regular module itself splits into those lines by semisimplicity, which is enough. |
| Geometric fixed points | The residual Weyl action is retained. For nonnormal H, restriction to its normalizer precedes geometric fixed points. Categorical fixed points, dimensions alone, and coinvariants are not substituted. |
| Fixed orientation | The H-factor of a virtual sphere is a line in degree dim(alpha^H), with character det(alpha^H). Dual/contragredient conventions do not change a sign line. |
| Rational factor model | Barnes Theorem 8.1 supplies the product of derived group-algebra categories. Greenlees--Quigley Theorem 2.1 identifies the relevant geometric-fixed-point invariants. Their published hypotheses require both objects rational, which is satisfied here. |
| Rational compactness | The category being classified is compact within rational genuine spectra. Finite products and semisimplicity identify these with perfect complexes, not all unbounded/infinite-dimensional modules. |
| Idempotent isolation | Rational Burnside idempotents act as endomorphisms of each sphere. Their images are retracts of that sphere. This is valid ordinary-thick reasoning and does not presume tensor-ideal closure. |
| Factorwise independence | Separate idempotent retracts remove any requirement to realize all desired subgroup characters with one common global representation. |
| Sufficiency of rational criterion | Semisimple complexes split into shifts of homology simples; every allowed shifted line is already obtained by a factor retract and an integer shift. This proves both inclusions. |
| Exact allowed characters | For H other than the trivial subgroup, the proof uses the image D_H(G), not an unsupported assertion that all sign characters of W_H extend to global representations. |
| Rational actual/virtual comparison | Replacing V-W by V+W preserves every determinant sign. After separating factors, ordinary integer shifts adjust the dimension difference. This establishes the rational comparison only. |
| Image of rationalization | Integral membership implies rational membership. The proof classifies the thick closure of the rationalized image, and does not silently assume the bare image is retract-closed. |
| Torsion counterexample | Taking a Moore cofiber on the free orbit yields zero rationally but regular mod-ell homology in degrees zero and one. Maschke and faithfulness exclude it when G is not elementary abelian of exponent two. |
| Internal smash closure | A two-stage thick-closure argument proves closure under smashing two members, because the generating spheres are closed under smash. This supplies a separate positive proof without assuming tensor-ideal closure. |
| Orbit classification | A sign-only transitive permutation module has elementary abelian action image; faithfulness and abelian transitivity force trivial stabilizers in that image. Thus H equals its core. The converse follows from independent quotient sign characters and justified internal smash closure. |
| Ordinary versus tensor ideal | Since the unit is included, tensor-ideal generation would be tautological. All positive integral steps use finite cofibers and integer shifts, and rational factor isolation uses retracts. |

## Material clarifications relative to the inherited report

### Compact Lie scope

It would be misleading to attribute the failure of the finite proof for compact Lie groups to failure of orbit compactness. The standard complete-universe genuine compact-Lie category still has compact generators G/H-plus for closed H, as explicitly stated in the inspected Mathew--Naumann--Noel author version. The obstacles are the changed rational algebraic structure, potentially positive-dimensional Weyl groups, and the nonfinite subgroup-class structure. No classification of that broader setting is claimed here.

### Rational necessity is strictly weaker than integral membership

The rational criterion is sufficient inside the rational compact category. It is not sufficient for the original integral problem, even on rationally acyclic compact objects. Proposition C of `PROOF.md` supplies a family of explicit counterexamples. This prevents the phrase "complete rational description" from being misread as an integral decision procedure with only an unknown proof.

### Source versions

The inherited orientation source was arXiv:2205.02382v2, dated 19 May 2022. The work is published in Proceedings of the American Mathematical Society, Series B 10 (2023), pages 101--113. The published version was retrieved and inspected for this audit; its orientation discussion is Sections 3.2--3.3, and Theorem 2.1 is stated for two rational objects. Those are the locators and hypotheses used in the reconstruction.

The Barnes arXiv PDF and AIM HTML were independently retrieved and are byte-identical to the supplied captures. The exact byte counts and SHA-256 values appear in `PUBLIC_SOURCE_METADATA.json`. All raw source captures remain outside this authored packet.

## What remains open in this report

Although orbit membership is completely determined by Proposition D, for a non-elementary-abelian finite group G the remaining task is to determine a necessary-and-sufficient condition for an arbitrary compact genuine integral G-spectrum X to belong to the ordinary thick closure of all RO(G)-representation spheres. Rational Weyl constituents give a complete rational answer, and coefficient-field homology gives additional necessary conditions, but neither an integral classification nor sufficiency of these tests is proved.

No result here establishes a comparison of actual and virtual integral closures for every such G, a minimal number of construction steps, or a classification in a different group category. The broader original AIM problem therefore remains unresolved by this work. This is a statement about the coverage of this report, not a claim that an exhaustive contemporary literature search proves present openness.

## Verification record and limits

- Reconstructed the coordinate attachment, orbit induction, regular-module obstruction, rational idempotent splitting and semisimple derived-category argument in full.
- Read the relevant primary-source statements and context. Inspected the published orientation page visually and the Barnes main theorem page visually. The external papers' entire proofs are not re-proved by this audit.
- The authored finite-check program, retained outside the public packet, exhaustively checks the finite sign-cell model through quotient rank eight and independently checks selected regular-representation obstruction witnesses over Q and finite fields. Aggregate outcomes are recorded in `VERIFICATION_METADATA.json`. It additionally checks all 37 subgroups of C3, C4, S3, D8 and C2-cubed against the permutation-image criterion, including the product-of-signs bijection for the 26 admitted orbits. It also includes negative controls for reversed stabilizers, wrong orbit counts, and wrong face counts. These finite tests supplement the general proof; they cannot establish it on their own.
- The proof remains a mathematical argument in ordinary prose, not a formal proof-assistant certificate.
- Frozen input identities and all five scholarly-source captures were rechecked. The public packet contains authored mathematical reports and public verification metadata; source documents, source extracts, raw computational data and coordination material are excluded.

## Acceptance decision

Accept the full authored proof and this audit for a **partial-result** report. Preserve the explicit finite, genuine, compact and ordinary-thick conventions, the inherited-result attribution, the rational-versus-integral distinction, and the exact remaining gap. Do not label the original AIM problem solved or the inherited theorem a new discovery.
