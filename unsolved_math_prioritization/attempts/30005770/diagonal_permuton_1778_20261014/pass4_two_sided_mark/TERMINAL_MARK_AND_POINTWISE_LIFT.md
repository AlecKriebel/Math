# Terminal exponential marks and a pointwise incoming-to-outgoing lift

Shared PASS4, row1778 /30005770, 14 October 2026.

## Exact setting

Let a_n=|Av_n(1324)|, lambda=lim a_n^(1/n), rho=1/lambda, and

    c=C(rho),       gamma=log c,
    C(s)=(1-sqrt(1-4s))/(2s).

Use the canonical normalized staircase states A in the nonempty class Av(213), the exact directed greedy kernel K, and its outgoing and incoming path sums h_A(z), ell_A(z). In particular

    sum_A z^|A| h_A(z)=sum_A z^|A| ell_A(z)=F(z)-1,
    F(z)=sum_n a_n z^n.

The last-state counting series is z^|A| ell_A(z), whereas the first-state series is z^|A|h_A(z). These are exact path enumerations of the finite avoidance class. No uniform law for an interior state is assumed.

The accepted first-frontier estimate from PASS3 gives, for every 0<eta<gamma, a constant C_eta such that the number of size-n avoiders whose first cell has size at least m is at most

    C_eta lambda^n exp(-eta m)                              (1)

simultaneously for all n,m. It also proves that

    G_out(z,u)=sum_A u^|A| z^|A| h_A(z)<infinity              (2)

for every 0<z<rho and every 1<u<c, with the same u throughout that z interval.

We prove the analogous incoming estimate and, more strongly, a pointwise comparison of the exact completion factors. Neither result discards their product in the unresolved two-sided mark.

## 1. A terminal cell is a first-frontier subset after one of two symmetries

Let pi have canonical normalized chain A_1,...,A_r and let its last cell have size m and normalized state A=A_r. The involution S used in normalization is reverse-complement-inverse.

- If r is even, the terminal cell is alone in the lowest occupied staircase row. All its points lie below every other cell, so they are precisely the m smallest values. Its actual pattern is S(A), an Av(132) permutation. Reverse-complement maps this strip to the top m values, with pattern rc(S(A))=A^{-1}, which avoids213.
- If r is odd, the terminal cell is alone in the rightmost occupied staircase column. Its points are precisely the final m positions. Its actual pattern is A in Av(213). Inversion maps this strip to the top m values with pattern A^{-1}, also in Av(213).

Both reverse-complement and inversion preserve1324 avoidance. In either case the image has a top m-value interval avoiding213. Its first greedy cell therefore has size at least m. We do not claim that it has size exactly m, or that either symmetry reverses the full canonical chain.

Writing M_last(pi) for terminal size and T(pi) for first size, this proves

    M_last(pi)<=T(rc(pi))       when r is even,
    M_last(pi)<=T(pi^{-1})      when r is odd.               (3)

Each parity branch is a size-preserving injection. Forgetting the parity has fibres of size at most two. Thus the terminal tail count is at most twice the corresponding first-cell tail count. Equation (1) yields an absolute uniform exponential terminal tail.

## 2. A three-point guard makes the first state exact

For a nonempty state A define

    P(A)=12 skew-sum A^{-1}.                                 (4)

This lies in Av(213), and the map A -> P(A) is injective. Take either image q from Section1, of size n, whose top a=|A| values induce A^{-1}. Put b=n-a. Prefix three new points in the position order

    n+2, b+1, n+3,

then all old points in their old position order, increasing each old value greater than b by one and leaving all old values at most b unchanged. Call the new permutation q^+; its size is n+3.

It avoids1324. An occurrence using only old points would already be in q. The first new point cannot occur: as the first global position it could only be the1, but too few later points are larger than it. The third new point is the global maximum and could only be the4; only two positions precede it. The middle new point, if used, must be the1 of a new occurrence; its other three points would all be old points above it and form213. Those points are in the old top a-value interval, which avoids213. This excludes every new occurrence.

The top a+2 values of q^+ induce exactly12 skew-sum A^{-1}=P(A), and so avoid213. The next value below them is the middle guard point. Including it forms213 with the two upper guard points. Hence the first canonical state of q^+ is exactly P(A), not merely a state containing it.

The guard is inverted by removing the first three global positions and standardizing. Together with the parity bit, this recovers the original pi. Therefore, for each fixed A and n,

    # {size-n avoiders with last normalized state A}
       <=2 # {size-(n+3) avoiders with first state P(A)}.    (5)

No assumption about the pattern of the old points below the top interval was used. In particular this guard applies to a complete permutation, not just a two-cell domino.

## 3. Pointwise completion-factor comparison

Multiply (5) by z^(n+3) and sum over n. Nonnegativity allows enlarging the image series to all objects with first state P(A). Since |P(A)|=|A|+2,

    z^(|A|+3) ell_A(z)<=2 z^(|A|+2) h_(P(A))(z).

Equivalently, the coefficientwise formal-series statement is z*ell_A(z)<=2*h_(P(A))(z). Thus, for every nonempty state A and 0<z<rho,

    ell_A(z)<=(2/z) h_(P(A))(z).                            (6)

This controls the exact incoming factor pointwise by an explicitly padded outgoing state. It is not a scalar-size Markov assumption and not a bound by h_A itself.

Summing (6), using injectivity of P and (2), gives the explicit incoming-mark estimate

    G_in(z,u):=sum_A u^|A|z^|A|ell_A(z)
       <=[2/(u^2 z^3)] G_out(z,u)<infinity                  (7)

for every 1<u<c and every z<rho. The simpler tail argument in Section1 proves the same finiteness without the pointwise refinement. Both preserve the exact finite uniform law when coefficients are divided by a_n.

## 4. Endpoint joint marks

The same size-n absolute moment bound now holds for the first and last sizes separately. If u,v>=1 and

    log u+log v<gamma,

then their joint endpoint moment is bounded by a constant times lambda^n. To prove this when both marks exceed one, put t=log u+log v and theta=log u/t. Holder's inequality over the finite size-n class gives

    sum_pi u^T(pi) v^M_last(pi)
      <= [sum_pi exp(t*T(pi))]^theta
         [sum_pi exp(t*M_last(pi))]^(1-theta)
      <= constant * lambda^n.                              (8)

The cases u=1 or v=1 use the corresponding one-sided bound directly. Thus the joint endpoint series converges for every z<rho. This marks the two endpoints of one path. It is not the two-sided completion weight of one interior state.

## 5. What straightforward product estimates actually give

Throughout this section u>=1 (and the target is u>1). The desired arbitrary-state mark is

    H(z,u)=sum_A (uz)^|A| ell_A(z) h_A(z).                   (9)

It is already known, without any exponential mark, that

    H(z,1)<=z F'(z)<infinity       for z<rho.

The elementary coefficient estimate also gives H(z,u)<=uz F'(uz) whenever uz<rho, since the number of marked cells is at most total size and a marked cell has size no greater than total size.

Here is the direct product consequence of the new two one-sided marks. Choose z<r<rho and 1<v<c. Set

    f_A=(vr)^|A| h_A(r),       g_A=(vr)^|A| ell_A(r).

Both families are summable by (2) and (7). By nonnegative coefficients, h_A(z)<=h_A(r) and ell_A(z)<=ell_A(r). Hence if

    uz <= (vr)^2,

then

    H(z,u)<=sum_A f_A g_A<infinity,                         (10)

where summability follows, for example, from sum f_A g_A <=(sum f_A)(sum g_A).

Allowing independent radii and marking parameters on the two factors replaces (vr)^2 by their product. Its supremum is the same rho^2 c^2. Thus this straightforward two-factor route gives at most the region

    uz<rho^2 c^2=rho(c-1),                                 (11)

using c=1+rho c^2. For actual1324, lambda>4, so c<2 and c-1<1. Therefore (11) is strictly contained in the already available trivial region uz<rho. Even at lambda=4 it would not improve that trivial region. This precisely identifies the radius mismatch; separate exponential first and last marks do not, by this product argument, supply a fixed u>1 valid up to z=rho.

Equation (6) sharpens the remaining problem to a product of outgoing factors at A and P(A):

    H(z,u)<=(2/z)sum_A (uz)^|A|h_A(z)h_(P(A))(z).            (12)

No estimate for that paired product with a common positive marking margin is established here. The padding map and inverse-pattern dependence must be retained if it is used in a later argument.

## Inputs, audit, and finite scope

- Exact staircase kernel: `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`, SHA-256 dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03.
- Absolute first-frontier and common outgoing mark: `pass3_kernel_bounds/WEIGHTED_OPERATOR_BOUNDARY.md`, SHA-256 b4b2057622a189442bcff813648db124642862ce65f3805bc843bc25550d9597.
- The primary staircase geometry is credited to Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Proposition1 and proof: https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf .

The three-point guard is adapted from the accepted PASS3 unrestricted-domino guard; the proof above explicitly verifies its extension to an arbitrary old lower region. Separate structural and analytic reviews are required. Finite checks are supplementary indexing tests, not asymptotic evidence.

The1324 anti-diagonal limit and the universal fixed-alpha target remain unresolved by this note.
