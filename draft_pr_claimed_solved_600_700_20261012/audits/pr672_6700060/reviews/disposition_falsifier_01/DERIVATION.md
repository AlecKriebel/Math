# Independent falsification of the PR672 prior-containment and disposition candidate

Reviewer: `/root/pr672_disposition_falsifier`. Begun 2026-10-15T05:43:30Z. This is an independent assessment of a proposed disposition, not a declaration that a PR has been closed. I did not read either current priority family's final findings before deriving this report. The controlling native statement, complete application, complete authored analytic verification and complete historical audit were read. The fresh parent mathematics/priority assessments and proposed comment were challenged rather than taken as premises. No source file, branch, queue, PR or cloud object was changed.

## 1. Claim actually submitted and original target

The native controlling guide and RELEASE_STATUS assert a credited, recent-preprint-based affirmative result for ambient-smooth, face-preserving maps with ambient-smooth inverse and nonsingular derivative through every corner. They expressly disclaim a new discovery and exclude broader corner-singular or merely facewise/interior-smooth maps. Turns are 1/5; this is not a claim of five failed independent proof mechanisms.

Gromov2017 printed60 gives the original comparison: a compact full-dimensional convex polyhedron P is extremal against combinatorially corresponding convex competitors whose corresponding dihedral angles all weakly decrease. It asks whether an extremal P also excludes face-corresponding diffeomorphic Euclidean domains whose faces have nonnegative mean curvature, whose corresponding angles weakly decrease, and where one angle strictly decreases at one ridge point. The full page was read textually and visually. It does not itself spell out the entire category at a nonsimple corner. Accordingly this review retains the submission's narrower explicit category; it does not certify that category as the only interpretation of the original question.

The closure candidate does retain that category in its first mathematical sentence, credits a correct scoped deduction, and says the broader category is not declared resolved. It does not claim a counterexample to the submission or pretend that lack of a broader result invalidates the scoped deduction.

## 2. Exact positive prior match

Bi2026 v1 printed1 defines an arbitrary compact convex polytope P in R^n with nonempty interior, an irredundant affine halfspace representation, and a smooth metric g on a neighborhood. Printed2 fixes outward normals and exterior angles. Theorem1.1 for n>=3 assumes nonnegative scalar curvature on P, nonnegative outward face mean curvatures, and exterior dihedral angles at least the Euclidean values along every codimension-two face. It explicitly concludes equality of the normal inner products on each nonempty closed intersection of distinct facets, in addition to flatness and totally geodesic faces. I read and visually inspected the complete page, including its hypotheses and displayed final conclusion. No restriction to simple polytopes, acute angles or an upper dimension is present.

Public arXiv v1 metadata independently inspected in this review identifies 6 August 2026, predating the native October5 record. The sufficient priority fact is this identified, public theorem and its exact mathematical containment. Neither a database label nor absence of search hits supplies that fact.

| Submitted datum | Transfer to the source theorem | Exact limitation |
|---|---|---|
| Compact, full-dimensional convex Euclidean P | Same polytope in Bi | No broader nonconvex reference claimed |
| Ambient-smooth F and inverse through all corners | g=F*e is smooth and positive definite on P and extends positively to a neighborhood | A merely smooth interior bijection is insufficient |
| Euclidean competitor | R_g=0 on the interior and by continuity on P | No curvature hypothesis outside P is needed |
| Face-preserving F and nonnegative outward competitor face mean curvature | Isometry preserves outward side, connection and second fundamental form, so H_g>=0 | No prescribed metric relative to the reference Euclidean faces is inserted |
| Each interior angle theta'<=theta | alpha_g=pi-theta'>=pi-theta=alpha_0 | Supplement reversal is essential |
| Strict angle decrease at one ridge point, including a ridge endpoint | Bi's equality of normal Gram entries holds on every closed facet intersection; hence no strict point remains | A mere flatness conclusion would not suffice |
| Nonsimple corners | Permitted by the source's arbitrary irredundant convex polytope hypothesis | Does not imply arbitrary combinatorial maps are ambient-smooth |
| Reference P is extremal in Gromov's sense | Additional unused hypothesis | Source yields a stronger all-P statement in the submitted smooth category |

## 3. General pullback bridge, checked without source-proof circularity

At each interior point, g(v,w)=<DFv,DFw> is positive definite. Smooth F and inverse yield inverse derivatives there; continuity of the chain rule extends their product identity to each boundary point, so DF remains nonsingular through all corners. Each local ambient extension gives a smooth positive-definite tensor after shrinking its open neighborhood. On overlaps these tensors agree on P; a finite partition of unity on a neighborhood forms a positive-definite extension agreeing with g on P. Since tensors agree on the dense interior, the relevant one-sided jets agree at all boundary points as well.

The local isometry to the Euclidean competitor proves R_g=0 in the interior. Smooth continuity passes that to P. Because F carries the interior side to the interior side of a corresponding face, it carries its outward metric normal to the competitor's outward unit normal. Levi-Civita invariance gives the identical second fundamental form and trace. For adjacent faces, normal inner products and their continuously defined closed-ridge limits are preserved. Supplementary interior/exterior angle conventions then give exactly the inequality Bi requires. His explicit Gram equality contradicts any strict interior inequality. This bridge uses no compactness theorem beyond the finite extension construction, no distance or volume comparison, and no WXY theorem.

In local linear coordinates with derivative A, G=A^T A. For a source defining covector u, the normalized g-normal pushes to A^{-T}u/|A^{-T}u|. The identity

    u^T G^{-1}v = (A^{-T}u) dot (A^{-T}v)

confirms the metric/Euclidean normal correspondence. This is valid even if det A<0; the outward side is determined by the defining inequality, not an orientation convention on A.

The central analytic work establishing Bi's theorem is expressly imported. The native analytic note and historical audit expand its smoothing, spherical normal interpolation, critical logarithmic trace estimate, smooth Dirac index input and limiting spinor argument. Those detailed verifications can be valuable independent checking. They do not turn the source theorem into an authored original theorem. In particular the elementary observation that a nonzero spinor suffices to cancel a scalar Gram difference is a proof clarification of an already stated source conclusion; it is not a newly resolved part of the target.

## 4. Low dimensions supply no novelty escape

For a planar polygon, total exterior turning equals2pi. A piecewise smooth embedded disk with nonnegative face curvature and smaller interior corner angles has exterior-corner turning at least2pi, strictly greater if any angle strictly decreases. Adding nonnegative smooth-arc curvature cannot restore total2pi. This is the classical turning/Gauss-Bonnet calculation, correctly signed: for counterclockwise traversal and outward normal, <D_T nu,T>=k, positive on a circle. It proves the planar case without a novel mechanism.

There is also a direct reduction to the same prior theorem. On P times[-1,1], use g+dt^2. Scalar curvature is R_g; side mean curvatures equal the planar arc curvatures because the new tangent direction contributes zero; end facets are totally geodesic. Old vertex-angle comparisons become side-facet comparisons along vertex times interval. New end/side exterior angles are exactlypi/2 for both reference and product metrics. All are smooth neighborhood metrics. Bi in dimension3 forces the old normal Gram entries to agree. This shows the all-dimensional claim requires no uncredited low-dimensional theorem beyond classical geometry and a routine metric product. Dimension1 has no codimension-two angle at which a strict violation could occur.

## 5. Attempts to defeat the priority/disposition inference

**Preprint is not accepted literature.** Public priority and journal validation are different assertions. The source's identified August preprint already states the stronger exact theorem; recent/unrefereed status does not make a derivative claim historically independent. Whether the source proof is ultimately valid remains a mathematical question. Here the accepted math gate has independently audited the needed route; this review checks implication, not a replacement full PDE audit. If a source error were found, the novelty question would reopen only with a repaired genuinely new proof. No such error or repair is supplied. The comment correctly refrains from claiming journal acceptance or consensus.

**Maybe the literal Question64 sentence is not printed in Bi.** Exact earlier printing of that sentence is unnecessary for this narrower conclusion. The hypothesis map is a short direct application of an explicit stronger theorem, including the decisive angle equality. The comment does not assert a literal earlier Question64 answer or adjudicate the first historical solver.

**Maybe the ambient interpretation is too narrow.** That limits both the submission and the matched prior theorem. The correct broader claim is left unverified. Enlarging the category would require a theorem or a reduction that preserves a smooth positive metric. For example F(x,y,z)=(x^3,y,z) on a positive half-box is a smooth bijection with smooth interior inverse, but its pullback diag(9x^4,1,1) degenerates at x=0. Relabeling it a corner diffeomorphism does not satisfy Bi. Conversely restricting to ambient-smooth maps does not create novelty, since the explicit prior matches that entire restricted claim.

**Maybe the detailed verification is itself a publishable contribution.** It may be publishable as a credited audit or exposition, subject to a different editorial goal. The closure candidate acknowledges its usefulness and does not call it mathematically erroneous. Under the present process of publishing a new original-problem resolution, attribution and proof checking alone do not meet originality. I see no authored mechanism in the controlling theorem statement, application or analytic note that escapes the identified prior containment. The wording correctly distinguishes a possible expository note from a repair establishing a new target result.

**Maybe disputed WXY versions matter.** They are unnecessary for this source match. The current comment neither validates nor refutes them and does not rely on them for the disposition. Thus uncertainty over those versions cannot rescue originality or invalidate this prior implication.

**Maybe the PR should be reclassified already_solved.** That is a repository vocabulary decision separate from mathematical priority and not needed for this closure. The proposed comment does not change any queue row, respects the original source/status qualifications, and does not allege the submitter hid the source.

## 6. Finite diagnostics and exact remaining boundary

The accompanying47 exact controls check nonorthogonal pullback normals, positive definiteness, interval-product old Gram entries and new orthogonality, loss of positivity at a degenerate corner, turning deficits and interior/exterior reversal. Normal and optimized runs are byte-identical and use explicit failure branches, not removable Python assertions. They illustrate and guard algebraic signs in this derivation; they do not prove a PDE theorem, community acceptance or historical novelty.

No mandatory or optional correction to the current closure candidate was identified. The exact accepted conclusion is a defensible rejection of new-original-problem-resolution priority, preserving a valid credited result in the stated smooth category. No PR disposition has been executed by this reviewer. It remains impermissible to expand this verdict to every corner category, to an unqualified historical first-solver claim, or to a judgment about journal acceptance.
