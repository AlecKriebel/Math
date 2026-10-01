# Independent source and counterexample audit: 30004437

## Verdict

**PASS_COMPLETE_CREDITED_SOURCE_RESULT.** The original unrestricted, degree-preserving real-zero amalgamation conjecture is refuted by the cited published counterexamples. The appropriate disposition is **already_solved 0/5**, credited to the prior authors. This is a source correction, not a new campaign discovery.

The verdict binds unchanged `SOURCE_ASSESSMENT.md`, SHA-256 `23a1984e50a456e0d7ff1a8799e58ef0fabb403da6bf0e8bdd93146153d67d6c`, and author `FROZEN_MANIFEST.json`, SHA-256 `06b26310f659053685978bd22640631844df775e0ff13ccd0eca78193ca0d8a8`. No mandatory correction remains.

All ten author files and five full primary PDFs match their hashes and byte counts. The author program was read and replayed in a separate directory: its 4,472-control output and exact certificate reproduce byte for byte. The independently written checker passes **1,611 exact controls**, including symbolic coefficient, shear, support, rank, permanent and Rayleigh identities. General hyperbolicity and support implications were audited analytically rather than inferred from finite samples.

## Exact source scope

I read the full OWR contribution, including the definition of the arbitrary tuple x on p.652 and the rendered first conjecture on p.653. This is a universal statement over finite blocks of distinct real variables, with exact compatibility and exact output restrictions and a total-degree bound. It is not restricted to one shared scalar variable. The 2025 cubic example has two shared variables, one private variable on either side, a nonzero constant term and no real-zero amalgam of any degree. It therefore directly refutes the assigned assertion at d=3.

The second OWR conjecture uses “weak” for one exact restriction and only the cubic-part condition on the other. The later same-named conjecture instead uses two shared variables and two exact restrictions, without a degree bound. I verified both displayed statements. The author correctly refrains from transferring the later negative result to the separate OWR cubic-part version. No conclusion about the generalized Lax conjecture or a classification of all compatible pairs is warranted or claimed.

## Published example and its real-zero property

The seven-variable basis polynomials, their excluded triples, the diagonal collapses and the resulting four-variable cubics agree with the full Kummer–Sawall final paper, printed pp.7–8. The displayed common cubic has value 20 at (1,1,1). After the shared shear and dehomogenization, both polynomials have total degree three and value 20 at the origin, and their private-zero restrictions agree exactly.

The stability inputs are correctly distinguished from numerical root tests. For F7^(-4), the source's Rayleigh sum of squares expands exactly to the required Rayleigh difference with the stated labels. The cited Wagner–Wei criterion applies because deletion and contraction yield smaller matroids, whose half-plane property is supplied by the complete COSW source, Proposition 10.4. For F7^(-5), the stated four-row transversal presentation has every nonzero maximal permanent equal to two. COSW Theorem 10.2, Corollary 10.3 and duality consequently give the unweighted basis polynomial, not merely some polynomial with the same support. The two complementary forbidden triples intersect in exactly one element, which identifies the claimed relabelling.

Diagonal specialization preserves stability. Homogeneous stability gives hyperbolicity in the nonnegative direction (1,1,1,0), where the value is nonzero. Pulling back by the shear and dehomogenizing at u=1 yields the exact real-zero inputs. No claim that every real-zero polynomial is stable is used.

## Full arbitrary-degree reduction

I reconstructed the argument for an arbitrary hypothetical extension R of degree D. Its exact cubic restrictions force D≥3. Homogenization gives H hyperbolic in e0, with restrictions u^(D−3) times the sheared cubics.

The cone must use the consistent convention: roots of H(te0+v) are nonpositive. The final paper's printed Definition 2.12 has the opposite adjective, diagnosed already by H(x)=x and e=v=1. This is explicitly reconciled in the frozen author assessment. I raised the same point independently before reading that assessment; it was already addressed, so no author revision or reviewer coauthorship was required.

Each input cone contains the required coordinate vectors and e0−e1−e2. All these vectors have nonnegative u coordinate. Multiplication by u^(D−3) therefore leaves their membership valid even though it may change the entire cone. Restricting the homogeneous polynomial along the relevant coordinate subspaces tests precisely the same one-variable polynomials, so these vectors also belong to H's cone. The proof does not require an incorrect equality of full cones.

Undoing the shear gives a homogeneous T whose cone contains the nonnegative orthant. The vector e0+e1+e2 is an interior direction because it maps to H's interior direction e0. Adding cone vectors keeps it interior. For any strictly positive vector, subtract a sufficiently small positive multiple of this interior vector; the remainder is in the nonnegative orthant. Thus every strictly positive vector is an interior hyperbolicity direction and T is stable.

Set k=D−3. Retaining terms of u-degree at least k and dividing by u^k produces a cubic T0 with the required restrictions P1 and P2. Its support equals the support of partial_u^k T: surviving monomials have distinct images, and differentiation multiplies each coefficient by a positive nonzero factorial. There is no cancellation or false assertion that T0 itself is stable. The derivative is a nonzero homogeneous stable polynomial, so its support is M-convex. The nondegenerate restriction lemma then identifies the ranks on each coordinate subset with the input ranks. I checked its exchange proof: a term outside the retained coordinate subset can be moved inside while preserving the maximum and reducing the outside mass, a contradiction. This yields a genuine amalgamating polymatroid from any degree D.

## Exact rank contradiction

The six displayed inequalities are three ordinary submodularity inequalities, one monotonicity inequality, then submodularity and monotonicity. Their unknown mixed ranks cancel. The input ranks are exactly those computed from the two published supports, and the sum is −1. A sum of nonnegative quantities cannot equal −1. The same certificate scales to −m for positive integer scaling. This verifies the whole obstruction, not merely an attempted low-degree coefficient search.

The independently checked symbolic examples with extra mixed high-degree terms confirm the homogenization, reverse shear and derivative-support mechanics without assuming those artificial test extensions are real zero. They are transcription controls, not candidate counterexamples to the published theorem.

## Attribution, access and publication boundaries

The complete final Kummer–Sawall paper, Algebraic Combinatorics 8(1) (2025), 1–15, DOI 10.5802/alco.399, supplies the principal result. The publisher records online publication on 3 March 2025. The complete Sawall–Schweighofer v2 manuscript supplies the earlier six-shared-variable counterexample; its final journal-layout PDF was not compared. The older counterexample is corroborating source history; the disposition already follows from the fully audited final 2025 proof.

The full 2013 Wagner–Wei corrigendum was not retrieved, and this review does not certify its contents or all examples in the earlier paper. The specific needed Rayleigh identity is verified algebraically, its criterion and smaller-matroid input were read in full, and the principal 2025 published theorem postdates the corrigendum. The access limitation is retained rather than silently erased.

The positive cases with no shared variables, one variable in each of the three blocks, and degree at most two remain unaffected. The final source correction covers the exact assigned universal conjecture. Publish the manifest-bound author artifacts and these portable review files only; omit source PDFs, extracts, renderings and replay directories. Parent retains publication authority.
