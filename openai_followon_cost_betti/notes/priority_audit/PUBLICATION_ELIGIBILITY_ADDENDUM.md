# Addendum: publication eligibility and exact prior duplication

Checkpoint: 2026-10-06, 9:35 p.m. America/Los_Angeles (2026-10-07 04:35 UTC). Bounded priority audit completion estimate: 98%. Mathematical resolution and publication eligibility remain conditional on the independent proof audits. This addendum preserves the original `AUDIT.md` and corrects/qualifies its public-disclosure search result.

## Newly verified explicit prior disclosure

The proposed short theorem-chain deduction is **already literally public in this researcher's own preliminary triage record**, not merely inferable from OpenAI and Gaboriau. The public [AlecKriebel/Math commit `387962dc519c86b1d1833cb0a41bd3fbddd2b446`](https://github.com/AlecKriebel/Math/commit/387962dc519c86b1d1833cb0a41bd3fbddd2b446), dated October 6, 2026, 9:00:30 p.m. PDT (October 7, 04:00:30 UTC), includes:

- [REPORT.md, section 7](https://github.com/AlecKriebel/Math/blob/387962dc519c86b1d1833cb0a41bd3fbddd2b446/openai_followon_triage_20261006/REPORT.md): exact target β₁(R_X)=0 and C(R_X)>1, identifying the height-action limit and action invariance.
- [Algebra/group notes, first ranked path](https://github.com/AlecKriebel/Math/blob/387962dc519c86b1d1833cb0a41bd3fbddd2b446/openai_followon_triage_20261006/agent_notes/algebra_groups_probability.md): the same target and derivation.
- [Independent cost proposal check](https://github.com/AlecKriebel/Math/blob/387962dc519c86b1d1833cb0a41bd3fbddd2b446/openai_followon_triage_20261006/agent_notes/physics_operators_topology.md), near the end: an explicit proof with 0≤β₁(Γ)≤99/M for every M, limiting to zero, transfer to the Bernoulli orbit relation, β₀=0, no ergodicity requirement on Y_M, and the infimum-group-cost boundary.

I fetched all three pinned raw files and verified byte equality with the provided local triage files. The API history snapshot is `local_project_public_triage_history.json`, and the fetched-file hashes/retrieval timestamps are in `web_source_manifest.json`. In this checkout the triage directory is untracked, so local history alone would have missed the public earlier remote commit. The audit now expressly includes it.

The triage declares itself a research agenda and makes all implications conditional on the upstream theorem surviving validation. It is **not** an unconditional certified source of the claimed fixed-price counterexample. It nevertheless publicly records the complete short conditional argument. Its provisional status does not erase that disclosure.

## Extent of duplication

| Proposed content | Prior public extent | Legitimate added claim |
|---|---|---|
| Exact Γ and Bernoulli/height actions | All in OpenAI family 259 | Citation and checked hypothesis verification |
| Two cost bounds, existential positive η | All in OpenAI Theorem 1.1 | Verified dependency audit; no independent cost discovery |
| β₁=0 via low-cost actions and the limit M→∞ | Explicit in the researcher's public triage; classical invariance/inequality | Completed validation record, not a new theorem-chain proof |
| Cost–Betti strictness for R_X | Explicit conditional statement in that same triage; logically implicit in upstream | Consequence accurately attributed to upstream |
| Failure of fixed price implies a cost–Betti counterexample | Explicit in PSV Remark 6.6 by 2018; immediate from Gaboriau | No new logical bridge |
| An explicit rational η satisfying OpenAI's parameter constraints | No such fixed rational specialization found in inspected source/triage | A reproducible specialization/check; insufficient by itself for a novel theorem |
| A direct L²-invariant computation for this exact amalgam, independent of the low-cost limit | Not found in inspected OpenAI source, triage, or primary citation chain | A separate detailed proof, **if** fully established and independently audited |

The absence of printed Betti terms in family 259 does not justify novelty; the positive gap's fixed rational specialization does not create a new counterexample; and a clean agent verdict does not turn source-derived mathematics into an independent discovery.

## Recommendation under the user's actual protocol

The prompt expressly asks for a short consequence note and permits an immediate newly available corollary. It also forbids a duplicate preprint advertised as a new solution when the entire result and proof are already public. These provisions can be satisfied without either overclaiming or treating preliminary notes as an unconditional completed theorem.

**Do not publish a paper consisting only of the already public three-line cost–Betti argument plus a numerical choice of η as a new solution.** That exact conditional argument has been disclosed. A change from provisional wording to a theorem, without a successful upstream proof audit, would be invalid; a change to polished layout after validation would not establish new mathematical priority.

**If the upstream inputs survive the full focused audits, and the final package includes a fully proved direct invariant computation for this Γ together with reproducible source-validation evidence, a publication as an expanded consequence/verification note is defensible within the user's expressly requested product.** The entire proposed proof package would then not be identical to the public triage: it would include a separately checkable argument and the validation absent from that preliminary record. This is publication of the completed form of the researcher's earlier observation, not another independent fixed-price discovery. The new contribution must be identified as an explicit invariant calculation/alternative proof and dependency verification. The target counterexample and essential cost estimate remain inherited. An explicit rational η helps make the example checkable but is supporting content, not the principal originality basis.

This is a **qualified go** for a completed consequence/verification note with that actual extra proof and sound upstream input; it is a **no-go** for a duplicate basic inference marketed as a newly solved open problem. If the direct computation reduces to the very same cost-limit proof, or the upstream cost lower bound has a material unresolved gap, this qualification fails. Then preserve the audited partial result and obstruction and withhold the requested full-solution Zenodo deposit.

The manuscript, abstract, Zenodo description, README, and tracker should use the same restricted framing. A suitable description is: “An explicit consequence of OpenAI's fixed-price construction, with a direct calculation of the first L²-Betti number and an independently checkable verification record.” Its introduction should acknowledge the earlier public triage commit and avoid “first”, “new solution”, or an independent-resolution claim. It must plainly distinguish logical priority from this note's verification and presentation contribution.

I have not inspected the proposed direct computation itself in this addendum. Its validity and whether it is substantively separate from the existing proof must be resolved by the mathematical reviewers before relying on this qualified recommendation. No publication action is certified by this audit alone.

## Earlier comparison announcement

The original audit began detailed numbered results in 2002. An earlier [Gaboriau announcement, *Sur la (co-)homologie L² des actions préservant une mesure*](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/CRAS-Cohom/CRAS-Cohom.pdf), *C. R. Acad. Sci. Paris Sér. I Math.* **330** no. 5 (2000), 365–370, author PDF pp. 1–2, already announces β_i(R_Γ)=β_i(Γ), a group cost comparison, and the lack of known strict examples. This puts the comparison/background by 2000. For precise full relation-level hypotheses and proofs, retain the numbered 2002 results in the dependency ledger. The inspected 2000 PDF hash is `1009925c9e43b0397dac811ab90f74c112b8470e5eec6f3d59f3e1fad2c5f169`.
