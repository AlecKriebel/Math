# Corrections and nonblocking recommendations

No blocking mathematical correction is required. No frozen file was edited.

## C1. Manifest exclusion is broader than the documented root-manifest exception

- Location: public/verify_manifest.py, actual-file comprehension.
- Finding: `p.name != 'SHA256SUMS.json'` omits a file with that name at **any depth**. In an isolated copy, adding `unexpected/SHA256SUMS.json` still produced a passing check.
- Current impact: none on the frozen inventory. A separate strict inventory check confirms there are exactly the nine declared payload files, the root manifest, and pre-existing Python bytecode caches. There is no hidden nested manifest.
- Suggested future fix: compare `p.relative_to(root).as_posix()` to the one root filename, and either restrict cache exclusions to actual .pyc files or document the broader exclusion. Recompute the release manifest after changing the verifier.
- Severity: nonblocking integrity hardening. This does not invalidate the frozen hashes or the mathematics.

## C2. Audit-state assertion intentionally verifies a pre-audit snapshot

- Location: public/verify.py, `status['independent_audit'] == 'pending'`.
- Finding: changing STATUS.json to an audited state will make the otherwise unchanged control script fail. This is not evidence of a mathematical regression.
- Current impact: none; the frozen package correctly reports its state at freeze and the separate audit gives the later disposition.
- Suggested release handling: keep the frozen snapshot and append the audit, or deliberately update the assertion and release metadata together, regenerate hashes, and rerun controls. Do not silently edit a frozen file or merely update its hash.
- Severity: nonblocking release-management note.

## C3. Prefer the exact primitive condition in the residual-target sentence

- Location: public/PROOF.md, Section 8, “construct a nonlinear g”.
- Suggested wording: “construct a holomorphic g whose nonlinear primitive F=int exp(g) belongs to A while exp(g) does not belong to A”.
- Reason: this aligns literally with Proposition 1 and avoids conflating nonconstant g with nonlinear g. It is not a counterexample to the current claim: affine g yields an entire primitive bounded on the closed unit disk and therefore cannot satisfy the target.
- Severity: optional clarity only.

## Scope clarification

The audit request mentioned an expanding high-modulus Jordan-barrier/path-crossing argument for Proposition 8. The frozen Proposition 8 instead contains a valid direct radial-crossing argument. Proposition 6 is the separate closed-barrier theorem. No missing Jordan-barrier premise needs repair in Proposition 8.
