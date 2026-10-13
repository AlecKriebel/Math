# Scope, source lineage and verification supplement

Companion to *Polynomial-time optimization and exact separation for rational
mixed-integer bipartite covers*, Alec Kriebel, 12 October 2026. Reviews occurred
12 October PDT / 13 October UTC. Extensive AI use and unrefereed status apply
to both the note and supporting materials.

## Original target and exact finite interpretation

The original source is Conforti's *Combinatorial Mixed-Integer Programming*,
[Oberwolfach Report51/2008](https://ems.press/content/serial-article-files/46195),
printed pp.2904–2905, Problem1. A specified finite bipartite graph has rational
edge demands, any chosen integer coordinates and unrestricted variable signs.
The question concerns membership in the convex hull; its paragraph discusses
linear optimization. The source leaves real-query encoding implicit. The
theorem expressly uses rational demands, rational objectives and rational query
points, with total binary input size. Dimensions and denominators vary. No
arbitrary-unencoded-real oracle model is inferred from the source wording.

The complete contribution includes an exact attained optimum or certified
unboundedness, strong separation and exact membership in the **actual** hull,
including boundary. It does not prove Conjecture2, the separate subtree-hull
intersection statement. It does not supply an optimal running-time exponent,
strongly polynomial total algorithm, compact extended formulation, facet
classification or executable polynomial implementation of LP/SFM/GLS.

## Proof mechanisms and mathematical audit

Bipartite sign change preserves the integer coordinates and turns cover rows
into difference rows. An unbounded relaxation yields a polynomial-bit rational
improving ray whose denominator clearing is integral, so continuous and mixed
boundedness agree. The target is always mixed feasible. Free signs are used;
arbitrary additional bounds or orientations are not silently included.

The signed-threshold decomposition is conformal on coordinates **and** row
differences. At most n layers occur. A layer of weight at least one can be
removed from a mixed point without increasing objective. A compact nearest
point in a closed objective sublevel supplies attainment without presuming
a mixed optimizer. At least one optimum lies at sup-distance less than n
from the relaxation optimum; there is no claim that every optimum does.

Only integer–integer rows are rounded upward. Assigning remaining original
coordinates sufficiently large completes any admissible bounded integer
assignment. Min/max closure and modular objective prove submodularity of the
exact continuous-completion value. The label count is O(n) per integer
coordinate, independent of numerical demand magnitudes and denominators.
Prefix arcs, baseline forcing, out-of-range prohibitions and implication
closure supply the exact ring-domain interface, including the smallest member
and smallest member containing a node. A value oracle alone would not suffice.

The note explicitly bounds every slice value uniformly: coordinate denominators
divide the demand-denominator lcm k; objective denominators divide the lcm q;
value denominators divide kq and absolute values are at most
n A0 (H-star+nB). Tight spanning forests after fixed/zero anchoring prove these
bounds. All logarithmic encodings are polynomial. Established rational
submodular minimization and the lattice reduction in GLS1988 Sections10.2–10.3
supply oracle-bit complexity, rather than inferring it from operation count.

An objective-independent compact mixed core plus the integral threshold
recession cone equals the actual finite convex hull. Interpolation of integral
steps and strict separation prove the equality. This establishes closedness.
Totally unimodular bounded-slice matrices and homogeneous-generator cofactors
give a polynomial facet-encoding bound without enumerating generators or
denominator residues. The checked GLS1988 strong-optimization interface
permits nonvertex exact optimizers and normalized improving rays for unbounded
polyhedra. Its strong optimization/separation theorem then decides exact
rational membership, including boundary queries.

Two independent mathematical families rederived materially different fragile
steps. The proximity/bit family checked all signed layers, compact attainment,
slice completion, oracle denominators/numerators and arithmetic model. The
ring/hull family checked closures, domain encodings, actual convex-hull
recession/closedness, facet bounds and exact GLS interfaces. Both found no
mathematical blocker. Root separately read the full proof and derivations.
AI audit verdicts are records, not proof premises or human peer review.

## Prior credit and bounded priority finding

Cook–Gerards–Schrijver–Tardos1986, printed p.258 Remarks(1), already give
all-coordinate mixed-integer optimal-point proximity at most n times the
largest subdeterminant of the integral combined matrix. In this TU system
that bound is n. The note's signed-layer argument is a direct specialization,
with an attainment refinement, not a newly invented general proximity theorem.

Takamatsu–Hara–Murota2004 Proposition2 establishes hybrid partial minimization;
its complete three-page author translation was inspected, including its
optimization-algorithm future-work conclusion. MurotaMETR2002-12 / SIAM2003
Section4.1 documents L-natural scaling and an earlier n-squared ground-set
ring lineage. Schrijver2000 Section6 supplies the exact ring-family interface.
GLS1988 provides rational LP, exact rational lattice submodular minimization
and well-described-polyhedron optimization/separation. These are inherited
tools, not new abstract algorithms here.

Conforti–DiSumma–Eisenbrand–Wolsey2009 and Conforti–Wolsey–Zambelli2010 provide
the relevant network/bipartite formulations and historical numerical-denominator
gap. Their pseudopolynomial dependence does not supply the present logarithmic
encoding guarantee. The earlier half-integral/nonnegative cover result has
different hypotheses. Leiserson–Saxe1985/1988 concerns feasibility; the
Papaefthymiou1990 thesis optimizes objectives supported on integer coordinates
and leaves a general-objective NP-completeness conjecture unproved. None is
misrepresented as an optimization hardness proof. Later bidirected-path,
rooted-forest DR and structured mixed L-natural bodies were checked against
their precise additional assumptions.

The independent priority audit ran72 focused queries and retrieved19PDFs,
with body locators, successes, failed fetches and version hashes recorded.
No inspected primary body was found to state the full exact rational target
solution. The publishable unit is an explicit assembled application and full
bit-model accounting. This is a bounded-search inference, not proof of
worldwide priority, current openness or novelty of every ingredient. Unindexed,
unpublished, differently worded and uninspected work remain possible gaps.
No individual was contacted and no outreach was prepared.

## Computational corroboration and provenance

Pinned [PR#1025](https://github.com/AlecKriebel/Math/pull/1025) head:
7769e6872c3d2f4267706dc2400be3519186cf3d, catalogue30001102/OWR-2489-008.
The complete35-file submitted snapshot is retained byte-for-byte as history.
Old environmental seals and review counts are stage evidence, not current
publication acceptance. Public primary URLs and retrieved-byte hashes accompany
authored source audit records; third-party source bodies are not redistributed.

The portable kit uses three unchanged mathematical programs: the submitted
exact checker and the two new families' independently written checkers. It
replays nine baselines and fifteen actual defective-source controls in
normal/-O/-OO modes, comparing complete stdout, stderr, exits and recursive
JSON types against pinned references. Five source faults remove negative
layers, make thresholds strict, reverse the LP sign, remove subunit layers or
reverse submodularity. Exact intended rejection reasons are required; an
unrelated crash or syntax error does not pass a control. The family report
preserves original first-error expectation corrections as labelled history.

Each submitted baseline checks24 small models,5380 sliceLPs,65014 submodular
pairs,1723 removable layers,1000 threshold vectors and1692 ring comparisons.
Each fresh proximity baseline checks45 models,2095 sliceLPs,199661 submodular
pairs,2474 removals,7380 vectors and large binary inputs. Each fresh ring
baseline checks1789 ring families,598 sliceLPs and8888 submodular pairs, plus
actual-hull boundary/recession examples. Modes repeat the same deterministic
mathematical cases; they are not counted as new independent problem instances.

Python3.10+ and standard library suffice; no credentials, network, solver or
UID1000 account is required. The recorded execution is macOS/Python3.14.6;
other operating systems are not tested here. The original UID1000 permission
harness is not replayed or simulated. Isolated flags are not a security sandbox.
Small-case enumeration deliberately has nonpolynomial worst-case complexity;
it corroborates identities and boundary cases, not universal asymptotics.

Exact metadata, portable navigation and verification receipts accompany the
package. The first fresh whole-package review passed mathematics and found two P3
repairs: the GLS10.2.7 problem locator and B=1 for an empty edge set. Both were
corrected in the current source/PDF; original review inputs and records are
preserved. A NEW second review remains required. This draft is not yet approved for
immutable publication. Extensive AI use, unrefereed status and all scope/credit
limits must persist through paper, package, metadata and tracker. No formal
proof-assistant or conventional human peer-review certificate is claimed.
