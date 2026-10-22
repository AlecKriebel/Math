# KP-1.30: five approaches to universal Khovanov 2-torsion

**Status: partial reductions and explicit obstructions; the universal problem is unresolved by this report.**

Research date: 8 October 2026. Catalogue identifier: 2689. This is an authored mathematical investigation, not a claim of a new solution or a claim that the partial observations below are new to the literature.

## 1. Target, conventions, and source control

K3, Problem 1.30, asks whether a nontrivial knot can have Khovanov homology with no nonzero element of order two.

The statement was checked in the author-hosted preliminary K3 book, printed pages 35–36 [K3]. It concerns knots in the classical setting of the cited sources and **ordinary, even, unreduced Khovanov homology with integral coefficients**. Here “contains 2-torsion” means that there is a nonzero element killed by 2. A cyclic group of order 4, for example, contains such an element. The target is not the assertion that every knot has a direct summand isomorphic to Z/2, nor an assertion about reduced or odd Khovanov homology.

Write H(K;R)=Kh(K;R) and V(K;R)=reduced Kh(K;R). Normalize the reduced unknot to one generator in bidegree (0,0), and the unreduced unknot to generators in (0,-1) and (0,1). Homological differentials have degree (1,0). Total ranks and dimensions below sum over both gradings. Unless otherwise specified, `rank` means dimension over Q, not dimension over F2.

The older AIM URL `https://aimath.org/pastworkshops/kirbylistrep.pdf`, supplied in the catalogue's literature background, retrieves a four-page workshop report. It does not contain Problem 1.30. The actual author-hosted K3 PDF used here has 436 pages. It is marked as a preliminary version with restrictions on reposting. No source PDFs or source text are part of this public packet.

### Literature boundary

Shumakovitch's original conjecture is broader, allowing links and specifying elementary exceptions [S14]. The present investigation concerns only its knot case. The 2026 K3 list still presents that case as a problem. Gujral–Wang prove a proper-rational-tangle rank obstruction and deduce the unknotting-number-one case, and more generally the case of a nontrivial knot obtained from an unknot or trefoil by one proper rational tangle replacement [GW25]. Díaz–Manchón supply further sufficient diagrammatic patterns, rather than a universal existence theorem for such patterns [DM25]. Searches for a subsequent universal proof or counterexample did not locate a verified one. A negative literature search is not proof that none exists.

Five mathematical approaches follow. Source retrieval, computation, and auditing are verification work and are not counted as additional approaches.

## 2. Approach I: force a coefficient-field rank gap

### 2.1 A torsion-count identity

For a finitely generated abelian group G, let t2(G) be the number of cyclic factors in its 2-primary subgroup, counting multiplicity and ignoring exponents. Thus t2(Z/4)=1, t2(Z/2 plus Z/8)=2, and t2(Z/3)=0. For graded groups sum this number over the gradings. Put

    t(K)=t2(H(K;Z)),       a(K)=t2(V(K;Z)),
    r(K)=dim_Q V(K;Q).

The universal coefficient theorem for a bounded complex of finite-rank free abelian groups gives

    dim_F2 H(K;F2) = dim_Q H(K;Q) + 2 t(K),               (2.1)
    dim_F2 V(K;F2) = r(K) + 2 a(K).                       (2.2)

To see the factor 2 directly, a 2-primary cyclic factor in integral cohomological degree i contributes once through tensor product in degree i and once through Tor in degree i-1. Odd-primary factors contribute neither. This also explains why merely testing the first Bockstein cannot replace the rank gap.

Choose a basepoint and set A=Z[X]/(X^2), with the basepoint action X lowering quantum degree by 2. The Khovanov complex is termwise free as an A-module. The reduced complex may be written as C/XC with the normalizing quantum shift. The short exact sequence

    0 -> reduced C{-1} -> C -> reduced C{+1} -> 0

has a rational connecting map

    delta_K : V^{i,j}(K;Q) -> V^{i+1,j+2}(K;Q).

Let rho(K) be its total rank. Finite-dimensional exactness, summed over the gradings, gives

    dim_Q H(K;Q) = 2 r(K) - 2 rho(K).                    (2.3)

Over F2, unreduced homology splits as two quantum-shifted copies of reduced homology [S14, Corollary 3.2.C]. Combining this with (2.1)–(2.3) proves the exact identity

    t(K) = 2 a(K) + rho(K).                              (2.4)

In particular,

    H(K;Z) has no element of order 2
      if and only if a(K)=0 and delta_K=0.               (2.5)

This is an exact reformulation, not a solution: there is no proof here that the two quantities on the right cannot vanish simultaneously for a nontrivial prime knot.

### 2.2 Bar–Natan interpretation

For a knot, rational reduced Bar–Natan homology has one free Q[H]-summand and finitely many torsion summands Q[H]/(H^b). Let m(K) count all torsion summands, and let s1(K) count those with b=1. The mapping-cone formulas in [KWZ19, Proposition 9.3 and its proof] give

    r(K)=1+2m(K),
    dim_Q H(K;Q)=2+4m(K)-2s1(K).

Consequently rho(K)=s1(K), and (2.4) becomes

    t(K)=2a(K)+s1(K).                                   (2.6)

The stronger proposed route “every nontrivial knot has an H-length-one summand” is already explicitly posed as [KWZ19, Question 9.4]. It must not be presented as an established lemma. In particular, torsion of higher H-length alone does not prove 2-torsion by this argument. H-torsion over Q[H] and integer 2-primary torsion are different notions.

### 2.3 Exact outcome and obstruction

The approach gives the complete nonnegative torsion budget (2.4), and a specific dichotomy that a proof must force: reduced 2-primary torsion or a nonzero rational connecting map. Unknot detection only says that r(K)>1 for a nontrivial knot; it does not by itself force either term of that dichotomy. For instance, the formal Bar–Natan module

    Q[H] plus three copies of Q[H]/(H^2)

has r=7 and unreduced rational rank 14, with s1=0. Setting a=0 violates none of these numerical identities. This is an algebraic profile, not an asserted knot realization or a counterexample.

## 3. Approach II: Bockstein and Turner spectral sequences

### 3.1 A conditional route that does work

If t(K)=0, every integral 2-primary Bockstein differential is zero. In particular the first Bockstein beta is zero. Shumakovitch's identity on H(K;F2) is

    d_T^* = beta nu^* + nu^* beta,                        (3.1)

where nu^* has bidegree (0,2) [S18, Lemma 3.2.A]. It follows that the first Turner differential is zero. If, in addition, the Turner spectral sequence collapses at E2, then

    dim_F2 H(K;F2)=dim_F2 E_infinity=2.

The characteristic-two reduced splitting gives dim_F2 V(K;F2)=1; UCT gives r(K)<=1, and the reduced Euler characteristic at 1 makes r(K) nonzero. Reduced rational unknot detection then implies that K is the unknot. Thus any nontrivial knot for which Turner collapses at E2 has 2-torsion. In particular, this applies in the F2-homologically-thin setting, where the required collapse is established in [S18, Theorem 2.3.A]. This recovers a known class rather than solving the general case.

### 3.2 Why the first-page identity does not finish the argument

Here is an explicit double-complex obstruction, entirely independent of a knot table. Use free abelian generators

    a at (0,0), c at (0,2), b at (1,2), e at (1,4).

Define d(c)=b and d(a)=d(b)=d(e)=0. Over F2 define T(a)=b, T(c)=e, T(b)=T(e)=0. Then d and T have degrees (1,0) and (1,2), both square to zero, and commute over F2. The integral d-homology is free on [a] and [e]. The map induced by T on it is zero, since T(a)=d(c). Nevertheless the higher zigzag is nonzero:

    a --T--> b <--d-- c --T--> e,

so the second Turner-type differential maps [a] to [e]. Equivalently, the matrix of d+T from span(a,c) to span(b,e) is invertible over F2.

Duplicate this block with quantum degree shifted by 2 and pair the two copies by nu. The reverse pairing X satisfies Xnu+nuX=id, and both maps commute with d; nu is acyclic. All first Bocksteins remain zero. Add a surviving two-generator nu-pair. The first page has dimension 6 and the limiting homology dimension 2, with a zero first differential. Using three doubled blocks gives dimensions 14 and 2 instead. Thus even several relevant algebraic constraints permit higher-page cancellation without integral 2-torsion.

These are abstract complexes, not Khovanov complexes of claimed knots. Their purpose is precise: (3.1), characteristic-two splitting, free integral homology, and the two-dimensional limit do not alone justify collapse at E1 or E2. A further knot-specific theorem ruling out such higher-page behavior under t=0 is missing.

There is a second elementary pitfall: Z --4--> Z has zero first Bockstein but a homology element of order 2. The exact check covers orders 2,4,8,16. “beta=0 implies no 2-torsion” is false even for finite free complexes.

## 4. Approach III: rational-tangle rank descent

### 4.1 A quantitative module lemma

Let R=F[H] and let M and N be finite direct sums of free R-modules and modules R/(H^b). Suppose R-linear f:M->N and g:N->M satisfy

    gf=H on M,       fg=H on N.

Let m and n be the numbers of torsion summands in M and N. Let s count the summands R/(H) in M. Then

    m-s <= n.                                           (4.1)

Proof. Put W=ker(H:M->M) intersect HM. Each torsion summand of length at least 2 contributes one dimension to W, while a free summand or length-one summand contributes none. Hence dim_F W=m-s. Let C=g^{-1}(ker H_M). It is H-stable. If z belongs to C, then g(Hz)=0, and applying f gives H^2 z=0. Thus C is finite-dimensional, even if N has a free summand.

For y in W, write y=Hx. Then y=g(f(x)), and f(x) belongs to C. Thus W is contained in g(C). Also g(HC)=0, so

    dim W <= dim g(C) <= dim(C/HC)
           = dim ker(H|C) <= dim ker(H|N)=n.

This proves (4.1). No classification of module homomorphisms is being assumed. The published lemma in [GW25] is the special case s=0. The proof here retains the contribution of the length-one bars.

### 4.2 Quantitative torsion bound

The proper rational tangle replacement maps used by Gujral–Wang have these composition properties on rational reduced Bar–Natan homology [GW25; ILM25]. Apply (4.1) and then (2.6). If J is obtainable from K by one proper rational tangle replacement, then

    s1(K) >= max(0,m(K)-m(J)),
    t(K) >= 2a(K) + max(0,(r(K)-r(J))/2).                (4.2)

In particular a strict decrease of reduced rational rank forces 2-torsion, with the stated lower bound on the number of 2-primary cyclic factors. This is an authored quantitative consequence of the cited framework; no novelty claim is made.

If J is the unknot, then r(J)=1 and (4.2) gives t(K)>0 for nontrivial K by unknot detection. This recovers the one-replacement argument. The separate trefoil-detection argument in [GW25] excludes a torsion-free nontrivial K with r(K)<=3 and yields their stronger trefoil-neighbor corollary.

### 4.3 Why arbitrary unknotting paths do not solve the problem

Every knot has a finite crossing-change path to the unknot, and a crossing change is a proper rational tangle replacement. But (4.2) constrains a knot at which a rank-decreasing step occurs. It does not move torsion backward through earlier rank-increasing steps. A hypothetical torsion-free starting knot would be a weak local minimum of r among all its one-replacement neighbors. There is no established result used here that every nontrivial knot has a lower-rank such neighbor.

Composing maps along d replacements gives maps whose composites are H^d. Since all torsion maps to zero under a map into the free module BN(unknot), this forces every H-torsion exponent of BN(K;Q) to be at most d. Combining with t(K)=0 forces those exponents to lie between 2 and d. In particular, a hypothetical torsion-free knot of proper rational unknotting number 2 must have all its H-torsion bars of length exactly 2. This is a restriction, not an impossibility: for M=R plus R/(H^2) and N=R, take f to be H^2 times projection to the free summand and g to be inclusion; the compositions are H^2.

The missing global rank-descent theorem, or an obstruction to these length-two profiles being realized by knots, is exactly where this approach stops.

## 5. Approach IV: construct an integral order-two cycle and preserve it

### 5.1 A local certificate

For a finite free integral cochain complex C, suppose x is in C^{i-1}, v is in C^i, and dx=2v. Then dv=0, since C^{i+1} is torsion-free. If there is a homomorphism

    lambda:C^i -> F2,   lambda d=0,   lambda(v)=1,

then v is not an integral boundary and [v] has exact order 2. This proves a local chain-level certification criterion.

The parity functional is an essential part of the argument; finding dx=2v alone is insufficient. Moreover the criterion is stronger than the target in one respect: it detects an order-two class nonzero modulo 2 in integral homology. In a Z/4 summand the order-two element is divisible by 2 and has no such parity certificate.

One elementary source of factors 2 is an odd unsigned incidence cycle. For a connected graph, impose the relations u+v=0 for each edge. A spanning tree expresses every vertex as plus or minus one root. If the graph is bipartite the quotient is Z; otherwise an odd cycle imposes precisely 2 times the root=0 and the quotient is Z/2. For an n-cycle, the Smith diagonal is (1,...,1,2) if n is odd and (1,...,1,0) if n is even. These exact matrices are checked for n=3 through 8.

Adequate-state and ladder constructions exploit structured parts of the Khovanov differential. The recent sufficient conditions [DM25, Theorem 8 and Corollary 10] include ladder height, a periphery condition, and constraints on the remaining smoothing arcs. They do not say that every nontrivial knot has an admissible diagram. We found no proof of that missing assertion.

### 5.2 The extension obstruction in a skein induction

The natural induction would resolve a crossing, find a torsion class in a simpler resolution, and keep it in the original complex. A short exact sequence 0->A->B->C->0 instead allows the connecting homomorphism H^{i-1}(C)->H^i(A) to kill that class.

This can happen in the smallest possible free-complex example:

    A : Z --2--> Z,
    B : Z^2 --[2,1]--> Z,
    C : Z in degree 0.

Embed the domain of A as the first coordinate of B and its target identically. This is a degreewise split short exact sequence. Here H^1(A)=Z/2, but H^0(B)=Z and H^1(B)=0. The connecting map H^0(C)=Z -> H^1(A)=Z/2 is surjective, because a lift of 1 has differential 1. Thus the entire torsion class disappears.

This is not a knot counterexample. It disproves the unqualified homological step that a skein induction would need. A valid induction must show, in the relevant shifted bidegree, that the connecting-map image does not meet the selected order-two subgroup. Neither nontriviality of the knot nor existence of a cycle in an arbitrary smoothing establishes that. The parity certificate and its survival, rather than the visual presence of a twist, remain the central obstruction.

## 6. Approach V: propagate through connected sums and reduce to prime knots

This route gives an exact reduction rather than a universal proof.

### 6.1 Connecting maps under tensor product

Use basepoints on connected-sum diagrams. Directly from the cube of resolutions and the basepoint Frobenius algebra, up to the normalizing shifts,

    C(K#J) = C(K) tensor_A C(J),
    reduced C(K#J) = reduced C(K) tensor_Z reduced C(J).

For completeness, a resolution of a connected sum joins exactly the two marked circles; their two A-factors become one factor by tensoring over A. All other circle factors remain unchanged. An edge belonging to either diagram applies its Frobenius map to that factor, with the usual tensor-product sign. This identifies the chain groups and all differentials.

Choose homogeneous A-bases and write d_K=d_K^0+X d_K^1. Modulo X the differential is d_K^0. Lifting a reduced cycle and taking its differential shows that the connecting map is induced by d_K^1. The equation d_K^2=0 implies d_K^0 d_K^1+d_K^1 d_K^0=0, so this induced map is well-defined. The tensor differential gives, on rational reduced homology,

    delta_{K#J}(x tensor y)
      = delta_K(x) tensor y + (-1)^{i(x)}x tensor delta_J(y).   (6.1)

If delta_K is nonzero, take a homogeneous x on which it is nonzero and any nonzero homogeneous y in V(J;Q). The first term in (6.1) lies in factorwise homological degrees (i(x)+1,i(y)); the second lies in (i(x),i(y)+1). They cannot cancel in the direct-sum Kunneth decomposition. Thus delta_{K#J} is nonzero. The same argument applies to delta_J. Conversely both zero implies their tensor-sum zero. Consequently

    rho(K#J)=0 if and only if rho(K)=rho(J)=0.             (6.2)

Only vanishing is asserted here; ranks of tensor sums are not generally additive.

### 6.2 Reduced torsion under connected sum

Let r_K,r_J be reduced rational ranks and a_K,a_J the reduced 2-primary counts. Field Kunneth and (2.2) give

    a(K#J)=a_K r_J + a_J r_K + 2a_K a_J.                 (6.3)

Both rational ranks are positive: the reduced Euler characteristic evaluated at q=1 is 1 for knots. Hence a(K#J)=0 if and only if a_K=a_J=0. Combining (6.2), (6.3), and (2.4) proves

    Kh(K#J;Z) has 2-torsion
      if and only if Kh(K;Z) or Kh(J;Z) has 2-torsion.     (6.4)

In particular, the universal conjecture is equivalent to its restriction to nontrivial prime knots. Every counterexample would have a nontrivial prime counterexample as a summand. This closes the connected-sum part of the induction but gives no decomposition of a prime knot into easier knots. The analysis therefore stops at that geometric barrier.

## 7. Reproducible checks and limitations

Run `python verify_exact.py` in this directory. It uses Python and SymPy, with no network access, external knot table, or source dataset. The recorded run used SymPy 1.14.0 and passed every explicit check. These checks use exceptions rather than Python assertions and remain active under `-O` and `-OO`.

The script constructs the entire integer cube-of-resolutions differential, by quantum grading, for the positive two-strand braid closures with 1, 3, and 5 crossings. It verifies d squared is zero and uses exact ranks over Q and F2. The resulting total dimensions are:

| Knot | unreduced Q | unreduced F2 | reduced Q | reduced F2 | t | rho |
|---|---:|---:|---:|---:|---:|---:|
| T(2,1), the unknot | 2 | 2 | 1 | 1 | 0 | 0 |
| T(2,3), a trefoil | 4 | 6 | 3 | 3 | 1 | 1 |
| T(2,5), a cinquefoil | 6 | 10 | 5 | 5 | 2 | 2 |

For example, the trefoil's unreduced rational generators have bidegrees (0,1), (0,3), (2,5), and (3,9); the additional F2 dimensions occur in (2,7) and (3,7). These calibrate coefficient conventions, normalization, and the total-rank identity. They are not new torsion examples.

The script also checks the Bockstein examples, the skeletal Turner zigzag, the torsion-killing short exact sequence, odd/even incidence Smith forms, a sharp finite-dimensional module-lemma example, and a sample tensor connecting map. These finite checks support the displayed algebra; they do not establish the universal conjecture, knot realizability of formal profiles, generic spectral-sequence collapse, or universal diagrammatic pattern existence. The connected-sum result is proved in Section 6, not inferred from a finite sample.

## 8. Precise remaining problem

A hypothetical counterexample can be taken prime. It must satisfy all of the following necessary conditions:

1. Its reduced integral homology has no 2-primary torsion.
2. Its rational reduced/unreduced connecting map vanishes, equivalently its rational reduced Bar–Natan module has no H-length-one torsion summand.
3. Its reduced rational rank is at least 5, by the unknot and trefoil detections invoked in [GW25].
4. It is a weak local minimum of reduced rational rank under proper rational tangle replacement.
5. Its Turner spectral sequence has a nonzero higher differential, since the first differential is zero but the first-page dimension exceeds 2.
6. If d proper rational replacements unknot it, all of its rational Bar–Natan torsion exponents lie in [2,d].

No contradiction among these conditions was established. In particular, replacing “unknown realizability” by “impossible” would be an unsupported proof step. The finished outcome is five mathematical attempts with rigorous partial consequences and identified barriers, not a solution of KP-1.30.

## References

- [K3] R. Inanc Baykur, Robion C. Kirby, and Daniel Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, author's preliminary AMS version; Problem 1.30, printed pp. 35–36. [Author-hosted PDF](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf).
- [S14] Alexander N. Shumakovitch, *Torsion of Khovanov homology*, Fundamenta Mathematicae 225 (2014), 343–364. [DOI](https://doi.org/10.4064/fm225-1-16); [inspected arXiv v2](https://arxiv.org/abs/math/0405474v2).
- [S18] Alexander N. Shumakovitch, *Torsion in Khovanov homology of homologically thin knots*. [Inspected arXiv v1](https://arxiv.org/abs/1806.05168v1). Published in Journal of Knot Theory and Its Ramifications 30 (2021), no. 14, 2141015, [DOI](https://doi.org/10.1142/S0218216521410157).
- [KWZ19] Artem Kotelskiy, Liam Watson, and Claudius Zibrowius, *Immersed curves in Khovanov homology*, [arXiv:1910.14584v2](https://arxiv.org/abs/1910.14584v2), especially Proposition 9.3, Question 9.4, and Corollary 9.5.
- [GW25] Onkar Singh Gujral and Joshua Wang, *A minimality property for knots without Khovanov 2-torsion*, Algebraic & Geometric Topology 25 (2025), 4073–4075. [Publisher PDF](https://msp.org/agt/2025/25-7/agt-v25-n7-p10-p.pdf); [DOI](https://doi.org/10.2140/agt.2025.25.4073).
- [ILM25] Damian Iltgen, Lukas Lewark, and Laura Marino, *Khovanov homology and rational unknotting*, [arXiv:2110.15107v2](https://arxiv.org/abs/2110.15107v2), revised 10 July 2025. The maps needed here are also explicitly stated in the proof of [GW25, Theorem 1].
- [DM25] Raquel Diaz and Pedro M. G. Manchon, *New torsion patterns in Khovanov homology*, [arXiv:2508.00606v1](https://arxiv.org/abs/2508.00606v1), especially Theorem 8 and Corollary 10.

All source-dependent claims are distinguished from the authored algebraic deductions. The source metadata file records exact inspected PDF hashes, byte counts, versions, and retrieval information without reproducing their contents.
