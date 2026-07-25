# Constant rank-two conjugators are impossible

This companion certificate studies the trace-corrected formal family

\[
N_A(x)=e^{-zA}\bigl(N_0+\eta z^{18}J+19y^{36}J\bigr)e^{zA},
\qquad
z=\log(1+y),\quad x=1+y,
\]

over \(\mathbf F_{37}[y]/(y^{37})\), where
\(\eta\in\{1,-1\}\).  It proves:

> No constant symmetric matrix \(A\) of rank two can make \(N_A\) the
> group-ring form of a binary semiregular \(C_{37}\) lift of the certified
> nine-orbit quotient.

The conclusion is internal to this displayed constant-generator formal
family.  It does not exclude a higher-\(y\) conjugator or a general
semiregular lift.

## Binary diagonal condition

For a diagonal circulant adjacency block, the coefficient at lag zero is
zero and every other coefficient is in \(\{0,1\}\).  Since
\(N=D-18I\) and

\[
y^{36}=1+x+\cdots+x^{36},
\]

write the diagonal coefficient sequence of

\[
R_A=e^{-zA}N_0e^{zA}
     +\eta z^{18}e^{-zA}Je^{zA}
\]

as \(r(t)\).  A binary diagonal block is possible only if

\[
r(0)=0,\qquad r(t)\in\{18,19\}\quad(t\ne0).
\]

Moreover, the number of nonzero lags with \(r(t)=19\) is the degree of
that diagonal block.  The certified quotient has diagonal degrees

```text
18, 20, 18, 20, 18, 20, 18, 20, 10.
```

## Split semisimple types

Suppose first that \(A\) is diagonalizable over \(\mathbf F_{37}\).
If its two nonzero eigenvalues are distinct, scale them to \(1,\rho\),
where \(\rho\ne0,1\), and let

\[
v_0=P_0\mathbf1,\qquad v_1=P_1\mathbf1,\qquad
v_\rho=P_\rho\mathbf1.
\]

At any lag outside

\[
\{0,\mathord\pm1,\mathord\pm\rho,
  \mathord\pm(\rho-1)\},
\]

the \(N_0\) term has no coefficient.  At coordinate \(i\), the remaining
coefficient, after removing \(19y^{36}J\), is \(6\eta F_i(t)\), where

\[
\begin{aligned}
F_i(t)={}&\chi(t)(v_{0i}^2+v_{1i}^2+v_{\rho i}^2)\\
&+(\chi(t-1)+\chi(t+1))v_{0i}v_{1i}\\
&+(\chi(t-\rho)+\chi(t+\rho))v_{0i}v_{\rho i}\\
&+(\chi(t-(\rho-1))+\chi(t+(\rho-1)))
v_{1i}v_{\rho i}.
\end{aligned}
\]

Binary coefficients require \(F_i(t)\in\{3,-3\}\).  The verifier checks
all 35 projective ratios \(\rho\) and all \(37^2\) triples satisfying
\(v_{0i}+v_{1i}+v_{\rho i}=1\).  None survives.

If the nonzero eigenvalue is repeated and semisimple, there are only two
spectral projectors.  The analogous exhaustive local check over the 37
possibilities \(v_{0i}+v_{1i}=1\) also has no survivor.  This is the
rank-two projector version of the earlier rank-one character-pattern
obstruction.

## A universal local function code for all other types

Let \(E_\pm(z)=e^{\pm zA}\).  Every diagonal entry of
\(E_-ME_+\), for any constant matrix \(M\), belongs to the span \(V(A)\)
of all products

\[
(E_-)_{ar}(E_+)_{sb}.
\]

Consequently every diagonal correction \(r(t)\) belongs to the larger
similarity-invariant space

\[
W(A)=V(A)+z^{18}V(A).
\]

This is an over-approximation: it forgets that \(M=N_0\), that the second
matrix is \(J\), and that \(A\) is symmetric.  Therefore failure inside
\(W(A)\) is a valid obstruction to the actual family.

Rank two leaves only the following rational/Jordan types after the split
semisimple cases:

1. an irreducible quadratic primary block;
2. a nonzero \(2\times2\) Jordan block;
3. one nonzero eigenline plus a \(J_2(0)\) block;
4. \(J_3(0)\);
5. \(J_2(0)\oplus J_2(0)\).

Scaling \(A\) merely decimates the 37 cyclic coefficients, so the
verifier uses projective representatives.  There is one trace-zero
irreducible class and 18 trace-one irreducible classes.  For every class
the exact intersection

\[
W(A)\cap\bigl(\{0\}\times\{18,19\}^{36}\bigr)
\]

is computed by row reduction.  A word is determined by its values on an
information set, so at most \(2^{13}=8192\) candidates are tested.

The complete results are:

```text
type                                      compatible-word weights
irreducible quadratic (all 19 classes)    18 (exactly QR and NR)
nonzero Jordan block                      16,17,18,19,20
nonzero eigenline + J2(0)                 16,17,18,19,20
J3(0)                                     18 (exactly QR and NR)
J2(0) + J2(0)                             18 (exactly QR and NR)
```

None permits weight 10.  The ninth diagonal block of the certified
quotient has degree 10, so every nonsplit and every nonsemisimple rank-two
type is impossible.

## Reproduction

Run:

```text
python3 verify_rank_two_conjugation_obstruction.py
```

The computation is exact over \(\mathbf F_{37}\), takes only a few
seconds, and uses negligible memory.
