# Independent review: monochromatic multipeaked alignment states

**Verdict: PASS_SCOPED_RELAXED_KERNEL_ENERGY_AND_ORBITAL_STABILITY.** No mandatory mathematical correction was found. The exact branch, global energy minimization, full-interaction Hessian and stated orbital Lyapunov conclusion are valid. The pure harmonic is excluded from the original physical kernel class, so the original conjecture remains **unsolved, 2/5 approaches**. No new-discovery, human-peer-review, or full physical-instability resolution is certified.

Reviewed `PARTIAL_RESULT.md`: SHA-256 `c94c1ab20bce9f571225305660f3d15074bcf9295afe01792473ecdb3b2906d0`. The submitted mathematical snapshot remained unchanged throughout the review.

## 1. Exact source and the kernel-class distinction

I read the full Primi contribution in [OWR24/2009, printed pp.1356–1359](https://publications.mfo.de/bitstream/handle/mfo/3125/OWR_2009_24.pdf?isAllowed=y&sequence=1). Its orientational angle is smooth, odd and periodic, and its physical attraction/repulsion description explicitly imposes one interior sign change in the positive half-circle. The multipeak conjecture occurs in the discussion of the Fokker–Planck approximation with positive small noise. A stability norm is not specified there. Rotational families of steady states are explicitly acknowledged, so the artifact's orbital formulation is appropriate and does not claim phase convergence.

The complete [Primi–Stevens–Velazquez revised preprint](https://webdoc.sub.gwdg.de/ebook/serien/e/MPI_Math_Nat/preprint2007_34.pdf), Lemma2.1 and Theorem7.1, was checked. Theorem7.1 lists smoothness, periodicity, oddness and conditions (35)–(36); it does not list the physical single-sign-change restriction. The report's displayed first-order stationary equation lacks the diffusion factor present in its preceding second-order equation; the full paper retains that factor. The submitted calculation uses the full paper's correct normalization.

For a sin(2πNx), the averaged kernel equals the original kernel, the sampled derivative sum is positive, and its integrated averaged potential is strictly positive on every nonempty compact subinterval required by (36). There are exactly N−1 interior zeros in (0,1/2), with alternating signs. For N≥3, this fails the physical single-sign-change requirement. The example is therefore a valid relaxed-class diagnostic, not a counterexample within that physical class.

The published [Carrillo–Gvalani–Pavliotis–Schlichting paper](https://doi.org/10.1007/s00205-019-01430-4), Proposition6.1 and its proof, was checked in the full source. It already identifies the nonuniform generalized-Kuramoto branch as a free-energy minimizer and describes its low-temperature concentration. The artifact correctly credits this result. The later [Bertoli–Goddard–Pavliotis paper](https://doi.org/10.1093/imamat/hxaf001) provides corroborating context, not a substitute for the nonlinear argument.

## 2. Exact branch and global minimization

The circle-length and diffusion constants are consistent: c=a/(2πN), D=σ²/2 and κ=c/D. Thus the nonuniform branch threshold κ>2 is exactly σ²<a/(2πN). The normalization integral is independent of the harmonic number N, by periodic change of variables. The convolution and logarithmic derivative in the stationary equation cancel precisely when b=κI1(b)/I0(b).

The coefficient-ratio proof of uniqueness is valid. Both power series converge absolutely on compact sets. Pairing derivative-numerator terms of unequal indices gives strictly negative terms, because the coefficient ratios 1/[2(j+1)] strictly decrease. This proves strict decrease of r(b)/b; the limits 1/2 and zero follow respectively from the first coefficients and 0<r(b)<1. The root exists uniquely for κ>2. Differentiating r as a tilted expectation gives its strictly positive variance, and strict ratio monotonicity gives κr'(b)<1 at the root.

The entropy identity is exact with the factor one-half in the interaction energy. The auxiliary parameter z is κm(f), so completing the interaction term gives KL(f||f_z)+E(|z|), with E(ρ)=ρ²/(2κ)−logI0(ρ). Its derivative changes sign only at the positive root b, apart from the stationary endpoint zero. Therefore b is the unique radial global minimum. Equality in relative entropy forces f=f_z, and self-consistency identifies exactly the phase orbit of the stated density. No restriction to 1/N-periodic perturbations is imposed in this argument. Densities with infinite entropy cannot be additional minimizers.

The low-noise conclusion also follows: r(b)/b=1/κ forces b→∞, while the periodic Laplace concentration gives equal masses at the N maxima. The equality of masses is a positive-temperature minimization conclusion; it should not be confused with an assertion that every zero-temperature measure on those points has the same entropy.

## 3. Full interaction Hessian

The second entropy variation is D∫h²/f_b. Differentiating the full interaction term contributes −c|m(h)|². These are exactly the two terms retained in equation (7). In particular the interaction is not held fixed at its equilibrium value.

Under the tilted density, cos−r and sin are orthogonal mean-zero functions. Their squared norms are C=r'(b)>0 and S=r(b)/b=1/κ. The second identity follows by integrating the derivative of sin(t)e^{b cos(t)} over a period. Orthogonal decomposition in the entire mean-zero weighted L² space gives the displayed form

$$Q=\alpha^2C(1-\kappa C)+\|u_\perp\|^2.$$

Its radial coefficient is strictly positive, and the sole zero direction is the phase derivative, proportional to f_b sin(2πNx). This conclusion is for the quadratic form; no unjustified operator-domain or spectral-gap theorem is inferred from it.

I read the complete [June2025 correction](https://academic.oup.com/imamat/article/90/2/231/8157363). It explicitly says that the discussed operator freezes the convolution at an invariant measure. That is different from the full McKean–Vlasov derivative. An independent exact diagnostic makes the distinction visible even at the uniform equilibrium: on the Nth cosine mode, the full linearization has eigenvalue (2πN)²D(κ/2−1), whereas the frozen operator has eigenvalue −(2πN)²D. Thus a frozen-convolution spectral calculation alone cannot supply the nonlinear stability conclusion. The submitted proof does not rely on that calculation.

## 4. Nonlinear evolution and the precise stability topology

For fixed D>0 and smooth periodic V, the claimed smooth mass-one evolution is justified. Convolution and its first derivative are uniformly bounded in terms of the kernel and conserved mass. In the expanded equation, these bound the transport and zeroth-order coefficients on any finite time interval. The maximum principle preserves nonnegativity and gives a finite exponential-in-time supremum bound. Local heat-semigroup construction, followed by these bounds and parabolic regularization, extends the solution globally and makes it strictly positive at positive times. No uniform-in-noise estimate is needed or claimed.

The gradient-flow dissipation identity is correct: the first variation is D(logf+1)−c m(f)·(cos,sin), and its spatial derivative reproduces the diffusion-plus-interaction flux. Integration by parts on the circle gives the nonpositive dissipation. For smooth initial densities with zeros, positive-time regularization and continuity of x log x at zero justify the initial-time energy limit.

The energy-to-orbit argument is rigorous and does not require a local Hessian coercivity estimate. If Δ=(F(f)−F_min)/D, the exact identity gives both KL(f||f_z)≤Δ and E(|z|)−E(b)≤Δ. Pinsker gives ||f−f_z||₁≤√(2Δ). Also |z|≤κ. The strict radial minimum on [0,κ] gives a positive energy gap away from any fixed neighborhood of b. Once |z| is close to b>0, keep its phase and compare radii. Direct differentiation of the normalized exponential family gives ||f_{ρ,θ}−f_{b,θ}||₁≤2|ρ−b|. Hence

$$\operatorname{dist}_{L^1}(f,\mathcal O_b)\le\sqrt{2\Delta}+2\bigl||z|-b\bigr|.$$

This proves the claimed epsilon-delta implication from small excess energy to small L¹ distance from the entire phase orbit. Energy dissipation propagates it for all nonnegative times. Sufficiently small L∞ perturbations of any fixed orbit member have small excess energy, since that density is smooth and bounded away from zero. The bounds may depend on the fixed noise parameter and equilibrium.

Accordingly, the actual conclusion is exactly the energy-small or L∞-small initial-data statement with an L¹ orbital output. It is not an L¹-to-L¹ basin theorem, asymptotic orbital convergence, fixed-phase selection, or uniform-in-noise decay rate. The artifact states these limits correctly.

## 5. Reproduction and outcome

All **21,141 submitted exact assertions** replayed with a byte-identical receipt. The independent checker passed **941 exact assertions**, deriving Taylor coefficients from cosine moments, checking derivative-numerator signs, differentiating both energy terms, verifying the Hessian and its kernel, and comparing full versus frozen Fourier linearizations. The all-parameter series and parabolic arguments were audited analytically; finite controls do not certify them by sampling.

From this directory:

```sh
(cd author_replay && python verify.py)
python independent_checks.py
```

The submitted checker uses standard-library Python; the independent checker also uses SymPy. Both regenerate deterministic receipts.

The complete relaxed-kernel result is sound and already related to credited generalized-Kuramoto theory. Its physical-kernel exclusion is decisive. Retain the original conjecture as unresolved after two routes, without claiming a new physical counterexample or importing the corrected frozen-convolution spectrum into a nonlinear stability theorem.
