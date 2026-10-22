# A literal counterexample to the proposed threshold scenarios

**30005310 / OWR-11695865-009. Complete source-literal negative-answer candidate, author turn1; independent review pending.** This is a consequence of elementary completion constructions and credited existing threshold results, not a claim of a new Gaussian-model discovery.

## 1. Precisely what is answered

The [2022 Oberwolfach report](https://ems.press/content/serial-article-files/46992), Roser Homs with Olga Kuznetsova, printedpp3146-3149, defines colored linear concentration models, the sufficient-statistic projection pi_G, and the elimination ideal I(G,n). Proposition3 assumes

    I(G,n+1)=0,    I(G,n) nonzero.                        (1)

Its second bullet then asserts WMLT(G)=n when a positive-definite S0 has statistics in V(I(G,n)); both listed threshold scenarios have WMLT at leastn. Conjecture4 says these are the only scenarios. The supplied cleaned question explicitly retains these numerical threshold conclusions.

**Counterexample.** Take the complete bipartite graph K4,4, with each vertex and edge its own color. Then

    I(G,4)=0,    I(G,3) is nonzero,
    WMLT(G)=2,    MLT(G)=4.                              (2)

The ideal assertions and WMLT=2 are proved directly below. MLT=4 is a credited instance of Blekherman-Sinn's prior complete-bipartite theorem; it is not needed merely to refute the two scenarios. Here n=3, so neither proposed value WMLT=3 nor WMLT=4 is correct.

There is also a **connected genuinely colored variant**: give vertices1 and2 one shared color, keep every other vertex color distinct, and keep every edge color distinct. It still satisfies I(G,4)=0, I(G,3) nonzero, and WMLT=2. Thus the objection does not depend on calling the singleton-colored model a colored graph. No exact MLT value is asserted here for that tied-diagonal variant.

**Boundary of the answer.** This refutes the literal general numerical threshold classification, including the stated implication in the second bullet. It does **not** refute a separately repaired, purely algebraic dichotomy saying only “a strict signed-SOS separator or a positive-definite intersection,” after removing its threshold claims. Our example has the second intersection. Nor does this example settle an unstated restriction to colored4-cycles: the graph used has eight vertices. The displayed definitions and Proposition3 impose no such restriction, though the surrounding examples are4-cycles. Any intended restricted or repaired question should be stated separately.

## 2. Model, statistics and sample convention

Label the parts L={1,2,3,4}, R={5,6,7,8}. There are all16 cross edges and no edges within either part. In the singleton-colored model, positive-definite concentration matrices K have zero off-diagonal entries within each part and otherwise free diagonal and cross entries. Identity is feasible.

The sufficient statistics of an8-by8 symmetric matrix S are its8 diagonal entries and its4-by4 cross block B=S_(L,R), for24 coordinates. This is exactly the report's projection: each vertex/edge color class has one member. For the genuinely colored variant, replace s11,s22 by their sum; this imposes K11=K22 and leaves23 statistics.

Let I(G,r) be the report's elimination ideal obtained from the(r+1)-minors of a symmetric matrix and the linear equations identifying its statistics. No replacement by only principal minors or by a positive-semidefinite ideal is made. The underlying determinantal variety includes all symmetric matrices of rank at mostr; PSD matrices provide valid test points within it.

The sample convention is the source's zero-mean/scatter-rank convention: r independent observations can be arranged as columns of X in R^(8 by r), with sample covariance a positive multiple of XX^T. The usual factor1/r is irrelevant to positive-definite completion and threshold existence; every completion below can be scaled by the same factor. The cited rigidity article explicitly uses N(0,Sigma). If instead an unknown mean is estimated first, the sample-count/rank shift must be handled separately; that is not the convention of the stated rank-indexed question.

The report's geometric criterion says the MLE exists uniquely exactly when pi_G(S) has a positive-definite completion with the same sufficient statistics. WMLT asks for positive probability, whereas MLT asks for probability one. An exceptional single sample configuration alone would not establish WMLT; Section5 gives an explicit open set.

## 3. I(G,3) is nonzero

The polynomial

    f(B)=det(B)                                          (3)

in the16 observed cross entries is nonzero: it is1 at B=I4. It is a4-by4 minor of the full symmetric matrix, using rows L and columns R. Hence it vanishes whenever rank(S)<=3 and belongs to the defining4-minor ideal. Replacing its cross entries by the corresponding statistic variables changes it by an element of the linear statistic ideal. Thus f belongs to the exact elimination ideal I(G,3).

All cross edges remain individually colored in the tied-diagonal variant, so the identical nonzero determinant belongs to its I(G,3) as well.

## 4. I(G,4)=0 by an exact submersion

Consider the polynomial Gram-statistic map

    Phi:R^(8 by4) -> R^24,    X -> pi_G(XX^T).            (4)

Write X as two4-by4 blocks U,V and evaluate at

    U=I4,
    V rows = e1+e2, e2+e3, e3+e4, e4+e1.                (5)

The Gram matrix has rank4 because U is invertible. We show the derivative of Phi is onto.

Let D=dU and H be a prescribed derivative of the observed cross block UV^T. Then

    dV^T=H-DV^T                                         (6)

achieves that cross derivative for any D. The four left diagonal derivatives set the four entries D_ii independently. The right diagonal derivative at row v_j is

    2 v_j dot d(v_j).

After using (6), its part depending on D is -2v_j D v_j^T. For v_j=e_j+e_(j+1), with indices mod4, this depends on

    D_jj+D_(j+1,j+1)+D_(j,j+1)+D_(j+1,j).

The first two entries are already fixed. The four remaining symmetric sums belong to the four distinct unordered pairs12,23,34,41, so they can be selected independently to produce any four right diagonal derivatives. Thus every cross and diagonal output derivative can be prescribed, proving rank(DPhi)=24.

The submersion theorem makes the image contain a nonempty real open set in R^24. Every polynomial in I(G,4) vanishes on this image, since every XX^T has rank at most4. A real polynomial vanishing on an open set is identically zero. Therefore I(G,4)=0. This reasoning directly proves the elimination statement and does not assume equality of generic completion rank and a statistical threshold.

For the tied-diagonal variant, its statistic map is the composition of Phi with the surjective linear map that replaces its first two diagonal coordinates by their sum. Its derivative therefore has rank23, and the same argument proves I(G,4)=0 for that model.

The exact checker constructs both Jacobians, finds full-row-rank square minors and records their nonzero integer determinants. Floating-point rank decisions are not used.

## 5. WMLT equals2: an open success set and a one-sample obstruction

Let X_* have eight rows in R^2: the four left rows are e1=(1,0), and the four right rows are e2=(0,1). Then

    S_*=X_*X_*^T=diag(J4,J4),    rank(S_*)=2,             (7)

where J4 is the all-ones matrix. Its observed diagonals are all1 and its cross block is0. It has the same statistics as the positive-definite matrix I8. This also holds after merging diagonal colors1,2.

To obtain positive probability, take the open box of data matrices X whose every entry differs from X_* by less than epsilon=1/100. Define M(X) to have diagonal entries ||x_i||^2, cross entries x_i dot x_j for i in L,j in R, and zero off-diagonal entries within each part. It has the same singleton statistics as XX^T, hence also the same tied-diagonal statistics.

In this entire box,

    M_ii >= (1-epsilon)^2=9801/10000,
    |M_ij| <= 2epsilon(1+epsilon)=202/10000 for cross edges.

Each row has four cross entries, so

    M_ii - sum_(j!=i)|M_ij| >= 8993/10000 >0.             (8)

A symmetric strictly diagonally dominant matrix with positive diagonal is positive definite. Thus M(X) is a positive-definite completion for every X in this open box. The data have rank2 there: the determinant of a left and a right row is at least(1-epsilon)^2-epsilon^2=1-2epsilon>0.

For any nondegenerate zero-mean Gaussian model, the joint density of two observations is positive throughout R^16. This nonempty open box has strictly positive probability. Therefore WMLT<=2 for both models. It is not merely an exceptional rank2 example.

With one observation x, choose the cross edge3-5. Its two endpoints have singleton diagonal colors in both models, and its edge has its own color. Any matching completion must contain the principal submatrix

    [[x3^2, x3*x5], [x3*x5, x5^2]],                       (9)

whose determinant is zero. A positive-definite matrix has every principal submatrix positive definite. Thus no one-observation covariance can have a positive-definite completion; if an entry vanishes, the zero diagonal is an obstruction as well. Hence WMLT>=2, and

    WMLT=2                                               (10)

for both models.

## 6. The source's second hypothesis holds, but its threshold conclusion fails

S0=I8 is positive definite, and pi_G(S0)=pi_G(S_*). Since rank(S_*)=2<=3, every polynomial in I(G,3) vanishes at these statistics. Therefore

    pi_G(I8) belongs to V(I(G,3)).                        (11)

This verifies the second bullet's hypothesis using an actual PSD rank2 preimage, not merely a point in the Zariski closure whose realizability is unknown.

The first bullet's strict nonvanishing signed-SOS condition cannot hold for any ideal polynomial: every one of them vanishes at S0=I8, whose Cholesky factor is I8 with positive diagonal. A polynomial that is zero there cannot be everywhere nonvanishing on the positive-diagonal Cholesky domain.

Yet with n=3 from Sections3-4, equation(10) is WMLT=2, not n=3. This alone refutes the two numerical scenarios in the question, for a connected model with a genuine diagonal-color equality as well as for singleton colors.

The missing lower-bound inference is elementary: a rank-n success configuration does not exclude success with fewer observations. Moreover the vanishing-ideal criterion gives an upper bound for MLT, not generally an equality. Neither lower assertion follows merely from(1).

## 7. Credited exact MLT in the singleton case

For the ordinary singleton-colored K4,4, Blekherman-Sinn's prior [Theorem2.7](https://arxiv.org/abs/1703.07849v2), published as *Maximum likelihood threshold and generic completion rank of graphs*, Discrete & Computational Geometry61(2019),303-324, [DOI10.1007/s00454-018-9990-3](https://doi.org/10.1007/s00454-018-9990-3), gives

    MLT(K_(a,b))=min(M,a+1),
    M=min{k: k(k+1)/2 >= a+b},    b>=a>=2.

For a=b=4, M=4, hence MLT(K4,4)=4. Their Theorem2.1 also gives generic completion rank4, consistent with the direct elimination calculation above. These are existing results, not new claims. The exact pair is consequently

    (WMLT,MLT)=(2,4),

where the proposed cases at n=3 would give(4,4) or(3,4). We do not transfer the ordinary-graph MLT value automatically to the tied-diagonal variant; its independently proved WMLT is sufficient for the counterexample.

## 8. What is and is not resolved

The literal universal threshold classification in the supplied question has a negative answer. The example is explicit, small, connected, and remains valid with a genuine color equality. The ideal conditions, weak threshold and positive-definite intersection are fully checked without an appeal to generic-rank/MLT equality.

This is a source correction and an application of classical threshold/completion facts, with no novelty claim. The repaired Boolean separator-versus-intersection question, or an explicitly restricted colored4-cycle question, is a different problem and is not declared solved here. No outreach to the report's authors is undertaken.

Exact computation checks the matrix identities, ideal obstruction polynomial, full-Jacobian minors and rational open-box bounds. Those checks support the written proofs; probabilities are established analytically by an open set and positive density, not by sampling. Independent adversarial review is required before any result PR.
