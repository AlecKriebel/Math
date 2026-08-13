# Independent hostile audit: the two-species single-linkage service theorem

**Audit date:** 2026-08-12 PDT  
**Frozen target:** `proof_first_single_linkage_2d_exception_service_theorem.md`  
**Target SHA-256:**
`17da97fb25965c2f5ec9369691343927c34f6b0da75cad31cdf99ec2611c0d13`

## Derivative transfer

After the PASS below, the two publication repairs identified by the audit
were applied.  The header-identical derivative is frozen at

```text
9d878860cb6427688995784ed230776d982eca758a6c306be4180c3e8ffaaf03
    research_notes/proof_first_single_linkage_2d_exception_service_theorem.md
```

The exact diff against the audited bytes has only the following changes:

1. `post-jump endpoint` and `bounded population displacement` were replaced
   by `centered post-jump displacement` and `centered population
   displacement`, respectively, which states the weight already used in the
   formulas;
2. the one four-row `aligned` display was split into four separate displays,
   leaving the untagged probability bound and equations (3.4)--(3.6)
   mathematically identical.

Reconstructing the old bytes from precisely these replacements recovers the
audited SHA `17da97fb...`.  The derivative compiles successfully to a
five-page PDF with Pandoc and Tectonic.  The proof and theorem statement are
otherwise byte-identical, so the PASS transfers verbatim to SHA
`9d878860...`.

## Verdict

**PASS.**  The theorem is proved uniformly for every strongly connected
orientation of

\[
                 \{0,B,2B,A+B\}
\]

and every fixed positive rate vector.  The proof does not rely on an
orientation or population enumeration.  I found no counterorientation, no
unpaid clock, and no failure of the physical-time Foster composition.

There is one harmless wording point worth preserving in any publication
revision.  The polynomial endpoint weight used in (3.4) is a weight in the
**centered population displacement** (as the definition of \(R\) in that
display says), not a weight in the raw coordinate \(A_\tau\).  A raw weight
\((1+A_\tau)^r\) is of order \(n^r\) and of course would not have expectation
\(O(n^{-1})\) on the defect event.  No displayed estimate or later inference
uses such a raw weight.

There is also a typesetting-only repair: the three `\tag` commands in the
single `aligned` block containing (3.4)--(3.6) are rejected by standard
`amsmath` (`\tag not allowed here`).  Splitting those three rows into three
display equations, or using an `align` environment without an outer display,
repairs the LaTeX render.  This does not affect the mathematical verdict.

## 1. Interior-face generator descent

Let \(x_k=(a_k,b_k)\) be any unbounded sequence with \(b_k\geq 1\), and pass
to a tier subsequence.  The only asymptotically competitive degree-two
monomials are

\[
             (x_k\vee1)^{2B}=b_k^2,
             \qquad
             (x_k\vee1)^{A+B}=a_kb_k .
\]

Their enabled stochastic factors are respectively \(b_k(b_k-1)\) and
\(a_kb_k\).  This gives the following exhaustive *asymptotic regimes*, not an
enumeration of orientations.

- If \(b_k\to\infty\) and \(a_k\) is bounded, \(2B\) is the unique top
  D- and S-complex.
- If \(a_k,b_k\to\infty\), the limit of \(a_k/b_k\) makes the common top set
  \(\{2B\}\), \(\{A+B\}\), or their pair.
- If \(b_k\) is bounded, it may be fixed at a positive integer on a further
  subsequence; then \(a_k\to\infty\) and \(A+B\) is the unique top D- and
  S-complex.  This remains true at \(b_k=1\), where the \(2B\) propensity is
  zero.

In each regime the common top set is nonempty and proper.  Strong
connectivity gives an edge whose source is in that set and whose target is
outside it.  Its source is therefore simultaneously top S and top D and the
edge is strictly D-descending.  The Anderson--Kim top-S descending-source
estimate applies for arbitrary positive constants and yields

\[
                {\cal L}V(a_k,b_k)\longrightarrow-\infty.
\]

The subsequence argument is sufficient for the asserted full limit: failure
of the full limit would provide a subsequence bounded below, and the same
tier refinement would contradict that bound.  Thus a finite \(F_1\) with
\({\cal L}V\leq-2\) on \(\{b\geq1\}\cap F_1^c\) exists.

## 2. Exact replay of the \(B=0\) macro

Write \(O=0\), \(Q=2B\), and \(T=A+B\).  Ignore lower-source firings only in
an auxiliary clock construction.  In one auxiliary attempt, an \(O\)-jump
either lands directly in \(B\) or \(Q\), or lands in \(T\) and the next
T-source jump lands in \(B\) or \(Q\).  Its success probability is exactly

\[
 p_*={\sum_{O\to B,Q}\kappa_{Oz}\over\lambda_O}
 +{\kappa_{OT}\over\lambda_O}
  {\sum_{T\to B,Q}\kappa_{Tz}\over\lambda_T}.
\]

If \(p_*=0\), every edge leaving \(O\) goes to \(T\) and every edge leaving
\(T\) goes to \(O\); hence \(\{O,T\}\) is a nonempty proper closed set in the
complex graph, contradicting strong connectivity.  Consequently the
auxiliary attempt count \(N\) is geometric with fixed parameter \(p_*>0\)
and has moments of every order.  Neutral attempts return exactly to
\((n,0)\); they do not accumulate hidden population debt.

Before the successful service, each attempt exposes at most two positive-
\(B\) races, and at every such clean stage

\[
       a\in\{n,n+1\},\qquad 1\leq b\leq2.
\]

The full physical chain is restored by declaring the first lower-source
firing during one of these races to be an included defect.  At any exposed
state, the T-source and lower-source aggregate propensities are

\[
             \lambda_T ab,
             \qquad
             q_{\rm low}(a,b)\leq C(1+b^2),
\]

so the exact exponential-clock race gives

\[
 {q_{\rm low}\over \lambda_Tab+q_{\rm low}}
       \leq {C(1+b)\over a}\leq {C\over n}.
\]

Conditioning successively on the auxiliary history and summing over the at
most \(2N\) exposed races proves, for every fixed \(r\),

\[
 \mathbb P_n(E)\leq {C\over n},
 \qquad
 \mathbb E_n\!\left[(1+N+|X_\tau-(n,0)|)^r;E\right]
       \leq {C_r\over n}.                                    \tag{A.1}
\]

This is the precise compensation statement behind (3.4).  The included
defect jump has bounded size.  On the clean event, the terminal T-source
jump is unpaired and gives

\[
                    A_\tau=n-1,\qquad B_\tau\leq3.             \tag{A.2}
\]

The clock bound is physical, not operational.  Each visit to \(B=0\) has an
\({\rm Exp}(\lambda_O)\) holding time.  A positive-\(B\) exposed race has
total rate at least \(\lambda_Tab\geq c n\).  A geometric sum of these
holding times therefore has

\[
                         \mathbb E_n\tau^r\leq C_r             \tag{A.3}
\]

for every fixed \(r\).  No clock has been suppressed in (A.1)--(A.3): the
auxiliary construction only indexes histories, while the first competing
lower firing is the actual terminal jump on \(E\).

From (A.2),

\[
 V(X_\tau)-V(n,0)\leq-\log n+C
\]

on the clean event.  On \(E\), the centered displacement is bounded and
neutral attempts return to the start, so

\[
 \mathbb E_n[|V(X_\tau)-V(n,0)|;E]
       \leq C\log(n+1)/n.
\]

Together with (A.3), these inequalities give the claimed stopped
physical-time drift \(-\tfrac12\log n\) for all sufficiently large \(n\).

## 3. Physical-time Foster gluing

At \(b\geq1\), let \(J\) be the next reaction time.  Since
\(J\sim{\rm Exp}(q(x))\) and the reaction mark has the usual propensity
law,

\[
 \mathbb E_x[V(X_J)-V(x)+J]
      ={\mathcal LV(x)+1\over q(x)}
      \leq-{1\over q(x)}<0.                                  \tag{A.4}
\]

At \(b=0\) outside a sufficiently enlarged finite set, the macro estimate is
at most \(-1\).  Thus, at successive episode endpoints stopped on first
entry to \(F\),

\[
       V(X_{S_{m\wedge N_F}})+S_{m\wedge N_F}
\]

is a nonnegative supermartingale and

\[
                  \mathbb E_x S_{m\wedge N_F}\leq V(x).       \tag{A.5}
\]

The finite set may be enlarged so that every boundary macro started outside
it has large \(A\); all preterminal clean states then have \(A\geq n\), and
the only possible first entry into \(F\) during that macro is its service
endpoint.  Hence the episode stopping used in (A.5) agrees with physical
first entry.

Finally, degree-two sources cannot increase total population because all
products are binary.  Population-increasing degree-zero and degree-one
rates are at most \(C(1+A+B)\), with bounded jumps, so a linear pure-birth
comparison proves nonexplosion.  On \(\{N_F=\infty\}\), infinitely many
episodes contain infinitely many actual reactions and therefore
\(S_m\to\infty\).  Fatou/monotone convergence in (A.5) forces that event to
have probability zero and gives

\[
                         \mathbb E_xT_F\leq V(x)<\infty.
\]

Within a closed irreducible population class, the construction never leaves
the class.  The class therefore meets \(F\), and the usual finite-set return
argument gives a finite mean return time.  Absorbing singleton classes are
already positive recurrent.  This completes the hostile replay.

## 4. Scope and flags

The result proves precisely the exceptional two-dynamic-species support.  It
does not address a genuinely three-dynamic-species carrier support.  No
pair-level or global certification flag is justified by this audit alone.
