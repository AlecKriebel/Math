# Early independence seal: primary source, scope, provenance family

Sealed UTC: 2026-10-02T00:24:51.268215+00:00. Agent: /root/pr30_primary_scope_provenance_adversary.

Before sealing I read applicable repository AGENTS instructions, independently fetched the primary sources identified below, inspected literal OWR Problem 12 and its printed-page pixels, and read only candidate PARTIAL.md. I have NOT read original review, readiness, code, results, attempts, history, sibling-family files or parent reports. Candidate PARTIAL SHA256: ab85b2029c8f4e0e931aeac63ea42aad1a6a2e34f7425428e1f9224fd5bddd43. No proof-search attempt was made; this audit uses zero attempts. No contact with any individual. Local branch observed main.

## Exact target and success criteria

Primary source: New Trends in Teichmüller Theory and Mapping Class Groups, Oberwolfach Reports 15 (2018), 2475-2534, report 40/2018; workshop 2-8 September 2018; DOI 10.4171/OWR/2018/40. Printed 2528, PDF ordinal 54 (zero-based 53), Problem 12, Dmitri Gekhtman. Download receipt and SHA256 retained in fetch_receipts.json; source PDF/text/page PNG privately in tmp/source_fetch.

Target: for every finite cover from a genus h surface to a genus g surface with h > g >= 2, find an embedded four-holed sphere H with all boundary curves essential in the base whose lifted interior has more than one connected component. Three-holed-sphere variant and restriction to regular covers are explicitly asked separately. The source's motivation concerns a conditional nonretraction result for the induced Teichmüller embedding, not a proof of universal existence of H. Source does not say 'pairwise nonparallel' boundary; genus-2 parallel copies of nonseparating cut curves are allowed. Interpret cover here as connected unbranched cover of closed oriented surfaces as in PARTIAL; degree d satisfies h-1=d(g-1). Essential means non-nullhomotopic in the closed base.

Exact criterion to audit: for a transitive monodromy action rho on d points, the number of lifted components equals the number of rho(pi1(H))-orbits. For a regular action this equals its index in deck group. Properness is insufficient in a general irregular action. Full target would require universal intransitivity for some H; neither 'kernel contains a simple curve' nor a universal trivial-monodromy H may be assumed.

## Genuine dependencies and optional background

Candidate partial proofs depend on basic covering classification/orbit lifting, primitive integral homology represented by simple nonseparating curves, cut systems and incompressible planar subsurfaces, surface Euler characteristic, and elementary finite-group arguments. These need direct derivations or independently checkable controls. They do not depend on compatible SL2 pants or Teichmüller submersions.

Funar-Pagotto primary source: Braided surfaces and their characteristic maps, arXiv:2004.09174v2, revised 20 Apr 2023; NYJM 29 (2023), 580-612. Independently read Theorem 1.2 (PDF 2), Theorem 5.1 and Proposition 5.1 (PDF 17), Proposition 5.2 and its proof through PDF 18. For every g >= 2 they construct infinitely many finite simple nonabelian characteristic quotients with no essential simple-loop classes in the kernel. The quoted existence uses quantum representations/strong approximation (Theorem 5.1 invokes [13]); no independent reproof of those deeper existence dependencies is claimed. Their finite-order simple-loop argument takes finitely many mapping-class orbit representatives and sufficiently large reduction primes q to retain order p; characteristicness transports this to all simple curves. This is a genuine external dependency only for the stated limitation of the trivial-monodromy strategy. It is not a counterexample to Gekhtman's target: nontrivial proper rank-3 images can still yield disconnected regular lifts.

Compatible pants primary source: Detcherry, Le Fils, Santharoubane, DOI 10.4171/GGD/797; online-first PDF copyright 2024, published 1 Oct 2024; final journal Groups Geom. Dyn. 19 (2025), no. 3, 861-877. Definition 1.1 and Theorem 1.2, PDF 1: irreducible SL2(C) or SO3 representations admit compatible pants; restrictions remain irreducible and boundary traces avoid +/-2; sausage type has Q8 exception. This controls representation-theoretic properties and does not supply permutation intransitivity or any finite-cover criterion. It is optional background, not a partial-proof dependency.

Gekhtman-Greenfield primary source arXiv:1901.02586v2, 7 Apr 2019, Isometric submersions of Teichmüller spaces are forgetful. Theorem 1.1 assumes holomorphic Teichmüller-isometric submersion and nonexceptional positive-genus target (2k+m >=5, k>=1), concluding same genus and a forgetful map. It does not establish disconnected inverse images of H or resolve the exact topological existence target. Gekhtman thesis 2019, defended 9 May 2019, Two Holomorphic Extremal Problems in Teichmüller Theory, DOI 10.7907/XKMM-8591: abstract/Table of Contents identify low-dimensional retract and submersion work; no universal finite-cover conclusion is inferred. Author research webpage lists related analytic papers and is only a bounded search check, not evidence that no later resolution exists.

## Falsifiers fixed before legacy evidence

1. Proper subgroup still transitive (natural S3 action, A3) falsifies misuse of regular refinement in an irregular cover.
2. Genus-2 H requiring four pairwise nonparallel boundaries would incorrectly narrow the source; two essential annular parallel pairs are admissible.
3. Trivial-monodromy general claim would contradict the cited nongeometric kernels; mere proper subgroup target does not.
4. Primitive integral lift must have gcd 1; any coordinate rescaling/lifting gap must be checked.
5. Large-genus band sum must genuinely be embedded, nonseparating and represent a_j a_k^-1 with coherent base paths; trivial boundary images then require an actual planar free generating set.
6. Source checks based on string/section counts cannot certify a deleted or invented proof.
7. Unique raw catalog identity, preserved SQL TEXT '{}' versus NULL, exact candidate blob identities and a true exact-file diff must be separately checked. Global program files may evolve after unrelated PRs; mutable mirrors cannot rewrite original-stage provenance.

Best-guess completion: 35% of this audit; 0% claimed progress toward the unresolved full discovery goal. Strongest result at seal: exact source target and its source boundaries established; candidate partial claims unverified until subsequent audit.
