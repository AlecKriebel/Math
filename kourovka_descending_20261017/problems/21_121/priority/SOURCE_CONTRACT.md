# Source contract for Kourovka 21.121

Stage: **source preparation only**. Preparation completion: **100%** for the stated bounded audit. Original discovery: **0%**. Research selection and any new mathematics remain pending the parent's independent source audit. No result from 21.122 is transferred here.

## Authoritative source and split scope

The latest main PDF linked by the official site on 24 October 2026 is the **20 October 2026 update-3**, `21tkt-3.pdf`. Problem 21.121 is on printed and physical PDF page **197**, attributed to **C. Shramov**. The corresponding `21upd-3.pdf` repeats its update. Fresh downloads were hashed in memory and agree byte-for-byte with the already authenticated sibling cache; `OFFICIAL_CACHE_PROVENANCE.json` records both fresh hashes and the reused cache paths. The fresh home page and repository index are separately cached.

The official entry has two questions. Only **(a)** carries the solved marker, with a negative answer and an editorial statement that C. Shramov confirmed the cited AI solution. **(b)** has no solved marker in this version. The official repository links a solution specifically to **21.121(a)**. These are attributed editorial facts, not a new proof verification or a declaration that the entire numbered problem is settled.

Primary links: [official current main PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf), [official updates PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf), [official repository](https://kourovkanotebookorg.wordpress.com/repository/).

## Definitions with all quantifiers retained

Fix a prime `p`. The ambient object `Gamma` is an **arbitrary abstract group**. No topology, linear representation, finite generation, local finiteness, solvability, or geometric origin is assumed.

For a finite group `H`, let `H_(p)` be a Sylow p-subgroup and let `|H|_p = |H_(p)|`, the largest power of p dividing `|H|`. This is an order, not the number of elements whose orders are powers of p. Define

`j_p(H) = min { [H:A] : A normal in H, A abelian, gcd(|A|,p)=1 }`.

The trivial subgroup is permitted, so this minimum exists. The normality requirement is **inside H**; the subgroup need not be normal in Gamma. It may depend on H.

The p-Jordan condition is

`there exist J>0 and a finite real exponent s such that`

`for every finite H <= Gamma, j_p(H) <= J |H|_p^s`.

Equivalently each such H has a normal abelian p-prime subgroup with that index bound. The **same** J and s must work for all finite H in the single fixed Gamma. The constants may depend on Gamma and the fixed p. Allowing a different J for every H would erase the intended condition.

Let `E_p(Gamma)` denote the set of admissible exponents. The cited September/October 2026 paper explicitly uses real exponents. Optimizing over integers would change the question: a nonempty set of admissible nonnegative integers has a least element automatically. For a finite real infimum, write `e_p(Gamma) = inf E_p(Gamma)`; the official entry writes `e(Gamma)` with p fixed.

**Endpoint convention:** the official short statement does not specify the exponent domain at degenerate endpoints. The cited paper permits all real exponents and discusses the infimum when finite. One can instead use nonnegative real exponents for a global definition. For the requested upper-bound question (b), either convention yields the same bound `e_p(Gamma) <= 3`; the distinction matters only at nonpositive or extended-real endpoints. Any later formal statement must record its convention. The supplied nonattainment examples have positive finite infimum, so they do not depend on that endpoint issue.

## The two questions, separately

**(a), prior result:** must every finite p-Jordan exponent itself be admissible? The official source records a negative answer. Jayadevan's cited construction works for every prime p and has

`E_p(Gamma) = (1,infinity)`.

The latest Zenodo version is **23421603, 16 October 2026**, reached by the latest-version API from the official-cited record **22751568, 14 September 2026**. Both authenticated PDFs give this same theorem scope. Kinyon–Urban's official-hosted mathematical edition, version 4 of 19 September 2026, supplies a separate example for p=2 in Section 3.45. None of these is a full answer to (b).

**(b), only prospective research scope:** for every prime p and every p-Jordan Gamma, is

`inf E_p(Gamma) <= 3`?

Because admissibility is upward closed, this asks whether, for each epsilon>0, a constant `J_epsilon` works at exponent `3+epsilon` for every finite H in Gamma. It does **not** require admissibility at exponent exactly three. A purported counterexample must have finite p-Jordan exponent **strictly larger than three**. Showing only that exponent three is not attained would be insufficient.

An affirmative answer restricted to finite-dimensional linear groups, algebraic groups, soluble finite subgroups, uniformly virtually soluble finite subgroups, or rank-two Cremona groups does not address every abstract Gamma. A family of unrelated finite groups also does not supply the required single ambient p-Jordan group and uniform constants without an additional checked construction.

## Definition boundaries

* **Generalized p-Jordan** controls only finite subgroups whose orders are prime to p, with a uniform ordinary Jordan bound. It is weaker than p-Jordan and cannot replace the hypothesis or conclusion.
* **Jordan** controls a normal abelian subgroup of uniformly bounded index, without requiring its order to be prime to p. It is a distinct condition.
* Bounds with an exponent depending on dimension, rank, component count, or a soluble-index parameter are existence results on their stated classes. A displayed upper exponent larger than three is not a lower bound on the optimal exponent.
* Normal abelian p-prime subgroups, arbitrary abelian subgroups, and nilpotent p-prime subgroups must not be substituted for one another.

Hu, Definition 1.6 and Theorems 1.5/1.7; Chen–Shramov, Definitions 1.2/1.3 and Theorem 1.4; and Larsen–Pink, Theorem 0.4 supply the primary definition/reference trail. Their exact scopes are recorded in `PRIORITY.md`.

## Preparation boundary

This contract does not prove or disprove (b), verify every proof in a cited paper, certify exhaustive literature absence, or select a new research target. No Lean archive was executed. The parent must independently review the source package before selection. No original research on 21.121 has started.
