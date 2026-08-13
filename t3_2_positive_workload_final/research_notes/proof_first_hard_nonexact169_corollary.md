# Corollary: the full 169-row nonexact physical hard menu

**Proof-first scoped corollary, 2026-08-12 PDT. Audit status: pending.**
This is a one-lemma extension of the audited macroscopic fast-Schur proof
for the 145 mixed nonexact rows. It does not alter that frozen proof.

Let (dU) be the maximal base complex occurring in either linkage. The
proof in *proof_first_hard_mixed145_macroscopic_schur.md* uses only:

1. (d\in\{1,2\}) and (q-pd\ge1);
2. strong connectivity of the linkage containing (dU);
3. if that linkage contains (V+I), it is not the exact pair
   \(\{dU,V+I\}\); and
4. every target has molecularity at most two.

It never uses that a linkage is mixed after deleting (V+I). Therefore it
extends to the other nonexact categories as follows.

* In each of the eight separated rows, (dU) belongs to the
  (V+I)-linkage. The same one/two-window Schur macro, geometric
  exact-return inverse, and entropy estimate apply verbatim.
* In each of the sixteen no-history rows, (dU) belongs to the base-only
  lower linkage. Its first nonself dominant reaction is an immediate direct
  base descent. There is no carrier window, so the dirty-event bound is
  vacuous and the entropy estimate is strictly easier.

The finite support table verifies that all additional rows satisfy the four
premises and that

\[
              169=145\ \text{mixed}+8\ \text{separated}
                       +16\ \text{no-history}.                 \tag{1.1}
\]

Consequently every nonexact physical hard ratio/support row has a raw
physical stopped episode with the same fixed corrected factorial potential
(W_\ell=G_\ell^4), arbitrary fixed endpoint moments, physical duration
moments, and

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
       \le-cG_\ell(X_0)^3\log s.                              \tag{1.2}
\]

This is an analytic corollary; the finite table supplies only (1.1) and the
four premises. It makes no pair or global claim before independent audit.
