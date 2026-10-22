# Independent full Gaussian argument and deliberate attacks

The exact accepted claim is almost-sure existence of a transcendental entire
F(z)=sum ξ_k z^k/sqrt(k!), with independent circular complex Gaussian ξ_k of
density exp(−|w|²)/pi, such that every nonempty open U contains a zero of F^(n)
for all sufficiently large n. The threshold depends on U. There is one common
probability-one set of samples. It is not a statement about a new random sample
for each n or U. I read the complete current14241-byte proof, not only the
historical10609-byte input referenced in its audit metadata.

Entire samples and marginals
---------------------------

P(|ξ_k|>k)=exp(−k²) is summable. The resulting one coefficient-tail event makes
sum k R^k/sqrt(k!) converge for every finite R deterministically. Thus no
uncountable intersection over R is required. The countable intersection ξ_k≠0
also has probability1; all derivatives remain nonzero entire functions and the
sample is transcendental. Defining every sample and derivative as exp(z) on the
common null complement preserves the derivative relationship, joint measurability
and all one-point laws. It does not insert a positive-probability exceptional case.

The j-th coefficient of F^(n) is ξ_(n+j)sqrt((n+j)!)/j!. At a fixed z its variance
sum_(j≥0)(n+j)!|z|^(2j)/(j!)² is finite by the ratio test and at least n!>0.
The partial sums converge in L² to a circular Gaussian. Its limit agrees almost
surely at this point with the analytic series, so the constructed jointly
measurable field has exactly the required one-point distribution. Spatial and
derivative-order independence do not follow and are never needed.

Covariance and the annular asymptotic
-----------------------------------

For x=r², the coefficient of x^j in n!exp(x)sum_(k=0)^n binom(n,k)x^k/k! is

  n!/j! sum_k binom(n,k)binom(j,k)
  = n!/j! binom(n+j,j) = (n+j)!/(j!)².

This universal Vandermonde identity verifies the kernel and its factorial, with
no symbolic black box. Nine exact rational boundary/interior coefficient cases
and two wrong-normalization controls supplement it in exact_counterchecks.py.
They are diagnostics only, not an infinite theorem test suite.

Fix0<a<b and n large enough that a sqrt(n)≥1 and b sqrt(n)≤n/2. Put x=r sqrt(n),
k=floor(x). The Laguerre sum is at most sum_j x^(2j)/(j!)²≤exp(2x). Its k-th term
is at least x^(2k)/(k!)² times exp(−k(k−1)/n), because each product factor
log(1−h/n)≥−2h/n for h/n≤1/2. The elementary integral estimate
log(k!)≤k log k−k+1+log k then gives

  2r sqrt(n)−4−2log(b sqrt(n))−b²
  ≤ log L_n(−r²) ≤ 2r sqrt(n).

The endpoints k=1 and integer x cause no division or sign failure. The estimate
is uniform on this fixed annulus, but is not asserted at0 or for n-dependent
unbounded radii. Adding r² to pass to log K_n leaves an explicit value error of
size≤b²+4+2log(b sqrt(n)). A derivative of that error is not bounded or used.

Zero statistic and correct expectation
--------------------------------------

For0≤φ∈C_c^infinity(D), φ nonzero, with D disjoint from0 in its closure, set
X_n=sum m_z φ(z), L=integral|Δφ|dA, A=integral φ/|z|dA. Analytic local
factorization shows log|F_n| is locally integrable and Δlog|F_n|=2pi times its
zero measure. Hence X_n=(1/(2pi))integral Δφ log|F_n|. L is strictly positive:
otherwise integration by parts would force the compactly supported harmonic φ
to vanish. A is strictly positive by φ's nonnegativity, nontriviality and support.

Z_n=F_n/sqrt(K_n) is not analytic. Only its one-point standard complex Gaussian
law is used. The radial density2r exp(−r²) makes E|log|Z|| finite. Joint
measurability and weighted Tonelli therefore justify absolute integrability in
probability×area and Fubini. Since integral Δφ=0, the constant Elog|Z| drops out:

  μ_n = E X_n = (1/(4pi))integral Δφ log K_n
      = A sqrt(n)/(2pi) + O_φ(log n).

The factor1/4pi includes the1/2 from log standard deviation. Integration by parts
uses Δ|z|=1/|z| near the compact support. No distributional error derivative or
boundary contribution is hidden. Eventually μ_n≥A sqrt(n)/(4pi)>0.

Deviation, holes and quantifiers
--------------------------------

The exact centered difference is (1/(2pi))integral Δφ log|Z_n|. The apparently
missing centering constant is annihilated by integral Δφ=0. With deterministic
probability measure dw=|Δφ|dA/L, the triangle inequality and Jensen give

  E exp((2pi/L)|X_n−μ_n|)
    ≤ integral E exp(|log|Z_n(z)||) dw(z)
    ≤ E(|Z|+|Z|^(−1)) = 3sqrt(pi)/2 <3.

The inverse-radius moment exists for a circular complex Gaussian: integrating
against2r dr cancels r^(−1) near0. The analogous real-Gaussian assertion would
fail and cannot be silently substituted. Truncation and Tonelli handle unbounded
Jensen. Each analytic sample's zero set has area0; assigning logarithms arbitrary
finite values there does not change these integrals. This argument uses no
independence of spatial values or of the functions F_n.

Markov now gives P(|X_n−μ_n|≥λ)≤3exp(−2pi λ/L), uniformly in n. A hole in D
forces X_n=0, hence its probability is eventually≤3exp(−A sqrt(n)/(2L)). This is
summable by grouping m²≤n<(m+1)². A zero outside supp φ is irrelevant: only the
implication hole⇒X_n=0 is used, not its false converse.

For measurability, compact subdisks exhaust D. Their minimum modulus is the
infimum over a countable dense subset, and has value0 exactly when a zero lies
in that compact subdisk. This makes holes measurable. First Borel–Cantelli needs
no independence. Apply it to a countable family of rational disks with closure
avoiding0. This is a pi-base: every nonempty open set contains one, even if that
open set contains0. It is not a neighborhood base at0. Countably many full-measure
events, intersected with the entire/transcendental sample event, give one common
full-measure event. Thresholds are allowed to depend on the chosen disk.

Finally the cofinite hitting property is deterministically equivalent to dense
union of zero sets along every infinite increasing derivative subsequence. If
infinitely many orders miss one U, enumerate precisely those orders to obtain a
counter-subsequence. The reverse direction follows from unboundedness of every
increasing integer subsequence. No uncountable probabilistic intersection occurs.

Specific unsuccessful attacks
----------------------------

- A nonzero polynomial answers the literal nonzero-entire statement through
  identically zero high derivatives. This does not witness the stronger claim;
  the Gaussian event has every coefficient nonzero and no zero derivative.
- The sample generally has no derivative zero exactly at0: F^(n)(0)=ξ_n sqrt(n!)
  is nonzero almost surely for all n. Dense/eventual open-set hitting does not
  require hitting the singleton0, so this is consistent rather than a gap.
- Pointwise O(log n) errors cannot safely be differentiated. The proof instead
  tests them against Δφ with total variation L; the error is bounded by L C_n/4pi.
- An upper-tail estimate alone would not control holes. The proof derives an
  absolute centered deviation, with both signs, using the exact Gaussian moments.
- Merely obtaining dense zeros for a chosen subsequence would not answer the
  every-subsequence problem. The final deterministic equivalence and cofinite
  threshold close that quantifier, without assuming derivative independence.
- An uncountable intersection over all U could fail. The countable pi-base and
  deterministic containment implication avoid it.

Verdict: the full Gaussian theorem is correct, with no substantive repair needed.
This analytic verdict does not authenticate a historical citation, Lean theorem,
the Boas–Reddy discussion, a selected deterministic sample or a bounded-coefficient
Gaussian law. Those are separately adjudicated in the priority/source report.
