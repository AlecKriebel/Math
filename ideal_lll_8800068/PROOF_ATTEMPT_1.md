# Proof attempt 1: a precise target and a triangular obstruction

Date: 2026-10-20 UTC. Problem ID 8800068 / AMR-087-0068.

## Result and scope

**Target not solved.** A standard precise lower-bound formulation is adopted below, so author-omitted conventions no longer prevent mathematical work. The direct transplantation of a standard near-critical triangular LLL basis fails for every monic quotient polynomial. In fact, a coefficient-ordered triangular ideal basis that is classically LLL-reduced must be a scalar coordinate basis. This is a proved restricted obstruction, not an upper bound for arbitrary ideal-lattice reduced bases and not a resolution of the historical question.

No claim of novelty is made for the elementary lemma.

## 1. Chosen target, including exact quantifiers

Seek an unbounded sequence of dimensions n_k, monic polynomials q_k in Z[X] of degree n_k, full-rank ideals I_k of R_k=Z[X]/(q_k), and ordered Z-bases B_k=(b_1,...,b_n) of their coefficient lattices L_k in Z^n. The coefficient map uses the ordered basis (1,X,...,X^{n-1}) and ordinary Euclidean norm, with no freely chosen change of metric.

Each B_k must be (delta,eta)=(3/4,1/2)-LLL-reduced, and

    liminf_{k -> infinity} (1/n_k) log_2(||b_1|| / lambda_1(L_k)) >= 1/2.

Equivalently, along this sequence the lower bound is 2^{(1/2-o(1))n_k}. Since the classical general upper bound is 2^{(n-1)/2}, this matches its exponential rate. A stronger desirable construction would have a fixed c>0 and ratio at least c 2^{(n-1)/2}, but that constant-factor assertion is not silently included in the rate target.

LLL-reduced here means |mu_ij|<=1/2 for every j<i and

    ||b_i^*||^2 + mu_{i,i-1}^2 ||b_{i-1}^*||^2 >= (3/4)||b_{i-1}^*||^2.

The existential basis itself may be supplied as input to an exact classical LLL routine which performs size reduction only when |mu|>1/2 and swaps only on strict failure of Lovasz. It is then stationary. This convention avoids a hidden tie-breaking assertion. It is not an HNF-start construction, a statement about every input basis, or a claim that the ideal is hard for every algorithm.

The target permits q_k to vary, including reducible q_k, and does not require principal ideals. Cyclic q_k=X^{n_k}-1, negacyclic q_k=X^{n_k}+1, irreducible/cyclotomic restrictions, and specified HNF-start behavior are stronger targets. A result for this broad target alone would have to be labeled as such rather than advertised as settling every reading of the 2006 question. The output measure is the first vector, not the shortest returned basis vector and not the determinant-normalized Hermite factor.

## 2. Source and status check

The historical source and model were checked against the recovered local text of Micciancio's 2006 slides, with the source audit in SOURCE_GATE.md. The source question is on PDF page 37; coefficient ideal lattices are described on PDF page 23. Public primary source:

https://helper.ipam.ucla.edu/publications/SCWS1/SCWS1_6240.pdf

The fixed-parameter convention and the distinct SVP/Hermite guarantees are given by Nguyen and Stehle, LLL on the Average (corrected version), section 2:

https://perso.ens-lyon.fr/damien.stehle/downloads/average-corrected.pdf

Targeted web searches on 2026-10-20 combined “ideal lattices”, “cyclic lattices”, “LLL”, “critical bases”, “reduced basis”, “worst-case approximation factor”, and recent-year terms. They did not locate a primary theorem giving the chosen family or excluding it. This is a bounded search report, not a proof of open status through 2026. Search-engine crawl/publish labels were not accepted as publication dates.

The recovered author-hosted Plantard–Susilo–Zhang paper was inspected again. Its Theorem 2 concerns the reducedness/correctness of iLLL, not a matching approximation lower-bound family; its 2014 acceptance date is printed on the first page:

https://thomas-plantard.github.io/pdf/PlaSusZha14.pdf

A newer related primary work, Kirchner–Espitau–Fouque, Algebraic and Euclidean Lattices: Optimal Lattice Reduction and Beyond, was inspected at its abstract and introduction. It concerns efficient algebraic/module reduction, heuristic approximation bounds and applications, rather than supplying the target extremal first-vector family:

https://eprint.iacr.org/2019/1436.pdf

Buchmann–Lindner, Density of Ideal Lattices, preliminary draft (Dagstuhl 2009), was inspected to check a possible density-transfer route. Its counting comparison fixes a number field/order and does not imply density of the union of coefficient ideals with arbitrary q near every Euclidean lattice shape. It therefore does not license transferring a general critical basis into an ideal lattice by perturbation:

https://d-nb.info/1367234891/34

## 3. General-lattice candidate

For n>=2 choose rational t_n with

    1/sqrt(2) < t_n < min(1, (1+1/n^2)/sqrt(2)).

Such a rational exists by density of Q. Let e_0,...,e_{n-1} be the fixed coefficient coordinate vectors. Define rational basis vectors

    b_1=e_0,
    b_i=(1/2)b_{i-1}+t_n^{i-1}e_{i-1},  2<=i<=n.

Clear all denominators using a common positive integer D_n and put c_i=D_n b_i. This makes an integral full-rank basis and leaves every ratio and reduction condition unchanged.

Its GSO is b_i^*=t_n^{i-1}e_{i-1}; its coefficients are mu_ij=2^{-(i-j)}. Hence it is size-reduced and strictly satisfies Lovasz because t_n^2+1/4>3/4. Its first norm is 1, whereas

    2b_n-b_{n-1}=2t_n^{n-1}e_{n-1}

is a nonzero lattice vector. Therefore

    ||b_1||/lambda_1(L(B)) >= 1/(2t_n^{n-1})
       > (1/2) 2^{(n-1)/2}(1+1/n^2)^{-(n-1)}.

This is a constant-factor near-worst-case family of general integral lattices after scaling. It is a valid control construction, but it is **not** an ideal-lattice solution.

## 4. Exact ideal-membership obstruction

### Proposition

Let q in Z[X] be any monic polynomial of degree n. Let L be the coefficient image of a full-rank ideal in Z[X]/(q). Suppose an ordered basis B=(b_1,...,b_n) has

    b_i in span_R(e_0,...,e_{i-1}),
    coefficient of e_{i-1} in b_i = d_i > 0,

and is (3/4,1/2)-LLL-reduced. Then for a positive integer a,

    L=a Z^n and b_i=a e_{i-1} for every i.

In particular its first-vector/SVP ratio is 1.

### Proof

For i<n, the polynomial represented by b_i has degree i-1. Multiplication by X has degree i<n, so there is no reduction modulo q in Xb_i. Ideal closure gives Xb_i in L. In its unique integral expansion in B, coefficients of b_{i+2},...,b_n must vanish by examining coordinates from highest to lowest. Comparing the e_i coordinate then gives

    d_i/d_{i+1} in Z_{>0}.

Because the first i basis vectors span the first i coordinate directions, GSO gives b_i^*=d_i e_{i-1}. If the positive integer d_i/d_{i+1} were at least 2, then

    d_{i+1}^2 + mu_{i+1,i}^2 d_i^2
       <= (1/4+1/4)d_i^2
       < (3/4)d_i^2,

contradicting Lovasz. Thus every ratio is 1 and d_i=a for all i.

Now b_1=a e_0, and ideal closure under the first n-1 powers of X gives a e_j in L for each j. Thus a Z^n is contained in L. Their determinants are both a^n, so their index is 1 and L=a Z^n. Each b_i has coefficients divisible by a; because its GSO is a e_{i-1}, all mu_ij are integers. Size reduction |mu_ij|<=1/2 forces them all to be zero. This proves the proposition.

### Application to the candidate

The scaled candidate is coefficient-ordered triangular with diagonal d_i=D_n t_n^{i-1}, not all equal. It therefore cannot be an ideal lattice for **any** monic q of degree n. One can see the failure already from Xc_1: its expansion would require coefficient 1/t_n on c_2, but 1<1/t_n<sqrt(2), which is not an integer. Changing the final column of the companion matrix, i.e. changing q, cannot repair this failure because no wraparound occurs in Xc_1.

This reasoning does not assume q is irreducible, cyclic, or cyclotomic. It also does not assume the ideal is principal.

## 5. What remains, and what does not follow

1. The construction satisfies all metric/reduction/rate requirements but fails ideal membership. The gap is not a missing denominator clearance or a basis tie convention; it is the proved multiplication-by-X obstruction.
2. A successful ideal construction must use a reduced basis that is not triangular in the fixed increasing-degree coefficient flag, unless it is the trivial scalar coordinate basis. Arbitrary orthogonal rotations can remove triangular shape but generally destroy coefficient ideal closure. An explicit proof of closure would still be required.
3. The proposition does not assert that LLL started at HNF returns a triangular basis. Swaps and reductions can leave the coefficient flag. Accordingly it proves neither good HNF-start performance nor a general impossibility theorem for ideals.
4. It remains possible that a nontriangular reduced basis of an ideal satisfies the chosen sharp rate. No such family is established here, and no upper bound excluding it is established here.
5. Fixed-order counting sparsity, cyclic quotient groups, and general-lattice perturbation arguments do not by themselves fill that gap.

Attempt outcome: **one proof attempt completed; general target unresolved; direct triangular transfer refuted; restricted structural lemma established.**

## 6. Verification and important target bifurcation

The elementary triangular proof was independently checked by a second mathematical pass. Its hypothesis is precisely the increasing-degree support condition in section 4. It is not invariant under arbitrary coordinate permutations and must not be described merely as “triangular” without that qualification.

The accompanying computation/check_attempt_1.py was run successfully for n=2,...,16 using exact rational arithmetic. It checks the rational choice of t, GSO, strict Lovasz inequalities, denominator clearance, the explicit short vector, and the nonintegral coefficient obstructing X-stability. These are finite sanity checks; the written arguments supply the universal proofs.

A separate symmetry argument clarifies why the historical ambiguity really matters. If multiplication by X acts orthogonally and the orbit of a shortest vector spans dimension n, its n orbit vectors give an independent sublattice with determinant at most lambda_1(L)^n by Hadamard. Thus det(L)^{1/n}<=lambda_1(L), and the LLL Hermite guarantee yields

    ||b_1||/lambda_1(L) <= 2^{(n-1)/4}.

In power-of-two degree q=X^n+1, multiplication by X is orthogonal and irreducibility ensures every nonzero orbit spans, so the SVP exponent-1/2 target is impossible in that subclass. A sharp Hermite-factor target is therefore genuinely different, not a cosmetic alternative convention. Cyclic q=X^n-1 is reducible, so the orbit-spanning premise cannot be silently assumed there. General monic q has neither orthogonality nor irreducibility guaranteed. This observation does not settle the broad varying-q target chosen above, but must accompany any account of its scope.
