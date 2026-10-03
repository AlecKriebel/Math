# Turn 2: a geometric floor on fixed-dimensional smooth input patches

Second substantive turn. The original high-dimensional, width-dependent robustness conjecture remains unresolved. This turn extends the fixed-circle obstruction to any fixed-dimensional input law having one smooth positive-density patch. It proves the conjectured lower order in spherical dimensions d=2,3,4 for every width, and in Gaussian dimensions d=1,2,3 for the GLOBAL Lipschitz norm. These are geometric lower bounds for all functions, not a sharp neural-architecture theorem. Birthday collisions, Poissonization and coordinate charts are classical tools; no historical novelty is certified.

## 1. A positive-density chart hypothesis

Let the input distribution have a measurable patch parameterized injectively by a C-Lipschitz map Φ:[-r,r]^s→R^d, where s≥1,r>0. Assume its restriction to that patch is the pushforward of a density ρ with

    0<a≤ρ(z)≤b<infinity.

The total probability of this patch need not be one. The constants s,r,C,a,b are fixed while n grows. Inputs are iid and their labels are independent fair signs, independent of the inputs. Partition the coordinate cube into m^s=M equal subcubes. Each image cell has probability p_j satisfying

    A_0/M ≤ p_j ≤ B_0/M,
    A_0=a(2r)^s, B_0=b(2r)^s,

and diameter at most2rC sqrt(s)/m. Boundary ties have probability zero under the density and can be resolved by a half-open convention.

If any cell contains both labels, every interpolating function has Lipschitz constant at least

    m/(rC sqrt(s))                                       (1)

on a domain containing those sample points. This is just their label difference2 divided by the cell diameter; no parameter count or activation hypothesis enters.

## 2. Uniform opposite-label birthday bound

Poissonize with an independent sample count N of mean n/2, coupled to the first N terms of one infinite iid labeled sequence. Counts of positive and negative observations in different cells are independent Poisson variables. Each sign count in cell j has mean x_j=np_j/4.

When M≥B_0 n/4, every x_j≤1. The chance that cell j contains both signs is (1-exp(-x_j))². Since exp(x)≥1+x gives 1-exp(-x)≥x/(1+x)≥x/2 for0≤x≤1, this probability is at least n²p_j²/64. Independence across cells therefore gives

    P(no opposite-label cell in the Poisson sample)
      ≤exp[-n² sum_j p_j²/64]
      ≤exp[-A_0² n²/(64M)].                              (2)

The Poisson count does not assume disjoint sample pairs or independent spacings. Its independent-cell property follows directly from the joint generating function exp[(n/2)(sum p_j z_j−1)], including an outside-patch category and the sign split.

The no-collision event decreases with sample size. If it holds for the first n samples and N≤n, it also holds for the first N samples. Thus

    P(no opposite-label cell among n samples)
      ≤exp[-A_0²n²/(64M)]+P(N>n)
      ≤exp[-A_0²n²/(64M)]+exp[-(log2−1/2)n].             (3)

The last estimate is the exponential Markov bound with parameter log2: E2^N=exp(n/2). This coupling direction is important; no conditioning on N=n and no lost sqrt(n) factor are required.

## 3. An all-functions high-probability floor

Fix A>0 and define

    B=64·2^s(A+1)/A_0²,
    m=ceil[(n²/(B log n))^(1/s)].

For all sufficiently large n, depending on the fixed chart and A, the quantity being rounded is at least1 and

    n²/(B log n) ≤ M=m^s ≤2^s n²/(B log n),
    M≥B_0 n/4.

By(3), an opposite-label cell exists with probability at least

    1-n^{-(A+1)}-exp[-(log2−1/2)n].                       (4)

On that single event, every interpolating function obeys

    Lip(f) ≥ c_(chart,A) (n²/log n)^(1/s),
    c_(chart,A)=1/[rC sqrt(s) B^(1/s)].                   (5)

The constants are explicit but dimension-dependent. This is not a theorem uniform over growing dimension or arbitrary singular distributions. It also does not assert that a network of a given width attains the floor.

## 4. Exact applications to the source models

For the unit sphere S^{d-1}, d≥2, put s=d-1 and r=1/(4sqrt(s)). The chart

    Φ(z)=(z,sqrt(1-||z||²))

has ||z||≤1/4 on the cube. It is C-Lipschitz with C=2, and its surface-density factor is1/sqrt(1-||z||²), between1 and4/sqrt15. Dividing by the fixed surface area gives the needed positive finite a,b. Both points in the collision lie on the sphere, so(5) bounds exactly Lip_{S^{d-1}}(f), the source's spherical norm.

For each fixed d≤4, the exponent2/(d-1) is strictly larger than1/2. Consequently(5) is eventually larger than c sqrt(n/k) simultaneously for every integer k≥1. It proves the source lower-bound order in these fixed spherical dimensions by geometry alone. In d=5 it gives sqrt(n)/(log n)^(1/4), which implies the conjectured order only for widths k at least a constant times sqrt(log n). More generally it certifies the width region

    k ≥ C_(chart,A) n^(1-4/s)(log n)^(2/s)

with an appropriate fixed constant. This algebraic comparison is not a general sharp width law.

For normalized Gaussian inputs N(0,I_d/d), choose an ordinary fixed cube in R^d. Its density has a positive minimum and finite maximum, and the identity map is a chart with s=d. Hence(5) applies to the global Lipschitz constant, or any prediction domain containing that cube and its collision points. It gives the sqrt(n/k) order in fixed d≤3. This is deliberately NOT asserted as a sphere-restricted Lipschitz bound for Gaussian observations off the sphere; the original paper's domain convention is preserved as a separate issue.

## 5. Exact finite controls and remaining gap

For M equal-probability cells covering all inputs, an independent exact formula for no opposite-label cell after n samples is

    sum_{j=0}^M (-1)^j binom(M,j) 2^(M-j)
                    ((M-j)/(2M))^n.                     (6)

One may obtain it from the exponential generating function of the independent Poisson cells, or by inclusion-exclusion. The checker verifies it against a separate dynamic program over empty/positive/negative cell states and against the occupancy Stirling-number formula. It also checks the rational rounding and collision-exponent algebra. These controls do not replace the general density and chart proof.

The difficult regime is growing dimension with widely separated generic points, where all-functions geometric floors no longer force the conjectured width penalty. The packet still needs architecture-sensitive reasoning there. Original unresolved2/5.
