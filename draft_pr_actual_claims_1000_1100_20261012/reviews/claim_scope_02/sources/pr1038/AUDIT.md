# Independent audit of the reconstructed KP 4.6 detector obstruction

Edition note: this is the full written mathematical audit of the reconstructed input identified below. Its mathematical review sections 1–8 are unchanged. The scope/method and final packaging history have been edited only to distinguish the earlier auxiliary computation from this proof-only edition. REPORT.md is an editorial descendant, not the exact byte sequence named in the original audit decision; see PROVENANCE.md.

## Decision

**ACCEPTED, with no mathematical correction or scope narrowing required.** This is a fresh independent acceptance of the reconstructed turn 3 report dated 2026-10-09. The exact audited report is 20,665 bytes, with SHA-256:

`2f098576972c6847af448217f0a37730c2cc55126c785722d40625fbe71ea174`

Acceptance is confined to the ordinary-invariant obstruction actually proved. It does not solve KP 4.6, establish that the test boundaries have no exotic fillings, establish that any proposed pair is diffeomorphic, or exclude refined detectors. The problem remains **UNSOLVED, 3/5 turns**. This is an audit of the reconstructed third approach, not another approach. No historical acceptance or equality with a missing historical artifact is asserted.

At the time of this audit, the reconstructed report and its supporting files were not changed. Their pending-audit statements described the pre-audit state; the decision supplied acceptance for the exact reconstructed input above. No mathematical correction overlay was necessary. The present REPORT.md updates that chronology and includes a written elementary derivation of its already stated Cartan arithmetic; this audit did not originally review those later editorial bytes.

## Scope and method

I independently read the entire frozen report, inspected the six cited primary-source PDFs at the locations recorded in `INSPECTION_MANIFEST.json`, checked their local byte counts and SHA-256 hashes against the supplied source manifest, replayed the arithmetic program in normal, `-O`, and `-OO` modes, and independently computed determinants, principal minors, and Smith normal forms using SymPy. The then-existing candidate ZIP was checked entry by entry against the frozen companion files. These are historical supplementary checks, not a claim that this proof-only edition contains that archive or executable companions, or that those computations were rerun during edition preparation.

This is a mathematical source-and-proof audit, not a formal proof in a proof assistant or a new proof of the published gauge-theory foundations. Source results are accepted as the cited mathematical inputs after checking their statements, hypotheses, coefficient conventions, and the relevant constructions. The original target's scope was checked against the audit assignment; I did not claim a new retrieval of the original Kirby problem text or a literature-wide status search.

## 1 Original target and local boundary convention

The report correctly states the target as an absolute exotic pair of compact connected orientable smooth 4-manifolds with the prescribed closed orientable 3-manifold as their entire boundary. The prescribed boundary may be disconnected. Infinite families and simple connectivity are not requirements.

The connected rational-homology-sphere assumption is explicitly confined to the detector propositions. It is not substituted for the original universal target. The report does not confuse relative non-diffeomorphism fixing a boundary marking with absolute non-diffeomorphism.

The conventions on a cap are consistent: its boundary is the oppositely oriented test manifold, and an allowed boundary identification reverses induced boundary orientations. Since the boundary is connected and closed extra components are excluded, the relevant pieces and their closure are connected.

## 2 DLM family, signs, and nonempty filling class

The relevant DLM input is Theorem 2 on printed page 3357. Direct visual inspection is essential because plain-text extraction omits minus signs. The PDF defines P as the boundary of the negative E8 plumbing and O as the boundary of the negative E7 plumbing; the family is mP # k(-O), with m at least 1 and k greater than 8m. The report uses exactly those signs. The theorem excludes both positive- and negative-definite smooth fillings without a first-Betti-number or fundamental-group hypothesis. Printed page 3359 removes rational first homology by surgery within its proof; it does not impose that condition on the initial filling. [DLM](https://msp.org/gt/2024/28-7/gt-v28-n7-p09-s.pdf)

Boundary-connected summing m copies of the negative E8 plumbing with k orientation-reversed negative E7 plumbings gives the asserted filling and form. The sign reversal makes each E7 block positive. The verified determinants are 1 and 2, respectively. The independent Smith forms are eight unit factors for E8 and six unit factors followed by 2 for E7. The plumbing homology sequence therefore yields the stated boundary homology, rather than merely its order.

For m=1 and k=9 the form has positive index 63, negative index 8, rank 71, absolute determinant 512, and boundary first homology (Z/2)^9. This shows that the universal quantifiers over fillings are nonvacuous. The arithmetic does not purport to compute Floer groups.

## 3 Indefiniteness, arbitrary first homology, and rank zero

The real homology sequence of a filling with rational-homology-sphere boundary makes H2(A;R) to H2(A,boundary A;R) an isomorphism. Poincare–Lefschetz duality then gives a nondegenerate real intersection form even if H1(A) is nonzero. For a positive-rank form, the absence of one sign would make the form definite, contradicting DLM. Reversing the filling orientation deals with the negative test boundary.

The separate rank-zero argument is sound. An interior connected sum with CP2 preserves the prescribed boundary and would turn a rank-zero form into a nonzero positive-definite form. Thus the conclusion does not depend on whether a zero-dimensional form is called definite. Both indices are at least one for every filling and cap under the report's conventions.

Real Mayer–Vietoris identifies the second homology of every closure with the direct sum of the second homologies of its two pieces. The vanishing of both H2(Y;R) and H1(Y;R) is exactly what is needed. Cycles can be pushed into their respective interiors, so cross terms vanish. This proves the orthogonal direct sum and indices at least two independently of the gluing map and with arbitrary first homology in the pieces.

## 4 Integral L-space and individual Spin-c conclusions

The integral input is legitimate. OS Definition 1.1 requires a free abelian hat group of the prescribed rank, Section 2 gives the reduced-group characterization and closure under orientation reversal and connected sum, and Proposition 2.3 includes elliptic manifolds. P and O have the requisite elliptic geometry. Consequently the reduced plus group vanishes over Z, as does the reduced minus group. Vanishing of the direct sum implies vanishing in each Spin-c summand. No mod-2 calculation has been promoted to an integral assertion. [OS L-spaces](https://arxiv.org/pdf/math/0303017v2)

The distinction between H1 and H^1 is handled correctly. Although the example has nontrivial 2-torsion in H1, H^1(Y;Z)=0. Integral cohomological Mayer–Vietoris therefore makes restriction on H^2 of the closure injective. Applying the affine H^2 action to Spin-c structures proves uniqueness of a global extension when its restrictions are fixed. It does not assert existence for an arbitrary incompatible pair of restrictions. The report consistently starts with an existing global structure, so individual vanishing does not come from cancellation in an extension sum. The same reasoning applies to the internal S3 cut.

## 5 Relative mixed map for a transplant

For T=W#E, placing the removed ball in E produces the stated cobordism order: twice-punctured E first, then once-punctured W. The first piece has positive index by the donor hypothesis, and the second by the indefiniteness result. Their common S3 has zero integral H^1. Thus the cut satisfies Definition 8.3, including its coboundary condition, and the total positive index is at least two. The mixed construction passes through the zero reduced Floer group of S3, and cut independence applies.

The claim includes the complete ordinary insertion domain. This is explicit in the displayed mixed-map definition on page 66. As additional checks, Theorem 3.1 and its construction on pages 24 and 43 introduce the exterior-algebra cobordism maps, and Proposition 4.20 with its proof on pages 45–46 verifies class-decorated composition. Across the internal sphere, first homology is an integral direct sum; every exterior monomial distributes between the two pieces. U is already part of the minus input module. These facts rule out an accidental proof only for the insertion 1. [OS four-manifolds](https://arxiv.org/pdf/math/0110169v2)

This proof does not require the outgoing boundary to be an L-space once W has positive index. That observation in the report is correct. No inference about hat maps or other Floer variants is hidden here.

## 6 Closed OS vanishing for every cap and every gluing

For an arbitrary filling A and cap C, puncturing one ball in each gives the test manifold itself as a positive-positive admissible cut. Its reduced integral Floer homology vanishes. The entire mixed map is therefore zero, and so is the coefficient defining the closed invariant. OS Theorem 10.1 states the corresponding individual-Spin-c conclusion directly. The variable-name mismatch in its opening line does not alter the proof or the intended restriction to the boundary.

The insertion argument is also integral. The map from H1(A;Z) direct sum H1(C;Z) onto H1(X;Z) is surjective because the next H0 map is injective for this connected gluing. Its kernel is an image of the finite group H1(Y;Z), hence is torsion. A surjection with torsion kernel induces an isomorphism after quotienting by torsion: if an element maps to torsion, a multiple lies in the finite kernel, so the element itself is torsion. Thus the report's exterior-algebra decomposition has no finite-index gap. U-powers and all such monomials remain within the zero mixed-map factorization.

The total positive index is at least two, so there is no chamber-dependent b2+=1 closed invariant being used. The statement genuinely covers all the allowed fillings, caps, and boundary identifications.

## 7 Seiberg–Witten vanishing and component selectors

The SW conclusion is correctly restricted to capped connected-sum transplants. Interior connected sum commutes with boundary gluing here, giving X=E#N with N=W glued to C. The previous topology gives b2+(N) at least two; E has positive index. These are exactly the useful hypotheses, regardless of the three first Betti numbers.

The crucial source support is present in KM. The disjoint union of configuration spaces indexed by Spin-c structures and the pullback products are given on page 456; Proposition 23.2.2 on page 457 permits arbitrary cohomology classes on that union. Definitions 27.1.6–27.1.7 on page 555 connect componentwise evaluation with the summed notation. Definition 27.3.3 on page 562 and the composition proof on pages 563–565 retain general cohomology classes, not merely the undeformed sum or real first-Chern-class weights. [KM](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/kronmrowka.pdf)

Here is the independent verification of the report's use of those inputs. A degree-zero cohomology class on a disjoint union can be the characteristic function of one Spin-c component. Hence e_sE and e_sN are legitimate integral cohomology classes, including when several structures have the same real first Chern class. Since the cut is S3, restriction identifies at most one global Spin-c structure with any fixed pair of restrictions. For the restrictions of the chosen global s, the pullback product of the two selectors is exactly e_s. This removes every other term individually, including torsion-distinct structures.

For twice-punctured E, the ends have the standard S3 Spin-c structure. The positive-index perturbation argument excludes reducible solutions; decorating an empty reducible moduli space cannot create a contribution. With the round S3 data, there are no irreducible critical points at the ends, and its ordinary check map is consequently zero for every selected component and every inserted cohomology class. KM page 560 explicitly gives the same vanishing for class-decorated ordinary maps. Proposition 27.2.4 and the following uniformity remark justify the perturbation mechanism. Equivalently, the exact triangle and the surjective bar-to-check map give the stated conclusion. The missing slash in the text extraction of Proposition 3.5.2 was resolved by visual inspection: the hypothesis is nonzero positive index.

Put twice-punctured N first. Its index at least two makes its mixed map canonical in the range actually stated by Theorem 3.5.3. Follow it with twice-punctured E, whose ordinary check map is zero. Class-decorated mixed composition therefore vanishes. No canonical mixed map for a stand-alone index-one donor is assumed.

Finally, H1(E#N;Z) is the integral direct sum of the first homologies of E and N. The configuration-space cohomology description includes the exterior classes for arbitrary b1 and the degree-two U class. Every ordinary insertion is a sum of products coming from the two factors, with U placed on either side. Multiply these products by the component selectors and use the zero composition term by term. Proposition 27.4.1 then identifies evaluation with the chosen individual ordinary SW invariant. This proves exactly the report's arbitrary-b1, torsion-sensitive, all-ordinary-insertion assertion. Narrowing it to b1=0 or to a Spin-c sum is unnecessary.

No isomorphism between Heegaard Floer and monopole Floer invariants is invoked to obtain an all-fillings SW assertion. The proof and its scope remain separate from the stronger all-closures OS result.

## 8 Ordinary maps, attribution, and surviving gap

Section 8 correctly separates undecorated plus/minus maps from mixed maps. For the former, infinity-map vanishing and exact-sequence naturality combine with surjectivity at the incoming L-space and injectivity at the outgoing L-space. This argument is not stated as a hat-map theorem or a result for twisted, local-coefficient, stable, or families invariants.

EMM Remark 1.8 already proposes the connected-sum route and describes stabilization and ordinary-invariant difficulties. The report gives it credit and distinguishes EMM's infinite-family ambition from the exotic pair required here. [EMM](https://arxiv.org/pdf/1901.07964v3)

The final gap is correctly preserved. A solution still needs appropriate homeomorphic fillings and a proof of absolute non-diffeomorphism for every prescribed boundary. Equal zero ordinary invariants supply neither that proof nor an obstruction to the existence of such a pair. No theorem resolving the current literature-wide problem is claimed.

## 9 Historical reproducibility and present packaging

During the independent audit, all six source PDF hashes and sizes matched their recorded values. Three arithmetic executions, in normal, -O and -OO modes, exited successfully and gave byte-identical recorded output. Independent determinant, principal-minor and Smith-form calculations agreed. The then-existing archive contained exactly its six designated files, with every payload matching its frozen counterpart. These remain historical descriptions of supplementary checks; no checker, standalone arithmetic output, fixture, log or archive is part of this edition, and no new arithmetic execution is claimed here.

The mathematical arguments and all qualifications in sections 1–8 above are retained in full. The present REPORT.md makes the elementary Cartan arithmetic readable as a derivation. The gauge-theory conclusions depend on the written topology and cited source theorems, not on finite arithmetic checks.

The present ACCEPTANCE.md records the accepted partial scope and original reconstructed input identity. INSPECTION_MANIFEST.json retains the source-inspection history. MANIFEST.json inventories only the present proof-only files. Source documents, extracted text, rendered pages and coordination material are not included.

The original audit made no publication, queue edit, new turn or alteration of its frozen input. This editorial preparation likewise adds no proof-search turn and proposes no queue change.
