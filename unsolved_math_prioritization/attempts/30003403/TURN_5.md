# Author turn 5: the PFA construction gate and an exact limit-cut obstruction

**Final author turn: the original PFA question remains unresolved after 5/5 turns.** 2026-10-01.

Turns 3 and 4 produced countable and explicit uncountable quotient targets. This final attempt seeks a mechanism for an arbitrary uncountable A embedded into L=eta_C. It examines a PFA forcing construction rather than assumes the self-similar recursion has a decreasing rank. The negative controls below concern methods, not the original target.

## 1. An exact forcing route to the full target

Fix a nonempty suborder A of L. Let P(L,A) consist of finite monotone partial functions from L to A, ordered by extension (a stronger condition contains the weaker one). Repetitions of values are allowed. For each x in L let

    D_x={p:x belongs to dom(p)},

and for each a in A let

    R_a={p:a belongs to ran(p)}.

Both are dense. To extend at a new x, take the value at the last existing domain point below x if there is one; otherwise take the value at the first existing domain point above x, or any value if the condition is empty. Monotonicity is preserved. To add a new target a to the range, insert a new domain point between all old points whose values are below a and all old points whose values are above a. The relevant finite gap is nonempty because L is dense and has no endpoints. If a already occurs there is nothing to add. This proof does not require A to be dense or endpoint-free.

There are at most aleph1 such dense sets. A filter meeting all of them has a union f:L->A that is total, onto, and monotone: any two pairs in the union occur together in a common stronger condition. Thus, **if P(L,A) is proper, PFA gives the requested epimorphism**. This is a sufficient forcing criterion, not an established properness theorem and not a converse.

## 2. The direct ccc argument fails even for a positive target

Take A=L itself. For each c in the input Countryman order C, let x_c be the eventually-zero sequence with first coordinate c in the positive copy of C, and y_c the analogous sequence with first coordinate c* in the negative copy. If c<d then

    x_c<x_d, but y_c>y_d.

Consequently the singleton conditions p_c={x_c maps to y_c} form an uncountable antichain in P(L,L). Two distinct conditions cannot have a common monotone extension. The finite-conditions poset is not ccc, so the usual MA_(aleph1) argument through ccc cannot be applied.

This persists if a condition specifies that a whole convex finite-prefix cylinder around x_c maps constantly to y_c: the cylinders are ordered like C, and the assigned values like C*. These cylinders have no endpoints. Moreover the mirrored points enter the natural decomposition E(D_xi) at the same stage, so merely matching source and target entrance levels does not remove this particular incompatibility.

None of this disproves properness; proper forcings can have uncountable antichains. None disproves the desired map: for A=L the identity already is an epimorphism. The calculation only rejects a proposed easy proof of the full forcing hypothesis.

## 3. Exact extension criterion at a limit condition

For a monotone map f:S->A from a suborder S of a linear order T and x in T\S, a monotone extension to S union {x} exists exactly when

    {a in A: f(s)<=a for every s<x in S,
             and a<=f(s) for every s>x in S}

is nonempty. Necessity is monotonicity. Sufficiency is obtained by assigning any such a to x. The finite conditions above always have an allowed value, but a union of countably many conditions need not. In a general construction, one must control these cuts in the target as well as the domain.

Here is a countercontrol that retains coinitiality, cofinality, and open fibers. Let

    T = sum_(q in Q) Q,
    S = sum_(q in Q\{0}) Q,
    A = Q,

all with the displayed index coordinate primary. Both S and T have order type Q, and S is coinitial and cofinal in T. Fix an irrational real alpha, say sqrt(2). Choose order isomorphisms

    h_-: Q below 0 -> Q below alpha,
    h_+: Q above 0 -> Q above alpha.

These exist because the four orders are countable, dense, and without endpoints. Their union h is an isomorphism Q\{0}->Q. Define f(q,t)=h(q) on S. It is monotone and onto, and every fiber is a copy of Q, hence has neither endpoint.

For any x in the omitted zero-index fiber of T, all source points with negative index lie below x, and all points with positive index lie above it. An extension value would therefore be a rational number at least every rational below alpha and at most every rational above alpha. No such rational exists. Thus f has no monotone extension to even one point of that middle fiber.

Yet T has order type Q and certainly has a monotone epimorphism onto A. This excludes only the extension of the chosen partial map. It shows that coinitial/cofinal placement and open fibers by themselves do not ensure a coherent limit construction. It is not a counterexample to strong surjectivity, and it is not a proof that P(L,A) is improper.

## 4. Why this does not turn into an intrinsic obstruction

To refute the original target one would need an uncountable A embedded into L for which **every** possible monotone quotient construction fails, equivalently for which every section copy realizes an inadmissible cut. The antichain calculation depends on deliberately reversed assignments, and the rational example deliberately chooses an unrealized target cut. Both have other successful maps. They therefore cannot serve as intrinsic obstructions.

Conversely, the PFA route requires a proof of properness, perhaps with additional promises that prevent such bad limits. Merely appending the requirement that every future domain cut admit an extension value would transfer the original section problem into the definition of conditions; no density/properness proof for that stronger forcing is supplied. The known Countryman forcing theorems use comparability and stationary-endpoint hypotheses that have not been established for this universal non-Countryman domain.

The fragmented rank theorem remains a valid credited source of well-founded induction for fragmented targets with normal input C. It does not rank arbitrary nonfragmented targets. The self-similar fibers of eta_C supply no decreasing substitute, and no new well-founded decomposition of all Aronszajn targets was obtained in this final turn.

## Final author disposition

The full assertion under PFA is unproved and unrefuted in this packet. All five substantive author turns are now used. Retained conclusions are the structural normality proof, the exact section/cut criterion, the ZFC quotient onto every countable target, and the finite-prefix lifting rule for explicit nonfragmented targets, with additional normal-input/axiom hypotheses where stated. The last turn supplies a precise forcing gate and two method countercontrols. It supplies no sixth search turn or hidden full-solution claim.

Status: original unsolved, 5/5. Completion estimate toward the original assertion: 30%. Independent full order-theoretic review is required before any PR or promotion.
