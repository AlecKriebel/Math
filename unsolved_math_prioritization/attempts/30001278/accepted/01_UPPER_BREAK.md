# Approach 1: compare the established upper break with the different

Use the notation of `NORMALIZATIONS.md`. Caruso's Theorem 3.28 gives

\[
\mu_{L/K}\leq U:=1+es+
\max\left\{eb-p^{-s},\frac e{p-1}\right\}.
\tag{1}
\]

This is a credited established result, not a theorem first proved here. The analysis below asks exactly when it implies the desired different bound.

## Exact sufficient region

Subtract the target \(B=1+es+eb-p^{-s}\):

\[
U-B=\delta:=\max\left\{0,
\frac{e(p^a-r)}{(p-1)p^a}+p^{-s}\right\}.
\tag{2}
\]

The first entry of (1) is the maximum if and only if

\[
e(r-p^a)\geq\frac{p-1}{p^n}.
\tag{3}
\]

The right side lies strictly between zero and one. Since the left side is an integer, (3) holds exactly when \(r\geq p^a+1\). In that range, (1) and the different-versus-break inequality give

\[
v_K(\mathcal D_{L/K})<\mu_{L/K}\leq B
\]

if \(L/K\) is ramified. If it is unramified, \(0<B\) gives the same conclusion.

Thus every semistable representation, at every rank and every exponent, satisfies the target in the entire region \(r\geq p^a+1\). For \(a=0\), this includes \(r=2,\ldots,p-1\). It also includes every endpoint \(b=1\).

## Precisely what the theorem does not yield alone

If \(r\leq p^a\), then

\[
U=1+e\left(s+\frac1{p-1}\right),\qquad
\delta=\frac{e(p^a-r)}{(p-1)p^a}+p^{-s}>0.
\tag{4}
\]

For \(a\geq1\), the exceptional integers are

\[
(p-1)p^{a-1}+1\leq r\leq p^a;
\]

there are \(p^{a-1}\) of them. When \(a=0\), the exceptional integer is just \(r=1\). The loss is bounded by

\[
0<\delta<\frac{e}{p(p-1)}+p^{-s}
\]

when \(a\geq1\); at \(r=p^a\), it is exactly \(p^{-s}\). No estimate of the form \(d<U\), without a quantified positive gap, implies \(d\leq U-\delta\).

For a concrete arithmetic check, \((p,e,n,r)=(3,1,2,7)\) gives

\[
a=2,\quad b=7/18,\quad s=4,\quad
B=871/162,\quad U=11/2,\quad\delta=10/81.
\]

Replacing the maximum in (1) by its first argument would remove a real positive term in this example.

## Why a merely qualitative gap is insufficient

For a totally ramified finite Galois extension with inertia order \(m\), in shifted upper numbering one has

\[
d:=v_K(\mathcal D_{L/K})=
\int_0^{\mu_{L/K}}\left(1-\frac1{|G^{(u)}|}\right)du.
\tag{5}
\]

This follows from the lower-numbering different sum and the Herbrand change of variables. On the initial shifted interval \((0,1]\), inertia has order \(m\), accounting for the tame term \(1-1/m\). Consequently

\[
d\leq \mu_{L/K}(1-1/m)\leq U(1-1/m).
\tag{6}
\]

This gives an additional valid sufficient condition \(U/m\geq\delta\), when the actual ramification degree is known. But the problem places no bound on rank or inertia order. The elementary inequality \(d<\mu\) alone has no uniform numerical margin. This is a logical limitation of this deduction, not a constructed counterexample to the conjecture, nor a claim that arbitrary profiles in (5) are realized by the specified semistable representations.

**Outcome:** a complete credited-theorem consequence on a large parameter region, plus an exact remaining loss. The full problem is not settled by Approach 1.
