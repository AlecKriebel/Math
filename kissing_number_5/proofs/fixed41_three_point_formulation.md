# Fixed-cardinality three-point formulation and a degree-5 barrier

## Status

This note does **not** prove that a 41-point code exists. It records:

1. a necessary fixed-cardinality three-point moment formulation for such a
   code; and
2. an exact rational pseudo-distribution satisfying its Bachoc--Vallentin
   blocks through total degree 5 and its two-point inequalities through degree
   20, together with a separately reoptimized certificate through degrees 6
   and 30.

Consequently, these particular finite relaxations are feasible and cannot
prove that 41 points are impossible.

## Measures and the exact marginal identity

Let \(C\subset S^4\) have \(N=41\) points and pairwise inner products at most
\(s=1/2\). Define the distinct-pair measure

\[
 \alpha(B)=\frac1N\#\{(a,b)\in C^2:a\ne b,\ a\cdot b\in B\}.
\]

It is a nonnegative measure on \(I=[-1,1/2]\) of mass \(N-1=40\).
Define the symmetric all-distinct-triple measure

\[
 \nu(E)=\frac1N\#\{(a,b,c)\in C^3:
 a,b,c\text{ pairwise distinct},\
 (a\cdot b,a\cdot c,b\cdot c)\in E\}.
\]

It is supported on

\[
 D=\{(u,v,t)\in[-1,1/2]^3:
 \Delta(u,v,t)=1+2uvt-u^2-v^2-t^2\ge0\}
\]

and has mass \((N-1)(N-2)=1560\).

With the Bachoc--Vallentin normalization

\[
 x(u,v,t)=\frac1N\#\{(a,b,c)\in C^3:
 a\cdot b=u,\ a\cdot c=v,\ b\cdot c=t\},
\]

the full three-point measure decomposes as

\[
 x=\delta_{(1,1,1)}
   +\int_I\bigl(\delta_{(1,q,q)}+\delta_{(q,1,q)}
                    +\delta_{(q,q,1)}\bigr)\,d\alpha(q)
   +\nu.
\]

For every Borel set \(B\subseteq I\), counting the first point after fixing
the ordered pair represented by the third coordinate gives

\[
 \pi_t x(B)=N\alpha(B).
\]

Substitution in the displayed decomposition gives the exact fixed-size
marginal identity

\[
 \pi_t\nu=(N-2)\alpha=39\alpha.
\]

Symmetry gives the same identity for the \(u\)- and \(v\)-marginals. In
polynomial form, for every polynomial \(h\),

\[
 \int_D h(t)\,d\nu=39\int_I h(q)\,d\alpha(q).
\]

This is linear only after \(N\) has been fixed.

## Harmonic matrix convention

Let \(P_k^{(m)}\) denote the normalized Gegenbauer polynomial for \(S^{m-1}\),
so \(P_k^{(m)}(1)=1\). For \(m=5\),

\[
 (k+2)P_k^{(5)}(q)
 =(2k+1)qP_{k-1}^{(5)}(q)-(k-1)P_{k-2}^{(5)}(q).
\]

For the stabilizer of one point in \(S^4\), define the polynomialized
transverse kernel

\[
 Q_k(u,v,t)=
 ((1-u^2)(1-v^2))^{k/2}
 P_k^{(4)}
 \left(\frac{t-uv}{\sqrt{(1-u^2)(1-v^2)}}\right).
\]

The expression extends polynomially to the boundary. The verifier evaluates
it by

\[
 Q_0=1,\qquad Q_1=t-uv,
\]

\[
 Q_{k+1}
 =\frac{2(k+1)}{k+2}(t-uv)Q_k
  -\frac{k}{k+2}(1-u^2)(1-v^2)Q_{k-1}.
\]

For total degree \(d\) and \(0\le k\le d\), set

\[
 Z_{k,d}(u,v,t)
 =\bigl(u^iv^jQ_k(u,v,t)\bigr)_{0\le i,j\le d-k}.
\]

The addition formula for spherical harmonics implies the necessary condition

\[
\begin{split}
 H_{k,d}={}&Z_{k,d}(1,1,1)\\
 &+\int_I\left(
 Z_{k,d}(1,q,q)+Z_{k,d}(q,1,q)+Z_{k,d}(q,q,1)
 \right)d\alpha(q)\\
 &+\int_D Z_{k,d}(u,v,t)\,d\nu(u,v,t)\succeq0.
\end{split}
\]

Using monomials instead of the radial Gegenbauer basis in the original
Bachoc--Vallentin paper is harmless: the two bases of polynomials of degree at
most \(d-k\) differ by an invertible change of basis, and the corresponding
matrices are congruent. Positive normalization factors from the addition
formula likewise do not affect positive semidefiniteness.

The ordinary two-point necessary inequalities are

\[
 1+\int_I P_\ell^{(5)}(q)\,d\alpha(q)\ge0
 \qquad(\ell\ge1).
\]

## Exact pseudo-distribution

The certificate
[`fixed41_bv_degree5_pseudodistribution.json`](../certificates/fixed41_bv_degree5_pseudodistribution.json)
places \(\alpha\) on

\[
 \{-1,-3/4,-1/2,-1/4,0,1/4,1/2\}
\]

and \(\nu\) on all 51 feasible permutation orbits over this grid. A stored
\(\nu\)-weight is the **total mass of the full permutation orbit**, not the
mass of each ordered triple.

The dependency-free exact verifier checks:

- every stored weight is a positive rational number;
- \(\alpha(I)=40\) and \(\nu(D)=1560\);
- every support triple lies in the full closed domain \(D\), including all
  determinant-zero boundary cases;
- each of the seven coordinate marginals satisfies
  \(\pi_t\nu=39\alpha\) exactly;
- the two-point Gegenbauer inequalities are strict for
  \(1\le\ell\le20\);
- all six matrices \(H_{k,5}\), \(0\le k\le5\), are positive definite, using
  exact Sylvester minors.

Run:

```text
python3 verifiers/verify_fixed41_bv_degree5.py
```

The minimum checked two-point moment is

\[
 \frac{282160579}{25600000000}>0.
\]

Because the measures are explicit positive atomic measures on \(I\) and
\(D\), they automatically satisfy every scalar moment and support-localizing
constraint at every order. The precise limitation is harmonic: the same
weights fail at total degree 6. In the \(k=0\) block \(H_{0,6}\), the principal
submatrix indexed by radial monomials \(1,u^3,u^5,u^6\) has determinant

\[
 -\frac{
 4444715971702706358727445076649065883676021
 }{
 7036874417766400000000000000000000000000000000
 }<0.
\]

Thus this certificate proves feasibility only through the stated degrees. In
fact, reoptimization repairs the obstruction:
[`fixed41_bv_degree6_pseudodistribution.json`](../certificates/fixed41_bv_degree6_pseudodistribution.json)
is a second exact rational pseudo-distribution on the same support. The same
verifier checks all \(H_{k,6}\), \(0\le k\le6\), as positive definite and
checks the two-point inequalities through degree 30. Its minimum checked
two-point moment is

\[
 \frac{87069760969}{32000000000000}>0.
\]

Neither certificate makes a claim beyond its stated exact degrees.

### Exact full-radial feasibility through harmonic degree 16

A third reoptimization gives
[`fixed41_bv_fullradial_k8_pseudodistribution.json`](../certificates/fixed41_bv_fullradial_k8_pseudodistribution.json).
It is checked in a basis-free finite-support form. Let

\[
 E=\{-1,-3/4,-1/2,-1/4,0,1/4,1/2,1\}.
\]

For each harmonic degree \(k\), collect the coefficient of a pair of radial
test functions at \(u,v\in E\) into the \(8\)-by-\(8\) matrix \(W_k\). Then
every finite radial block has the factorization

\[
 H_{k,r}=V_r^{\mathsf T}W_kV_r,
\]

where \(V_r\) is the evaluation matrix of the chosen radial polynomial basis
on \(E\). Therefore \(W_k\succeq0\) proves positivity for **every** radial
degree, not merely one monomial truncation.

The verifier proves \(W_k\succeq0\) exactly for \(0\le k\le8\). For \(k=0\),
the marginal identities force the kernel vector

\[
 (-1/40,-1/40,-1/40,-1/40,-1/40,-1/40,-1/40,1),
\]

and the complementary \(7\)-by-\(7\) principal block is positive definite.
For \(k>0\), the endpoint rows \(u=\pm1\) vanish and the active
\(6\)-by-\(6\) interior block is positive definite. All assertions use exact
Sylvester minors. The same certificate satisfies the two-point inequalities
through degree 50, with minimum checked moment

\[
 \frac{6551770997}{4000000000000}>0.
\]

This exactly establishes feasibility at total degrees 7 and 8 (indeed, for
arbitrary radial degree at harmonic degrees through 8).

A final reoptimization,
[`fixed41_bv_fullradial_k16_pseudodistribution.json`](../certificates/fixed41_bv_fullradial_k16_pseudodistribution.json),
passes the identical exact kernel-matrix verification through harmonic degree
16 and the two-point inequalities through degree 100. Its minimum checked
two-point moment is

\[
 \frac{197167927189}{128000000000000}>0.
\]

Thus no true negative eigenvalue occurs in this mechanism through \(k=16\);
the numerical discovery solution had a smallest active-block eigenvalue about
\(2.0\cdot10^{-6}\), and rationalization at denominator \(10^{14}\) retained
exact positivity.  The subsequent exact parity-tail analysis in
[`fixed41_bv_all_harmonics.md`](fixed41_bv_all_harmonics.md) proves that this
same certificate in fact passes every harmonic degree, as well as every
ordinary two-point Gegenbauer inequality.  It is still only a
pseudo-distribution, not a 41-point code.

## Exact dual certificate format for a future contradiction

Let \(R_k(q)=Z_k(1,q,q)+Z_k(q,1,q)+Z_k(q,q,1)\). A finite-degree
infeasibility certificate can use \(c_\ell\ge0\), matrices \(F_k\succeq0\),
polynomials \(h_1,h_2,h_3\), a scalar \(\lambda\), and polynomials
\(r_\alpha,r_\nu\) certified nonnegative on \(I,D\), respectively. It is
enough to verify the polynomial identities

\[
\sum_\ell c_\ell P_\ell^{(5)}(q)
+\sum_k\langle F_k,R_k(q)\rangle+r_\alpha(q)
-39\sum_{i=1}^3h_i(q)+\lambda=0,
\]

\[
\sum_k\langle F_k,Z_k(u,v,t)\rangle+r_\nu(u,v,t)
+h_1(u)+h_2(v)+h_3(t)=0,
\]

and the strict rational inequality

\[
\sum_\ell c_\ell+\sum_k\langle F_k,Z_k(1,1,1)\rangle-40\lambda<0.
\]

Integrating the first two identities and using the mass and marginal
equalities expresses the last quantity as a sum of nonnegative terms, a
contradiction. For a machine-checkable SOS version, one may take

\[
 r_\alpha=\sigma_0+(q+1)(1/2-q)\sigma_1
\]

and

\[
 r_\nu=\tau_0+\sum_{z\in\{u,v,t\}}
 \bigl((z+1)\tau_{z,-}+(1/2-z)\tau_{z,+}\bigr)
 +\Delta\tau_\Delta,
\]

with rational SOS Gram matrices. Exact polynomial coefficient comparison and
rational \(LDL^{\mathsf T}\) checks would then turn a numerical dual into a
rigorous nonexistence proof.
