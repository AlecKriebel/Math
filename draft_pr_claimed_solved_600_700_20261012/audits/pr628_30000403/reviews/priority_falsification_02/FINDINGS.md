# Adversarial falsification of the proposed PR628 priority implication

Review completed: 2026-10-15 UTC. Exact timestamps and SHA256 bindings are in `SOURCE_BINDINGS.json` and `VERDICT.json`.

## Verdict and scope

**The proposed mathematical implication survives independent falsification.** The full scoped upper bound in PR628, including its degree-one statement for geometric stabilizer V4, follows by a short homogeneous-space deduction from prior compression theory. In fact the deduction gives degree one for every noncyclic geometric stabilizer. No unresolved mathematical bridge remains in this implication.

This is a priority/substantiveness finding, not a reversal of mathematical acceptance. I found no reason to reopen the parent mathematical gate. I have not claimed that either Bresciani paper explicitly states the identical Hurwitz theorem, that the packet copied its proof or coordinates, or that a comprehensive historical-first search has been completed. An application of a general theorem can be a new observation; what fails here is support for presenting the already subsumed universal bound as a substantive new resolution. The distinction must remain in any public disposition.

The reviewed target is exactly the ordinary **inner coarse** lifting problem at head `677673860f9e67dffc610f52384f0bd60e65e363`, characteristic zero, at least three distinct branch points, and a base field containing the field of definition of the Hurwitz datum. Actual marked-cover descent, positive characteristic, an effective pointwise algorithm, and the best bound for each fixed datum are outside the packet's claim.

No other subagent's report was read. My independent derivation was checkpointed in `INDEPENDENT_DERIVATION.md` before this verdict; the parent closure candidate was read only after that checkpoint. No Git mutation, remote write, external communication, or modification outside this assigned review folder was performed.

## Proof and hypothesis map

Write H=PGL2 over k. Let X be the ordinary coarse Hurwitz space, let x be the specified rational point of its reduced geometric quotient, and let F be the reduction of the scheme-theoretic fiber over x.

### B01. The orbit descends, and possible nilpotents do not obstruct the argument — closed

The fiber is already defined over k. Since k has characteristic zero, it is perfect, and reduction of a finite-type k-scheme is geometrically reduced. The geometric quotient premise says that the geometric underlying fiber is a single H-orbit. The reduced orbit has its usual homogeneous-space scheme structure. Thus F over the algebraic closure is H/E, where E is the geometric stabilizer of the coarse cover point. Equivalently one can descend the invariant reduced geometric orbit directly; neither construction needs a rational point of F.

The reduced orbit and the entire geometric fiber have identical field-valued points. Any morphism from a field into a scheme annihilates nilpotents. Consequently a K-point constructed in F is a K-point of the original ordinary coarse Hurwitz fiber. A nonreduced scheme fiber is therefore harmless. The word “non-reduced” in the source's Hurwitz terminology has the separate pre-quotient meaning already clarified in the packet.

The stabilizer E is finite because it acts faithfully on the branch divisor: a projective transformation fixing every one of three distinct branch points is the identity. In characteristic zero its scheme structure is reduced and étale. Thus H/E is smooth. No classification of finite subgroups is required here.

This step uses the source/packet's geometric quotient premise. It does not silently replace a categorical quotient with a geometric quotient. In the Hurwitz setting all orbits have dimension three and the stable configuration-space construction provides precisely the stated geometric quotient.

### B02. The quotient gerbe is finite étale — closed

Let G=[F/H]. Geometrically G is BE. The orbit F has a point over a finite separable extension of k; after that extension its quotient gerbe is the classifying gerbe of the finite étale stabilizer. Hence G is a finite étale gerbe over k by descent. This assertion does not require G to be neutral over k, nor E to be a constant group over k.

### B03. The associated family has faithful projective-line inertia — closed

Form U=[(F×P1)/H] with the diagonal action. The map U→G is representable, smooth and proper, with geometric fiber P1. After choosing a geometric object of G, the family is the projective line with the E-action induced by E⊂H. That inertia action is faithful. Its geometric total stack is [P1/E].

These are exactly the abstract universal-family data admitted by Bresciani 2303.01409v2, Definition 5 and Lemma 6. Theorem 2 places them in its structure/compression correspondence. One need not prove that an actual marked-cover stack has faithful inertia on its target. We constructed the needed abstract structure from the **coarse orbit** itself.

### B04. The coarse compression is a conic — closed

The stack U has finite inertia. Its coarse space Y exists, and geometrically it is P1/E. Quotients of P1 by finite groups in characteristic zero are smooth projective genus-zero curves: the invariant function field is rational, and a quotient of a smooth curve by a finite group has a smooth coarse curve. These facts also follow by the tame quotient construction. Formation of the coarse space commutes with the field extensions used here. Therefore Y is a smooth projective genus-zero k-curve, possibly nonsplit. Its anticanonical plane model is a smooth conic.

This conclusion concerns the coarse curve Y, not the universal P1 over the gerbe. Confusing these two curves would invalidate the split-target argument; the construction keeps them distinct.

### B05. A nonempty free open exists and is a scheme — closed

Every nonidentity element of E fixes finitely many geometric points of P1. The union of their fixed loci is finite, so the locus of trivial inertia in U is a nonempty open. Let Y0⊂Y be its image. Over Y0, the stack U is its coarse space: after the geometric trivialization this is the free finite quotient P1_free/E, and the assertion descends. In particular Y0 is a nonempty k-open, with finite complement.

### B06. The rational map has exactly the geometric fibers demanded by Proposition 2 — closed

The inverse of the coarse map on Y0, followed by U→G, gives a morphism Y0→G and therefore a rational map Y⇢G. Pull it back along any geometric object Spec(kbar)→G. The result is P1_free, a nonempty open of P1. Its geometric fiber is irreducible, with smooth projective completion of genus zero. This is precisely the genus-zero-fiber condition for rational maps used in Bresciani 2211.03438v1, Proposition 2. It is not merely an assertion that Y itself has genus zero.

### B07. A compression point gives a lift on the specified split line — closed

This was the strongest possible obstruction to the proposed implication. Let K/k be any field extension and choose y∈Y0(K). Under Y0⊂U it corresponds to an H-torsor T over K with an H-equivariant morphism T→F×P1. The P1 component is a K-point of the associated Brauer–Severi curve C_T. A smooth genus-zero curve with a rational point is P1, and H1(K,PGL2) classifies these curves. Thus T is a trivial H-torsor. Choosing a trivialization and evaluating the F component at the identity gives f∈F(K).

This is strictly stronger than neutrality of G. For example, when E=1 the gerbe G is already neutral even if F is a nontrivial PGL2-torsor, whereas Y is the nonsplit associated conic and has no rational point. The argument above correctly detects that case. It never infers a split base from gerbe neutrality alone.

Bresciani's 2023 Theorem 2 alone only identifies descent to some twist, as the text before Definition 15 explicitly warns. The additional torsor calculation is therefore logically necessary. It is short, uses the standard torsor/conic correspondence already used by PR628, and is the formal coarse-homogeneous counterpart of the split-P1 criterion proved for divisors in Bresciani's 2022 Lemma 11 (pp.7–8).

### B08. A degree-at-most-two point can avoid the excluded locus over every characteristic-zero k — closed

If Y is split, its rational points are infinite and meet Y0. Otherwise embed Y as a smooth plane conic. In the dual plane remove the closed set of tangent lines and the finitely many loci of lines through a geometric boundary point of Y\Y0. This is a proper closed set defined over k. Because k is infinite, a k-line exists outside it. Its intersection with Y is reduced, degree two, and contained in Y0. As Y has no k-point, this intersection is a single closed point of separable degree two. Thus Y0(K) is nonempty for some [K:k]=2.

Characteristic zero supplies both perfectness and infinitude; no assumption that k is a number field, algebraic over Q, real closed, or finitely generated was used. In particular no general period-equals-index assertion for two-torsion Brauer classes was used: the class is a conic class from the start.

Combining B07 and B08 gives the entire universal upper bound for all finite geometric stabilizers, including cyclic and trivial ones.

### B09. The noncyclic, and in particular V4, improvement exactly satisfies Proposition 2 — closed

Suppose E is noncyclic. If Y(k) were empty, apply Bresciani 2211.03438v1, Proposition 2, to P=Y and Φ=G. The required hypotheses are: a field k; a smooth projective geometrically connected genus-zero curve Y with no k-point; a finite étale gerbe G; a rational map Y⇢G; and geometrically irreducible genus-zero fibers. B02, B04 and B06 establish all of them. The conclusion forces the geometric band of G to be cyclic. But G over kbar is BE, so that band is E up to the usual inner ambiguity; cyclicity is unaffected by that ambiguity. This contradicts noncyclic E.

Hence Y(k) is nonempty. It is split, Y0(k) is nonempty, and B07 gives F(k) nonempty. V4 is noncyclic, so the exact PR628 refinement follows. No additional hypotheses about a constant band, a k-rational normalizer section, a cyclic character, an actual cover object, or a distinguished branch point appear in the proposition.

There is an independent elementary verification. For a tame finite E-action on P1 of degree n>1, let the branch indices be e1,...,et. Riemann–Hurwitz gives sum(1−1/ei)=2−2/n, so t≤3. If t=2, then 1/e1+1/e2=2/n; since ei≤n, both indices equal n. The group fixes the two ramification points, hence is a finite subgroup of the multiplicative group and is cyclic. The cases t=0,1 give no nontrivial noncyclic action. Thus a noncyclic E has exactly three branch values. Their reduced divisor descends to Y as the image of the intrinsic inertia locus in U and has degree three. A conic admitting an odd-degree divisor is split (by its degree-two index, or directly by Riemann–Roch). This again proves the noncyclic improvement. It does not assume the branch divisor of the original cover has stabilizer E.

### B10. The actual-cover center is invisible for the right reason — closed

The geometric stabilizer used throughout is Stab_H(f) for a point of the inner coarse Hurwitz space. It may be strictly smaller than the group preserving the branch divisor. Central deck automorphisms of an actual marked cover act trivially on its coarse point; they are absent from this H-stabilizer. Since E is literally a subgroup of PGL2, its action on the auxiliary line is faithful. Replacing G with an actual-cover residual gerbe would introduce another band and might break this argument, but no such replacement was made. The conclusion remains a coarse lift, exactly as asserted in the packet.

### B11. Boundary and limiting cases — closed

- E=1 is allowed; the construction reduces to the familiar PGL2-torsor/conic bound and does not incorrectly prove degree one.
- Cyclic E can have a nonsplit compression; the proof asserts degree at most two, not universal degree one.
- Every noncyclic E gives degree one. This includes V4, all noncyclic dihedral groups, A4, S4 and A5, without using a classification in the proof.
- Split Y with boundary entirely nonrational still has free rational points, since only finitely many points are removed.
- A nonreduced coarse fiber has the same field-valued points as its reduction.
- The arguments permit nontrivial Galois action on E and on its quotient line.
- The theorem does not extend as written to r<3 or to wild characteristic; those cases are outside the target.

## Strongest valid mathematical conclusion

The reconstructed argument proves the following general statement, which is stronger than the PR's upper-bound statement:

Let k have characteristic zero and F be an H=PGL2-homogeneous k-space with finite geometric stabilizer E. Form the conic Y as above. For every field extension K/k,

    F(K) is nonempty  if and only if  Y(K) is nonempty.

The reverse implication is B07 plus infinitude. For the forward implication, a point f∈F(K) defines a morphism P1_K→U_K→Y_K, so any rational point of P1_K maps to a K-point of Y. Consequently the minimum degree of a closed point of F equals 1 if Y is split and 2 otherwise. If E is noncyclic, Y is necessarily split.

Thus even a proposed repair phrased as an abstract compression-conic criterion or as the improvement for all noncyclic strata is already the same short prior-theory consequence. Producing explicit equations or an efficient algorithm for Y for specific Hurwitz data would require additional work, but none is supplied in this packet.

## Prior sharpness and what was actually stated earlier

The primary source *Lifting results for rational points on Hurwitz moduli spaces*, author manuscript GPGL2.pdf, Remark 3.14 (p.15), explicitly records necessity of the degree-two bound in cyclic stabilizer examples. It uses G=C2 and identifies the cover-point stabilizer with the divisor stabilizer for the stated double covers. Its displayed examples have larger branch number; I do not misattribute the packet's exact six-point Q(i) coordinates to Cadoret. Since the global universal constant ranges over all r and all characteristic-zero fields, those earlier examples already supply its lower bound. The fresh retrieval of this manuscript hash-matched the supplied primary copy.

For six-point divisors specifically, Bresciani's 2022 introduction attributes examples for every even n≥6 to Marinatto 2013; the publisher's primary abstract independently confirms failure of split-line descent for even cardinality outside four. The full Marinatto paper was not obtained in this review. I therefore use Cadoret's directly inspected mathematical sharpness statement for the decisive universal lower bound, and label the six-point Marinatto attribution as contextual rather than a newly reverified explicit construction. This does not leave a gap in the universal-priority argument.

The dated material supports this precise claim: by 2023 the general structure/compression machinery, the cyclic-band obstruction, the split-family rational-point mechanism, and known quadratic lower bounds suffice for a short proof of the full scoped universal result. The Hurwitz application and its torsor explanation are deductions written here. The source statements must not be upgraded to a quotation of an identical published Hurwitz theorem.

## Reasonable salvage analysis

1. The packet's elementary normalizer proof and its elliptic realization of arbitrary S3-action on V4 remain mathematically useful alternate proofs. A different proof of a short existing consequence can have expository value; the current record establishes no further independently novel resolution beyond that consequence.
2. The exact six-point arithmetic certificate remains a checkable construction. New coordinates or executable verification do not restore novelty of the universal constant, whose lower bound was already known. This review makes no claim that the exact coordinates previously appeared anywhere.
3. Strengthening the claim to all noncyclic stabilizers does not repair novelty: B09 already gives that stronger result from the same prior proposition.
4. Determining optimal bounds for specified fields, groups, classes, branch counts or individual points would be a different research result; the packet expressly excludes it and supplies no new theorem establishing it.
5. Actual marked-cover descent when a center remains is a different obstruction problem, which the packet also expressly excludes. It cannot be promoted as a completed repair without new proof.
6. Positive characteristic, explicit compression equations, complexity bounds and constructive algorithms would likewise require new assumptions or new work. They are possible future questions, not resolved salvage routes in this PR.

There is therefore no concrete, verified repair in the present packet that retains the claim to a substantive novel resolution of the original bound question. Preserving the proof and certificates as exposition or verification artifacts is reasonable, but it is a change of contribution type.

## Closure candidate check

I read only the parent `CLOSURE_COMMENT_CANDIDATE.md`, after independently recording the derivation. Its mathematical and priority wording is appropriately qualified: it calls this an explicit implication and expressly says the identical theorem is not stated verbatim in the sources. I found **no mandatory factual edit**.

The parent applied all five optional precision suggestions: “every nonempty open of a conic”; an explicit PGL2-torsor; Bresciani 2022 Lemma 11 (pp.7–8); the verified Cadoret author-manuscript locator alongside the publication DOI; and bibliographic spaces. I reread the revised candidate in full. These optional closure-comment issues are **resolved**, with no pending closure edit or unsupported factual claim found. The final revised bytes are bound in the verdict.

## Remaining issues

Mandatory unresolved issues: **zero**.

Optional limitations: (O01) earliest historical priority is not determined by this bounded audit; (O02) historical originality of the exact example coordinates and alternate proof is not certified. These limitations prohibit overstatement about literal prior publication, copying, or the absence of every possible small new artifact. They do not defeat the established short implication or repair the universal-resolution claim.
