# Prior-proof dependency audit and limits

This document checks the route from the cited published theorem to the exact original question. The established Frank–Lieb theorem is the credited mathematical input. We do not label this a new independent proof of every theorem it uses.

## A. Main paper, with published numbering

All energies below include the common factor \(1/2\). Put \(I_\mu[\rho]=\frac12\iint\rho(x)|x-y|^\mu\rho(y)\,dx\,dy\), \(m=\|\rho\|_1\), and
\(A[\rho]=(2m)^{-1}\inf_a\|\rho-1_{B_m+a}\|_1\).

1. **Theorem 2.1 (preprint Theorem 3)** is a quantitative fixed-ball convolution inequality for arbitrary densities in \([0,1]\), not merely for indicators. The convolution ball radius is restricted to a fixed middle interval relative to the mass-ball radius. The density extension is explicitly provided in the supplement, rather than inferred from the set theorem without argument.
2. **Theorem 2.3 (preprint Theorem 5)** integrates the fixed-ball inequality by layer cake for the increasing kernel \(r^\alpha\). It gives
   \(I_\alpha[\rho]-I_\alpha[1_{B_m}]\ge c m^{2+\alpha/N}A[\rho]^2\).
   Outside the middle radius interval the deficit is nonnegative by rearrangement; inside it the quantitative bound contributes a positive constant times \(m^{\alpha/N}\). The homogeneity and positivity require \(\alpha>0\).
3. **Proposition 2.5 and Lemma 2.6** bound the Coulomb/Riesz loss by \(C m^{2-\lambda/N}\theta^2\), provided \(1_{(1-\theta)B_m}\le\rho\le1_{(1+\theta)B_m}\) and \(0\le\theta\le1\). Positive definiteness of the Riesz quadratic form discards a nonnegative term. The potential of a ball has bounded derivative at its boundary when \(\lambda<N-1\), producing the quadratic shell bound. For \(N=3,\lambda=1\) this is the ordinary Coulomb potential. No assumption that \(\rho\) is an indicator or that its support has a smooth boundary occurs.
4. **Lemma 3.1** proves the ball potential crosses its boundary value with a quantitative outward slope for sufficiently large mass. Attraction scales as \(R^{N+\alpha}\), repulsion as \(R^{N-\lambda}\), so \(R^{-\alpha-\lambda}\) is small. The local slope estimate and far-field monotonicity yield the correct signs inside/outside the ball. The adjacent Euler–Lagrange discussion is a consistency check, not a convexity-based sufficiency argument for general \(\alpha\).
5. **Proposition 3.3** combines attraction gain, minimality against a ball, and the bathtub bound on repulsive potential to obtain \(A[\rho]\le C m^{-(\alpha+\lambda)/N}\). This is only an initial closeness estimate and by itself does not prove rigidity.
6. **Lemma 3.5** modifies a density by filling some interior deficit and deleting equal exterior mass. It preserves \(0\le\rho\le1\), total mass and the direction of deviation from the ball, reduces the \(L^1\) error, and guarantees that at least half the changed mass lies outside the selected boundary shell. The two cases compare interior missing mass with exterior excess mass. They work for fractional densities.
7. **Lemma 3.6** improves the potential bound when the error is confined to a shell. Its exponent \(1-\lambda/(N-1)\) is positive; in the target it is \(1/2\). The transverse integral is locally finite precisely in the required range. **Lemma 3.7** supplies a support-diameter bound for minimizers. For the target parameters this is exactly the earlier theorem whose full proof was checked, so no reliance on an omitted general-dimensional extension is needed.
8. **Proposition 3.4** iterates the density modification at widths \(2^{-n}\). The main potential term decreases energy; the attractive remainder is controlled by the diameter bound, and the repulsive remainder by the shell lemma. Set \(\epsilon_n=2^nR^{-N}\|\rho_{n-1}-1_B\|_1\). While \(\epsilon_n\) is below a fixed small bound, a single mass threshold makes the energy-decrease coefficient strictly positive. Minimality then forces every change to vanish. If a first crossing occurs, the preceding shell has width at most \(C A[\rho]\); if none occurs, the unchanged density lies in every shrinking shell and already equals the ball almost everywhere. Constants depend on \(N,\alpha,\lambda\), not on the chosen minimizer or iteration count.
9. **Section 3.4, p. 1261**, uses the resulting shell with \(\theta=C A[\rho]\le1\) in the reverse bound. Hence
   \[
   c m^{2+\alpha/N}A[\rho]^2
   \le C' m^{2-\lambda/N}A[\rho]^2.
   \]
   Once \(m^{(\alpha+\lambda)/N}>C'/c\), a positive asymmetry is impossible. For the target the exponent is \((\alpha+1)/3>0\). Asymmetry zero means equality to a translate of the ball, because the translation infimum is attained: the overlap is continuous, tends to zero at infinity and is positive for some translate. This is exact rigidity at each sufficiently large mass.

## B. Densities, translations and the supplement

Frank–Lieb, *A note on a theorem of M. Christ*, arXiv:1909.04598v1, gives the exact density theorem used above. All 18 pages were read at proof-chain level. Its proof has three relevant reductions:

- Near a ball, radial surplus/deficit profiles give a quadratic form on the sphere. Mass cancels the degree-zero mode. A centering condition cancels degree one, and the spectral gap on the remaining modes controls the deficit
- Shell modification and a small translation reduce a density with small \(L^1\) asymmetry to that local setting. The translation is obtained from a continuous vector field and Brouwer's theorem. Centering is introduced within the proof; it is not an extra restriction on the optimization problem
- General densities are compared with an indicator of the same mass; the set case uses a monotone, measure-preserving symmetrization flow. The error estimates first give a weaker bound away from balls, then the local proposition supplies the required quadratic bound

The appendix computes the relevant spherical-harmonic eigenvalues and proves a gap below the translation eigenvalue. Its special-function formulas and the standard Riesz/bathtub principles remain credited classical inputs. Christ's primary Theorem 1, strict-admissibility convention and Proposition 11 flow with proof were checked. The flow is built from common Steiner operations, so it preserves equality of the two repeated sets and fixes the centered ball. The full general three-set theorem and every earlier Steiner-flow construction were not re-certified. For unbounded finite-measure sets the bounded-set flow argument is passed through truncation and continuity; the main application also has the explicit diameter bound below.

Some preprint displays have typographical sign/index slips. For example, the radius defined by \(\int_R^{R_+}r^{N-1}dr=F^+\) must satisfy \(R_+^N=R^N+NF^+\), and a ball-overlap function decreases with separation. The audit uses these defining identities and the stated inequalities; it does not promote such transcription slips to a different theorem. We do not claim an error-free line-by-line recertification of all printed displays.

## C. Exact earlier diameter and existence inputs

**Diameter.** Frank–Lieb, arXiv:1607.07971v4, Section 4, Theorem 7 (published Theorem 4.1), treats exactly \(N=3\), Coulomb repulsion and every \(\alpha>0\). The full proof was checked: an energy bound puts at least half the mass in one ball; removing a small neighborhood and dilating the remainder gives a potential bound on the essential support; a far point would then contradict that bound. Trial balls yield \(E_\alpha(m)\le C_2m^{5/3}+C_3m^{2+\alpha/3}\), and hence diameter at most \(C_\alpha\max\{1,m^{1/3}\}\). The unrelated no-flat-spots theorem and liquid/solid phase results are not necessary for the later rigidity proof.

**Existence.** The 2021 paper cites Choksi–Fetecau–Topaloglu, Ann. IHP C 32 (2015), Theorem 2.1. Its full-density class \(\mathcal A\) permits arbitrary mass and cap, and is not radially restricted for \(-N<p<0<q\). Set \(p=-1\), \(q=\alpha\), cap 1. That paper uses \(|x-y|^\alpha/\alpha+|x-y|^{-1}\), without the factor \(1/2\). A harmless dilation matches the coefficients: take \(\ell=\alpha^{-1/(\alpha+1)}\), \(\rho(x)=\eta(x/\ell)\). Then
\[
 E_\alpha[\rho]=\frac{\ell^5}{2}\iint\eta(u)\bigl(|u-v|^{-1}+|u-v|^\alpha/\alpha\bigr)\eta(v)\,du\,dv,
\]
with mass \(m=\ell^3\int\eta\) and unchanged cap. Thus existence is nonvacuous for every original mass. The theorem's hypotheses and this normalization were checked; its entire concentration-compactness proof and Lions' theorem were not independently recertified.

## D. Scope of the audit

The original question, published theorem and its complete main proof were checked beyond their wording, with the density, mass, translation and normalization issues traced to explicit lemmas. The source-resolution recommendation relies on the established theorem and identified external inputs. It is not a claim that finite sanity controls prove the analytic inequalities, nor that every cited classical proof has been rebuilt from first principles. No general quantitative gap for arbitrary densities, sharper threshold, other kernel, or intermediate-mass result is certified here.
