# Independent geometric adversarial audit

Audit completed 2026-10-18 UTC. Scope: original OWR question, geometric dictionary,
positive mixture extraction, uniformity, exceptional events, and area-count moment
transfer for PR218 / 30006020. **No substantive mathematical defect found in this
family.** This is an internal mathematical audit of the stated result, not a claim
of human peer review, universal priority, or permission to promote the case.

## Inputs and independence

`INPUT_PINS.json` verifies the four pins supplied by Root, including the final PDF
and published verification ZIP. `PRIMARY_CACHE_RECEIPT.json` independently hashes
the original OWR, DL and DGZZ PDFs against `verification/PRIMARY_INPUTS.json`.
The primary PDFs were read from legitimate old local caches; fresh local text
extractions were made for this audit. Direct public PDF opens also succeeded.
No historical review verdict was read to reach this mathematical conclusion. The
original candidate and final manuscript were read before source reconstruction.

The exact final manuscript is
`authenticated_sources_01/existing_publication_audit/preprint/cylinder_areas.tex`.
Line references below are to that file. The primary reading copies under
`private_reading/` are **private source material, excluded from the authored output
manifest and not for redistribution**.

## Reconstruction of the original claim

OWR printed p.2386 defines uniform sampling among square-tiled surfaces with at
most N squares. Its footnote explicitly states that automorphism weighting makes
no difference to the limiting law. It fixes N tending to infinity first. Its
Theorem 2 on p.2387 identifies the known large-genus law specifically as the
principal holomorphic quadratic law Q(1^(4g−4)). Problem 2 immediately asks for
intermediate normalized areas, specifically [g^(-1/2),2g^(-1/2)]. The all-stratum
extensions are described as conjectural; the diagonal N=floor(alpha g) regime is
the separately numbered Problem 3.

Thus final lines 28–45 preserve the controlling ensemble and order of limits.
The manuscript does not solve all possible interpretations of “full spectrum”;
its explicit intermediate-window theorem does answer the written example and all
intermediate rates in that ensemble. The total-variation model additionally
describes the entire multiset, but is not relative-error control of arbitrarily
rare events (line 211).

DL printed pp.5096–5097 identify a component of the horizontal multicurve with a
horizontal cylinder; multiplicity is cylinder height. Theorem 1.4 explicitly
allows m=infinity. The bound is on maximum height, not on the degree or
primitivity of a torus cover. All positive heights are retained here.
DGZZ printed §2.1 states that the lower-dimensional strata have negligible
fixed-genus square-count contribution. This supports the use of the holomorphic
counting formula for the principal law. No uniform-in-g version of that
negligibility is required or used.

## Independent extraction of the area mixture

DL (3.1) and (3.2) give, for a weighted graph (Gamma,m), the product of graph mass
and area density. Their normalizing polynomial evaluation cancels, leaving a
common positive factor times

    F_Gamma(x_1/m_1,...,x_k/m_k) / (|Aut(Gamma,m)| prod m_i).

On the one-vertex graph with k loops, each monomial is
`A_(g,k) ctilde_(g,k)(j) prod x_i^(2j_i−1)/(2j_i)!`, with sum j_i=n=3g−3.
Consequently its height factor is exactly prod m_i^(-2j_i). Summing positive
heights gives prod zeta(2j_i); no cutoff error or interchange involving signed
terms is present. The simplex integral is

    prod (2j_i−1)! / (2n−1)!.

The residual monomial weight is therefore, up to one common factor,

    [A_(g,k)/2^k] ctilde_(g,k)(j) prod [zeta(2j_i)/(2j_i)] / k!.

Conditional on that monomial the vector has Dirichlet(2j_1,...,2j_k) law.
This verifies final lines 74–94, including every factor of 2 and k!, and yields
Gamma total parameter **2n=6g−6**. In particular a maximal cylinder is counted
once; its height does not create extra components.

The factor 2^k k! is the unweighted graph automorphism group. For unequal
heights the weighted graph group is smaller. DL Remark 2.5 makes precisely the
orbit/stabilizer conversion used when replacing a sum over weighted graph
isomorphism classes by a labelled height sum divided by the unweighted group.
It would be wrong to assign 2^k k! to each individual weighted graph; the
manuscript's *summed* expression is correct. The new rational controls directly
compare both sums for mixed and repeated heights 1,2,3.

For independently chosen ordered components, the k! convention also agrees with
the unlabelled assembly law: there are k!/prod c_j! ordered tuples with cycle
counts c_j, yielding weight prod a_j^(c_j)/c_j!. Repetitions cause no extra
factor. The finite Poisson conditioning in final line 65 is valid.

## Uniformity and exceptional events

DL (6.1), printed p.5116, permits every fixed C in the range k<=C log G, uniformly
over all valid degree vectors. In this application G=g−k and
k<=floor(0.6 log(6g−6)), hence k<=C log G for some fixed C and all sufficiently
large g. Also G tends uniformly to infinity over this range. Thus the triangular
substitution in final lines 84–89 is legitimate. There is no requirement that
selected j_i be macroscopic or bounded away from 1.

Direct cancellation gives the ratio at lines 96–99. Its numerator minus
denominator is

    30g − 24gk + 8k² + 14k − 30.

For k=O(log g), the ratio differs from one by O((k+1)/g). Multiplying these
positive ratios over k proves the stated O(log²(g)/g) bound. Together with DL's
uniform positive coefficient comparison, normalization gives a uniform density
ratio on the **latent** composition plus Dirichlet space. Pushing forward to
area multisets cannot enlarge total variation. For any nonnegative statistic f,
the same density bounds compare its integrals, even if f depends on g; zero
expectation is also harmless. No pointwise-to-uniform inference is being made.

DGZZ Theorem 1.12, printed p.137, applies to the cylinder-count law by its
Theorem 1.7, printed p.132. Taking t=11/10 gives E[t^K]=O(n^0.05).
Chernoff at k_g=0.6 log(2n)+O(1) gives exponent
eta=0.6 log(1.1)−0.05=0.007186...>1/220. Summing this exponential tail above
A log n, with sufficiently large fixed A, gives every fixed moment
E[K^r]=O(log^r n). It does not give a bounded total count, nor is one needed.

DGZZ Theorem 5.2, printed p.205, bounds multivertex excess by
O(log^25(g) g^(-1) 2^k) uniformly for k<=log(g)/log(9/4). The manuscript's
cutoff lies strictly inside that range for large g. Its exponent is at most
−1+0.6 log 2<0. Averaging over the conditional K law therefore leaves a
polynomially small error. The known range restriction is respected in final
lines 107–111.

Combining these bounds makes both geometric and model bad events polynomially
small. Cauchy–Schwarz then gives

    E[K^r;bad] <= O(log^r n) O(n^(-c/2)) = o(1).

Thus even exceptional surfaces carrying many unusually small components do not
invalidate any fixed compact-window count moment. An unquantified exceptional
probability, or total variation alone, would not have sufficed; lines 114–122 and
207 correctly supply the stronger argument. No rate for the DL coefficient
error is needed, because the good-event window moments are bounded independently
of n before transfer.

## All intermediate rates and normalized moments

For q=ns_g tending to infinity with q=o(n), removing r selected assembly
components gives the exact factorial identity at lines 149–154. All selected
sizes in fixed q-scale windows sum to O(q), so h_(n-r)/h_n tends uniformly to
one. Harmonic sums of zeta(2j)/(2j) give log(b/a)/2. This proves the unmarked
Poisson law without assuming a microscopic theorem or its tail is uniform on
growing windows.

The three Gamma ranges at lines 173–183 are sufficient even for q diverging
arbitrarily slowly. In the central range a Lipschitz test error sums to
O(q^(-1/2)); below aq/2 it is O(log(q+2)e^(-c_a q)); above 2bq it is an
exponential tail in j. The coefficient ratio h_(n-j)/h_n is bounded through
n/2 and at most O(sqrt n) beyond it. The latter polynomial factor is killed by
the exponential tail. There is no hidden log(n) union-bound loss.

For moment order r, split the exact marked factorial sum by total selected
size <=n/2. On the complement some selected j>=n/(2r); because q=o(n), that
component's probability of falling inside a fixed q-window is e^(-c_r n) for
large n. The remaining weight sums are O(log n), and the coefficient ratio is
O(sqrt n). This gives uniform moments of every fixed order, as claimed in
lines 196–203. Conditional on every composition, total Gamma shape is exactly
2n; hence the total lies outside [n,4n] with exponentially small probability.
Since K<=n, this event contributes o(1) to every fixed moment. This is a valid
uniform-integrability argument for normalized counts. No independence of the
total from the unnormalized marked process is assumed.

At fixed genus, counts in positive area windows are continuity observables
except when an area lies at an endpoint. All multi-cylinder pieces have simplex
densities. The sole single-cylinder area is 1, eventually outside every window
[a s_g,b s_g]. With K<=3g−3 at fixed genus, the fixed-genus square-count limit
also transfers fixed count moments. This validates lines 209–211 and the exact
iterated sampling order; it supplies no diagonal N(g) claim.

## The 4g−4 reservation

OWR p.2387 literally prints 4g−4 in its microscopic statement. The exact DL
monomial density above forces 6g−6. Final lines 52–53 acknowledge the discrepancy
and do not use the microscopic assertion. These two normalizations would yield
different fixed microscopic density formulas. They cannot be equated.

The intermediate intensity dx/(2x) is invariant under every fixed positive
dilation, and the direct q argument proves it independently. Therefore this
unresolved short-report discrepancy is not a conditional in the proved
intermediate-window result. It remains a source ambiguity about the unused
microscopic summary, not a falsification of the manuscript's stated theorem.

## New reproducible controls and remaining boundary

Run `python3 independent_geometry_controls.py`. The script imports no frozen
verifier. It constructs genus-zero one-vertex graph polynomials directly by
enumerating half-edge intersection degrees, using
<tau_d>_(0,N)=(N−3)!/prod d!. Across global g=2,3,4,5, it evaluates 12,292 raw
terms and checks all 398 paired monomials against the extracted F expansion.
It verifies beta normalizers, total-area first/second moments, and orbit versus
labelled-height summation exactly for g=2,3,4 with height cap 3. It checks the
prefactor cancellation by factorials at g=100 and 1000, then records finite
relative errors through g=10^6. Results are in
`INDEPENDENT_GEOMETRY_RESULTS.json`.

These are finite algebra/convention controls. They do not prove the uniform
large-genus intersection asymptotics or the multivertex bounds independently of
DL/DGZZ; those remain explicit credited primary theorem inputs. The strongest
verified result in this family is the stated principal-quadratic,
N-then-g, all-intermediate-rate geometric Poisson process law with all fixed
joint compact-window count moments. **Exact remaining gap within this audit:
none found, conditional only on the openly cited published geometric theorems.**
The broader strata, primitive-cover ensembles, all directions jointly and
diagonal sampling remain outside the theorem. Universal priority is outside
this family's finding, particularly the unavailable announced small-components
manuscript. No communication or outreach was prepared or initiated.
