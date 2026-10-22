# Independent adversarial review of the actual-outcome gate

Completed: 2026-10-17T09:36:27.383737-07:00 (America/Los_Angeles).
Completion estimate: **100% of this eligibility audit**, not of the mathematical review/publication program.

## Verdict

**No actionable gate findings remain.** The final lower and upper gates agree with my independent eligibility decisions on every PR from #1100 through #1200 inclusive. The 14 PRs to forward to the original rigorous review process are:

**#1102, #1108, #1114, #1118, #1119, #1121, #1129, #1135, #1136, #1141, #1142, #1150, #1151, #1155.**

The other 87 entries are excluded: 68 explicitly leave the full original target unresolved or accept only a scoped/partial result; 19 expressly attribute the full target's resolution to prior work. No queue status was read or used in this review. These classifications identify recorded claims; they do not endorse mathematical validity or establish priority.

## Independent derivation and evidence

Before opening either `lower/OUTCOME_GATE.json` or `upper/OUTCOME_GATE.json`, I independently read the outcome passages in all 101 saved PR bodies. All bodies are nonempty. I also read only outcome/credit passages from the retained #1138, #1140 and #1148 records when examining the prior-result boundary. I saved the independently derived candidate list and per-PR quotations, body hashes, and head SHAs in `INDEPENDENT_GATE.json` before comparing the two existing gates.

My initial categories placed #1168 and #1198 with the expressly prior accepted results. On comparison, the upper gate more precisely labels them partial for the **full original** target, because stronger original naturality and the broader literal K3 category are not certified. I accepted that labeling clarification and preserved the initial classifications and explanation. Both were excluded throughout; no candidate was added or removed.

I then checked all 101 records, numeric problem IDs, pinned head SHAs, categories and eligibility decisions against the independent map and saved metadata. #1157 is mapped through the body's explicit GREEN-012 / ID102 statement, rather than mistaking the code suffix 012 for its numeric problem ID. Every saved body is exactly the matching `PR_OUTCOME_METADATA.json` body plus one appended newline. All 150 quoted passages in the final lower/upper gates occur verbatim at their recorded line ranges. The independent receipt additionally records source hashes and line ranges for its own quotations. The #1148 fallback README hash and pinned-head provenance agree.

`FINAL_VALIDATION.json` binds this final comparison to the exact lower/upper gate hashes and records no remaining discrepancy. It records the inventory timestamp and the final counts. PR body hashes identify the textual snapshots; the separately recorded head SHAs identify the corresponding Git result.

## Adversarial scope cases

- **Complete special cases:** #1111, #1112, #1128, #1130, #1156, #1157, #1160, #1161, #1176 and #1195–#1200 were challenged against the stated original target. Their complete subtheorems, broader-formulation counterexamples, single-clause answers or restricted categories do not fill the explicitly recorded original gap. #1156, for example, proves the maximum-equality clause while expressly leaving the combined gap question unresolved. #1176 refutes the variable-base extension while explicitly leaving original base 2 unresolved.
- **Existential and negative answers:** #1108's single example is expressly claimed to answer the original existential question; a universal every-cone theorem is unnecessary for that target. Likewise the admitted parameter choices in #1150 and the characteristic-zero instance in #1155 are claimed counterexamples to universal assertions. Their limited parameter choices alone are not reasons to exclude them at the claim gate.
- **Prior ingredients versus prior full resolutions:** Generic no-novelty/no-priority language did not exclude #1102, #1114, #1136, #1141, #1142, #1150 or #1151. Their sources are recorded as ingredients or narrower antecedents, while full original-target deductions are expressly claimed. #1129 remains eligible because its published first clause is accompanied by an asserted complete authored Motzkin-clause deduction. The independent receipt quotes that second clause as well as the full-resolution heading.
- **The #1148 boundary:** Its full all-degree target cannot be excluded merely because it follows from an imported theorem or disclaims novelty. The additional pinned README expressly calls it a “credited prior-result implication” and a “credited consequence of prior work.” That express outcome framing supports the prior-only exclusion. #1138 and #1140 likewise expressly record a historical or published full prior resolution. Their mathematical correctness and historical sources were not audited here.
- **Body versus outcome status:** The selected retained STATUS/ACCEPTANCE outcome fields agree with the bodies. No partial-status/full-body contradiction changes eligibility. #1114 expressly records full resolution; #1141's source-credited-corollary status still states the exact target; #1142 accepts the stated two-boundary-component negative result. Whether each matches every hypothesis in the original problem remains part of its later mathematical audit, not a reason to suppress an explicit full claim here.

## Finding corrected

The initial lower gate falsely said that #1138, #1140, #1141 and #1142 had empty PR bodies. Their actual saved bodies contain 2,534, 3,143, 3,397 and 3,764 bytes respectively, and all match the inventory. I reported this concrete documentation defect to the parent. The lower classifier corrected `OUTCOME_GATE.json`, `REVIEW.md` and `build_gate.py`, added body quotations, and retained the correct eligibility decisions. I checked the corrected wording and final quotations. **Resolved; no change to the 14-candidate list.**

## Boundaries of this review

This work inspected outcome language and scope only. It did not audit mathematical arguments or priority sources for excluded entries, read other worker audits, change PRs, comment externally, merge, close, prepare papers, upload, update the tracker, or commit. All outputs of this review are confined to `gate_reviews/independent_01/`. The next step is the original rigorous mathematical and priority process, beginning with #1102.
