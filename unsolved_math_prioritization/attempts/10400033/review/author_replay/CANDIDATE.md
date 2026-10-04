# A tournament bound for the third Vassiliev invariant

**Candidate proof; separate adversarial review pending.**
This addresses Ohtsuki Conjecture 2.11 (Willerton), target 10400033.
The argument uses the established Polyak–Viro formula. Historical novelty
has not been established.

## 1. Statement and normalization

Let \(v_3\) be the additive degree-three Vassiliev invariant which changes
sign under mirror image and takes value \(1\) on the right-handed trefoil.
For every classical knot diagram \(D\) with \(n\) crossings, we prove

\[
\boxed{\quad |v_3(D)|\le
\left\lfloor\frac{n(n^2-1)}{24}\right\rfloor .\quad}
\tag{1}
\]

In fact, when \(n\) is even, the argument gives

\[
|v_3(D)|\le \frac{n(n^2-4)}{24}.
\tag{2}
\]

The right side of (2) is an integer for even \(n\).
No positivity, alternatingness, primeness, or crossing-minimality hypothesis
is imposed on the diagram. The cases \(n<3\) follow immediately from the
three-arrow formula below.

The normalization and exact target are those in
[Ohtsuki, Section 2.4, pp. 403–405](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).
Equivalently, for the normalized Jones polynomial \(J_K(q)\),

\[
v_3(K)=-\frac{J_K'''(1)+3J_K''(1)}{36}.
\tag{3}
\]

This is the convention in
[Willerton, Section 1](https://arxiv.org/abs/math/0104061v1).

## 2. The precise imported arrow formula

Orient the knot and its Gauss circle. For each crossing, draw an arrow
from its overpassing preimage to its underpassing preimage and assign its
crossing sign \(\epsilon_c\in\{-1,1\}\).

We count subdiagrams by **three-element subsets of crossings**, preserving
the cyclic order and arrow directions. Each subset is counted once.
In particular, cyclic automorphisms of a pattern are not additional
occurrences.

The two unsigned arrow patterns below are specified without a drawing.
Label six consecutive endpoints \(0,1,\ldots,5\) around an oriented circle;
each ordered pair gives an arrow from its first endpoint to its second.

| Pattern | Arrow pairs | Coefficient |
| --- | --- | --- |
| \(P\) | \((3,0),(5,1),(2,4)\) | \(1/2\) |
| \(T\) | \((3,0),(1,4),(5,2)\) | \(1\) |

An occurrence means that the selected three-arrow diagram is isomorphic
to the given pattern after an orientation-preserving cyclic relabeling
of its six endpoints. The two patterns are disjoint types: \(P\) has two
intersecting pairs of chords, while \(T\) has three.

[Polyak–Viro, Theorem 2, equation (5), printed p. 448](https://www.math.stonybrook.edu/~oleg/math/papers/1994-Polyak-Viro.pdf)
gives, in this subdiagram-counting convention,

\[
v_3(D)=
 \frac12\sum_{\substack{S\subset\operatorname{Cross}(D)\\G_D|_S\simeq P}}
       \prod_{c\in S}\epsilon_c
 +\sum_{\substack{S\subset\operatorname{Cross}(D)\\G_D|_S\simeq T}}
       \prod_{c\in S}\epsilon_c.
\tag{4}
\]

The formula is imported, not proved or claimed as new here. All arrows
in these patterns have multiplicity one. The convention can also be
expressed as pairing an arrow pattern with the sum of all subdiagrams;
see [Chmutov–Duzhin–Mostovoy, Section 13.1.1](https://www.math.cinvestav.mx/~mostovoy/cdbook/cdbook-as-submitted.pdf).
If one instead counts labelled embeddings of an unbased pattern, its
automorphism multiplicity must be divided out. Pattern \(T\) has three
cyclic automorphisms; this does not give a factor of three in (4).
The distinction is also visible in the conversion between based and
unbased diagrams in
[Zhang, Remark 4.1, pp. 19–20](https://arxiv.org/abs/2306.01591v1).

Write \(N_P,N_T\) for the numbers of these subsets, with signs ignored.
The triangle inequality, valid for arbitrary crossing signs, gives

\[
|v_3(D)|\le \frac12 N_P+N_T.
\tag{5}
\]

No assumption that a sign assignment is realizable, or that individual
summands have the same sign, is used in this inequality.

## 3. Orienting the chord-intersection graph

For an arrow \(c\), write \(t_c,h_c\) for its tail and head, and let
\((t_c,h_c)\) be the open arc followed in the positive direction around
the Gauss circle.

Construct a partially oriented complete graph \(G\) whose vertices are
the crossings. Two vertices have an edge precisely when their chord
endpoints alternate around the circle. For such a pair, orient the edge by

\[
c\longrightarrow d
\quad\Longleftrightarrow\quad t_d\in(t_c,h_c).
\tag{6}
\]

This gives exactly one direction to each intersecting pair. Indeed,
when the endpoints alternate, exactly one of \(t_d,h_d\) belongs to
\((t_c,h_c)\); checking their cyclic order shows

\[
t_d\in(t_c,h_c)\quad\Longleftrightarrow\quad
t_c\notin(t_d,h_d).
\]

Pairs of nonintersecting chords remain unoriented and have no edge in \(G\).

**Pattern correspondence.** Every occurrence of \(P\) gives a directed
two-edge path in \(G\), and every occurrence of \(T\) gives a directed
three-cycle.

To verify this explicitly, denote the arrows in each row of the table
by \(c,a,b\), in the order listed. For \(P\), the intersecting pairs are
\(c,a\) and \(c,b\); the arc rule gives \(b\to c\to a\).
The pair \(a,b\) is absent. For \(T\), all pairs intersect and the rule
gives \(c\to b\to a\to c\). These conclusions are unchanged by cyclic
relabeling. Reversing the orientation chosen for the entire Gauss circle
reverses all graph edges and still gives a path or cycle.

We need only these implications. A directed path can arise from another
arrow-pattern type too; those extra paths will cause no difficulty.

## 4. Completing to a tournament

Independently orient each missing edge of \(G\) by a fair coin. Together
with the fixed edges, this gives a random tournament \(\mathcal T\) on
the \(n\) crossings. Let \(C(\mathcal T)\) count its unordered three-element
vertex subsets that form directed cycles.

For a fixed three-element subset \(S\):

- if its Gauss subdiagram is \(T\), all three graph edges are already a
  directed cycle, so its probability of being cyclic is \(1\)
- if its Gauss subdiagram is \(P\), its two fixed edges are a directed
  path, and exactly one of the two orientations of its missing edge
  closes a directed cycle, so the probability is \(1/2\)
- for every other type, the probability of being cyclic is nonnegative

There is exactly one cyclicity indicator per subset. Thus no subset or
pattern is counted multiple times. Linearity of expectation gives

\[
\mathbb E C(\mathcal T)
 =\sum_{|S|=3}\mathbb P(S\text{ is cyclic})
 \ge N_T+\frac12N_P
 \ge |v_3(D)|.
\tag{7}
\]

The indicators for different triples need not be independent. The only
independence required by this construction is the fair orientation of
the missing edges; each individual missing edge has the stated marginal
probability regardless of overlapping triples.

This is a finite auxiliary probability space of graph completions.
No random-knot assumption is involved.

## 5. The tournament extremal bound

Let \(\mathcal T\) be any tournament on \(n\ge1\) vertices, and let
\(d_1,\ldots,d_n\) be its outdegrees. Every three-vertex tournament is
either cyclic or transitive. A transitive triple has a unique vertex
which points to its other two vertices. Consequently,

\[
C(\mathcal T)=\binom n3-\sum_{i=1}^n\binom{d_i}{2},
\qquad
\sum_i d_i=\binom n2.
\tag{8}
\]

Writing \(\bar d=(n-1)/2\) and expanding the squares gives the exact identity

\[
C(\mathcal T)=
\frac{n(n^2-1)}{24}
-\frac12\sum_{i=1}^n(d_i-\bar d)^2.
\tag{9}
\]

In particular, every completion satisfies

\[
C(\mathcal T)\le
\left\lfloor\frac{n(n^2-1)}{24}\right\rfloor,
\tag{10}
\]

since the cycle count is an integer. Its expectation satisfies the same
inequality. Combining (7) and (10) proves (1).

For even \(n\), the mean \(\bar d\) is a half-integer while every \(d_i\)
is an integer. Therefore each square in (9) is at least \(1/4\), giving

\[
C(\mathcal T)\le
\frac{n(n^2-1)}{24}-\frac n8
=\frac{n(n^2-4)}{24}.
\]

Together with (7), this proves (2). The case \(n=0\) has no crossings,
no counted triples, and invariant zero. This completes the proof.
\(\square\)

## 6. Sharpness, scope, and verification boundary

For odd \(n\ge3\), the standard \(n\)-crossing diagram of \(T(2,n)\)
has \(v_3=n(n^2-1)/24\), as recorded by Willerton and in the original
problem list. Thus the bound in (1) is attained for every such odd \(n\).
This known torus-knot evaluation is used only for sharpness, not for
the proof of the universal inequality.

The argument applies to any classical knot diagram, including negative
crossings and composite knots. It does not infer crossing-number
additivity for connected sums. It bounds the formal arrow evaluation
more generally, but does not claim that this evaluation is a virtual-knot
invariant.

The exact checks verify the two pattern types, the graph correspondence,
all sign choices on small formal diagrams, and the finite tournament
identity. A separate Jones bracket state sum calibrates formula (4) on
classical braid closures. These are transcription and normalization
controls; the all-diagram conclusion follows from the proof above.
Separate adversarial review of the imported formula, its multiplicities,
and every domination step is required before promoting this candidate.
