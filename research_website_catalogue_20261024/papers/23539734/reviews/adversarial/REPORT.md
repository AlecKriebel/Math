# Adversarial review: A fixed birational map without a prime-field cycle-distribution limit

Review completed UTC: 2026-11-14T23:40:07.690547+00:00. Completion estimate: 100% for this assigned adversarial lane.

**Verdict: no substantive defect found in the stated mathematical claims.** Theorem 1 and Proposition 4 survive independent algebraic, finite-graph, analytic-quantifier, weak-convergence, and exceptional-completion attacks. This is AI-assisted internal review, not independent human peer review. No historical firstness, novelty, or current open-problem status is certified.

## Objects and independence

Zenodo record 23539734, DOI 10.5281/zenodo.23539734, version 1.1, manuscript dated 21 October 2026. The actual eight-page published PDF has SHA-256 e555c20722ca9edb2bc8d164103e748b87c37b56e5eb8bed18c80b33031f737c; the actual controlling 25,497-byte, 538-line TeX has SHA-256 8d93d964cf09e2d895048456aca91d075edb2d2002b85de0dd061f6e2aa9e25f. SOURCE_READY.json has SHA-256 1e18c3ce5d1b7556f97ee9c90f4d8ed21fa6a4d19e54cee8b730210a15795eaa. These full fields are distinct and physically rechecked.

I read the complete target PDF/TeX before any foreign primary body, code/data, historical/current review or inventory opinion, then wrote substantive quantified reconstruction and five attack families. INITIAL_RECONSTRUCTION.md was sealed at 2026-11-14T23:32:07.563745+00:00 with SHA-256 09fb1503b66151e6b1bb3604f8ca7393053b21f54991bf711727e3f504d83a44. No sibling scientific reports or root opinions were read later. Raw primary texts from the expressly permitted cache and all ten supporting Python sources were read only after this seal. Root's own independence gate opened before this lane shared substantive findings. An extra narrow subreview was attempted, but all concurrency slots were occupied.

## Exact result tested

For every p=3 mod4, L(u,v)=(u,(u²+1)v) permutes all p² affine points. For point-weighted least periods divided by p, every fixed x in [1/2,1) has eventual CDF D_p(x)=1-phi(p-1)/(p-1)+o(1), with the displayed 1/p+64p^{-1/4} error; limsup is 1 and liminf at most 23/24. For every prime subset of positive upper relative density in that class, neither these fixed-x CDF values nor the period measures converge. The all-odd-prime proposition concerns the regular invariant domain, or uniform-point deletion/completion affecting only exceptional fibers and retaining every regular point. It does not assert a full-affine permutation in class 1 or a moving-x estimate.

## Attack outcomes

1. **Rational map, reductions, and raw graph dynamics.** Both rational compositions are identities off u²+1=0; L^m(1,1)=(1,2^m) proves infinite order. Complex fibers u=±i preclude a polynomial inverse, and generic invariant fibers are lines. Direct full functional graphs include class-1 tails and recover precisely the claimed permutation/regular-domain behavior. No reduction or nonperiodic-point assumption was hidden.

2. **Point versus cycle weighting and endpoint attacks.** Maximal fibers exclude p-1 points each, not one cycle each. Proper-divisor periods lie below p/2. The exact CDF formula requires px<p-1. At p=3, D_3(1/2)=5/9 while D_3(3/4)=1; this is the paper's explicitly excluded small-prime cutoff, not a defect. At moving x=(p-1)/p all points are included. Universal, moving-threshold, and equal-cycle-weight extensions were not used.

3. **Independent character mechanism.** Beyond checking the supplied indicator/Jacobi proof, I derived the norm by a distinct double-sum route, bypassing Gauss sums. For nonprincipal chi, S=sum_{a!=0}eta(a-1)chi(a); its norm is determined by C(1)=p-2 and C(t)=-eta(t)-1 for t!=0,1. This gives |S|²=p except chi=eta, when |S|²=1. The principal term is p-r, not p at bad reductions. Exact integer autocorrelations verify every character norm simultaneously for all odd primes through 251. The 64 N^{1/4} bound and ensuing uniform o(1) are valid.

4. **Analytic subsequences and prime means.** The Mobius rearrangement includes p=2 correctly; the large-d tail and summed Siegel-Walfisz errors are negligible. The absolutely convergent Euler product and coarse 7/24 bound justify the mean contradiction at 13/48. Increasing CRT/Dirichlet primes give theta->0. No zero-density versus positive-density inference is made from those two subsequences alone.

5. **Positive upper density, weak convergence, and adversarial completions.** A convergent selected sequence must eventually lie in every fixed neighborhood of its limit. An atomless whole-prime law gives the selected upper density at most each neighborhood mass, hence zero. Dense-block attempts do not evade this. The globally bounded continuous ramp isolates maximal periods, so the weak-convergence argument does not rely on an invalid CDF-continuity shortcut. Arbitrarily large mixed exceptional assignments retain total mass <=2/p; every bounded statistic changes by vanishing mass. The stated uniform regular weights and domain assumptions are necessary and explicit.

6. **Foreign input and historical scope.** DH Proposition 2.1/equation (2.1) at m=2 directly supplies the continuous shifted-prime scalar law, while AS formula (1.1), Theorem 1.3(i), and Section 6 support the exact n=1 translation and prime-power removal. Continuity is used, not absolute continuity. MP Lemma 2 supports the mean; BCST Section 2 supports the classical primitive indicator; OS Section 2.1 contains the older triangular family. The complete Vivaldi primary body states the p-normalized point-weighted statistic and broad existence assertion; its later genus-one heuristic and distinct p² prime average are kept separate. Roberts reference 9 verifies the retained unseen-2011-preprint lead but cannot settle that body's contents or priority. Foreign bodies were read as raw cached primary text; source-lane provenance and fuller literature coverage remain that lane's responsibility.

## Reproducible artifacts and custody

The new independent_verifier.py imports no submission/review helper and writes no files; it passed **177,208 exact checks** over all 168 odd primes through 1009 (87 in class 3). It checked 65,792 points in full functional graphs at 24 odd primes through 97, all character norms by integer autocorrelation at 53 odd primes through 251, exact primitive indicators for group orders 1..250, and every retained exceptional count with mixed assignments including 10^100 at applicable primes through 101. INDEPENDENT_RESULTS.json records scope and counts. This is finite evidence, not an inference about infinite primes.

The active verify.py passed its archive check (68 manifested payloads plus the manifest itself), 147,619 class-3 checks, and 46,298 all-odd checks. All ten supplied Python files were inspected. Every executable route was replayed: the active verifier invokes its two helpers; the seven archived routes also passed. In the present environment SymPy is available, so both originally SymPy-dependent routes replayed successfully. The archived broad finite and analytic runs reproduced exactly 8,347,742 and 230,780 controls respectively. Their scopes remain separate and are not added to the new active-checker total. Scripts that write receipts were executed from byte-identical copies under this lane; original inputs were preserved.

ORIGINAL_PAYLOAD_CUSTODY.json confirms all 69 original archive payloads match their extracted source bytes. No manuscript, native source/archive payload, site, spreadsheet, Git state, release, or external communication was changed by this lane. Detailed derivations, read scope/hash ledger, stdout/receipts, log, manifest, and final seal accompany this report.

## Remaining gap and recommendation

No exact proof gap or counterexample remains from these attack families. The infinite-prime conclusions use credited standard unconditional prime-distribution theorems, not computation. Historical firstness and the unseen preprint's relationship remain unresolved and are already disclaimed in the manuscript. Passing this lane supports the stated mathematical claims with these boundaries; it does not authorize broader historical or scientific wording. No new research follow-up is proposed.
