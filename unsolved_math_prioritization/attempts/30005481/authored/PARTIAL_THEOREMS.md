# Hook-shaped extendability: exact partial results

Problem 30005481 / OWR-12697711-017. Research date: 7 October 2026.

## Disposition and scope

The full equivalence between extendability and weak SOS-hyperbolicity remains unresolved in this work. Five substantive approaches are recorded below. No counterexample to the equivalence, full proof, historical novelty, or independent-review claim is made. In particular, being nonextendable is not by itself a counterexample: a counterexample would also have to be weakly SOS-hyperbolic.

We work in the source's intended range 1 <= d <= n. Write e_k for the elementary symmetric polynomial, e for the all-ones vector, and m=e_1/n. A hook-shaped form has the form sum_{i=1}^d a_i e_1^(d-i)e_i. The closed hyperbolicity cone is K_p={u: p(u+t e) has no positive real zero}. For u,v in K_p, set

    Delta_{u,v}p = D_u p D_v p - p D_u D_v p.

Weak SOS-hyperbolicity means that this polynomial is a sum of squares for every pair u,v in K_p. Checking only Delta_{e,e}, or finitely many pairs, is insufficient.

For g(t)=a product_i(t-r_i) with sum r_i=0, the associated operator is T_p g(t)=a p(r-t e). It is defined on R[t]_{n,0}, the polynomials of degree at most n whose t^(n-1) coefficient vanishes. An extension must be diagonal and preserve real-rootedness on all of R[t]_n. A scalar multiple of a map has the same extendability status.

The standard finite Pólya-Schur criterion says that a diagonal map T-hat:R[t]_n -> R[t]_d preserves real-rootedness if and only if T-hat((t-1)^n) is real-rooted with all its zeros of one sign. Zero outputs are admitted in the usual preserver convention. All symbols used below have nonzero leading coefficient.

## Approach 1: inverse-symbol geometry and a critical-value criterion

This approach reduces the extension side to a one-dimensional real-algebraic feasibility problem. The source already gives the inverse-symbol equivalence; the critical-value derivation here makes it explicit.

Define

    g_0(t)=(t-1)^(n-1)(t+n-1),
    delta_d f=t f'-(d-1)f.

Thus delta_d(t^(d-k))=(1-k)t^(d-k), and delta_n((t-1)^n)=g_0. Diagonal maps commute with these degree-indexed delta operators. If G=T(g_0), an extension exists precisely when delta_d f=G for some f with all its zeros real and of one sign. Indeed f is the extension's value at (t-1)^n; conversely that value specifies a diagonal extension, and the finite Pólya-Schur criterion applies.

Write G=sum_{k=0}^d b_k t^(d-k), with b_1=0 and b_0 nonzero. Every possible symbol is

    f_c(t)=F(t)+c t^(d-1),
    F(t)=sum_{k != 1} b_k/(1-k) t^(d-k).

Consequently, on t>0, H=F/t^(d-1) satisfies H'=G/t^d. This is a scalar horizontal-level problem, not a matrix-SOS problem.

### Proposition 1 (simple-root positive-symbol criterion)

Suppose b_0>0, G has exactly one negative root and d-1 distinct positive roots r_1<...<r_{d-1}, and G(0) is nonzero. Then f_c has d positive real roots, counted with multiplicity, if and only if

- H(r_i)+c <= 0 at every local minimum of H;
- H(r_i)+c >= 0 at every local maximum of H.

Equivalently,

    max_{local maxima r_i}[-H(r_i)] <= c
        <= min_{local minima r_i}[-H(r_i)].

An empty collection of maxima contributes no lower bound. To test negative-root extensions as well, apply the same construction after t is replaced by -t and the leading sign is adjusted.

Proof. The only critical points of H on (0,infinity) are the r_i, and its derivative changes sign at each. At infinity H tends to positive infinity. At zero its sign is (-1)^d infinity, because the constant coefficient of F has sign (-1)^d. The displayed inequalities give a zero of H+c in each of its d consecutive monotonic intervals. If a critical value is zero, that zero has multiplicity two and is counted for its two adjoining intervals. Adjacent critical values cannot both be equal because H is strictly monotone between them. These zeros exhaust the degree d of f_c. Conversely, to have d positive zeros, every monotonic interval must supply its prescribed crossing, with the same endpoint convention. This forces the inequalities. This is also the usual alternating-critical-value characterization of real-rootedness applied to F/t^(d-1). ∎

### Repeated-root obstruction

If f has positive real zeros a_j, then away from them

    delta_d f / f = 1 + sum_j a_j/(t-a_j),
    (delta_d f / f)' = -sum_j a_j/(t-a_j)^2 < 0.

Thus a zero of delta_d f not shared with f is simple. At a positive zero of f of multiplicity k, delta_d f has multiplicity exactly k-1. A repeated positive zero of G of multiplicity k therefore forces multiplicity k+1 in f. This supplies the inverse implication needed when using multiplicities; the forward multiplicity assertion alone would not suffice.

For

    G(t)=(t-1)^2(t-2)^2(t+6)
        =t^5-23t^3+66t^2-68t+24,

one has

    F=t^5+23t^3-33t^2+(68/3)t-6,
    H(1)=23/3,   H(2)=185/24,
    H(2)-H(1)=1/24.

A one-sign inverse symbol would have to have triple zeros at both 1 and 2, impossible in degree five. Equivalently, the necessary choices c=-H(1) and c=-H(2) disagree. This recovers the published nonextendability obstruction with a direct exact calculation.

Limit: no argument here converts the critical-value interval into a necessary or sufficient SOS certificate. This is the missing bridge in the original conjecture.

## Approach 2: the full quadratic case and product closure

We attempted an induction through low-degree factors. It succeeds for all symmetric quadratics and products of already certified factors, but a general hook-shaped form need not factor in that way.

### Proposition 2 (degree at most two)

Every symmetrically hyperbolic form of degree at most two has an extendable associated operator and is weakly SOS-hyperbolic.

For degree one, a nonzero symmetric form is a scalar multiple of m; its Wronskians are nonnegative constants for cone directions, and extension is immediate.

For degree two, after multiplication by a nonzero scalar, every hyperbolic symmetric form is

    p(x)=a m(x)^2-b sum_i(x_i-m(x))^2,  a>0, b>=0.

This follows by decomposing the permutation representation into the mean and its orthogonal complement. Along x+t e, the two roots are real for every x exactly when b>=0. For b=0 the form is a square of a linear form and the claim is immediate.

For b>0, an invertible change on the effective variables changes p into the Lorentz quadratic q(z)=z_0^2-|z'|^2, up to a positive scalar. Let L be its associated Lorentz bilinear form. Then

    Delta_{u,v}q(z)=4 L(z,u)L(z,v)-2 L(z,z)L(u,v).

Every vector in the forward Lorentz cone is a nonnegative combination of null vectors (1,A), |A|=1. The expression is bilinear in u,v, so it suffices to use u=(1,A), v=(1,B). Choose orthonormal spatial coordinates in which

    A=(c,s,0,...),  B=(c,-s,0,...), c^2+s^2=1.

Direct expansion gives

    Delta_{u,v}q / 4 = (c z_0-z_1)^2+s^2 sum_{j>=3} z_j^2.

The formula includes A=B and A=-B by the evident limiting choices; one may embed a one-dimensional spatial subspace into a two-dimensional one. Therefore every required Wronskian is SOS. Pullback by a linear map preserves SOS.

For extension, if the input leading coefficient is b_0 and its t^(n-2) coefficient is b_2, the associated map has output a b_0 t^2+2b b_2. Its value at g_0 is a t^2-b n(n-1). Set r=sqrt(b n(n-1)/a). The all-positive-root symbol a(t-r)^2 satisfies delta_2[a(t-r)^2]=a t^2-b n(n-1), so Proposition 1's inverse-symbol equivalence supplies an extension.

### Product identity

For any forms p,q and any directions u,v,

    Delta_{u,v}(pq)=q^2 Delta_{u,v}p+p^2 Delta_{u,v}q.

This follows by the product rule; all mixed cross terms cancel. If p,q are hyperbolic with respect to the same e, their product cone is the intersection of their cones. Thus weak SOS-hyperbolicity is closed under products of such forms. A product of real linear factors, all nonzero at e, has the explicit certificate

    Delta_{u,v} product_i L_i
      =sum_i L_i(u)L_i(v) product_{j != i} L_j(x)^2,

after orienting every L_i to be positive at e. Cone membership makes the coefficients nonnegative. Repeated factors are allowed.

Limit: neither arbitrary sums of these forms nor the general hook-shaped coefficient parametrization preserve this product argument. It cannot be extrapolated to degrees three and four merely from their known extendability.

## Approach 3: an all-dimensional determinantal subfamily

A possible sufficient-direction strategy is to build a definite determinantal representation from an extension. We can do so for the following substantial family, but not for a general one-sign extension symbol.

### Proposition 3 (shifted penultimate elementary form)

Let n>=2 and s=1+n b !=0. The hook-shaped degree n-1 form

    p_b(x)=e_{n-1}(x_1+b e_1(x),...,x_n+b e_1(x))

has an extendable associated operator and is weakly SOS-hyperbolic.

Hook shape follows by expanding a common shift:

    e_{n-1}(x+z e)=sum_{k=0}^{n-1}(n-k)e_k(x) z^(n-1-k).

The k=0 term is a multiple of e_1^(n-1); the remaining terms have the required hook shape. At e, p_b(e)=n s^(n-1), nonzero.

For a centered-root input g, differentiation of its product gives

    T_{p_b}g(t)=(-1)^(n-1) g'(s t).

The same formula defines a diagonal real-rootedness-preserving map on every input polynomial, by Rolle's theorem and the nonzero real rescaling. Thus it is the required extension.

For the SOS side, let B be an n by (n-1) real matrix with orthonormal columns spanning e-perp. Set L_i=x_i+b e_1(x) and A(x)=B^T diag(L_i)B. Cauchy-Binet gives

    det A(x)=e_{n-1}(L)/n.

Indeed the squared maximal minors of B are all 1/n, as the orthogonal complement is spanned by e/sqrt(n). After multiplying A by sign(s), A(e) is positive definite. Its closed determinant hyperbolicity cone is exactly the pullback of the positive-semidefinite cone.

For a symmetric definite pencil A and p=det A, direct differentiation at invertible A, followed by polynomial continuation, gives

    Delta_{u,v}p = tr(adj(A) A(u) adj(A) A(v)).

For cone directions write A(u)=UU^T and A(v)=VV^T. The right side is

    || U^T adj(A(x)) V ||_F^2,

a sum of squares of polynomials. Constant scalar multiples of p scale Delta by a positive square, so this proves the claim for p_b as stated, including boundary directions.

Limit: a general extendable symbol has arbitrary positive roots. Its polarization can be represented as a symmetrized family of products, but an average of determinants does not automatically inherit the displayed adjugate certificate. No closure theorem that repairs this step was established.

## Approach 4: SOS obstruction hunting on the published quintic

Take the published symmetric hyperbolic quintic in five variables

    p=4500 e_5-220 e_1 e_4+7 e_1^2 e_3,
    w=(6,1,1,1,1), e=(1,1,1,1,1).

The exact identity

    p(w+t e)=750 t^2(t+1)^2(t+8)

shows w belongs to its closed hyperbolicity cone. Blekherman-Lindberg-Shu report that Delta_{e,w}p is not SOS, using a computational check. We do not turn that reported numerical computation into an independently verified rational separation certificate. The example is consistent with the target conjecture, not a counterexample to it.

We sought a simpler exact non-SOS obstruction by restricting to two natural ternary subspaces. That strategy fails for a concrete reason: both restrictions are SOS. Let W=Delta_{e,w}p. Direct symbolic computation gives

    W(0,a,b,c,0)=49(a+b+c)^2 H_0(a,b,c),
    W(a,b,c,c,c)=9(a+b-7c)^2 H_1(a,b,c).

The rational Gram matrices for H_0 and H_1 are in SLICE_GRAM_CERTIFICATES.json. Their monomial vectors have respectively seven and eight cubic entries. The checker reconstructs W from p, verifies both polynomial identities coefficient by coefficient, verifies each exact Gram identity, and proves PSD by positive leading minors of a full-rank principal block, together with exact full-matrix rank.

For H_0 the rank is four, and the positive principal block has leading minors

    24, 1863/4, 2135565/4, 3608550.

For H_1 the rank is six, with leading minors

    2975,
    37291974,
    1420680016818/125,
    11642798212191333/500,
    358731464786860973688/3125,
    418175813455241820831/62500.

A symmetric matrix with a positive definite principal block of its full rank is PSD: its Schur complement has rank zero and is zero, so the matrix is congruent to the positive block plus a zero block. Thus these are exact certificates; no floating-point eigenvalue is used for their validity.

The initial numerical optimization of the second slice appeared infeasible. Imposing the exact kernel constraints made the solver find a feasible point, which was rationalized and checked. That failed numerical run is not evidence of non-SOS. Likewise, SOS of these slices says nothing about the full five-variable Wronskian.

Limit: neither a universal SOS construction nor an exact full-space separating functional was obtained. The two certificates rule out these particular restriction routes only.

## Approach 5: a sharp extension threshold in a hyperbolic deformation

This approach deforms the known nonextendable example through hyperbolic hook-shaped quintics, and solves the extension question exactly throughout that family. It leaves the weak-SOS status on either side of the threshold open.

### Theorem 4 (exact one-parameter extension boundary)

For the preceding quintic p, define, for epsilon>=0,

    p_epsilon=p+epsilon (e_1/5)D_e p.

Let epsilon_* be the unique positive zero of

    D(epsilon)=167620 epsilon^3-8871 epsilon^2+2820 epsilon-752.

Then:

1. p_epsilon is hook-shaped and symmetrically hyperbolic for every epsilon>=0.
2. Its associated operator is extendable exactly when epsilon>=epsilon_*.
3. epsilon_* is approximately 0.146702017518328; this decimal is illustrative only. The defining polynomial and uniqueness proof specify it exactly.

#### Proof of hyperbolicity preservation

On centered-root input lines, m(r-t e)=-t and d/dt[p(r-t e)]=-D_e p(r-t e). Hence

    T_{p_epsilon}=(I+epsilon t d/dt)T_p.

The diagonal Euler operator B_epsilon=I+epsilon t d/dt preserves real-rootedness in degree at most five: its Pólya-Schur symbol is

    B_epsilon((t-1)^5)=(t-1)^4((1+5epsilon)t-1),

whose zeros are all positive for epsilon>=0. The source theorem gives hyperbolicity of p, so the associated-operator equivalence gives hyperbolicity of p_epsilon. Alternatively one can apply B_epsilon directly on every centered line and then translate the line parameter. Moreover p_epsilon(e)=750(1+5epsilon), so there is no vanishing-at-e degeneracy. Differentiating a hook-shaped form in the e direction and multiplying by e_1 again gives a hook-shaped form.

#### The normalized extension symbol

The sign convention T_p g(t)=p(r-t e) gives

    T_p((t-1)^4(t+4))=-750 G(t),
    G=(t-1)^2(t-2)^2(t+6).

Multiplication of the operator by -1/750 has no effect on extendability. Thus put G_epsilon=G+epsilon t G'. Every inverse symbol, up to this harmless scalar, is

    f_epsilon,c=F+epsilon t F'+c t^4,
    F=t^5+23t^3-33t^2+(68/3)t-6.

Commutation of delta_5 with t d/dt proves delta_5 f_epsilon,c=G_epsilon. The fixed constant coefficient is -6 and the leading coefficient is 1+5epsilon>0. Therefore a one-sign real-rooted symbol must have five positive zeros; five negative zeros would give a positive constant coefficient, and zero is not a root.

For epsilon>0,

    G_epsilon=(t-1)(t-2)C_epsilon(t),
    C_epsilon=(1+5epsilon)t^3+(3+15epsilon)t^2
                -(16+34epsilon)t+12.

We have C_epsilon(0)=12, C_epsilon(1)=-14epsilon, C_epsilon(2)=32epsilon. Its positive leading coefficient and these signs give one negative root, a root alpha in (0,1), and a root beta in (1,2). These three roots exhaust its degree, so they are simple and ordered. The four positive critical points of

    H_epsilon=(F+epsilon t F')/t^4
              =(1+4epsilon)H+epsilon t H'

are consequently alpha,1,beta,2. They are, in order, maximum, minimum, maximum, minimum. Since G(1)=G(2)=0,

    H_epsilon(1)=(1+4epsilon)23/3,
    H_epsilon(2)=(1+4epsilon)185/24.

In particular the second minimum is strictly higher than the first. Also H_epsilon(beta)>H_epsilon(2), by strict decrease on (beta,2).

The critical-value criterion therefore says an extension exists exactly when

    H_epsilon(alpha)>=H_epsilon(2).

When an extension exists, the endpoint value

    c_2=-(1+4epsilon)185/24

already works. This can also be seen by counting crossings: with c=c_2, the first maximum is nonnegative, the first minimum is negative, the second maximum is positive, and the last minimum is zero. There are three positive zeros before 2, counted with multiplicity, and a double zero at 2. Conversely any admissible level must lie above the higher minimum and below the first maximum, so it forces the displayed inequality.

#### Cubic discriminant and exact threshold

At this distinguished c_2, exact factorization gives

    f_epsilon,c_2=(t-2)^2 Q_epsilon(t),
    Q_epsilon=[(24+120epsilon)t^3-(89+260epsilon)t^2
                 +(100+136epsilon)t-36]/24.

For epsilon>=0 its coefficients alternate strictly in sign. Thus Q_epsilon has no nonpositive real zero. It has three real zeros, counted with multiplicity, exactly when its cubic discriminant is nonnegative. Direct calculation yields

    Disc_t(Q_epsilon)=(4epsilon+1)D(epsilon)/5184.

It follows that for epsilon>0 an extension exists exactly when D(epsilon)>=0. At epsilon=0 the repeated-root obstruction from Approach 1 gives nonextendability, consistent with D(0)=-752.

Finally

    D'(epsilon)=502860epsilon^2-17742epsilon+2820.

Its discriminant is -5357482236<0 and its leading coefficient is positive. Hence D is strictly increasing on the whole real line, D(0)<0, and D tends to infinity. There is exactly one positive zero epsilon_*, proving the theorem. ∎

### What this does and does not settle

The theorem gives a fully exact extension boundary inside a rigorously hyperbolic hook-shaped family. It does not identify the weak-SOS boundary. The original conjecture predicts that these boundaries coincide. Establishing or separating them remains a concrete finite-parameter target. Even at epsilon=1, where the explicit inverse symbol proves extendability, this report does not assert weak SOS-hyperbolicity of p_1.

The universal proofs above are written arguments. The supplied exact computations verify identities and finite test controls; they are not a formal proof assistant certificate of the original conjecture.

## Attribution

The original conjecture, inverse-symbol framework, finite-degree extension theorem, and base quintic are due to Blekherman, Lindberg and Shu. The Pólya-Schur theorem, product identities, quadratic Lorentz argument, and definite-determinant SOS identity are established mathematical tools or elementary consequences. The displayed deformation analysis and rational slice certificates are authored derivations in this work, without a priority or novelty claim.
