# Independent source audit: the equivariant-center period problem

**Verdict: PASS_EXACT_PUBLISHED_RESOLUTION.** Gasull–Rojas's published Theorem A covers every parameter and the full origin period annulus in the original Problem 16. Recommended status: **already_solved, 0/5 original proof attempts**. No mandatory correction is required. The resolution is credited to its authors; this audit is not a new analytic proof or a novelty claim.

The frozen `KNOWN_RESULT.md` has SHA-256 `383e6a3493fbe287e1fa1c163d01224e8f5c34b6c9f4f31c27193dd7995b2620`. All 32,500 submitted reduction controls reproduce byte-identically. The separate checker passes 9,270 exact controls. Neither set of checks independently proves the published global analytic theorem.

## 1. Exact original and published coverage

I read Section 3.5 of Gasull's full problem paper and inspected the rendered original p.16. The requested equation is

\[
\dot z=iz+(z\bar z)^n z^{k+1},\qquad n,k\in\mathbb Z_{>0},
\]

and the question concerns decreasing period throughout the **period annulus of the center at the origin**. Conjugation belongs only in the radial factor z·bar(z); replacing the final z power by a conjugate monomial would give a different problem. The surrounding discussion includes n=0 as an isochronous comparison, but Problem 16 itself requires n>0 and k>0. [Original primary source, Section 3.5 and Problem 16](https://arxiv.org/abs/2012.02524).

I inspected the full publisher HTML, including equation (1), Theorem A, Theorem B and Section 4's reduction, and the rendered preprint Theorem A. The published equation is the identical monomial with an arbitrary nonzero complex coefficient a. Theorem A states decreasing period for every positive integer n,k and all a≠0, with limiting periods 2π at the center and 2(k+n)π/(k+2n) at the outer boundary. Setting a=1 covers the entire original request. The introduction explicitly identifies Gasull's Problem 16 as the target. [Published Theorem A](https://link.springer.com/article/10.1007/s00009-025-02879-2).

The publisher verifies the title, authors Armengol Gasull and David Rojas, Mediterranean Journal of Mathematics 22, article 112, and version-of-record publication on 24 June 2025. The full preprint is arXiv:2411.12408v1. This is a published result, not merely a recent unverified announcement. The present audit accepts the published analytic theorem as an imported result and verifies its exact application; it does not recertify every resultant and Sturm calculation in its proof.

## 2. Symmetry and reversibility correction

Writing the nonlinear term as z^(n+k+1)·bar(z)^n shows that rotation by omega multiplies it by omega^(k+1), while the vector field output transforms by omega. Thus omega^k=1 is the correct symmetry condition. The imported Z_(k+2) label is inconsistent with this monomial and is properly corrected to Z_k. In particular, the correction does not change the equation or impose a different parameter restriction.

For rho=exp(iπ/k), the real-linear involution R(z)=rho·bar(z) satisfies F(Rz)=−R(F(z)): the nonlinear coefficient comparison uses rho^k=−1, and conjugation changes i to −i in the linear part. The linearization is rotation. This agrees with the source's reversible-center convention.

Although unnecessary for a=1, the stronger published coefficient claim is also consistent with physical time: the spatial substitution z=cw, with |c|=|a|^(−1/(2n+k)) and arg(c)=−arg(a)/k, changes the coefficient to one without changing time.

## 3. Parameter and period normalization

Direct polar differentiation yields

\[
\dot r=r^{2n+k+1}\cos(k\theta),\qquad
\dot\theta=1+r^{2n+k}\sin(k\theta).
\]

With m=2n+k, R=r^m, Theta=k theta and tau=k t, the radial coefficient is b=m/k>1. Cartesian coordinates X+iY=R exp(i Theta), followed by x=−(1+b)Y, y=−(1+b)X and s=−tau, give

\[
x_s=-y+xy,\qquad
y_s=x+D x^2+(D+1)y^2,\qquad
D=-\frac{k}{2(k+n)}\in(-1/2,0).
\]

I recalculated the chain rule and quadratic coefficients. The inequalities are strict for the original n,k>0, so the isochronous endpoints are excluded. The time reversal does not change a positive period.

The k-fold angular map must not be mistaken for a one-to-one coordinate change on the punctured plane. A full orbit around the original center comprises k repeated sectors, each corresponding to one turn of the quadratic orbit. The time change tau=k t divides the physical sector time by k relative to the quadratic period, so the k sectors cancel that factor. Hence the full physical periods agree, as stated explicitly in the published Section 4. There is no missing factor k in the boundary period.

For an additional consistency check, the quadratic full annulus is x<1 in the relevant parameter range. Since x=−(1+b)R sin Theta, its pullback has dot(theta)=1−x/(1+b)>b/(1+b)>0. Thus the angular traversal used in the period comparison does not stop inside that annulus. The radial transformation is strictly increasing away from the center, so it preserves the ordering of nested origin orbits. The source's full theorem, rather than a local Taylor coefficient alone, supplies the asserted global monotonicity and boundary coverage.

Finally,

\[
\frac{\pi}{D+1}=\frac{2(k+n)\pi}{k+2n},\qquad
\pi<\frac{2(k+n)\pi}{k+2n}<2\pi.
\]

These are the stated physical-time limits. No claim about other centers, n=0, k=0, or every reversible quadratic center is needed.

## 4. Reproduction and justified status

The submitted checker was replayed and compared with the frozen receipt. The independent program checks parameters, phase exponents, quadratic coefficient identities and rational chain-rule values, including the positive angular lower bound on the stated annulus. Its 9,270 assertions are supplementary source-application controls.

```
cd author_replay
python verify.py
cd ..
python independent_checks.py
```

The exact source request is covered by the published theorem, so an already-solved source correction is justified. The unrelated nonautonomous equation in campaign record 4700009 is not used. Preserve the distinction between a published analytic theorem and finite reduction checks, and credit Gasull–Rojas throughout publication.
