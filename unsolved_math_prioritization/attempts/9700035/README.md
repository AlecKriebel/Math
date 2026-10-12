PR41 / AMR-096-0035: full indexed target UNSOLVED; scoped partial.

The span is the union of all prescribed pair routes, including exterior excursions. The unconditional interior expected-length law and full-length lower bound are valid; the full law requires the explicit additional t^4 P(D>t)->0 condition (finite fourth moment suffices). This argument does not close the expected exterior-length gap from the ordinary axioms. A full SIRSN supplies finite major-road intensity p(1); a weak SIRSN does not automatically do so. The published question permits sufficient extra assumptions; this is not a general SIRSN solution or a priority certificate.

Original16, main PROOF, all code, full saved results, source/prior/provenance and two turns are exact archives. The imported prior is PRESENT and its Steiner wording is historical, corrected by current interpretation. Root actually reproduced211/3809 original checks and1326/122 family controls, and checked full149MB/all15458 SQL joins. Finite checks supplement primary analytic reading. The credited Kahn model moment import requires the exact joint-event/T_n/time-tail/slow-length qualifications appended below; it is independent of the main conditional theorem.

Current NEW whole-source-first review is PENDING; all embedded historical PASS/model/reasoning/deadline labels are archival. Current model/reasoning/deadline/verdict remain present nulls. Original2/5, new0/audit0. No paper, DOI, tracker, shared/native/Git/remote mutation or outside contact.

CURRENT_PROOF_DEPENDENCIES paths resolve against repository_root/draft_pr_publication_program_20260930/audits/pr41_9700035, including after canonical copying. Private scratch is never an anchor. All copied members and saved outputs are0444; old file writers need separately reviewed fresh code-only directories and new result files. Foreign primary PDF/text/render/HTML/cache bodies are individually hash-bound but not copied. The full retained root130+15 first-party closures are copied, including archival original helper inputs. A fresh whole-current source-first review is required before promotion; no old PASS transfers. The queue patch is local prospective named-column data only.

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
