# A four-element negative answer to the representable-polymatroid rank-sum question

## Result and credit

Complete negative answer accepted by the accompanying [mathematical audit](MATHEMATICAL_AUDIT.md). This AI-assisted manuscript and audit are unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. No novelty or priority is claimed.

The answer to problem 30004007 / OWR-16633-025 is **no**. In fact, over every field there is a representable polymatroid on four elements which is outside the nonnegative-real cone of **all** matroid rank functions on those four elements.

The principal counterexample below is the budget-additive counterexample already given by Shaddin Dughmi, Tim Roughgarden and Qiqi Yan, *From Convex Optimization to Randomized Mechanisms: Toward Optimal Combinatorial Auctions*, full author version dated 16 April 2011, §D.2, printed p. 22. Their Definition 2.1 explicitly allows nonnegative **real** weights, and Claim 4.5 proves a necessary discrete-Hessian condition. We provide an explicit all-field subspace representation, a short direct proof and an exact separating functional. This is a credited application to the question as printed by László Végh, not a claim to have discovered the counterexample.

- Original question: https://ems.press/content/serial-article-files/46772 , printed p. 3018, PDF p. 50.
- Prior counterexample: https://theory.stanford.edu/~shaddin/papers/convex-current.pdf , Definition 2.1, Claim 4.5 and §D.2.
- Stable manuscript reference: https://arxiv.org/abs/1103.0040v3 .

## 1. Explicit representation over the unchanged field

Fix any field F. Set V={a,b,c,d}, and use the following subspaces of F²:

T_a=F²,   T_b=F(1,0),   T_c=F(0,1),   T_d=F(1,1).

Let g(S)=dim_F(sum_{v∈S}T_v). The three lines are pairwise distinct over every field, including F₂: the determinants of their three pair matrices are 1, 1 and −1. Consequently

g(S)=min(2, 2·1_{a∈S}+|S∩{b,c,d}|).

In particular, g(∅)=0, g(a)=2, g(b)=g(c)=g(d)=1, and every set of at least two elements has value 2. This is an integer-valued, normalized, monotone, submodular function, because it is the dimension function of the displayed subspaces. No extension of F and no change to V is used.

## 2. Direct obstruction to arbitrary nonnegative real coefficients

Suppose g=Σ_k λ_k r_k, where λ_k≥0 are real numbers and each r_k is the rank function of a matroid on V. Discard zero coefficients. For each i∈{b,c,d}, monotonicity gives r_k(ai)−r_k(a)≥0. Since g(ai)−g(a)=0, every positive-weight summand satisfies

r_k(ai)=r_k(a).                                             (1)

For distinct i,j∈{b,c,d}, subadditivity gives r_k(i)+r_k(j)−r_k(ij)≥0. Since g(i)+g(j)−g(ij)=0, every summand satisfies

r_k(ij)=r_k(i)+r_k(j).                                      (2)

Fix one summand r. If r(a)=0, equation (1) and monotonicity force r(b)=r(c)=r(d)=0. If r(a)=1, each nonloop among b,c,d is parallel to a, by (1). Any two such nonloops would be parallel to each other, and hence have pair rank 1, contrary to (2). Thus at most one of b,c,d is a nonloop. In both cases,

r(b)+r(c)+r(d)≤r(a).

Multiplying by λ_k and summing would give 3≤2. This contradiction rules out every nonnegative real decomposition. The argument does not assume representability of the summand matroids; it therefore rules out the required same-field linear matroids in particular.

For completeness, the transitivity used here follows from submodularity: if r(a)=r(i)=r(j)=r(ai)=r(aj)=1, then r(aij)≤r(ai)+r(aj)−r(a)=1, so r(ij)=1.

## 3. A universal exact separating inequality

For any set function h with h(∅)=0, define

L(h)=−5h(a)+3[h(b)+h(c)+h(d)]
     +2[h(ab)+h(ac)+h(ad)]−2[h(bc)+h(bd)+h(cd)].             (3)

Then every matroid rank function r on V satisfies L(r)≥0, whereas L(g)=−1.

Here is a universal proof, so no representable-matroid enumeration is needed. Let x_a=−1 and x_b=x_c=x_d=1. Form the matrix

H_r(i,j)=r({i,j})−r(i)−r(j).

The diagonal entry is −r(i). A row or column belonging to a loop is zero. On the nonloops, an entry is −1 exactly when the two elements are parallel (including the diagonal), and is zero otherwise. The nonloops partition into parallel classes C. Therefore

−xᵀH_r x=Σ_C (Σ_{i∈C}x_i)²≥0.

Expansion of the left side gives exactly L(r). For g, H_g has diagonal (−2,−1,−1,−1), off-diagonal entries −1 between a and each other element, and zero between distinct elements of {b,c,d}. Hence xᵀH_g x=−2+6−3=1, and L(g)=−1 as claimed.

By linearity, L≥0 on the entire nonnegative real rank cone and its closure. Thus even limits of nonnegative rank sums cannot equal g. This specializes the discrete-Hessian obstruction in Dughmi–Roughgarden–Yan, Claim 4.5 and §D.2, to an explicit integer separating functional.

## 4. A second, independently derived all-field witness

The budget-3 function

f(S)=min(3, 2·1_{a∈S}+|S∩{b,c,d}|)

also has an all-field representation in F³:

U_a=span(e₁,e₂),   U_b=F e₃,
U_c=F(e₁+e₃),     U_d=F(e₂+e₃).

The last three generating vectors form a basis, and each is outside U_a. It follows immediately that the displayed dimension function is f.

For this f, the following nonnegative polymatroid slacks all vanish:

- h(a)+h(i)−h(ai), for i=b,c,d;
- h(V)−h(ai), for i=b,c,d;
- h(b)+h(c)+h(d)−h(bcd);
- h(V)−h(bcd).

If f were a nonnegative real rank sum, each positive-weight rank summand r would make each slack zero. Then r(b)=r(c)=r(d)=t, r(V)=3t and r(a)=2t. But t is 0 or 1 and r(a) is 0 or 1; hence t=0 and r is identically zero. This contradicts f(V)=3.

For a separate explicit separator put

E(h)=3h(a)+2Σ_{i=b,c,d}h(i)−2Σ_{i=b,c,d}h(ai)
     +4h(V)−2h(bcd),
K(h)=4E(h)−h(V).

E is the sum of the eight slacks above. A nonzero matroid rank has E(r)≥1 because E is integer-valued and E(r)=0 forces r=0. Also r(V)≤4. Thus K(r)≥0 for every matroid rank, while K(f)=−3.

The relation to the credited witness is exact:

g(S)=f(V\S)+Σ_{v∈S}f(v)−f(V),
f(S)=g(V\S)+Σ_{v∈S}g(v)−g(V).

We do not need an unproved assertion about preservation of a rank cone by this singleton-weighted duality: both obstructions above are proved directly. No originality is claimed for this variant.

## 5. Ground-set minimality

Four is the smallest possible ground-set size, even if the input is any real-valued normalized monotone submodular function, rather than a representable one. Here is a direct three-element decomposition using matroids representable over every field.

Write the three elements as 1,2,3, and h_{12}=h({1,2}), etc. Define

p₁=h_{123}−h_{23}, and similarly p₂,p₃;
q_{12}=h_{13}+h_{23}−h_3−h_{123}, and similarly q_{13},q_{23};
t=h_1+h_2+h_3−h_{12}−h_{13}−h_{23}+h_{123}.

All p_i and q_ij are nonnegative. Moreover q_ij+t=h_i+h_j−h_ij≥0. For nonempty A⊆{1,2,3}, let u_A(S)=1 if S meets A, and 0 otherwise. Each u_A is a rank-one matroid rank with nonloops A, representable over every field. Let r₂(S)=min(2,|S|), represented by (1,0),(0,1),(1,1).

If t≥0, then

h=Σ_i p_i u_{ {i} }+Σ_{i<j}q_ij u_{ {i,j} }+t u_{ {1,2,3} }.

If t<0, put k=−t. Then q_ij−k≥0 and

h=Σ_i p_i u_{ {i} }+Σ_{i<j}(q_ij−k)u_{ {i,j} }+k r₂.

Both identities follow by evaluation on the seven nonempty subsets. They apply to arbitrary real coefficients. Smaller ground sets follow by adding loops and restricting. Thus the four-element all-field witness has minimum possible ground-set size. Also its ambient dimension 2 is minimum: in dimension at most 1, the subspace rank is itself a rank-one matroid rank (or zero).

## 6. Verification and exact scope

Historical supplementary checks in the author package verified both complete 16-entry rank tables, produced unit-minor certificates valid in every characteristic, and checked all rank axioms. They enumerated all 2^15 set systems on four elements containing ∅, filtered by hereditary closure and augmentation, and obtained all 68 labeled matroids. Both separators and both equality-forcing arguments were checked against every one, not a sampled representable subset. The checks also covered the universal parallel-class identity, exact duality, the algebraic three-element decomposition, positive controls and negative mutation controls. These computations are recorded as historical supplementary evidence; no mathematical conclusion here depends on an omitted executable or certificate.

The complete proof is Sections 1–3; it is independent of enumeration and numerical optimization. Section 4 proves a separate dual witness directly. Section 5 is an optional sharpness supplement. The original question has no common-dimension restriction and the all-field representation respects its printed hypotheses. No claim is made about enlarged-ground-set representations or approximations, which are different problems.

This proof-only edition distributes no programs, raw outputs, generated certificates or datasets, copied third-party source documents/text/images, or private coordination material. Edition preparation rechecked frozen byte identities and publication integrity; it did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection or literature search.
