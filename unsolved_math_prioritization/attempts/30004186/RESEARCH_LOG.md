# Research log: peaked reduced Ostrovsky waves

Model and effort: gpt-6-astra, xhigh. Start: 2026-09-30 04:48 UTC. Two-hour ceiling: 06:48 UTC. Maximum five substantive responses. Only this problem folder and its dedicated branch may change; no queue generator or shared state is used.

## 04:48–04:51 UTC: source and readiness audit

Read the complete upstream record, attempted the original problem page, and recovered the full OWR report and the two primary Geyer–Pelinovsky papers. Checked current literature and the recent related Hunter–Saxton model. Confirmed the exact distinction between linear/spectral instability and nonlinear conclusions, and the need to state a solution class and stability norm.

No prior project attempt was found in all-state PR, branch, queue, state, attempt-path, or related-target checks. No pinned prior-report entry exists for the OWR code. Completion estimate: 15% toward a full original-target result; source scope verified.

## 04:51–04:59 UTC: substantive response 1/5

Constructed a local Banach-space Lagrangian system on continuous periodic profiles that are C1 on the interval cut at the moving corner. Its vector field uses only first derivatives, is locally Lipschitz uniformly on bounded sets, and preserves physical mean zero. Bounded spatial slopes give continuation. This avoids importing a smoother Sobolev theorem outside its domain.

A narrow perturbation of width delta squared has amplitude O(delta cubed) and changes the right corner slope by minus delta. The exact slope equation is w'=u(q)-w². An L∞ comparison with the traveling wave bounds the true moving-corner forcing. On logarithmic time scales that forcing is smaller than the exponentially growing slope perturbation. The resulting fixed excess in the slope supremum gives orbital W^{1,infinity} departure uniformly over all translations.

Saved the complete scoped candidate and 20 passing exact identity checks. The norm distinction remains central: neither L2 nor H1 orbital instability has been proved, and no conclusion about weak continuation after breakdown is asserted. This is a partial result toward the original source target, not an unqualified solution.

Completion estimate: 90% toward a fully checked strong-norm theorem, pending separate review; approximately 35% toward the broader low-regularity source problem. Historical novelty remains unconfirmed. Candidate frozen for review; no additional proof attempt or full-target promotion.

## 05:03–05:06 UTC: checkpoint and historical correction

The initial checkpoint push was denied because the action reviewer did not find sufficiently specific publication authorization. After the exact user authorization transcript was supplied, the same push was retried once and succeeded. Remote commit 5ada227eee9e4709996d80019ac231c8475b7c47 was verified. No alternate route was used.

The independent reviewer discovered the superseded nonlinear claim in Geyer–Pelinovsky arXiv v1 (April 2018). Its exact Section 4 and the January 2019 version history were checked. SOURCE_AUDIT now preserves that history and distinguishes the candidate's corner-compatible, fixed-threshold argument from the old stronger-norm-to-L2 argument. The mathematical candidate remains byte-for-byte frozen; the review is still pending. Completion estimates and attempt budget are unchanged.

## 05:09 UTC: separate scoped review passed

The independent reviewer found no mathematical gap in the frozen strong-norm theorem, verified the source-history correction, and passed 135 independent exact assertions in addition to the 20 submitted checks. All six review files are copied unchanged into independent_review. Completion estimate: 100% toward the independently AI-reviewed strong-norm candidate, with the original L2/H1 and global weak-solution questions still unresolved. Preparing the one authorized draft PR with partial status; no shared queue files changed.
