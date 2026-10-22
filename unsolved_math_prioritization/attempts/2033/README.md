# EP-291 / problem 2033: audited harmonic-coprime partial theorems

**Status: partial. Infinitude of gcd(L_n H_n,L_n)=1 remains unresolved by this work.**

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the explicitly stated partial theorems; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The complete substantive proof and independent mathematical audit are retained. No mathematical correction was required. Historical finite tests and rigorous arithmetic bounds are described, but executable programs, detailed receipts, full computational certificates, raw datasets, and copied source documents are omitted. This edition is not an executable reproduction package. Edition preparation did not rerun mathematical tests or newly inspect scholarly sources.

For L_n=lcm(1,...,n), H_n=sum_{j=1}^n 1/j, and q_n=gcd(L_n H_n,L_n), the accepted results are unconditional avoidance of every fixed finite prime set on arbitrarily long intervals of endpoint ratio 6/5, positive lower natural density of each such finite-prime survivor set, and lower logarithmic density strictly greater than 283/2000 for integers avoiding only the universal leading digits p-1 for all odd primes.

The universal-digit survivor set U is larger than the coprime set: 33 belongs to U but q_33=11. The non-universal harmonic zero digits over a growing prime family remain uncontrolled. No independence of three or more reciprocal prime logarithms is assumed, and no full solution or novelty is claimed.

## Files

PROOF.md retains the full substantive proof, exact mathematical finite-bound description, and unresolved gap. AUDIT.md retains the independent mathematical reasoning and historical finite checks. ACCEPTANCE.md and ACCEPTANCE.json bind the exact accepted scope to this edition's proof/audit bytes. SOURCES.json records public citations, source hashes and sizes, and historical inspection limits. VERIFICATION.json preserves historical check identities and limitations. MANIFEST.json lists all eight members and hashes the other seven; its own digest is independently recorded in the publication description.

## Attribution

The exact local leading-digit criterion and one-prime harmonic density are prior work of [Peter Shiu, The denominators of harmonic numbers (Revised), arXiv:1607.02863v2](https://arxiv.org/abs/1607.02863v2). The retained revised PDF has eight pages despite its record's seven-page comments field.

[Wu and Yan, On the denominators of harmonic numbers. IV](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.282/) prove a conditional upper-density-one result for noncoprime cases, not unconditional coprime infinitude. [Sanna, On the p-adic valuation of harmonic numbers](https://iris.unito.it/bitstream/2318/1622121/1/padicharm.pdf) gives relevant fixed-prime prior progress. No source body or PDF is distributed here.

## Verification warning and distribution

Python optimization removes assert-based checks in the original candidate's programs. Their optimized execution is not an integrity certificate. The independent auditor's exception-based checks passed in normal, -O and -OO modes, including controlled rejection tests. This edition reports that historical verification without distributing executable code, full certificates, masks, detailed receipts, or raw data. Preparation performed byte-integrity and publication-plan checks, with no new mathematical test execution or source inspection. The original candidate and audit remain unchanged.
