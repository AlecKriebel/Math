# Independent final scoped review: free commutators, 30004022

## Verdict

**PASS_FULL_FIVE_TURN_SCOPED_PACKET. No mandatory mathematical revisions. Original target remains UNSOLVED, 5/5 substantive author turns.**

The fixed-factor obstructions, imaginary-axis rigidity, bounded linearization and arbitrary-law truncation estimate are valid in their stated scopes. The broader matrix-valued construction relies on credited pre-existing subordination and does not establish the stronger scalar/positive-factor extension requested by the source. No historical-priority or novelty certification is made.

This is an independent AI-assisted mathematical and executable audit, not human peer review or formal proof-assistant certification. Review did not constitute a sixth author search.

## Frozen input and reproduction

`FINAL_AUTHOR_MANIFEST.json` SHA-256:

`7700308e01180f2771479a42b644247ee20f1b2b0324e95c43832362dbcb9153`.

All 45 listed author files were verified, as were 85 entries in the four historical turn manifests. The final packet has 46 files including its manifest. All seven locally supplied primary PDFs match their recorded lengths and hashes. All five author checkers were replayed byte-for-byte, totaling **10,364 exact assertions**. The replay and source receipts accompany this report.

An independent checker imports no author code. It uses analytic R/S-transform series rather than the author's colored noncrossing recursion, and different exact Hermitian matrix families. Its **125 exact assertions** pass, including a five-dimensional outlier family with both actual and bounded rank fraction 2/5. Small assertion counts do not replace the analytic audit below, and no finite matrix is assumed free.

## Exact source and representation boundary

The complete Götze–Chistyakov contribution, *Representations of Free Commutators*, printed pp. 3194–3195 of [OWR 53/2018](https://ems.press/content/serial-article-files/46774?nt=1), was independently read in full, and both pages were visually inspected. Its general identity places the arcsine law on the same side as the commutator square. Its stronger factorization and scalar Nevanlinna description are given for even inputs and an explicitly stated free-square-root subclass. The final question seeks extensions of those representations to nonsymmetric inputs. It already acknowledges earlier general moment and functional descriptions. The packet's unresolved disposition is therefore appropriate; the larger matrix method cannot be promoted to a new solution merely because it determines the law.

[Nica–Speicher, Remark 1.12](https://arxiv.org/abs/funct-an/9612001) was checked for the known projection-based positivity failures. Those precedents are credited. [Belinschi–Mai–Speicher, Theorem 2.2](https://arxiv.org/abs/1303.3196), together with its linearization discussion, was checked directly in the hashed primary PDF. Its bounded self-adjoint, operator-valued hypotheses and fixed-point branch are the ones used in Turn 4. [Ando–Matsuzawa, Section 2](https://www.impan.pl/shop/en/publication/transaction/download/product/86036) was read in the hashed local primary PDF for the affiliated-operator algebra and self-adjointness statements; a fresh web open of that publisher URL failed, so no successful fresh online retrieval of that paper is claimed. The local PDF provides the inspected theorem text.

The arithmetic reference's positive free-multiplicative convolution framework supports commutativity for arbitrary positive laws. Later literature PDFs were hash-bound as specified by the author. This review does not certify that every later literature result has been exhausted.

## Turn 1: projection obstruction and moment legitimacy

### Freeness and the algebraic square

Replacing a centered function of UPU by U times the corresponding centered function of P times U expands an alternating centered word into an alternating centered word in the original free algebras. Because U is centered and U²=1, this proves P and UPU are free. Start/end factors cause no exception. Direct expansion gives

    [i(PU−UP)]² = (P−UPU)².

The difference of two projections lies between −1 and 1, so its square is bounded by 1. The trace parameter t=p(1−p) is invariant under p↔1−p.

### Independent moment derivation

From the projection Cauchy transform, the inverse relation yields

    R_P(w)=[w−1+sqrt(1+(4p−2)w+w²)]/(2w).

For D=P−P', freeness gives R_D(w)=R_P(w)−R_P(−w). On the formal branch with constant moment 1, its moment generating function satisfies

    M_D(v)²=[1−(2p−1)²v²]/(1−v²).

Expanding that branch independently recovers the three stated moments of Y=D²:

    2t,  2t−2t²,  2t−4t²+4t³.

This verifies the coefficients without reusing the author's cumulant code. The branch at p=1/2 gives the arcsine law on [−1,1] for D, and at p=0 or 1 it gives D=0.

The arcsine-on-[0,4] moments are 2,6,20. Independent formal S-transform inversion recovers the product-moment expressions 2b1, 4b2+2b1² and 8b3+12b1b2. Thus the forced second-factor moments and determinant t³(t−1/4) have the correct normalization and sign. This determinant is negative for every 0<p<1 except p=1/2. Cauchy–Schwarz with x^(1/2) and x^(3/2) excludes a positive measure. The boundary factor delta_(1/4) at p=1/2 and delta_0 at p=0,1 are correct.

### Initially unbounded factors

The proof does not assume the moments it later uses. Compact spectral distribution of a positive affiliated operator in a faithful finite tracial algebra implies actual boundedness, since the spectral projections beyond that support have trace zero. If A is bounded positive with mean alpha>0, the bounded compression by a B-spectral projection gives

    E_B(e_m B^(1/2) A B^(1/2) e_m)=alpha B e_m.

The outer factors B^(1/2)e_m are bounded. Positivity and the product norm bound therefore imply B≤||R||/alpha. With alpha=2, every putative positive factor in Turn 1 is compact. The third-moment test is consequently legitimate for arbitrary positive laws originally proposed as factors.

## Turn 2: analytic rigidity without moments

The sign convention G(z)=integral(z−x)^−1 dmu(x) is consistent. For symmetric eta, iyG_eta(iy) is real. If N(iy)=−is(y), the scalar equation therefore forces G_mu(is(y)) to be purely imaginary. Continuity of s and its positive asymptotic slope provide a nonempty interval of positive values, with an interior accumulation point in the upper half-plane after multiplication by i.

For reflected mu, G_ref(is)=−conjugate(G_mu(is)). The identity theorem and uniqueness of finite-measure Cauchy transforms therefore force symmetry of mu. All integral expressions used along the imaginary axis are bounded; no first moment or expansion at infinity is being smuggled in.

Direct independent simplification of the centered two-point transform gives exactly

    Im[(-is)G(-is)]
      = s p(1−p)(2p−1)/[(s²+p²)(s²+(1−p)²)].

It never vanishes for s>0 and a nontrivial p≠1/2. Centering changes neither that asymmetry nor the commutator with U. Conjugation by U sends the example commutator to its negative, so the required symmetric output law is valid for this example.

The theorem only excludes the unchanged imaginary-axis-preserving mapping class and equation with the original nonsymmetric transform. It does not exclude revised scalar equations, functions leaving that axis, or matrix-valued systems. The packet keeps that boundary explicit.

## Turn 3: arbitrary positive fixed factors

### Compact-factor lemma and domains

The compact-product lemma is sound in the stated finite tracial affiliated framework. The key order step can be read in its positive affiliated-operator sense: for A_n=min(A,n),

    R−B^(1/2)A_nB^(1/2)
       = B^(1/2)(A−A_n)B^(1/2) ≥ 0.

The right side is the square T* T of the corresponding closed affiliated product. Thus the truncated positive product is dominated by the bounded R and is itself bounded. Equivalently one may work on the completely dense common polynomial domains and their positive-form closures. Subsequent B-spectral compression produces only bounded factors, so conditional expectation and bimodularity are applied within their legitimate domain.

Choosing one truncation with alpha_n>0 yields B≤M/alpha_n. Since B is nonzero, its now finite mean beta is positive. Commutativity of positive free multiplicative convolution gives the reversed positive product the same compact distribution. Repeating the bounded-factor argument then gives A≤M/beta. There is no need to condition an undefined unbounded product or assume a nonexistent trace moment. The exclusion of delta_0 and faithfulness hypotheses are essential and are present.

The background affiliated *-algebra facts were verified in Ando–Matsuzawa Theorem 2.2 and Proposition 2.6. They concern closures of products/sums in a finite von Neumann algebra, not arbitrary densely defined operators on unrelated Hilbert spaces.

### Classification coefficients and quantifiers

After normalizing the first factor to mean one, independent S-transform calculations verify all coefficients in the product and forced-factor moment formulas. The determinant is

    t³[-8(r−1)+(32r²−8r−16s−4)t].

If r>1, the negative constant term gives a strictly negative determinant for some sufficiently small positive p, with t=p(1−p). The theorem's assumption holds throughout a sufficiently small interval of p, so the selection is legitimate. It does not substitute p=0 for a positive-variance case. When r=1, positivity makes the first law delta_1; undoing normalization gives precisely the nonzero Dirac laws. Their rescaling converse is immediate. The zero Dirac law cannot produce the nonzero Y_p.

For normalized arcsine r=3/2,s=5/2, the determinant becomes 16t³(t−1/4), agreeing with the scaled Turn 1 test. The fixed factor is required to be independent of the input. Input-dependent factorizations remain outside this impossibility theorem.

## Turn 4: bounded linearization and subordination

The lower corner Q is self-adjoint and Q²=I. The noncommutative identity [a,b]Q[a,b]^T=−c has the stated sign, hence the Schur complement at epsilon=0 is z−c.

For epsilon>0, inversion of i epsilon I−Q gives the exact upper-left inverse

    [z−c/(1+epsilon²)+i epsilon(a²+b²)/(1+epsilon²)]^−1.

The imaginary part is at least eta I. The inverse exists and is bounded by 1/eta: the coercivity bound gives an injective closed range, and the corresponding adjoint bound makes that range dense. Both inverse bounds are therefore valid, not merely formal inverses.

The resolvent difference has the stated error

    [2epsilon² A B+epsilon(A²+B²)]/[(1+epsilon²)eta²].

The plus sign on the dissipative term is essential and correct. The independent checker uses complex Hermitian three-dimensional matrices, verifies the full nine-dimensional block inverse by multiplication, and checks every principal minor of the exact positive-semidefinite error-bound matrix. These are deterministic tests of the identity and bound; their matrices are not free.

For the analytic free step, the larger algebras M3 tensor alg(a) and M3 tensor alg(b) are free over M3: entries of centered alternating matrix products are sums of centered alternating scalar words. Their generated subalgebras containing X=M tensor a and Y=N tensor b inherit this property. Both variables are bounded self-adjoint. D=Lambda_epsilon−Q0 has strictly positive imaginary part, since Q0 is self-adjoint. This verifies every operative hypothesis of the credited BMS Theorem 2.2.

The order h_Y(h_X(W)+D)+D and the companion reciprocal-transform equation match that theorem. Its unique analytic branch and convergence from any strict upper-half-plane starting matrix are credited inputs. They are not derived from the finite checker or claimed to provide a finite-iteration stopping error. No real-axis density limit follows from the upper-half-plane norm estimate.

## Turn 5: arbitrary laws, rank and limits

Free self-adjoint affiliated realizations of arbitrary Borel laws exist in the finite tracial free-product framework. The affiliated algebra is closed under the indicated closed sums, products and involution. Hence i(ab−ba) is self-adjoint there; no finite variance or product moment is needed. This does not rely on the generally false unrestricted domain rule for arbitrary unbounded operators.

Range supports and polar decomposition give equality of left and right support traces. The range of a closed sum is contained in the closure of the sum of the original ranges; likewise a closed product's range is contained in the first factor's closed range. Passing to adjoints yields the second factor bound. Thus both rank inequalities used in the proof remain valid for affiliated operators.

Clipping changes exactly the spectral subspace |a|>T, including no mass at the boundary atoms ±T. The four-term commutator-difference identity is exact in the affiliated algebra. Each input error occurs twice, giving rank at most 2q_a+2q_b, capped at 1. No smaller coefficient is silently assumed.

For arbitrary self-adjoint affiliated H,K, both resolvents are bounded and the algebraic resolvent identity is valid in the affiliated algebra. Its difference has rank no greater than that of H−K and norm at most 2/eta. For a bounded V, |trace(V)|≤trace(|V|)≤||V|| rk(V). These facts yield exactly 2delta_T/eta. The independent five-dimensional family attains the rank bound 2/5 before the trace estimate, and separately checks unchanged threshold atoms.

Functional-calculus clipping preserves the separate input algebras and their freeness. Combining its rank estimate with the bounded pencil gives the stated two-term bound. With epsilon=T^−3 and T≥1, the regularization term is bounded by 2(T^−4+T^−1)/eta² and tends to zero; probability tails also tend to zero without moments. Uniformity is valid on eta≥eta0>0.

The inner exact subordination fixed-point limit is taken for each fixed T,epsilon before the outer T limit. The packet neither exchanges uncontrolled limits nor asserts an effective algorithm for arbitrary uneffectively specified measures. It also does not infer real-axis densities from this estimate.

## Final assessment and evidence use

All five retained scoped results pass. The source's broader nonsymmetric scalar/positive-factor problem remains unresolved; ruling out particular unchanged ansatzes is not a universal impossibility theorem for every revised representation. Conversely, the credited matrix-valued route to the Cauchy transform is not the stronger source extension.

The accompanying independent checker and all five author replay receipts are reproducible exact controls. Domain/order arguments, Cauchy uniqueness and the cited analytic subordination theorem are reviewed mathematically rather than inferred from those finite tests. No source PDF is redistributed in this portable review bundle. Original disposition remains **unsolved, 5/5**, with no mandatory revision and no new author turn.
