# Independent adversarial audit: 5300076 / AMR-052-0076

Audit date: 2026-10-04 UTC. Frozen author target: rank 649. Disposition: **PASS AS A PARTIAL RESULT; retain unsolved, 5/5**. This is an independent computational and mathematical audit, not human peer review or a novelty certification.

## Decision and binding

The original theorem proofs survive the audit. Global lift convergence for actual critical period two is proved for every real exponent greater than one. The explicit two-cycle disproves universal convergence of the conjugated maps in the stated continuous strictly unimodal class, while the lift sequence is constant. It does not disprove lift convergence. No full resolution of the imported question is established or independently verified.

The audit binds the exact twelve-file frozen input, including its manifest, through `AUDITED_INPUTS.json`. Its manifest SHA-256 is `bb67c99bd596788d00ce4aea34bda21048d85ab6e2742ba4e3e17cc4a8aff4fc`; `RESULT.md` is `5ff46f68f9141501ec2adcde3156dbc7f1d924d5cb1a1f2fcd09e1313ccb1c92`. The independently inspected 19,996-byte author ZIP is `2592012077430536891db273c9030b7790a98fe8c39e03db4afd4a9486b4c3a8`. Every ZIP member's bytes match the corresponding frozen input, and its inventory contains no extra files.

All 48,709 author assertions replayed, with byte-identical JSON output. The independent suite adds 4,812 assertions without importing the author's functions. The authored manifest verifier passes. Original author files were not edited. No remote repository or helper was used or modified.

## 1. Exact sequence distinction and source hypotheses

I independently read Bielefeld's §3, including the algorithm on printed pp. 8–9, and visually inspected printed p. 9. The starting setting is piecewise monotone interval maps with a prescribed endpoint map. The nearby polynomial theorem is conditional on actual postcritical finiteness and absence of a Thurston obstruction; it concludes convergence of the polynomial lifts. Convergence of the conjugated maps is discussed separately as an experimental phenomenon. Question 2 changes the lifting family and uses periodic/preperiodic kneading without specifying an output sequence or a topology. [Primary source](https://arxiv.org/pdf/math/9201271).

Thus the source does not clarify the final question enough to certify the full-map counterexample as a complete negative solution. Conversely it does not impose smooth endpoint hypotheses or prohibit a fixed critical point. The author's continuous strictly unimodal maps are within the natural two-lap interpretation; their counterexample cannot be rejected merely because it lacks endpoint differentiability. Flat intervals would destroy the claimed homeomorphic lift and need separate conventions. The author's explicit restriction avoids this issue rather than proving a result for flat maps.

Tiozzo's appendix independently corroborates the output distinction: its algebra identifies the two tower sequences, and Theorem 5.4 concludes convergence of the polynomial/lift sequence under its stated hypotheses. It does not identify the tower maps as the same output. [Tiozzo, appendix](https://arxiv.org/pdf/2112.02398v1).

The conservative residual question is therefore the correct one for this packet. Source context supports it, but it is an explicit conservative interpretation, not a newly discovered unambiguous definition in Question 2.

## 2. Lift identities, normalization, and marked configurations

Fix alpha > 1 and beta = 1/alpha. With P_k(x) = k(1-|2x-1|^alpha), the two inverse branches on [0,k] are (1 plus or minus (1-y/k)^beta)/2. Composing the left branch with f on its increasing lap and the right branch on its decreasing lap produces one increasing endpoint-preserving homeomorphism h. The branches meet at 1/2. The relations P_k h = f and f_next = h P_k follow directly, so f_next = h f h^{-1}. The new turning point is 1/2 and the new maximum is h(k). No differentiability of the starting map is needed.

Uniform distance between two members of the lift family is exactly the distance between their heights, attained at x = 1/2. Thus scalar height convergence is equivalent to uniform lift convergence. This observation does not imply convergence of the conjugated maps.

For a genuinely finite critical orbit, labeling all marked points and their forward images gives the inverse-branch update in the original packet. Strict order follows on each lap from the lap orientation and the inverse-branch orientation. Points across the turning point remain on opposite sides of 1/2. Only the critical label has image equal to the maximal height, so no other label can collide with the normalized critical label in a single strict-interior step. This proves finite-step order preservation, not uniform separation from collisions over infinitely many steps.

After normalization, a finite critical orbit cannot have 0 < k < 1/2. Its next iterate lies strictly between 0 and k. Strict increase on the left lap then propagates strict positive descent forever, contradicting finiteness. This statement depends on normalization; the author correctly establishes that normalization from step one. Independent tests also start with turning points both below and above 1/2, so this dependence was not silently omitted.

The derivative of an inverse branch becomes unbounded as its image approaches k because beta-1 < 0. This invalidates a global Euclidean Lipschitz proof; it does not refute convergence in another metric. The compact-orbit/strict-distance-decrease criterion in the packet is valid: a positive limiting distance would yield a subsequential limit with unchanged distance after one continuous update, contradicting strict decrease.

## 3. All-exponent period-two proof, including the boundary

An exact critical two-cycle becomes 1/2 -> k -> 1/2 with 1/2 < k < 1 after the first conjugacy. The lower bound follows from strict increase on the left lap; equality gives a fixed critical point. The upper bound excludes k=1 because f(1)=0. Evaluating the right inverse branch gives

k_next = [1 + (1-1/(2k))^(1/alpha)]/2.

Set t=2k-1 and q=-log(t). The update becomes t_next=(t/(1+t))^(1/alpha) and q_next=H(q)=log(1+exp(q))/alpha. For every finite q >= 0,

0 < H'(q) = exp(q)/(alpha(1+exp(q))) < 1/alpha < 1.

The mean-value theorem gives the global Lipschitz constant 1/alpha, even though it is not attained by the derivative at a finite point. H maps the complete space [0,infinity) into itself. Banach's theorem therefore supplies a unique fixed q_* and the asserted geometric error bound for every finite starting q. Since H(0)>0, q_*>0. Consequently t_* lies strictly between 0 and 1. Rearrangement yields t_*^(alpha-1)(1+t_*)=1; its left side is strictly increasing from 0 to 2, proving uniqueness independently. Finally exp(-q) is 1-Lipschitz on this domain, giving the claimed height and uniform-lift error bound.

Two different boundary issues must remain distinct:

- q=0 corresponds to t=1 and k=1. Although not an exact two-cycle configuration, this finite endpoint is a harmless extension of the recurrence and moves immediately into its positive interior.
- t=0, k=1/2 corresponds to q=infinity, not to a point of the complete metric space above. In t coordinates it is another fixed point. It is the separate fixed-critical case. The positive period-two limit must not be asserted there.

There is no uniform convergence assertion over all starting heights approaching 1/2 or all alpha approaching 1. For each fixed alpha>1 and actual two-cycle starting map, however, q is finite and the proof is global. The author does not commit this boundary error. A clarification is recommended only to prevent later overstatement.

The fixed-critical and height-one endpoint-preperiodic controls also follow exactly from h(c)=1/2 and h(1)=1, respectively.

## 4. Universal full-map two-cycle proof

Write the centered map as F(u)=-g(|u|), where g is an increasing homeomorphism of [0,1]. At critical height 1/2 the centered lift is Q(u)=-|u|^alpha. Its increasing lifting homeomorphism is H(u)=sign(u)g(|u|)^(1/alpha). Therefore the next centered map is -g(|u|^alpha)^(1/alpha). This derives, rather than assumes, the fiber transformation U(g)(t)=g(t^alpha)^(1/alpha).

For omega=pi/log(alpha), choose epsilon>0 and A>epsilon*sqrt(1+omega^2), and set L_theta(s)=s(A+epsilon*sin(omega*log(s)+theta)). Its derivative is strictly positive by the sine/cosine amplitude bound. Its upper and lower positive linear bounds imply that g_theta(t)=exp(-L_theta(-log(t))) extends continuously to an increasing homeomorphism with endpoint values 0 and 1. These statements hold for every alpha>1, including exponents arbitrarily close to one; A is allowed to depend on alpha.

The exact identity L_theta(alpha*s)/alpha=L_(theta+pi)(s) uses only omega*log(alpha)=pi. Thus U sends g_theta to g_(theta+pi), and U squared is identity on this family. For theta=0 and s=sqrt(alpha), the sine is +1 in one phase and -1 in the other. The values differ by the strictly positive expression in the original report. Consequently the full-map sequence alternates and fails pointwise convergence at the specified test point. Its critical point is fixed, all its lifts are exactly P_(1/2), and its critical orbit is finite. There is no hidden change of critical height or exponent between steps.

The stationary example g(t)=t^gamma is likewise valid, but proves only failure of common-limit convergence when gamma differs from alpha. It must not substitute for the nontrivial cycle when claiming failure of convergence itself. Neither example by itself is a negative solution of lift convergence.

## 5. Remaining logical controls

The author's example f(x)=x(1-x) has critical value 1/4 and an infinite positive strictly descending critical orbit. Its symbolic critical-value itinerary is constant left. Periodic symbolic data therefore cannot be replaced by actual critical finiteness. This is a genuine obstruction to narrowing the residual target to a finite-dimensional configuration space.

The affine conjugacy to a-|z|^alpha is correct: b=(2k)^(1/(alpha-1)) gives b^(alpha-1)=2k, exactly the coefficient cancellation needed. Because b changes with k, a theorem about parameter order in that family does not identify the normalized iteration's limiting behavior.

The holomorphic-germ obstruction is correct: the first nonzero Taylor order must equal alpha on the positive side and must be even on the negative side. It blocks a direct polynomial substitution, not every possible complex-geometric method. The family R_epsilon(x)=-(1-epsilon)x correctly shows that finite-time continuity and uniform convergence of maps do not transfer infinite-time orbit convergence to a parameter limit.

All five recorded approaches have distinct mathematical content. The 15% estimate is subjective and not audited as a quantitative measurement.

## 6. Independent literature gate and the 2026 manuscript

I freshly retrieved the primary PDF, Tiozzo's v1 PDF, and Benedicks–Rodrigues v1 PDF. All three bytes and hashes reproduce the author's metadata. I also inspected the latter's abstract/history page, HTML, and PDF sections 2–4. The manifest records only metadata; no source text, PDF, screenshot, or downloaded corpus enters this audit package.

The manuscript's stated target is kneading/entropy monotonicity. Its inverse-root setup centers on a finite periodic critical orbit. Importantly, Propositions 3.3–3.4 assert pairwise nonexpansion and strict distance decrease globally on the proposed Teichmüller space. It is inaccurate to summarize all its contraction claims as merely local. The author's cautious wording can stand, but the distinction should be preserved. I did not verify the proposed geometric construction, its identification with the normalized real update, fixed-point existence and nondegeneration for every allowed initial map, or its extension to symbolic eventual periodicity. No theorem with all those required quantifiers was found. [Benedicks–Rodrigues v1 PDF](https://arxiv.org/pdf/2605.12238v1).

The arXiv history inspected lists v1 submitted May 12, 2026. The byte-pinned PDF carries an internal May 13 date, while the HTML returned during this audit displays August 24. These are recorded as distinct presentation observations, not inferred revisions. No peer-review acceptance or global current-open-status assertion is made. The earlier Levin–Shen–van Strien noninteger discussion and restricted large-exponent result remain related local/lifting-property evidence, not a substitute for the target theorem.

## 7. Test coverage and limitations

`independent_checks.py` uses exact rational algebra, 75-digit Decimal computations, and bounded floating-point diagnostics. It covers arbitrary initial critical locations; direct first-step conjugacy and second-step scalar reduction; marked actual period-three, period-four and preperiodic configurations; logarithmic extreme-coordinate behavior; the excluded t=0 boundary; exact formal phase involution; and logarithmic cycle separation without exponent underflow. It imports no author module.

The extreme q contraction diagnostics allow sixteen floating-point ULPs at the relevant output scale. Log-periodic diagnostics use relative tolerance 1e-10; the exact all-alpha phase and derivative arguments above are the proof. These finite checks do not prove universal convergence, establish source correctness, certify historical novelty, or exhaust all literature. ZIP/input/source byte checks are reproducibility evidence only.

## Required disposition

No blocking mathematical correction was found. Preserve the existing claims and their exclusions. The recommended disposition remains **unsolved, 5/5**, with the two advertised partial conclusions independently checked. `CORRECTIONS.md` lists optional scope clarifications for any revised packet; it does not alter or silently replace the frozen author input.
