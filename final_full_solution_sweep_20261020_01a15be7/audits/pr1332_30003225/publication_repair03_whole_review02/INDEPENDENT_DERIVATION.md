# Reconstruction before candidate or earlier review reading

At this point I have read the cached problem record, the primary arXiv-paper text at Background/terminology (printed pp.5–7), §4.2 (printed pp.30–32), and primary workshop lines around Conjecture 1 (printed pp.2679–2680). I have not read the preparation's manuscript, its reports/checkers/results, root mathematical adoption, or any earlier reviewer report. Filenames, the caller-pinned verifier, and tracker configuration have been observed. The cached record says union; both primary mathematical sources say intersection. This is an actual transcription distinction, not a harmless equivalent formulation.

Use neutral geometric indexing to avoid importing a desired conclusion. Blow up the origin p_0, then n−1 successive free points following y=0. Call the final divisor D_n; in the final affine chart x=u, y=u^n v, its valuation is (1,n). Fix k common centers p_0,...,p_{k−1}, with 1≤k≤n. The reference divisor created at the last fixed center is D_k, valuation (1,k). Contact counts common blowup centers, so distinct free chains in this family have contact at least k. The source's remark i_0=1 compares to the first exceptional E_0; therefore p_{i_0} in its displayed conjecture cannot safely be read with a rigid zero-based indexing inconsistent with that remark. State the geometric chain independently and disclose the source mismatch.

For k≥2, every all-free n-center chain sharing these k centers is specified uniquely by the finite smooth jet P(x)=a_k x^k+...+a_{n−1}x^{n−1}. There are no nonzero restrictions on these coefficients: being free means a finite affine value away from the old-component intersection. Its final chart is x=u, y=P(u)+u^n v. Arcs transverse to the final exceptional have ord(x)=1 and ord(y−P(x))=n with the final v-center away from the old component. Their image is dense in the irreducible closed coefficient cylinder

  N_P={ord x≥1, ord(y−P(x))≥n}.

The density can be checked in every sufficiently high finite jet space by the open conditions on the coefficients of t in x and t^n in y−P(x). Thus it includes arcs whose x or y is identically zero and the constant arc; no chart argument on those special arcs is needed.

Intersecting over all P, the choice P=0 forces ord y≥n. The choices P=c x^k with c≠0 then force k ord x≥n. Conversely those two inequalities make every P(x) have order at least n. Hence exactly

  ⋂_P N_P={ord x≥ceil(n/k), ord y≥n}.

Indeed only P=0 and P=x^k are needed. At k=n the family has one member and the formula remains valid. At k=1, the finite-slope subfamily already forces ord x,ord y≥n; the vertical-direction charts impose no stronger restriction, since every smooth curvetta jet evaluated on an arc with both coordinates of order ≥n has order ≥n. Thus the same formula extends there.

For the reference D_k, arcs meeting it at order q at a general smooth point have ord x=q, ord y=kq. Their closure is the rectangle

  Cont_q(D_k)={ord x≥q, ord y≥kq}.

This follows from the same irreducible-cylinder/dense-open argument, not from identifying raw exact-order contact with its closure. Equality with the intersection forces q=ceil(n/k) and kq=n, equivalently k divides n. So n=3,k=2 gives a rectangle (2,3) not equal to any q(1,2). The order pair (2,3) excludes q≥2, and (1,2) in Cont_1(D_2) excludes q=1. Both can be represented by explicit monomial arcs (t²,t³) and (t,t²). For an arbitrary toric prime divisor rather than the specified D_k, the rectangle *is* the maximal divisorial set for (m,n), m=ceil(n/k): divide by gcd(m,n) for the primitive valuation and use that gcd as multiplicity. Non-representability must therefore specify the reference divisor.

This mechanism establishes a counterexample to the universal source intersection conjecture under the geometric last-common-center reading and gives an exact all-free-chain classification. It does not classify satellite chains, settle the general generalized Nash adjacency problem, or establish bibliographic novelty. The union transcription is a separate problem, not resolved by negating the source intersection conjecture.
