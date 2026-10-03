# Independently derived boundary analysis

This proof outline was fixed before historical review conclusions or another new audit family's conclusions were read. The only central imported result is the arc reflection theorem explicitly printed as Theorem 1 in Roth's original OWR contribution, pp. 528–529. Its relevant implication is that a positive unrestricted lower limit of hyperbolic distortion at every point of an open circle arc implies holomorphic continuation through the arc with circle-valued boundary values. No independent proof of that published theorem is claimed.

Let Phi(z)=(1-|z|²)|f'(z)|/(1-|f(z)|²) for a holomorphic disk self-map. Its denominator is strictly positive in the disk. Constants have Phi=0 and cannot satisfy the target hypothesis. Schwarz–Pick gives 0≤Phi≤1.

## The actual all-approaches quantifier

If the unrestricted lower limit at 1 is positive, choose c>0 and delta>0 so Phi(z)>c at every disk point with |z-1|<delta. Shrink delta below 1. For every xi on the open circle arc |xi-1|<delta/2, if |z-xi|<delta/2 then |z-1|<delta by the triangle inequality. Thus the unrestricted lower limit at xi is at least c. The imported arc theorem applies with exactly its hypotheses. In particular it applies when the target unrestricted limit equals 1. The arc is open; no assertion about its endpoints is needed. It is enough to obtain a lower bound on each fixed neighboring point; uniform convergence on a preassigned arc was not assumed.

## Nonvanishing derivative, with the sign checked independently

Write eta=f(1), so |eta|=1. Continuity of the holomorphic continuation provides a small neighborhood of 1 in which f has no zeros. The real function u=-log|f| is harmonic there, strictly positive on the disk side, and zero on the circle arc. An elementary barrier proves the Hopf conclusion. Choose a small ball B(c,a), c=1-a, tangent to the circle at 1 and contained in the nonzero neighborhood. The minimum m of u on |z-c|=a/2 is positive. In the annulus a/2<|z-c|<a, the harmonic function v(z)=m log(a/|z-c|)/log 2 has the same inner value m and outer value 0. The maximum principle gives u≥v, because u≥m on the inner circle and u≥0 on the outer circle. Along z=1-t, v=m log(a/(a-t))/log 2. Since u is differentiable across 1, its inward radial derivative is at least m/(a log 2)>0. Consequently the outward radial derivative of log|f| is strictly positive.

Differentiating |f(e^{it})|²=1 at t=0 shows Im(eta_bar f'(1))=0. The outward radial derivative of log|f| is Re(eta_bar f'(1)). Hence eta_bar f'(1)=alpha>0, f'(1)=alpha eta, and f is locally conformal by the complex inverse function theorem. Taylor's theorem gives f(z)=eta+alpha eta(z-1)+O(|z-1|²) for unrestricted complex z near 1. This argument uses local nonvanishing after extension; it never assumes that f has no zeros throughout the disk.

## Necessity, verified independently of the arc theorem's converse

In polar coordinates near 1, set N(r,t)=1-|f(re^{it})|². It vanishes at r=1 along a smaller circle arc and is smooth across that arc. The identity N(r,t)=(1-r) integral_0^1 [partial_r |f|²](1+s(r-1),t) ds follows from the fundamental theorem of calculus. Dividing by 1-r² gives a continuous extension of A(r,t)=N(r,t)/(1-r²). At (1,0) its value is 2alpha/2=alpha. The numerator |f'(re^{it})| tends to alpha. Therefore Phi=|f'|/A tends to 1 along every disk approach to 1, including arbitrarily tangential ones. This establishes the necessary direction without applying l'Hopital along just a radius.

Reflection through the circle is f_ext(z)=1/conjugate(f(1/conjugate z)) on a sufficiently small exterior neighborhood. Nonvanishing in the reflected interior neighborhood makes this expression holomorphic; it agrees with the continuation by the circle boundary identity and local Schwarz reflection/uniqueness.

## Julia inequality is consistent and supplies no extra rigidity

Apply the pseudo-hyperbolic Schwarz–Pick inequality to z and r, then let r increase to 1 using (1-|f(r)|²)/(1-r²)→alpha. It yields |eta-f(z)|²/(1-|f(z)|²) ≤ alpha |1-z|²/(1-|z|²). This is a deduction from Schwarz–Pick and the proved expansion, not an assumption needed to obtain extension. Alpha is finite and positive but is neither forced to equal 1 nor bounded away from 0 independently of f. For general source point xi, the correct real coefficient is conjugate(eta) xi f'(xi)>0; setting xi=1 gives the submitted formula.

## Controls against stronger or weaker interpretations

Powers z^k, k≥2, have Phi=k r^(k-1)/(1+r²+...+r^(2k-2))→1 as r→1, but fail global injectivity. The family exp(-a(1-z)/(1+z)), a>0, has Phi=a u/sinh(a u), u=(1-|z|²)/|1+z|², and boundary derivative a/2. It is zero-free but has an essential singularity at -1, so neither finite Blaschke status nor extension around the entire circle follows.

The radial/non-tangential condition is strictly weaker. In right-half-plane coordinates W=(1+z)/(1-z), take F(W)=W+a log(1+W), a>0, with the principal logarithm. Re W>0 implies Re log(1+W)=log|1+W|>0, so F maps the half-plane into itself. On every fixed non-tangential sector at infinity, F/W→1, F'→1 and Re F/Re W→1, hence its hyperbolic distortion Re W |F'|/Re F tends to 1. On the tangential path W=1+i y, y→∞, its distortion tends to 0 because Re F=1+(a/2)log(4+y²) and |F'|→1. Cayley conjugation gives a disk self-map satisfying the angular/radial distortion limit but failing the unrestricted limit. At each finite boundary value W=i y with y≠0, Re F(i y)=(a/2)log(1+y²)>0, so it does not map any neighboring circle arc to the circle. This is only a check on the weaker interpretation, not a counterexample to the selected condition.

The original statement makes no assumption of a rate of convergence. Rates strong enough to force global automorphisms are different rigidity questions. The neighboring OWR Problem 2 concerns regularity of boundary sets for conformal metrics and is outside this result.
