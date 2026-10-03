Historical source/review text follows as an exact archival body; its prior PASS is not a current whole-packet verdict. The appended source qualifications govern current ancillary applicability.

# Independent review of the conditional SIRSN spanning length theorem

**Verdict: PASS for the stated conditional partial result.** The in-square expected-length law and full-length lower bound follow from the standard axioms. The full asymptotic follows from those axioms plus the explicit additional condition \(t^4\mathbb P(D_1>t)\to0\). No mandatory mathematical correction was found. The unconditional dataset target remains **unsolved**; this review does not certify historical priority.

Reviewed on 30 September 2026 by a separate gpt-6-astra, xhigh reviewer. The frozen artifact is PROOF.md for 9700035, SHA-256 **f267e5fbeebea4f8e252dc9cb5cf030dcdbb7e002087656b360bbef87e9f3919**. No author file was edited.

## Source and hypotheses

The original problem is Open Problem 35 in [Aldous's 2012 manuscript](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf), printed page 50. It asks for the unconditional asymptotic and explicitly singles out distant excursions as the obstruction. In the [published 2014 paper](https://doi.org/10.1214/EJP.v19-2920), Open Problem 9 on page 38 instead asks which additional assumptions, if any, suffice. Both passages were read. The latter page was also rendered and visually checked.

The [published full text](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf), Sections 2.1–2.3, defines the span as the union of the designated routes for all sampled pairs. It is not a minimal connecting network. Those pages provide the consistent finite-dimensional route laws, measurability in the endpoints, independence of the Poisson sample from the route process, and the monotone sampled-network coupling. They also define length intensity as expected geometric length per unit area. I checked the relevant definitions and scaling equations on pages 6–9 and 28; pages 8 and 28 were rendered.

Consequently the two intensity estimates used in the proof have the correct constants and meaning:

\[
 \mathbb E\operatorname{len}(S(\lambda)\cap A)
   =\ell\sqrt{\lambda}\,|A|,
 \qquad p(\lambda,r)\le p(1)/r.
\]

The first uses equations (2.1), (2.16), and (2.21)–(2.22); the second uses monotonicity in the sampling intensity and (6.1)–(6.2). The parameters \(\ell\) and \(p(1)\) are different. Finite \(p(1)\) is a standard SIRSN hypothesis; it is not available merely from the definition of a weak SIRSN. The full conditional theorem is stated for the former and therefore has the needed assumption.

The paper removes closed endpoint disks in (2.17), while the submitted description uses distance at least \(r\). This causes no gap: its annuli exclude the inner closed square, so their points are strictly farther than \(r\) from all endpoints in the sampling square. Moreover the source's feasible routes are countable unions of straight segments, whose intersections with an endpoint circle have zero length. Either radius convention gives the same length intensity in that setting.

## Poisson exhaustion and the interior law

For fixed \(\lambda\), the finite spans within expanding squares are coupled as subsets of the same sampled network. The route consistency is essential: adding endpoints does not replace a previously prescribed route. Every route between two Poisson points appears once the expanding square contains both endpoints. Therefore the increasing union is exactly \(S(\lambda)\), with no unjustified passage to the closure of a network.

Length restricted to the unit tile is a measure on these measurable unions of route segments. Continuity from below, followed by monotone convergence for expectations, proves \(a_\lambda(r)\uparrow\ell\sqrt\lambda\). Local integrability is supplied by finite intensity; neither mixing nor ergodicity is needed.

The tiling lower bound also checks out. If the translated side-\(r\) square lies inside the side-\(n\) sampling square, all its endpoint pairs are among those defining the larger span. Each corresponding tile has the same expected locally generated length by translation invariance. There are \(n^2+O_r(n)\) admissible integer-centered tiles for fixed \(r\), even for noninteger \(n\). Boundaries have zero expected length because their area is zero and all considered networks are subsets of \(S(\lambda)\). The finite tile sum therefore does not overcount a positive expected length.

The order of limits is correct: first let \(n\) increase for fixed \(r\), and only then let \(r\) increase. The upper bound by the entire sampled network yields the matching limit. Routes are allowed to leave the square throughout this argument; only the measured part of each finite span is restricted to it.

The proof that \(\ell>0\) is also valid. If it vanished, the length of \(S(1)\) in each member of a countable covering by bounded squares would vanish almost surely. This contradicts the positive-length route between two distinct Poisson points.

## De-Poissonization

The construction with an infinite sequence of uniform endpoints is legitimate using the consistent finite route laws. Only finitely many endpoints are used in each \(F_m(n)\); it does not assert that the infinitely dense endpoint sequence defines a locally finite feasible subnetwork.

For fixed endpoints, invariance gives the law
\(\operatorname{len}R(x,y)\overset d=|x-y|D_1\). Independence of the sample and network allows its conditional use after the endpoints have been revealed. Summing over unordered pairs, without any independence assumption between routes, yields

\[
 \mathbb E F_m(n)\le \sqrt2\,n\,\Delta {m\choose2}.
\]

The same upper bound holds for full rather than in-square length.

For the upper sandwich, on \(\{N_+\ge k\}\) one has \(F_{N_+}\ge F_k\). The auxiliary count is independent of \(F_k\), so
\(\mathbb E F_{N_+}\ge\mathbb P(N_+\ge k)\mathbb EF_k\).
This proves (10); it would be invalid to use the same factorization for a count chosen from route geometry, but no such dependence is present.

For the lower sandwich, split by \(N_-\le k\) and \(N_->k\). Monotonicity bounds the first contribution by \(\mathbb EF_k\); the pair estimate bounds the second. The exact factorial shift is

\[
 \mathbb E[N(N-1)\mathbf1_{\{N>k\}}]
 =\mu^2\mathbb P(\operatorname{Pois}(\mu)>k-2).
\]

The threshold is \(k-2\), not \(k\). With \(\mu=(1-\varepsilon)k\), choose the exponential Markov parameter \(-\log(1-\varepsilon)>0\). The exponential rate is \(\varepsilon+\log(1-\varepsilon)<0\); the two-unit threshold shift contributes only a fixed factor for fixed \(\varepsilon\). The error in (11), divided by \(k=n^2\), therefore tends to zero despite its polynomial prefactor. The upper-count probability tends to one. Letting \(k\) tend to infinity and then \(\varepsilon\) decrease to zero proves the claimed binomial interior law.

## Exterior estimates

The first strip estimate follows directly from \(T_{\lambda,n}\subset S(\lambda)\) and the area \(4n+4\). For a point of the annulus \(Q_n^{2r}\setminus Q_n^r\), at least one coordinate is farther than \(r\) outside the original square. Its Euclidean distance from every endpoint in \(Q_n\) is therefore greater than \(r\). Any part of the finite span there is contained in the major-road network \(E(\lambda,r)\).

The annulus area is \(4nr+12r^2\). Multiplication by the intensity bound \(p/r\) yields \(p(4n+12r)\). This is a pointwise inclusion followed by an expectation bound; the finite span need not be stationary or independent of \(E(\lambda,r)\).

For \(J=\lfloor\log_2R\rfloor\), the strip and annuli \(r=1,2,\ldots,2^J\) cover the requested exterior up to radius \(R\), sometimes beyond it. Overcoverage is harmless for an upper bound. The inequalities \(J+1\le1+\log_2R\) and \(\sum_{j=0}^J2^j\le2R\) give (14). Annular boundaries are either allocated to the adjacent annulus or are negligible for the length estimates. Extending this bound to infinitely many annuli would diverge; the author correctly does not do so.

If a route visits a point beyond \(Q_n^R\), the two subpaths joining that point to its endpoints have total length at least \(2R\). Rectifiability and continuity of the feasible route suffice for this statement. Its exterior contribution is at most its full length times the indicator of this event. If the endpoint distance is \(c\le\sqrt2n\), then

\[
 \mathbb E[cD_1\mathbf1_{\{cD_1\ge2R\}}]
 \le \sqrt2n\,h(\sqrt2R/n).
\]

This bound is uniform over endpoint locations. A Poisson count of mean \(\lambda n^2\) has expected unordered pair count \(\lambda^2n^4/2\). Multiplication produces exactly \(\lambda^2n^5h(\sqrt2R/n)/\sqrt2\), including the exponent and constant in (15). Overlapping routes can only reduce the union length. No route independence or disjointness was inserted.

## Tail condition and the two limits

The strict-tail layer-cake identity proves
\(\mathbb E[D_1\mathbf1_{\{D_1>t\}}]=o(t^{-3})\) from \(t^4\mathbb P(D_1>t)\to0\). For the nonstrict version used in \(h\), the bound
\(h(t)\le\mathbb E[D_1\mathbf1_{\{D_1>t/2\}}]\)
handles arbitrary atoms. Finite fourth moment supplies the displayed condition by dominated convergence applied to the fourth-moment tail. It is sufficient, and is not claimed necessary.

The choice \(R=\delta n^2\) is made for each fixed \(\delta>0\), and eventually satisfies \(R\ge1\). The normalized far term is a constant times
\(n^3h(\sqrt2\delta n)\), which tends to zero for this fixed \(\delta\). The normalized near term has limsup at most \(24p\delta\), since its \(n\log R\) contribution divided by \(n^2\) vanishes. Nonnegativity permits taking the limsup in \(n\) first and then sending \(\delta\) to zero. There is no implicit uniformity in a shrinking \(\delta=\delta(n)\).

This gives the full Poisson law. Applying only the upper de-Poissonization sandwich to full length gives the binomial limsup at intensity \(1+\varepsilon\). The already proved unconditional interior lower bound supplies the opposite inequality. This last passage needs no further tail assumption or hidden lower sandwich for exterior length.

## Scope and reproduction

The scalar Pareto example correctly separates finite first moment from the required tail estimate. It does not construct a compatible random route network and therefore is not a SIRSN counterexample. The ordinary first-moment hypothesis cannot close this proof without additional geometric or tail information.

The ancillary applicability statements are consistent with the cited primary results. Aldous's Proposition 3.1 and its continuum verification provide bounded stretch in the binary-hierarchy model. The proof of Theorem 5.1 in [Kahn's paper](https://arxiv.org/abs/1503.03976) explicitly obtains route-length moments of every order less than \(\gamma-1\), so \(\gamma>5\) supplies a fourth moment. Its subsequent proposed improvement is explicitly a conjecture and was not used as a theorem. This review does not certify all proofs in the later model literature or exhaustively establish novelty.

The author's program was copied and rerun outside the author directory: all **211 assertions passed**, with byte-identical JSON output. The independent program passes **3,809 exact assertions**, including 1,800 finite-law monotonicity-sandwich cases, 45 atomic pair-tail cases, exact Poisson index shifts, tile counts, annular constants, and limit diagnostics. These are controls for algebra and probability identities, not simulated SIRSN evidence or a substitute for the measure-theoretic proof.

**Publication disposition:** suitable for a qualified draft PR with the original target marked **unsolved**. Keep the additional tail hypothesis prominent, preserve the unconditional/conditional distinction, and make no full-solution or priority claim. No mandatory correction remains.

## Final hash coverage addendum

At 06:14 UTC on 30 September 2026, I compared the final PROOF.md byte-for-byte against the frozen reviewed version. The only change replaces the first status line to state that the partial passed independent review and to link this report. All mathematical text and the unresolved original-target qualification are unchanged. Final covered SHA-256: **464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c**. The author verification program is unchanged, and its receipt differs only in the recorded proof hash; all 211 assertion results remain identical. The PASS_CONDITIONAL_PARTIAL verdict extends to this exact final artifact.


# Imported moment-proof qualifications

These clarify ancillary applicability, not the submitted SIRSN theorem. The
exact [Kahn v3 PDF](https://arxiv.org/pdf/1503.03976v3), SHA256
`84af8a3084755d70c20a16f5de08e06129542058a88ff7d2f16399e5bfafe18c`,
was directly acquired and its complete Theorem5.1 proof read. Printed pp26–27
were inspected as pixels; pp12–13 and30 were also rendered and inspected to
check the further literal qualifications below. Its displayed conditional probability estimates
(18),(21),(22) are stronger than the event inclusion warrants; use
`P(L>r_m, T<=T_n)`, then add `P(T>T_n)`. The radius must use `T_n`, although
the displayed choice prints `T`. The asserted moment range survives these
repairs. Stronger moments in Remark5.1 remain conjectural.

Theorem3.1's geometric lower-bound/exponential-tail argument was also read.
Its literal cap-measure inequality directions on p12 and speed/constant presentation on p13
should not be copied as certified formulas. For the empty forbidden set
needed here, the independent reconstruction below supplies the required
positive-constant time tail. Theorem6.1 uses slow length bounded by speed
times time; its printed quotient must be a product. Full geodesic existence
and uniqueness foundations are external imports, not recertified here.

## Independent check of the needed time tail

Fix dimension d>=2 and gamma>d. Choose
`alpha>2^((gamma-1)/(gamma-d))`. Inside a fixed coarse ball, build deterministic
nested radius `a_j=a alpha^(-j)` nets. There are at most `C_0 M^j` relevant
child-ball pairs at depth j, with fixed `M=(2alpha+1)^d`; an extra fixed factor
in C_0 covers the pair count. Lines meeting both child balls have kinematic
measure at least `c_alpha a_(j+1)^(d-1)`, where `c_alpha>0`.

For example, offsets in a radius-a_(j+1)/4 perpendicular disk and directions
in a fixed cone with sine at most1/(8alpha) yield a positive lower measure:
the centers are at most2alpha a_(j+1) apart, so the other ball is still met.
The cone/offset integrals define c_alpha directly. Only positivity and the
scaling exponent are needed; no reversed inequality from the printed source
is used.

For u>=1, choose speed

    v_j = [c_alpha a_(j+1)^(d-1) / (K(j+1)+u)]^(1/(gamma-1)),
    K > log M.

The probability of no sufficiently fast connecting line for a given pair is
at most `exp[-K(j+1)-u]`. A union bound over every pair and depth is at most
`C exp(-u)`. On the complementary event, the recursive binary connector uses
at most `2^j` segments of length `C a_j` at depth j, and therefore has time at
most

    C a^((gamma-d)/(gamma-1))
      sum_j [2 alpha^(-(gamma-d)/(gamma-1))]^j
            (K(j+1)+u)^(1/(gamma-1))
    <= C' u^(1/(gamma-1)).

The geometric ratio is less than1, and alpha>2 also makes the Euclidean
segment-length sum finite. Net radii tend to zero, so the connector has the
specified endpoints. Consequently the geodesic time between two fixed
endpoints satisfies `P(T>C'u^(1/(gamma-1)))<=C exp(-u)` under the imported
existence/minimal-time framework. This verifies the time-tail mechanism with
unspecified positive constants and avoids inaccurate literal source constants.

## Independent check of the route-length moment step

Write `T_n=C(n+1)^(1/(gamma-1))` after increasing C to absorb the preceding
tail prefactor. For a path of Euclidean length L starting at x, each
`r<=L` requires maximum speed in B(x,r) at least `r/T`.
On `{L>r_m,T<=T_n}` this imposes the deterministic fast-line constraints at
every dyadic radius `r_l=2^l r_0`. The annular line sets are disjoint Poisson
sets. Successive speed-threshold events can be bounded by their unconditional
annular probabilities after excluding earlier faster lines; conditioning on
the geodesic time is never introduced.

The source's sequence decomposition then gives the event bound

    P(L>r_m,T<=T_n)
      <= 2^(-(gamma-1)(m+1)) p_n(r_0)(1+p_n(r_0))^m
      <= [2^(-(gamma-1))(1+p_n(r_0))]^(m+1),
    p_n(r_0)=2^(gamma-1)c r_0^(d-gamma) T_n^(gamma-1).

For any `0<kappa<gamma-1`, set

    p_* = 2^(gamma-1-kappa)-1 > 0,
    r_0(n) = [2^(gamma-1)c T_n^(gamma-1)/p_*]^(1/(gamma-d)),
    m = floor((n+1)/kappa).

Thus `r_0(n)=C(n+1)^(1/(gamma-d))`, and the event bound is at most
`2^(-(n+1))`. Adding the time-tail event gives

    P(L>C 2^((n+1)/kappa)(n+1)^(1/(gamma-d))) <= 2^(-n).

A tail partition, with an initial finite term and harmless index-shift
constant, proves `E L^delta<infinity` for `delta<kappa`: its series has ratio
`2^(delta/kappa-1)<1`, up to a polynomial factor. Since kappa can approach
gamma-1, the credited range is `delta<gamma-1`. In the planar model gamma>5
therefore suffices for a fourth moment.

These are verification clarifications of a credited existing proof mechanism,
not a new target attempt or a new-priority claim. The PR's conditional theorem
is independent of this model citation. Current source discussion should bind
this note if it retains the ancillary model applicability statement. Original
two substantive attempts, new substantive attempts0, audit attempts0; no paper
or DOI is warranted for this unresolved target.
