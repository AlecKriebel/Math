# Candidate-aware adversarial verification of the annular-jet theorem

## Verdict and scope

**No substantive mathematical gap found.** The full strong theorem survives this review:

There is a dense subset B of H(C) such that every f in B is hypercyclic for differentiation, and for every fixed nonconstant complex polynomial p,

\[
 |(pf)^{(n)}(0)|\longrightarrow\infty.
\]

The word “fixed” concerns the limit: its threshold can depend on p. The same f works for all p, with no uniform threshold over polynomial coefficients being asserted. Consequently every such pf fails to be hypercyclic. The exceptional set constructed here is meagre in H(C), which also resolves the apparent tension with the reported residual preservation class.

This was a **candidate-aware** adversarial test of an explicitly supplied hypothesis. It is not a blinded rediscovery, a novelty assessment, a priority search, or an independent historical-source authentication. The allowed report necessarily exposed its own status and prior-review language; those statements were not used as evidence. A direct successive-block construction below independently verifies the difficult existence step without invoking Baire's theorem.

## Exact input boundary

The sole mathematical reconstruction read was:

- `../source_question_family/freeze_20261017T182054Z/REPORT.md`, SHA-256 `937cc8726463b877986a8e1029b9d3608da7a21d2f70a41d052e964b09634a9a`.

The identity files read were `MANIFEST.json` (SHA-256 `380120978dde9fb18b556de83f5f875f5428d31d898c8e5072cbc82b1724d858`), `SOURCE_RECORD.json` (SHA-256 `34d786d7ac6cc8e7845543d1628dda06173f215552fdcc72f47e0f7610a564bc`), and `SHA256SUMS` in that same freeze. The first three hashes were recomputed locally. `INPUT_BINDINGS.json` records this boundary in machine-readable form.

No candidate PROOF/AUDIT, sibling report, separate prior verdict, later literature, historical PDF body, Git/index mutation, external application, or external communication was used. No historical source body was copied into this review folder.

## 1. Exact claim and falsification targets

Let a_n=f^(n)(0), ell_n=(n+1)^(-1/2), and u_n=log(n+e). For each nonnegative integer M, define

\[
X_M=\{f\in H(\mathbb C): \ell_n\le |a_n|\le u_n\text{ for every }n\ge M\}.
\]

The proof must establish three logically distinct statements:

1. HC(D) is dense relative to every X_M, despite the positive lower jet bounds.
2. Every f in every X_M has the asserted escape for every nonconstant p, irrespective of all jet phases.
3. The union of these relatively dense hypercyclic classes is dense in the ambient entire-function space.

The principal attempted falsifications were: noncomplete relative spaces; product-topology versus compact-open discrepancies; insufficient tail control after derivative shifting; failure at zero or large target coefficients; inability to preserve earlier orbit hits; leading-term cancellation for linear or complex polynomials; illicit countability of the polynomial family; and incompatibility with the source's generic preservation claim.

## 2. Independent structural check of the annular spaces

Set A_n={w in C: ell_n <= |w| <= u_n}. There is a natural bijection

\[
\mathbb C^M\times\prod_{n\ge M}A_n\ \longrightarrow\ X_M,
\qquad (a_n)\longmapsto\sum_{n\ge0}a_n\frac{z^n}{n!}.
\]

It is well defined: the finitely many free coefficients cause no problem, and the remaining series is normally convergent because

\[
\sum_{n\ge M}u_n\frac{r^n}{n!}<\infty
\quad\text{for each finite }r.
\]

For example u_n <= n+1 and the latter majorant sums to (r+1)e^r. The displayed map is continuous for the product topology: truncate a uniformly bounded tail, then control finitely many coefficients. Its inverse is continuous by continuity of all fixed derivative evaluations. Thus it is a homeomorphism. In particular X_0 is compact, and every X_M has the expected complete metrizable relative topology. This is consistent with the report's shorter argument: each X_M is closed in the complete compact-open metric on H(C).

The annuli are nonempty even at the boundary n=0, where ell_0=u_0=1. A boundary coefficient need not be perturbable inside an annulus because the proof preserves every low coefficient and only changes arbitrarily high ones. The constant baseline jets ell_n give a nonempty X_M.

## 3. Direct diagonal construction, avoiding Baire

This verifies relative density with an explicit mechanism. Fix g in X_M, r>0, and delta>0. Write b_n=g^(n)(0). Choose L>=M so that both the Taylor tail of g and the baseline tail after L have r-disk norm less than delta/4. Let

\[
F_0(z)=\sum_{n=0}^{L}b_n\frac{z^n}{n!}
       +\sum_{n>L}\ell_n\frac{z^n}{n!}.
\]

Then F_0 is in X_M and ||F_0-g||_r<delta/2.

Enumerate all triples (q_i,R_i,s_i), i>=1, where q_i has Gaussian-rational coefficients and R_i,s_i are positive integers. Write

\[
q_i(z)=\sum_{k=0}^{d_i}\beta_{i,k}\frac{z^k}{k!}.
\]

For the zero polynomial use d_i=0 and beta_(i,0)=0. Construct F_i by changing only the coefficients at a fresh block N_i,...,N_i+d_i, with N_i larger than every index previously modified and larger than L. At that block replace ell_(N_i+k) by gamma_(i,k), where

\[
|\gamma_{i,k}|\ge\ell_{N_i+k},\qquad
|\gamma_{i,k}-\beta_{i,k}|\le\ell_{N_i+k},\qquad
|\gamma_{i,k}|\le\max(|\beta_{i,k}|,1).
\]

These choices are possible by retaining beta when it is outside the tiny lower disk and otherwise moving radially to its boundary; use the positive real boundary point for beta=0. The strict upper constraint is not needed: the closed upper bound holds for sufficiently large N_i since u_n tends to infinity. Equality cases are admissible.

Choose N_i sufficiently large to satisfy all the following finitely many requirements:

\[
\ell_{N_i}e^{R_i}<\frac1{2s_i},\qquad
\|F_i-F_{i-1}\|_r<\frac{\delta}{2^{i+1}},
\]

and, for every j<i,

\[
\|D^{N_j}(F_i-F_{i-1})\|_{R_j}
 <\frac{1}{2^{i-j+1}s_j}.
\]

These simultaneous requirements are feasible. The block coefficient displacement has the N_i-independent bound |gamma_(i,k)-ell_(N_i+k)| <= |beta_(i,k)|+2. For any previously fixed derivative order t and disk radius R, its derivative norm is bounded by

\[
\sum_{k=0}^{d_i}(|\beta_{i,k}|+2)
 \frac{R^{N_i+k-t}}{(N_i+k-t)!}\ \longrightarrow\ 0.
\]

This is the full finite-prefix/tail neighborhood control; no previously achieved condition is discarded when a later target is inserted.

All coefficients of F_(i-1) beyond the preceding blocks are still baseline coefficients. All earlier changed coefficients lie below N_i and hence vanish under D^(N_i). Therefore

\[
\|D^{N_i}F_i-q_i\|_{R_i}
\le \ell_{N_i}e^{R_i}<\frac1{2s_i}.
\]

Every coefficient eventually stabilizes. Let F be the series with those stable coefficients. All F_i and F have the same finite initial prefix and obey the common bound u_n after M, so dominated Taylor tails give F_i -> F uniformly on every compact disk, and every fixed derivative also converges uniformly on compact disks. This checks normal convergence globally, beyond the one disk used to ensure closeness to g.

For each j, the later changes obey

\[
\sum_{i>j}\|D^{N_j}(F_i-F_{i-1})\|_{R_j}
\le\frac1{s_j}\sum_{h=1}^\infty2^{-(h+1)}
=\frac1{2s_j}.
\]

Hence ||D^(N_j)F-q_j||_(R_j)<1/s_j. Also ||F-g||_r<delta, and F is in X_M. The countable target family is dense in H(C): Taylor polynomials approximate an entire target, Gaussian-rational coefficients approximate their finite coefficients, and integer disks and reciprocal-integer tolerances form a cofinal family. Thus the full derivative orbit of F is dense. This proves HC(D) dense relative to X_M without Baire.

It also independently validates the report's relative Baire proof: its one-block estimates are correct, the hitting sets are relatively open, each is relatively dense, and X_M is complete. The spaces need not be invariant under D.

## 4. Polynomial escape, including complex cancellation and d=1

Fix any f in X_M and any p(z)=sum_(j=0)^d c_j z^j with d>=1 and c_d nonzero. At n>=M+d the exact derivative-normalized identity is

\[
(pf)^{(n)}(0)=\sum_{j=0}^{d}c_j(n)_j a_{n-j}.
\]

No extra j! is present: it is canceled between the binomial coefficient and p^(j)(0)=j!c_j. Let C=sum_(j<d)|c_j|. The highest contribution has modulus at least

\[
L_n=|c_d|\frac{(n)_d}{\sqrt{n-d+1}},
\]

and the sum of moduli of all remaining contributions is at most

\[
E_n=C n^{d-1}\log(n+e).
\]

For n>=2d,

\[
L_n\ge |c_d|2^{-d}\frac{n^d}{\sqrt{n+1}},\qquad
\frac{E_n}{L_n}
\le\frac{2^d C}{|c_d|}\frac{\sqrt{n+1}\log(n+e)}{n}
\longrightarrow0.
\]

The reverse triangle inequality therefore gives |(pf)^(n)(0)| >= L_n/2 eventually, and this lower bound tends to infinity. If C=0, there are no lower terms and the conclusion is immediate. For d=1 the bound is especially transparent: the leading term has modulus at least |c_1|sqrt(n), while the only possible error is at most |c_0|log(n+e). Arbitrary complex phases and arbitrarily large fixed lower coefficients cannot defeat this estimate.

The proof began with an arbitrary p and used only its finite degree and coefficients. Thus it proves the uncountable universal quantifier for each f directly; there is no intersection over a countable polynomial surrogate. Allowing p=p_n to vary with n would be a different statement and is not asserted.

Continuous evaluation at zero sends a dense orbit in H(C) to a dense subset of C. An escaping scalar sequence cannot be dense: its tail avoids the unit disk, and one can choose an open disk inside the unit disk avoiding its finitely many preceding values. This explicitly accounts for n=0 and every finite exceptional prefix.

## 5. Ambient density and the category compatibility check

Given any entire g, disk r and epsilon>0, choose a polynomial P within epsilon/3 of g. For sufficiently large M>deg(P),

\[
G_M=P+\sum_{n\ge M}\ell_n\frac{z^n}{n!}
\]

lies in X_M and is within epsilon/3 of P on that disk. The relative-density construction above gives an F in X_M intersect HC(D) within epsilon/3 of G_M. Thus

\[
B=\bigcup_{M\ge0}(X_M\cap HC(D))
\]

is dense in H(C), and hence also dense relative to HC(D).

There is a sharper direct category check. Each X_M is closed with empty ambient interior. Indeed, for g in X_M, change a sufficiently high jet n>=M by adding 3u_n z^n/n!. Its r-disk norm tends to zero, but the new nth jet has modulus at least 3u_n-|a_n| >= 2u_n>u_n. Therefore every ambient neighborhood of g contains a function outside X_M. The union of all X_M is meagre, as is B. A residual common preservation class may consequently be disjoint from this dense exceptional class without contradiction. This compatibility statement does not require independently accepting or reproving the historical theorem itself.

## 6. Separate fixed-polynomial perturbation audit

The report's separate local construction also withstands checking. At a root alpha of p of multiplicity m>=1, its coefficient C_k=c_m(k+m)!/k! is nonzero. Every term in B_k involves the already chosen jet a_(k+m-j) with j>m, hence index less than k. Moving C_k b_k+B_k to the radius-rho circle costs at most rho, so the normalized jet correction is at most rho/|C_k|. This works for complex C_k and the S=0 case.

The correction e has jets delta_k satisfying

\[
|\delta_k|\le\frac{\rho}{|c_m|}\frac{k!}{(k+m)!}.
\]

For every n,k>=0 the ratio (n+k)!/(n+k+m)! is at most n!/(n+m)!. Termwise differentiation, justified by normal convergence, therefore gives

\[
|e^{(n)}(z)|\le\frac{\rho}{|c_m|}\frac{n!}{(n+m)!}e^{|z-\alpha|}\longrightarrow0
\]

locally uniformly. The cutoff K only improves this bound. Tails of a dense derivative orbit are dense because a nonempty open subset of H(C), after removal of finitely many points, still contains a nonempty open subset. Accordingly adding e preserves hypercyclicity. The recurrence excludes a fixed scalar disk for all product derivatives n>=K+m; finitely many earlier values cannot fill that disk. Its stated closeness bound follows by summing rho R^k/(|c_m|(k+m)!) for k>=K. No defect or circularity was found in this separate mechanism.

## 7. Repair requirements and remaining limits

No mathematical repair is required to obtain the strong theorem. Optional exposition improvements are to add the explicit fixed-p/nonuniform-threshold qualification and the proof that the exceptional class is meagre; both make quantifier and category distinctions immediately checkable. The direct construction in Section 3 can replace or supplement Baire if a fully explicit coefficient argument is preferred.

The strongest verified scope is the dense simultaneous-counterexample theorem, plus the independent fixed-polynomial local perturbation statement. The exact remaining gap is **none identified in these mathematical claims**. Novelty, later priority, historical wording beyond the permitted reconstruction, publication readiness, and numerical construction of a particular entire function were outside this review. No finite numerical sample was used to certify an infinite orbit property.
