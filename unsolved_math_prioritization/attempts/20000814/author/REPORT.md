# Smooth embedded limits of complete-intersection space curves

Problem 20000814 · AIM-ARITHMETIC_GEOMETRY-0060 · catalog rank 759  
Investigation date: 2026-10-05  
Disposition: **partial progress, five substantive approaches; general question not solved**

## 1. Target and result

The actual target is Problem 13 of the AIM *Components of Hilbert Schemes* list, PDF page 2: in characteristic zero, must a smooth special fiber of an embedded flat family of complete-intersection curves in projective three-space itself be a complete intersection? The catalog's “bad-surface and Rao-module reduction” title describes a previous research attempt, not the original question. The primary AIM text and its characteristic, ambient-space, and smoothness qualifications were checked directly. [AIM]

Use the precise trait version: let k be algebraically closed of characteristic zero, R = k[[t]], and let C_R be a closed subscheme of P^3_R, flat and projective over R. Assume its geometric generic fiber is a smooth complete intersection of type (a,b), with 1 <= a <= b, and its special fiber C is smooth. The usual curve-selection and normalization argument in the finite-type Hilbert scheme reduces the embedded specialization question to this setting, after the usual extensions of the trait. This is not a question about abstract smooth limits, a changing ambient space, set-theoretic intersections, or merely locally complete-intersection curves.

**Proved here, by reconstructed classical arguments:**

1. C has degree ab, genus 1 + ab(a+b-4)/2, and canonical bundle O_C(a+b-4).
2. C is a complete intersection exactly when its Hartshorne–Rao module vanishes.
3. The existence of **any integral degree-a surface** containing C forces C to be a complete intersection. The surface need not be smooth or normal.
4. Consequently, a non-complete-intersection limit must have minimal containing-surface degree c satisfying **3 <= c < a**. In particular, **every type (a,b) with a <= 3 has an affirmative answer**.
5. Such a counterexample also produces a nonempty, nonreduced, locally complete-intersection curve Z in P^3 with
   - deg Z = (a-c)(b-c);
   - omega_Z = O_Z(2c-a-b-4);
   - p_a(Z) = 1 + (a-c)(b-c)(2c-a-b-4)/2.
   Its degree cannot be one. Therefore **type (4,4) also has an affirmative answer**.
6. If F_c defines a minimal containing surface, then every equation of C of degree m <= b is a multiple of F_c. The minimal surface is unique, up to scaling. In particular h^0(I_C(a)) = binomial(a-c+3,3), compared with 1 on the generic fiber if a < b and 2 if a = b.

These statements sharpen the previously supplied reduction, which stopped at a <= 2 and required a smooth degree-a containing surface. They do **not** establish a new theorem of global priority: the principal ingredients are classical, and the integral-surface implication is an instance of the published speciality/liaison lemma. The quadric assertion is also explicitly recognized in the literature. The combined refinements and the extra (4,4) consequence are presented without novelty claims. [DGF, CE]

The unresolved case is not “an arbitrary singular degree-a surface.” It requires a jump to a lower-degree integral surface, with all degree-a equations reducible or nonreduced, together with an actual smooth embedded specialization from the complete-intersection component.

## 2. Previous work and source verification

The full supplied upstream report was inspected, not just its summary. Its numerical, subcanonical, ACM, smooth-surface, and quadric arguments were identified. Its limitations explicitly say that it had not obtained the full Ellia–Hartshorne 1999 chapter. Its label `partially_solved` is consistent with the limited theorem it actually proves; it does not certify the full AIM question.

Read-only checks of AlecKriebel/Math found:

- the exact queue entry still `queued`, `0/5`, on the inspected main branch;
- no default-branch attempt directory at `unsolved_math_prioritization/attempts/20000814` (GitHub returned 404);
- no ID-matching branches or pull requests, and no exact-ID or “specializations” code-search hits.

These are bounded search results, not a claim that every unindexed, deleted, or privately held user attempt has been excluded. No repository files, branches, or pull requests were changed in this investigation.

The AIM PDF was readable through the web tool, but a byte download returned HTTP 403. No AIM byte hash is invented, and no successful page-image inspection is claimed. The Di Gennaro–Franco arXiv PDF was downloaded, its ten-page text extracted, and the relevant theorem, lemma, proof, and reference list inspected; its exact byte hash is recorded in SOURCE_METADATA.json. The original Ellia–Hartshorne chapter was located bibliographically, but a full readable chapter was **not** obtained. Its contents are not represented as inspected.

Targeted later-literature searches found no verified proof or characteristic-zero counterexample to the exact full question. This is not an exhaustive current-status certification. The 2012 work on specialization to extremal curves permits singular special fibers; the 2024 work on abstract limits of plane curves changes the embedding issue. Neither settles this embedded P^3 problem. The positive-characteristic bundle constructions and their warning about interchanging limits are useful controls, not characteristic-zero counterexamples. [HLS, DS, KPR]

## 3. The five approaches

### Approach 1: preserve the actual geometric data

Flatness gives the degree and arithmetic genus. Smoothness of both geometric fibers gives a smooth proper family over the trait. Connectedness of the geometric fibers is locally constant; the complete-intersection fiber is connected, so C is a connected smooth curve, hence integral.

Set e = a+b-4. The relative line bundle omega_(C_R/R)(-e) is trivial on the generic fiber. A rational trivializing section has a vertical divisor. Since the special fiber is integral, the divisor is an integer multiple of that fiber, which is the principal divisor of t. Thus omega_C = O_C(e). Full details, including the ACM implication, are in PROOFS.md, Sections 1–2.

**Outcome:** the old numerical/subcanonical/Rao reduction is valid. Neither smoothness of the curve nor subcanonicity alone gives ACM. Semicontinuity permits a jump of Rao cohomology at the special point.

### Approach 2: replace “smooth surface” by “integral surface”

The Hartshorne–Serre construction gives a rank-two vector bundle E on P^3 with

0 -> O -> E -> I_C(a+b) -> 0,

and Chern classes c1(E)=a+b, c2(E)=ab. An irreducible degree-a equation lifts to a section of E(-b). A divisorial zero would factor that equation; the only possible entire factor is excluded by H^0(E(-a-b))=0. The section therefore has no divisorial zero. Its second Chern class is zero, so it has no zeros at all. Its resulting extension of two line bundles splits, and C is CI(a,b).

This short argument is written out completely in PROOFS.md. It agrees with Di Gennaro–Franco's Lemma 2 specialized to T=P^3, which requires an integral containing surface, not a smooth one. [DGF]

**Outcome:** the previous report's restriction to singular containing surfaces is much weaker than what the classical tools yield. A minimal degree-a equation would be irreducible, so any counterexample must have c < a.

### Approach 3: classify subcanonical curves on quadrics

For a smooth quadric P^1 x P^1, the vanishing of H^1(O(j,j)) for every integer j lets the subcanonical trivializing section lift from C to the quadric. Intersecting its effective zero divisor with C forces the two bidegrees of C to agree, except for a ruling line, which is already a complete intersection.

For a quadric cone, use its resolution F_2. If the strict transform has class rE+nF, smoothness of C makes its intersection with the exceptional section either zero or one. In the latter case n=2r+1 and g=r(r-1); the subcanonical divisibility n | (2g-2) forces n=1. In the former case the class descends to a multiple of the hyperplane section, hence C is cut out by the quadric and another form. Reducible or double quadrics reduce to plane curves.

**Outcome:** every smooth integral subcanonical curve contained in a quadric is a complete intersection. Together with c < a this proves all a <= 3. This quadric fact is classical and is explicitly used in Chiodera–Ellia, page 419. [CE]

### Approach 4: isolate the residual obstruction and equation jump

Lift a minimal degree-c equation to a section of E(c-a-b). Minimality excludes any divisorial zero. Its zero curve Z has the degree and canonical bundle listed above. Since c<a<=b, its canonical twist is at most -6. A reduced degree-D projective curve has at most D connected components and hence arithmetic genus at least 1-D. But the required Z has genus at most 1-3D. Thus Z cannot be reduced. A pure locally Cohen–Macaulay degree-one curve is a line, so D=1 is impossible. This proves the (4,4) case and rules out c=a-1 when a=b.

Bézout gives an independent exact constraint: because deg C=ab>cm for m<=b, every degree-m equation through C contains the integral degree-c surface. Hence the fixed-factor assertion and the exact dimension jump.

**Outcome:** concrete necessary conditions, not an existence or nonexistence theorem for the remaining nonreduced residual curves. Ribbons and other multiple curves can have negative arithmetic genus, so the negative value is not by itself a contradiction once reducedness is absent.

### Approach 5: test the deformation shortcut and characteristic shortcut

An explicit family is supplied in PROOFS.md, Section 6. Its generic fiber is a smooth CI(2,2), while its central fiber is a smooth plane cubic together with a transverse line. The central fiber is singular and is not a complete intersection. A Hilbert–Burch resolution proves flatness and constant Hilbert polynomial; exact rational Gröbner calculations certify that a t=1 fiber and the plane cubic are smooth.

This is a **negative control**, not a counterexample to the question. It demonstrates why flatness, the CI Hilbert polynomial, and the openness of the CI locus do not prove closedness along an arbitrary limit. Separately, the control program expands the characteristic-two difference-of-squares identity used in KPR: the equality available modulo 2 is genuinely different over Q. The literature explicitly warns that the corresponding flat-limit operations do not commute. [KPR]

**Outcome:** no remaining shortcut from openness, generic ACM, or characteristic-p examples solves the characteristic-zero smooth-special-fiber problem.

## 4. Verification and limits

Run `python verify_controls.py` from this directory. The checked-in result records **43,052 exact checks**, including seven projective Jacobian unit-ideal computations, 1,620 CI numerical types, 1,001 odd-degree cone checks, and 7,434 residual numerical triples. These finite calculations are regression controls for the displayed identities; the proofs of the general partial statements are mathematical, not inferred from finite sampling.

The first run of the control program exposed a structural-expression comparison in the Hilbert–Burch minor test; replacing it with expanded polynomial equality made the check compare the intended polynomials. No failed mathematical identity was suppressed. The final program exits nonzero on any failed assertion.

External foundational inputs are named openly: cohomology of projective space, smooth proper connectedness, Hartshorne–Serre correspondence, the zero-section Chern-class formula, adjunction, Hilbert–Burch, and the standard resolution of the quadric cone. PROOFS.md explains their exact uses. This is neither a formal proof-assistant verification nor a claim of human peer review.

**Stopping point:** five substantive approaches have been completed. No full proof or characteristic-zero smooth counterexample was obtained. It remains to exclude or realize a smooth subcanonical C with 3<=c<a in the closure of the CI(a,b) locus; a numerical candidate or a nonreduced auxiliary Z does not establish that closure condition.

## References

- [AIM] Izzet Coskun, recorder, and Li Li, editor, *Components of Hilbert Schemes*, AIM problem list, Problem 13, PDF p. 2. https://aimath.org/WWN/hilbertschemes/hilbertschemes.pdf
- [EH] Philippe Ellia and Robin Hartshorne, *Smooth specializations of space curves: questions and examples*, in *Commutative Algebra and Algebraic Geometry*, Lecture Notes in Pure and Applied Mathematics 206 (1999), 53–79. Bibliographic location: https://books.google.cat/books?id=KI7AcWnNOA4C . Full chapter not obtained.
- [DGF] Vincenzo Di Gennaro and Davide Franco, *A speciality theorem for curves in P^5*, arXiv:math/0507162v1 (2005), especially Theorem A and Lemma 2; Geometriae Dedicata 129 (2007), 89–99. https://arxiv.org/abs/math/0507162 ; https://doi.org/10.1007/s10711-007-9197-x
- [CE] Ludovica Chiodera and Philippe Ellia, *Rank two globally generated vector bundles with c1 <= 5*, Rend. Istit. Mat. Univ. Trieste 44 (2012), 413–422, especially p. 419. https://rendiconti.dmi.units.it/volumi/44/230.pdf
- [KPR] N. Mohan Kumar, Chris Peterson, and A. Prabhakar Rao, *Degenerating families of rank two bundles*, especially Sections 3–4. https://www.math.wustl.edu/~kumar/papers/KPRProceeding.pdf
- [HLS] Robin Hartshorne, Paolo Lella, and Enrico Schlesinger, *Smooth curves specialize to extremal curves*, arXiv:1207.4588. https://arxiv.org/abs/1207.4588
- [DS] Kristin DeVleming and David Stapleton, *Smooth limits of plane curves of prime degree and Markov numbers*, J. Éc. polytech. Math. 11 (2024), 683–731. https://www.numdam.org/articles/10.5802/jep.263/
- [H] Robin Hartshorne, *Lectures on Deformation Theory*, 2004 author notes, Theorem 9.4 and Corollary 9.5 (openness/unobstructedness direction). https://math.berkeley.edu/~robin/math274root.pdf . These notes are not identical in numbering or contents to the later 2010 book.
