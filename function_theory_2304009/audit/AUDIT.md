# Independent adversarial audit: Function Theory 4.9

Date: 2026-10-04 UTC. Problem: **2304009 / AMR-022-4009**, queue rank 574.

## Verdict

**Accept the known negative resolution of the complete imported question. Recommended disposition: `already_solved`, `1/5`.** No mathematical gap or mandatory correction was found in the frozen reconstruction. This is a verification of established mathematics, with historical credit to Pommerenke (1961), not a new-discovery claim.

The author package proves that for every `0 < d < 4` and every positive integer `N`, some monic polynomial has at least `N` distinct connected components of its **closed** unit sublevel set with diameter **strictly greater than** `d`. In particular, `d=2`, `c=1` contradicts the exact bound `1+c^2` for arbitrarily large `N`.

This audit accepts the argument conditional on the explicitly stated classical Hilbert lemniscate theorem and standard logarithmic-capacity/Green-function facts. These inputs are appropriate standard theorems; none conceals the target component-counting question. This is an independent AI-assisted audit, not human peer review or formal proof verification.

## 1. Frozen artifact and source identity

The input manifest SHA-256 is

`ca309e19c702eeb882e8c7900b9c7084b48aba37994d77b2ad15aaaaf3a16377`.

It matches the requested freeze and the external author receipt. Every listed byte count and hash was independently recomputed, and the public inventory contains exactly the ten frozen files. The frozen public directory was not modified. Both supplied verification programs pass.

The supplied complete selected catalogue record identifies numeric ID 2304009 with Hayman–Lingham Problem 4.9. Its statement asks only for a degree-independent bound at each positive parameter. It does not include the asymptotic questions in the subsequent source update. Independently, selecting ID 2304009 from another already-cached full dataset snapshot produces exactly the same complete record. That snapshot has SHA-256 `37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`, different from the older immutable revision used by the author; this is recorded as a crosscheck, not a claim to have rehashed the author's unavailable full older corpus.

The complete supplied prior report merely declares the question open and reports finding no result. That assessment is directly contradicted by the primary source's own update. It contains no substantive previous proof to repair or continue.

### Primary-source inspection

- [Hayman–Lingham, 2018 v2](https://arxiv.org/abs/1809.07200v2), printed pp.74–75: the definition is the closed set `|f| <= 1`; the preceding polynomial convention is monic; the problem really prints `1+c^2`; Update 4.9 explicitly records a disproof and separately raises degree-asymptotic counting questions. Both pages were visually inspected, along with the reference to Pommerenke [644].
- [Erdős, 1961](https://real.mtak.hu/201135/1/cut_MATKUTINT_6_1_-_2_1961_pp221_-_254.pdf), printed pp.246–247, §IV.1: the original monic convention, closed sublevel inequality, and diameter question were checked in the page images. A fresh rendering of p.246 confirms that OCR's apparent strict sublevel inequality is misleading: the scan prints `<=`.
- [Erdős, 1976](https://users.renyi.hu/~p_erdos/1976-12.pdf), printed p.349, §3: the original proposer credits Pommerenke for arbitrarily many components of diameter near four and then distinguishes the subsequent asymptotic questions. The page image and reference list were checked.
- [Huang, 2025 v2](https://arxiv.org/abs/2509.11597v2), Theorem 1.1 and pp.2–4: the complete later proof was read. The visually inspected v2 priority note expressly identifies the earlier Pommerenke resolution and the later work as a rediscovery. The official arXiv version metadata was independently checked online.
- [Bloom–Levenberg–Lyubarskii, 2008](https://aif.centre-mersenne.org/articles/10.5802/aif.2411/), introduction, equation (1.1): the exact one-variable Hilbert approximation statement was visually checked, and its publisher metadata and author-preprint version were crosschecked. The result used is a one-variable theorem, irrespective of the two-variable subject of the paper.

All six retrieved source PDFs match their stated hashes and byte counts. The original [Pommerenke paper](https://doi.org/10.1307/mmj/1028998561) was not directly inspected: the supplied attempted-download files are block pages. Accordingly this audit does not certify the content of its original proof. The historical attribution rests on the inspected primary retrospective and the later explicit acknowledgments. The mathematical reconstruction is verified from its own argument and the retrieved standard input.

## 2. Independent check of the universal proof

### Capacity-one ellipse

For `0<d<4`, let `A=1+d/4`, `B=1-d/4`, `L=1+3d/4`, and `a=L/2`. Then

`L-d = 2A-L = B > 0`.

The exterior map `F(w)=w+(d/4)/w` is injective on `|w|>1`: two distinct preimages would have product `d/4`, incompatible with both moduli exceeding one. Its derivative has no zero there, its boundary is the stated ellipse, and its behavior at infinity identifies the exterior component and gives capacity one. There is no missing factor of two: the ellipse has semiaxes `A,B`, and `(A+B)/2=1`.

### Separated compact segments and the Hilbert hypothesis

Independently simplifying the margin gives

`m = 1-(a/A)^2 = (4-d)(5d+12)/(4(4+d)^2)`,

so `0<m<1`. With `h=Bm/4`, all `N` closed horizontal length-`L` segments are nondegenerate and mutually disjoint. The stated paths to the half-plane `x>a` prove that their union has connected complement. This argument applies to the **union**, which is the hypothesis needed by Hilbert's theorem, rather than merely to the individual segments.

For `N>=1`, the displayed epsilon actually simplifies to `h/(3(N+1))`; the alternate term `h/4` is always larger. The gap between consecutive closed epsilon-neighborhoods is

`2h/(N+1)-2epsilon = 4epsilon > 0`.

For all points in those neighborhoods, the proof's upper bound on the ellipse equation is valid. Its last universal estimate is

`1-m+m/8+26m^2/256 <= 1-(99/128)m < 1`.

Thus the neighborhoods remain inside the open ellipse and have positive mutual separation, even for very thin ellipses or very large finite `N`. No uniform positive gap as `d` tends to four or `N` tends to infinity is asserted or required.

### Approximation and actual connected components

The compact union `K` is nonempty and has connected complement, so the cited Hilbert theorem applies exactly as written. Its polynomial `r` cannot be constant because its selected sublevel set must lie in the bounded `K_epsilon`. The normalization factor `M=||r||_K` cannot vanish, since `K` contains a nondegenerate segment. Therefore `q=r/M` is legitimate and satisfies

`K subset E(q) subset K_epsilon subset Omega`.

Each segment lies in a connected component of `E(q)`. No component can contain two different segments: a connected subset of the union of finitely many positively separated closed neighborhoods must lie in one neighborhood. Consequently there are at least `N` distinct components, and each has diameter at least `L>d`. The argument correctly avoids inferring a component count just from the number of zeros or segments.

### Capacity identity and monic normalization

If the leading term of `q` is `alpha z^n`, then `cap(E(q))=|alpha|^(-1/n)`. The stated proof using `(1/n)log|q|` is valid: this function is positive harmonic outside the lemniscate, continuous with zero boundary limit, and a bounded complementary component would contradict the maximum principle. Its asymptotic constant is `(1/n)log|alpha|`, which yields the negative exponent in capacity.

Inclusion in the capacity-one ellipse gives `|alpha|>=1`. For **any complex** `w` with `w^n=alpha`, `p(z)=q(z/w)` is monic and `E(p)=w E(q)`. This is a similarity with factor `|w|>=1`; it preserves the complete component decomposition and cannot shorten the selected components. There is no assumption that `alpha` or `w` is positive real. Direct division by the leading coefficient, which would alter the relevant polynomial level, is correctly avoided.

### Target quantifiers

Fix `c=1`. If a finite uniform `A(1)` existed, choose a positive integer `N>A(1)` and use `d=2`. The constructed monic polynomial violates the bound with strict diameter `>2`. Allowing its degree to depend on `N` is exactly what is needed against a bound uniform in degree. The target is not being replaced by a restricted or easier bundled subquestion.

## 3. Reproducibility and adversarial controls

The author's controls replay without change: **287 exact geometry parameter pairs, 20 normalization cases, and six negative controls**. Their limited evidential role is clearly disclosed.

The independent verifier imports none of the author's code. It adds:

- **903** exact rational geometric cases, including `d=10^-30`, `d=4-10^-30`, and component count `N=10^12`;
- **48** full polynomials with exact Gaussian-rational coefficients and nonreal normalization factors, producing **288** exact evaluation identities `p(wz)=q(z)`;
- exact distance-scaling checks and six controls for wrong rescaling, wrong capacity exponent, changing the polynomial level, touching neighborhoods, the degenerate endpoint, and root/component confusion;
- a separate optional replay of all six private PDF hashes.

These are finite algebraic controls, not a universal numerical proof. The universal geometric inequalities, topology, capacity reasoning, and quantifier deduction are checked in the preceding section. No Hilbert approximant, coefficients, effective degree bound, or asymptotic estimate is computed.

Run from the attempt directory:

`python3 public/verify.py`

`python3 public/verify_manifest.py`

`python3 audit/verify_independent.py`

Private-source byte validation is optional: `python3 audit/verify_independent.py --check-private-sources`. That optional mode requires the six separately obtained PDFs; ordinary mathematical controls do not. No source PDF, source extract, or source image is included in the publishable audit inventory.

## 4. Corrections and limits

There are **no mandatory corrections to the frozen author package**. Two source-level issues already handled correctly should remain explicit: Huang's printed reciprocal-log energy kernel is erroneous, and its informal open-domain notation is replaced by compact sets in the reconstruction. Neither issue propagates into the author proof.

The frozen README and status file appropriately say that audit was pending **at author freeze**. This separate audit supersedes that pending state for review purposes; editing those historical frozen files is unnecessary.

Do not promote the result into a claim about every sufficiently large prescribed degree, effective coefficient construction, optimal degree-versus-component growth, or the `o(n)` / `o(n^epsilon)` follow-ons. The source reports more about prescribed degrees, but the present proof claims only existence at some degree. The classification `already_solved`, rather than a new locally discovered solution, is essential.

The author-recorded repository search snapshots show no existing attempt or relevant duplicate at the time checked. This auditor did not repeat live repository searches or change remote state. A publication-stage collision check and exact queue diff remain the parent's responsibility. Only the requested Status and Turns change is approved by this audit; no other queue cell is needed for the mathematical conclusion.
