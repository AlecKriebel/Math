# Scoped results for multigraded regularity

Status: authored proof, awaiting independent audit. These results do not solve the
general finitely presented module problem. No novelty or priority is claimed.

## 1. Conventions and computational inputs

Let K be a field and let X be the product of r projective spaces of positive
dimensions. Write S=K[x_1,...,x_N], partitioning the variables into blocks
E_1,...,E_r of sizes m_j=n_j+1. Each variable in E_j has coarse degree e_j.
The irrelevant ideal B is the product of the block ideals. Its squarefree monomial
generators choose one variable from each block, so their number is q=product m_j.
The partial order throughout is coordinatewise order on Z^r.

For a module M, d-regularity means:

* H_B^0(M) vanishes in every degree of every d+e_j+N^r;
* for each i>=1 and u in N^r with sum(u)=i-1, H_B^i(M) vanishes on d-u+N^r.

For a sheaf F, d-regularity instead requires H^h(X,F(a))=0 for h>0 and
a in d-u+N^r, sum(u)=h. If F is the sheaf associated to M, this is precisely
the module conditions with local-cohomology indices i>=2 only. One must not
silently retain or discard the i=0,1 conditions. The local-to-sheaf exact sequence
and this distinction are standard; see Maclagan--Smith, arXiv:math/0305214,
Definitions 1.1 and 6.2 and Proposition 6.4 in the inspected preprint.

An effective general-module formulation must supply a finite homogeneous
presentation matrix and shifts over an effectively represented field with exact
arithmetic and equality testing. A bare arbitrary field is not a machine input.
For the monomial theorem below, finite exponent vectors and the characteristic
suffice: all matrices have integer entries, and ranks depend only on the prime
subfield. Characteristic 0 and every positive prime are supported.

## 2. A sheaf counterexample to a universal finite frontier

**Proposition 1.** On X=P^1_K x P^1_K let i:D->X be the diagonal and
F=i_*O_D. Then

reg(F) = {(a,b) in Z^2 : a+b>=0}.

Its minimal elements are exactly {(t,-t):t in Z}. Thus a finite box containing
every minimal degree does not exist for arbitrary coherent sheaves on products.

**Proof.** The diagonal identifies D with P^1_K and
i^*O_X(a,b)=O_{P^1}(a+b). Closed-immersion pushforward is exact and preserves
cohomology, so H^h(X,F(a,b))=H^h(P^1,O(a+b)). For h>=2 this is zero.
For h=1, dim H^1(P^1,O(l))=max(-l-1,0). The least sum of a degree in either
d-e_1+N^2 or d-e_2+N^2 is d_1+d_2-1. Consequently all required H^1 groups
vanish if and only if d_1+d_2>=0. A degree with positive sum can be decreased
by e_1 and remain regular. A degree with sum zero cannot be decreased in either
coordinate. Every strictly smaller degree has negative sum. This proves both
assertions. The infinitely many boundary degrees are pairwise incomparable. QED.

This disproves the *finite-output sheaf interpretation*, not the possibility of
some algorithm using an infinite but finitely described region. The displayed
half-space itself has a simple finite description.

**Proposition 2.** The associated finitely generated Cox module
M=S/(x_0*y_1-x_1*y_0) has reg(M)=N^2, although its associated sheaf is F.

**Proof.** The ideal of the diagonal is prime and does not contain B; hence M
has no B-torsion. In bidegree (a,b) with a,b>=0, restriction of bihomogeneous
polynomials to the diagonal surjects onto K[s,t]_(a+b): each monomial of degree
a+b factors into one of degree a and one of degree b. Thus H_B^1(M)_(a,b)=0.
Proposition 1 and the local-to-sheaf sequence now give all the regularity
conditions for d in N^2.

If d_1<0, choose e_1=d_1 and e_2>=max(d_2,-d_1). Then e>=d,
M_e=0, and H^0(X,F(e)) has dimension e_1+e_2+1>0. The same exact sequence
gives H_B^1(M)_e!=0, contradicting d-regularity. Interchange the coordinates
for d_2<0. This proves the converse. QED.

Even B-torsion module examples need care: S/(x_0,x_1) in this product has
regularity {d_1>=1}, whose minimal-element set is empty. The module S/(all
variables) has regularity {d_1>=1} union {d_2>=1} union N^2 and only one minimal
element, (0,0). Thus a list of minima alone need not describe a regularity region
without a lower-boundedness hypothesis. Our algorithm retains the whole region.

## 3. Complete finite-cell algorithm for monomial quotients

**Theorem 3.** Given a monomial ideal I by finite exponent vectors, there is a
terminating exact algorithm for the module regularity of S/I and for the sheaf
regularity of its associated sheaf. The output includes:

1. a finite Boolean formula defining the whole region in Z^r;
2. a finite union of coordinate orthants, allowing lower endpoints -infinity;
3. every actual minimal element, including the possibility of none;
4. an explicit finite box containing every minimal element.

This is a scoped application of elementary multigraded Cech methods. It is not
asserted to be a new theorem in the monomial literature.

**Step A: finite degree cells.** Give S its finer Z^N grading, deg x_l=e_l.
For each variable l, let c_l be the largest exponent appearing in any supplied
generator of I, or zero if I=0. Partition the integer line into

(-infinity,-1], {0}, {1}, ..., {c_l-1}, [c_l,infinity).

The singleton list is empty when c_l=0. There are product_l(c_l+2) cells in
Z^N. Choose -1 for each negative interval and c_l for each final interval as
representatives.

**Step B: exact Cech complexes.** Form the local Cech complex on the q monomial
generators b_1,...,b_q of B. In cohomological degree i its terms are indexed by
i-element subsets sigma of {1,...,q}, with the empty subset representing S/I
at degree zero. Let T_sigma be the variables occurring in the b_j for j in
sigma. Localizing at their product inverts exactly these variables.

At fine degree a, the localized quotient has dimension one precisely when:

* a_l>=0 for each l outside T_sigma; and
* no generator exponent alpha of I satisfies alpha_l<=a_l for every l outside
  T_sigma.

Otherwise its dimension is zero. Indeed a fine-degree component of the
localized polynomial ring has at most the single Laurent monomial x^a; the
second condition states exactly that this monomial is not in the localized
monomial ideal. Exponents in inverted variables impose no divisibility
restriction. This also covers I=(1), where every term is zero.

Whenever source and target components are both one-dimensional, the natural
localization map takes x^a to x^a. Hence, in these bases, the Cech differentials
have entries 0 and the usual incidence signs +/-1. All conditions deciding the
bases are constant on a cell: negative signs and comparisons with exponents
between 0 and c_l are constant there. The entire matrix complex, and therefore
the dimension of each cohomology group, is constant on the cell. Finite exact
Gaussian elimination computes every such dimension. The complex stops at q.

**Step C: recover all coarse supports.** For a cell C with nonzero H_B^i,
its coarse-degree image is a product of integer intervals, since disjoint blocks
are summed independently. Sums of integer intervals contain every integer
between their endpoints, with the same statement for unbounded intervals.
Let U_j be the upper endpoint in block j: it is +infinity if any coordinate
cell in that block is the final interval, and otherwise the sum of its finite
upper endpoints.

Coarsening a graded vector space is a direct sum of fine components. Taking
cohomology commutes with these direct sums. Therefore the coarse local
cohomology support is exactly the union of these cell images. Cancellation
between different fine degrees is impossible. For any v, the image of C
intersects v+N^r if and only if v_j<=U_j for every finite U_j. Necessity is
immediate. For sufficiency choose independently in every image interval a
coordinate at least v_j, which is possible by that upper-endpoint condition.

**Step D: an exact Boolean regularity formula.** For each nonzero cell profile
(i,U), i>=1, and each u>=0 of total i-1, append the clause

OR over finite U_j of (d_j >= U_j+u_j+1).

This says exactly that the corresponding support rectangle misses d-u+N^r.
For i=0 append one clause for each k, with thresholds
U_j+1-delta_(jk), testing avoidance of d+e_k+N^r. The conjunction of all
clauses is the full module regularity region. For the sheaf version omit
i=0 and i=1; all other steps are unchanged. An empty conjunction means all
Z^r; an empty disjunction means false. Everything is finite.

**Step E: finite exact extraction of minimal elements.** Let T_j be the finite
set of thresholds appearing in coordinate j. If a minimal satisfying d had
d_j not in T_j, decreasing d_j by one would change no literal: over the
integers a comparison d_j>=t changes only at d_j=t. The resulting degree
would still satisfy the formula, a contradiction. Therefore every minimal
degree belongs to the finite product of the T_j. Check these candidates and
keep exactly those satisfying the formula whose immediate predecessors
d-e_j all fail. In an upward-closed set this predecessor criterion is exact:
if a strictly smaller e were in the set, choose j with e_j<d_j; then
e<=d-e_j and upward closure would make that predecessor regular.

If some T_j is empty, there are no minimal elements, even though the region
can be nonempty. This is deliberately retained rather than treated as failure.
To describe the whole region, distribute the finite conjunction of finite
disjunctions. Each selection of one literal per clause gives an orthant whose
j-th lower endpoint is the largest selected j-th threshold, or -infinity if
there is none. Remove orthants contained in another. This yields a finite,
exact region representation whether or not minima generate it.

**Step F: a proved a priori box.** Every finite U_j lies between -m_j and
sum_(l in E_j)(c_l-1). The largest cohomology index is q. Thus each threshold
appearing in the module formula satisfies

-m_j <= threshold <= q + sum_(l in E_j)(c_l-1).

The i=0 clauses obey the same bounds. Sheaf clauses are a subset. The
threshold argument proves that this explicit box contains every minimal
degree. This is a computable bound from the input exponents, not an appeal
to Dickson's lemma. It may be very loose. QED.

## 4. Why the general module problem is not thereby solved

A nonmonomial homogeneous presentation need not have the fine Z^N grading.
The one-dimensional localized pieces and cellwise fixed matrices used in Step B
are then unavailable. A Gröbner degeneration to a monomial object does not
preserve the entire multigraded regularity region in general. Accordingly we do
not pass arbitrary presentations to the monomial algorithm.

Here is a precise limitation of another tempting reduction. For any T>1 define
U_T=((1,1)+N^2) union ((0,T)+N^2), a subset of N^2. Its minimal elements are
(1,1) and (0,T). It has the same known lower orthant and the same fixed inner
orthant for every T, but one frontier coordinate is arbitrarily large. Also let
U_infinity=(1,1)+N^2. Any algorithm querying a membership oracle only finitely
many times before returning the frontier of U_infinity sees identical answers
on U_T if T exceeds all queried second coordinates. It would then miss (0,T).
This is an oracle obstruction, not an impossibility theorem for finitely
presented algebraic modules. Extra structure from a presentation may help;
we have not supplied the missing uniform argument.

Thus membership decision plus lower bounds, one inner regularity orthant, and
Dickson finiteness is insufficient on its own. The outstanding module task is
to derive a justified terminating completeness criterion or computable global
frontier bound for arbitrary finite homogeneous presentations, preserving the
relevant torsion and sheaf qualifications.
