# Independent adversarial audit: 30001242 / OWR-3472-013

Date: 2026-10-04 UTC. Rank: 558.

## Verdict

**PASS. No blocking mathematical or attribution defect found.** The recommended
disposition is **already_solved**, retaining the recorded **1/5 substantive
author turns**. This is a credited explanation of an existing negative answer,
not a newly resolved open problem. The review is an independent AI-assisted
assessment, not formal verification or human peer review.

The ring-independent ordinary-containment assertion is the literal catalogue
claim, and it is already denied explicitly by both cited 2009 primary sources.
The supplied family correctly witnesses this denial with a fixed field,
dimension, embedding dimension, number of generators, and generator degrees.
No conclusion about a broader tight-, Frobenius-, or plus-closure question is
included in this verdict.

## Frozen input and integrity

The reviewed author package consists of the eight files listed in its frozen
manifest plus that manifest itself, for nine files total. The manifest SHA-256
is:

    f21a7d5d214e56c29508b8758b8a80794deeb8ad3c731538a7b359ad2d7ef13e

All eight declared byte counts and hashes match; the frozen directory contains
no additional files. Its contents were not edited. The local primary PDF and
bibliographic metadata hashes also match the source manifest. Details are in
[input_integrity.json](input_integrity.json). The separate audit manifest pins
this report and its original review artifacts.

## Source and quantifier audit

The catalogue record identifies the question as a degree m_0, depending only
on dimension d and the prescribed generator degrees, such that R_(m_0) is
contained in the ordinary ideal of generic forms. Its accompanying generated
literature assessment calls this open. That assessment is contradicted by the
cited primary discussion itself.

1. H. Fischbacher-Weitz, joint with H. Brenner, *Generic bounds for tight
   closure*, Oberwolfach Report 22/2009, printed pp. 1211–1214. The complete
   contribution was reviewed. Printed p. 1212, PDF page 56, distinguishes
   ordinary containment from tight-closure containment and explains that the
   former needs ring-dependent information, already for hypersurface parameter
   ideals. Printed p. 1213 gives an ordinary-containment bound involving a(R).
   See [the report](https://doi.org/10.4171/OWR/2009/22).
2. H. Brenner and H. Fischbacher-Weitz, *Generic bounds for Frobenius closure
   and tight closure*, arXiv:0810.4518v3. The introduction on p. 1 explicitly
   rejects a ring-independent ordinary bound in the parameter case. Construction
   2.2 and Definition 2.3 on p. 8 specify the parameter space and distinguish
   an open-set generic statement, its generic point, and countable genericity.
   Theorem 3.4(c), pp. 12–14, permits dependence on a(R) for ordinary membership.
   See [the inspected version](https://arxiv.org/abs/0810.4518v3).

The two decisive source pages were checked visually, and fresh text extraction
from the PDFs independently confirmed their negative-answer passages. The
companion PDF identifies v3 and the date 30 July 2009. The journal publication
metadata is supplemental; neither publisher full-text equivalence nor a current
web-version claim is needed for this verdict.

Specific ambiguity checks:

- The report uses d for ring dimension; the companion paper uses d+1. Actual
  dimension two is used consistently in the candidate, so the companion
  parameter count is n=d+1=2. The report allows n>=d, including equality.
- The target is vanishing of a graded quotient, equivalently eventual
  containment of all homogeneous elements. It is not a bound on coefficient
  degrees in a representation of an already-member polynomial. The source
  formulas expressly concern the former.
- Allowing a bound for each fixed R, or allowing dependence on a(R), the
  presentation degree, or other ring data, changes the assertion. Such a
  variant is not refuted or declared solved by the packet.
- The source's normality hypothesis belongs to its Frobenius-closure result.
  It is not a missing hypothesis of the arbitrary-standard-graded ordinary
  question. A fixed algebraically closed field of positive characteristic can
  be chosen if one wishes to remain inside the companion paper's ambient
  field convention.
- The negative assertion is already explained in the original discussion;
  the packet has not mistaken an introductory question for a genuinely
  unanswered broader conjecture.

No new network access, repository search, or remote write was performed for
this audit. The package's historical retrieval and repository-search claims
were not independently repeated. They are not needed for the mathematical
verdict. A local source audit cannot certify current remote availability or
exhaustiveness of repository search.

## All-N proof audit

Let N>=2, F_N=x^N-y^(N-1)z, and R_N=k[x,y,z]/(F_N), with degree-one
variables. The following arguments were checked independently of the finite
computations.

### 1. Domain, dimension, grading, and boundary cases

Regarding F_N as a polynomial in z over k[x,y], its coefficients have gcd 1.
It is degree one over k(x,y), hence irreducible there, and Gauss's lemma gives
irreducibility in the polynomial ring. Irreducibles are prime in this UFD.
The argument works over every field extension, including positive
characteristic dividing N: no derivative, separability assumption, or
characteristic-zero factorization is used.

The monic relation in x gives a unique remainder of x-degree less than N.
Consequently k[y,z] embeds, and R_N is free of rank N over this subring.
This supplies a graded Noether normalization and dimension two. It does not
assert that R_N is integrally closed. The relation is homogeneous, and N>=2
ensures three independent degree-one generators. N=2 causes no exception;
N=1 is deliberately unnecessary and excluded from the six-parameter setup.
The case N=0 is outside the construction.

### 2. Genuine generic parameter ideals

For the coefficient rows of two linear forms, their signed-minor vector v is
annihilated by both rows. The polynomial F_N(v) defines a principal open set
U_N in affine six-space. At the pair (y,z), v=(1,0,0) and F_N(v)=1, so the
open is nonempty over every field. Over the fixed infinite field, it is dense
and has the intended rational-point meaning; scheme-theoretic density follows
from irreducibility of affine space.

On U_N the rows have rank two. The map (x,y,z) -> (v_x t,v_y t,v_z t) is
surjective and its kernel is precisely the two-form ideal. Since
F_N(vt)=F_N(v)t^N, the further quotient is k[t]/(t^N), as a graded ring.
The same calculation applies at the generic point and after field extension.
Its Hilbert function is one in degrees 0 through N-1 and zero from N onward.
Thus the exact cutoff is N, with no off-by-one discrepancy, and the ideal is
R_N,+-primary.

This also matches the source's primary-parameter space, rather than merely
some unrelated coefficient open set. A rank-two pair outside U_N leaves
k[t], while a rank-zero or rank-one pair leaves a quotient of a polynomial
ring in at least two variables by at most one equation. Neither quotient is
zero-dimensional. Hence U_N is exactly the primary-pair locus for this family.

Finite-field rational points should not be confused with a dense scheme
point set. This is harmless here: the theorem fixes an infinite field, the
open has an explicit rational witness in every characteristic, and the
below-N obstruction holds for every pair even after field extension.

### 3. Every pair fails below N

For 0<=m<N, the degree-m part of the relation ideal (F_N) is zero. After
quotienting by a linear ideal L of rank r<=2, one therefore has

    (k[x,y,z]/(L,F_N))_m = (k[x,y,z]/L)_m.

The right side is the degree-m piece of a polynomial ring in 3-r>=1
variables. It is nonzero, including m=0 and dependent or zero-form pairs.
This rules out every alternative choice of generic open subset below N.
In particular, nongeneric pairs cannot provide an accidental smaller bound.

### 4. Uniform contradiction and scope

An integer bound B(2;1,1)=M would be contradicted by any N>max(M,1).
Only the defining degree of the ring needs to vary; the field, characteristic,
and six-dimensional parameter-space format remain fixed. Multiplication by degree-one generators propagates containment
from R_M to all higher homogeneous degrees in a standard-graded ring, so the
single-degree and tail formulations agree.

Every particular example nevertheless has finite generic cutoff N. Thus the
construction denies uniformity across rings without claiming the absence of
cutoffs for an individual ring. It neither depends on nonreduced rings nor
claims normality. No external closure theorem is required by the proof.

## Computational audit

1. The frozen verifier was run without editing it. Its output is byte-for-byte
   identical to the frozen checks.json: **3,720 degree matrices and 7,535
   counted assertions**, all passing. The replay is saved as
   [replayed_checks.json](replayed_checks.json).
2. [independent_verify.py](independent_verify.py) is a separately written
   standard-library-only verifier. It does not import or execute author code.
   It reconstructs the same deterministic samples, changes the monomial order,
   and computes relation ranks by incremental sparse elimination.
3. Its independent prediction first solves the two linear relations, substitutes
   the resulting linear forms into F_N symbolically, and uses the polynomial-
   quotient Hilbert function depending on whether this restriction vanishes.
   This also checks all tested degrees for rank-one pairs, where the original
   verifier's general below-N check alone did not give a full tail prediction.
4. All **3,720** independently computed dimensions match. The **626 pair/N
   instances** comprise 324 generic rank-two, 136 exceptional rank-two,
   143 rank-one, and 23 rank-zero instances. The author's labels ending in
   “pair_degree_cases” count pair/N instances, not individual m matrices;
   this is a naming clarification rather than a numerical defect.
5. Coverage is Q with N=2,3,4 and 12 pairs per N; F_2 with N=2,...,6 and
   all 64 ordered pairs; and F_3,F_5,F_7 with N=2,...,6 and 18 pairs per N.
   Cases in characteristics dividing N are included. Results are in
   [independent_checks.json](independent_checks.json).

For a local replay from this directory:

    python3 ../public/verify.py
    python3 independent_verify.py

The finite controls detect implementation and boundary errors in the sampled
cases. They are not an infinite proof, a proof of genericity, or a substitute
for the algebraic argument above.

## Required changes and publication boundary

**Required changes: none.** The author package remains frozen. This audit
supplies the independent-review outcome without rewriting the frozen
pending-review metadata. The one recorded substantive author turn is accepted
as the package's accounting; the audit does not reconstruct an external
interaction history or add a new author attempt.

This audit contains original analysis, code, results, bibliographic links,
and integrity metadata only. It contains no primary-source copies, page
images, extracted papers, catalogue corpus, or machine-specific source paths.
No repository queue, branch, or other remote state was changed.
