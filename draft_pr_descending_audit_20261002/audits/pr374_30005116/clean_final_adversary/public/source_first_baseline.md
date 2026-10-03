# Source-first baseline (sealed before candidate access)

This is an independent audit baseline, not a claim of novelty or a solution.
The discovery goal is to determine the maximum induced C4 density for every
edge density over **all** graph sequences whose orders tend to infinity.

## Sources and reading

Fresh bytes were fetched on 2026-10-03; the private fetch receipt records exact
timestamps, source URLs, response metadata, PDF and extracted-text hashes.
Critical formulas were inspected both in text and in rendered pages. No candidate
result, candidate code, old review, root audit or sibling audit was read before
this document and the baseline control program were sealed.

* OWR, https://ems.press/content/serial-article-files/46961, PDF pages 63–64,
  printed 1227–1228: Problem 10 is unrestricted; Conjecture 11 specifies the
  dense range and triangle-density construction, with reciprocal endpoints known.
* Liu–Mubayi–Reiher, https://homepages.math.uic.edu/~mubayi/papers/XizhiReiherInduced.pdf:
  definitions (pages 1–2), Construction 1.9 (page 5), Conjecture 1.17 and
  Theorems 1.16/1.18 (page 10), Proposition 6.1 (page 22).
  Their densities count unordered induced vertex subsets. The low-density
  profile is 3p²/2. The dense upper bound is 3p(1-p)²; its equality at p=1-1/k
  does not prove the interior dense conjecture.
* Pikhurko–Razborov, https://pikhurko.github.io/E/PikhurkoRazborov17cpc.pdf:
  construction (page 2), Theorem 1.1 (page 3), structural and edit-distance
  deduction (pages 8–9). The near-minimum-triangle statement has uniform
  epsilon–delta–n0 quantifiers and allows an arbitrary triangle-free last block.
  Its edit conclusion uses the special deterministic outer structure and triangle
  removal, not a general identification of cut distance with edit distance.
* Balogh–Lidický–Mubayi–Pfender–Volec, https://homepages.math.uic.edu/~mubayi/papers/Semi_Inducibility.pdf:
  definitions (page 2), AC4 pattern and Theorem 1.3 (page 4).
  AC4 fixes two edges and two nonedges, leaving two pairs unconstrained, and
  counts injections divided by n⁴. It is not the induced C4 pattern, which fixes
  all six pairs. That theorem cannot establish the requested profile.
* Coudert–Coulomb–Ducoffe, https://dmtcs.episciences.org/13878/pdf,
  section 6.2, page 18: cographs arise recursively by union and complement;
  join follows. This is a restricted host class.

## Exact formulation and independent deductions

For a graph G on n vertices let p_G=e(G)/binom(n,2) and
q_G=N_ind(C4,G)/binom(n,4). Define F(p) as the supremum of limiting q_G
over sequences n→infinity and p_G→p. Success requires F(p) for every p,
including p=0,1; a theorem only on a host class is partial evidence.

For a symmetric measurable graphon W in [0,1], write p(W)=integral W and
J(W)=integral W12 W23 W34 W41 (1-W13)(1-W24), and q(W)=3J(W).
The factor is 4!/|Aut(C4)|=24/8=3. Uniform sampling with replacement differs
from sampling distinct vertices with probability at most 6/n, so
|q(W_G)-q_G|≤18/n. Also p(W_G)=(1-1/n)p_G. These errors are independent
of the structure or depth of G and therefore apply to every graph sequence.
Continuity in L1 gives |p(W)-p(V)|≤||W-V||1 and
|q(W)-q(V)|≤18||W-V||1 by telescoping six [0,1] factors.

Each induced C4 supplies two perfect matchings, each an unordered pair of
edges. Consequently 2N_ind(C4,G)≤binom(e(G),2), implying F(p)≤3p²/2.
A complete bipartite graph with part proportions a,1-a has p=2a(1-a) and
q=6a²(1-a)²=3p²/2, giving equality for p≤1/2. Clique plus isolates has
p=a² and q=0, proving the lower feasible boundary is zero for every p.

For a complete multipartite graphon with part masses a_i summing to one,
S_j=sum_i a_i^j, p=1-S2 and q=6sum_{i<j}a_i²a_j²=3(S2²-S4).
All sums converge absolutely for countable support. For p∈[1-1/r,1-1/(r+1)]
put a=(r+sqrt(r((r+1)(1-p)-1)))/(r(r+1)) and b=1-ra.
The proposed LMR construction has r masses a and one mass b, and provides
the lower bound Phi(p)=3((1-p)²-ra⁴-b⁴). At p=1-1/k it gives
3(k-1)/k³, matching the known upper bound. At p=1, q=0 follows from the
two required nonedges, and the construction is interpreted by a limiting sequence.
An interior unrestricted inequality q(W)≤Phi(p(W)) is **not** deduced here.

For a union of children of masses a_i and normalized densities p_i,q_i,
p=sum a_i²p_i and q=sum a_i⁴q_i. For their join,
p=1-sum a_i²(1-p_i) and
q=sum a_i⁴q_i+6sum_{i<j}a_i²a_j²(1-p_i)(1-p_j).
The 2+2 allocation is the only C4 crossing a join node: either child contributes
a nonedge. Empty-mass children contribute zero. These are identities, not a
proof that arbitrary cographs attain the multipartite upper curve.

For W(x,y)=f(x)f(y), let m=E[f], s=E[f²], t=E[f³]. Then p=m² and
q=3(s²-t²)². For 0<m<1, boundedness and Cauchy–Schwarz give
m²≤s≤m and s²/m≤t≤s-(m-s)²/(1-m). The lower t bound follows from
(E[f²])²≤E[f]E[f³]; the upper follows by expanding E[(1-f)(f-d)²]≥0
at d=(m-s)/(1-m). Equality for the lower bound forces
f∈{0,s/m}; for the upper f∈{d,1}, modulo null sets. Thus this applies
to arbitrary measurable f, not just sampled finite support.

Because 0≤t≤s, the maximal q at fixed m,s uses t=s²/m. Maximize
s²-s⁴/m² on s∈[m²,m]: its unique nonzero critical maximum is s=m/sqrt(2)
when m≤1/sqrt(2), and otherwise s=m². The rank-one maximum is
3p²/16 for p≤1/2, and 3p⁴(1-p)² for p≥1/2. Equality is achieved by
f=1/sqrt(2) on a set of measure sqrt(2)m, zero elsewhere in the first case,
and f≡m in the second. q=0 is achieved by f∈{0,1} with mean m.
Mixing these two probability distributions preserves m and varies q continuously,
so every ordinate between zero and the maximum is attained. Endpoint means
0 and 1 force constant f and q=0. This restricted maximum is not F(p).

## Planned falsification and exact gap

Audit the universal mechanisms, not merely a numerical grid: optimization with
arbitrarily many parts; countable support; zero children; reciprocal and p=1
endpoints; arbitrary-depth cotrees; measurable rank-one moment laws; exact
normalization and collision bounds; and the credited stability theorem's
quantifiers. Distinguish L-infinity perturbations, L1 edits and cut distance.
Fresh exact-count controls will supplement proof review. Candidate scripts and
past reports must wait until the mathematical verdict and new programs are sealed.

Completion estimate: source baseline ~15% of the audit workflow; unrestricted
discovery remains unproved. Final acceptance of future refreshed objects is pending.
