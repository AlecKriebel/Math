# Independent dynamics adversarial review: PR #615 / 4200010

Reviewed frozen canonical proof:
`submission/FULL_PROOF.md`, SHA-256
`541bc3c95d8f04b1d89cac3d2af21815ab331c7eeff9d79ff3591ba8f53eabd1`.

Review completed 2026-10-13 UTC. The assigned mathematical review is complete
(completion estimate: 100%). This is an AI-assisted independent re-derivation,
not human peer review and not a historical priority certificate.

## Verdict and strongest verified result

**No mathematical defect requiring repair was found in the frozen theorem.**
In the unrestricted smooth symplectic category, the construction supplies the
requested positive-Liouville-volume region outside the almost-periodic and
positive-exponent regions. Its almost-periodicity convention is explicitly
that the full restricted L2 Koopman representation has compact orbits.

The strongest verified conclusions are:

1. The specified compact connected symplectic four-manifold and real smooth
   autonomous Hamiltonian exist with the asserted normalization.
2. Every tangent-vector Lyapunov exponent is zero at every point of the
   claimed band. In fact, the same calculation proves every exponent zero
   everywhere on this particular manifold, including critical energy slices.
3. The band has ambient Liouville measure exactly 1/4. Every one of its energy
   components, with the actual Liouville conditional probability, is ergodic
   and carries a nonzero absolutely continuous spectral observable.
4. Every positive-volume invariant measurable subregion of the band fails
   almost periodicity. A globally smooth observable suffices to witness this;
   the candidate's measurable seam-discontinuous observable is also valid.
5. Every individual trajectory in the band fails Bohr almost periodicity.
   This separately addresses a natural orbitwise reading, although it is not
   needed for the stated L2 theorem.

There is no remaining mathematical gap for these assertions. Historical
priority, novelty, and any unstated restriction to Euclidean phase space or
natural mechanical Hamiltonians remain outside this verdict. The example is
not weakly mixing, and must not be promoted as proving the source's separate
weak-mixing guess.

## Source match and exact boundary of the verdict

The primary [2000 problem list](https://people.math.harvard.edu/~knill/seminars/intr/)
defines the regions using invariant Liouville measure and asks for positive
measure in their complement. It states no prescribed ambient manifold,
exactness, contact-type, analyticity, natural-mechanical, or genericity
restriction. The following weak-mixing sentence is labeled a guess.
The [primary two-page PDF](https://people.math.harvard.edu/~knill/seminars/bozeman/intr-l.pdf)
was also opened; its extracted text is defective, so the HTML is the directly
readable wording used here.

Knill's [2016 account, section 4](https://people.math.harvard.edu/~knill/pde/pde.pdf)
explicitly associates almost periodic invariant-measure dynamics with pure
discrete Koopman spectrum. This corroborates the declared convention but does
not retroactively formalize every intended meaning of the older question.
The [1998 spectral paper cited by the problem](https://people.math.harvard.edu/~knill/publications/knill_singularcontinuous1.pdf)
was opened for context; no theorem from it is required below.

Under the printed unrestricted question and this standard spectral convention,
the candidate addresses the full existential target, rather than just a
zero-measure energy surface or a non-almost-periodic factor. The Hamiltonian
construction is on a nonexact symplectic manifold: the symplectic area of a
torus fiber is one. The statement must retain that ambient category. No
historical first-resolution inference follows from the mathematical audit.

No source fulltext or downloaded third-party file was saved by this review.

## 1. Exact skew-shift dynamics and spectrum

Put a=sqrt(2). For F(x,y)=(x+a,y+x) on R^2/Z^2, changing a lift by (r,s)
changes its image by (r,r+s), an integer pair. Thus F is well-defined. Its
inverse is (x-a,y-x+a), and its Jacobian is [[1,0],[1,1]], preserving dx∧dy.

Direct recurrence for positive and negative n gives

    F^n(x,y) = (x+n a, y+n x+a n(n-1)/2).

The second coordinate shows why the derivative is polynomial rather than
exponential: D F^n=[[1,0],[n,1]]. The independent script checks the lift
recurrences and group law in Q(sqrt(2)), rather than substituting a rounded
rotation angle.

For the Fourier character e_(k,l), pullback is

    U e_(k,l) = exp(2πi k a) e_(k+l,l).

An invariant L2 function has Fourier coefficients of equal absolute value on
each chain (k+j l,l). When l≠0 the chain is infinite with distinct indices, so
square summability forces every coefficient on it to vanish. When l=0,
invariance requires exp(2πi k a)=1, forcing k=0. Hence F is ergodic for Haar
measure. This step uses irrationality, completeness of the Fourier basis,
finite invariant measure, and genuine full invariance; none can be inferred
from a finite numerical orbit plot.

The stronger spectral structure is also explicit. For l≠0 choose a residue r
modulo |l| and set

    v_j = exp(2πi a[j r+l j(j-1)/2]) e_(r+j l,l), j∈Z.

Then U v_j=v_(j+1). Each chain is a bilateral shift. In particular g=e_(0,1)
has orthonormal translates U^n g. This is a direct obstruction to compactness,
independent of the ergodicity argument. Nonconstant eigenfunctions e_(k,0)
coexist with these shift subspaces. A nontrivial pure-point factor cannot be
mistaken for the full system being almost periodic.

## 2. Global suspension and Hamiltonian legitimacy

The deck transformation (z,t)↦(Fz,t-1) acts freely and properly discontinuously,
because integer translates move t by integers. The quotient N is a smooth
compact connected mapping torus. It preserves both dx∧dy and dt; hence they
descend to closed forms β and τ, and β∧τ has total volume one.

The flow ψ_s[z,t]=[z,t+s] is smooth and complete. In the fundamental domain
0≤t<1, integer times satisfy ψ_n[z,t]=[F^n z,t]. This sign agrees with the
specified deck action. The resulting clock exp(2πi t) is a flow eigenfunction,
and the time-one transformation is not ergodic. The full flow can nevertheless
be ergodic; the candidate correctly uses continuous-time invariance.

On M=N×S^1_E, the global two-form ω=β+τ∧dE is closed and

    ω^2/2 = β∧τ∧dE.

It is nowhere zero and integrates to one, so it is a symplectic form with the
asserted normalized Liouville measure. Here dE denotes the global closed
one-form on the circle; E itself is not a global real function. This distinction
is essential and respected by the proof.

The step function q is smooth because exp(-1/r) extends flatly by zero at
r=0, and its defining denominator is everywhere positive. The resulting h(E)
is zero in neighborhoods of the two endpoints of the circle chart, so its
periodic extension is a genuine real smooth Hamiltonian. On I=(1/8,3/8),
h(E)=E, h'=1, and h''=0. The contraction convention gives

    X_H=h'(E)∂_t.

Thus B=N×I is invariant and μ(B)=1/4. Every N×{E} with E∈I is a regular
connected energy component: locally h is one-to-one, so that slice is both
open and closed in its energy level. Because μ=ν dE and H=E in the band, the
normalized conditional invariant measure is exactly ν=β∧τ. There is no hidden
coarea weight in this band. Any critical points or additional components at
the same energy outside the band are irrelevant to this component statement.

No Hamiltonian-isotopy assumption on F as a map of its own torus is needed.
The autonomous Hamiltonian is on M, and its time maps are isotopic to the
identity there. The nontrivial mapping-torus monodromy creates no contradiction.

## 3. Zero exponents with every tangent direction included

On the covering space consider

    V1=∂_x-t∂_y, V2=∂_y, V3=∂_t, V4=∂_E.

The deck derivative sends V1(t) to ∂_x+(1-t)∂_y=V1(t-1), and fixes the other
three frame fields. Hence this is a global smooth frame. Its minus sign is
necessary. Declaring it orthonormal defines a legitimate smooth global metric.

For any E write b=h'(E), c=h''(E). The full flow is
([z,t],E)↦([z,t+s b],E). In the global frame its derivative is

    S_s = [[1,0,0,0], [s b,1,0,0], [0,0,1,s c], [0,0,0,1]].

The second shear is the transverse energy derivative; omitting it outside the
plateau would be incorrect. On the band c=0 and b=1, yielding exactly the
candidate's formula. The independent script checks arbitrary fractional and
negative times, actual seam crossings, the inverse, and preservation of ω.

Write S_s=I+s L_E. Since L_E^2=0, S_s^{-1}=I-s L_E. The norm of L_E is
max(|b|,|c|). Smoothness and compactness give a finite uniform bound K, so

    ||S_s||, ||S_s^{-1}|| ≤ 1+K|s|.

This yields, for every nonzero vector v and every point,

    ||v||/(1+K|s|) ≤ ||DΦ_s v|| ≤ (1+K|s|)||v||.

The logarithm divided by |s| tends to zero on both sides. Thus every exponent
exists and is zero; no appeal to Oseledets' almost-everywhere assertion or to a
numerical exponent estimate is needed. All smooth metrics on compact M are
uniformly equivalent. The candidate's K=1 bound on B is therefore valid, and
the same proof independently establishes a global strengthening.

## 4. Continuous-time ergodicity and spectral falsification

If v∈L2(N,ν) is invariant under all ψ_s, then its distributional derivative in
t vanishes in every product chart away from the seam. This follows by testing
the translation-invariance equality against compactly supported smooth
functions and differentiating the test functions. A locally integrable
function with zero derivative in t is independent of t almost everywhere, so
v(z,t)=w(z) in the fundamental domain. Gluing, equivalently invariance under a
translation crossing the seam, gives w(Fz)=w(z) almost everywhere. The previous
Fourier argument makes w constant. Thus the full suspension is ergodic.

Strong continuity is justified first on continuous functions by compactness
and uniform continuity, and then on all L2 functions by density and unitarity.
Consequently invariance at all rational times already implies full invariance.
These arguments do not substitute ergodicity of the time-one map, which would
be false.

For the candidate's fundamental-domain G([x,y,t])=exp(2πi y), its correlation
has an exact continuous-time formula. For t∈[0,1) put k=floor(t+s). Then

    G(ψ_s[x,y,t]) conjugate(G([x,y,t]))
      = exp(2πi[k x+a k(k-1)/2]).

Integration in x is zero unless k=0, when it is one. The length of the set of
t∈[0,1) with floor(t+s)=0 is max(1-|s|,0). Therefore

    <G∘ψ_s,G> = max(1-|s|,0).

In the convention C(s)=∫exp(2πi λs)dσ(λ), the spectral measure is

    dσ(λ) = (sin(πλ)/(πλ))^2 dλ,

with the value at λ=0 interpreted as one. This follows by Fourier transforming
the triangle, the convolution of two interval indicators. It is a nonzero
absolutely continuous spectral measure. The exact partition computation for
505 rational times reproduces the formula, including negative time and seam
boundary cases. The analytic formula, not that finite test, proves the claim
for every real s. At distinct integer times the correlation is exactly zero.

The discontinuity of G across the measure-zero seam is harmless in L2. It is
also removable if desired: choose a nonzero smooth bump ρ with compact support
in (0,1), and define W([x,y,t])=ρ(t)exp(2πi y). All derivatives vanish near the
seam, so W is globally smooth on N. At integer times its translates have
pairwise inner products

    <W∘ψ_n,W∘ψ_m> = (∫_0^1 |ρ(t)|^2dt) δ_(n,m).

This produces the same compactness obstruction using a smooth test function.
It is an optional manuscript simplification, not a required repair.

## 5. Arbitrary measurable invariant subsets and the maximal good region

Let C⊂N×I be measurable, positive-volume, and invariant modulo null sets for
the full flow. For each rational s the indicator equality holds in L2(N×I).
Fubini and the countability of Q give a common full-measure set of energies
on which the section indicator is invariant at every rational time. Strong
continuity extends this to all real times, and suspension ergodicity forces
each section indicator to be constant almost everywhere, taking value zero or
one. The section mass is measurable. Thus

    C = N×J modulo null sets, μ(C)=Leb(J)>0,

for a measurable J⊂I. This classification is necessary: an arbitrary invariant
set cannot simply be assumed to contain whole energy surfaces pointwise.

On N×J, integer translates of either G or W remain orthogonal; their norms
are fixed and positive. After normalization they have pairwise distance sqrt(2).
Thus the restricted L2 orbit is not precompact. Neither ergodic decomposition
nor averaging different integrable frequencies is being used to manufacture
continuous spectrum: it is present on each individual energy component.

Restriction to an invariant measurable subset is a bounded intertwining map
of Koopman representations, so it preserves precompact orbits. If any global
almost-periodic region intersected B in positive measure, that intersection
would contradict the previous paragraph. Since there are no positive exponents
in B, its measure lies in the complement of both regions.

The maximal good region exists modulo null sets under this convention. Almost
periodicity passes to invariant subsets. It passes to countable disjoint unions
because any L2 vector is approximated by finitely many summands, with uniformly
small invariant tail norm. Let a be the supremum of measures of good regions,
choose a sequence whose measures tend to a, and take its countable union after
disjointification. That union is good, has measure a, and absorbs every other
good region modulo null sets. Hence no uncountable-union or nonmeasurability
loophole undermines the final complement claim.

## 6. Separate orbitwise almost-periodicity test

Fix an arbitrary point in the band and sample its trajectory at integer times.
All samples lie in the same embedded torus fiber at a fixed clock coordinate.
Evaluating the continuous scalar function exp(2πi y) on that fiber gives

    u_n=exp(2πi[y+n x+a n(n-1)/2]).

For distinct shifts p,q, the ratio u_(n+p)/u_(n+q) has phase

    (p-q)x+a[(p-q)n+(p(p-1)-q(q-1))/2].

The coefficient of n is the irrational number (p-q)a. Irrational-rotation
density therefore gives sup_n |u_(n+p)-u_(n+q)|=2. The translated scalar
sequences are pairwise separated in the uniform norm and cannot be precompact.

A Bohr almost-periodic trajectory would have precompact translates in the
uniform metric. Sampling integer times preserves precompactness. All those
samples lie in the fixed compact fiber, on which the scalar function is
uniformly continuous, so applying it also preserves precompactness. This
contradicts the separated scalar translates. Thus no trajectory in the band
is Bohr almost periodic. Uniform recurrence is a different, weaker notion and
is not excluded by this calculation; it must not be silently substituted.

## Reproduction, limits, and repairs

Run `python3 independent_reproduction.py` from any location. The program uses
only the standard library, performs 7,036 exact checks, emits the results and
SHA-256 bindings of all frozen inputs, and imports neither author nor prior
audit code. Its recorded output is `RESULTS.json`. The finite checks cover
irrational-field iterate algebra, bilateral-shift phase gauges, continuous-time
correlation cells, seam and transverse derivative matrices, and orbitwise phase
differences. Deliberate controls distinguish time-one invariance, rational
rotation, wrong frame sign, omitted energy derivative, clock factors, zero
speed, and a zero-volume single energy.

The script does not establish infinite Fourier square summability, quotient
smoothness, cutoff flatness, disintegration, strong continuity, irrational
rotation density, or asymptotic limits. The independent arguments above check
those points. Counts are coverage metadata, not proof certification.

Mandatory mathematical repairs: **none**. Optional useful additions to a
preprint are the smooth W witness and a short explanation of maximal-good-set
existence. Neither changes the theorem. Retain the explicit almost-periodicity
definition, unrestricted ambient category, and distinction between the
existential question and weak-mixing guess. Do not infer first priority from
this audit. No original artifact, Git state, PR, queue, or publication record
was changed; no outreach was performed.
