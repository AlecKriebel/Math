# Root mathematical audit: PR41 / AMR-096-0035

The byte-frozen PROOF.md (SHA256
464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c)
has a valid unconditional interior law and full-length lower bound. Its full
expected-length law is valid under its explicit additional fourth-order tail
condition. The indexed unconditional problem remains UNSOLVED. This is a
qualified partial result, with no full-solution, novelty, exhaustive priority,
external human peer review, or completed acceptance claim.

## Literal problem and assumptions

Aldous's directly acquired 2012 manuscript, Open Problem35, asks for the full
expected geometric length of the union of every prescribed pairwise route
between k independent uniform points in a square of area k. The expected
length should be asymptotic to ell*k. It explicitly identifies distant
excursions as the difficulty. Published2014 Open Problem9 instead asks which
additional assumptions, if any, suffice. The preserved prior's Steiner-minimum
interpretation and published problem-number/year identification are wrong;
current SOURCE_AUDIT already corrects them without altering imported records.

The applicable full SIRSN setup includes compatible, measurable, finite simple
routes, consistent finite-dimensional laws, translation/rotation/exact Euclidean
scale invariance, independent Poisson sampling, finite expected unit-distance
route length Delta, finite sampled-network intensity ell, and finite limiting
major-road intensity p(1). The latter is unavailable for a merely weak SIRSN.
Length counts overlaps once. Ell and p(1) are distinct constants. Standard
random-measure and sampling constructions are assumptions of this setup; no
uncountable global route union or ergodicity assertion is added.

## Interior and de-Poissonization, independently reconstructed

Write Q_n for the centered side-n square and T_(lambda,n) for the union of
routes between its Poisson sample points. It is a subset of S(lambda), whose
mean length measure is ell*sqrt(lambda) times planar area. For a fixed unit
tile C, the spans generated in increasing endpoint windows exhaust S(lambda)
on C: each countable pair eventually occurs. Continuity from below of the
geometric length measure and monotone convergence give a_lambda(r) increasing
to ell*sqrt(lambda). For fixed r, n^2+O_r(n) integer-centered tiles have their
translated endpoint windows inside Q_n. Their expected local contributions
bound the interior length below; the entire S(lambda) bounds it above.
Deterministic tile boundaries have zero expected length by the area intensity.
Take n to infinity first, then r. No route confinement, mixing, or ergodicity
is needed. Ell is positive: otherwise a countable square cover would make the
entire sampled network length zero, contradicting a route between distinct
Poisson points.

For independent uniform endpoints, adding points preserves routes and makes
F_m(n) monotone. Conditional on endpoints, each pair length has law cD with
c at most sqrt(2)n; hence E F_m <= sqrt(2)n Delta binom(m,2). Independent
auxiliary Poisson counts with means (1+epsilon)k and (1-epsilon)k give the
upper and lower sandwiches. Independence of the upper count and F_k supplies
the factor P(N_+>=k); a geometry-dependent count would not. The lower excess
uses exactly E[N(N-1)1_(N>k)] = mu^2 P(Pois(mu)>k-2). For fixed epsilon,
the Chernoff rate epsilon+log(1-epsilon) is negative; its exponential beats
the polynomial prefactor and the two-unit shift. First k grows, then epsilon
decreases. Thus E interior length/k tends to ell, and full length has liminf
at least ell.

## Exterior and the extra hypothesis

The first width-one strip has expected length at most
ell*sqrt(lambda)(4n+4). In Q_n^(2r) minus Q_n^r, each route point is farther
than r from both endpoints, so it lies in the major-road network. Its area
4nr+12r^2 and intensity bound p(1)/r give p(1)(4n+12r). Summing dyadically
only through R gives the valid upper bound

    ell*sqrt(lambda)(4n+4) + 4p(1)n(1+log2 R) + 24p(1)R.

The annuli are truncated; an infinite sum of these upper bounds diverges.
Removing closed endpoint discs versus writing distance >=r causes no gap:
the operative annuli are strictly farther than r, and feasible countable
straight-segment routes have zero length on endpoint circles.

A route visiting beyond Q_n^R has total length at least2R, by its two
endpoint-to-visited-point subpaths. Its exterior contribution is at most
L*1_(L>=2R). With h(t)=E[D*1_(D>=t)], monotonicity in endpoint distance gives
the uniform pair bound sqrt(2)n h(sqrt(2)R/n). Expected unordered Poisson
pair count is lambda^2 n^4/2, so the far contribution is at most
lambda^2 n^5 h(sqrt(2)R/n)/sqrt(2). No independence between different routes
or disjointness is assumed; union subadditivity suffices.

The additional t^4 P(D>t)->0 implies h(t)=o(t^-3) by layer cake; use a strict
cutoff at t/2 to cover atoms at t. Finite fourth moment is sufficient, and is
not claimed necessary. For each fixed delta>0 put R=delta n^2. Dividing by
n^2, the far term tends to zero and the near limsup is at most24p(1)delta.
Only after n tends to infinity does delta decrease to zero. There is no
uniformity assertion for delta depending on n. The full Poisson law follows;
the upper de-Poissonization sandwich and unconditional interior lower bound
then give the full binomial law under the same extra hypothesis.

Pareto tails and escaping random measures diagnose insufficient generic
inference rules, rather than construct admissible SIRSN counterexamples. A
fourth-order big-O tail is insufficient for this proof. The remaining gap is
o(k) expected total exterior union length under the ordinary axioms, through
a derived tail rate or a materially different bound. Replacing this gap by
the additional hypothesis does not resolve the indexed problem.

## Imported model statements and source qualifications

Root directly read the published definitions2.1-2.3, operative major-road
scaling6.1-6.2, both original problem passages, the binary-hierarchy stretch
proof through Lemmas3.2-3.4/Proposition3.1, its continuum-limit use, and final
Euclidean-stretch verification. The latter gives bounded D in that existing
model. Its full continuum construction remains a credited external theorem;
this audit does not recursively recertify every foundational construction.

Root directly read Kahn's complete Theorem3.1 proof, Theorem5.1 proof and
Remark5.1, and Theorem6.1 proof/Theorem6.2 construction statement. Several
literal source formulas need qualification. Theorem5.1's conditional
probabilities in (18)/(21)/(22) must instead be joint events with T<=T_n;
after the unconditional annular Poisson bound, add P(T>T_n). Its radius r_0
must depend on T_n, supplying the polynomial (n+1) factor. A floor gives an
upper envelope, and a correctly shifted moment sum includes its initial
finite term. The unchanged moment range q<gamma-1 survives.

For the empty forbidden set, Theorem3.1's required time tail can be verified
without copying its reversed cap-measure inequalities or reciprocal constant
presentation: connecting child balls have measure at least c_alpha a_j^(d-1).
Choose v_j=[c_alpha a_j^(d-1)/(K(j+1)+u)]^(1/(gamma-1)), K exceeding the net
growth logarithm. A union bound is C exp(-u), while the recursive path-time
series has geometric ratio 2 alpha^(-(gamma-d)/(gamma-1))<1 and is bounded
by C' u^(1/(gamma-1)). Choose alpha>2^((gamma-1)/(gamma-d))>2, so the path
also has finite Euclidean length and limiting endpoints. This supplies the
needed tail under the credited minimal-time/existence framework.

For 0<kappa<gamma-1, the joint fast-line bound uses
p_n(r_0)=2^(gamma-1)c r_0^(d-gamma) T_n^(gamma-1). Choose p_n constant
2^(gamma-1-kappa)-1 and m=floor((n+1)/kappa); then
P(L>C2^((n+1)/kappa)(n+1)^(1/(gamma-d)))<=2^-n. The moment series has
ratio2^(q/kappa-1)<1 for q<kappa. Thus gamma>5 supplies a fourth moment
in the planar model, while gamma=5 is not covered by this claim. Remark5.1's
stronger exponent remains conjectural. Theorem6.1 bounds slow length by
speed times time, correcting its printed quotient. Its finite fast-line
count and compatible-geodesic pigeonhole argument yield the claimed finite
major-road mean. Geodesic existence and uniqueness are explicitly credited
external inputs. The ancillary model citation is independent of the main
conditional theorem. Bind the adjacent SOURCE_PROOF_QUALIFICATIONS note in
current discussion; preserve the old source/review bytes as archives.

Root read the abstract and main nonpausing-geodesic statement in the exact
Blanc-Curien-Kahn arXiv v1, and current primary metadata/author index. This
supports a bounded contextual observation, not whole-paper certification or
an exhaustive no-resolution/priority claim. The publisher DOI was unavailable
through the web tool; the exact acquired preprint/version is the verified
operative reference. No outside person was contacted.

## Actual reproduction and remaining gates

Root read both complete original checker sources before executing unchanged
copies privately. All211 author and3809 old independent checks passed with
complete saved/actual result objects equal. Root also actually executed the
fully read independent original-data auditor: all16 files/Git modes and
complete17-path diff, raw corpus and all15458 SQLite joined rows, whole
present nonempty prior, and native absence were checked. SQL was genuinely
mode=ro&immutable=1 with query_only verified. All real sources, PID/argv/cwd,
clocks, complete streams, exits, private inputs/results and whole-object
comparisons are in root_original_actual_reproduction (130 members plus self,
manifest d8fb8a576676a690f9cb365f426bf3f344780bc1d03fbdc02f8534a44f3487f7).
Main and all13 native inputs were unchanged. Finite checks supplement the
analytic proof and do not certify infinite-dimensional conclusions.

Root exposure was after raw triage/candidate context; independence is supplied
by the separately sealed source-first primary and network-measure families.
The current packet, its fresh independent whole review, final actual evidence
reconciliation, merge and one present acceptance remain future gates. Original
two substantive attempts of five remain unchanged; new research/audit turns0.
Current runtime/model/deadline fields must remain null. Workflow audit is about
65% complete; full unconditional discovery estimate0%. No paper, new DOI,
tracker row, release, or human peer-review assertion is warranted.
