# BGT model-mapping audit

The closest inspected prior source is Basdevant–Gouéré–Théret (2021 preprint, 2022 journal), arXiv:2106.12266, DOI 10.1214/22-AAP1795. Theorem 1 and Proposition 3, PDF pp. 3–4, imply the ordinary undirected Bernoulli bond FPP diagonal expansion

μ_q(1,1) = 2 − 2^(3/2) sqrt(q) + o(sqrt(q)).

Its Proposition 6 and Lemma 18 compare oriented and unrestricted FPP at the leading rare-mark order. The technical proofs are in Sections 2.5 and 3.3. Those are substantial prior methods controlling nonmonotone detours, and must be credited. This source is more relevant than a generic Hammersley citation.

## Independent exact per-path calculation

Use one rare-mark field X_e in {0,1} on the unoriented edges of a fixed square, and capacity c_e=1−X_e. For a simple path P from (0,0) to (N,N), let b count south/west steps, k_f count marked north/east traversals, and k_b count marked south/west traversals. The forward count is 2N+b. Thus:

- target asymmetric dual cost C_A(P)=2N+b−k_f; target deficit R_A(P)=k_f−b;
- ordinary symmetric FPP cost C_S(P)=2N+2b−k_f−k_b; symmetric deficit R_S(P)=k_f+k_b−2b.

Consequently R_A(P)−R_S(P)=b−k_b≥0. For a common confined path set, min C_A≤min C_S and max R_A≥max R_S. The coefficient in BGT agrees numerically with the target after dividing its diagonal deficit by 2, but that fact and the one-sided comparison do not give an upper bound on target deficit. The theorem's unrestricted lattice domain also differs from the finite target confinement; neither issue may be silently discarded.

The missing comparison would bound the *extra optimized asymmetric reward* by o(sqrt(q)N), in the appropriate successive limits. It is precisely a uniform detour estimate, not a change of notation. A proof adaptation changing the penalty from two to one, or an additional comparison theorem, must actually be supplied and checked before labeling the entire target a corollary. We have not authored such an adaptation in this priority-only audit.

## Why the tempting algebraic repairs fail

Writing the target cost as half the path length plus an endpoint potential does not make the remaining random cost nonnegative and symmetric: subtracting the potential (x+y)/2 from each directed traversal produces forward cost 1/2−X_e and backward cost 1/2. On marked forward edges it is negative, whereas BGT assumes nonnegative Bernoulli times shared by both directions. Thus the potential transform does not put the target in the theorem's hypotheses.

Replacing a marked edge by a marked starting site gives independent site marks of probability 1−(1−q)^2, which has the correct first-order intensity 2q. But it still leaves the target backward penalty one. BGT site FPP has penalty two relative to the endpoint displacement. Merely replacing q by 2q therefore does not fix the hypothesis mismatch.

The route “identify the target with standard Bernoulli FPP and apply Theorem 1” is blocked at these exact mismatches. The route may be reopened with a materially new deterministic reduction, an explicit published asymmetric-cost theorem, or a fully checked deduction. This audit has not found one as of the checkpoint. This is not evidence that no such deduction exists.

## Updated disposition

The direct theorem identification above remains invalid. A closer check of the published *larger bad-sequence sum* gives a complete different mapping: the target half penalty is compensated by the factor 2 on discarded-site counts in bond Lemma 19. See BGT_FULL_COROLLARY.md for the event inclusion, origin and boundary conventions, and full limit deduction. This is an old-input full corollary, although no literal published announcement of the named Aldous conjecture has been located. The earlier inability to conclude from the literal theorem statement must not be read as the final priority verdict.
