# Hostile independent audit: raw exponential entropy to fourth-power drift

**Audit date:** 2026-08-12 PDT  
**Frozen target:** `proof_first_separated_raw_exponential_w4_lift.md`  
**Target SHA-256:**
`3badb799468f6912659916ab2bc4ee556f5c113f00fbea01d106c88449cc0134`  
**Target size:** 155 lines, 4234 bytes  
**Verdict:** **STRICT PASS.**

The verdict is only for the deterministic-probabilistic lift stated in the
target.  In particular, it does not certify the upstream raw-transform
estimates, the construction of the stopping rule, or its almost-sure
termination.  Those exclusions are already explicit in the frozen target.

## 1. Domain and sign check

Put (g=G_\ell(x)) and (g'=G_\ell(X_\tau)=g+Y).  The hypothesis that the
shifted entropy is at least one on the population lattice gives

\[
                         g\ge1,\qquad g'\ge1.               \tag{A.1}
\]

This is the exact fact needed twice in the proof.  First, on
(A=\{Y\le-rh\}), the condition (h=o(g)) implies (g-rh\ge1) eventually,
so monotonicity of (t^4) is being used entirely inside ([1,\infty)):

\[
 (g')^4-g^4\le(g-rh)^4-g^4.                                \tag{A.2}
\]

If (Y) is still more negative, (A.1) prevents passage through zero, so
the fourth power cannot turn upward.  Second, if
(((g+Y)^4-g^4)^+>0), then (A.1) and strict monotonicity force (Y>0).
Thus the target applies its positive-tail calculus inequality only in its
stated range (y\ge0).  There is no hidden lower-tail moment assumption.

For completeness, with (z=rh/g\to0),

\[
 (g-rh)^4-g^4
 =g^4(-4z+6z^2-4z^3+z^4)
 \le -2r g^3h                                             \tag{A.3}
\]

for all sufficiently large entrances.  This verifies the constant and the
sign in (2.4), including the potentially delicate case (g+Y\) near one.

## 2. Markov threshold and boundary exponent

The disjoint terminal partition gives

\[
 \mathbb E e^{\theta Y}
 =\mathbb E[e^{\theta Y};S]
  +\mathbb E[e^{\theta Y};E]
  +\mathbb E[e^{\theta Y};B].                              \tag{A.4}
\]

For (r=c/(4\theta)), exponential Markov at the negative threshold is

\[
 \mathbb P\{Y>-rh\}
 \le e^{\theta rh}\mathbb E e^{\theta Y}
 \le C e^{-3ch/4}+C_N e^{ch/4}a^{-N}.                      \tag{A.5}
\]

The target's bound (h\le C_0\log a) yields
(e^{ch/4}\le a^{C_0c/4}).  Since (h\to\infty), this same bound also
forces (a\to\infty).  Choosing one fixed
(N>C_0c/4+2) therefore makes the second term (o(1)), exactly as claimed.
There is no missing factor of \(\theta\): it cancels in
(\theta r=c/4).

## 3. Positive fourth-power tail

For (g\ge1,y\ge0), expansion gives

\[
 (g+y)^4-g^4=4g^3y+6g^2y^2+4gy^3+y^4.
\]

Each (y^j), (1\le j\le4), is bounded by a constant depending only on
(\theta) times (e^{\theta y/2}), while
(1,g,g^2\le g^3\).  Hence (3.1) is valid with a uniform
(C_\theta).  By the sign check in Section 1 it controls the entire positive
part even though (Y) itself need not be nonnegative.

The labelled Cauchy--Schwarz step is also valid for subprobability events:

\[
 \mathbb E[e^{\theta Y/2};D]
 \le \bigl(\mathbb E[e^{\theta Y};D]\bigr)^{1/2}
      \mathbb P(D)^{1/2}
 \le \bigl(\mathbb E[e^{\theta Y};D]\bigr)^{1/2}.          \tag{A.6}
\]

Apply this first to (D=S\cup E), using disjointness and (1.3), and then
to (D=B), using (1.4).  Relabelling square roots of constants is harmless.
This proves the two estimates in (3.2).

Moreover, no comparison between (G) and (a) was silently used in
(3.3).  Indeed,

\[
 \frac{1+G^3}{G^3h}
 \left(e^{-ch/2}+a^{-N/2}\right)
 \le {2\over h}\left(e^{-ch/2}+a^{-N/2}\right)\longrightarrow0. \tag{A.7}
\]

Thus the boundary charge is negligible for every fixed positive (N);
the larger choice of (N) in Section 2 already suffices.

## 4. Assembly, integrability, and duration

On (A), (A.3) gives the deterministic negative bound.  On (A^c), the
increment is bounded above by its positive part.  Therefore

\[
 \mathbb E[(g+Y)^4-g^4]
 \le -2rg^3h\,\mathbb P(A)
     +\mathbb E[((g+Y)^4-g^4)^+;A^c].                       \tag{A.8}
\]

Equations (A.5) and (A.7) make the right side
(-2rg^3h\{1-o(1)\}+o(g^3h)\), hence at most (-rg^3h)
eventually.  The expectation is well-defined: its negative part is bounded
by the deterministic number (g^4), and Section 3 makes its positive part
integrable.  Finally

\[
 \mathbb E\tau=o(g^3h)
\]

is exactly the amount needed to absorb the added physical duration and to
retain a fixed negative constant (c_*>0).

The target's last sentence about polynomial endpoint marks is valid with
its natural universal reading: the asserted family of estimates includes
the constant polynomial one.  Alternatively, a single endpoint mark also
suffices whenever it is bounded below by a positive constant.  No claim
that an estimate with one possibly vanishing polynomial implies the
unmarked estimate is used in the proof.

## 5. Audit disposition

All requested hostile checks pass:

1. the fourth-power monotonicity remains one-sided when the terminal
   entropy approaches its lower value one;
2. the Markov threshold has the correct sign and exponent;
3. (h\le C_0\log a) is used with the correct inequality direction;
4. labelled Cauchy--Schwarz includes the omitted subprobability factor
   (\mathbb P(D)^{1/2}\le1);
5. the positive fourth-power tail follows from an explicit expansion;
6. the boundary term needs no unstated (G\)-versus-(a) comparison; and
7. the duration hypothesis is precisely sufficient for absorption.

Accordingly, the exact frozen target earns **STRICT PASS**.
