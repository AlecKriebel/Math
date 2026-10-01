# Independent full review: spherical Fibonacci separation, 30002163

## Mathematical verdict

**PASS_COMPLETE_EXACT_FINITE_SOURCE_TARGET. No mandatory mathematical correction.**

The unchanged PROOF.md SHA-256 `c2cc924751b2f5e6d22d129de6170c3415cca9167c721a0798fc01631cca8c2c` proves the exact minimum chordal distance2/sqrt(F_n) at every nontrivial finite Fibonacci size. This is the whole imported source target, not only an asymptotic statement or a finite computational sample. A claimed_solved1/5 disposition is supported, with the exact unshifted rational-angle convention and no historical-novelty certification. Parent retains the publication decision.

The original author freeze is FROZEN_MANIFEST.json SHA-256 `42cde2c3c2fe38df4625b84ec24548c4b3d3baaa6baf9e435f547d4237cfd203`. The additive FROZEN_MANIFEST_v2.json SHA-256 `9d3a6ea7af3004ac7c454eb8b46f1b1dfd04a9e33ae282188c7af365c608c18e` and METADATA_QUALIFICATION.md SHA-256 `93af926d190304ff45487f978e2fe1597974612bc387478312d88342d7f1b098` are also verified and included in this verdict. They preserve the original bytes and explicitly label all progress estimates subjective and uncalibrated, rather than correctness probabilities.

## Independence and source coverage

The reviewer did not contribute to the proof. I independently read the complete original contribution, visually checked the displayed formula and conjecture, and checked the companion Lambert map and modular reindexing. Source details and access limits are in SOURCE_NOTES.md. The exact target is Euclidean chord distance on the unit sphere, with no height shift and the finite rational ratio p/q. The one-based endpoint alternative is congruent. F_1=F_2=1 gives a singleton and is correctly excluded rather than assigned a fictitious pairwise distance.

The author's frozen mathematics was not changed during review. All fourteen original manifest-bound artifacts and both full source PDFs match their hashes and byte counts. The421,647 exact author controls and separately labeled2,061,234 binary64 diagnostics both replay byte-identically. A separately authored program passes242,425 exact assertions, including114,492 direct pair-distance certificates through size377. The latter use rational cosine enclosures, not the author's proof-derived pair lower bound. All these finite checks supplement the uniform analytic proof audited next.

## 1. Geometric inequality and signs

I independently expanded the scalar product of the two spherical points. With latitude fractions a<b, d=b-a and U=2(a+b-2ab), the squared distance is exactly2[U-c sqrt(U^2-4d^2)]. The discriminant equals16a(1-a)b(1-b), and U-2d=4a(1-b)>=0. Thus the square root and all sign choices used in the proof are legitimate, including either polar endpoint.

For c<=0, dropping the nonnegative second term givesD²>=2U>=4d. For0<c<1, write V=sqrt(U²-4d²). Both U-cV and2d sqrt(1-c²) are nonnegative. The exact difference of their squares is(V-cU)². Taking square roots therefore preserves the required inequality. This is not a local metric approximation; it remains valid close to a pole. The independent vertical boundD²>=4d² also has the correct factor and uses the ordinary unwrapped height difference.

## 2. Cassini's integer obstruction

For q=F_n and p=F_(n-1), the sign in p²+pq-q²=(-1)^n is correct, including the initial nontrivial pair(1,2). Consecutive Fibonacci coprimality is immediate from the Euclidean recurrence. The auxiliary integer l²+lm-m² cannot vanish for m>0 because the corresponding rational ratio would solve an irreducible quadratic of discriminant5.

I expanded the substitution s=mp-lq independently. It gives exactlyq²B=(-1)^n m²-(2p+q)ms+s² for either sign of s. Taking absolute values yieldsq²<=m²+(2p+q)m|s|+s². In the alleged dangerous regime m²<q, r=|s|<q/4 and mr<=q/4, its right side is strictly belowq+13q²/16. For every q>=8, q+13q²/16<q²; the margin already holds atq=8. The strict inequalities do not assume the residue has a preferred sign or that l is positive. Hence the lemma's mr>q/4 conclusion is sound.

This is a uniform Diophantine argument. No numerical continued-fraction asymptotic or unproved lower approximation constant is used.

## 3. Every pair and every finite size

For a genuine pair0<=i<j<q, m=j-i lies between1 andq-1. If m²>=q the vertical difference alone proves the target bound. Otherwise the nearest angular residue has0<r<=q/2 by coprimality. Reducing longitude modulo2pi is legitimate, while wrapping the latitude gap would not be; the proof does only the former.

On this reduced interval, positive cosine occurs exactly when0<r<q/4. In that case the angle lies strictly between0 andpi/2, where sine concavity gives sin(theta)>=2theta/pi=4r/q. Combining it with the geometric bound and the proved residue inequality givesD²>4/q. If cosine is nonpositive, the other geometric bound givesD²>=4m/q>=4/q. The equality boundaryr=q/4 belongs to the nonpositive-cosine case, so it is not omitted. These cases exhaust all pairs forq>=8.

The remaining Fibonacci sizes are exactly2,3,5. Their listed gap splits and cosine signs are correct. In the only positive-cosine small case(q,m,r)=(5,2,1), the same elementary sine chord bound gives32/25>4/5. The north-pole calculation gives exact attainment4/q in squared distance, so the lower bound is a minimum, not merely an infimum estimate. The zero-based construction includes the north pole and excludes the south pole; the source's alternative endpoint indexing is related by(x,y,z)->(x,-y,-z) andk->q-k, giving the same minimum at the other pole. No pair in either convention is left uncovered.

## 4. Companion source and scope limits

The companion planar lattice swaps the two Lambert coordinates. Reindexing by the invertible residuep gives longitude p^(-1)k/q, and Cassini implies p^(-1)=(-1)^n p modq. This is the OWR point set or its longitude reflection. The proof's source comparison is therefore exact and does not infer the spherical result from the companion planar shortest-vector result.

The theorem does not cover midpoint-height spirals or replacement of p/q by an irrational golden angle; those are different finite configurations. Nor does it prove optimal packing among arbitrary point sets or any discrepancy rate. The source wording is finite and universal over the nontrivial Fibonacci sequence, which the written proof completely covers.

## 5. Separate controls and their limitations

The independent checker first bounds pi by rational alternating-series intervals in Machin's identity and checks the exact tangent identity. Its branch is justified by0<4arctan(1/5)-arctan(1/239)<4/5<pi/2. For each finite gap it forms a rational upper bound for cos(theta) using monotonicity on[0,pi] and an even Taylor truncation. If H=q(i+j-1)-2ij and P=i(q-i)j(q-j), the desired direct scalar-product inequality is H>=2sqrt(P)cos(theta). H is nonnegative by the exact identity H=q(j-i-1)+2i(q-j). Nonpositive cosine upper bounds are immediate; positive ones are certified by exact squared-integer comparison. This is a direct chord-distance test independent of the uniform lemma's pair bound. It includes every pair for the tested sizes and exact pole attainment.

Separate signed-residue and rational-latitude checks challenge the algebra and polar branches. The author diagnostics remain explicitly binary64 and uncertified; no step in this verdict relies on their apparent numerical minima. The all-n conclusion rests on the uniform proof in Sections1–4 above.

The only review discussion concerned how repository-required subjective progress metadata is labeled, not a mathematical assumption or proof change. Preserve the agreed additive metadata clarification and the historical freeze. No mathematical correction is required.
