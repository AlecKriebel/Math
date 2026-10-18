# Independent lambda-ring adversarial report

**Verdict:** the proposed universal nonmembership statement is contradicted at n=8 by a later primary theorem, combined with the transfer argument already given in the original source. In the original generic setting, the resulting membership is e8 in gamma^5. This is a source-backed mathematical deduction, not a claimed new self-contained proof of the 2023 theorem.

## Scope and independence

I read the root AGENTS.md, the two assigned primary sources, and a later primary source supplied as a lead by the parent reviewer. I did not inspect the candidate, submitted proof, another shard, or another review. My pre-lead findings are preserved separately in ORIGINAL_FINDINGS.md. The initial lambda-filtration analysis was independent; the later-literature lead was not independently discovered by this subagent. No further agents were spawned. No external communication or Git mutation occurred.

## Exact claim and hypotheses

Write E=F(S), where S is the Severi–Brauer variety of the maximal-index even Clifford algebra of the original odd-dimensional form. The original theorem assumes ind C0(phi)=2^n before passage to E. The relevant X_E is the maximal orthogonal Grassmannian, equally identifiable with a component of the maximal Grassmannian of the even-dimensional companion of dimension 2n+2. Let e_n denote the K-theoretical special Schubert class defined by its split restriction. The target is

    for every n>=8, e_n is not in gamma^d K(X_E),
    d=n+1-floor((n+1)/2)=ceil((n+1)/2).

This is Conjecture 4.7, not Theorem 4.3, in [Karpenko's original paper](https://sites.ualberta.ca/~karpenko/publ/a16i3.pdf), p.11; it is repeated as Conjecture 3 in the [OWR report](https://ems.press/content/serial-article-files/46609), p.227. Theorem 4.3 establishes gamma=topological in this generic setting. It does not establish the claimed position of e_n.

## Lambda-ring mechanism and the scalar-extension trap

After the Clifford algebra splits, restriction to a splitting field is an isomorphism of K-groups and commutes with exterior powers. It is therefore an isomorphism of augmented lambda rings, and transports the gamma filtration exactly. The original p.11 explicitly permits the gamma computation on the split complex Grassmannian.

The topological filtration does not have the same invariance. One only obtains

    res(gamma^i K(X_E)) = gamma^i K(X_split)
      subset topological^i K(X_split).

On X_E the first filtration equals its own topological filtration by Theorem 4.3. Nothing here says that restriction is strict for the two topological filtrations. In particular, the split Schubert representative has codimension n, while the corresponding preimage in K(X_E) can fail to be represented by a codimension-n coherent sheaf over E. Describing e_n as a K-class does not imply that the associated Schubert subvariety is defined over E.

Consequently, observing that the split class has leading Chow degree n does not separate it from gamma^d for d<=n. It is compatible with that membership. At n=8, the original remark proves e8 in gamma^4 and conjectures its absence from gamma^5; it does not prove exact gamma depth four.

Integral information is essential. On the split Grassmannian, Chow Chern classes of the tautological bundle are c_i(T)=(-1)^i*2e_i (2023 source, p.4). After inverting 2, their leading terms generate the Chow ring. Induction through the finite topological filtration then identifies gamma and topological filtrations after inverting 2. Thus some 2-power multiple of the split e_n lies in gamma^d whenever d<=n. A rational calculation or a statement merely about 2-adic sizes cannot establish the original integral nonmembership. A parity obstruction must be defined on actual K-theory generators with all correction terms, rather than on the homogeneous Chow presentation substituted for K-theory.

## Decisive n=8 check using the 2023 primary result

The actual text of [On isotropy fields of Spin(18)-torsors](https://sites.ualberta.ca/~karpenko/publ/spind18-04.pdf), dated 28 August 2023, proves Theorem 4.1 and gives Corollary 4.4 on p.6. Its exponent table is

    i0,...,i8 = 0,1,2,3,3,3,4,4,4,

where the index of the mth Grassmannian is 2^(i_m). Crucially, the paragraph following the corollary applies the resulting extension assertion to **any** 18-dimensional nondegenerate quadratic form with trivial discriminant and Clifford invariant. There is a finite extension L/E of degree N not divisible by 16 with Witt index at least 5. The generic 18-dimensional form from the original construction satisfies these hypotheses. Thus no identification of two different genericity conventions is needed.

Apply the original p.11 proof with m=18, r=4 and n=8. Put Y for the associated quadric, whose dimension is 16, and h for the K-class of a hyperplane section. Because the Witt index over L is at least 4, l3 is represented over L by a 3-dimensional linear space, so

    l3 in topological^13 K(Y_L).

Transfer supplies N*l3 in topological^13 K(Y_E). To justify the power-of-two extraction integrally, take also a finite splitting extension of 2-power degree 2^s. Its transfer supplies 2^s*l3 in the same term. Since v2(N)<=3, an integer Bezout combination, followed if necessary by multiplication by a power of 2, gives

    8*l3 in topological^13 K(Y_E).

This uses neither division by an odd integer in K nor unproved saturation of the filtration. In the common split K-group, the identity used in the original proof specializes to

    8*l3 = l0 + h^15 + 2*h^14 + 4*h^13.

The hyperplane terms all lie in topological^13, so l0 also lies there. In the incidence correspondence from the original source,

    e8 = f_* g^*(l0).

The pullback preserves topological filtration, and f_* lowers its term number by the fiber dimension 8. Therefore

    e8 in topological^5 K(X_E) = gamma^5 K(X_E).

For n=8 the target exponent is exactly 9-floor(9/2)=5. This contradicts the universal target. It establishes a counterexample to the advertised nonmembership, without determining whether e8 belongs to gamma^6 or higher. It makes no assertion about every n>=9.

The same conclusion also follows by the contrapositive of the original implication Conjecture 4.7 => Conjecture 3.3, but the explicit calculation above checks the quantifiers and term shifts directly. The 2015/2016 conjectured fourth-Grassmannian index was 16 for dimension 18; the later value is 8.

## Independent finite algebra check of the later proof

The 2023 proof reduces its critical-exponent test to a mod-2 polynomial. Independently expanding

    product over I subset {5,6,7,8} of (x + sum over i in I of x_i)

over F2, I found 150 surviving monomials, with x-degrees 1,2,4,8,16. The coefficient of x^8*x7^4*x8^4 is 1. Under x=e1, the x^8 term is e8. The coefficient monomial has exponents below the respective flag-basis bounds (4<7 and 4<8), so it survives the basis reduction used in the source. Terms with some exponent 8 vanish by x_i^8=0; the other coefficient terms are already within the indicated flag basis. The check is reproducible with `_local/check_polynomial.py`; output is `_local/polynomial_check.json`.

This verifies the concrete polynomial witness in Theorem 4.1. It does not independently reprove Proposition 3.2, the earlier structural theorems cited there, or the source's specialization result. Those are identified external mathematical inputs, rather than hidden assumptions in a claimed self-contained proof.

## Exact integral computation that would have sufficed

Remark 4.4 of the original paper says that gamma^d is the integer span of all

    e1^a0 * product_i c_i(T)^ai,
    a0 + sum_i i*ai >= d.

Using the source's K-theoretical Chern-class convention, expand these actual K-classes in an integral Schubert basis of rank 2^n. The split dimension D=n(n+1)/2 truncates the list: weighted degree above D vanishes. The resulting integer matrix M_n gives an exact membership problem M_n*z=v_n, where v_n is the coordinate vector of e_n. Hermite or Smith normal form plus explicit transformation matrices yields an auditable answer at each n.

A nonmembership certificate could instead be a covector w_n modulo 2^k satisfying w_n*M_n=0 but w_n*v_n!=0, or a rational separator if the target lay outside the rational column span. For a proposed all-n result, a finite batch of matrices is insufficient: a uniform theorem validating the certificate for every n is needed. In this case no such nonmembership certificate can exist at n=8, given the established membership above. Any calculation purporting to produce one must have an erroneous K-presentation, wrong filtration weights, incomplete generator list, or an invalid reduction.

## Final limitations and status

The strongest conclusion is a primary-source-backed refutation of the stated universal target at n=8, together with an explicitly checked transfer bridge. The fresh computation verifies one finite algebraic witness within the later source. No standalone full K-ring expansion for e8 was obtained, and no new exact gamma-depth theorem is claimed. The original lambda-ring route is blocked as a route to the full advertised conclusion because that conclusion is false at its first permitted n.

Review completion estimate: 100% for this assigned source-only adversarial audit; 0% toward proving the contradicted universal nonmembership statement.
