# Turn 3: an obstruction to all atoroidal common-boundary realizations

**Unreviewed scoped partial. Author turn 3/5. KP-1.6 remains unresolved.**
This turn goes beyond the disjoint-pair test: it gives a necessary metric
condition for arbitrary intersecting surfaces at a fixed knot, and uses it
to exclude every atoroidal boundary knot for an explicit S-equivalent pair.
Satellite boundary knots remain allowed by the original question.

## 1. A form-label map on the actual same-knot graph

Retain the notation of turn 2: N=2k+1>=3, V_(N,a)=[[a,k+1],[k,0]],
T_N={4 beta² delta² mod N: beta|k, delta|k+1}, and H_N=<T_N>.
All residues a below are units. Let ell_N(h) be the shortest number of
factors from T_N whose product is h, for h in H_N. In particular ell_N(1)=0.
Since 1 belongs to T_N, products of at most r factors form exactly T_N^r.
Since T_N is inverse-closed, this is the ordinary undirected Cayley metric.

Suppose a knot K has a genus-one Seifert surface of class [V_(N,a)]. Its
Alexander polynomial is

    -k(k+1)t² + (2k(k+1)+1)t - k(k+1),

which has nonzero quadratic coefficient. Thus K has genus one, and every
genus-one Seifert surface under consideration is minimal genus. The vertices
of the Kakimizu graph G(K) are isotopy classes of such minimal surfaces;
an edge means that the two classes admit disjoint-interior representatives.

Each vertex has a well-defined integral congruence class of its Seifert
pairing. Isotopy preserves linking numbers and changing a homology basis
changes the matrix by congruence. Every vertex has the same Alexander
polynomial, hence the same discriminant N². By AFMW Theorem 5.8, the forms
are in the orbit of the initial primitive form under the group of primitive
special squares. Thus all remain primitive. Propositions 6.7–6.8 label them
by a coset a H_N in (Z/NZ)^×. AFMW Theorem 1.1 says that the ratio of the
labels of any adjacent vertices lies in T_N. This is a necessary assertion
at the actual knot; the converse only supplies some knot and is not used.

It follows, by multiplying the ratios along any path, that

    d_G(K)([F],[F']) >= ell_N(b a^(-1))                 (1)

whenever F,F' have labels a,b. This is a genuine constraint on every
common-boundary realization, including intersecting surfaces and satellite
knots. It does not prove that every algebraic path lifts to a same-knot path.

For comparison with geometric intersections, the Scharlemann–Thompson
path bound recalled on Sakuma–Shackleton p.203 is

    d_G(K)([F],[F']) <= i([F],[F'])+1,

where i is the least number of intersection components of transverse
spanning representatives, with their boundary longitudes arranged disjointly.
Consequently any such realization must satisfy

    i([F],[F']) >= ell_N(b a^(-1))-1.                  (2)

Only this weak necessary lower bound is asserted. The graph distance is not
claimed equal to the arithmetic distance.

## 2. Published atoroidal input and its exact consequence

Sakuma–Shackleton, *On the distance between two Seifert surfaces of a knot*,
Osaka J. Math. 46 (2009), 203–221, Corollary 1.3 on p.204, proves:

    If K is an atoroidal genus-one knot, diam G(K) <= 2.

The full published PDF and its p.204 were inspected. The word atoroidal is
essential: it means every incompressible torus in the exterior is boundary
parallel. No general satellite conclusion is contained in the corollary.
Combining it with (1) proves the following scoped theorem.

**Atoroidal realization obstruction.** If V_(N,a) and V_(N,b) occur on one
atoroidal boundary knot, then b a^(-1) belongs to T_N². In particular,
any h in H_N\T_N² gives an S-equivalent pair that cannot occur on any
atoroidal knot, even if the surfaces are allowed to intersect.

This is a necessary condition, not an atoroidal realization characterization.

## 3. An exact determinant -342 pair

For N=37, k=18, positive divisors of k are 1,2,3,6,9,18 and those of k+1
are 1,19. Enumerating their special squares gives

    T_37={1,4,7,9,16,28,33,36},
    T_37²={1,4,7,9,10,11,12,16,21,26,27,28,30,33,34,36},
    H_37=T_37² union {3,25}.

The membership 3 in H_37 has the short exact certificate

    4 * 16 * 33 = 3 (mod 37).

Each factor is in T_37; 3 is not in T_37². Thus ell_37(3)=3. Consider

    A=[1 19],       B=[3 19].
      [18 0]         [18 0]

Both have standard unimodular skew part, determinant -342, and polynomial
`-342 t²+685t-342`. Their primitive residues 1 and 3 are distinct, and
AFMW's S-equivalence criterion proves they are S-equivalent. If they share
any boundary knot K, (1) forces the two surface classes to have graph
distance at least three. The atoroidal corollary rules out every atoroidal K.
Therefore any successful realization must have an essential nonperipheral
torus in its complement, i.e. must be satellite in the usual exterior sense.
Equation (2) also gives at least two intersection components.

This is NOT an unrestricted counterexample to KP-1.6. The original question
does not require an atoroidal or hyperbolic boundary knot. The source
S-equivalence graph is connected precisely because the arithmetic subgroup
is generated by T_37; that fact still does not construct a satellite K
carrying the entire needed path.

## 4. The determinant -42 pair and the stronger whole-class quantifier

For the turn-2 pair N=13, a=1,b=12, one has ell_13(12)=2, since 12=3*4.
Thus the new diameter obstruction does not decide that pair. If realized,
the two surfaces cannot be disjoint, but distance two is compatible with the
published atoroidal bound. No band construction has been obtained here.

There is a separate useful restriction on the stronger whole-class question.
Valdez-Sánchez, *The Kakimizu complex for genus one hyperbolic knots in the
3-sphere*, Algebraic & Geometric Topology 25 (2025), 1667–1730,
DOI 10.2140/agt.2025.25.1667, Theorem 1 on p.1668, proves that this complex
is either one d-simplex, or at most two d-simplices meeting in one common
(d-1)-face, with 0<=d<=4 and only one simplex for d=0,4.
In particular it has at most five vertices. More specifically its graph
is complete except possibly for a single pair of vertices.

Choose one actual surface vertex for each distinct form label realized at
a fixed hyperbolic K. Distinct labels require distinct vertices. Every
algebraically forbidden disjoint pair must be a nonedge between the chosen
vertices, so there can be at most one such label pair. For N=13, within
H_13={1,3,4,9,10,12}, the forbidden pairs are exactly

    {1,12}, {3,10}, {4,9}.

Any five of the six labels contain at least two of these three disjoint
pairs. Hence a fixed hyperbolic K in this primitive class realizes at most
four of its six core congruence types. It cannot be a knot realizing every
form in that S-class. This is stronger here than simply counting five
vertices, but it does not exclude a satellite universal knot. It also does
not decide whether each prescribed pair has its own common knot.

The proof only uses the published structure theorem as an input; it does
not reconstruct that theorem or infer an analogue for satellite knots.

## 5. Two examined shortcuts that do not close the satellite gap

(a) Johnson–Pelayo–Wilson, *The coarse geometry of the Kakimizu complex*,
AGT 14 (2014), 2549–2560, Lemma 12 on pp.2556–2557 gives finitely many
fundamental surfaces up to spinning about JSJ tori **in the core**. The core
is defined on p.2551. Spinning is an orientation-preserving diffeomorphism
supported away from K, so it preserves the integral Seifert form. Therefore
there are finitely many form types among the minimal surfaces contained in
that core. But the theorem does not say every minimal surface lies in the
core or is obtained from a core surface by a form-preserving operation.
Bounded distance from the core is not the same as bounded form variation.
Thus this does not prove global finiteness of form types for every K, and
cannot remove the satellite exception or answer the whole-class question.

(b) Myers, *Concordance of Seifert surfaces*, Pacific J. Math. 298 (2019),
429–444, proves that an individual nondisk Seifert surface is concordant to
one on a hyperbolic knot. The linking-number argument on pp.430–431
preserves its matrix. This result is about one surface at a time. It does
not supply simultaneous concordances of two possibly intersecting surfaces
with the same new hyperbolic boundary. Using it that way would assume the
missing compatibility and, for the N=37 pair, force a contradiction with
the rigorous atoroidal obstruction. No such simultaneous extension is used.

## 6. Status

Three substantive author turns are now complete. This turn provides the
all-knot arithmetic distance lower bound, a concrete obstruction to every
atoroidal common boundary, and a stronger hyperbolic whole-class limitation.
The unrestricted determinant -42 pair, satellite realization of the
new determinant -342 pair, and general composite classes remain open here.
Completion estimate: 35%, with 2/5 author turns remaining. All results are
unreviewed partial deductions from the credited inputs; no novelty claim,
no full-target promotion, and no claimed-result PR.
