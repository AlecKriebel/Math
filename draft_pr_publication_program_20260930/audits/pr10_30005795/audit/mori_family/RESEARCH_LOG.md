# Mori/divisorial geometry independent audit log

Scope: frozen `source_snapshot/BOUND.md`, head `925f9e9f46f2c7407fd142cedf36995a4519a378`. Read no previous verdicts. Audit Section 3, including Mori dream space finiteness, endpoints, the coefficient of S, restriction to S, and signed intersection weights. Do not alter canonical files, snapshots, or queue; no Git mutations or external communications.

## 2026-10-01 04:36:01 UTC — Start, 5% complete

Read frozen BOUND.md. Exact target claim: smooth complex Fano X and the report's normal Du Val prime surface S should yield finitely many fixed prime divisors E_j != S with bounded nonnegative coefficient functions over `[0,tau]`; restrictions E_j|S must be effective Cartier, and the corresponding valuation-weight integrals must be finite. Treat model-dependent positivity separately from restriction existence.

Independent route: reconstruct the finite-cone geometry directly, test endpoint linear equivalence rather than only numerical effectivity, and check the report's actual definitions of P and N. Primary sources requested: BCHM Corollary 1.3.2, Okawa Section 2.3, and official OWR report. AMS viewer currently inaccessible through browsing; alternate primary copy to be located.

Strongest verified result so far: only the conditional finite-sum setup is stated clearly; the geometric justification remains under audit.

## 2026-10-01 04:38:03 UTC — Geometric reconstruction, 65% complete

Checked primary Okawa arXiv v2 Section 2.3 and propositions 2.8/2.13. The chambers are **closed** rational polyhedral cones covering the effective cone, not only an interior decomposition. Negative parts on the relevant small modification are effective exceptional divisors; strict transforms give a finite set of prime divisors on X. Chamber coefficient maps are Q-linear; uniqueness on rational overlaps makes their real extensions agree. Therefore endpoint walls do not generate a missing support or unbounded coefficient issue.

Checked published BCHM numbering through the AMS primary PDF's indexed content. The published Mori dream result is Corollary 1.3.2, while arXiv v2 labels the same result 1.3.1. The source citation is correct; do not mistake the preprint numbering difference for a mathematical gap.

Independent argument in progress: H ample gives `tau <= (-K_X.H^2)/(S.H^2)`, hence compactness. Finite Cox generation yields rational endpoint and Q-effective representative. The endpoint/convex-combination argument then correctly excludes S; linear/numerical equivalence is the only exposition detail to make explicit. Effective Cartier E_j != S restricts effectively because O_S is a domain and the restricted local equation is nonzero.

New boundary observation: in the exact smooth Fano **threefold** setup every movable divisor is nef. This follows from divisorial/fiber-type extremal contractions and choosing an effective member that avoids the relevant exceptional divisor. Consequently P(u) itself is nef on X; signed-weight treatment is unnecessary for this precise dimension. A separate adversarial geometric falsifier was assigned to test the endpoint and movable-to-nef implications without reading prior verdicts.

Strongest verified result: finite support, bounded coefficients, endpoint exclusion of S, and effective restrictions have a checkable proof under the ordinary Mori dream fixed-part interpretation. No counterexample found. Remaining audit gap: independently verify the stronger threefold positivity argument and write the exact proof/assessment.

## 2026-10-01 04:43:08 UTC — Full reconstruction recorded, 95% complete

Wrote `REPORT.md` with a complete finite-cone/endpoint proof, local Cartier restriction argument, the distinct movable-to-nef proof, and the exact scope of the signed-weight clipping inequality. Wrote a provisional machine-readable verdict. The boundedness assertion can be verified directly on each closed chamber; continuity at rational and real walls follows from the uniqueness of the normalized fixed divisor.

The internal falsifier's initial response independently supports both endpoint and movable-to-nef implications, while observing that the coefficient-of-S statement would be false outside the explicitly intended nonnegative parameter segment. No such enlarged claim occurs in frozen BOUND.md. Its final artifact is pending.

Temporary primary-source downloads are confirmed ignored by Git. Frozen BOUND.md has SHA-256 `dd4b6addb46edc8532362d35cecf5a3316dfcf27d9795306f9d34ebac3c8f450`. No canonical files, snapshots, or queue entries were edited; no Git mutation or outside communication was performed.

Strongest verified result: Section 3 passes in its exact smooth Fano threefold/prime normal surface scope. Recommended changes are expository, principally making endpoint Q-linear effectivity explicit and marking the signed-weight discussion as a generalization.

## 2026-10-01 04:46:40 UTC — Independent falsifier complete, 100% complete

Read the finalized internal geometric falsifier report. It independently verifies the rational effective endpoint/Pic_Q bridge and S-avoidance for the exact `[0,tau]` segment. It also checks the supplemental positivity route using Wiśniewski's original 1991 fiber-locus inequality, Theorem (1.1), p.143. No central step is transferred to an equivalent unsupported claim.

The boundary stress test `X=Bl_p(P^3), S=E` gives `sigma_E(-K_X-uE)=-u-2>0` for `u<-2`, but the candidate makes no claim there. Its `tau=2` endpoint is non-big and fits the verified argument. This is recorded as a successful scope test, not a blocker.

Parent requested acceptance remain centered on the candidate's finite support proof and signed-weight safeguard. `REPLACEMENT.md` supplies exact replacement prose and primary evidence with that scope; `Mov(X)=Nef(X)` remains supplemental. Final machine-readable verdict is `pass_with_expository_clarifications`.

Strongest verified result: finite nonnegative integrals and effective Cartier restrictions hold in the exact smooth Fano threefold/prime normal surface/Mori dream fixed-part setup. No mathematical blocker remains. Remaining discovery work is outside this audit: no novelty, priority, LCT proof, or full K-stability formula certification is claimed here.
