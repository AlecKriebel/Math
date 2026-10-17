# Proof 17  Dominant endpoint entropy and nearby power comparisons

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Exact one phase integration of the entropy kernel](14_one_phase_entropy.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Setup and exact input

Let independent `Z_j` be uniform on the complex unit circle. By independent Haar phase changes and an overall sign, a real centered-cross sign comparison can be written

`U=c+sum_(j=0)^(n-1)(a_j Z_j+b_j/Z_j)`,

`V=c+sum_(j=0)^(n-1)(a_j Z_j+s_j b_j/Z_j)`,

where `c,a_j,b_j>=0`, `s_j in {-1,+1}`, and, if convenient, `a_j>=b_j` by reversing the corresponding phase. Write `K(z)=|z|^2 log|z|`, `K(0)=0`.

The exact one-phase integration formula is the independently accepted one-phase formula in [Exact one phase integration of the entropy kernel](14_one_phase_entropy.md), SHA-256 `6ba4304c78cf26263996475da83e6e8f54f4258bd55a27bdecf95ad91152b534`. If `a>0` and both roots of `az^2+wz+b` are in the closed unit disk, it states

`E_Z K(aZ+b/Z+w)=(a^2+b^2+|w|^2) log a+|w|^2+b^2+(b/(2a)) Re(w^2)`. (1)

It permits real signed `b` and unit-circle or repeated roots.

## Theorem: explicit entropy gap in a dominant-endpoint regime

Choose one index, denoted `0`, with `a=a_0>0`, `b=b_0`. Let `Y` be an independent bounded circularly symmetric random variable and let `|Y|<=rho` almost surely. Suppose

`a >= b+c+sum_(j>=1)(a_j+b_j)+rho`. (2)

Then

`E K(U+Y)-E K(V+Y)`

`= (b/(2a))*[(1-s_0)c^2+2 sum_(j>=1)(1-s_0 s_j)a_j b_j] >=0`. (3)

The value is independent of the circular-noise law as long as (2) remains true.

### Proof, including the root boundary

Condition on every variable except `Z_0`, and put

`w_s=c+sum_(j>=1)(a_j Z_j+s_j b_j/Z_j)+Y`.

By the triangle inequality, `|w_s|+b<=a`. For a strict inequality, Rouché's theorem on the unit circle compares `az^2` with `w_s z+s_0 b`: the two roots of their sum are strictly inside the disk. In the non-strict case, replace the leading coefficient by `a+epsilon`, apply the strict result, and let `epsilon` decrease to zero. Continuity of polynomial roots puts both roots in the closed disk. This also treats vanishing or repeated roots. Thus (1) applies to every conditional polynomial.

Haar orthogonality and independent zero means give

`E |w_s|^2=c^2+sum_(j>=1)(a_j^2+b_j^2)+E|Y|^2`,

`E Re(w_s^2)=c^2+2 sum_(j>=1)s_j a_j b_j`.

Here circular symmetry gives `E Y=E Y^2=0`, including `Y=0`. The other terms in (1) have the same average for every sign pattern, while its final term is `(s_0 b/(2a)) E Re(w_s^2)`. Subtraction proves (3). Every summand in the bracket is nonnegative.

For a dominant pair that is flipped, (3) becomes

`(b/a)[c^2+2 sum_(j>=1:s_j=+1) a_j b_j]`.

For a dominant pair that is unflipped, it becomes

`(2b/a) sum_(j>=1:s_j=-1) a_j b_j`.

In particular, `b=0` makes the entropy gap zero for all sign patterns under (2). No strict power conclusion follows from this first derivative in a zero-gap case. Other equality cases are precisely characterized by the zero bracket in (3), without asserting equality of higher moments.

## Quantitative prescribed-power interval when the entropy gap is positive

Let `X=U+Y`, `W=V+Y`, and choose a common deterministic support bound `R>0`, for example

`R=c+sum_j(a_j+b_j)+rho`.

Their second moments agree. Put

`delta=[E K(X)-E K(W)]/R^2`.

Because the second moments agree, this is also exactly

`E K(X/R)-E K(W/R)`;

the scale-dependent quadratic term cancels. If `delta>0`, then for

`2<p<min(3, 2+e^2*delta)` (4)

there is strict power comparison `E|X|^p>E|W|^p`. The inequality is non-strict at an included upper endpoint `p=2+e^2*delta<=3`.

To prove this quantitatively, define `D(p)=E|X/R|^p-E|W/R|^p`. Boundedness by one permits twice differentiating for all `p>=2`, with the integrands defined as zero at zero. The elementary maximum

`sup_(0<=t<=1) t^p (log t)^2=4/(e^2 p^2)<=1/e^2`

shows `|D''(p)|<=2/e^2`. Also `D(2)=0` and `D'(2)=delta`. Taylor's integral formula therefore gives

`D(p)>=(p-2)*delta-(p-2)^2/e^2`. (5)

This proves (4), including all claimed boundary distinctions. The bound is uniform in the circular-noise law satisfying (2). Formula (5) in fact applies beyond 3 up to the stated quadratic bound's positive endpoint, but the target here is `2<p<3`.

## Scope

The theorem treats every centered-cross dimension and every real sign pattern in (2), and provides a nontrivial near-2 prescribed-power interval whenever (3) is positive. It includes genuinely unequal nonzero endpoints, mixed pair-product signs, and center sizes outside the previously accepted center-dominant condition. It does not establish the kernel comparison for noise radii beyond the margin in (2). Consequently it is not a full radial-bisubharmonic cone theorem and does not prove all powers or arbitrary radial-noise robustness for this coefficient regime. It is a sign comparison; arbitrary coefficient-box monotonicity is not asserted for the nonconvex entropy test.

## Exact rational mixed-sign example

Take `n=2`,

`a_0=4, b_0=1, a_1=1, b_1=1/2, c=1`,

and flip only the first pair (`s_0=-1,s_1=+1`). The endpoint condition holds with independent circular noise bounded by `rho<=1/2`. Both endpoint pairs are genuinely unequal and nonzero. The center does not satisfy the old sufficient condition `c>=3 sum_j(a_j+b_j)`.

The exact entropy gap is `1/2`, at every allowed noise law. With `Y=0`, `R=15/2`, hence `delta=2/225`, and (5) proves the strict power inequality throughout

`2<p<2+2e^2/225`, approximately `2<p<2.065681`.

With the uniform bound `rho<=1/2`, take `R=8`; then `delta=1/128`, giving strict comparison throughout `2<p<2+e^2/128`, approximately `2<p<2.057727`, uniformly over those noise laws. These examples are positive certificates, not witnesses against any majorant claim.
