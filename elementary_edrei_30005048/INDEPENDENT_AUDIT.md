# Independent adversarial audit: row 1839

Audit date: 2026-10-21. Scope: mathematical dependency audit, not a novelty certificate.

## Interim verdict

The easy direction, sign-reciprocal closure, and pole extraction can be established without importing the infinite classification. The hard missing ingredient in a genuinely short elementary proof is a positive moment representation for the logarithmic coefficients. Finite symmetric-group character theory and averaged star transpositions can supply it without invoking the Edrei or Thoma classification, but this reconstructs the strategy already present in Okounkov's cited work. It must not be advertised as a new resolution of the request for a more straightforward proof.

Source inspected: locally recovered text of Andrei Okounkov, *On the representations of the infinite symmetric group*, arXiv:math/9803037, especially Sections 2.1 and 2.4. Section 2.4 explicitly says that it follows Thoma except for the final moment argument. No copied source text is included here.

## 1. Conventions and normalization

Use T(a)_{ij}=a_{j-i}, i,j>=0, and a_n=0 for n<0. PF-infinity means all finite minors are nonnegative, not strictly positive. With a_0=1 and a_1=A>0, replace a_n by a_n/A^n to normalize a_1=1. If a_1=0, the 2-by-2 minors force all a_n=0 for n>0. If a_0=0 but the sequence is not zero, remove the initial zero block and divide by the first positive coefficient; restore C z^m at the end. The zero sequence needs its own harmless exception.

The adjacent minors give a_n^2>=a_{n-1}a_{n+1}. There are no internal zeros. Thus an infinite-support normalized sequence satisfies a_{n+1}/a_n decreasing to alpha>=0, and a_n<=A^n. The power series therefore has positive radius at least 1/A. Finite-support sequences have ratio parameter zero by convention; do not divide by their eventual zero coefficients.

## 2. Product sufficiency: accepted

The factors 1+bz and (1-az)^(-1), a,b>=0, have totally nonnegative upper-triangular Toeplitz matrices. For the first, the matrix is upper bidiagonal, with minors either zero or products of nonnegative entries. For the second, diagonal scaling reduces a>0 to the upper triangular matrix with entries 1 for j>=i, whose minors are zero or one (subtract successive selected columns or use its path matrix). The a=0 case is the identity.

Convolution is multiplication of these matrices. For any fixed minor, upper triangularity restricts the Cauchy-Binet sum to finitely many intermediate indices, so no infinite Cauchy-Binet convergence is being assumed. The exponential factor exp(gamma z) is the coefficientwise limit of (1+gamma z/N)^N. If sum_j(a_j+b_j)<infinity, the products converge uniformly on sufficiently small disks avoiding denominator poles; hence coefficients and each fixed minor converge. This proves PF-infinity sufficiency.

This argument is not the necessity theorem.

## 3. Coefficient truncation: rejected, exact certificate

The sequence a_n=1 for every n>=0 is PF-infinity by the geometric-factor argument. Truncating its generating series after z^2 gives (1,1,1,0,...). The minor with rows (0,1,2) and columns (1,2,3) is

    [1 1 0]
    [1 1 1]
    [0 1 1]

and has determinant -1. Thus ordinary coefficient truncation does not preserve PF-infinity. A reduction to real-rooted finite polynomials cannot use it.

## 4. Reciprocal sign involution: accepted, finite proof available

If H(0)=1 and E(z)=1/H(-z), then E is PF-infinity whenever H is. This can be proved without infinite classification. In a finite leading principal block T_N(H), inverse Toeplitz entries are the coefficients of 1/H. Conjugating the inverse by diag(1,-1,1,-1,...) gives T_N(E). Jacobi's complementary-minor identity says its minors equal complementary minors of T_N(H), divided by det T_N(H)=1: the signs from the inverse identity cancel the diagonal-conjugation signs. Every fixed minor lies in some finite block. This also handles all necessary zero entries and avoids unproved spectral claims.

Equivalently, the symmetric-function involution sends h_n to e_n and s_lambda to s_lambda-transpose. If this route is used, its identity must be stated rather than treating reciprocation as ordinary convolution by a PF-infinity factor.

## 5. Pole peeling: accepted with an explicit finite-theory dependency

For an infinite-support sequence, put alpha=lim a_{n+1}/a_n and b_n=a_n-alpha a_{n-1}. Coefficient nonnegativity alone does not prove that b is PF-infinity.

For every partition lambda, border its Jacobi-Trudi determinant by the long first row corresponding to (N,lambda), divide by a_N, and let N tend to infinity. Its new first row tends to (1,alpha,alpha^2,...). Perform the column operations C_j <- C_j-alpha C_{j-1} in decreasing j order. Expansion along the first row yields det[b_{lambda_i-i+j}]>=0. This proves positivity of all ordinary Schur specializations. To deduce positivity of arbitrary Toeplitz minors, one must invoke or prove the finite skew-Schur decomposition into ordinary Schur functions with nonnegative integer coefficients (or the corresponding finite skew-representation theorem). Omitting this step leaves a real gap. It is finite representation/combinatorics, not the infinite Edrei/Thoma classification, but is not a trivial calculus lemma either.

## 6. Infinite peeling: accepted after filling the convergence argument

Work without rescaling after each extraction. Let H_0=H and H_{k+1}(z)=(1-alpha_{k+1}z)H_k(z), where alpha_{k+1} is the limiting coefficient ratio of H_k, or zero when H_k is entire. Each residual is PF-infinity and has constant coefficient 1. Its linear coefficient is A-sum_{j<=k}alpha_j>=0. Thus sum alpha_j<=A. Also each residual coefficient decreases with k and remains nonnegative. Define its coefficientwise limit H_infinity.

For every fixed k, the limiting coefficients are bounded above by those of H_k. Consequently radius(H_infinity)>=radius(H_k)=1/alpha_{k+1} whenever the latter is finite. Since a summable sequence alpha_j tends to zero, H_infinity is entire. If extraction stops, it stops at an entire residual. The finite products converge uniformly on compact sets, since sum alpha_j<infinity, and the identity

    H_infinity(z)=H(z) product_j(1-alpha_j z)

first follows on a disk about zero by coefficient limits. It then supplies the meromorphic continuation of H. This is the missing justification behind the phrase 'iterate until the residual is entire'; radius improvement need not be strict at each extraction because poles can have multiplicity.

## 7. Second peeling and zero-free residual: accepted, useful short proof

Let A be the entire PF-infinity residual from the first peeling. By Section 4, B(z)=1/A(-z) is PF-infinity as a power series. Peeling B gives an entire PF-infinity residual R and Q(z)=product_j(1-beta_j z), with sum beta_j finite. Near zero, A(-z)R(z)=Q(z), and all three sides extend to entire functions, so the identity holds everywhere.

If R(w)=0, then Q(w)=0. Since Q is a convergent genus-zero product with nonnegative beta_j, its zeros are exclusively the positive real points 1/beta_j. But R has nonnegative coefficients and R(0)=1, hence R(x)>=1 for every x>=0. Contradiction. Thus R is zero-free.

This argument needs neither a hidden pole-location theorem nor an unsupported interchange of zeros and limits. Merely declaring the doubly peeled residual zero-free would not have been enough.

## 8. Zero-free elimination: exactly where positive moments are essential

Suppose a PF-infinity series R is entire, zero-free, and R(0)=1. Then R'/R is entire. Write R'/R=sum_{k>=1} c_k z^(k-1). A positive measure mu on a compact real interval with c_k=int x^(k-1) dmu yields, for every epsilon>0,

    c_(2m+1) >= epsilon^(2m) mu({|x|>=epsilon}).

The coefficient sequence of an entire function has limsup |c_k|^(1/k)=0. The displayed bound therefore forces mu to be supported at zero. Hence c_k=0 for k>=2, R(z)=exp(c_1 z), and c_1>=0.

There is no valid replacement by 'zero-free entire functions are exponentials of linear functions': they are exponentials of entire functions, whose degree can exceed one. Nor do nonnegative coefficients, log-concavity, or positive radius alone provide the needed moment measure.

## 9. Finite-character/star-transposition route: precise audit checklist

To avoid circularity, a reconstruction must prove the following finite claims or clearly identify them as dependencies:

1. The specialization h_n -> a_n gives nonnegative Schur values s_lambda, and the Frobenius character identity identifies the cycle-multiplicative function phi(sigma)=product_cycles c_length as sum_lambda s_lambda chi_lambda on S_n. Here c_k are the logarithmic coefficients, with a_1=c_1=1 after normalization.
2. The weights w_lambda=dim(lambda)s_lambda are nonnegative and sum to one, since phi(identity)=c_1^n=1. Omitting the dimension factor gives the wrong measure.
3. Consequently phi extends linearly to a positive tracial state on each finite complex group algebra. Positivity is not a consequence of cycle multiplicativity alone.
4. Set X_N=N^(-1) sum_{i=1}^N (i,N+1). Every summand is a self-adjoint involution in a unitary representation, so X_N is a self-adjoint contraction. Its spectral distribution under the positive state is a probability measure on [-1,1]. This uses only finite-dimensional spectral theory.
5. In X_N^k, the (N)_k words with distinct indices are all (k+1)-cycles, and therefore have state value c_(k+1). All other words have state of absolute value at most one. Hence, for fixed k,

       |phi(X_N^k)-c_(k+1)| <= 2[1-(N)_k/N^k] <= k(k-1)/N

   for N>=k, by the collision union bound. The k=0 case is mass one. There is no estimate uniform in unbounded k here, and none is needed.
6. Compactness of probability measures on [-1,1] gives a weakly convergent subsequence. Every polynomial moment passes to the limit, giving int x^k dmu=c_(k+1). The same subsequence works for every k because weak convergence tests all continuous functions; selecting unrelated subsequences for each moment would be defective.

No classification of extremal characters, infinite factor representations, or Thoma parameters is required for these six steps. Invoking such a theorem instead would be circular or equivalent to the desired conclusion. The finite Frobenius/Jacobi-Trudi theorem remains a significant standard input, and its use must be disclosed in any claim of elementary character.

## 10. Normalization, summability, and final product

Starting with a_0=1, a_1=A, both peeling stages spend the nonnegative linear coefficient. The pole parameters alpha_j, zero parameters beta_j, and final exponential parameter gamma therefore satisfy sum alpha_j+sum beta_j+gamma=A. Under a_1=1 normalization this is exactly total mass one; without it one must not leave the sum incorrectly equal to one. Nonnegative summable parameters justify the genus-zero products locally uniformly, and identify the numerator and denominator as Laguerre-Polya functions with zeros on the nonpositive real axis after the prescribed sign change.

For general initial data restore C z^m. If the problem statement normalizes a_0=1, do not silently add unnecessary exceptional forms.

## Final scope restriction

A successful completion of this checklist proves the known infinite classification from finite representation theory plus elementary determinant, analytic, and compactness arguments. It does not by itself answer whether the proof is new or substantively more straightforward than the representation-theoretic proof already cited in the 2022 problem. The proper finding is a reconstruction and gap repair, not a solved-status claim.

## Completed review of the companion report

The auditor read the complete companion REPORT.md after incorporation of Sections 6 and 7's convergence/zero-free arguments. No blocking mathematical error was found in the reconstruction as written. The finite-algebra dependencies are explicitly disclosed, and the UNSOLVED verdict matches the original proof-simplification question. The file check_examples.py was independently inspected and run under both normal Python and python -O; both runs returned the stated exact counterexamples successfully. These tests certify only those examples, not the analytic theorem or novelty.
