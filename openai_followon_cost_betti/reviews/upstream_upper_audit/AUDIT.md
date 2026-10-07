# Independent audit of family 259: group and upper-cost actions

Audit timestamp: 2026-10-06 21:30 PDT (2026-10-07 04:30 UTC).

Assigned audit completion estimate: 100%. This is an estimate of coverage of
the assigned group/action/upper-cost dependency, not of the full cost–Betti
research target. The positive Bernoulli lower bound has not been verified in
this review, so the full counterexample remains unresolved by this report.

## Scope and verdict

Source checkout: `/Users/alec/Desktop/math`, HEAD
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The checkout was used read-only.
No upstream build, write, Git mutation, or external communication occurred.

The entire `build/group-actions.tex` was read, including all its proofs.
The introduction, conclusion, manuscript README and INPUTS were read; the
compression proof was read to check the manuscript's cost-at-least-one
corollary. The Lean catalogue and relevant scope listings were inspected.
The high-cost proofs in deployment, finite models, planar diagrams, and rank
surgery are outside this assigned review.

**Verdict:** no mathematical obstruction was found in the explicit group,
freeness, p.m.p. property, standard Borel property, or upper-cost graphing.
The stated inequality `Cost(R_(Gamma acting on Y_M)) <= 1 + 99/M` holds for
every integer `M > 100` by the proof below. There is an unstated but readily
proved strengthening: both X and every Y_M are ergodic. This avoids any need
to invoke a classical theorem for nonergodic actions in this part of the
follow-on argument.

The strongest result verified by this review is an explicit infinite
101-generator group and a sequence of free ergodic p.m.p. actions whose costs
tend to one. Establishing `Cost(R_X) > 1` requires the separate lower-cost
audit. The upper-cost result alone does not produce the requested
counterexample.

## Explicit data and independent proof

All source pointers in this report are relative to the above pinned
checkout and manuscript directory
`preprints/A-group-without-fixed-price-October-5-2026`.

Let

\[
A=F(a,b_1,\ldots,b_{99}),\quad
u_0=1,\quad u_i=u_{i-1}ab_i,\quad
w=u_{99}a=ab_1ab_2\cdots ab_{99}a,
\]

and define

\[
J=\langle b_1,\ldots,b_{99},w\rangle\le A,
\quad B=J\times\langle t\rangle,
\quad \Gamma=A*_J B,
\quad\langle t\rangle\cong\mathbb Z.
\]

Equivalently this gives the finite presentation

\[
\Gamma=\langle a,b_1,\ldots,b_{99},t\mid
[t,b_i]=1\ (1\le i\le99),\ [t,w]=1\rangle.
\]

The amalgam embeddings are injective by the usual reduced normal form,
whose full coset-string proof is supplied at `build/group-actions.tex:38–67`.
That proof does not assume the conclusion: factor actions on alternating
coset strings agree on J and therefore define an action of the amalgam.
An alternating word outside J increases the string length at every step.
In particular A embeds and is infinite. The generators a, all the b_i,
and t generate both factors, giving 101 generators; finite generation
gives countability. The embedded B shows that t has infinite order.

J is free on the 100 displayed generators. In a nonempty abstract reduced
word in b_i and w, maximal b-only blocks remain reduced after expansion.
Every w starts and ends with a, and every inverse w starts and ends with
inverse a. Boundaries with b-only blocks cannot cancel. Consecutive w
symbols of opposite signs would be an adjacent inverse pair in the
abstract word and are excluded; those of equal signs cannot cancel.
Thus the expansion is a nonempty reduced A-word. This checks the
argument at `build/group-actions.tex:69–78` independently.

The exponent sum in a gives a homomorphism chi_A from A to Z. Define
chi_B(j t^n)=chi_A(j); this is a homomorphism because B is a direct product.
The restrictions coincide on J, so the amalgam gives

\[
\chi:\Gamma\to\mathbb Z,\qquad
\chi(a)=1,\quad\chi(b_i)=\chi(t)=0,
\quad\chi(u_i)=i,\quad\chi(w)=100.
\]

There is no requirement that chi vanish on J. In particular,
chi(w)=100 creates no inconsistency with the embedding into B.
See `build/group-actions.tex:126–157`.

Give X_0=[0,1]^Gamma product Lebesgue measure and the right action
(x g)(h)=x(g h). The action law follows from
((x g) k)(h)=x(g k h)=(x(g k))(h). The countable product is standard
Borel, and coordinate permutations preserve the product probability.
For any g different from the identity, a fixed point satisfies
x(g)=x(1). These two independent continuous coordinates agree on a null
set. Countability gives a conull Borel free locus X. It is invariant
because stabilizers are conjugated by translation. Restricting to X
preserves all graphing costs, as checked at
`build/group-actions.tex:94–103,105–124`.

For any positive integer M, let Y_M=X times Z/MZ, give the second
coordinate uniform probability, and act by

\[
(x,r)g=(xg,r+\chi(g)\bmod M).
\]

The homomorphism law gives the right-action law. Each coordinate map
preserves measure, and the first coordinate already makes the product
free. The finite product is standard Borel. All Y_M-orbits are infinite
because Gamma is infinite and the action is free.

## Ergodicity, supplied here as an additional proof

The transformation T:x -> x t on X_0 is mixing. To check this without
assuming a Bernoulli-action theorem, first take cylinder events C,D whose
finite coordinate supports are S,T_0. A translate D t^n depends on one
of the sets t^n T_0 or t^(-n) T_0, depending on the translate convention.
Either convention is sufficient: the intersection with S is empty for
all but finitely many n. Indeed each equality t^n h=k with h,k in the
two finite supports allows at most one n because t has infinite order.
For all sufficiently large n the coordinate families are disjoint, so
the events are independent. Approximation of measurable events in
measure by cylinders proves mixing for all measurable C,D. Passing to
the invariant conull subset X preserves this statement.

Therefore every t-invariant measurable subset of X has measure zero
or one: apply mixing to the subset paired with itself. In particular
the full Gamma-action on X is ergodic.

Now let E be a Gamma-invariant measurable subset of Y_M, modulo null
sets. Since t has height displacement zero, each fiber E_r is
t-invariant modulo a null set, and has measure zero or one. Translation
by a carries height r to height r+1 and preserves the measure of the
fiber, so all fiber measures are equal. Hence E has product measure
zero or one. Thus each Y_M-action is ergodic. This argument also works
for M=1 and every other positive M, not only M>100.

## Upper-cost graphing checked in full

Fix M>100 and 0<p<1. Put

\[
N_p=\{x\in X:x(t^n)\ge p\text{ for all }n\in\mathbb Z\},
\quad
C_p=(\{x:x(1)<p\}\cup N_p)\times\mathbb Z/M\mathbb Z.
\]

Distinct t^n index independent coordinates; the probability of the
first N nonnegative coordinate inequalities is (1-p)^N, so N_p is
null. It is Borel and t-invariant. Thus nu_M(C_p)=p. Every t-orbit meets
C_p: if it never meets the first part, each of its points belongs to
the exceptional second part. This last null correction is legitimate
and ensures exact generation, not only almost-everywhere generation.
See `build/group-actions.tex:177–190`.

Use the full t-map and the 100 generators b_i,w restricted to C_p.
For a generator j of J and any z, choose n with z t^n in C_p. The path

\[
z\longrightarrow zt^n\longrightarrow zt^n j
\longrightarrow zt^n jt^{-n}=zj
\]

is available; j commutes with t in B. Thus the graphing generates R_B
on every point. Every map is a restriction of an element of B, proving
the opposite containment as well. Its cost is exactly 1+100p.
The argument works for w even though w moves height by 100, since
the t-steps preserve whatever height occurs at their endpoints.
See `build/group-actions.tex:192–205`.

Add the a-map on the union of source heights 0 through 98, whose
measure is 99/M because M>100 makes these 99 fibers distinct. The cost
is 1+100p+99/M. Let E denote the generated relation. It already contains
R_B and all a-edges from those 99 source heights.

Suppose E contains all a-edges from source heights k through k+98
modulo M. For z at height k+99, set y=z u_99^(-1), which has height k.
The successive points y u_i are connected using the known a-edge from
height k+i-1 and the unrestricted b_i-edge, for 1<=i<=99. Thus y is
E-equivalent to z. The w-edge connects y to
y w=y u_99 a=z a. Hence z is E-equivalent to z a, supplying the next
source height. This checks `build/group-actions.tex:229–244` pointwise;
no measurable choice is required in this recurrence.

Starting from heights 0 through 98 and taking k=0 through M-100
supplies every remaining height 99 through M-1. The final a-edges
end at height 0 modulo M, as required; there is no missing wraparound
edge. Since a and B generate Gamma, the graphing generates R_Gamma.
For every p>0 its cost is 1+100p+99/M. Taking the infimum and letting
p tend to zero gives

\[
\operatorname{Cost}(R_{Y_M})\le1+99/M.
\]

The argument establishes an infimum bound; it does not assert that
a graphing attains the limiting cost. See
`build/group-actions.tex:218–253`.

As all these orbits are infinite, the usual cost-at-least-one theorem
gives

\[
1\le\operatorname{Cost}(R_{Y_M})\le1+99/M,
\quad\lim_{M\to\infty}\operatorname{Cost}(R_{Y_M})=1.
\]

The manuscript proves the lower bound in
`build/compression.tex:275–286`, and invokes it correctly at
`build/conclusion.tex:40–46`. The compression proof is not needed to
justify the explicit upper-cost graphing. The main project should cite
the classical lower-bound source directly rather than treating this
manuscript as its priority source.

## Boundary and quantifier checks

* M is an arbitrary integer exceeding 100; no divisibility or
  coprimality condition involving 100 is needed.
* The w-map need not fix the height. Its displacement 100 is accounted
  for by the word recurrence and commutation path.
* p is arbitrary in (0,1); the same group/action is used for all p.
  Only the generating graphing changes as p tends to zero.
* The t-marker construction requires t to have infinite order, which
  was established by injectivity of B. It does not presume ergodicity
  or a measurable transversal for the t-relation.
* All the Borel maps in the graphing preserve measure because they are
  restrictions of the already constructed p.m.p. action.
* Pointwise freeness is obtained once, by invariant conull restriction.
  No infinite class or cost assertion depends on the discarded null set.
* The construction does not claim that Gamma has property (T).
* The upper bound survives the strict M>100 condition in the source.
  In fact the same proof works for M=100, but that strengthening is
  unnecessary and was not substituted for the stated theorem.

## Lean and provenance limitations

The catalogue header `lean/formalization.yaml:1–2` says it lists papers
with formalized main results. A search of this catalogue for the exact
manuscript path/title, fixed price, and Gaboriau found no corresponding
entry. No `lean/docs/259.md` exists. `CONTENTS.md:6401–6410` lists family
259 without a Lean link; the immediately following family 260 has one
at line 6417. Searches of ComparatorChallenges and docs found no
relevant fixed-price declaration. Accordingly no machine-verified proof
of this family was identified or relied upon, and no Lean build was run.
This is an absence-of-identified-proof finding, not an assertion that
the repository contains no incidental relevant lemma.

`INPUTS.md:7–10` explicitly warns that the manuscript was developed
from an intermediate source argument and the source record does not
establish that it was the final revision. That warning increases the
importance of the independent lower-bound audit; it does not invalidate
the elementary upper bound checked here.

## Exact remaining dependency and obstruction

There is no unresolved gap in the audited upper-action route. The exact
remaining core dependency is a rigorously established positive cost
gap for R_X. The manuscript states eta=alpha/100 with
K=exp(96) 96^99 / 95^95, 0<alpha<1/200, K alpha^3<1/2 at
`build/introduction.tex:63–80`, but this report has not certified the
finite-model/rank/deployment proof of that claim. It would be invalid
to infer the requested Cost(R_X)>1 from this report alone.

The group-cost infimum equals one by the verified upper sequence and
the aperiodic lower bound. Therefore this construction cannot refute
the equality between group cost and 1 plus the group's first L2-Betti
number. The relation-level claim remains distinct.

## Source integrity

SHA-256 hashes are recorded in `SOURCE_HASHES.json` in this folder.
The pinned Git HEAD was checked before source reads. Review artifacts
were written only in the assigned review folder.
