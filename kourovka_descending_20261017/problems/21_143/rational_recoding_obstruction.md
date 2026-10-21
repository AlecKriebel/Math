# Finite-state repair of the Guba–Sapir language

2026-10-17. Research note for Kourovka 21.143. This is an encoding-specific
partial deduction, not a resolution or an audited originality claim.
Discovery estimate: 8%. Author metadata: Alec Kriebel,
https://orcid.org/0009-0001-9320-500X.

## Precise scope

Let A={x,X,y,Y} be the standard symmetric generators of F, with x=x0 and
y=x1. Evaluation is ordinary multiplication, and the Cayley metric is
left invariant. Let N be the regular unique Guba–Sapir language described
in approach_constructive.md. A rational relation means a relation
recognized by a finite two-tape transducer; epsilon moves and finite word
labels are allowed. This is different from synchronously regular padded
relations. Rational relations are closed under inverse and composition.

Claim: there is no finite-state rational recoding, defined on every word
of N and preserving the represented element, from N into ANY presentation
whose generator multipliers are rational. This includes classical
automatic structures and graph automatic presentations. It does not
exclude a new presentation related to N by a nonrational procedure.

## Lemma 1: a rational multiplier forces asynchronous fellow travelling

For a finitely generated group G and fixed s in G, suppose

    T subset A* x A*,    eval(u)s=eval(v) for every (u,v) in T,

and T is rational. Then there is K such that the generator paths of every
accepted pair admit an asynchronous K-fellow-traveller matching. Paths
are parameterized continuously on their lengths, extended constantly at
their ends, and matching clocks are nondecreasing and onto their path
intervals; pauses are allowed.

Proof. Trim the transducer to successful paths. At each coaccessible
state q choose one accepting suffix, with input/output labels (a_q,b_q).
If a successful prefix with labels (p,r) reaches q, its concatenation
with this suffix is accepted, so

    eval(p) eval(a_q) s = eval(r) eval(b_q),
    eval(p)^-1 eval(r) = eval(a_q) s eval(b_q)^-1.

Thus the two prefix endpoints are at distance at most
C=max_q(|a_q|+|s|_A+|b_q|). If transitions have multi-letter labels, let B
be the maximum sum of the lengths of their two labels. Follow each
transition on its two paths, one tape at a time if needed. During it,
distance is at most C+B. The resulting finite monotone lattice matching
visits every letter on both tapes. Linear interpolation, allowing pauses,
gives the asserted continuous clocks. Epsilon/epsilon transitions can be
removed from the parameterization. Terminal padding is constant. QED.

No finite-fiber assumption is used. The multiplier relation need not be
functional. The bound is on paths in the input generator alphabet, not
on the interpretation of arbitrary symbol encodings.

## Lemma 2: the y-multiplier of N is not rational

For n>=1 use the two N-words

    u_n = y x^n,
    v_n = x^n y X^(n+1) y x^(n+1).

Both words avoid the forbidden subwords defining N. They satisfy
eval(u_n)y=eval(v_n). The constructive note proves this for all n:
a_n=x^n y X^(n+1) is supported on [0,2^-n] and commutes with y, whose
support is [1/2,1], giving the equality. The exact PL checker separately
reproduces it for n=1,...,64; the finite check does not replace this proof.

Pass to the exponent-sum quotient F -> Z^2, equipped with l1 distance.
It does not increase distance. The quotient path of u_n has nondecreasing
x-coordinate and y-coordinate in [0,1]. The v_n path visits (n,0) and
then (-1,2), in that order. In an asynchronous matching with bound K,
let a and b be the corresponding x-coordinates on u_n. Then

    a >= n-K,    b >= a,
    K >= |b+1| + |2-y_coordinate| >= b+2 >= n-K+2.

Here b>=0, since the entire u_n path has nonnegative x-coordinate.
Consequently 2K>=n+2. This holds for continuous clocks and arbitrary
pauses, since a nondecreasing onto clock reaches both specified vertices
in order. There is no uniform asynchronous bound. Lemma 1 now shows that

    M_y(N)={(u,v) in N x N : eval(u)y=eval(v)}

is not rational. In particular it is not synchronously regular.

## Proposition: rational recoding cannot repair N

Suppose L is a language over a finite symbol alphabet B, with an
interpretation nu:L->F. We do not assume that nu is letterwise evaluation
or even injective. Suppose its full y-multiplier relation

    M_y(L)={(p,q) in L x L : nu(p)y=nu(q)}

is rational. If a rational relation R subset N x L has domain N and
preserves represented elements, meaning eval(u)=nu(p) whenever (u,p) is
in R, then relational composition gives

    R ; M_y(L) ; R^-1 = M_y(N).

The forward inclusion follows from preservation. For the reverse
inclusion, choose any R-output for each of u and v; totality supplies
them, and the FULL multiplier relation contains that output pair.
Rational relations are closed under composition and inverse, so this
would make M_y(N) rational, contradicting Lemma 2. QED.

This algebraic composition proof avoids any implicit composition of
asynchronous clocks. It also explains why the statement applies to
graph automatic encodings: output symbols need not be group generators.
If a transducer has a larger domain, intersect its input with regular N
first. If it is only a partial or heuristic normalizer, the totality
hypothesis is absent and the proposition says nothing.

## What is and is not blocked

Finite-state substitutions, finite-state padding/removal rules and any
other evaluation-preserving rational normalization of the complete GS
language cannot produce automatic multipliers. A proposed conversion of
all of N must therefore be nonrational, or a construction must start from
a language not connected to N by such a transduction. Neither alternative
has been excluded. Unbounded iteration of bounded local rewrite steps
need not define a rational transduction; the proposition does not exclude
such algorithms merely because their individual steps are bounded.
Arbitrary computable normal-form algorithms are not finite-state
transducers, and their existence would not contradict the proposition.

This is not a negative solution of 21.143. It does not exclude all regular
languages or all possible normal-form algorithms. No publication is
authorized by this partial deduction.

## Separate wreath and higher-filling approaches attempted by root

An embedded restricted wreath product Z wr Z is not automatic, since it
is not finitely presented. But automatic groups need not pass automaticity
to arbitrary finitely generated subgroups. Restricting a hypothetical
automatic language for F to a wreath subgroup is unjustified: no regularity
or combing-convexity of that restriction has been shown. A homomorphic
retraction cannot supply the missing projection: every homomorphism from F
to a solvable group kills the simple nonabelian F', and hence has abelian
image. A retraction onto nonabelian Z wr Z would contradict this.
The support-based idea needs an actual coarse confinement theorem for
arbitrary automatic paths; that theorem remains unsupported. Route blocked.

Higher filling could in principle give a presentation-independent
obstruction, but infinite-dimensional flats alone give Euclidean lower
bounds, compatible with combing upper bounds. No controlled projection
from F onto a badly filling subgroup or super-Euclidean filling lower
bound was obtained. Replacing this gap by a claim of inherited subgroup
filling would be invalid. Route remains open without decisive evidence.

## Review and remaining gap

Two independent approach agents checked the original evaluation-preserving
recoding argument using accepting suffixes and asynchronous clock
refinement. A fresh reviewer independently passed this stronger relational
composition version, including its graph-automatic scope, after two scope
sentences were tightened; see reviews/partial_adversary01.md. Formal proof
assistant verification and independent human review are not claimed.
The exact remaining question is unchanged: construct a full regular
automatic structure for F, or give a proof excluding EVERY such structure.
