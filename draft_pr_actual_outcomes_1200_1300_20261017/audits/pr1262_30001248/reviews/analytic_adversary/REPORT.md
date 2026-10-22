# Independent adversarial mathematical review of PR1262

Reviewed target: problem 30001248 / OWR-3473-009, original PR head
`fb7b750865f3e220590f128661c487c5984bae75`. This is a fresh review of all
eight supplied records. No other new derivation or priority family's output
was inspected before these conclusions. The candidate and the historical
reports it retains were available, so this is an adversarial verification,
not a claim of a blind discovery.

**Verdict: PASS, with the published quantitative local limit theorem explicitly
imported.** I found no blocking mathematical defect in the sharp fixed-p
triangle modular equivalence, the density-to-cell comparison, or the elementary
reconstruction of the credited ordinary 2K2 obstruction. The deep local limit
theorem is not reconstructed by this review. Finite exact checks below support
specific combinatorial identities; they do not certify an asymptotic theorem.

This review is AI-assisted and unrefereed. It provides no external human peer
review, formal proof-assistant verification, worldwide novelty certificate, or
permission to regard a bounded literature inspection as exhaustive priority.

## 1. Integrity and scope

At the start, `authenticate_inputs.py` verified the byte count and SHA-256 of
each of the eight files against `SUBMITTED_SNAPSHOT.json`, compared each file
to its original head's Git blob, recomputed its Git blob identity, checked all
seven non-self entries of the supplied `MANIFEST.json`, and checked the
captured original branch/head/body. The original body hash is
`3ab8f23a031f563bb7b5367792af9b723b1d637ada5cc78d44c717197be51d3c`.
The same checks are repeated at the end. The captured original PR body is
checked; this is not a fresh live GitHub-state assertion. The local checkout
remained `main`; no Git object, index, branch, ref, or service state was changed.

I read the complete PROOF.md, AUDIT.md, ACCEPTANCE.md, ACCEPTANCE.json,
README.md, MANIFEST.json, SOURCES.json and VERIFICATION.json. In particular,
the previously lost supporting packages are not silently treated as recovered
or run. The three older report identities and their recovery assertions remain
historical statements made by the submitted edition. I did not possess the
old external packages, reconstruct their seals, or execute absent old code.
The new input authentication establishes the identity of this edition.

The mathematical target is fixed 0<p<1, ordinary unlabeled triangles counted
once in the labeled-vertex independent-edge graph G(n,p), and the relative
metric Delta(q)=max_a |q P(T=a mod q)-1|. For every positive integer sequence,
Delta(q_n) tends to zero exactly when q_n=o(n^2). This is an asymptotic result;
the nondegenerate triangle normalization is valid for every n>=3. No sparse
p(n), endpoint limit, labeled-embedding convention, unrestricted induced-count
theorem, or disconnected-count classification is included.

## 2. Matching the actual historical question and the imported theorem

I freshly retrieved all five PDFs named in the submitted source ledger. Their
byte counts and SHA-256 hashes match the historical pins exactly. This is a
fresh retrieval and reading, distinct from accepting an old inspection claim.
Raw PDFs, extractions and page renders are confined to ignored scratch;
`SOURCE_RETRIEVALS.json` and `SOURCE_INSPECTION.json` describe exactly what was
read, rather than making full-document proof-audit claims.

Scott's contribution, joint with Tateno, on printed pp.1279–1280 / PDF pp.55–56
of [OWR 23/2009](https://ems.press/content/serial-article-files/46223?nt=1)
has precisely the fixed-p triangle setting. Both pages were read in full and
visually inspected. The stated modular theorem uses all integer moduli in the
smaller n^2/log n range and the relative residue error. The same contribution
states a triangle local limit theorem using centered Gaussian cell masses,
notes the standard-deviation-scale obstruction, and ends with the separate
general-subgraph conjecture. It provides a proof description rather than a
complete technical proof. The current target therefore matches the triangle
range question, and the general conjecture is not substituted for it.

The actual [Sah–Sawhney v1 PDF](https://arxiv.org/pdf/2006.11369v1) states
Theorem 1.1 on p.3, with true standard deviation, the full integer lattice and
a uniform normalized pointwise error O(n^(-1/2+epsilon)). Its independent-model
proof in Section 5, pp.28–31, sums once over subgraphs isomorphic to H, gives
the exact mean and standard-deviation conventions, and concludes with that
same pointwise scale. I read the full Section 5 and the relevant interfaces
listed in the receipt, and visually inspected p.3. For H=K3 the variable is
exactly T, rather than 6T or a homomorphism count. For any fixed p in (0,1),
lambda=min(p,1-p)/2 is admissible. With epsilon=1/4, the premise is

    sup_k |P(T=k)-sigma^(-1) phi((k-mu)/sigma)|
       <= C_p n^(-1/4)/sigma.

The constant is independent of k and q. The quantitative rate, rather than
just o(1) after normalization, is essential to the chosen growing window.
The source's short connected-H statement omits the one-vertex degeneracy;
this creates no ambiguity for K3. The actual 2024 restatement explicitly
requires at least two vertices. The arXiv landing page links the related
journal DOI [10.1112/jlms.12523](https://doi.org/10.1112/jlms.12523).
I did not obtain a journal PDF through that DOI, and do not claim to have
independently compared the final journal proof with v1.

The Fourier/decoupling estimates in the deep source theorem are named standard
imports. Reading its theorem and transfer interface is not a reconstruction
of every technical lemma in that paper. No defect was found at the interfaces
needed for this specialization.

## 3. Exact variance, span, and an independent central limit argument

Let Y_e=I_e-p and v=p(1-p). Products indexed by distinct edge sets are
orthogonal: an edge in their symmetric difference contributes a centered
factor occurring only once. The coefficient of Y_e in T is p^2(n-2), that of
an unordered adjacent pair is p, and that of the three edges of a triangle is
1. There are N=binom(n,2) edges, 3 binom(n,3)=N(n-2) unordered wedges, and
binom(n,3) triangles. Hence

    Var(T) = N(n-2)^2 p^5(1-p)
             +3 binom(n,3) p^4(1-p)^2
             +binom(n,3) p^3(1-p)^3.

The covariance count gives the other formula independently. An unordered
pair of distinct triangles sharing one edge is specified by an edge and two
different additional vertices. There are N binom(n-2,2)=6 binom(n,4) such
pairs, each with covariance p^5-p^6, counted twice in the variance. Thus

    Var(T)=binom(n,3)p^3(1-p^3)+12 binom(n,4)p^5(1-p).

In particular the variance is asymptotic to p^5(1-p)n^4/2, and sigma has
leading coefficient sqrt(p^5(1-p)/2). A coefficient 6 in the covariance formula
or denominator 2 in the asymptotic standard deviation is false. Both errors
are distinguished by the direct count and the finite exact controls.

Let L=p^2(n-2) sum_e Y_e and R=T-mu-L. Orthogonality gives the useful exact
identity, valid for n>=3,

    Var(R)/Var(L)
      = [(1-p)/p + (1-p)^2/(3p^2)]/(n-2).

Consequently R/sigma goes to zero in L2 and Var(L)/sigma^2 goes to one.
The ordinary Bernoulli/binomial CLT for the N independent edge variables and
Slutsky prove (T-mu)/sigma => N(0,1), without using the deep local theorem.
The true variance normalization also gives E|Z_n|<=1 exactly. Empty graphs
and graphs consisting of exactly one triangle show that the support contains
0 and 1, so the maximal lattice span is 1. For p strictly between 0 and 1
both witnesses have positive probability. Labeled embeddings would give 6T;
that substitution would indeed introduce modular obstructions and is absent.

## 4. Adversarial reconstruction of growing-modulus sufficiency

The potentially dangerous step is summing a pointwise LLT error over a
growing or infinite residue progression. The candidate avoids this. Write
alpha=p^5(1-p)>0 and D=N(n-2)^2. Changing one edge changes T by at most n-2.
The Doob exposure martingale therefore has increments of conditional range
length at most n-2. Hoeffding's lemma, followed by exponential Markov and
optimization, gives

    P(|T-mu|>=u) <= 2 exp(-2u^2/D).

The exact variance lower bound sigma^2>=alpha D has the correct inequality
direction, and yields a bound by 2 exp(-2 alpha R^2) at u=R sigma. For
R^2=(16/alpha) log n this is 2n^(-32). All constants may depend on fixed p;
there is no assertion uniform as p approaches an endpoint.

For sufficiently large n, sigma>=1 and R>=4. The full Gaussian integer-grid
tail is bounded by intervals pointing toward zero on each tail:

    sum_{|k-mu|>R sigma} sigma^(-1) phi((k-mu)/sigma)
       <= 2 integral_{R-1/sigma}^infinity phi(u) du
       <= 2 exp(-(R-1)^2/2) <= 2 exp(-R^2/4).

The last expression is 2n^(-4/alpha)<=2n^(-16), since alpha<=1/4. These are
total tails, so they bound any one residue's discarded tail; multiplication
by q<=sigma=O_p(n^2) remains negligible. No infinite sum of a uniform error
bound is taken.

For 1<=q<=sigma and every residue a, the finite central interval contains at
most 2R sigma/q+1 members of a+qZ. Multiplying its LLT error by q gives
delta_n(2R+q/sigma). Both endpoints, the factor q and the tail factors are
accounted for. The candidate's full comparison bound follows.

The Gaussian grid requires uniformity over the shift determined by a and mu.
For an L1 absolutely continuous function with integrable derivative, compare
each mesh point to its following interval. Summing absolute errors gives

    |h sum_j f(b+jh) - integral f| <= h integral |f'|.

The conditions also ensure absolute summability of the point samples: the
same argument with absolute values bounds h sum |f(b+jh)| by integral |f|
plus h integral |f'|. Thus this passage does not presume convergence of a
possibly divergent series. For phi, the derivative integral is sqrt(2/pi).
Putting h=q/sigma proves the all-shift Gaussian discrepancy bound. Combining
the steps gives

    Delta_n(q) <= delta_n(2R_n+q/sigma_n)
       +2q(n^(-32)+n^(-16)) +sqrt(2/pi)q/sigma_n.

Since delta_n R_n goes to zero and q=o(sigma_n) eventually implies q<=sigma_n,
every term vanishes. This covers arbitrarily slowly subcritical moduli.
Primality, divisibility, monotonicity and pre-established support surjectivity
never enter the proof. The argument remains valid for bounded and composite
q; q=1 is exactly uniform directly.

The historical second derivation uses a smaller window, residue-grid tail
bound and Gaussian Poisson summation. Its displayed Fourier series is
absolutely convergent; the geometric upper bound follows from j^2>=j. Its
stated integrable-derivative alternative independently gives the same
conclusion. I found no inconsistency between the two window choices.

## 5. Sharp necessity, including oscillating and supercritical moduli

Suppose relative uniformity holds while q_n is not little-o of sigma_n.
Pass to a subsequence with q_n/sigma_n bounded below by a positive constant,
and then a further subsequence with sigma_n/q_n -> r in a bounded interval
of [0,infinity). On that subsequence q_n>=2 eventually. The sum of q_n-th
roots of unity vanishes, and the first modular Fourier coefficient is bounded
in modulus by Delta_n(q_n). This is where relative rather than unscaled
pointwise residue error is needed.

Centering changes only a unit-modulus phase; there is no assumption that the
mean phase converges. With t_n=2pi sigma_n/q_n and t=2pi r,

    |E exp(i t_n Z_n)-E exp(i t Z_n)|
       <= |t_n-t| E|Z_n| <= |t_n-t|.

The independent CLT therefore makes the coefficient's modulus tend to
exp(-2pi^2 r^2)>0, contradicting uniformity. The endpoint r=0 gives limit 1,
so q much larger than sigma is included. A sequence need not have a global
ratio limit: one violating subsequence already excludes convergence of Delta
to zero. This resolves the oscillating-sequence case without a monotonicity
assumption. The proof establishes a qualitative obstruction and a positive
subsequence lower limit; it does not advertise a uniform finite-n lower bound
for all q. Converting sigma=Theta_p(n^2) yields exactly the claimed threshold.

## 6. Gaussian cell convention

The original OWR theorem uses the integral of phi over the unit-count cell
around k, while the imported theorem samples its density. Taylor expansion
about the midpoint cancels the linear term, and the integral of u^2/2 over
[-1/2,1/2] is 1/24. Uniformly in k,

    |cell_mass(k)-sigma^(-1)phi((k-mu)/sigma)|
       <= ||phi''||_infinity/(24 sigma^3).

Thus the pointwise cell-mass error is O_p,epsilon(n^(-5/2+epsilon))+O_p(n^(-6)),
which is o(n^(-2)) for epsilon<1/2. This is a pointwise comparison, not an
attempt to sum that uniform bound over infinitely many cells. The latter
operation is not used in modular sufficiency. The coarser O(sigma^(-2))
comparison in the older independent report is also true and does not conflict
with the sharper midpoint estimate.

## 7. Ordinary 2K2 obstruction, independently checked

The ordinary number Y of unordered disjoint edge pairs equals binom(M,2)-W,
where M is the edge count and W is the number of unordered adjacent pairs.
Conditional on M=m, the graph is exactly uniform G(n,m). With
A=N(n-2), pi_j=(m)_j/(N)_j, and B=A(4n-10), splitting the ordered pairs of
wedges into equal, singly overlapping and edge-disjoint pairs gives

    Var(W|M=m)=A(pi_2-pi_4)+B(pi_3-pi_4)+A^2(pi_4-pi_2^2).

Each edge belongs to 2(n-2) wedges. After excluding the fixed wedge itself,
each of its two edges yields 2(n-2)-1 other wedges; no other wedge contains
both its edges. This proves the factor 4n-10 without counting an ordered
edge pair as a new ordinary copy.

For fixed j<=4 and r=m/N bounded away from 0 and 1, expanding the finite
product in 1/N uniformly gives the stated first-order coefficient. Hence
pi_3-pi_4=r^3(1-r)+O_p(1/N) and
pi_4-pi_2^2=-4r^3(1-r)/N+O_p(1/N^2). The large terms combine as

    r^3(1-r)(B-4A^2/N)=-2A r^3(1-r)=O_p(n^3).

The errors A=O(n^3), B/N=O(n^2), A^2/N^2=O(n^2) have the required sizes.
Thus the conditional variance is O_p(n^3). Fixing m=floor(pN), Chebyshev
puts at least 3/4 of the conditional mass in an interval containing at most
C_p n^(3/2)+1 integers. Pigeonhole supplies an atom Omega_p(n^(-3/2))
conditionally, even if the actual variance were smaller. The binomial point
probability at m is Omega_p(N^(-1/2))=Omega_p(n^(-1)). Multiplication proves
an unconditional atom Omega_p(n^(-5/2)).

For the unconditional variance, the coefficient of a single centered edge
is p binom(n-2,2), and each unordered disjoint centered pair has coefficient
1. Orthogonality gives

    Var(Y)=N binom(n-2,2)^2 p^3(1-p)
            +3 binom(n,4)p^2(1-p)^2=Theta_p(n^6).

The support has 0 and 1 for n>=4. Consequently the exhibited atom is larger
than the Gaussian local scale by Omega_p(sqrt(n)), excluding a uniform
Gaussian LLT even in the correct ordinary-copy and span-one convention.
This conclusion is credited to Sah–Sawhney Theorem 1.3. Their pp.31–32 proof
uses a more general graph-factor and conditional-limit argument; the present
elementary conditional-variance calculation avoids importing that additional
limit theorem for this particular example.

One nonblocking presentation note: the pi_4 denominator requires N>=4, so
these displayed conditional formulas should be read for n>=4, the range in
which the 2K2 count has positive variance. This is harmless in the stated
asymptotic supplement. A future standalone formulation should say n>=4
there, and reserve n>=3 for the triangle normalization. No finite-n theorem
for a nondegenerate 2K2 count at n=3 is claimed by the asymptotic result.

## 8. Fresh finite exact checks and their limits

`exact_checks.py` was newly authored for this review. It uses only the Python
standard library and explicit exception checks; none disappear under -O.
It independently enumerates all simple labeled-vertex graphs for n=3,4,5,6,
using integer edge masks and direct triangle/wedge/disjoint-pair incidence.
It does not execute or transcribe an absent historical checker.

The normal, -O and -OO runs produce byte-identical deterministic JSON. They
check 33,864 graphs, 34 conditional wedge-variance strata (n=4,5,6), 132
pointwise centered expansions on specified witness graphs and three rational
p values, 60 exact mean/variance/scale identities, 12 first-order finite-product
coefficients, all wedge-overlap counts and leading cancellations, actual
span-one witnesses, and the 1/24 midpoint constant. Rational p values are
1/5,1/2,4/5 for weighted moments; the hypergeometric coefficient controls use
four other/intersecting rational densities. The n=3 disjoint count is correctly
recorded as degenerate and is excluded from the pi_4 strata.

Negative controls reject covariance coefficient 6, a doubled ordinary
disjoint-pair variance, and replacing B by 4A^2/N in the exact conditional
variance. These checks expose the relevant counting errors rather than
merely checking that a script can run. They remain finite consistency tests.
The analytic expansion, uniform error estimates, CLT and imported LLT are
mathematical arguments, not inferences from these small enumerations.

## 9. Ancillary assertions and publication limits

The fresh Berkowitz PDF is the exact v3 byte sequence identified in the
submitted edition. I read pp.1–4 and 7–9 and visually inspected pp.2,7,8,9.
The identified mean, variance-versus-standard-deviation notation, leading
standard-deviation constant, exponent and mesh-step defects are present in
the specified displays. The p.7 pointwise corollary and p.8 variance formula
support the intended normalization. This is a narrow check of those displays;
it neither rejects the whole paper nor repairs and certifies every technical
lemma. The internal 2024 date and 2017 archive version stamp are both visible
in text; the landing history identifies v3 as the 2017 revision. I assign no
unverified cause and infer no new version from the internal date.

Fresh reading of the DeMarco–Kahn–Redlich journal PDF pp.1–2 confirms its
ordinary unlabeled convention, fixed q>1, nonisomorphic connected graphs with
at least two vertices, sparse threshold, and q/family dependence of constants.
It is not an input uniform in growing q. Fresh reading of the 2024 joint
paper pp.1–3 and 5 confirms the connected-count restatement, downward-closed
finite-family condition, permissible coordinates and skew normalization, and
nonlinear transform of Gaussian graph factors. These are peripheral statement
checks. Neither paper's complete proof is certified here.

The exact threshold therefore passes as credited coverage of the original
triangle question. No mathematical repair is needed for that theorem. The
retained recovery/provenance caveats and absence of first-resolution or
novelty claims must remain explicit. A separate priority audit is still needed
before any publication decision; this review did not perform an exhaustive
literature search or assess a future preprint package, publication metadata,
service code, Zenodo deposit, tracker row, or eventual merge.
