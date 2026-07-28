# An all-copy theorem for complete qutrit graph-orbit codes

## Theorem and scope

Let \(A_n\) be the \(n\times n\) matrix over \(\mathbb F_3\) with zero
diagonal and every off-diagonal entry equal to one.  Let \(|G_n\rangle\)
be its qutrit graph state.  For every nonzero
\(s\in\mathbb F_3^n\), consider the logical qutrit orbit
\[
 |k\rangle_L=Z^{ks}|G_n\rangle,\qquad k\in\mathbb F_3.            \tag{1}
\]
Then every rank-two projection inside this three-dimensional orbit obeys
\[
 \boxed{Q_n(P)\geq0\quad\text{for every }n\geq1.}                \tag{2}
\]

For odd \(n\), equality occurs when all entries of \(s\) are the same
nonzero value and the omitted logical state is an eigenstate of the Weyl
line \((1,1)\), after the harmless relabelings described below.  For even
\(n\), this family is strictly positive.

This is an exact all-copy theorem for one structured code family.  It does
not prove the Werner endpoint inequality for an arbitrary rank-two code.

## 1. Reduction to five signed coset sums

Use the notation and the proved logical-Weyl reduction from
`agent_qutrit_graph_codes.md`.  For
\((a,b)\in\mathbb F_3^2\), define
\[
 K_{a,b}
 =\sum_{\substack{t\in\mathbb F_3^n\\s\cdot t=-b}}
 (-1)^{n-w_a(t)}2^{w_a(t)},                                  \tag{3}
\]
where \(w_a(t)\) is the number of sites at which
\[
 (t_i,(A_nt)_i+a s_i)\ne(0,0).                               \tag{4}
\]
The minimum over all logical two-planes is
\[
 \min_P Q_n(P)
 =\frac{2K_{0,0}+
 \min\{K_{1,0},K_{0,1},K_{1,1},K_{1,2}\}}
 {3^n2^{n-1}}.                                                \tag{5}
\]
It is therefore enough to prove that the numerator in (5) is
nonnegative.

Write
\[
 n_r=|\{i:s_i=r\}|,\qquad r=0,1,2.                            \tag{6}
\]
Permuting sites preserves every \(K_{a,b}\), while multiplying \(s\) by
two only relabels the four nonzero Weyl lines.  Thus the three counts in
(6), up to exchanging \(n_1,n_2\), contain all relevant information.

## 2. A nine-character formula

Put \(\omega=e^{2\pi i/3}\).  For a fixed vector \(t\), let
\[
 q=\sum_i t_i.
\]
Since \((A_nt)_i=q-t_i\), a site with syndrome value \(r\) is an identity
site precisely when
\[
 t_i=0,\qquad q+ar=0.                                        \tag{7}
\]

Insert two character projectors, one for \(\sum_i t_i=q\) and one for
\(s\cdot t=-b\).  If \(\chi,\psi\in\mathbb F_3\) are their character
indices, the one-site sum is
\[
 f_{q,a,r}(\chi+\psi r)
 =\begin{cases}
 3,&q+ar=0,\ \chi+\psi r=0,\\
 -3,&q+ar=0,\ \chi+\psi r\ne0,\\
 6,&q+ar\ne0,\ \chi+\psi r=0,\\
 0,&q+ar\ne0,\ \chi+\psi r\ne0.
 \end{cases}                                                  \tag{8}
\]
Indeed, in the first two lines the \(t_i=0\) summand has weight \(-1\)
and the other two have weight \(2\); in the last two lines all three
summands have weight \(2\).

Consequently
\[
 \boxed{
 9K_{a,b}
 =\sum_{q,\chi,\psi\in\mathbb F_3}
 \omega^{-\chi q+\psi b}
 \prod_{r:n_r>0}
 f_{q,a,r}(\chi+\psi r)^{n_r}.}                              \tag{9}
\]
Although (9) is written with \(\omega\), the terms pair to give the real
integer (3).  Formula (9) has only 27 terms, independently of \(n\).

## 3. Syndromes using one value

The only admissible one-value case has all entries equal to the same
nonzero value.  Exchange \(1,2\) if needed.  Direct evaluation of (9)
gives
\[
 K_{0,0}=3^{n-1}\bigl(1+2(-1)^n\bigr),                       \tag{10}
\]
\[
 K_{1,0}=K_{0,1}=K_{1,2}=3^{n-1}2^n,                         \tag{11}
\]
\[
 K_{1,1}=3^{n-1}\bigl(1-(-1)^n\bigr).                        \tag{12}
\]
For even \(n\), the minimum line is zero and
\[
 2K_{0,0}=6\cdot3^{n-1}>0.                                  \tag{13}
\]
For odd \(n\), the minimum is \(K_{1,1}=2\cdot3^{n-1}\), while
\(K_{0,0}=-3^{n-1}\).  Hence
\[
 2K_{0,0}+K_{1,1}=0.                                        \tag{14}
\]
This proves the theorem and the stated equality case in this stratum.

## 4. Syndromes using two values

There are two cases up to relabeling: the active values are
\(\{0,1\}\) or \(\{1,2\}\).  Put
\[
 x=n_r,\qquad y=n_{r'},\qquad x,y\geq1,\qquad x+y=n.          \tag{15}
\]
The \(K_{0,0}\) expression in either case has the form
\[
 9K_{0,0}
 =2\,6^n+3^n\varepsilon,                                    \tag{16}
\]
where \(\varepsilon\) is a sum of four signs with absolute
coefficients \(1,2,4,2\).  Thus
\[
 K_{0,0}\geq\frac{3^n}{9}(2^{n+1}-9)>0
 \quad(n\geq3).                                              \tag{17}
\]
When \(n=2\), necessarily \(x=y=1\); direct substitution in (9) gives
\(K_{0,0}=9>0\).

For the \(K_{0,1}\) line, the analogous sign coefficients have total
absolute value six, so
\[
 9K_{0,1}\geq3^n(2^{n+1}-6)>0.                              \tag{18}
\]

It remains to bound the three lines with \(a=1\).  Every one of their
formulas is either manifestly nonnegative, or is bounded below by
\[
 6^n-3^x6^y-6^x3^y
 =6^n\left(1-2^{-x}-2^{-y}\right)\geq0.                     \tag{19}
\]
The last inequality follows from \(x,y\geq1\), with equality possible
only at \(x=y=1\).  Therefore all four candidate line values are
nonnegative, while \(K_{0,0}>0\).  The numerator in (5) is strictly
positive.

For auditability, (16)--(19) can also be read directly from the following
unscaled monomials supplied by (9).  In the \(\{0,1\}\) case,
\[
\begin{aligned}
9K_{0,0}={}&
3^x3^y+2\,3^x(-3)^y+4(-3)^x(-3)^y
+2(-3)^x3^y+2\,6^x6^y,\\
9K_{1,0}={}&
3^x6^y+2(-3)^x6^y+6^x6^y
+6^x3^y+2\,6^x(-3)^y,\\
9K_{1,1}=9K_{1,2}={}&
3^x6^y-(-3)^x6^y+6^x6^y
+6^x3^y-6^x(-3)^y.
\end{aligned}                                                \tag{20}
\]
The \(\{1,2\}\) formulas differ only by which one of the three \(a=1\)
lines has the coefficients \(2\) instead of \(-1\); the same bound (19)
applies.

## 5. Syndromes using all three values

Now \(n_0,n_1,n_2\geq1\), so \(n\geq3\).  Formula (9) gives
\[
 9K_{0,0}=2\,6^n+3^n\varepsilon_0,\qquad |\varepsilon_0|\leq9,
                                                                    \tag{21}
\]
and
\[
 9K_{0,1}=2\,6^n+3^n\varepsilon_1,\qquad |\varepsilon_1|\leq6.
                                                                    \tag{22}
\]
Hence both quantities are strictly positive because
\[
 2^{n+1}>9,\qquad 2^{n+1}>6\qquad(n\geq3).                  \tag{23}
\]

The three \(a=1\) lines coincide and are manifestly positive:
\[
 \boxed{
 9K_{1,b}
 =3^{n_0}6^{n_1+n_2}
  +6^{n_0}3^{n_1}6^{n_2}
  +6^{n_0+n_1}3^{n_2}>0
 \quad(b=0,1,2).}                                           \tag{24}
\]
Thus \(K_{0,0}\) and all four line candidates are positive, proving
strict positivity in the final stratum.

Sections 3--5 exhaust every nonzero syndrome and prove (2).  Notice that
the only cancellation occurs in the one-value, odd-length family (14);
every syndrome using at least two values has a strictly positive endpoint
numerator at every length.

## 6. Independent exact checker

`discovery/search_complete_graph_codes.py` evaluates (3) by a nine-state
integer transfer.  A direct \(3^n\)-term enumeration was independently
compared with it for random syndromes and every one of the five
\((a,b)\) values through \(n=6\).  The results agreed exactly.

The checker can scan one representative of every syndrome orbit at each
length.  Its output through \(n=58\) reproduced (13)--(14) as the global
minimum: zero at odd length and a positive value at even length.  That
finite scan is not the proof of the theorem; the uniform proof is the
27-character evaluation and case analysis above.
