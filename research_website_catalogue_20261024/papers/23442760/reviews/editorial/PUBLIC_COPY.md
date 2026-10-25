# Quadratic convergence of SOS-density bounds on convex bodies

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X

Version 1.0, 17 October 2026 · Unrefereed preprint · CC BY 4.0

## Original abstract

For every fixed compact convex body K⊂ℝⁿ with nonempty interior and every real polynomial f, the normalized Lebesgue sum-of-squares density bound of degree at most 2r has error O_{K,f}(r⁻²) for every integer r≥1. We give a self-contained proof and an explicit constant, using one global square. A quadratic Taylor upper estimator reduces the objective to a scalar endpoint problem. Homothetic contraction compares every sublevel shell with the same core mass that normalizes a fixed power of a Dirichlet polynomial; that mass cancels before summation. This proves the quadratic upper rate in the convex-body/Lebesgue regime of the 2018 Oberwolfach question. A classical interval example shows that the exponent is sharp in the worst case. The proxy and the broad localization and relative-mass mechanisms have established precedents; no firstness or new-method claim is made.

## In plain language

A polynomial can be minimized by concentrating a sum-of-squares probability density near one of its minimizers. This note proves a quadratic error rate on every fixed full-dimensional compact convex body with Lebesgue measure, using a single global square.

## Main result

Let $K\subset\mathbb R^n$ be compact and convex with nonempty interior, with $n\ge1$, and let $f$ be a real polynomial. The bound $H_r(f,K)$ minimizes $\int_K f q\,dx$ over global sums of squares $q$ of degree at most $2r$ subject to $\int_K q\,dx=1$. For every integer $r\ge1$, the error satisfies $0\le H_r(f,K)-f_*\le C_nG/r^2$, where $f_*=\min_K f$.

For any minimizer $a$, set $H=\max_K\|\nabla^2f\|_{\mathrm{op}}$, $\gamma=1+H/2$, $g(x)=\nabla f(a)\cdot(x-a)+\gamma\|x-a\|^2$, and $G=\max_K g$. The theorem gives $0<G<\infty$ and the explicit constant $C_n=4(n+2)^2(\pi/2)^{2n+4}(1+2^{n+2})$. A single square of a real polynomial, normalized over the whole body, witnesses this upper bound.

The objective need not be convex, and the boundary of $K$ need not be smooth or semialgebraic. The same proof applies to objectives of class $C^2$ on an open neighborhood of $K$. The constants belong to the fixed body and objective; no useful bound uniform over all dimensions or degenerating bodies is asserted.

## Why it works

At a constrained minimizer, the gradient points nonnegatively along every segment into the convex body. Taylor's formula therefore supplies the nonnegative quadratic upper proxy $g$. After scaling it to $u=g/G$, contraction toward the minimizer compares every sublevel volume with a smaller one: $F(t)\le(t/s)^nF(s)$ for $0<s\le t$, where $F(t)=\operatorname{vol}_n\{x\in K:u(x)\le t\}$.

An explicit Dirichlet polynomial has a positive core of width proportional to the inverse square of its degree and a controlled tail. A fixed even power makes it a global square. Every dyadic tail shell is bounded relative to the same core mass that lower-bounds the normalizing integral. That mass cancels before summation, leaving the quadratic rate. The degree calculation and a constant-density fallback cover every positive integer order.

For $K=[0,1]$ and $f(t)=t$, the note also proves the classical lower estimate $H_r(f,K)\ge1/[4(r+1)^2]$. The same estimate holds for $f(t,y)=t$ on $[0,1]\times[-1,1]^{n-1}$. Together with the upper theorem, this gives a fixed worst-case instance of order $r^{-2}$ in each dimension. It does not give a positive matching lower rate for every objective; constant objectives have zero error.

## Scope and prior work

The note addresses the convex-body/Lebesgue regime in Laurent's contribution, joint work with de Klerk, to the 2018 Oberwolfach report. It explicitly uses probability densities of unit mass. Slot and Laurent's Theorem 11 gives the earlier $O(\log^2 r/r^2)$ bound for this hierarchy and asks whether the logarithm can be removed.

The constrained-gradient and quadratic-upper-estimator reductions already appear in de Klerk–Laurent and Slot–Laurent. Endpoint polynomial localization and comparison of shell mass with local core mass have classical precedents, including Totik–Varga. Their older endpoint-polynomial theorem, combined with Markov's inequality and the relative-mass argument, also yields the scoped quadratic upper rate. The interval/product worst-case exponent is likewise prior work of de Klerk–Laurent. No firstness or new-method claim is made, and present worldwide open status is not certified.

The theorem uses Lebesgue measure and a quadratic proxy. It does not assert the same rate for arbitrary reference measures or for the restricted hierarchy whose densities must be polynomials of the original objective for general nonconvex $f$. The construction assumes a global minimizer is available; it does not supply an efficient way to locate one or compute all required integrals. The explicit constant is coarse, rather than an optimal asymptotic coefficient.

The complete source and verification archive accompanies the paper. Finite exact checks and numerical examples supplement the written universal proof; they are not certificates of its infinite quantifiers.

## References

[Monique Laurent, joint work with Etienne de Klerk, Convergence analysis of Lasserre measure-based approximations for polynomial optimization, Oberwolfach Report 50/2018, pp. 2991–2993. Report.](https://doi.org/10.4171/owr/2018/50) The convex-body convergence question is interpreted with explicit unit-mass probability densities.

[Lucas Slot and Monique Laurent, Improved convergence analysis of Lasserre's measure-based upper bounds for polynomial minimization on compact sets, Mathematical Programming 193 (2022), 831–871. The cited numbering follows arXiv:1905.08142v2. Journal article.](https://arxiv.org/abs/1905.08142v2) Theorem 11 gives the earlier logarithmic-factor bound; Lemmas 1 and 4 contain the constrained-gradient and quadratic-proxy reductions.

[Etienne de Klerk and Monique Laurent, Comparison of Lasserre's measure-based bounds for polynomial optimization to bounds obtained by simulated annealing, Mathematics of Operations Research 43 (2018), 1317–1325. Article.](https://doi.org/10.1287/moor.2017.0906) The quadratic Taylor upper estimator for general polynomial objectives is an established reduction.

[Vilmos Totik and Tamás Varga, Non-symmetric fast decreasing polynomials and applications, Journal of Mathematical Analysis and Applications 394 (2012), 378–390. Article.](https://doi.org/10.1016/j.jmaa.2012.03.006) The older endpoint-polynomial theorem and shell/core comparison are credited antecedents; the stated older-ingredient deduction is retained.

[Etienne de Klerk and Monique Laurent, Worst-case examples for Lasserre's measure-based hierarchy for polynomial optimization on the hypercube, Mathematics of Operations Research 45 (2020), 86–98. Article.](https://doi.org/10.1287/moor.2018.0983) Interval/Jacobi and product-box examples already establish the classical worst-case quadratic exponent.

[Monique Laurent and Lucas Slot, An overview of convergence rates for sum of squares hierarchies in polynomial optimization, Recent Developments in Industrial and Applied Mathematics (2026), 149–176. Final chapter.](https://doi.org/10.1007/978-981-95-1446-5_8) The final overview records a logarithmic factor for general convex bodies; its contents do not certify worldwide openness.

## Research status

AI tools were used extensively in the solution, derivations, source checks, verification, drafting, and adversarial review. This preprint is unrefereed and has not received external human peer review. It is not a formal proof-assistant certificate.

## Contributions

Substantive proof checks, counterexamples, and precise comparisons with prior work are welcome. Authorship and acknowledgments depend on actual research contributions and mutual agreement.

## Paper and support

The complete 5-page deposited paper is available below.

Download the paper and complete source and verification archive from [the selected Zenodo edition](https://zenodo.org/records/23442760).
