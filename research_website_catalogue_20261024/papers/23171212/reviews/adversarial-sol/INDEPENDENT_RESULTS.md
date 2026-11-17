# Actual independent source-first derivations and falsifiers — row 175

2026-11-17 UTC. These results precede all new foreign proofs, support/code/results, archived audit opinions and current peer/root findings. The actual native manuscript and its proof necessarily were read, and native public metadata author assertions were visible. The following is a checkable reconstruction, alternative idempotent argument and adversarial control family; it is not a finite test plan or an assertion that the source proof was unseen.

## 1. Exact linear decomposition in the given norm

The contraction bound gives ||A^n||≤1. If Av=λv+w and Aw=λw with |λ|=1 and w nonzero, then A^n v=λ^n v+n λ^(n−1)w and ||A^n v||≥n||w||−||v||. This contradicts power boundedness. Every Jordan block for a peripheral eigenvalue is therefore size one, including if there are several equal eigenvalues. Every eigenvalue has modulus at most one by applying the norm bound to an eigenvector.

Let E be the peripheral sum and F the remaining generalized eigenspace sum. They are complementary invariant subspaces, so the spectral projection P is defined, commutes with A, is identity on E and zero on F. Every stable Jordan block has powers which are finite sums of binomial(n,j) α^(n−j) times nilpotent powers for |α|<1. A polynomial times a decaying exponential tends to zero; α=0 blocks vanish eventually. Hence ||N^n||→0 on F, without requiring stable diagonalizability or a normal matrix.

To prove the projection is compatible with the original norm, take a subsequence m_j for which the finite torus tuple of peripheral powers converges. For n_j=m_(2j)−m_j, n_j≥j and each λ_i^(n_j)→1. Thus B^(n_j)→I_E and A^(n_j)→P in finite-dimensional operator norm. P is an operator-norm limit of contractions, so ||P||≤1. For E=0, simply A^n→0=P. Since P(U)⊂U∩E and P fixes every element of U∩E, P(U)=V exactly; no assumption that U factors as a Cartesian product is needed.

When E is nonzero, B^(n_j−1)→B^(−1) and every B^(n_j−1) has norm at most one. Therefore both B and its inverse are contractions in the restricted original norm; ||x||=||B^−1 Bx||≤||Bx||≤||x||. This gives a surjective isometry and B(V)=V. On E=0 the corresponding ball is the singleton {0}; the Koopman operator on it is the identity on constants, not a zero-dimensional observable space.

## 2. Two actual mechanisms for unimodular factorization

For K_A f=ζf, |ζ|=1, let ω_f be a uniform modulus of continuity on compact U. For every x∈U and n≥0,

    |f(x)−f(Px)| = |f(A^n x)−f(A^n Px)|
                 ≤ ω_f(||N^n||*||I−P||).

Both arguments belong to U. The bound tends to zero uniformly, so f=f∘P. The restriction g=f|V is nonzero exactly when f is, because f=g∘P and P maps onto V. It satisfies g(Bx)=ζg(x). Conversely pullback along P intertwines K_B and K_A, so this is a bijective correspondence of unimodular eigenspaces, preserving the sup norm.

An alternative idempotent check avoids comparing paired stable fibers. Uniform continuity and A^(n_j)→P give K_A^(n_j)→Q strongly, where Qf=f∘P and Q²=Q. For nonzero eigenfunction f choose x0 with f(x0)≠0. Then ζ^(n_j)=f(A^(n_j)x0)/f(x0) converges to a scalar c of modulus one, and Qf=cf everywhere. Idempotence gives c²f=cf, so c=1. Thus Qf=f. This is the concrete reversible-idempotent mechanism without invoking a general decomposition theorem as an unsupported replacement for the target.

For a stable-only matrix, P=0, so a nonzero unimodular eigenfunction is constant and its eigenvalue must be 1. For a mixed matrix, the result removes every dependence on stable generalized coordinates; eigenfunctions need not be holomorphic in the remaining coordinates.

## 3. Peripheral point spectrum and the closure trap

Diagonalizing B gives coordinates z_i with z_i(Bx)=λ_i z_i(x). The monomials z^p conjugate(z)^q have eigenvalue product λ_i^(p_i−q_i). They are nonzero on V because V has nonempty interior in E. Every integer exponent can be written as p_i−q_i with p_i,q_i nonnegative, so these eigenvalues fill the group Γ, including negative exponents. This uses complex continuous, rather than holomorphic, observables.

For any ζ∈T outside Γ, let M_m=(1/m)sum_(j=0)^(m−1) ζ^(−j)K_B^j. Its norm is at most one. On a monomial of eigenvalue γ it has scalar multiplier

    (1−(γ/ζ)^m)/(m(1−γ/ζ)),

whose absolute value is at most 2/(m|1−γ/ζ|). This tends to zero for each monomial, even if Γ is dense and there is no uniform lower bound on |1−γ/ζ|. Every fixed finite polynomial therefore tends uniformly to zero under M_m. Coordinate/conjugate polynomials form a self-conjugate unital point-separating algebra on compact V; complex Stone–Weierstrass makes them dense in C(V). For an alleged eigenfunction f, M_m f=f, and approximation by a fixed h gives ||f||≤||f−h||+||M_m h||. First m→infinity, then approximation error→0, yields f=0. There is no illicit interchange of an infinite frequency family or a uniform operator-norm convergence assertion.

K_B is an invertible isometry. For |ζ|>1 a Neumann series in K_B/ζ gives the resolvent; for |ζ|<1 factor ζI−K_B=−K_B(I−ζ K_B^−1) to get another Neumann series. Thus its spectrum is on T and contains closure(Γ). If Γ is infinite, finitely many small arcs and pigeonhole give nonidentity group elements with arbitrarily small angular distance δ from 1. The powers with angles 0,δ,...,floor(2π/δ)δ form a δ-net, so closure(Γ)=T. If Γ has finite order q it is exactly the qth roots and B^q=I. Then (ζI−K_B) inverse is the finite polynomial sum divided by ζ^q−1 for ζ^q≠1, so no other spectral values occur. Consequently σ(K_B)=closure(Γ) exactly, while σ_p(K_B)=Γ exactly.

Actual irrational-rotation control: choose λ=exp(2πi sqrt(2)) on one complex coordinate. The value ζ=exp(2πi sqrt(3)) belongs to σ(K_B)=T but is not an eigenvalue. If ζ=λ^n, then sqrt(3)=m+n sqrt(2) for integers m,n. Squaring contradicts irrationality of sqrt(2) if mn≠0; if either is zero, 3=m² or 3=2n² is impossible. Thus the distinction between the dense countable point group and its closed full spectrum is concrete. The negative-power eigenfunction conjugate(z) has value λ^−1, which would be missed by a monoid or holomorphic-only argument.

## 4. Every open-disk point and why zero is not matrix singularity

Let α be any matrix eigenvalue with 0<|α|=a<1. A nonzero algebraic left eigenfunctional ell exists because A^T−αI is singular; no conjugate transpose convention is needed for a complex-linear functional. For R=max_U|ell|>0 and μ≠0, |μ|<1, choose theta with exp(i theta)=μ/|μ| and let

    s=(log|μ|+i theta)/log a,     f_mu(x)=(|ell(x)|/R)^s outside ker ell,
    f_mu(x)=0 on ker ell.

The logarithm inside the power is the real logarithm of a positive radius, not a multi-valued complex logarithm. Re(s)>0, so |f_mu(x)|=(|ell(x)|/R)^Re(s)→0 at the whole hyperplane. Hence f_mu is continuous and nonzero, and f_mu(Ax)=a^s f_mu(x)=μ f_mu(x). The argument of α is irrelevant because the function is radial in |ell|. This supplies negative real and nonreal μ, not only positive eigenvalues.

For μ=0 use f_0=max(0,|ell|/R−a). On A(U), |ell|≤aR; at a maximizing point of U it has value 1−a>0. Thus K_A f_0=0, including if A is invertible as a matrix. Since ||K_A||=1, all eigenvalues lie in the closed disk; the factorization/peripheral calculation excludes exactly the unwanted boundary values. The point spectrum is D union Γ. Closedness of Banach spectrum and the norm bound then give the whole closed disk as the full spectrum.

Concrete scalar control: A=(1/2)I, μ=i/2 gives s=1−i*pi/(2 log2). At radius r=|ell|/R, f(r/2)=(i/2)f(r), |f(r)|=r and f(0)=0. Also f_0(r)=max(0,r−1/2) is a nonzero kernel function although det A is nonzero. At the limiting boundary |μ|=1, the same formula has Re(s)=0 and generally fails continuity at r=0. Therefore one must not extend the radial construction to arbitrary unimodular μ by taking a parameter limit.

## 5. J empty: nilpotent complement and full resolvents

If J is empty, every stable matrix eigenvalue is zero, so the finite-dimensional restriction N is nilpotent, N^d=0. Define Qf=f∘P. It is bounded with norm one, idempotent and commutes with K_A. Its range is the pullback of C(V), and ker Q consists exactly of the continuous functions vanishing on V. Thus C(U)=ran Q direct-sum ker Q as two closed commuting invariant summands. On ker Q, K_A^d=0 because A^d(U)⊂V. This is a nilpotent Koopman restriction; K_A itself is never nilpotent, since constants are fixed.

If F is nonzero, choose a nonzero complex-linear functional vanishing on E. Its restriction is a nonzero element of ker Q. A nilpotent operator T on a nonzero space has a nonzero kernel vector: for any h nonzero choose the least m with T^m h=0, then T^(m−1)h is such a vector. Its full spectrum is {0}, because

    (ζI−T)^−1 = sum_(j=0)^(d−1) T^j / ζ^(j+1),   ζ≠0.

If F=0 the second summand is absent; an empty summand does not add an artificial spectral zero. Bounded block-diagonal operators on these two closed summands have the union of their spectra, with the block inverses giving an inverse when both exist; any inverse of the full commuting operator restricts to inverse blocks. Point spectra are also the union because an eigenvector has a nonzero component in at least one block. Here F nonzero is equivalent to singular A. This proves Γ union Z_A and closure(Γ) union Z_A, including every zero-eigenvalue Jordan block and all-peripheral cases.

The condition k≥1 matters. In a dimension-zero space, U is a singleton and C(U)=C; even the zero-dimensional zero matrix would give only spectrum {1}, so a careless extension of the nilpotent {0,1} conclusion to k=0 is false. That extension is expressly outside the note's domain.

## 6. Actual finite hand controls for nonnormality, nilpotency and limiting groups

1. **Original-norm skew control.** Let R=[[1,1],[0,1]], set ||x||_*=max(|x1−x2|,|x2|), and A=R diag(−1,1/2)R^−1=[[-1,3/2],[0,1/2]]. This is a contraction of norm one in the specified complex norm. P=[[1,−1],[0,0]], P²=P, AP=PA=−P, and ||P||_*=1, although its Euclidean norm is sqrt(2)>1. Directly A^n=[[(-1)^n,(1/2)^n−(-1)^n],[0,(1/2)^n]], so A^(2n)→P. The ball is skew, not E×F in the original coordinates. Γ={±1}; every unimodular eigenfunction depends only on x1−x2. The stable left coordinate x2 supplies every μ in D and the zero-eigenfunction max(0,|x2|−1/2). This tests the exact nonnormal/original-norm claim rather than an orthogonal projection in a silently replaced Euclidean norm.

2. **Defective stable block.** Let A=[[1/2,1/4],[0,1/2]] in the maximum norm; its operator norm is 3/4≤1. The power is (1/2)^n I+n(1/2)^(n−1)J, where J=[[0,1/4],[0,0]]. It tends to zero, despite the nontrivial Jordan block. The functional x2 is a left eigenfunctional for 1/2 and gives the disk construction; P=0, Γ={1}. A peripheral size-two Jordan block with λ=1 instead has powers I+nJ and cannot be a contraction in any fixed finite-dimensional norm. This checks both permitted and forbidden Jordan phenomena.

3. **Nonzero nilpotent control.** N=[[0,1/2],[0,0]] on the maximum-norm ball satisfies N²=0 but N≠0. K_N² f=f(0), and K_N restricted to functions vanishing at zero has nilpotency order two (take f=x1). Constants give eigenvalue 1 and x2 gives eigenvalue 0. The annihilating identity K_N³=K_N² and the finite nilpotent resolvent leave exactly {0,1}. A=0 is the order-one version, K_A an evaluation projection.

4. **Peripheral plus nilpotent control.** A=diag(−1,N) with the preceding N in dimension three has J empty, is singular and nonzero. A²=P=diag(1,0,0). On observables, K_A²=Q, K_A^4=Q, so K_A satisfies t²(t²−1)=0. The peripheral coordinate, constants and last coordinate give eigenvalues −1,1,0 respectively. Thus the optional zero is controlled by singularity, not by A=0, and no open disk is generated by a zero-only stable spectrum.

5. **Periodic versus irrational controls.** A=I has K=I, Γ={1} and no zero. A=−I has K²=I and exactly ±1, with even/odd observables. If two peripheral values have orders 2 and 3, Γ is the sixth roots and K^6=I. A scalar irrational rotation has dense Γ with full circle spectrum but only its exact group as point spectrum, as proved above. Adding a separate stable coordinate 1/2 gives the mixed row with the same exact boundary group and the whole open disk. Accumulation of eigenvalues on the circle does not make every limit an eigenvalue.

## 7. Concrete observable-space countermodel outside the hypotheses

For the scalar contraction A=1/2 on the ordinary closed disk and any μ=exp(i beta)≠1, set f(z)=exp(−i*beta*log|z|/log2) for z≠0 and f(0)=0. It is bounded and Borel but discontinuous at 0, and f(z/2)=μ f(z). Thus every unimodular μ is admitted if continuous observables are replaced by arbitrary bounded Borel observables. Here S is empty and Γ={1}, so the theorem would fail on that different space. This is an actual falsifier of an unjustified observable-space extension, while confirming why continuity at the stable limit is essential. Holomorphic-only observables similarly omit conjugate monomials and need not generate negative exponents; the theorem explicitly uses all continuous complex observables.

## 8. Compact-semigroup identification reconstructed before its foreign source

Let H be the operator-norm closure of the matrix powers. It is compact in finite dimension, consists of contractions and is abelian. For fixed f, uniform continuity on U gives ||f∘L−f∘M||≤ω_f(||L−M||), so its image under L↦K_L is compact in strong operator topology. That image is also compact and hence closed in Hausdorff weak operator topology, and contains all powers; its strong and weak closures of the powers therefore agree with this image. Although general composition reverses multiplication, the elements here commute, so the representation is multiplicative.

The norm closure G_B of B's powers is a compact group: recurrence puts I and B^−1 in the positive-power closure, and the closure of the cyclic group is a group. For every D in G_B, DP lies in H because P lies in H and the products A^mP=B^mP lie in H; close in m. The set G={DP:D∈G_B} is a group ideal with identity P; any L∈H restricts on E to an element of G_B. If I is any nonempty ideal and h∈I, hP∈I∩G. Multiplication by its inverse in G gives P∈I, then all G⊂I. Thus G is the minimum ideal and P its identity idempotent. Its operator image has identity Qf=f∘P, precisely the idempotent in the second factorization proof above. There is no unproved claim here that an arbitrary spectral projection of a contraction is contractive; the recurrence calculation supplies the particular fact needed.

The precise attribution to EFHN's dated author edition, and the exact old Küster inclusion/open-converse statements, are deliberately still unread external interfaces at this source-first freeze. They will be checked from the actual primary bodies after the seal, without adopting an old audit opinion or conducting a broad priority search.

## Source-only result and remaining interface

The complete original analytic classification has been reconstructed, including the full Banach spectrum rather than only the mixed unimodular exclusion. No internal mathematical obstruction was found by these actual counterexample/boundary mechanisms. This provisional source-only result is conditional only on subsequent verification of the actual historical/classical-source interfaces for those ancillary assertions; it is not a final publication or priority authorization. No scientific/native program or finite harness has run. Current root/peer findings, archive judgments, README/results/program bodies and foreign proofs remain unopened at this freeze.
