# A finite algebraic consistency test at any number of maturities

**30003427 / OWR-15218-003. Author turn 1/5. Algorithmic classical-consequence
candidate; independent review pending.**

## 1. Outcome and scope

For every fixed finite set of quoted European calls at finitely many dates,
we give a finite polynomial feasibility system exactly equivalent to the
source definition of epsilon consistency. The number of variables has an
explicit bound depending only on the number of dates and quotes, not on an
unknown model. Applying classical real quantifier elimination produces a
finite Boolean combination of polynomial sign conditions in the quoted
data and epsilon alone. Thus this is an algorithmic necessary-and-sufficient
characterization, not an infinite-dimensional condition with unknown laws.

For rational or real-algebraic quoted data the procedure terminates and
computes the entire admissible epsilon set as finitely many intervals and
points with real-algebraic endpoints. It returns its least admissible value
when one exists, or reports emptiness or a nonattained infimum. Strict
positivity in the source makes the last alternative necessary; Section 6
gives an exact two-maturity example. For arbitrary real data the same
quantifier-free formula is a formal semialgebraic characterization. We do
not claim a Turing algorithm that reads unspecified noncomputable reals.

This answers the literal finite-data characterization and smallest-bound
request in an algorithmic sense. It does not supply short recognizable
calendar inequalities, an efficient computational method, an arbitrage
classification, or the source's separate conjecture about particular
calendar-vertical baskets. These are distinct stronger objectives.
Conditional Carathéodory compression and real quantifier elimination are
classical inputs; no novelty or priority claim is made.

## 2. Exact model in discounted coordinates

Use dates t=0,...,T, T>=1, a positive deterministic bank account B(t), and
q=sum_t N_t quoted calls. Let k_(t,i)=K_(t,i)/B(t)>0 be the discounted
strikes. At time zero the calls have bid/ask intervals [b_(t,i),a_(t,i)]
and the stock has interval [s_b,s_a], with 0<s_b<=s_a. The input convention
is 0<b_(t,i)<=a_(t,i) and increasing strikes at each date; invalid input
can be rejected by these polynomial conditions. The equality of a bid and
ask is allowed.

The source model is a finite filtered probability space. Let R_t be the
discounted cash-settlement reference price, and Z_t the discounted shadow
price. Definitions 2.1, 2.2 and 2.4 of Gerhold–Gülüm are equivalent to:

    epsilon>=0,  s_a−s_b<=epsilon,
    s_b<=Z_0<=s_a,
    R_t>0, Z_t>0, R_t>=epsilon, |R_t−Z_t|<=epsilon (t>=1),  (1)
    (Z_t) is a martingale,
    b_(t,i)<=E[(R_t−k_(t,i))^+]<=a_(t,i).                  (2)

All processes are adapted. The first line includes the initial spread.
The equivalence does not replace R by a martingale or midpoint: given
R,Z one takes the discounted stock bid min(R,Z) and ask max(R,Z) at
positive times. They are strictly positive, contain both processes, and
have width at most epsilon. Conversely two points in such a stock spread
satisfy (1). Rescaling by B(t) restores the source's undiscounted model.
Cash settlement discounted to time zero is exactly (R_t−k_(t,i))^+.

The source puts no physical measure in the data. The probability law is
part of the model to be found. If its initial sigma field is nontrivial,
replace it by the trivial sigma field and put Z_0=E Z_1. The deterministic
initial interval is convex, so the new Z_0 is still in it. The martingale
property at later times and all payoffs are unchanged. We can therefore
use a deterministic root without loss.

Some explicit inequalities in the source are stated only for
`epsilon<min_(t,i) k_(t,i)`. That inequality is not part of Definition 2.4.
Our system works without it; to work in that commonly used restricted
range, simply adjoin it to the system and to the output set.

## 3. Uniform finite-tree bound, with auxiliary reference prices retained

**Lemma.** If a source-consistent finite model exists, one exists on a
rooted tree of depth T with at most b=q+2 children at every nonterminal
node. It can be represented on the full b-ary tree with strictly positive
conditional probabilities. In particular it has at most b^T terminal atoms
before harmless duplicate labels are inserted or identified.

**Proof.** Remove zero-probability atoms from a given finite model and
represent its filtration by its finite tree of positive-probability atoms.
Write C_1,...,C_q for all the discounted terminally recorded call payoffs;
a payoff at an earlier maturity is held unchanged as a random variable
through date T. At each original node u let

    V(u)=(E[C_1|u],...,E[C_q|u]).

At a node u at date t<T, each child w has a shadow value Z(w) and a vector
V(w). Its original conditional probabilities express

    (Z(u), V(u))

as a convex combination of the finitely many vectors `(Z(w),V(w))` in
R^(q+1). Carathéodory's finite-dimensional theorem preserves that barycenter
using at most q+2 of these actual children and nonnegative weights. Discard
any zero weights. Do this at the root and recursively at every retained
node, always using that node's original children and conditional vector.
The depth is finite.

Every local selected barycenter preserves the shadow martingale equation.
All selected nodes retain their original R and Z, so strict positivity,
reference lower bounds, spread constraints, and every pathwise condition
in (1) persist. At a leaf, V equals the full actual payoff vector, including
payoffs from its history. Backward induction shows that conditional payoff
expectations under the new tree are V(u) at every retained node. In
particular all q unconditional expectations are preserved exactly and
remain in their quote intervals. This proves the bound.

If a node has fewer than b children, duplicate one or more of its chosen
children together with their continuation subtrees, splitting each original
positive weight into positive pieces. This fills exactly b children without
changing any price or conditional expectation. Finite extra labels are
allowed in the filtration in the source definition. The resulting full tree
has b^T leaves. Conversely every such tree is itself a permitted finite
filtered model. ∎

This is the standard conditional Carathéodory/martingale Tchakaloff
mechanism. Compare Beiglböck–Nutz, Theorem 5.1, with support bound
(n+k+1)^T. Their theorem is stated for a martingale's path and observable
functions thereof; rather than misidentifying an arbitrary adapted reference
price with a function of the shadow path, the proof above carries the
original filtration and reference values explicitly. No infinite-support
extension or compactness theorem is needed because the original problem
already assumes finite probability spaces.

## 4. An explicit finite polynomial system

Let b=q+2. The nodes at level t are words u in {1,...,b}^t. The root is
empty. For each nonterminal node u and child uj use a variable p_(u,j).
For every node use a weight w_u and a shadow value z_u. For each nonroot
node at level t use a reference value r_u and N_t payoff variables c_(u,i).
The following finite list, denoted F_D(epsilon), is the feasibility system:

1. epsilon>=0, s_a−s_b<=epsilon, s_b<=z_empty<=s_a,
   w_empty=1.
2. At every nonterminal u:

       p_(u,j)>0 (j=1,...,b),
       sum_j p_(u,j)=1,
       w_(uj)=w_u p_(u,j),
       z_u=sum_j p_(u,j) z_(uj).

3. At every nonroot u:

       r_u>0, z_u>0, r_u>=epsilon,
       −epsilon<=r_u−z_u<=epsilon.

4. At every level-t node u and every call i there:

       c_(u,i)>=0,
       c_(u,i)>=r_u−k_(t,i),
       c_(u,i)(c_(u,i)−r_u+k_(t,i))=0.

5. At each quoted date t and strike i:

       b_(t,i)<=sum_(|u|=t) w_u c_(u,i)<=a_(t,i).

All expressions have degree at most two in the model variables and input
parameters after discounting. The third constraint in item 4, together with
the first two, is exactly `c=(r−k)^+`; it has no spurious negative or
incorrect branch. The weights are positive products of normalized positive
conditional probabilities, so they sum to one at each level automatically.
No free signed measure is being introduced.

**Theorem.** The source data D are epsilon-consistent if and only if the
finite polynomial system F_D(epsilon) has a real solution.

**Proof.** Necessity follows by the lemma, full-tree padding and taking its
actual node values, probabilities, weights and call payoffs. For sufficiency,
let the leaves of the full tree be the finite probability space, with leaf
probabilities w_u. The history filtration has the specified conditional
probabilities p. Node values define adapted r,z; item 2 is precisely the
martingale property. Items 3–5 give the required support, spread and call
constraints. Section 2 reconstructs the strictly positive bid/ask processes
and the original bank-account units. The time-zero stock spread and shadow
value are enforced in item 1. ∎

In particular every date is coupled to all the others by the same tree and
martingale. This is not a collection of independent one-maturity tests.
There are at most (b^(T+1)−1)/(b−1) nodes, so even the number of existential
variables is explicit before any model is known.

## 5. Quote-only characterization and smallest-bound algorithm

Treat D and epsilon as free variables, with all the finitely many tree
variables existentially quantified. By effective real quantifier elimination
(Tarski–Seidenberg), compute a quantifier-free Boolean formula

    Psi_(T,N_1,...,N_T)(D,epsilon)

in polynomial sign conditions that is equivalent over the reals to
`exists tree variables F_D(epsilon)`. This is a finite recipe for necessary
and sufficient conditions in the quoted data alone. It does not leave
unspecified measures, support sizes or processes to quantify over. The
formula can be compiled once for a fixed quote shape, or data may be
substituted before elimination. Classical cylindrical algebraic decomposition
or the effective algorithm in Basu's survey, Section 2.1, provides such a
procedure. No new quantifier-elimination algorithm is claimed here.

For exact rational or real-algebraic data:

(a) Build the explicitly bounded tree formula above.
(b) Eliminate all tree variables over the real closed field of real
    algebraic numbers, leaving the one variable epsilon.
(c) Isolate the real roots of the finitely many nonzero output polynomials,
    include zero as a boundary, and test the formula on each intervening
    interval and each root. Polynomials that specialize identically to zero
    are handled by their constant sign. This gives the full set

       E_D={epsilon>=0: Psi(D,epsilon)}

    as a finite union of intervals and points with their exact endpoint
    inclusion flags. Unbounded intervals are allowed.
(d) If E_D is empty, report that no admissible bound exists. Otherwise its
    infimum e_* is the leftmost endpoint. Test Psi(D,e_*). If true, e_* is
    the smallest admissible epsilon; if false, no smallest exists and e_*
    is the exact nonattained infimum. If desired, algebraic sample points in
    a nonempty fiber give an explicit finite model by the preceding theorem.

A nonempty E_D is bounded below by zero, so its infimum is finite. Endpoints
are real-algebraic for algebraic inputs. We do not assume E_D is closed or
monotone in epsilon: increasing epsilon also strengthens R_t>=epsilon.
The optional source range epsilon<min k can be intersected at step (b).
Strict inequalities in all of these steps are preserved, not replaced by
closed constraints.

For arbitrary real input data, Psi remains a valid finite formula in those
real parameters, and E_D is semialgebraic over their generated coefficient
field. This is a mathematical characterization, not a claim of finite-bit
computation on an unspecified noncomputable real input. The terminating
exact algorithm is stated only for effectively represented algebraic data
(or a real-arithmetic model with the required exact sign oracle).

The procedure can be extremely expensive. Neither the tree bound nor the
quantifier-elimination claim certifies practicality or a short hand-written
list of calendar inequalities. Those aspirations are not used to overstate
the result.

## 6. The smallest admissible bound need not be attained

This example uses two positive quoted dates, 1 and 2, B(t)=1 and an initial
stock quote [1,1]. At both dates quote the following exact calls:

    strikes:   1/4, 1/2, 3/4;
    bid=ask:  13/16, 5/8, 7/16.

For every 0<epsilon<1/4 there is a two-state consistent model, constant
between dates 1 and 2. Give the low state probability 1/4 and high state
probability 3/4. At each positive date set

    reference R_low=epsilon,       R_high=4/3;
    shadow    Z_low=epsilon,       Z_high=4/3−epsilon/3.

The shadow has mean one and is constant after date 1, hence is a martingale
from z_0=1. Both reference and shadow are strictly positive. Each reference
is at least epsilon, and the only nonzero difference is epsilon/3 at the
high state. Their min/max define an admissible stock spread, with initial
width zero. Every low-state call pays zero; the high-state expected call
payoff is (3/4)(4/3−k)=1−3k/4, exactly the quoted prices.

At epsilon=0, any model would have R_t=Z_t>0 and E R_t=1. Fix either quoted
date and call the resulting random variable X. The call price at 1/2 is
the arithmetic average of those at 1/4 and 3/4. The nonnegative butterfly
payoff

    (X−1/4)^+−2(X−1/2)^++(X−3/4)^+

is strictly positive on (1/4,3/4), and its expected value is zero. Hence
X has no mass in that open interval. The difference of the first and third
call values then gives

    P(X>=3/4)=(13/16−7/16)/(3/4−1/4)=3/4.

The expected value on that upper set is

    E[X 1_(X>=3/4)] = 7/16+(3/4)(3/4)=1.

The complementary event has probability 1/4, but must have expected X-value
zero because E X=1. This contradicts strict positivity of X. Atoms at the
two interval endpoints are included correctly in this argument.

Thus E_D contains (0,1/4) but not 0, and its infimum is zero with no minimum.
This is an attainment qualification under the literal strict-positive model,
not an intertemporal arbitrage theorem or a claim about a nonnegative-stock
variant. The exact two-date panel is used only to show why the algorithm
must distinguish a minimum from an infimum; the theorem above covers general
panels with arbitrary option bid–ask widths and arbitrary finite T.

## 7. Validation and attribution

The proof is a direct finite-model reduction plus two classical mathematical
methods. Gerhold–Gülüm retain full credit for the model, the one-maturity
result and peacock formulations. Beiglböck–Nutz and classical Carathéodory
supply the finite-compression context; Tarski–Seidenberg and standard real
algebraic algorithms supply elimination. The recent Lee two-date results
are distinct prior context and are not assumed to prove any step here.

The exact checker tests finite-tree barycenter preservation, polynomial
encoding and the nonattained-bound example. It does not run a general CAD
solver and does not substitute finite tests for the proof. Independent
review must decide both mathematical correctness and whether the literal
source target warrants an algorithmic/classical-consequence disposition.
