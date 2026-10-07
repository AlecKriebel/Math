# Classical cost--Betti bridge: independent source check

Checked 2026-10-06, 21:29 America/Los_Angeles (2026-10-07 04:29 UTC).
Assigned route: classical reduction only. This report does **not** certify the
upstream Bernoulli lower bound or the upstream finite-height upper bounds.
No external communication or Git mutations were performed.

## Verified classical inputs

The primary article is Damien Gaboriau, *Invariants l2 de relations
d'equivalence et de groupes*, Publications Mathematiques de l'IHES **95**
(2002), 93--150, DOI [10.1007/s102400200002](https://doi.org/10.1007/s102400200002).
The [published PDF](https://numdam.org/item/10.1007/s102400200002.pdf)
was inspected at the actual statements, including visual inspection of
printed pp. 126 and 128. Under its standard, countable, p.m.p. relation
conventions:

- Corollary 3.16, p. 126: if R is produced by a free p.m.p. action of a
  countable discrete group G, then beta_n(R,mu)=beta_n(G), for every n.
- Properties 3.15(1), p. 126: infinite equivalence classes imply beta_0(R)=0.
- Corollary 3.23, p. 128: C(R)-1 >= beta_1(R)-beta_0(R), with equality for
  treeable relations.

The global space convention is standard Borel with an atomless probability
measure (p. 93 and section 1.3, p. 110). Ergodicity is absent from these
statements and their section hypotheses; the introduction also expressly
remarks on absence of ergodicity hypotheses (p. 95). The equality question
is posed immediately afterward on p. 129. Gaboriau's
[FAQ](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/FAQ.pdf), p. 1, points
to these same printed locations.

The comparison of group cost and action cost uses Gaboriau, *Cout des
relations d'equivalence et des groupes*, Inventiones Mathematicae **139**
(2000), 41--98, DOI [10.1007/s002229900019](https://doi.org/10.1007/s002229900019).
[Definitions I.5(2)--(4), p. 50](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/Cout/Cout.pdf)
distinguish relation cost, the infimum over free-action costs defining
group cost, and fixed price.

Source bytes, retrieval times, and SHA-256 hashes are recorded in
`sources/manifest.json`. Downloaded third-party PDFs and their renders are
local reading evidence; this report does not establish redistribution
rights for a publication package.

## Fully proved conditional deduction

**Proposition.** Let G be a countably infinite discrete group. Suppose:

1. For each integer M>100 there is an essentially free p.m.p. action
   on a standard probability space Y_M satisfying
   C(R_Y_M)<=1+99/M.
2. There is an essentially free p.m.p. action on a standard probability
   space X satisfying C(R_X)>=1+eta, for a specified eta>0.

Then beta_0(G)=beta_1(G)=0, and every essentially free p.m.p. action
Z of G has beta_0(R_Z)=beta_1(R_Z)=0. In particular,

    C(R_X)-1 >= eta > 0 = beta_1(R_X)-beta_0(R_X).

Moreover C(G)=1=1+beta_1(G). Thus this would refute the general
**relation-level** equality, while satisfying the stated **group-level**
equality for this particular group.

**Proof.** Countability allows replacing each essentially free action by
its invariant conull Borel subset of points with trivial stabilizer.
This changes neither the measured relation nor its invariants. Every
orbit in the restricted action is in bijection with the infinite group
G. Consequently beta_0(R_Y_M)=0. By Corollaries 3.16 and 3.23,

    0 <= beta_1(G) = beta_1(R_Y_M)
       <= C(R_Y_M)-1 <= 99/M,

for every integer M>100. Given epsilon>0, choose an integer
M>max(100,99/epsilon). This proves beta_1(G)=0. Corollary 3.16
then gives beta_1(R_Z)=0 for every free p.m.p. action Z. Infinite
orbits give beta_0(R_Z)=0, and Corollary 3.16 gives beta_0(G)=0.
Applying assumption 2 proves the strict displayed inequality.

For every free p.m.p. action Z, Corollary 3.23 and nonnegativity of
beta_1 give C(R_Z)>=1. Therefore C(G)>=1. Assumption 1 gives
C(G)<=1+99/M for every M>100, hence C(G)<=1. The asserted
group cost equality follows. No orbit equivalence between X and
Y_M, no ergodic decomposition, and no exchange of limits with a
varying Betti number are used. The Betti number being bounded is the
single number beta_1(G). QED.

**Generalization of the verified deduction.** The integer parameter and
constant 99 have no structural role: it suffices to have free p.m.p.
actions Y_k with C(R_Y_k)<=1+epsilon_k and epsilon_k->0, together
with a free p.m.p. action having cost greater than one.

## Full beta_0 correction and boundary checks

The general proposed equality is

    C(R)=1+beta_1(R)-beta_0(R),

not C(R)=1+beta_1(R) without an aperiodicity condition. The latter
specialization is justified here by infinite free orbits.

- Finite-group boundary: for |G|=n<infinity, beta_0(G)=1/n and
  beta_1(G)=0 (Gaboriau 2002, Example 1.6, p. 109). A free action
  has finite classes of size n. The corrected equality gives
  C(R)=1-1/n; dropping beta_0 would give the wrong value 1.
- Nonfree boundary: infinitude of the acting group alone does not
  imply infinite orbits. The trivial action of an infinite group has
  singleton orbits, C(R)=0, beta_0(R)=1, beta_1(R)=0. Moreover
  Corollary 3.16 cannot identify the group's Betti numbers with those
  of this relation.
- Atomic boundary: an essentially free p.m.p. action of an infinite
  countable group cannot have a positive-mass atom. All translates
  of such an atom would have the same positive mass, contradicting
  probability measure. Thus the atomless convention causes no gap
  for the conditional proposition, even if the phrase "standard
  probability space" initially allows atoms.
- Infinite-cost boundary: neither a finite Betti number nor a finite
  cost is assumed for arbitrary Z. The low-cost actions force the
  common beta_1 to be finite and zero. For the intended finitely
  generated group, a finite generator graphing bounds every
  action's cost by the number of generators.
- Nonergodic boundary: the source results apply to a specified
  invariant probability measure. One must keep the measure in the
  notation until freeness identifies beta_n(R,mu) with beta_n(G).
  No hypothesis that a nonergodic action has isomorphic ergodic
  components is needed.

## Elementary checks of the displayed upstream group and actions

Only `build/introduction.tex` and `build/group-actions.tex` from family
259 were read. Their hashes and the clone HEAD are in
`upstream-read-manifest.json`; HEAD was the requested
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

The displayed definitions are

    A = F(a,b_1,...,b_99),
    w = ab_1ab_2...ab_99a,
    J = <b_1,...,b_99,w> <= A,
    G = A *_J (J x <t>),

where <t> is infinite cyclic. Standard amalgam normal form embeds A
and J x <t> into G. Hence G is infinite (already because A embeds),
countable, and generated by the 101 listed elements
a,b_1,...,b_99,t. The provided reduced-word proof that the displayed
generators freely generate J also passes an elementary check: any
nonempty reduced word in them expands to a nonempty reduced word in
A, since w starts and ends in a, while all b_i symbols are different
from a, and adjacent opposite-sign w symbols are excluded.

The exponent sum of a on A extends to chi:G->Z by
chi(jt^n)=chi(j) on J x <t>. In particular chi(w)=100,
chi(a)=1, and chi(b_i)=chi(t)=0. Agreement on J makes the
amalgam extension valid; one must not incorrectly assume chi(J)=0.

For X_0=[0,1]^G with product Lebesgue measure, the formula
(xg)(h)=x(gh) defines a right action by coordinate permutations.
It is Borel and p.m.p. For g!=1, xg=x implies x(g)=x(1), an
event of probability zero by independence and the atomless base.
Intersecting over the countably many nonidentity g gives the stated
invariant conull free set X. Products with Z/M, endowed with uniform
measure, remain standard and atomless. The formula

    (x,r)g=(xg,r+chi(g) mod M)

is a p.m.p. right action. Any stabilizer in this product is already
a stabilizer in X, so it is free. These elementary checks establish
the group/action hypotheses; they do not establish either cost bound.

Although unnecessary for the classical bridge, both displayed actions
are ergodic. The Bernoulli action is mixing: cylinder events depend on
finite sets of coordinates, and sufficiently distant group translates
have disjoint coordinate sets, giving independence; approximation by
cylinder events extends this to measurable events. Put
H_M=ker(chi mod M). It contains the infinite cyclic group <t>, so
H_M is infinite, and the same argument shows the H_M restriction of
X is mixing and ergodic. A G-invariant subset E of Y_M has sections
E_r in X invariant under H_M, each of measure zero or one. The
element a cycles all M heights, and invariance makes their measures
equal. Thus E has measure zero or one.

The upstream main theorem parametrizes eta by

    K=e^96 96^99 / 95^95,
    0<alpha<1/200, K alpha^3<1/2, eta=alpha/100.

An exact permitted choice is alpha=(4K)^(-1/3), so eta=
(4K)^(-1/3)/100>0 and K alpha^3=1/4. Since
K>96^4>200^3/4, this alpha is strictly below 1/200. This
converts its symbolic gap to a fixed explicit expression **if the
upstream Bernoulli lower-bound theorem is valid**.

## Dependency status and checkpoint

| Dependency / mechanism | Evidence | Status | Exact remaining gap |
| --- | --- | --- | --- |
| Classical inequality with beta_0 | Actual published Cor. 3.23 and proof inspected | Verified classical input | None for the stated use |
| Free-action Betti identity | Actual published Cor. 3.16; global conventions checked | Verified classical input | None for the stated use |
| beta_0=0 | Infinite free orbits plus Prop. 3.15(1) | Verified | None |
| Group/action admissibility | Definitions and elementary arguments above | Verified elementary check | No cost information follows |
| Limit-to-zero deduction | Explicit epsilon proof above | Verified conditional result | Requires genuine upper bounds for arbitrarily large M |
| Bernoulli positive cost gap | Upstream theorem statement read, proof not audited here | Unverified here | Requires independent validation of pivotal upstream proof |

Assigned classical-bridge completion estimate: 100%. Unconditional
core resolution is not established by this route, and no percentage
is asserted for other agents' dependency audits. Publication-package
completion contributed by this route: 0% (reading evidence and research
notes only). Strongest result: the fully proved conditional proposition
and elementary group/action checks above.

No novelty claim is supported by this reduction. Its mathematical
machinery and implication are classical; any breakthrough would be
the validated upstream failure of fixed price. Whether the same
consequence has already been publicly recorded is for the separate
priority audit.
