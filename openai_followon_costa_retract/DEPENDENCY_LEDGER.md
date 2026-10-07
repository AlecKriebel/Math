# Dependency ledger — candidate v1

| ID | Exact needed statement | Assumptions | Validation basis | Status / exact gap |
|---|---|---|---|---|
| D1 | A is a domain, A[p⁻¹]=C[p,p⁻¹,x,y,z], trdeg A=4 | Explicit H, complex scalars | §2 UFD localization argument reconstructed; inverse identities checked | Verified written argument |
| D2 | Actual θ=gΦ:A[w]→C[p,s,u,m,e] is an isomorphism | Domain and p nonzero, polynomial certificates | Stabilization audit; 32 integer identities, both Φ inverse orders; gq polynomial identity and qg uses domain cancellation | Verified maps including p=0 |
| D3 | A is not C^[4] | Exact valuation filtration; smooth G; line-bundle complement; char0; original nonsquare field | Full §§3–6 written proof reconstruction and independent bundle skeptic; principalization exact certificates; ledger notes/nonpolynomiality/audit.md | Written proof passed; inherited OpenAI theorem, no independent cancellation claim |
| D4 | i=θj, r=εθ⁻¹ give ri=id, (ir)²=ir, image=i(A) | Actual θ and unital coefficient/evaluation maps | Direct categorical/algebraic compositions, explicit generator formulas | Verified; spectrum directions separately checked |
| D5 | Smoothness of Spec A | C hypersurface Jacobian criterion | Laurent polynomial chart and F,J derivatives at p=0 with Bezout identity | Verified independently |
| D6 | Costa question and classical cancellation relation | Field k; ambient n+1 and cancellation dimension n | Nagamine1811.04153v2 Prop1.4/proof read; earlier Epstein–Nguyen intro; Costa metadata with exact question reproduced in primary papers | Verified provenance via primary reproductions; original Costa full text inaccessible |
| D7 | Actual Lean MainStatement matches D1–D3 | Genuine quotient, C-algebra equivalence, finite type, domain, Krull dimension | 55 unchanged modules/hash closure and model comparison; no textual holes. Actual intermediate mechanisms differ from printed ones | Source/semantic audit only. Full kernel build, axiom report and comparator not reproduced due disk limits; NOT relied upon as formal certification |
| D8 | No earlier exact explicit construction found | Bounded current primary-source/corpus search on2026-10-06 | Priority audit, cited full statements, source disclosure and remote corrections check | Qualified no-conflict verdict; absence of hits is not proof of first priority |

Strongest verified claim: using the independently audited written OpenAI nonpolynomiality theorem, the exact transported maps realize a smooth nonpolynomial complex trdeg4 algebra retract of C^[5]. Final package reviews and publication have not yet happened.
