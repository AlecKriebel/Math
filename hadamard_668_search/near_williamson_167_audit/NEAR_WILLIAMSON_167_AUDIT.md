# Near-Williamson audit at base order 167

Date: 2026-07-24

Status: exact reduction obtained; no order-167 quadruple found; no
nonexistence result.

This note audits the independent route suggested by Kharaghani, Mohammadian,
and Tayfeh-Rezaie, *A search for Hadamard matrices of Williamson type*,
[arXiv:2605.08661](https://arxiv.org/abs/2605.08661).  It deliberately
separates statements in that paper from the order-167 derivations made here.

## What the paper proves and computes

The following are literature facts.

- A near-Williamson quadruple of odd order \(n\) consists of one circulant
  sign matrix \(A\) and three symmetric circulant sign matrices \(B,C,D\)
  satisfying
  \[
  AA^\top+BB^\top+CC^\top+DD^\top=4nI.
  \]
  The quadruple \((AR,B,C,D)\), with \(R\) the reversing back-circulant
  permutation, is Williamson type and gives a real Hadamard matrix of order
  \(4n\).  Thus a quadruple at \(n=167\) would directly give \(H(668)\).
- The authors exhaustively classify near-Williamson quadruples for every odd
  \(n\leq35\), in about ten desktop hours, and report 73,630 equivalence
  classes at \(n=35\).
- They find examples at \(n=47,53,59\) after restricting \(A\) to be
  "almost symmetric": \(a_j=a_{-j}\) for every \(j>1\).  Together with
  earlier work this establishes the construction for every odd \(n\leq63\).
- Their algorithm uses the row-sum four-square equation, Fourier/PSD bounds,
  automorphism representatives for a symmetric block, and a mod-4
  linearization.  For fixed \(A,B\), that linearization first decides, for
  every half-index, whether \(D_j=C_j\) or \(D_j=-C_j\), and then solves a
  linear congruence system for \(C\).
- The paper provides neither an infinite construction of near-Williamson
  quadruples nor an order-167 example.  Its reported exhaustive range is 35
  and its reported construction range ends at 63.

## Exact order-167 equations

The following are our derivations, specialized to \(n=167\).

Write \(P_X(s)=\sum_j x_jx_{j+s}\) for periodic autocorrelation and
\(\widehat X(k)=\sum_jx_j\zeta^{kj}\), where
\(\zeta=e^{2\pi i/167}\).  The matrix equation is exactly

\[
P_A(s)+P_B(s)+P_C(s)+P_D(s)=0\qquad(1\leq s\leq83),
\]

or, equivalently,

\[
|\widehat A(k)|^2+|\widehat B(k)|^2+
|\widehat C(k)|^2+|\widehat D(k)|^2=668
\qquad(0\leq k\leq83).
\]

At \(k=0\), if \(a,b,c,d\) are row sums,

\[
a^2+b^2+c^2+d^2=668.
\]

Normalize the central entries to \(+1\).  Symmetry forces
\(b,c,d\equiv167\equiv3\pmod4\), and the three symmetric blocks may be
ordered so that \(|b|\geq|c|\geq|d|\).  Exact enumeration gives **68**
signed row-sum profiles.

Equivalently, if \(S_X\) is the negative support of row \(X\), then the four
supports would be a cyclic supplementary difference family with

\[
k_X=|S_X|=(167-r_X)/2,\qquad
\lambda=k_A+k_B+k_C+k_D-167,
\]

and

\[
\sum_X |S_X\cap(S_X-s)|=\lambda
\quad\text{for every }s\ne0.
\]

For a symmetric row \(X\),

\[
\widehat X(k)=1+2\sum_{j=1}^{83}x_j
\cos\left(\frac{2\pi kj}{167}\right)
\]

is real.  For a genuinely one-defect \(A\), use a multiplier and reversal to
put the negative member of the exceptional pair at \(+1\).  Then
\(a_1=-1,a_{-1}=+1\), all other pairs are symmetric, and

\[
|\widehat A(k)|^2=
\left(1+2\sum_{j=2}^{83}a_j
\cos\left(\frac{2\pi kj}{167}\right)\right)^2
+4\sin^2\left(\frac{2\pi k}{167}\right).
\]

Thus the imaginary part is a fixed two-entry defect, rather than 83 new
degrees of freedom.

There is also a useful exact cyclotomic formulation.  For every row \(X\),
\(\alpha_X=|\widehat X(1)|^2\) lies in the real cyclotomic field
\(\mathbb Q(\zeta+\zeta^{-1})\), whose degree is 83.  Its 83 conjugates are
exactly \(|\widehat X(k)|^2\), \(1\leq k\leq83\).  Hence all 83 nontrivial
spectral equations are the conjugates of the single algebraic-integer
identity

\[
\alpha_A+\alpha_B+\alpha_C+\alpha_D=668.
\]

Their traces are fixed:

\[
\operatorname{Tr}(\alpha_X)=\frac{167^2-r_X^2}{2}.
\]

The sum of these four trace equations is already implied by the row-sum
four-square equation, so this elegant degree-83 packaging supplies no
additional scalar obstruction.

## Exact split of the paper's almost-symmetric family

If the exceptional pair agrees, \(A\) is fully symmetric and
\(a\equiv3\pmod4\).  If it disagrees, it contributes zero to the row sum and
\(a\equiv1\pmod4\).  Consequently the 68 profiles split exactly into

- 34 profiles in the ordinary all-symmetric Williamson subfamily; and
- 34 genuinely one-defect near-Williamson profiles.

This distinction is important: restricting \(A\) as in the paper does not
turn the order-167 problem into one 84-bit search.  It creates 34 separate
one-defect row-sum shards, in addition to the Williamson overlap already
audited elsewhere in this repository.

For a one-defect profile, let \(x_j\) be the negative-support bit of the
symmetric core of \(A\), with \(x_0=x_1=0\), and let \(b_j,c_j,d_j\) denote
the negative-support bits of \(B,C,D\).  Reduction of the autocorrelation
identity modulo eight gives the explicit modified product law

\[
d_t=b_t+c_t+x_t+x_{2t-1}+x_{2t+1}\pmod2,
\qquad 1\leq t\leq83,
\]

where all subscripts are reduced modulo 167 and then modulo sign.  In
particular, \(D\) is pointwise determined by \(A,B,C\).  More generally,
without assuming a one-defect \(A\),

\[
c_t+d_t \equiv
\frac{P_A(2t)+P_B(2t)+334}{4}\pmod2.
\]

The script exhaustively verifies the closed form for every normalized
one-defect \(A\) and symmetric \(B\) at orders 7 and 11, then checks
deterministic order-167 samples with exact integer autocorrelations.

One way to prove the closed form is to write a sign row as \(1-2u\).  If its
negative support is \(S\), then

\[
P(s)=n-4|S|+4|S\cap(S-s)|.
\]

For a symmetric support, the intersection parity at lag \(s\) is the support
bit at \(s/2\): all other terms pair under the reflection
\(j\mapsto-j-s\).  Adding the one unmatched support element at \(+1\)
contributes the two extra core bits at \(s-1\) and \(s+1\).

After writing \(d_t=(-1)^{e_t}c_t\), pair the directed edges in each
autocorrelation under \(j\mapsto-j-s\), remove the one fixed edge, divide by
four, and reduce modulo four.  This gives a GF(2) linear system in the 83
negative-support bits of \(C\).  When \(e\ne0\), its coefficient matrix has
the \(e\)-vector in its kernel: adding \(e\) to \(C\) swaps \(C\) and \(D\),
and cannot change their autocorrelation sum.  Therefore its rank is then at
most 82.  Rank 82 is ideal for the paper's algorithm: a consistent input
leaves exactly the two solutions related by \(C,D\) exchange, before
row-weight and exact autocorrelation checks.

## Complete front-end size

For a one-defect \(A\) of row sum \(a\), the number of negative symmetric
core pairs is

\[
h_A=(165-a)/4,
\]

and for normalized symmetric \(B\) of row sum \(b\),

\[
h_B=(167-b)/4.
\]

A common multiplier fixes the exceptional pair of \(A\) at
\(\{+1,-1\}\); the residual reversal identifies its two orientations.  This
leaves

\[
\binom{82}{h_A}\binom{83}{h_B}
\]

gauge-fixed \(A,B\) inputs for each distinct \((a,b)\) shard.  Deduplicating
the one repeated \((a,b)\) pair among the 34 profiles leaves 33 shards and
the exact total

\[
5\,389\,321\,893\,816\,717\,644\,217\,498\,408\,040\,941\,405\,747\,563\,982\,000
\approx 5.3893\times10^{48}.
\]

This count is **before** individual PSD bounds and the joint
\(\operatorname{PSD}(A)+\operatorname{PSD}(B)\leq668\) test.  It is also
after the decisive \(C/D\) pointwise relation and the natural
defect-location/orientation multiplier gauge.  The corresponding normalized
unrestricted-\(A\) front end, before symmetry quotients, is about
\(1.178\times10^{74}\) \(A,B\) inputs.

A deliberately small numerical pilot sampled 100 fixed-weight \(A,B\) pairs
in each of the 34 one-defect profiles (3,400 pairs total, deterministic seed
260724).  Twelve sampled \(A\)'s and eleven sampled \(B\)'s passed their
individual PSD bounds; none of the paired samples passed both individual
bounds or the joint PSD bound.  All 3,400 passed the elementary \(C,D\)
row-weight compatibility gate, so that gate supplies no observed pruning.
These are heuristic frequencies, not exact counts or evidence of
nonexistence.  Even granting an unsubstantiated factor of \(10^6\) from the
PSD filters would leave more than \(10^{42}\) gauge-fixed \(A,B\) inputs.

A separate exact-integer pilot sampled 10 \(A,B\) pairs in each profile (340
total), all with nonzero \(e\).  Every reduced GF(2) system had rank 82; 174
were consistent and 166 were inconsistent.  Thus the published back end
behaves as favorably as one could expect on this sample—zero or one \(C,D\)
pair up to exchange—but it only halves the front-end sample and does not
address its \(10^{48.73}\) size.  The rank frequencies are observations, not
a proof that every order-167 input has rank 82.

The remaining paper algorithm can make each surviving \(A,B\) input cheap:
after \(D_j/C_j\) is known, its second mod-4 reduction is a linear system in
the 83 half-signs of \(C\), followed by exact autocorrelation verification.
It does not remove the need to generate or otherwise characterize the
astronomical \(A,B\) front end.

## Assessment

The near-Williamson route is mathematically valid and independent of the
Legendre-pair and Eliahou lanes.  The explicit modified product law is useful
for any future SAT or algebraic encoding, and the one-defect Fourier formula
shows exactly what structure the paper's successful \(47,53,59\) searches
were exploiting.

It does **not** presently extend materially to 167.  Prime order 167 has no
medium multiplier subgroup: after using the multiplier to normalize the
single defect, no nontrivial multiplier compression remains for \(B\).
Even the paper's strongest reported structural restriction leaves roughly
\(10^{48.73}\) \(A,B\) inputs.  PSD pruning can be sampled as a heuristic,
but no plausible constant-factor or ordinary exponential filtering closes
that gap.  A viable continuation would require a new theorem that
parametrizes or algebraically eliminates most \(A,B\) pairs, not a larger
implementation of the published enumeration.

Therefore:

- do not promote this to a production search lane now;
- retain the modified product law and exact profile/count audit as a
  resumable side result;
- revisit only if a new construction theorem controls the one-defect core,
  or if an independent lane produces a candidate whose four circulant blocks
  can be recognized in this form.

## Reproduction

The exact audit uses negligible memory and one process:

```bash
python3 audit_near_williamson_167.py
```

An optional small numerical PSD pilot is available through
`--samples-per-profile`.  The exact reduced-system pilot is available through
`--rank-samples-per-profile`.  Both are bounded diagnostics; neither is an
exhaustive search.
