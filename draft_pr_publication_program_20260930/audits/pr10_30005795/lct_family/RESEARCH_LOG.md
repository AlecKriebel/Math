# Independent LCT family audit log

Scope: frozen PR10 source `source_snapshot/BOUND.md`, head `925f9e9f46f2c7407fd142cedf36995a4519a378`. This audit checks the threshold endpoint, global/local valuation domain, Cartier restrictions, the finite integral identity, degenerate cases, and the reciprocal characterization for the effective real divisor B. It does not certify the separate Mori-dream-space finiteness or source-priority routes. No canonical candidate, snapshot, branch, or publication state is changed.

## 2026-10-01 04:35:52 UTC — intake and independent reconstruction

- Read BOUND.md before status, logs, or prior verdicts; have not used prior verdicts as evidence.
- Main branch observed. Unrelated pre-existing worktree changes are left untouched.
- Primary lemma text consulted only to fix the intended local valuation domain. Its first inequality uses prime divisors over S with P in their center, matching the frozen text's local restriction.
- Independent proof route: choose one log resolution of the finite Cartier support, write the pulled-back real boundary, and characterize log canonicity by finitely many coefficient inequalities. On a smooth surface, further point blowups preserve coefficients at most one, including negative coefficients.
- Delegated an independent endpoint/real-divisor subaudit without requesting convergence to a verdict.
- Completion estimate: **30%** toward completing this audit (not toward a new mathematical discovery).

Primary sources opened: [published Appendix B Lemma 27](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/kstable-divisors-in-mathbb-p1times-mathbb-p1times-mathbb-p2-of-degree-112/999FB6032A21485AD71CF230CC802E6C), [Fujino, Introduction to the log minimal model program](https://www.math.kyoto-u.ac.jp/~fujino/MMP21.pdf). The proof will be recorded as a checkable deduction rather than relying on the short published proof.

## 2026-10-01 04:39:27 UTC — endpoint proof and exact falsification cases

- Reconstructed `lct(S;B)=min_{m_i>0} A_S(E_i)/m_i` on one resolution of finite Cartier support; no rationality assumption on B is needed. Positivity and attainment follow because the minimum is finite and each numerator is a positive log discrepancy.
- Independently checked that strict transforms must be included in the minimum. This matters on the A1 surface `xy=z^2` with Cartier divisor `(x=0)=2L`: the strict-transform ratio is 1/2, while the crepant exceptional ratio is 1.
- Two exact smooth examples show the componentwise bound is not the sharp constant: transverse half-weight curves give `(K0,Kopt)=(1,1/2)`; tangent unit-weight curves give `(2,4/3)`. Fraction arithmetic independently checks endpoint inequalities from the displayed resolution data.
- Counterexample to replacing global thresholds by unrestricted local thresholds: a multiple line away from P has local threshold infinity but positive order at its own divisorial center. The frozen statement correctly excludes that misuse.
- Counterexample to replacing klt by lc: the cone over a smooth plane cubic has exceptional log discrepancy 0, and a hyperplane section through the vertex has positive exceptional order. No finite K can control it. The frozen statement retains klt/Du Val.
- Wording defect identified at BOUND.md:56: ordinary discrepancies of a klt surface are not necessarily positive; the proof requires **log discrepancies** `A_S(E)>0`. A Du Val crepant exceptional divisor already has ordinary discrepancy 0. This is a minor repair, with no change to the bound.
- Completion estimate: **75%** toward completing this audit; remaining work is to finish the written certificate, incorporate the independent endpoint challenge, and list precise scope limitations.

Additional primary source opened: [Kollár, Families of varieties of general type, Chapter 11](https://web.math.princeton.edu/~kollar/FromMyHomePage/modbook-final.pdf), Definitions 11.1, 11.5, 11.8 and Section 11.4. It distinguishes ordinary discrepancy from `1+a` and permits real coefficients. Exact examples and derivations remain the principal evidence.

## 2026-10-01 04:42:47 UTC — independent challenge and completed certificate

- Independent endpoint subaudit completed before reading this family's verdict: same finite-resolution formula and positive endpoint; real coefficients, B=0, local centers, and nonproper finite-type algebraic surfaces all pass. It supplies an explicit analytic counterexample if one broadens the scope to arbitrary noncompact analytic surfaces.
- Requested a second adversarial pass on the explicit examples and the restriction argument. It independently confirmed the tangent-curve blowup data `(A,m)=(3,4)`, the A1 chart `x=t*v^2` giving `E+2L'`, and the nonzerodivisor restriction condition `S not contained in E`.
- Wrote `LCT_AUDIT.md` with the strongest verified claim, full proof, exact examples, counterexamples to weakened assumptions, one actionable terminology repair, and exact limitations of this family pass.
- Frozen BOUND.md SHA256 observed: `dd4b6addb46edc8532362d35cecf5a3316dfcf27d9795306f9d34ebac3c8f450`.
- Final disposition for this family: **pass with one minor wording correction**. No mathematical counterexample within the algebraic finite-family hypotheses. Separate finiteness/Mori-dream and source-priority families remain outside this certificate.
- Completion estimate: **100%** toward this audit goal. No new discovery claimed. No canonical candidate, snapshot, queue, branch, commit, remote, or publication state was modified; no external communication was prepared or initiated.
