# Reviewer checklist: ten load-bearing proof interfaces

This checklist is designed for a skeptical audit of Version 0.2. None of the computational checks below substitutes for these mathematical steps.

## 1. Marked-channel augmentation

**Location:** Section 3 and Appendix A.

Verify that the augmented state records the target of the **actual reaction channel that fired**, rather than inferring a target from the population displacement. Check that projection gives the ordinary embedded chain, that the reachable augmented class is closed, and that population-class irreducibility implies augmented-class irreducibility. Confirm that only channels with identical source and target are combined.

## 2. Residual factorial identity

**Location:** Lemma 3.1.

For a reachable state \((x,t)\), verify that \(x\ge t\), that \(r=x-t\in\mathbb N_0^d\), and that
\[
V(x-s+u,u)-V(x,t)=\log\frac{(x)_t}{(x)_s}.
\]
Check the zero complex, \(2A\), and \(A+B\) explicitly.

## 3. One-jump entropy bound

**Location:** Lemma 3.2.

Check that the sums are over enabled sources, that \(p_x(t)>0\), and that substituting
\((x)_s=p_x(s)\Lambda(x)/\bar\kappa_s\) gives the exact identity before applying the entropy and rate-range bounds. Verify that \((x)_0=1\) creates no exceptional case.

## 4. Target-following recursion

**Location:** Lemma 4.1.

For a fixed simple path \(t=y_0\to\cdots\to y_L=c\), verify that every designated source is literally present, the residual remains fixed on designated edges, deviations stop the episode immediately, and the continuation probability is exactly \(q_kp_k\). Check the zero-length case \(c=t\).

## 5. Scalar envelope

**Location:** Lemma 4.2 and Proposition 4.3.

Differentiate
\[
\log p+C_0+qpM
\]
on \(0<p\le1\), verify both branches including equality at \(M=-1/q\), and check that finite backward composition sends a terminal upper bound tending to \(-\infty\) to an initial upper bound tending to \(-\infty\).

## 6. Top-complex case split

**Location:** Lemma 5.2.

Audit the exhaustive use of molecularity at most two. In particular, check: all complexes top; a top complex with two divergent particles; and the four one-divergent-particle subcases. Verify that the final service-species functional is a signed linear stoichiometric invariant, not mislabeled as a nonnegative conservation law.

## 7. Falling-factorial asymptotics

**Location:** Lemma 5.1.

Check the normalized-log extraction and
\[
\log(r^{(n)}+c)_y=R_nw\cdot y+o(R_n)
\]
for unary, mixed binary, and pure double sources. Confirm that a divergent coordinate with normalized weight zero remains in the divergent set and is not treated as bounded.

## 8. Finite and nonempty exceptional set

**Location:** Proposition 6.1.

For finiteness, verify the bad-sequence contradiction and the selection of one fixed terminal complex after subsequence extraction. For nonemptiness, verify that a global minimizer of the proper potential exists and that every finite episode endpoint has potential at least that minimum.

## 9. Trace-chain closure

**Location:** Proposition 7.1 and Appendix A.

Distinguish first hitting of \(K\) from positive return. Check finite mean \(K\)-to-\(K\) excursions, irreducibility of the finite trace chain, the uniform block probability of hitting a chosen \(k_*\), and the Tonelli bound converting trace excursions into original embedded jumps.

## 10. CTMC conversion and nonexplosion

**Location:** Proposition 7.2.

Verify the uniform lower rate bound supplied by the carried target, the finite expected physical return-time estimate, and the direct nonexplosion argument: recurrent visits to one marked state contribute an infinite subseries of independent identically distributed positive exponential holding times.
