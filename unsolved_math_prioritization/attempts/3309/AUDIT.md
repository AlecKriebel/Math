# Independent audit: forest edge-correlation reductions

## Decision and scope

This is an AI-assisted, unrefereed authored-prose edition with an internal AI mathematical audit. It has no external human peer review or formal proof-assistant certification. It is not a computational reproduction package: the complete mathematical arguments and essential formula witnesses are included, while programs, raw expanded certificates, source documents, and datasets are not distributed. Historical checks and source inspection are described as historical evidence, not as newly executed checks or blanket acceptance of external source proofs.

**ACCEPT the explicitly bounded partial mathematics, not a solution of the general conjecture.** The audited exposition proves equivalence of three universal pairwise statements, verifies weighted K4 certificates and established closure operations, and rules out three tempting shortcuts. It supplies neither a general proof nor a counterexample. No novelty claim is accepted or needed.

The intended problem is corpus 3309 / OPG-1757. For a finite simple graph, sample uniformly from every acyclic edge subset, including the empty set, keeping isolated vertices. For **distinct** edges e and f, the question is whether P(e,f) <= P(e)P(f). This is pairwise negative correlation. Full negative association of disjoint-coordinate increasing events is stronger and is not proved. Uniform spanning trees, rooted forests, fixed-component forests, and infinite-volume uniform spanning forests are different laws. The original OPG display omits distinctness; the primary Grimmett–Winkler formulation supplies it. An edge cannot be tested against itself.

The candidate's full authored proof was read. Its finite witness was independently checked without importing or executing its checker. The independent calculations use GF(2) incidence-column independence to recognize forests and exact symbolic/rational arithmetic, unlike the candidate's disjoint-set and component-count implementations. No scholarly source author's code was executed. The independent exact checks described here preceded preparation of this public prose edition; they were not rerun during editorial preparation.

## 1. Authenticated statement and overlapping record

The two whole source corpora were historically independently hashed and their record counts checked: problems.json has 15,458 records, and research_results.json has 6,701 entries. Their public verification metadata appears in SOURCES.json. Matching byte identities authenticate the supplied snapshot; they do not certify the truth of its prose. The authored proof and audit inventories were separately authenticated before editorial preparation, as recorded in VERIFICATION.json.

The primary overlap source was recovered in full from the [official MFO repository](https://publications.mfo.de/bitstream/handle/mfo/4396/OWR_2025_47.pdf). Jonathan Leake's contribution, *Stable polynomials*, occupies printed pp.2557–2560 of Report 47/2025. Definition R(c,S) is on p.2559; Conjecture 6 and the distinct-index counting interpretation are on p.2560. The latter states the same all-forest Rayleigh question at the all-one vector. Thus corpus 30006450 / OWR-14299575-001's first question overlaps the repaired OPG question. Its additional interpolation-class question is broader and remains untouched. The source is Report 47/2025, with the workshop dated 12–17 October 2025; the corpus's 2026 display year is preserved as source-data metadata rather than silently treated as the report year.

At unit weights, differentiation of the multiaffine forest polynomial gives Delta(e,f)=N_e N_f−N N_ef. Dividing by N² yields the desired inequality. The same-coordinate derivative in R(1,S) is harmless because the second derivative is zero; the probabilistic interpretation must still use distinct edges. In the original simple-graph measure, conditioning on f present is legitimate because the singleton {f} has positive mass.

## 2. Complete audit of the bipartite and weighted reduction

The candidate's Theorem 1 is correct with its exact quantifiers:

- U: every finite simple graph, uniform all-forest law, every distinct edge pair;
- B: the same assertion restricted to finite simple bipartite graphs;
- W: every finite loopless multigraph, every strictly positive edge-weight vector, every distinct labeled edge pair, product-weighted all-forest law.

W implies U and U implies B directly. The substantive implication B implies W is valid as follows.

Fix a finite loopless multigraph H, positive integers n_g for its labeled edges, and a common even L>=2. Replace each edge by n_g internally vertex-disjoint paths of length L. All new internal vertices are exclusive to their path. The resulting microscopic graph is simple even when H has parallel edges: every microedge has an internal endpoint unique to its path. It is bipartite because original vertices all have color zero and each path has even length. Original isolated vertices remain harmless.

A microscopic cycle must use entire replacement paths, since every internal vertex has degree two in the host graph. Accordingly, a microscopic edge subset is a forest exactly when each gadget has at most one full path and its active labeled macroedges form a forest of H. Two full paths in one gadget are forbidden separately; two active parallel macroedges give the appropriate two-edge multigraph cycle. Partial paths cannot introduce another cycle. This establishes both directions of the support correspondence, rather than only a formal partition identity.

Put d=2^L−1. For a prescribed macroforest A, a gadget absent from A has d^{n_g} configurations. A present gadget has n_g d^{n_g−1}. These choices form a Cartesian product once A is fixed. Therefore the projected mass is exactly proportional to product_{g in A} n_g/d, and the conditional gadget choices are independent. The normalizing identity is Z_micro(1)=d^{sum n_g} Z_H(n/d).

Now mark a fixed microscopic edge in a fixed path of each gadget. Conditional on the macroedge being absent, its inclusion probability is p0=(2^{L−1}−1)/d. Conditional on presence, its path is the unique full path with probability 1/n_g; otherwise it has the same proper-subset law. Thus its conditional mean is p0+delta_g Y_g, where delta_g=2^{L−1}/(n_g d)>0. For two **different** macroedges, the marked microedges are distinct and conditionally independent. Total covariance gives exactly

Cov_micro(X_g,X_h)=delta_g delta_h Cov_macro(Y_g,Y_h).

This transfers the pairwise sign without treating a whole-path event as an individual edge or invoking full negative association. It does not assert conditional independence for two edges in the same gadget.

For any fixed strictly positive target weight vector, choose n_g along even L so n_g/(2^L−1) tends to that target. All n_g can be positive. The macro partition polynomial is at least one on the nonnegative orthant; covariance is a rational function with its square as denominator, and is continuous. The finite-graph limit is therefore valid and proves B implies W. Strict counterexamples would survive sufficiently close approximation, but no counterexample is produced. Extension to zero weights follows by continuity or deletion; loops can be omitted separately because they never occur in a forest.

Uniform-to-weighted equivalence is already credited to Cocks and Erickson in [Erickson (2012), p.76](https://ajc.maths.uq.edu.au/pdf/52/ajc_v52_p075.pdf). The present explicit simple-bipartite marked-edge realization is accepted as a correct derivation with no novelty conclusion.

## 3. K4 and all closure cases

Use a=01,b=02,c=03,d=12,e=13,f=23 and S=1+c+e+f. Independent symbolic expansion of the complete forest polynomial confirms

Delta(a,b)=(dS+ef)²+dS²+ef(1+e+f),

Delta(a,f)=(be−cd)²+be(1+b+e)+cd(1+c+d).

There are two vertex-automorphism orbits of distinct edge pairs, so these identities cover all pairs. Each right-hand side is nonnegative for nonnegative weights and strictly positive for positive weights. They are polynomial identities, not weight sampling. The independently obtained unit-weight counts are N=38, N_e=14, N_adj=4, N_opp=5, giving Delta_adj=44 and Delta_opp=6; covariances are −11/361 and −3/722.

For a nonloop distinguished edge x, write Z=A+xB. A enumerates deleted-edge forests; B enumerates those among them whose two terminals are disconnected. Coefficientwise A>=B, and B has the empty monomial, so B>0 at nonnegative activities. This observation is essential for the following sign arguments.

Parallel replacement gives A+(a+b)B. The old-old differences specialize x=a+b; a new-old difference is the original x-old difference; the new-new difference is B². Series replacement gives (1+a+b)A+abB=q Z(ab/q). Its old-old difference is q² times the specialized original difference; its a-old difference is b(1+b) times the x-old difference; its a-b difference is A(A−B). Every pair position is covered. The b-old case follows by interchange, with all multipliers nonnegative.

For the edge-gluing operation, the two factors meet only at the two identified terminals after their distinguished nonloop edges are removed. With Z_i=A_i+x_i B_i, the glued forest polynomial is A1 B2+B1 A2−B1 B2. Two terminal-connecting forests would form a cycle; all other combinations are acyclic. On one side the effective distinguished activity is (A2−B2)/B2>=0, and the Rayleigh difference acquires B2². A zero effective activity is justified by continuity, including a bridge factor. For a cross-side pair g,h, direct differentiation gives Delta_glued(g,h)=Delta_1(x1,g) Delta_2(x2,h). The proof's r_i=A_i/B_i log-derivative calculation has positive denominators and the correct sign. Both identities also passed independent formal-jet algebra.

Products cover disjoint and one-vertex unions: same-side differences acquire the other factor's square; cross-side differences vanish. Deletion specializes x=0. For contraction, the leading x² coefficient of Delta_Z is Delta_B; dividing by x² and taking x to infinity proves the required inequality. Loops created on contraction may be discarded, as no forest contains them. These steps prove closure for the exact constructed family, not a decomposition theorem for every graph.

The resulting family generated from edges and K4 by these operations is valid. These are established results: [Erickson (2012), pp.76, 79–80](https://ajc.maths.uq.edu.au/pdf/52/ajc_v52_p075.pdf) supplies explicit prior attributions and two-sum identities; [Wagner, Theorem 5.8](https://arxiv.org/abs/math/0602648) covers I-Rayleigh two-sum closure. The present argument is self-contained and does not depend on accepting uninspected source proofs. The Semple–Welsh and Cocks attributions here are mediated by the inspected Erickson paper; their full original articles were not audited.

## 4. Shortcut obstructions and exact limits

The triangle forest polynomial is 1+a+b+c+ab+ac+bc. At a=b=c=−1/2+i sqrt(3)/6 it vanishes with all imaginary parts positive. Real stability therefore fails, although its positive-real pairwise Rayleigh difference c+c² is nonnegative. This directly blocks the stated stability shortcut, not the conjecture.

The K4 opposite-pair difference has coefficient −2 on bcde. Coefficientwise nonnegativity is false even though the square identity proves nonnegativity at positive values. Again this is not a negative-correlation counterexample.

Adding a root and projecting an augmented spanning tree weights each forest by product_C(sum_{v in C} r_v). The factor depends on component sizes/weights. For the triangle, equalizing the empty forest and each single-edge forest forces all positive r_v=2, but then the three-vertex tree factor is 6 versus empty-forest factor 8. No fixed positive star weights repair this projection to the uniform triangle law. Independent enumeration also recovers rooted multiplicities 1,2,2,2,3,3,3, summing to 16 over the seven unrooted forests.

No conclusion about arbitrary disjoint increasing events, interpolation classes, general real stability, or the full graph family follows.

## 5. Independent controls, dependencies, and remaining gap

The independent exact checker passed in Python normal, -O, and -OO modes. Its explicit exceptions survive optimization. In each mode it checks the K4 identities, triangle zero, eight generic series/parallel/two-sum identities, and five finite gadgets. The gadget cases include lengths 2 and 4, nonuniform multiplicities, a bridge, and parallel macroedges. Every projected macrostate count and every individual microscopic conditional mean is checked, as are cross-gadget representative conditional covariance and every macroedge pair's transfer. There are 16 checked cross-pair transfers across these five cases. Finite coverage is explicitly bounded; the general reduction is proved by the argument above.

Negative mathematical controls reject self-pairs, a changed K4 identity, odd gadget length, a zero-sized bundle, and a corrupted series formula. Independent candidate-witness controls reject a changed forest coefficient, repeated marked edge, altered macro covariance, and altered micro covariance. The source-author programs were never run. SymPy 1.14.0 and Python 3.12.14 are the checker dependencies; the mathematics rests on elementary counting, polynomial algebra, differentiation, and continuity, not numerical approximations.

Recent literature is used only for scope. [Gupta, arXiv:2609.26134v1](https://arxiv.org/abs/2609.26134) claims the complete-graph unit-weight family; its all-n proof and code were not audited here. Its displayed August date is retained despite the identifier. [Çiçeksiz–Ravichandran, arXiv:2610.00549v1](https://arxiv.org/abs/2610.00549) gives conditional high-fugacity forest claims and complete-host random-cluster results. The forest q→0 limit rescales edge weights by q; fixed weights instead select connected subgraphs on connected hosts. Those claims do not prove the present general uniform-forest target. Different recent source descriptions are preserved rather than synthesized into an unsupported resolution.

**Residual:** establish Delta_G(e,f)>=0 for every finite graph at every positive vector, or equivalently solve the simple-bipartite uniform case. The accepted reduction and family certificates do not do this. This public audit is an authored partial-results review with public metadata and citations. No general-source acceptance, full-conjecture acceptance, or novelty certification follows; source documents and corpus contents are not included.
