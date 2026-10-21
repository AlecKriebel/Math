# Constructive automaticity investigation for Thompson's F

Author metadata: Alec Kriebel, https://orcid.org/0009-0001-9320-500X.

## Scope and exact success criterion

This is a constructive route for Kourovka 21.143, independently investigating
normal forms and encodings. The target is the usual finite dyadic
piecewise-linear Thompson group F, with a finite inverse-closed generating
alphabet A. A solution must exhibit a regular language L in A*, surjecting
onto F, with synchronously regular padded relations

    M_a = {(u,v) in L x L : evaluation(u) a = evaluation(v)}

for every a in A union {1}. Equivalently, a regular combing must have one
uniform synchronous fellow-traveller constant for every pair of adjacent
endpoints, and for equal endpoints if representatives are not unique.
One may seek unique representatives, making M_1 diagonal. A symbol encoding
not evaluated letterwise in the fixed finite generators is not already this
structure. Counter automata and tree automata are also insufficient.

Failure of a named normal form is not a negative answer to 21.143. No
resolution or novelty is claimed here.

## Research log

- 2026-10-17 21:07:47 UTC — Initial primary-source inspection and independent
  family selection. Discovery estimate: **5%**. Three families are being
  distinguished: regular finite-generator Guba–Sapir normal forms; regular
  index/exponent encodings; tree/caret/forest encodings. A child audit is
  independently investigating the third family. The first family already
  has a direct parametric obstruction, below; proof and exact arithmetic
  checks are in progress.
- 2026-10-17 21:09:15 UTC — Exact PL computations passed for n=1,...,64
  in both the Guba–Sapir and unary-index obstruction families, and for
  x_i, i=1,...,64. Also passed: 8,188 exact generator/point depth checks
  and all 1,365 words of length at most five. Discovery estimate: **7%**.
  The first check detected an initially reversed composition convention;
  it was corrected, and both standard finite presentation relators now
  independently pass. No uncorrected discrepancy remains. These checks
  certify formulas on the stated finite ranges; universal proofs below
  carry the unbounded claims. Adversarial review requested.
- 2026-10-17 21:13:28 UTC — Assigned constructive investigation completed.
  Discovery estimate: **7%**; completion of this finite route audit:
  **100%**. The base Guba–Sapir obstruction passed independent adversarial
  review; the separate tree audit and its recurrence passed two independent
  checks. Both reproduction programs passed. A fresh root-level audit was
  asked to additionally check the exact quotient matching formula and
  binary-index rational-decoder barrier before their promotion. Local
  binary and zipped repairs are preserved as partial mechanisms, with
  exact inter-block/first-return gaps. No full automatic structure or
  encoding-independent nonautomaticity proof was found.

## Family A: regular finite-generator rewriting normal forms

Use x=x_0, y=x_1 and capital letters for inverses. The Guba–Sapir normal
language N consists of freely reduced words avoiding y^epsilon x^i y and
y^epsilon x^(i+1) Y for epsilon in {1,-1}, i>=1. It is regular, and is a
unique normal form language for F. Corwin–Golan–Hermiller–Johnson–Šunić,
Section 2.2, records the convergent system and the same N; their bounded
regular convergent *prefix* system proves autostackability, a weaker
property. Source: https://arxiv.org/abs/1811.11691.

For n>=1, consider

    u_n = y x^n,
    v_n = x^n y X^(n+1) y x^(n+1).

Both belong to N, and the y-rule gives u_n y =_F v_n. Their lengths are
n+1 and 3n+4, respectively: the length gap is 2n+3.

The group equality can also be checked without assuming the infinite
rewriting rule. Use the PL generators with x having vertices
(0,0),(1/2,1/4),(3/4,1/2),(1,1), and y having vertices
(0,0),(1/2,1/2),(3/4,5/8),(7/8,3/4),(1,1); products mean composition
f_(uv)=f_u after f_v. The closed support of a_1=x y X^2 is [0,1/2], and
a_n=x^(n-1) a_1 X^(n-1) has closed support [0,2^-n]. Thus a_n commutes with y,
whose closed support is [1/2,1], including n=1 because both maps fix 1/2.
Consequently

    v_n = a_n y x^(n+1) = y a_n x^(n+1) = y x^n y.

This proves the equality for every n>=1 directly from the PL model.

**Finite-fiber length-gap lemma.** If a synchronously regular relation R
between two word languages has finite fibers in both coordinate directions,
then its accepted pairs have uniformly bounded length difference. Indeed,
let a finite automaton have q states. If one word continues for at least q
letters after the other ends, an accepting path repeats a state in that
one-tape tail. Pumping the resulting cycle leaves the shorter word fixed
and produces infinitely many longer partners. This contradicts finiteness
of that fiber. The same argument applies to a nondeterministic automaton
by fixing an accepting path.

Since N is unique, M_y restricted to N has one-element fibers in each
direction. The displayed family and lemma prove that **M_y on N is not
synchronously regular**. This is a language-specific obstruction.

There is a separate geometric certificate. Map the free generators to the
standard basis of Z^2; the defining relators have zero exponent sums, so
this gives a quotient map F -> Z^2 that does not increase the l1 metric.
At time t=2n+3, the completed u_n path has coordinates (n,1), while the
prefix of v_n has coordinates (-1,2). Their Cayley distance is therefore
at least n+2. Consequently N has no uniform synchronous fellow-traveller
constant. This lower bound uses only a quotient metric, not an unvalidated
geodesic-length implementation.

The same family even defeats bounded asynchronous fellow travelling of
these paths. In any monotone pairing of the paths, inspect the points
(n,0), then (-1,2), visited in that order by v_n in the abelian quotient.
If a K-close pairing exists, the paired point of u_n at the first time
has x-coordinate at least n-K. The x-coordinate on u_n is nondecreasing,
so its paired point at the second time has coordinate b>=n-K. Since
b>=0 and its y-coordinate is either zero or one, its l1 distance from
(-1,2) is at least b+2. Hence K>=n-K+2, so K>=(n+2)/2. This argument
also works for continuous monotone reparametrizations: the y-coordinate
on u_n lies in [0,1]. This statement concerns the displayed paths, not
every possible asynchronous structure for F.

For completeness, the exact *discrete l1-quotient* monotone matching
distance is 2 for n=1,2, and ceil((n+3)/2) for n>=3. This does not assert
the exact Cayley-graph distance. The lower bound 2 follows from the point
(-1,2). If K<n, matching the earlier point (n,0) forces positive
x-coordinate on u_n, hence y-coordinate exactly one there. Writing that
x-coordinate as a and the later one as b>=a gives

    K >= n-a+1,       K >= b+2 >= a+2,

so 2K>=n+3. If K>=n, that alternative itself is a lower bound. Together
these give max(2,min(n,ceil((n+3)/2))). To obtain the corresponding upper
bound n when n>=2, keep u at the origin while v goes to (n,0), move both
up one unit, then keep u at (0,1) during v's return to (-1,2); advance u
along its horizontal segment as v subsequently travels to (n,2). The
maximum distance is n. The second upper bound is obtained by first moving
u up to (0,1), then horizontally to an integer a closest to (n-1)/2 while
v first moves horizontally; hold u there through v's excursion to
(-1,2), then finish the two horizontal segments together. Its maximum
distance is max(n-a+1,a+2)=ceil((n+3)/2). For n=1 this second construction
has distance two. The two upper bounds and the lower bounds prove the
formula, which is also checked by a separate finite dynamic program for
n=1,...,20.

Status: universal proof and exact finite computations completed;
an independent adversarial review by the obstruction-route agent passed
the normal-form membership, equality, finite-fiber pumping, and synchronous
and asynchronous lower bounds. The direct route using N is
**blocked**. Reopening requires a
materially different normal-form language, not just a faster normalizer.

## Family B: index/exponent encodings

Elder–Taback construct a regular symbol language L_infinity over {a,b,#}
and a deterministic nonblind one-counter graph automatic structure. Their
Lemma 3.7 proves that this particular representation is not graph
automatic: multiplication by x_1^-1 requires unbounded counting. Source:
https://arxiv.org/abs/1501.04313, Lemmas 3.1 and 3.7, Theorem 3.6.

An independent length-gap proof uses the adjacent pair

    b^n  ->  b^n #^(n+1) b,

representing x_0^-n and x_(n+1)^-1 x_0^-n = x_0^-n x_1^-1,
respectively. The symbol-length gap is n+2. Since this symbol normal form
is unique, the finite-fiber length-gap lemma again excludes a synchronous
regular multiplier on this representation. Exact PL verification passed
for n=1,...,64. These symbol words are not ordinary generator words,
even though their lengths are controlled in a metric sense.

### Binary compression: finite-state decoding barrier

Replacing unary indices by binary indices can make incrementing an index
finite-state in a suitable digit order. That observation alone does not
produce classical automaticity. Here is an explicit barrier to decoding
such compressed strings into generator words by a rational relation.

For a dyadic rational t in (0,1), let depth(t) be the exponent d in its
reduced denominator 2^d. Each of x,X,y,Y satisfies

    depth(a(t)) <= depth(t)+1.

This follows directly on their finitely many linear pieces; the low-depth
endpoints also satisfy the bound. Every generator has breakpoint depth at
most three. Since breakpoints of f after g lie among breakpoints of g and
g^-1 applied to breakpoints of f, induction gives

    maximum breakpoint depth(evaluation(w)) <= |w|+2.

Now x_i=X^(i-1) y x^(i-1), i>=1, has its deepest breakpoint at
1-2^-(i+2), with a genuine slope change. Thus every generator word
representing x_i has length at least i. This is an elementary lower bound,
not an assertion of the exact geodesic length of x_i.

A rational transduction has the following short-witness property: for
every input in its domain there is an accepted output of length at most
C|input|+D, for fixed constants C,D. Normalize input transition labels to
single letters or epsilon. Delete every input-epsilon cycle from an
accepting path. The path is still accepting with the same input; it has
at most |input| input-consuming transitions, with boundedly many
epsilon transitions between them, so its output length is linear. If the
relation is semantically correct, the shortened output remains a correct
representative. Applying this to a binary encoding of x_i, whose input
length is O(log i), contradicts the lower bound i. Therefore **a binary
index encoding of this kind admits no total, semantically correct
finite-state decoder relation to ordinary generator representatives**.
In particular it admits no single-valued rational decoder. This does not
assume that all accepting paths have short output; only one short witness
per input is needed.
The same issue for binary powers x_0^m follows more immediately from
abelianization. This excludes a particular finite-state conversion route;
it neither decides graph automaticity nor excludes another uncompressed
automatic combing.

### A local repair that does not yet globalize

Interleaving the b and # runs can repair the one displayed unary witness:
represent b^n by (b#)^n and b^n #^(n+1)b by (b#)^n #b. This motivates
encoding an index relative to cumulative negative exponents, as in a
forest frontier. However, on a general standard negative word the new
x_1^-1 travels past every negative letter whose index lies before its
current insertion position, and every such crossing increases that
position. Its stopping condition compares an index to an unbounded
cumulative exponent count. No global regular domain plus all regular
multiplier relations has been constructed for the proposed interleaving.
Merely asking for such a regular encoding restates the missing part of
the problem. Status: **blocked pending a genuinely new global mechanism**.

## Family C: tree/caret/forest encodings

The independent audit is in [tree_language_audit.md](tree_language_audit.md),
with its own proofs and checks. It gives encoding-specific obstructions:

1. Separated preorder codes p(T)#p(S) of reduced equal-leaf-count tree
   pairs are nonregular. Opposite combs isolate the sublanguage
   1^n 0^(n+1)#(10)^n0, n>=2.
2. Synchronously paired preorder codes remain nonregular. Writing
   A=(1,1), B=(1,0), C=(0,1), D=(0,0), intersection with
   (AB)^+(CD)^+D gives {(AB)^k(CD)^kD:k>=1}.
3. No regular decoration or encoding can decode exactly onto either of
   those domains by a finite-state transduction, since such transductions
   preserve regular languages.
4. The naive ranked-tree language Pair(T,S) also fails regular tree
   recognition: a finite automaton cannot compare arbitrary equal leaf
   counts in two separate branches. Opposite combs give a direct
   state-repetition contradiction.

These are stronger than saying that one tree's parentheses need a stack:
the witnesses remain inside reduced equal-size pairs. They are still
specific to the chosen decoding maps and do not disprove an arbitrary
automatic structure. The independent script checked 203,456 pairs through
seven carets, and the proof covers all sizes.

Published caret-type strings supply a three-counter graph automatic
structure, not the needed finite-state structure; that particular domain
is not context-free. Source: Taback–Younes,
https://arxiv.org/abs/1501.04315. Forest generators can have local geometric
effects, but linear serialization must still validate arbitrarily nested
components and identify the correct frontier. Proving those global tests
regular would be substantive new work, not a consequence of local caret
changes.

The interleaving idea above has a precise first-return cost. If s_i counts
negative generators at index i, an appended x_1^-1 has frontier height

    H_i = 1 + sum_(j<i) s_j - i,
    H_(i+1) = H_i + s_i - 1,

and inserts/combines at the first i with H_i=0. The exact slot-prefix
language for this first return is nonregular: intersection with b*#*
gives {b^n#^(n+1):n>=0}. A local zip of one comb family does not provide
a globally recoverable regular encoding of all such degree sequences.
See the independent audit for the crossing derivation and bounded checks.

Status: these direct serialized-tree and naive separate-tree routes are
**blocked**. A shared alignment skeleton, a non-finite-state decoding, or
a different group-word combing would be a genuinely different route; no
complete instance with all required automata is supplied.

## Family D: bounded regular prefix normalization

The autostackable construction gives regular tests for bounded local
prefix rewrites. This is useful algorithmic structure. It does not make
the relation obtained after arbitrarily many rewrites regular. In the
Guba–Sapir example above, the input u_n y has length n+2 and its normal
form v_n has length 3n+4. Thus normalization increases length by 2n+2.
Any rewrite calculus whose individual step increases length by at most B
requires at least (2n+2)/B steps on this family. No fixed bound on the
number of such stages can produce all right-generator multipliers.
Equivalently, a fixed number of bounded changes cannot repair the
unbounded adjacent normal-form length gaps. Status: **blocked as a
finite-stage compilation**; the published unbounded convergent procedure
remains valid but does not supply automaticity.

## Reproduction and remaining gap

Run `python3 constructive_checks.py` from this folder. The standalone
standard-library program writes `constructive_check_results.json`.
It checks the generator inverse identities, two finite presentation
relators, both adjacent-pair families, the dyadic breakpoint formula,
and an exhaustive short-word depth bound. The PL composition and all
comparisons use rational arithmetic. An optional finite dynamic program
also records exact discrete asynchronous distances in the l1 quotient;
these are lower bounds for Cayley distances, not exact word distances.
Finite checks can validate formulas and conventions; the parametric proofs
must supply the universal quantifiers. The remaining global gap is a new
regular finite-generator combing with a uniform fellow-traveller constant,
or an invariant obstruction applying to every such combing. Neither is
supplied here.

The strongest verified conclusion is a collection of exact barriers for
the named constructive families, with an explicit unbounded geometric
failure even for asynchronous fellow travelling of the Guba–Sapir paths.
None is a universal obstruction to F being automatic. A new successful
route would need to avoid these particular encodings or provide a
substantive new global regularity mechanism. No outside contact,
publication operation, Git operation, or shared queue edit was performed
by this route.

Final root synthesis 2026-10-17T21:15:16.994979+00:00: fresh comprehensive partial review passed the additional discrete quotient matching and rational-decoder claims. All statements remain encoding-specific, with no full resolution or novelty assertion. See reviews/partial_adversary01.md.
