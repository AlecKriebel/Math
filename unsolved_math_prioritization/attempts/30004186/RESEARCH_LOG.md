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
