# Independent review: an unrestricted Lyapunov-dimension maximizer counterexample

**Verdict: PASS for the complete counterexample to the literal unrestricted assertion in record 4900006.** No mandatory mathematical correction was found. This verdict does not resolve the historical Lorenz-specific question, any chaotic/transitive-attractor formulation, or a generic/typical-system refinement. It does not establish novelty or human peer review.

The reviewed `COUNTEREXAMPLE.md` has SHA-256 `a9ea8220014aed7c082c995023a3bc7cdd10014544a85376d99267d908323266`. The original artifact remains unchanged. The independent review was performed with gpt-6-astra at xhigh reasoning on 2026-09-30.

For a queue tracking the **actual imported statement**, which quantifies over smooth dissipative systems with a global attractor and has no further restriction, the justified recommendation is **claimed_solved, 2/5**, explicitly labeled as an unrestricted-formulation counterexample. A queue instead tracking Eden’s historical Lorenz question or a strange-attractor/typical-system refinement must retain **unsolved** for that separate target. The title and publication summary must preserve this distinction.

## 1. Source and definition audit

The complete pinned record and its prior imported report were read. The record asks whether, for a smooth dissipative dynamical system with a global attractor, the supremum of local Lyapunov dimension is attained at an equilibrium or an unstable periodic orbit. Neither chaos, transitivity, genericity nor a particular Lorenz vector field is among its hypotheses. The imported report is source triage, not a verified theorem or a historical-scope certificate.

Three primary sources were checked against the frozen local copies, including visual inspection of the decisive formulas:

- **Eden (1989), printed pp. 408–409 and 411.** Equation (3.4) uses an index inherited from the global exponent sums. Questions 1–2 concern critical trajectories in that framework; Question 3 is explicitly posed in the Lorenz-system application. Its parameters and equilibrium appear immediately above the question. The supplied product system does not answer that particular Lorenz question. The thesis was not recovered, so this review makes no claim about its exact original quantifiers. [Primary article](https://www.numdam.org/article/M2AN_1989__23_3_405_0.pdf)
- **Parker–Goluskin, arXiv:2510.14870v2, pp. 5–7.** Definitions 2.1–2.2 use growth rates of tangent vectors and exterior products, with the initial-direction supremum outside the time limsup. Definition 2.3 chooses the smallest global index with a negative next partial-sum supremum. The discussion after equation (18) explicitly describes an equilibrium-or-periodic-orbit maximizer assertion for the global attractor. This later primary text supports the broad formulation being tested. It is a 2026 preprint version; it is not evidence that the same unrestricted wording was Eden’s original conjecture. [Versioned primary source](https://arxiv.org/abs/2510.14870v2)
- **Kuznetsov–Mokaev (2018), Section II.** The discussion describes the stationary-point/unstable-periodic-orbit question on a strange attractor, and then a separate typical-system refinement for self-excited attractors. Equations (5)–(6) and the following displayed formula use finite-time singular-value dimensions followed by an infimum over time of a spatial supremum. Those qualifications and that order of operations must be retained. [Primary preprint](https://arxiv.org/abs/1807.00235)

The candidate correctly distinguishes pointwise Kaplan–Yorke indices from the fixed-global-index expression. Neither a source’s phrase “local Lyapunov dimension” nor its name “Eden conjecture” can be used to collapse these distinctions.

## 2. Analytic vector field, completeness and volume contraction

Write
\[
 F(s)=-\frac{(s-1)(s-4)}{1+s^2},\qquad
 g(r)=rF(r^2).
\]
All denominators are strictly positive for real coordinates, so the five-dimensional vector field is real analytic everywhere. For \(s\ge0\), the following exact identities certify the claimed bounds without numerical sampling:
\[
 F(s)+4=\frac{3s^2+5s}{1+s^2}\ge0,
\qquad
 \frac32-F(s)=\frac{\frac52(s-1)^2+3}{1+s^2}>0.
\]
Thus \(|g(r)|\le4r\). The angular speeds are constant and the remaining equation is \(\dot w=-100w\); these give at most exponential growth in either time direction. Local existence therefore extends to all real times. There is no finite-time escape hidden outside the attractor.

A Cartesian calculation gives the oscillator divergence \(2F(s)+2sF'(s)\). Independently clearing the denominator yields
\[
 8-2sF'(s)
 =\frac{5\bigl((s-1)^2+s^2+s^4\bigr)+3(s^2-1)^2+10s^3}{(1+s^2)^2}\ge0.
\]
Each oscillator divergence is at most \(3+8=11\); including \(w\) gives total divergence at most \(-78\) everywhere. This is a genuine uniformly volume-contracting complete flow, in addition to possessing a compact global attractor.

## 3. Global attractor and exhaustive recurrent-orbit classification

The only nonnegative zeros of \(g\) are \(0,1,2\). Its signs on \((0,1),(1,2),(2,\infty)\) are respectively negative, positive and negative. Scalar uniqueness prevents a trajectory from crossing any of those equilibria.

The closed radius-two disk is invariant for both positive and negative times: all complete radial trajectories starting in \([0,2]\) remain there. Hence
\[
 \mathcal A=\overline{\mathbb D}_2\times\overline{\mathbb D}_2\times\{0\}
\]
is compact and invariant under the whole flow. For every bounded set of initial conditions, the excess of either radius above two is uniformly bounded by the excess of the solution from the largest initial radius. That scalar solution decreases to two when it starts above two. The \(w\) coordinate decays uniformly on bounded sets. Consequently \(\mathcal A\) attracts every bounded set uniformly, not only individual points.

Minimality follows from full invariance: a closed set attracting the bounded set \(\mathcal A\) must contain \(\mathcal A\), because the image of \(\mathcal A\) at every time is still \(\mathcal A\). This verifies the standard global-attractor convention. The attractor is not chosen by adding an irrelevant invariant torus to a smaller global attractor.

At an equilibrium both complex coordinates vanish, since each nonzero coordinate has a nonzero angular speed; also \(w=0\). Thus the origin is the sole equilibrium. A periodic trajectory must have constant radius in each oscillator and \(w=0\). Each active radius is one or two. If both coordinates are active, a common period would make \(\sqrt2\) rational. The usual parity/infinite-descent argument excludes that possibility. Therefore exactly four periodic circles exist: one active oscillator, at radius one or two, with the other oscillator zero. The radius-one circles are unstable; the radius-two circles are stable. There are no additional periodic combinations on connecting trajectories or outside the listed invariant sets.

## 4. Independent singular-value and limit calculation

For one oscillator at \(v=(x,y)\), with \(s=x^2+y^2\), its Cartesian Jacobian is
\[
 DF_\omega(v)=F(s)I+2F'(s)vv^{\mathsf T}+\omega J,
\qquad J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]
Passing to the rotating orthonormal radial/angular frame cancels \(\omega J\) exactly and leaves the diagonal variational coefficients
\[
 g'(r)=F(r^2)+2r^2F'(r^2),\qquad F(r^2).
\]
The initial frame is fixed once the initial point is fixed. Output-frame rotations are orthogonal, so they do not change singular values or exterior norms. In particular this is not an eigenvalue approximation to a nonnormal variational system.

For a nonzero initial radius the logarithmic singular values are therefore
\[
 \int_0^t g'(r(s))\,ds,
 \qquad
 \int_0^t F(r(s)^2)\,ds=\log\frac{r(t)}{r(0)}.
\]
This independently verifies the author’s formula (4). The limiting exponents follow directly from convergence of the radius and Cesàro averages of continuous functions; no appeal to an unverified multidimensional linearization is needed:

- At radius zero, or at a radius in \((0,1)\) tending to zero: \((-4,-4)\)
- At radius one: \((3,0)\)
- At a radius in \((1,2]\) tending to or equal to two: \((0,-24/17)\)

The zero-radius case is checked separately by its exact derivative \(e^{-4t}\) times a rotation. These cases cover every point of \(\mathcal A\). The extra coordinate always contributes \(-100\). Each individual limit exists, so ordering the finitely many limiting values gives the limiting singular-value spectrum.

For the exterior-product convention, choosing an initial coordinate blade in the initial orthonormal frames realizes the sum of any selected rates. Every other initial exterior vector is a finite sum of such blades, so its exponential growth rate is at most the largest corresponding sum. Thus the initial-direction supremum **outside** the time limit in Parker–Goluskin’s definition equals the computed leading partial sum. No impermissible exchange of limits and suprema is used.

## 5. Both dimension conventions and strict orbit comparison

The independent checker recomputes leading sums by maximizing over all subsets of the five rates, rather than copying the author’s sorting calculation. The six unordered types give:

| Types | Spectrum | Pointwise Kaplan–Yorke dimension | Fixed-index \(D_4\) |
|---|---|---:|---:|
| OO | \(-4,-4,-4,-4,-100\) | \(0\) | \(96/25\) |
| OU | \(3,0,-4,-4,-100\) | \(11/4\) | \(79/20\) |
| OS | \(0,-24/17,-4,-4,-100\) | \(1\) | \(332/85\) |
| UU | \(3,3,0,0,-100\) | \(203/50\) | \(203/50\) |
| US | \(3,0,0,-24/17,-100\) | \(6827/1700\) | \(6827/1700\) |
| SS | \(0,0,-24/17,-24/17,-100\) | \(2\) | \(1688/425\) |

The supremal leading sums are \((3,6,6,6,-94)\), making the fixed global index exactly four. The fifth exponent is \(-100\) at every point, and the fixed expression is consequently \(4+M_4/100\). The values at stable trajectories can be larger than their pointwise Kaplan–Yorke values; this is precisely why the two columns must not be conflated.

Both columns have their unique maximal **type** UU, realized exactly by the invariant torus \(|z_1|=|z_2|=1,w=0\). Every orbit on that torus is aperiodic. The only equilibrium has type OO, and the only unstable periodic orbits have type OU. Even allowing the stable periodic orbits, type OS, does not change the strict comparison. This completely refutes the literal unrestricted maximizer assertion under either specified convention.

At the torus and every equilibrium or periodic orbit, the orthogonal-frame singular values are exact exponentials for every \(t>0\). Thus the same strict pointwise comparisons hold for every positive finite time. The candidate correctly infers only a lower bound \(\inf_{t>0}\sup_{x\in\mathcal A}d_{KY}(t,x)\ge203/50\). It does not claim to have computed that entire finite-time infimum, or to have exchanged it with a pointwise asymptotic limit. The constant-in-time values at the equilibrium/periodic candidates are strictly smaller, so this qualification does not weaken the asserted obstruction.

## 6. Checks, limits of verification and publication scope

The 10,024 author assertions reproduced byte for byte from an isolated copy. The frozen verifier and receipt hashes are respectively `149a4c470db2a2ae3538e53edab83ef7137bba4a1d35ba37db31407fd4e77acf` and `1b4c23f30cdf29f0f3b13255c69ef3d0cd38ab2892fb42861bb45f7906ed1880`.

The independent standard-library checker passes **4,529** exact assertions. It verifies polynomial identities supplying global bounds, 651 Cartesian-to-rotating-frame calculations, all nine ordered spectrum combinations using exterior subset sums, all dimension comparisons, and finite rational controls for the radial signs. The finite integer checks for incommensurability are supplemental; irrationality of \(\sqrt2\), global attraction, completeness and all asymptotic limits are established analytically above. Numerical agreement alone is not the basis of this verdict.

Reproduction from this review directory:

```sh
(cd author_replay && python verify.py)
python independent_checks.py
```

No mandatory correction remains. The existing source qualification must remain prominent: this is a complete elementary counterexample to the **unrestricted record/later broad formulation**, with no chaotic, generic, Lorenz-specific, original-thesis or novelty claim. The mathematical argument is independently AI-reviewed and remains unrefereed.
