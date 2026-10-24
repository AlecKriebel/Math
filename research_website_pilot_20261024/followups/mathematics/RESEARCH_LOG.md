# Conceptual screening log

## 2026-10-24 23:07 UTC — checkpoint, screening 40% complete

Task: independently screen at most one or two paper-level follow-up questions to the published binary-grandparent FUSF degree decrease. This is a bounded screening task, not a claim of solving the resulting questions. No external communication is authorized or attempted.

Read the complete published `main.tex`. Its strongest verified result is the exact base value `(24-sqrt(2))/7` and a finite rational upper certificate below `3.21` for the square. The square's exact value, higher powers, direction of further changes, and any mechanism beyond that example remain unproved there.

Initial route screening:

- **Exact square value alone:** technically useful but insufficiently structural to recommend as its own paper without a general recurrence/convergence theorem.
- **Unimodular power invariance:** inherited from the tracial framework; do not repackage as a novel target.
- **Characterize invariance by unimodularity:** false without substantial restrictions: nonunimodular graphs with no nonconstant harmonic Dirichlet functions have degree 2 for every power. Tang's Diestel–Leader examples provide a prior family.
- **Universal nonincrease versus a strict increase under squaring:** a precise residual question. Resistance monotonicity controls old-edge marginals but not the newly added edges. No direction follows from the published counterexample alone.
- **Large powers of the grandparent graph:** exact geometry gives `d_G(x,y)=ceil(a/2)+ceil(b/2)`, where `a,b` are tree distances to the common ancestor. Thus `T^(2n-1) ⊂ G^n ⊂ T^(2n)`. The comparison tree powers have degree 3, but inclusion does not compare summed free resistances. A possible limiting value 3 is a question, not a supported conjecture.

Primary sources inspected in bounded screening: BLPS, *Uniform Spanning Forests*, author PDF, Theorem 6.4 and potential-theory section; Gaboriau, arXiv:math/0405458v3, Proposition 2.9; Tang, arXiv:1908.09889v2, introduction and Section 5. Relevant URLs will be recorded in the final screening note.

Next: use a bounded small-family numerical screen only to detect easy counterexamples or misleading conjectures. Finite free-exhaustion values are upper bounds and numerical stabilization is not an infinite-volume proof.

## 2026-10-24 23:14 UTC — checkpoint, screening 100% complete

Retain only the sign question, stated as a question. A general sign theorem would merit a separate paper; an opposing example should ideally explain a different mechanism rather than merely repeat the original certificate calculation.

The 14-family screen found no reliable increase. Shallow free approximations often suggested increases that disappeared at larger depth. These remain nonproof. Verified progress toward resolving the sign question: 0%; the screening task itself is complete.

Corrected geometry bookkeeping: grandparent powers omit exactly one ninth of all neighbors of T^(2n), asymptotically two ninths of its outer sphere. A weighted-square control was recorded and explicitly left unverified. No further computation planned. Final report: SCREENING_VERDICT.md. No source or website files modified; no person contacted. Parent owns commit and push on main.
