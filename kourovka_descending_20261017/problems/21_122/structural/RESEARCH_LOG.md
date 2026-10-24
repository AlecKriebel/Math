# Structural research log: Kourovka21.122

## 2026-10-24T23:13:16Z — family opened

Exact target: for every finite group word w and every profinite G, if the set G_w of values has cardinality below2^aleph0, then G_w is finite. Closed verbal subgroup finiteness is not the requested conclusion. Source: official21st edition, printedp197, P.Shumyatsky. No other current family's mathematics was read. Discovery estimate **0%**.

Primary scope checks: Shumyatsky2401.15707v2 proves w(w(G)) finite and strong conciseness for dense FC-centre; it does not assert G_w finite for arbitrary G. Zozaya2608.02237v1 proves all words strongly concise in metabelian profinite groups. Its central-polynomial theorem explicitly retains metabelianity. DKS1907.01344v2 Cor4.2 retains pro-p verbal subgroup and finite-width hypotheses. These restrictions will not be deleted.

Mechanisms considered independently: (i) FC-centre/compact normal subset and central quotient reductions, (ii) iterated verbal and finite-width closure, (iii) central-valued word maps and finite-difference methods. No complete solution is claimed.

## 2026-10-24T23:17:00Z — explicit central-polynomial counterbarrier

Constructed a compact Heisenberg-by-Z3 group where the derived word δ2 is central-valued but has no finite Passi degree. Let M=[[10,3],[3,1]] act on Heisenberg(Z3) through its determinant-one action on the horizontal coordinates. Since M≡I mod3, its Z powers extend continuously to Z3. The central exponent of δ2(a,t^n,b,t) equals det((M^-n−I)e1,(M^-1−I)e2), an exact exponential recurrence. This is a barrier to extending the metabelian central-polynomial theorem by deleting its hypothesis. It is not a21.122 counterexample: δ2 is a known strongly concise multilinear word and the example has infinitely many, hence at least continuum many, word values. Proof/checker are being written. Discovery estimate toward full21.122 **2%**.

## 2026-10-24T23:28:53.752455+00:00 — reviewed countermodel and frozen route ledger

The independent central countermodel reviewer passed the final ac18f9ace... proof and supplied exact imageδ2(G)=9Z3. This is only an unconditional central-polynomial shortcut obstruction; it does not refute a small-image-dependent polynomiality theorem. Preserved the accepted proof and review unchanged. FC_WIDTH_AND_MARGINAL_ROUTES.md is frozen with separate standard-library finite-group controls and its own fresh audit in progress. SYNTHESIS.md records outcomeunsolved, all mechanism statuses and exact gaps. No unrestricted finite-width bound, central reduction or marginal propagation bridge was obtained. Discovery estimate **2%**.

## 2026-10-24T23:33:13.750373+00:00 — terminal structural family checkpoint

Inspected both actual review receipts: central_countermodel_review accepted exact proofac18f9ace... and all-degree reasoning; route_review accepted final noted0235434... at100% with no substantive objection and independently verified all finite-group/topological quantifiers. The only route-note correction was to define X0 exactly rather than by containment. Both reviewed proof packages are frozen. Outcomeforfull21.122fromthisfamily **unsolved**; discovery estimate **2%**. No new unsupported width, marginal, centrality or polynomiality bridge was promoted. Parent will integrate and checkpoint these files; no git/outreach/publication actions by this subagent.
