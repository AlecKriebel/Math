# Affine point to hyperplane matching applicability certificate

Problem: 30000391, OWR-1183-011, priority rank 1223
Audit date: 2026-10-10 UTC
Disposition: affirmative by an existing published theorem, for every positive finite dimension
New proof turns: 0

## Conclusion and attribution

Let d be a positive integer, and let P be any subset of R^d with affine span R^d. Let H be the set of affine hyperplanes that are affine spans of subsets of P. There is an injection f from P into H such that p belongs to f(p) for every p in P. No finiteness, regular-cardinality, continuum-hypothesis, or general-position assumption is needed.

This follows from Jonathan David Farley's Theorem 11 in *A question of Björner from 1981: Infinite geometric lattices of finite rank have matchings*, Australasian Journal of Combinatorics 82(3) (2022), 228-236. The theorem covers geometric lattices of any cardinality and finite rank greater than one. Its matching is incidence-preserving, as defined on printed page 230. This certificate supplies the elementary affine-lattice identification; it does not claim a new solution or a new general matching theorem.

Primary theorem: https://ajc.maths.uq.edu.au/pdf/82/ajc_v82_p228.pdf
Original problem: Anders Björner, *Matching points to hyperplanes*, printed pages 51-52 of Oberwolfach Report 1/2006: https://ems.press/content/serial-article-files/46029?nt=1
Report DOI: https://doi.org/10.4171/owr/2006/01

## Exact original scope

The original passage explicitly assumes aff(P)=R^d before stating Conjecture 1. The target consists of hyperplanes spanned by P, and the required map goes from points to hyperplanes, is injective, and assigns an incident hyperplane to every point. A mere cardinal inequality or a matching in the non-incidence relation would not suffice.

On printed page 51, the report records the finite case and the full-space case P=R^d, then the cases d=2; d=3 or 4 with |P| regular; and |P|<aleph_omega. Page 52 discusses singular cardinals as the obstacle and observes that CH would imply the conjecture from the available results. Farley's unrestricted finite-rank theorem eliminates that cardinality obstacle in the usual ZFC setting.

The natural precise dimension convention is d>=1 and finite. If the wording 'every dimension' is read to include d=0, the singleton P=R^0 has no hyperplane containing its point, so that literal extension is false. This boundary case must not be silently claimed. For d=1, the hyperplanes are singleton points and the map p -> {p} settles the problem directly. The theorem application below includes this case as a rank-two lattice.

## Construction of the geometric lattice

For S contained in P, put

    cl(S) = P intersect aff(S),   cl(empty set) = empty set.

Let L consist of the cl-closed subsets of P, ordered by inclusion. Its bottom and top are the empty set and P. Arbitrary intersections of closed sets are closed, and the join of a family is the closure of its union. Thus L is a complete lattice. This construction is important: the meet is the intersection of the closed point subsets, not an unjustified ambient intersection in a poset of affine subspaces spanned by P.

For p in P, write v_p=(p,1) in R^(d+1). For nonempty S,

    q in aff(S) iff v_q in span{v_s : s in S}.

Indeed, the final coordinate of a linear expression for v_q forces the coefficients to sum to one. All v_p are nonzero, and no two are proportional. The linear span of all v_p has dimension d+1 because P affinely spans R^d.

For F in L define

    r(F) = dim span{v_p : p in F}.

Then r(empty set)=0 and r(F)=dim aff(F)+1 for nonempty F. If F is a proper subset of G in L, a point p in G\F has v_p outside the span of F. Consequently r(F)<r(G). Every flat has a finite basis consisting of at most d+1 of its points, whose closure is the flat. Extending such a basis one vector at a time shows that lattice covers increase rank by exactly one. Hence L has rank d+1 and has no infinite chain.

The atoms are exactly the singletons {p}, since the vectors v_p are nonzero and pairwise nonproportional. Every flat is the join of its singleton atoms.

For completeness, upper semimodularity can be checked without invoking a general infinite-matroid representation result. If G and G' are distinct covers of F, write G=cl(F union {p}) and G'=cl(F union {q}). The vectors v_p and v_q represent distinct one-dimensional extensions modulo span(F), so their joint span increases the rank by two. Therefore G join G' covers both G and G'. Thus L is geometric in precisely the finite-height sense used by Farley on printed page 229.

Equivalently, the standard submodular rank inequality follows because span(F intersect G) is contained in span(F) intersect span(G). The argument does not assume that these two linear intersections coincide.

## Identification of the coatoms

The coatoms of L are exactly its rank-d flats.

If F is a coatom, aff(F) has affine dimension d-1, is spanned by points of F contained in P, and is therefore an element of H. Moreover,

    P intersect aff(F) = F.

Conversely, if h belongs to H, choose a subset S of P spanning h. Then F_h=P intersect h is closed, contains S, and has affine span h. Its rank is d, so it is a coatom. These two operations are inverse bijections:

    coatom F  <->  hyperplane aff(F),
    hyperplane h  <->  flat P intersect h.

In particular, distinct coatoms produce distinct ambient hyperplanes. This is the step that turns lattice injectivity into the exact injectivity demanded by the problem.

## Applying the published matching theorem

The lattice L has finite rank d+1>=2. Farley's Theorem 11 therefore provides an injective map m from its atoms to its coatoms satisfying {p} subset m({p}). Define

    f(p) = aff(m({p})).

The coatom identification shows f(p) belongs to H and p belongs to f(p). If f(p)=f(q), intersecting the common hyperplane with P gives m({p})=m({q}); injectivity of m yields p=q. This proves the stated conclusion.

## Infinite sets and degeneracy

All constructions above are set-theoretic and work for arbitrary infinite P. No enumeration of P is required. If P is infinite, every flat is generated by a finite subset of P, so |L|<=|P|^(<omega)=|P| in ZFC; the singleton flats give the reverse inequality. Thus |L|=|P|, although no cardinal bound is needed to apply Farley's theorem.

The proof does not require P to be discrete, closed, measurable, dense, or in general position. Collinear subsets and large lower-dimensional concentrations inside a full-spanning P cause no problem. Points are elements of a set, so there are no repeated-point labels to match separately.

The full-span hypothesis must be retained. For example, if more than one point of P lies on a single line in R^2 and P spans exactly that line, then the only P-spanned ambient hyperplane is that line, and an injection from P to that singleton hyperplane set is impossible. One may instead formulate a separate relative-span problem, but that is not the stated ambient problem.

There is no claim here about infinite-dimensional affine spaces, matching every hyperplane as well as every point, measurable or definable choices of f, or a theorem in ZF without the axiom of choice.

## Audit level

The complete Farley paper was read. The lattice restriction lemma, singular-cardinal step, and both branches of the final argument were checked, with short implicit justifications expanded in INTERNAL_PROOF_AUDIT.md. The cited transversal-obstruction statements were also cross-checked in the original Aharoni-Nash-Williams-Shelah paper. Imported theorems were not all re-proved or recursively audited. The acceptance is therefore a verified application plus an internal proof audit relative to explicitly identified literature dependencies, not a claim of an independent foundational proof of every dependency.
