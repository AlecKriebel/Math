# Independent adversarial review: 5100011 / k203,a

**Verdict: PASS — complete proof of the full source-corrected arbitrary-fixed-point assertion.** No mandatory mathematical revision. Recommended status: `claimed_solved`, 2/5 author turns, retaining all shared-input and published-theorem credit. This is an independent AI audit, not a human peer review or a novelty certificate.

## 1. Exact frozen object and reviewer independence

Reviewed PROOF.md SHA256 `3b8e009c730ce29c59f4240b1b8d52e90970f5061d58d4983512a8979e3ce820`, identified by MANIFEST.json SHA256 `48305c718e9a58084523203c06856abb261c036694232aa9a4bd3fa1c9801cd7`. All eleven author-file hashes and all four primary-PDF hashes match. The complete pinned statement/report were read; their joint hash `3ab49e065fad850da6eafd6a6506f7aaf9ca986bad939543149c4349d5ea6171` matches the source manifest. No frozen author artifact was modified.

I did not participate in either of the two author turns, the arbitrary-M radial reduction, or the shared k203,b central-pedal pole mechanism. Before reading this proof, I separately derived a dn-trace product mechanism for a different outer-pedal target, k303,b; that unfinished checkpoint was preserved before this audit. It is not used as evidence for the present proof. I previously authored the related k110 package supplying the already-reviewed, credited polarity consequence of Chavez-Caliz; that established input is explicitly identified in the submitted proof, not counted as a new contribution here. The new arbitrary-M meromorphic argument is independently checked below.

## 2. Exact source and scope

Both [arXiv2004.12497v11 Table3 p.6](https://arxiv.org/pdf/2004.12497v11) and the [published Table3 p.346](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) specify AA_M, N=0mod4 and all M. Their definitions give signed areas and the pedal of the original billiard side lines. This is not the pedal of the outer tangent polygon. For each chosen real M, M stays fixed while the initial orbit phase changes.

The actual source setting is a strictly nested nondegenerate confocal ellipse pair, a>b>0, with primitive period. Admissible star winding numbers are included. Negative or zero signed pedal area is allowed. The proof does not substitute unsigned filled-lobe area, hyperbolic/degenerate caustics, arbitrary even listed traversal count, or a moving pedal point.

Primary inputs were checked directly: Stachel's published Theorem4.3/(4.9), the contact-phase interpretation, the [NIST DLMF period/pole/quarter-shift tables](https://dlmf.nist.gov/22.4) and [addition identities](https://dlmf.nist.gov/22.8), and Chavez-Caliz's complete published area-product theorem/proof with its signed-area and complex-transversality definitions. Full primary PDFs were accessible, not just abstracts or search snippets. Relevant table pages were visually inspected. The printed Stachel dn-shift sign typo is not used; the correct DLMF signs are used throughout.

## 3. Arbitrary-M radial reduction

For each real side line the perpendicular foot has the form q_i+T_iM, with T_i the rank-one orthogonal projection onto its direction. Opposite sides give q_(i+m)=-q_i and T_(i+m)=T_i. Hence the linear terms in the ordered shoelace sum cancel in pairs.

The quadratic identity is valid without convexity or any choice of orientation for individual line directions. For arbitrary nonzero tangent vectors t,s, put U_t=t t^t/(t^t t). Independently clearing denominators verifies

    det(U_t M,U_s M)
      = |M|² det(t,s)(t·s)/(2|t|²|s|²)
        +[det(t,M)(t·M)/|t|²−det(s,M)(s·M)/|s|²]/2.

The second part telescopes around the polygon. This gives exactly the submitted |M|²/8 sum sin(2Delta_i) term, with the correct shoelace factor. Thus reflection or negation of M leaves the pedal area of the same centrally symmetric ordered polygon unchanged. This does not assume phase invariance; the proof correctly establishes that only later.

## 4. All meromorphic singularities

The complex extension uses n^t n, not a Hermitian norm. The identity n^t n=dn²(u)/beta² is exact, so q_M is meromorphic for each fixed real M.

At a common simple pole of sn,cn,dn, q_0 has a removable zero and the matrix n n^t/(n^t n) is regular. The leading coefficient of n^t n is nonzero because it equals dn²/beta². No hidden pole survives there.

At a zero r of dn, sn and cn are finite and the projection has order at most two. DLMF's formulas at K+iK' make sn and cn even in the local coordinate epsilon, and dn odd. Both q_0 and the projection matrix are therefore even Laurent functions. Period/reflection transformations extend this to every congruent zero, for every M. There are no other possible poles.

For a singular vertex q_M(r+epsilon), its two neighboring arguments are regular because the real step delta is strictly between0 and2K. Their difference is an odd holomorphic function of epsilon by evenness about r. Combining the two incident determinant terms therefore multiplies an at-most-double even pole by an odd function vanishing at least to first order. The resulting pole is at most simple.

Simultaneous singularities have not been overlooked. The indices differing by N/2 can be singular together, but they are never adjacent for primitive N>=4. Each incident edge then belongs to exactly one singular-vertex grouping. This includes the alternating pair at N=4. No product of two singular neighboring vertices remains to produce a higher-order pole.

## 5. Period quotient and complete cancellation

The projection identities under2K and2iK' are algebraically correct. The already-proved real radial lemma gives T_(−M)=T_(JM)=T_M on the real axis. Since all these are meromorphic and regular for real phase, the identity theorem extends those equalities to complex phase. Determinant covariance then gives the correct imaginary anti-period, not an ordinary imaginary period.

For N=4n, m=N/2 and h=2K/m, gcd(tau,m)=1. The real periods2K and delta=tau h generate h. The quotient by h and4iK' is a genuine compact torus, with two distinct possible simple poles at r and r+2iK'. Translation quotients are unramified, so the local pole orders do not change.

For F(u)=S(u+K), those two poles are genuine. Each reduced real translate occurs twice in the N-term sum, with the same residue because dn has real period2K. Their coefficients add rather than cancel. The other imaginary row has the opposite residue by anti-periodicity. Thus one scalar multiple of F removes the residue of T_M at the first pole and automatically at the second. There are no higher principal parts. The difference is a holomorphic function on the compact torus, hence constant; its anti-periodicity forces the constant to vanish.

This proves T_M=c(M)S(u+K), including c(M)=0. The coefficient is real by evaluating on the real axis, where S is strictly positive. Since tau is odd and N=4n, n delta=K tau is congruent toK modulo2K, so K is a period of the trace. Therefore the comparison is with the correct contact-area trace S(u), not a different phase. The universal area formula in Section3 has the correct factor and was independently reduced using Jacobi addition identities.

All asserted meromorphic cancellations are justified analytically. None is inferred only from numerical agreement.

## 6. Completion with the published area product

Chavez-Caliz's even-period AA' theorem applies: the submitted four complex intersections are finite, distinct and have nonzero gradient determinant for every strict noncircular confocal pair. No generic-limit assumption is needed. The polarity calculation maps the outer polygon to the contact polygon by diag(alpha²/a²,beta²/b²), in the same cyclic order. All real outer vertices are finite because an antipodal chord through the center cannot be tangent to the inner ellipse.

Thus AA_inner is a fixed multiple of the published AA' constant. The newly proved A_M=c_M A_inner completes AA_M for every fixed M. This is not a proof only for M=O, only for generic M, or only for a nonzero pedal area. Orientation reversal and repeated admissible traversals behave as stated. A circular boundary, if separately included, follows from rigid rotation plus the radial lemma; it is not inserted into the nondegenerate complex-modulus proof.

## 7. Reproducibility and limits

The author checker was read and replayed in an isolated copy. Its output is byte-identical to the frozen receipt:21,419 exact assertions and2,691 high-precision diagnostics PASS.

The separately authored independent_checks.py passes19,039 exact assertions: a symbolic non-unit-tangent radial identity, the Jacobi area numerator reduction, Laurent-order/residue algebra, period/residue multiplicity, disjoint incidence groups for simultaneous poles, and direct rational arbitrary-point four-period geometry.

It also passes1,539 non-interval numerical diagnostics at90 decimal digits across27 primitive families, including15 star families. Direct Euclidean pedal constructions are compared with the meromorphic formula for internal and far-external M, real phases, generic complex phases and points within about10^(-9) of simultaneous pole phases. Period signs, reflected local germs, the absence of an even double-pole part and phase-independent ratios/products agree. Maximum scaled discrepancy:2.4309762185084e−72.

The finite controls are diagnostics, not the universal proof. This review does not establish historical priority or an exhaustive literature result. Shared author inputs must retain their current attribution; their contributors are not independent reviewers. The complete exact claim is proved within the recorded two author turns, so no further author-search turns are needed before the separately authorized publication stage.

No mandatory correction is required. Preserve signed-area/primitive/elliptical-caustic restrictions and the arbitrary fixed-M quantifier in any public summary.
