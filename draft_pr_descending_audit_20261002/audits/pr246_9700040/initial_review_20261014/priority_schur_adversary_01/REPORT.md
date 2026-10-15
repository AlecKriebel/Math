# Independent Schur / Plancherel priority audit

PR246; 9700040 / AMR-096-0040. Candidate head supplied for this audit: `0b4db59eb5515f2d90d8b8df33b6b729b78b48f1`. This report assesses earlier mathematical coverage, not queue classification. No queue, Git index, branch, ref, provider record, or external communication was changed. All authored work is confined to this shard.

## Supported conclusion

**The candidate's full positive joint-law sum is exactly an earlier ascending Poissonized Plancherel / Schur path probability.** This is a complete parameter identification, not an analogy with a general framework. Borodin–Olshanski (2004) identify the requisite quadrant-Poisson shape path and give its dynamics and extended Bessel correlations. Nica's explicitly versioned 2015 manuscript prints the same multi-time positive weight; summing its first-row barrier events gives the candidate sum. There is no new joint distribution hidden in that sum.

**The stationary identification also has a short, complete classical route:** the 1993 Aldous–Diaconis stationary representation `(Gamma(B(i)))` becomes exactly the inverse first-row path under finite patience sorting and RSK. A separate direct Poisson-coordinate proof verifies that identification without trusting typographical defects in the unfinished notes. No central mathematical difficulty remains to be transferred to another unsupported assertion.

I did **not** locate a primary publication that explicitly presents this formula as an answer to the precise February 2018 Aldous problem. Thus “earlier explicit solution of that named problem located” would overstate the search. The supported finding is **automatic complete classical coverage of the candidate law**, with a potentially useful new exposition and rational evaluation wrapper. The live problem listing does not establish novelty or disprove this coverage. The candidate itself appropriately disclaims novelty.

## 1. Exact Schur-process specialization

Write `rho_a` for the exponential specialization with generating function `H(rho_a;z)=exp(a z)`. Then

`D_a(lambda/mu)=s_{lambda/mu}(rho_a)`.

In Okounkov–Reshetikhin, [math/0107056v3](https://arxiv.org/pdf/math/0107056v3), §§2.2.4–2.2.8, use the following finite list of symbols:

- `phi[j-1/2](z)=exp(Delta_j z)`, for `j=1,...,m`;
- `phi[m+1/2](z)=exp(z^{-1})`;
- every other symbol is `1`.

Their transition weight (9) is `s_{lambda^j/lambda^{j-1}}(rho_{Delta_j})` on each ascending edge and `s_{lambda^m}(rho_1)` on the terminal edge to the empty partition. Definition 2 gives exactly the candidate's unconstrained chain weight. Their partition function in §2.2.8 gives

`Z=exp(sum_j Delta_j)=exp(x_m)`.

All symbols are entire in the required annulus; there is a finite number; positivity follows from the exponential specialization. Thus no limiting admissibility argument is needed. Restriction to selected query positions is covered by §2.2.10, and §2.2.11 explains the continuous parameter. This matches the **whole path**, not merely the Schur measure at one position.

The 2018 sampling paper's §6, equations (6.2), (6.4), and (6.6), gives the same specialization using `gamma` parameters. Set `N=m`, `rho^+_{j-1}=rho_{Delta_j}`, `rho^-_j=rho_0` for `j<m`, and `rho^-_m=rho_1`. The zero negative specializations force each intermediate `mu(j)=lambda(j)`. All `alpha,beta` parameters vanish. Its explicit exponential identity already appears in the authenticated [2015 v2](https://arxiv.org/pdf/1407.3764v2), printed pp23–24. The published pp413–416 provide the same facts. This is supporting confirmation, not the earliest necessary source.

## 2. A stronger earlier theorem: the actual Poisson path

Borodin–Olshanski, [math-ph/0402064v2](https://arxiv.org/pdf/math-ph/0402064v2), 29 September 2004, §2 Definition 2.2 and Theorem 2.3, take a unit PPP in the quadrant and the RSK shape `lambda_Pi(u,v)` of its rectangle. With the horizontal admissible curve

`C: (u,v)=(x,1), x>0`,

their Remark 1.5 identifies the ascending process, and Theorem 2.3 identifies its entire law with the Poisson construction. The rates in §1, (1.9), are rate-one births of boxes with the Plancherel up transition

`p_up(lambda,nu)=f^nu/[(n+1)f^lambda]`, `nu` covering `lambda`, `|lambda|=n`.

Here is the explicit finite-duration consequence, independently reconstructed. If `mu subset nu`, `|mu|=n`, `|nu|=n+d`, then

`P_Delta(mu,nu)=exp(-Delta) Delta^d/d! * f^{nu/mu} f^nu n!/[f^mu (n+d)!]`.

There are `f^{nu/mu}` one-box paths and the up probabilities telescope. Multiplying these transitions from the empty diagram leaves

`exp(-x_m) [f^{lambda^m}/|lambda^m|!] product_j [Delta_j^{d_j} f^{lambda^j/lambda^{j-1}}/d_j!]`,

which is precisely the candidate weight. This theorem plus the explicit transition calculation covers every terminal size and every finite collection of cut positions.

For arbitrary positive integer indices, `X_r>x` is equivalent to `lambda_1(x,1)<=r-1`. Therefore the candidate's constraints are merely a first-row barrier event of this already identified process. No monotonicity assumption on the sorted-threshold indices is used; any redundant constraints can be retained. Repeated thresholds merge by the smallest index, consistently with the candidate.

## 3. Nica prints the same multi-time weight before the source posting

Mihai Nica, [arXiv:1404.4015v3](https://arxiv.org/pdf/1404.4015v3), 29 April 2015, Theorem 3.2 and Remark 3.3 (printed p6), gives the full positive skew-tableau / exponential-Schur multi-time distribution of the Poissonized Robinson–Schensted process. Its proof is in §3.4 (printed pp8–12). The final publication is *Stochastic Processes and their Applications* 127(2), February 2017, 449–474; the canonical [version history](https://arxiv.org/abs/1404.4015v3) records those dates.

For an exact parameter mapping, let `theta=sqrt(x_m)` and map the candidate rectangle by

`(u,v) -> (u/theta, theta v)`.

This preserves area and carries `[0,x_m] x [0,1]` to `[0,theta]^2`. The queried rectangles become `[0,x_j/theta] x [0,theta]`. They are the positive branch of Nica's diagram process, with parameter `s=theta-x/theta`, taken in reverse order. Set the central shape `nu=lambda^m` and, for `j=1,...,m-1`, set `s_j=theta-x_{m-j}/theta`, `mu^(j)=lambda^{m-j}`. Discard the other branch by taking its marginal (equivalently, use its empty list of queried times).

The resulting chain weight is

`exp(-theta^2) s_{lambda^m}(rho_theta) product_j s_{lambda^j/lambda^{j-1}}(rho_{Delta_j/theta})`.

Exponential homogeneity cancels the powers of `theta`, since the skew sizes sum to the terminal size. This is **exactly** the candidate's weight, with no asymptotic limit. Summing over the prescribed first-row bounds gives exactly formula (3).

Two source cautions were checked rather than silently repaired:

1. The displayed factorial form of Theorem 3.2 has `|mu^(j)/lambda^(j+1)|` in a right-branch exponent. This is a typographical defect, sometimes using an undefined index. The denominator, Remark 3.3, and the uniform-tableau counting proof use `mu^(j)/mu^(j+1)`, which is the intended formula. Both the v3 and current v4 PDFs show the defect.
2. Current v4 PDF displays a 2021 title date, and current v3 PDF displays a 2022 title date. I did not silently use either as a 2015 document date. I retrieved the actual [v3 source archive](https://arxiv.org/src/1404.4015v3): its TeX contains the theorem and Schur expression at lines 573–600, its member timestamp is 29 April 2015, and the canonical version record agrees. The article source has `maketitle` and no explicit date, consistent with a compilation-dependent title date. Mathematical chronology is pinned to the versioned source and version history, not that displayed title date. See `NICA_SOURCE_ARCHIVE_PIN.json`.

## 4. Stationary law: the exact old representation and remaining bridge

Aldous–Diaconis's [unfinished 1993 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf), §4.1 printed pp36–37, already specify the drift-jump rules and equation (42) gives its invariant positions as `Gamma(B(i))`, where `Gamma` is an independent rate-one Poisson arrival sequence and `B(i)` are the limiting pile-top ranks. The published [1999 survey](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf), printed p418, identifies the top row of the insertion tableau with the pile tops; its Proposition 4 provides the one-time RSK count.

The following explicit deduction removes any unspecified joint `B` law. Give labels `1,2,...` independent uniform priorities in `[0,1]`. For each `n`, deal labels `1,...,n` in priority order. Compatibility of patience sorting under deleting all labels greater than `n` implies

`#{i:B(i)<=n}=LIS(priority-ordered permutation of [n])`.

The inverse permutation has the relative order of the first `n` priorities in label order. RSK preserves shape under permutation inversion. Hence this count is the first row of the Plancherel growth shape obtained by inserting the first `n` priorities. Independently placing the labels at `Gamma(n)` turns the shape path into the unit-PPP rectangle path `lambda_Pi(x,1)` from §2. Consequently

`#{i:Gamma(B(i))<=x}=lambda_Pi(x,1)_1`

as a joint path identity in law. Thus the *existing stationary representation* and the *existing full shape-path theorem* combine to supply exactly the all-index stationary law.

The published [1995 paper](https://www.stat.berkeley.edu/~aldous/Papers/me71.pdf), §2.2, manuscript pp5–6, explicitly identifies the empty Hammersley particle count with the increasing-path count and gives its nearest-right graphical Rule 2. Its Lemma 4, manuscript p7, gives the simultaneous area-preserving scaling law. These published facts supply both the inverse-LIS representation and scaling premises. There is also a direct check that avoids relying on unfinished-note formulas. Define inverse LIS levels `Z_i(v)` and `Y_i(s)=exp(s)Z_i(exp(s))`. The change `(u,v)->(x=uv,s=log v)` has unit Jacobian; a fixed particle drifts with derivative `Y_i`, and events perform the nearest-right jump. Area-preserving quadrant scaling gives stationarity. The first `k` coordinates are autonomous. This verification is elementary and complete. The 1993 printed transformation has a sign issue (`x exp(t)` where the direct inverse-level computation requires `x exp(-t)`), and its initial-time wording is also rough; it should not be cited as a literally correct formula. These source defects do not make the correctly mapped stationary law a new joint-law theorem. They do mean that a rigorous exposition should include the short verification rather than outsource it to a defective display.

## 5. Extended Bessel / finite determinant description

Theorem 3.3 of the 2004 paper, equation (3.4), covers the horizontal path in interior time

`t_j=(log x_j)/2`, `theta(t_j)=x_j`.

Its lattice configuration is `{lambda_i-i+1/2}`. The candidate event forbids all particles at query `j` in `{r_j-1/2,r_j+1/2,...}`. For a finite upper cutoff, inclusion–exclusion and the theorem give `det(I-K)` on the forbidden sites. Letting the cutoff increase gives the complete barrier probability. No unexplained trace-class convention is needed: define the determinant as this limit. An omitted site with integer coordinate `h=lambda_i-i>H` forces `N(x_m)>=H+2`, so a Poisson upper tail bounds the exact probability cutoff error.

This is an additional earlier explicit description of the **simultaneous** inverse law, not merely a Bessel formula for a marginal. It is not the ordinary spatially stationary Hammersley Poisson configuration, nor an edge scaling limit.

## 6. The 2013 direct dynamics lead is not an established cover theorem

The independently supplied lead [arXiv:1303.2795v1](https://arxiv.org/pdf/1303.2795v1), §6 printed pp8–9, describes the one-row projection and its Plancherel degeneration to linear velocity `v(y)=y` and identical unit-rate backward PPP clocks. Its finite prefix generator agrees exactly with the source: independent particle PPPs restricted to the disjoint current gaps give the same jump intensities as one common field. This is direct earlier recognition of the mechanism.

However, the introduction labels the note informal and unproved; Claim 4.2 is justified only infinitesimally, Conjecture 3.3 concerns nonexplosion, and Claim 5.4 is the stationary Gibbs assertion. The [Thoma-cone companion](https://arxiv.org/pdf/1303.2794v2), §1.6, explicitly calls the covering construction conjectural. Its §10 identifies the degenerate boundary point `(alpha=0,beta=0,delta=1)`, and the [Young bouquet paper](https://arxiv.org/pdf/1110.4458v1), Definition 3.4.3 and §5.3, identifies the corresponding Poissonized Plancherel Gibbs path. None of those statements alone proves the unproved local-cover invariance. **This route is blocked as a stand-alone rigorous prior-solution citation.** The 1993 / 2004 / Nica route above does not need it.

## 7. Independent controls and exact residual uncertainty

`check_schur_mapping.py` imports no candidate code. It exhausts all 5,914 permutations of sizes 0 through 7, checks 2,459 distinct chain-count equalities and 7,377 skew determinant equalities, and checks exactly that the candidate, the rescaled Nica expression, and the Poissonized Plancherel Markov weights coincide. It includes nonmonotone row bounds `(2,1,3)`. Every control passed.

`check_extended_bessel.py` independently checks the interior-time orientation and half-integer barrier against the known `(r_1,r_2)=(1,2)` law at `(x_1,x_2)=(1/2,3/2)`. Cutoff matrices of orders 17, 25, and 37 converge to `0.5086442335822535196...`; the last discrepancy is about `9.2e-38`. These are ordinary high-precision numerical controls, not validated interval calculations or historical evidence. The analytic mapping is the substantive argument.

I did not find the exact rational enclosure in candidate formula (5) in the inspected earlier sources. It is a useful elementary consequence of the same normalized positive sum and a Poisson-tail bound. The fixed-dimension transpose also follows immediately from transposition of standard skew tableaux. An original arrangement of these computational details is possible; that does not establish a novel stationary law or a new discovery. No claim about the proposer's acceptance of this level of explicitness is supported, and no outreach was attempted or prepared.

Assigned bounded audit completion estimate: **100%**. Historical exhaustiveness is not claimed. The exact remaining uncertainty is attribution of an earlier *expressly stated answer to the named drift-jump problem*, and whether the source's qualitative explicitness aim regards this classical consequence as satisfactory. Those are distinct from the verified complete mathematical coverage described here.
