# EP-538: focused independent recheck of the safe-kernel lower bound

Date: 2026-10-10. Target: the prior STARFLEET Math matching-order result for Erdős Problem 538, and Sections 3–8 of the retained reconstructed mathematical audit.

## Decision

**Accepted for the stated finite lower bound and its original global cap. No mathematical correction is needed in Sections 3–8.** The construction produces, for every natural number N, a set A of positive integers at most N such that every integer m has at most two ordered pairs (p,a), with p prime, a in A, and m=pa, and

    log(N+1) <= 4 + 8192(ell(N)+1) sum_{a in A} 1/a,

where L(N)=floor(log_2 N) for N>=1, L(0)=0, and ell(N)=floor(log_2 L(N)) when L(N)>=1, with ell(N)=0 otherwise. The logarithm on the left is natural.

This is a second conventional mathematical review of a prior claim, credited to STARFLEET Math. It does not claim novelty, an exact maximum, a sharp leading constant, or matching dependence on an unbounded r. The upper bound is outside this focused review. No author program or primary-audit checker was executed; no Lean build, dependency installation, or formal-kernel verification was performed. Independent finite controls are supplementary to the proof below.

Primary public attribution:

- P. Erdős, *Problems and Results on Combinatorial Number Theory* (1973), section 4, printed p.124, equation (4.5): https://www.renyi.hu/~p_erdos/1973-21.pdf
- STARFLEET Math, *Erdős Problem #538: the matching-order bound*: https://www.starfleetmath.com/
- STARFLEET Math verification archive: https://www.starfleetmath.com/downloads/verify/erdos-538/erdos-538-solution.zip

## 1. Child count, including the nonzero-coefficient requirement

Fix k>=2 and d=k-1. Over a finite field of odd order q, a palette vertex is independently assigned a uniformly distributed label (phi,c) in F_q^d x F_q. For a child with k vertices, the matrix of phi-columns has d rows and d+1 columns. Favorability requires rank d, a one-dimensional kernel with every coordinate nonzero, a nonzero coefficient vector c, and isotropy of its kernel line for the diagonal bilinear form with entries c.

Order the columns from 0 through d. Every favorable child has a unique normalized kernel vector (1,t_1,...,t_d), where all t_i are nonzero. The last d columns must be independent: a relation on them would extend to a kernel vector with first coordinate zero, impossible in the given one-dimensional full-support kernel. Conversely, any ordered basis b_1,...,b_d and nonzero tail t determine the first column uniquely as -sum t_i b_i. The resulting matrix has exactly the desired kernel. These constructions are inverse, so there is no hidden multiplicity in the parameter count.

There are (q-1)^d tails and product_{i=0}^{d-1}(q^d-q^i) ordered bases. For each such matrix, isotropy imposes the single nontrivial linear condition

    c_0 + sum_{i=1}^d c_i t_i^2 = 0.

There are q^d solutions, exactly one of which is the prohibited zero vector. The favorable probability is therefore exactly

    (1/q) (1-1/q)^d product_{j=1}^d(1-q^{-j}) (1-q^{-d}).

The total sample-space denominator is q^{(d+1)^2}, since each of d+1 vertices has d+1 label coordinates. For q>=2(d+1), both the first power and the middle product are at least (1-1/q)^d >= 1-d/q >= 1/2; the last factor is at least 1/2. This proves the claimed probability >=1/(8q). The argument needs d>=1. It does not silently apply to k=1.

## 2. Exact outside danger probability

Keep a favorable child fixed and use its basis b_i and normalized kernel as above. Write the new column as sum a_i b_i and let its new diagonal coefficient be c_x. The parent matrix has rank d and d+2 columns. Its two-dimensional kernel has basis

    u=(1,t_1,...,t_d,0),
    v=(0,-a_1,...,-a_d,1).

The diagonal form restricted to this plane is identically zero precisely when its three Gram entries B(u,u), B(u,v), and B(v,v) vanish. The first is already zero. The other two give

    sum c_i t_i a_i = 0,
    c_x = -sum c_i a_i^2.

The first is a nonzero functional of a. Indeed, if all c_i t_i vanished for i>=1, then the nonzero t_i would force c_i=0 for i>=1; child isotropy would then force c_0=0. This contradicts the required nonzero coefficient vector.

A nonzero functional on F_q^d has exactly q^{d-1} zeros. For every zero a, exactly one c_x works. The basis-coordinate change from a to phi_x is bijective, so exactly q^{d-1} of the q^{d+1} outside labels are dangerous. The probability is exactly 1/q^2, uniformly over every favorable child, including children with some zero c_i. No stronger assumption that every c_i is nonzero is needed.

Conditional on the fixed child labels, all m-k outside labels are independent. In fact the conditional safe probability is exactly (1-1/q^2)^{m-k}; the weaker union bound >=1-(m-k)/q^2 is sufficient. If 2(m-k)<=q^2, a fixed child is both favorable and safe with probability >=1/(16q).

## 3. One labeling works for the whole palette

For each k-subset S let I_S indicate that S is favorable and none of the other palette vertices is dangerous for it. Linearity of expectation gives

    E sum_S I_S >= binom(m,k)/(16q).

The probability space is finite. Hence some single labeling has at least this many safe children. This is not a separate choice of labels for each child. Dependence between child indicators is irrelevant, and no integrality rounding is being suppressed: an integer-valued random variable has a realized value at least its real expectation.

Take all safe children in this one labeling to be F. Any parent T of size k+1 that contains a member of F has rank d, so its relation space is a plane. A selected facet omitting x yields an isotropic kernel line whose coordinate x is zero and whose other coordinates are nonzero. Distinct omissions give different lines, because proportional nonzero vectors have identical zero-coordinate sets.

If three selected facets existed, take representatives u,v of the first two lines. They form a basis. A representative of the third is a*u+b*v with a and b both nonzero. Its isotropy, together with that of u and v, gives 2ab B(u,v)=0. Odd characteristic implies B(u,v)=0, and the entire Gram matrix is consequently zero. The parent extension is then dangerous for each selected facet, contradicting safety. Thus every (k+1)-subset contains at most two members of F.

Apply Bertrand's postulate to 2k to obtain a prime 2k<q<4k, in particular q<=4k and q odd. Put m=2k^2. Then q>=2k and

    2(m-k)=4k^2-2k <= q^2.

We have simultaneously obtained a common palette with

    |F|/binom(m,k) >= 1/(16q) >= 1/(64k)

and parent cap two. Only existence is required; no efficient labeling search is claimed.

## 4. Weighted transfer, with all color collisions accounted for

Consider any finite weighted family of k-element subsets of an arbitrary ground set, with nonnegative weights and total weight W_k. The union of these supports is finite. Give each ground element a uniform independent color from the palette of size 2k^2. For a fixed support, the union bound over its pairs gives collision probability at most

    binom(k,2)/(2k^2) = (k-1)/(4k) < 1/2.

Weighted expectation therefore supplies one coloring whose rainbow supports have total weight at least W_k/2. This is a weighted statement; there is no comparison between support count and support mass.

For that fixed coloring, apply a uniform random permutation of the palette. For any rainbow support, its k distinct colors map uniformly to all k-subsets: each target subset has exactly k!(m-k)! preimage permutations. Hence its probability of entering F is |F|/binom(m,k), irrespective of its weight. Another finite average gives a single permutation retaining weight at least W_k/(128k).

It remains to check parent cap after lifting colors back to ground elements. If a (k+1)-element ground parent is rainbow, deletion corresponds injectively to a facet of a single palette parent, giving cap two. If it is not rainbow, a deletion can produce k distinct colors only when exactly one color occurs twice and every other color occurs once. In that case only the two occurrences of the repeated color may be deleted. They may yield the same palette subset and both may be selected, but there are still only two ground facets. Every other repeated-color pattern has zero rainbow deletions. Thus the lift counts ground occurrences correctly even when the color map is noninjective.

## 5. The cap really holds for every integer product

For each k>=2 apply the preceding result to the prime supports of squarefree a<=N with exactly k prime factors, weighted by 1/a. Prime supports identify the integers uniquely. Let A_k be the retained family and M_k its reciprocal mass; then W_k<=128k M_k.

For an arbitrary integer m:

- If m is positive and squarefree, each representation m=pa with a in A_k corresponds to deleting p from its prime support. Necessarily the parent has k+1 prime factors. These are exactly the ground facets controlled above; the cutoff a<=N merely discards some possible facets. There are at most two representations, even when m>N or p>N.
- If m is positive and not squarefree, m/p can be squarefree for at most one prime p. Such a representation requires precisely one exponent of m to be two, that prime to be p, and every other exponent to be one. If there are two repeated primes or an exponent exceeds two, no such representation is possible. Thus this case contributes at most one pair.
- If m<=0 there are no representations by positive a and positive primes.

For k=1 take all primes at most N. Their products with another prime have two representations when the primes are distinct, one when equal, and none otherwise. This layer already has cap two and satisfies W_1<=128 M_1 without finite-field machinery.

Unite A_1 through A_K. Every representation m=pa satisfies Omega(a)=Omega(m)-1, where Omega counts prime factors with multiplicity. Since the chosen a are squarefree, a in A_k has Omega(a)=k. Thus all representations of a fixed m belong to one and the same selected layer. The bounds do not add over layers, even for nonsquarefree m. The union A has the original global cap two and mass M satisfying

    W_{<=K} = sum_{k=1}^K W_k <= 128 sum_{k=1}^K k M_k <= 128 K M.

Squarefreeness is imposed only on the constructed lower witness, not on the statement of the original extremal problem.

## 6. Harmonic truncation and the exact coefficient 8192

Assume first N>=1. Let H_N=sum_{n<=N}1/n, let W be the reciprocal mass of squarefree a<=N including a=1, let P(N)=sum_{p<=N}1/p, and let J=sum_{a<=N, squarefree} Omega(a)/a.

Every integer has a unique decomposition n=b^2 a with a squarefree. Enlarging the summation region yields

    H_N <= W sum_{b=1}^N 1/b^2 <= 2W,

because 1/b^2<=1/(b(b-1)) for b>=2 and the latter sum telescopes. Expanding Omega(a) as the number of prime divisors and writing a=pb yields

    J <= P(N) H_N.

This only enlarges a finite region: the actual b are squarefree, coprime to p, and obey pb<=N, whereas the right side allows every p<=N and every b<=N.

Let T be the mass of squarefree integers with Omega>=K+1. Then (K+1)T<=J. If K+1>=4P(N),

    T <= H_N/4 <= W/2.

The remaining squarefree mass is exactly 1+W_{<=K}. Hence W<=2(1+W_{<=K})<=2(1+128KM), and therefore

    H_N <= 4 + 512 K M.                         (1)

For clarity, the necessary prime-harmonic estimate has an elementary finite proof. For j>=2 put n=2^j. Every prime n<=p<2n actually satisfies n<p<2n, since n is composite. Such a p divides binom(2n,n): it occurs once in (2n)! and not in n!. Therefore the product of all these distinct primes is at most binom(2n,n)<=2^{2n}. If there are h of them, comparing logarithms gives h*j<=2n, and their reciprocal sum is at most h/n<=2/j. The j=1 block has mass 1/2+1/3=5/6<=2. Partial last blocks are bounded by their full blocks. Consequently, for L=floor(log_2 N)>=1,

    P(N) <= 2 H_L.

Split {1,...,L} into the blocks {2^i,...,min(2^{i+1}-1,L)}. Each contains at most 2^i terms, all <=2^{-i}, so each contributes at most one. There are ell(N)+1 blocks, giving H_L<=ell(N)+1. If L=0, P(N)=0.

Set K=16(ell(N)+1), an integer >=16. The derived estimate even gives 4P(N)<=8(ell(N)+1)<=K, so the required K+1>=4P(N) certainly holds. Substitute in (1) and use the integral bound log(N+1)<=H_N to obtain

    log(N+1) <= 4 + (512*16)(ell(N)+1) M
              = 4 + 8192(ell(N)+1) M.

The unused slack in the prime bound does not change the claimed coefficient. For N=0 choose A empty and obtain 0<=4 directly. At N=1 the same construction, which omits the unit, may also be empty and yields log 2<=4. No ordinary real logarithm of zero is taken.

## 7. Review boundaries and independent controls

The mathematical acceptance above covers all parameters, not just the finite tests. Particular failure modes explicitly excluded are: using a different labeling for each child; treating zero c as favorable; deriving a characteristic-two conclusion from polarization; applying a palette cap only to rainbow parents; adding the layer caps; limiting the original cap to m<=N; or omitting the unit when decomposing squarefree harmonic mass.

Historical supplementary controls were authored independently for this recheck. They use direct brute-force relation spaces rather than the primary audit's modular Gaussian-elimination routine. They compare raw favorable-label counts and direct restricted Gram matrices with the count formulas; enumerate binary forms; check color-collision and weighted-permutation identities; and check squarefree integer layer and harmonic inequalities with exact rational arithmetic. They passed normal, -O, and -OO modes with byte-identical output. Only outcome and hash/byte metadata are retained in this publication edition; code and raw computational certificates are excluded. These historical mathematical checks were not rerun during publication preparation. No finite computation is offered as a proof of the universal conclusion.
