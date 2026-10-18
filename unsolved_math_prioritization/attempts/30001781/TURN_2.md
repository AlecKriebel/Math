# Turn 2: asymmetric simplex and Dirichlet rows through convex moment comparison

2026-10-01. Second substantive author turn. Original corrected conjecture remains unresolved. This adds a genuinely asymmetric class to the common-quotient result of turn1. Classical Gamma/Dirichlet identities, symmetrization and the published Chevet theorem retain credit; no novelty claim.

## 1. First remove an inessential symmetry obstacle

For any random matrix B with finite moments, centered entries and an independent copy B', let N(B)=B_(k,m), the maximal submatrix Euclidean norm. N is a norm on the space of matrices for k,m>=1. For p>=1, convexity gives

    E N(B)^p <= E N(B-B')^p.                                  (1.1)

Indeed condition on B and use E(B')=0. Thus an all-p moment bound for symmetrized row laws gives an all-p bound for the original row laws, with the expected sqrt(2) normalization factor if isotropy is restored. Independent isotropic log-concave rows stay independent, isotropic and log-concave under (X_i-X_i')/sqrt(2); the new laws are centrally symmetric. Closure of log-concavity under products, reflection and convolution is classical. This is central symmetry only, not coordinate unconditionality.

In particular, consider independent centered variance-one log-concave scalar entries Z_ij, with no symmetry assumption, and a common coisometry U:R^D->R^N, UU*=I. The symmetrized scalar entries (Z_ij-Z_ij')/sqrt(2) are independent, centered, variance one and symmetric log-concave. Their joint matrix law is unconditional. Applying turn1 to that latent matrix and then (1.1) gives

    ||N(Z U*)||_Lp <= C [Lambda_(k,m)+p], p>=1,                 (1.2)

where Lambda=sqrt(m) log(3N/m)+sqrt(k) log(3n/k). The source deviation estimate implies this moment estimate by the tail integral; sqrt(p)+p is bounded by2p for p>=1. Constants do not depend on the latent dimension or the separate scalar laws. This comparison does not apply to arbitrary dependent coordinates inside a row.

## 2. General Dirichlet row construction

Fix D=N+1>=2 and positive weights alpha_1,...,alpha_D. For row i choose a concentration c_i>0 such that

    alpha_ij=c_i alpha_j >=1 for every j.

Set a_i=sum_j alpha_ij, q=(sqrt(alpha_j))/sqrt(sum_j alpha_j), and fix a coisometry U:R^D->R^N whose kernel is span(q). The same U works for every row because the weight ratios are common. Let P_i be independent Dirichlet(alpha_i1,...,alpha_iD) vectors. Define the random row column-vector

    X_i=sqrt(a_i(a_i+1)) U diag(alpha_i1^(-1/2),...,alpha_iD^(-1/2)) P_i.   (2.1)

These rows are centered, isotropic and log-concave. To check this rather than assume it, the Dirichlet moment identities are

    E P_ij=alpha_ij/a_i,
    Cov(P_i)=[diag(alpha_ij)-alpha_i alpha_i*/a_i]/[a_i(a_i+1)].

The U-image of diag(alpha_ij)^(-1/2) alpha_i is zero since it is a multiple of Uq. Multiplying the covariance by the matrices in (2.1) gives I_N. The density of P_i on its affine simplex is proportional to product_j p_j^(alpha_ij-1); its logarithm is concave because all exponents are nonnegative. The map in (2.1) is injective on the affine hyperplane sum p_j=1, so its image has a full-dimensional log-concave density in R^N.

The theorem is

    ||A_(k,m)||_Lp <= C [Lambda_(k,m)+p], p>=1,                 (2.2)

and consequently, for universal C',c'>0,

    P(A_(k,m)>C' Lambda_(k,m)+t)<=exp(-c' min(t^2,t)), t>0.    (2.3)

Here A has the rows (2.1). The constants are independent of n,N, the weights and all c_i subject to alpha_ij>=1. The proof supplies a common weighted-simplex geometry, not arbitrary row-specific weight ratios or arbitrary isotropic log-concave laws.

## 3. Exact Gamma coupling and conditional expectation

For each i let G_ij be independent Gamma(alpha_ij,rate1) variables, and put

    S_i=sum_j G_ij,   P_ij=G_ij/S_i,
    Z_ij=(G_ij-alpha_ij)/sqrt(alpha_ij),
    Y_i=U Z_i.

The variables Z_ij are independent centered variance-one log-concave variables: the second derivative of the logarithm of the Gamma density is -(alpha_ij-1)/g^2<=0; affine standardization preserves log-concavity. Thus the row matrix Y is covered by (1.2).

For clarity, the standard independence assertion does not require a limiting approximation. In the change of variables G_j=s p_j, sum p_j=1, the Jacobian is s^(D-1). Multiplying the Gamma densities gives a factor s^(a_i-1) exp(-s) times product_j p_j^(alpha_ij-1). Normalizing separates the Gamma(a_i,rate1) density for S_i and the Dirichlet density for P_i. Hence S_i is independent of P_i and of X_i, and E S_i=a_i. The displayed Dirichlet moments follow by increasing the appropriate density exponents by one or two and using Gamma(z+1)=z Gamma(z).

Because U diag(alpha_i)^(-1/2) alpha_i=0, the coupling gives the exact identity

    Y_i = [S_i/sqrt(a_i(a_i+1))] X_i.                         (3.1)

Let d_i=sqrt((a_i+1)/a_i), and let D_0 be the deterministic diagonal matrix of the d_i. Since a_i>=D>=2, max_i d_i<=sqrt(3/2)<sqrt(2). Row independence and the independence of each S_i from P_i give

    E[D_0 Y | X_1,...,X_n] = A.                               (3.2)

In (3.2), Y and A denote row matrices. Conditional Jensen for the convex function N^p therefore implies

    E N(A)^p <= E N(D_0 Y)^p <= (max_i d_i)^p E N(Y)^p.

The last inequality is deterministic: multiplying rows by a diagonal matrix of operator norm d multiplies every selected submatrix norm by at most d. Equation (1.2) now proves (2.2).

No event controlling min_i S_i is needed. In particular, there is no failed union bound n exp(-cN), no restriction n<=exp(cN), and no claim that the normalizers are independent of the unnormalized Gamma entries. Only their exact independence from the normalized Dirichlet rows is used.

## 4. Moment-to-tail conversion

Here Lambda>=1. If ||W||_Lp<=C_0(Lambda+p) for all p>=1, Markov gives

    P(W>e C_0(Lambda+p))<=exp(-p).

For t>=2e C_0 choose p=t/(e C_0). The threshold 2e C_0 Lambda+t is at least e C_0(Lambda+p), giving an exponential upper bound exp(-t/(e C_0)). For0<t<2e C_0, the p=1 bound and Lambda>=1 give P(W>2e C_0 Lambda+t)<=1/e. Reducing a universal c' if needed makes this at most exp(-c' min(t^2,t)) throughout the small-t range. Increasing C' as necessary proves (2.3). This is a tail above a universal multiple of the sharp scale, not a concentration assertion around the exact mean.

## 5. Uniform regular simplices are a concrete asymmetric instance

Take every alpha_ij=1. Then a_i=D, P_i is uniform on the standard simplex and

    X_i=sqrt(D(D+1)) U P_i,   U(1,...,1)=0.

This is uniform on a centered regular N-simplex in isotropic position. The vertices have squared radius D^2-1=N(N+2), and the covariance is the identity as checked above. For N>=2 a simplex is not centrally symmetric, hence not unconditional. Thus the argument truly goes beyond linear images of centrally symmetric unconditional latent laws in turn1; it uses conditional expectation and symmetrization instead of an exact representation of X itself as such an image.

## 6. Original gap and failed broader shortcuts

A direct search through common rotations is blocked by turn1, and uniform-simplex or the above weighted Dirichlet examples are blocked as counterexample routes by this turn. The Gamma coupling proves the corrected sharp order for this substantial class with all dimensions and all sample sizes covered.

For different weight ratios in different rows, the natural coisometries U_i differ. Then Y is no longer one matrix Z followed by one common U*, so (1.2) cannot be applied as written. More generally, arbitrary log-concave rows need not be conditionally represented by these Gamma/Dirichlet data. Merely observing that each fixed fiber has a small exponential width does not justify a uniform chaining argument when the fiber metric varies with the row coefficient vector. Neither shortcut closes the original conjecture.

The original question remains unresolved after two substantive author turns. Three further turns remain. All partial claims will require separate independent review in the final packet.
