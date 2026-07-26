# Targeted quartic construction search in two frozen \(\delta=3\) strata

**First certified release (UTC):** 2026-07-26T09:43:34Z.

**Status:** exact-computation structural result; not peer reviewed.

> This is AI-assisted research.  Exact symbolic checks are evidence about
> the encoded algebra, not peer review.  The result concerns a frozen
> pair of leading-shape families and is not a universal quartic or degree-bound
> theorem.

## Result

No characteristic-zero Keller counterexample candidate and no
noninjectivity witness was found.

There are two full counterexample exclusions:

- `D3-BB-21` cannot contain a quartic Keller counterexample.  The
  nonzero part of its complete \(E_7\) parameter space is contradicted
  by exact \(E_6/E_5\) coefficients with every lower coefficient
  arbitrary.  At the \(E_7\)-origin, every Keller map exits
  structurally as an automorphism.
- `D3-BS-N2-Z` cannot contain a quartic Keller counterexample.  Its
  complete nonzero \(E_7\) parameter space is covered by two safely
  normalized charts and contradicted by exact \(E_4/E_3\) descent with
  every lower coefficient arbitrary.  Its \(E_7\)-origin has the same
  structural automorphism exit.

These are counterexample exclusions, not claims that the strata contain
no Keller automorphisms.  The exact machine scope is in
[`SCOPE.json`](./SCOPE.json).

## Frozen scope and determinant system

The canonical source is
`../../audit_delta_ge3_denominator/DENOMINATOR.json`, containing exactly
26 families and having SHA-256

```text
440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a
```

The two priority normal forms are
\[
\begin{aligned}
\texttt{D3-BB-21}:&\quad h=pq,\quad R=p^2q,\\
\texttt{D3-BS-N2-Z}:&\quad h=p^2,\quad R=p^2q.
\end{aligned}
\]
For
\[
F=L(p,q,r)^t+H_2+H_3+H_4
\]
we retain the fixed data
\[
H_4=(hp^2,hq^2,0),\qquad H_3=(U,V,R),\qquad
H_2=(A,B,T),
\]
where \(A,B,T\) are quadratic and \(U,V\) are cubic.  Every calculation
comes directly from
\[
\det\!\left(L+zJH_2+z^2JH_3+z^3JH_4\right).
\]
The Keller identities are \(E_j=[z^j]\det(\cdots)=0\) for \(j>0\),
with \(\det L\ne0\).  No BCW reduction is used.

## Exact \(E_7\) tangent spaces

Put
\[
\alpha=J(hq^2,R),\qquad
\beta=-J(hp^2,R),\qquad
\gamma=J(hp^2,hq^2).
\]
The exact verifier reconstructs the entire degree-one and degree-two
syzygy kernels of
\[
\alpha a+\beta b+\gamma c=0.
\]
They give respectively the \(r^1\) and \(r^0\) coefficients of
\((U_r,V_r,T_r)\).
The \(r^2\) block has no \(T_r\) term; a separate rank-two check of
\(\alpha a+\beta b=0\) proves that its kernel is zero.  Thus no
highest-\(r\) tangent is omitted.

For `D3-BB-21`,
\[
(\alpha,\beta,\gamma)
=(-5p^2q^3,-p^4q,8p^3q^3),\qquad
\gcd(\alpha,\beta,\gamma)=p^2q,
\]
and bases are
\[
\left(\frac85p,0,1\right)
\]
in degree one and
\[
\left(-\frac15p^2,q^2,0\right),\quad
\left(\frac85p^2,0,p\right),\quad
\left(\frac85pq,0,q\right)
\]
in degree two.

For `D3-BS-N2-Z`,
\[
(\alpha,\beta,\gamma)
=(-2p^3q^2,-4p^5,8p^5q),\qquad
\gcd(\alpha,\beta,\gamma)=2p^3,
\]
and the corresponding bases are
\[
(0,2q,1)
\]
and
\[
(-2p^2,q^2,0),\quad(0,2pq,p),\quad(4p^2,0,q).
\]

Write the degree-one parameter as \(x\) and the degree-two parameters as
\(y_0,y_1,y_2\).  With the binary summands of \(U,V,T\) zero, but with
every \(r\)-dependent coefficient of \(A,B\) retained, the complete
\(E_6\) compatibility ideals have reduced loci
\[
\begin{array}{c|l}
\texttt{D3-BB-21}
&
x=0,\quad y_2=0,\quad
3y_0^2-8y_0y_1+12y_1^2=0,\\[2mm]
\texttt{D3-BS-N2-Z}
&
x=0,\quad y_1(y_0-y_2)=0.
\end{array}
\]
The verifier checks equality of the full ideals, not only these radicals.
Thus this zero-binary \(E_6\) projection has two rational planes on the
branch-square target and two conjugate nonzero lines over
\(\mathbf Q(\sqrt{-5})\), together with the origin, on the two-branch
target.  Restoring binary summands can affect lower-\(r\) coefficients
of \(E_6\), so this is not an exhaustion of the full \(E_6\) locus with
arbitrary binary data.

## Structural audit of the \(E_7\)-origin

At the \(E_7\)-origin, \(U,V,T\) are arbitrary binary forms.  Write
\[
A_r=a_pp+a_qq+2a_rr,\qquad
B_r=b_pp+b_qq+2b_rr.
\]
The complete \(E_6\) solve, performed with all eleven binary coefficients
present, has rank six.  For `D3-BB-21` it gives
\[
(a_p,a_q,a_r,b_p,b_q,b_r)
=\left(\frac85\ell_8,0,0,0,0,0\right),
\]
whereas for `D3-BS-N2-Z` it gives
\[
(a_p,a_q,a_r,b_p,b_q,b_r)
=(0,0,0,0,2\ell_8,0).
\]

If \(\ell_8=0\), every nonlinear term is binary.  After an invertible
linear target normalization, the map is a triangular extension of a
plane Keller map of degree at most four and hence is an automorphism.

If \(\ell_8\ne0\), the third component is
\[
F_3=\ell_8r+B_3(p,q),\qquad \deg B_3\le3.
\]
It is a coordinate with explicit inverse
\[
r=\frac{F_3-B_3(p,q)}{\ell_8}
\]
of degree at most three.  Straightening it produces plane Keller fibres
of degree at most \(3\cdot4=12<100\); Moh's plane range and the
fibrewise/Ax argument make \(F\) an automorphism.  Thus the origin cannot
contain a counterexample.  This exit is independent of the more
restrictive determinant regression below.

## Auxiliary exact obstruction A: zero binary nonlinear tangent

Here
\[
U=V=T=0,
\]
while \(A,B\) are completely arbitrary ternary quadratics and
\[
L=\begin{pmatrix}
\ell_0&\ell_1&\ell_2\\
\ell_3&\ell_4&\ell_5\\
\ell_6&\ell_7&\ell_8
\end{pmatrix}
\]
is arbitrary.  This retains 12 quadratic coefficients and all nine
linear coefficients.

For both targets, the complete linear solve of every \(E_6\) and \(E_5\)
coefficient has rank eight and gives
\[
\ell_2=\ell_5=0,\qquad
\det L=\ell_8(\ell_0\ell_4-\ell_1\ell_3).
\]
The decisive \(E_4\) squares are
\[
\begin{array}{c|c}
\texttt{D3-BB-21}&
[pq^2r]E_4=\dfrac{24}{5}\ell_8^2,\\[2mm]
\texttt{D3-BS-N2-Z}&
[p^3r]E_4=8\ell_8^2.
\end{array}
\]
In characteristic zero, \(E_4=0\) forces \(\ell_8=0\), hence
\(\det L=0\).  Notice that \(E_6/E_5\) alone still has invertible
solutions; the \(E_4\) descent is essential.

## Exact obstruction B: a nonzero `D3-BS-N2-Z` tangent

Take the degree-two basis direction
\[
U=0,\qquad V=2kpqr,\qquad T=kpr,\qquad k\ne0,
\]
set only the binary summands \(U_0,V_0,T_0\) to zero, and again retain
arbitrary \(A,B,L\).  The complete \(E_6/E_5\) solve localized at \(k\)
has rank 11 and leaves an invertible affine family.  Three \(E_4\)
coefficients are
\[
[p^4]E_4=4k\ell_4,\qquad
[p^3r]E_4=-8k^2\ell_7,\qquad
[p^2q^2]E_4=2k\ell_1.
\]
They force \(\ell_4=\ell_7=\ell_1=0\).  The solved linear determinant is
\[
\det L=
-\ell_0\ell_5\ell_7+\ell_1\ell_5\ell_6
+\ell_2\ell_3\ell_7-\ell_2\ell_4\ell_6,
\]
so it vanishes.  This excludes this entire normalized nonzero tangent
line inside the stated zero-binary-summand ansatz.

## Full `D3-BB-21` nonzero-\(E_7\) descent

The complete \(E_7\) parameterization, with no binary coefficient
specialized, is
\[
\begin{aligned}
S&=ap+bq+cr,\\
U_r&=\frac p5(8S-kp),\\
V_r&=kq^2,\\
T_r&=S.
\end{aligned}
\]
Equivalently,
\[
\begin{aligned}
U&=U_0+\frac{pr}{5}\bigl((8a-k)p+8bq+4cr\bigr),\\
V&=V_0+kq^2r,\\
T&=T_0+(ap+bq)r+\frac c2r^2,
\end{aligned}
\]
where \(U_0,V_0\in k[p,q]_3\) and \(T_0\in k[p,q]_2\) are arbitrary.
Direct substitution also replays \(E_9=E_8=E_7=0\), rather than taking
the two highest identities on trust from the frozen classification.
Write
\[
\begin{aligned}
U_0&=u_0p^3+u_1p^2q+u_2pq^2+u_3q^3,\\
V_0&=v_0p^3+v_1p^2q+v_2pq^2+v_3q^3,\\
T_0&=t_0p^2+t_1pq+t_2q^2,
\end{aligned}
\]
and write \(A_i,B_i\) for the coefficients of
\((p^2,pq,pr,q^2,qr,r^2)\) in \(A,B\).

Selected raw \(E_6\) coefficients successively force
\[
c=0,\qquad b=0,\qquad
C:=12a^2-8ak+3k^2=0.
\]
More precisely,
\[
\begin{aligned}
[pq^2r^3]E_6&=\frac{12}{5}c^2,\\
[pq^4r]E_6\big|_{c=0}&=\frac{24}{5}b^2,\\
[p^3q^2r]E_6\big|_{b=c=0}&=\frac25C.
\end{aligned}
\]
The two endpoint equations are
\[
v_0(3a-k)=0,\qquad u_3(2k-a)=0.
\]

After \(b=c=A_5=B_5=0\), the ordinary \(E_6\) pivots are
\[
\begin{aligned}
B_2={}&av_1,\\
B_4={}&
\frac{-(48a-16k)t_0+(45a-15k)u_0+(a+3k)v_2}{5},\\
A_4={}&
\frac{(16a-32k)t_2+(5a+15k)u_2}{25},\\
A_2={}&
\frac{-(16a+8k)t_1+25au_1+(-3a+6k)v_3+40\ell_8}{25}.
\end{aligned}
\]
Substitution into the whole \(E_6\) polynomial leaves exactly
\[
\frac25C\,p^3q^2r
+\frac35v_0(3a-k)p^6
+3u_3(2k-a)pq^5.
\]
Thus no unlisted \(E_6\) coefficient is being silently discarded.

After these same pivots, a raw \(E_5\) coefficient is
\[
\boxed{
[p^2qr^2]E_5=\frac25ak(8a-k).
}
\]
It is independent of every coefficient of \(U_0,V_0,T_0,A,B,L\).
The two resultants are
\[
\begin{aligned}
\operatorname{Res}_k\!\left(C,ak(8a-k)\right)&=1680a^6,\\
\operatorname{Res}_a\!\left(C,ak(8a-k)\right)&=420k^6.
\end{aligned}
\]
Over characteristic zero, \(C=0\) and \(E_5=0\) therefore imply
\(a=k=0\).  Together with \(b=c=0\), every nonzero \(E_7\) tangent is
impossible.  The remaining origin is the structural automorphism exit
proved above.  Consequently:
\[
\boxed{\texttt{D3-BB-21 cannot contain a Keller counterexample.}}
\]

As a regression, put \(\tau^2=-5\), \(a=3s\), and
\(k=(4+2\tau)s\).  The boxed coefficient becomes
\[
\frac{24}{5}s^3(25+8\tau),
\]
whose norm after removing \(s^3\) is \(108864/5\).  This recovers the
two conjugate lines found in the initial sparse reconnaissance.

## Full `D3-BS-N2-Z` nonzero-\(E_7\) descent

The complete \(E_7\) parameterization is
\[
\begin{aligned}
S&=ap+bq+cr,\\
U_r&=-2kp^2,\\
V_r&=2qS+kq^2,\\
T_r&=S.
\end{aligned}
\]
Thus, with the same arbitrary binary forms \(U_0,V_0,T_0\),
\[
\begin{aligned}
U&=U_0-2kp^2r,\\
V&=V_0+2apqr+(2b+k)q^2r+cqr^2,\\
T&=T_0+(ap+bq)r+\frac c2r^2.
\end{aligned}
\]
The verifier reconstructs these derivatives and substitutes them into
the original weighted determinant.

The coefficient ladder uses only characteristic-zero domain
implications:
\[
\begin{aligned}
[p^3r^3]E_6&=4c^2,\\
[pq^2r^2]E_5\big|_{c=0,\ E_6\text{ pivots}}
  &=-24(b+k)^3,\\
[p^3r^2]E_5\big|_{c=0,\ E_6\text{ pivots},\ k=-b}
  &=-12a^2b,\\
[p^2q^4]E_6\big|_{k=-b}
  &=bu_2+6au_3.
\end{aligned}
\]
Hence
\[
c=0,\qquad b+k=0,\qquad a^2b=0,\qquad bu_2+6au_3=0.
\]
All six lower \(E_6\) pivots have nonzero constant coefficients, and
the verifier replays the complete residual before using this ladder.

The point \(a=b=k=0\) is the structural origin treated above.  On the
remaining locus either \(b=0,a\ne0\), or \(a=0,b\ne0\).  Replacing the
source variable \(r\) by \(r/s\), with \(s\ne0\), sends
\((a,b,k)\) to \((a/s,b/s,k/s)\), leaves the frozen top unchanged, and
scales \(\det L\) by \(1/s\).  The verifier checks this identity
symbolically.  The two nonzero components may therefore be normalized
without a hidden division.

### Chart I: \(a=1,\ b=k=0\)

The last \(E_6\) constraint gives \(u_3=0\).  After the complete ordinary
\(E_6\) pivots,
\[
[p^2q^2r]E_5=4u_2,\qquad
[p^3qr]E_5=8(2t_2-3v_3).
\]
Thus \(u_2=0\) and \(2t_2=3v_3\).  Completing all remaining \(E_5\)
pivots gives
\[
\ell_8=t_1-\frac12v_2,
\]
and then
\[
[p^2r^2]E_4=12v_3.
\]
After \(v_3=0\), the remaining \(E_4\) equations give
\[
\ell_1=\frac{v_2}{2}\ell_2,\qquad
\ell_4=\frac{v_2}{2}\ell_5,\qquad
\ell_7=\frac{v_2}{2}\ell_8.
\]
The second column of \(L\) is therefore \(v_2/2\) times its third
column, so \(\det L=0\).

### Chart II: \(a=0,\ b=1,\ k=-1\)

Here \(u_2=0\), and the complete \(E_6\) pivots leave the following
decisive \(E_5\) coefficients:
\[
3v_0,\qquad
-\frac32(4t_1-u_0-2v_2),\qquad
3u_3(t_1-v_2).
\]
Consequently
\[
v_0=0,\qquad u_0=4t_1-2v_2,\qquad
u_3(t_1-v_2)=0.
\]
After the remaining ordinary \(E_5\) pivots, the whole residual is
\[
6u_3(\ell_8-t_0)pq^4+3u_3(t_1-v_2)q^5.
\]

If \(u_3\ne0\), this forces \(v_2=t_1\) and \(\ell_8=t_0\).
The \(E_4\) equations then give
\[
\ell_6=t_0t_1,\qquad
\ell_3=t_1\ell_5,\qquad
\ell_0=t_1\ell_2.
\]
The first column of \(L\) is \(t_1\) times its third column.

It remains to put \(u_3=0\) and \(d=t_1-v_2\).  First,
\[
[p^3r]E_4=8(\ell_8-t_0)^2,
\]
so \(\ell_8=t_0\).  If \(d\ne0\), all remaining \(E_4\) pivots are
licensed by explicitly checked factors \(d\) or \(d^2\), and contain no
denominators.  After their complete replay,
\[
\boxed{[q^2r]E_3=12d^3,}
\]
a contradiction.

Finally take \(d=0\).  Two ordinary \(E_4\) pivots eliminate
\(\ell_3,\ell_0\), after which
\[
\boxed{[p^3]E_3=-4(-\ell_6+t_0v_2)^2.}
\]
The reduced \(\det L\) is exactly divisible by
\(-\ell_6+t_0v_2\).  Thus \(E_3=0\) again forces \(\det L=0\).
Every nonzero chart is excluded, and the origin is an automorphism
exit.  Consequently:
\[
\boxed{\texttt{D3-BS-N2-Z cannot contain a Keller counterexample.}}
\]

## Modular reconnaissance with all binary summands sampled

The deterministic modular search broadens the exact ansätze by sampling
all
\[
4+4+3=11
\]
binary coefficients of \(U_0,V_0,T_0\).  At each sample, \(A,B\) and
\(L\) remain arbitrary: the script solves all \(E_6/E_5\) identities
over the finite field, parameterizes the complete affine solution space,
and tests \(E_4,\ldots,E_1\) together with \(\det L\ne0\).

The frozen run used good splitting primes \(23,29\), seed `20260726`,
three binary trials for each of seven tangent cases per prime, and up to
512 deterministic affine points per invertible solution space.  It tested
3,072 lower affine points and found no full modular hit.

Prime \(7\) is deliberately rejected: it divides the norm of the decisive
`D3-BB-21` \(E_5\) coefficient and creates a finite-characteristic
degeneration irrelevant to the characteristic-zero target.

This modular absence is not an obstruction and is not used in any exact
claim.  In particular, the arbitrary-binary `D3-BB-21` obstruction above
comes from the exact symbolic coefficient, not from the finite-field
portfolio.

## Reproduction

The exact certificate and the broader default modular portfolio are:

```sh
/usr/bin/python3 verify_ansatz_obstructions.py
/opt/homebrew/bin/gp -q verify_independent_pari.gp
/usr/bin/python3 search_modular.py
```

The PARI/GP verifier independently reconstructs the full
`D3-BB-21` \(E_7\) parameterization, every displayed \(E_6\) pivot, the
decisive \(E_5\) coefficient and resultants, and both structural-origin
\(E_6\) blocks.  It shares no symbolic implementation with the primary
SymPy verifier.

Two additional hostile suites independently reconstruct the complete
fine-family exclusions:

```sh
../d3_bb21_descent/verify_hostile_strict.sh
../d3_bs_n2_z_audit/verify_strict.sh
```

The first uses dependency-free sparse arithmetic over \(\mathbb Q\); the
second reconstructs the full `D3-BS-N2-Z` descent directly in PARI/GP.
Their terminal markers are respectively
`D3_BB21_HOSTILE_RELEASE_AUDIT_PASS` and
`D3_BS_N2_Z_HOSTILE_STRICT_PASS`.

The fail-closed release check is:

```sh
./verify_strict.sh
```

Its final marker is:

```text
D3_CONSTRUCTION_SEARCH_STRICT_PASS
```

The wrapper requires six corrupted primary certificates, an independent
PARI/GP coefficient mutation, optimized-Python assertion bypass, and the
bad-prime modular mutation to fail.

## Limitations

This package does not claim:

- that either excluded stratum contains no Keller automorphisms;
- a quartic-row exclusion or a new global degree bound;
- a characteristic-zero Keller counterexample;
- a noninjectivity witness;
- that modular non-discovery is evidence of impossibility.

The search is a direct homogeneous-determinant calculation and uses no
BCW reduction.
