# Initial literal-primary seal: PR42 / id 2233 / EP-653

Prepared independently in this dedicated family before candidate-snapshot access.
Initial seal time is the UTC timestamp in `initial_seal.json`, produced after
the accompanying controls. The seal closes only this initial stage; it is not a
PASS, publication recommendation, problem solution, or historical model/runtime
attestation. This audit adds zero substantive problem attempts and zero audit
turns to the original/source budgets.

## Access and independence disclosure

Read root `/Users/alec/Documents/Math/AGENTS.md`. A root-wide AGENTS filename
inventory found only root AGENTS and `unsolved_math_prioritization/AGENTS.md`;
the latter does not govern this family. Read only the supplied flat
`../pinned_problem.json` as local problem input. No candidate branch, candidate
file, previous review, prior attempt, sibling interpretation, or root
interpretation was deliberately accessed before this seal.

The pinned `background` contains a 2026-08-17 literature triage. I was exposed
to its status, bounds, and assessment. Those are source claims, not independently
audited proof inputs. The decoded `statement` contains a literal newline where
the intended `j\neq i` command was split; `literal_controls.py` records its
exact decoded representation and hash. I repair that notation explicitly to
`j != i` for mathematical interpretation.

Important accidental exposure: general web searches unexpectedly returned
snippets from ResearchGate titled *An incidence bound for distinct
pinned-distance counts* (claiming a 5/7 defect exponent via circles and a recent
incidence theorem), and from erdosproblemaday.com/report/653 (finite-work and
literature review details). These pages were not opened or used as proof inputs.
Further exact-title searches also returned snippets of that report. They are
excluded foreign material. I cannot honestly claim the circle mechanism below
was fully free of pre-seal candidate-related exposure. The elementary line
mechanism and definitions are independently checkable regardless of this
exposure. Search snippets are not accepted as author proofs or priority evidence.

No external individual was contacted. Automated public-source retrieval only.
No branch, Git index, canonical research log, candidate, or native document was
edited. This family writes only its own files. No papers, DOI, historical model,
or original runtime provenance claim is made.

## Literal scope and primary-source limits

For a set P of n distinct planar points, define

    R_P(p) = number of distinct positive Euclidean distances |p-q|,
             q in P minus {p};
    nu(P) = cardinality of {R_P(p): p in P};
    g(n) = max_{|P|=n} nu(P).

The exact target is g(n)/n -> 1, equivalently: for every epsilon>0 there exists
N such that every integer n>=N admits an n-point set P with nu(P)>=
(1-epsilon)n. A subsequence alone is insufficient without an all-n transfer.
The maximum is well-defined because nu ranges over finitely many integers and
there is at least one configuration.

The literal flat statement and Bloom list n locations but do not explicitly
say pairwise distinct. The standard set interpretation is supported by the
Erdos--Fishburn publisher abstract, which specifies a set of n points and
1<=f_i<=n-1. All the deductions here explicitly assume distinct points. For
repeated locations zero distances and multiplicities change the geometry;
the intersection counting argument counts distinct locations, not copies.

Actual current Bloom page: `foreign_primary/bloom653.html`, fetched HTTP 200 on
2026-10-02 during the PID/time-captured initial fetch. It states the same
definition and near-n question, marks OPEN, and attributes 3n/8, 7n/10 and a
defect of order n^(2/3). This is evidence of the tracker's current statement,
not a proof or proof of unresolved status. The site itself warns its open
status reflects the owner's belief. The 3/8 bound is weaker than the elementary
line construction below, so it must not be treated as the strongest available
lower bound solely on this evidence.

Primary original-source access:

* Erdos--Fishburn, *Distinct distances in finite planar sets*, Discrete
  Mathematics 175 (1997), 97-132: the publisher's indexed abstract establishes
  its count-vector definition and sum-minimization topic. The actual publisher
  requests, including PDF, returned 403. Guessed Renyi PDF filenames returned
  404 and establish nothing. No full proof or operative coefficient was read;
  neither the claimed 3/8 lower bound nor n^(2/3) upper bound is imported here.
* Csizmadia--Ismailescu, *Maximum number of different distance counts*,
  Intuitive Geometry, Bolyai Society Mathematical Studies 6 (1997), 301-309:
  Google Books primary scan search responses, captured in
  `csizmadia_book_about.html` and `csizmadia_book_page301.html`, identify a
  construction of 10N+5 points with 7N-4 different counts on page 302. These
  snippets establish at most that the source states such a construction and
  asymptotic ratio .7; they do not expose a complete proof or all-n theorem.
  Page-image attempts for 301-309 all returned the same 382-byte placeholder,
  visually inspected for PA301, not actual pages. No original lower bound,
  exponent, or full-paper verification is imported as a proved theorem.

Every downloaded foreign file is individually inventoried with URL, UTC time,
status, byte size and SHA256 in the fetch inventories. It is excluded from the
first-party closure. Original sources were unavailable beyond the specified
abstract/snippet limits; outside author input could help, but no outreach is
prepared or initiated.

## Mechanism L: exact line-family spectrum

Any point on a line has at most two other points at a given positive distance.
Therefore every R_P(p)>=ceil((n-1)/2), and every R_P(p)<=n-1. Thus all counts
lie in an integer interval of length ceil(n/2), so nu(P)<=ceil(n/2).
For P={(i,0):0<=i<n}, distances from i are exactly the integers 1 through
max(i,n-1-i). Their different counts fill the whole stated interval. Hence

    max_{P collinear, |P|=n} nu(P) = ceil(n/2),
    and g(n)>=ceil(n/2).

This is a complete family theorem for n>=2, not a novelty claim. It shows that
collinear constructions cannot attain the conjectured ratio. Assuming a
generic perturbation preserves a large spectrum is unsafe: if all unordered
pair distances are different, each pinned count equals n-1 and nu(P)=1.
Repeated distance structure is essential, and integer counts are unstable
under perturbation of exact equalities.

## Mechanism C: two low-count centers and circle intersections

Let k=nu(P), h=n-k. Since the counts are distinct positive integers in
{1,...,n-1}, h>=1. Write a_1<...<a_k for the count spectrum. For every i,

    a_i <= (n-1) - (k-i) = h+i-1.

This statement is about distinct spectrum representatives, not the i-th point
in the full list with multiplicities. If k>=2, choose p,q with counts a_1,a_2.
For each point z outside {p,q}, z lies on one of the a_1 positive-radius circles
centered at p and on one of the a_2 circles centered at q. Two such circles
have at most two intersection points because their centers are distinct;
tangent/disjoint pairs only reduce that number. Thus

    n-2 <= 2 a_1 a_2 <= 2h(h+1).

If k=1 then h=n-1 and the same last inequality holds for n>=2. Therefore

    g(n) <= n - ceil((sqrt(2n-3)-1)/2),       n>=2.

The square-root expression is zero at n=2 while h>=1 separately, so one may
replace the ceiling by max(1,ceiling). The deduction is elementary and weaker
than the claimed historical n^(2/3) bound. It remains compatible with g(n)/n
->1, since sqrt(n)=o(n). It cannot refute the conjecture.

A broader circle incidence encoding, without importing any theorem, is also
checkable: choose m distinct spectrum representatives, all among the smallest
m count values. For m<=k their positive-radius circle union C has size
M=sum R(p_i)<=m(h+m-1). No two circles coincide since their centers differ.
Every selected center contributes exactly n-1 point-circle incidences;
therefore I(P,C)=m(n-1), not merely an approximate count. Any stronger imported
incidence theorem must apply to all real planar points and distinct arbitrary
positive-radius circles, with absolute constants and the correct n,M terms.
Without reading/validating that theorem, a stronger defect exponent is an
unsupported gap. This encoding is not asserted exposure-independent or novel.

## Boundary checks and finite constructions

For n=1, the single count is zero, so g(1)=1; positive-count arguments start at
n=2. For n=2, both counts are 1, so g(2)=1. Three equally spaced collinear points
give counts (2,1,2), so g(3)=2. The points

    (0,0), (2,0), (1,sqrt(3)), (-2,0)

have exact squared-distance count vector (1,2,2,3), proving g(4)=3 by the trivial
n-1 upper bound. `literal_controls.py` checks these squared distances exactly,
the line formulas through n=200, all size 2-5 subsets of a 4x4 integer grid,
and deterministic samples. The grid/sample checks are finite diagnostics only;
the universal proofs are the preceding paragraphs. Squaring is injective on
positive distances, so exact squared-distance equality suffices.

Important logical distinctions: g is a MAXIMUM of spectrum cardinality; a
single configuration with small nu is not an upper bound for g. R_P(p) counts
different radii, not neighbors/degrees (the complete geometric graph always
has degree n-1), not total pairwise distances, not sum R, and not the number of
points realizing a count. A sublinear upper defect, whether sqrt(n), n^(2/3)
or n^(5/7), does not contradict the near-n conjecture.

## Checkpoint

Scientific completion estimate toward settling the literal asymptotic
question: 5%. Audit stage completion estimate after initial seal: 35%.
Strongest fully checked results of this family are the exact collinear maximum,
the elementary universal square-root defect, and g(2),g(3),g(4). Exact remaining
gap: neither a uniform n-o(n) construction nor a linear-defect universal bound
is available. Historical stronger bounds remain source statements, not
independently full-proof-verified results in this initial stage.
