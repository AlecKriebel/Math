# Row 1882 source and current-literature gate

Checked 2026-10-21. Target: 30002506 / OWR-12866-016, Bohr-Radius Characterization of ℓ¹.

## Recovery and scope

The exact historical queue row is 1882, immediately following 1881 / 30002208. Its initial status and turn counter are queued and 0/5. The complete problems corpus contains the matching ID and source number. No matching ID, source number or title occurs in the full research-results corpus values. Input hashes and byte counts appear in PUBLIC_VERIFICATION.json; corpus content is not included in this authored note.

The original source is A. Defant's problem 6 in the open-problem section of *Dirichlet Series and Function Theory in Polydiscs*, Oberwolfach Report 06/2014, printed pages 388–389 (PDF pages 54–55). The original assumptions are a complex Banach sequence space X with ℓ¹ contained in X contained in c₀ as sets, whose canonical coordinate vectors form a 1-unconditional basis. X_n is the first n-coordinate subspace. The problem asks whether a dimension-independent positive lower bound on the scalar holomorphic Bohr radii K(B_X_n) forces X=ℓ¹ as sets. The generated short statement omits the explicit inclusion and basis assumptions; these must be restored, not weakened or silently replaced by symmetry.

Primary source: https://doi.org/10.4171/owr/2014/06
Official PDF: https://publications.mfo.de/bitstream/handle/mfo/3396/OWR_2014_06.pdf?isAllowed=y&sequence=1

## Current gate: open, not a known-solution closure

Defant, Galicer, Mansilla, Mastyło and Muro, *Local constants and Bohr's phenomenon for Banach spaces of analytic polynomials*, arXiv:2509.26326v2 (1 October 2025), explicitly retain Lempert's problem as open immediately after Theorem 2.21, on PDF page 28. Their positive theorem uses projection constants, not the required monomial-unconditional constants.

Let A=sup_{m,n} χ_mon(P_m(X_n))^(1/m). Proposition 2.28 and Theorem 2.29, PDF page 32, give K_m=χ_mon^(-1/m) and (1/3) inf_m K_m ≤ K ≤ inf_m K_m. Consequently inf_n K(B_X_n)>0 is equivalent to A<∞. Thus the paper's open problem is the recovered target, rather than merely a similarly named problem. It records only a near-ℓ¹ bound, with an arbitrarily small positive power of log log n; that does not provide a uniform embedding into ℓ¹.

Latest version inspected: https://arxiv.org/html/2509.26326v2
Version/status page: https://arxiv.org/abs/2509.26326
PDF: https://arxiv.org/pdf/2509.26326v2

This is affirmative recent evidence of an open status, not proof that no later solution exists. Targeted current searches found no later resolution. The 2021 similarly titled characterization concerns vector-valued functions on a one-dimensional disk, not the scalar functions on the sequence-space coordinate balls here. The dataset's additional UPV download was blocked by its anti-bot page; it was not relied on as inspected full text.

## Repository duplication gate

Connected GitHub all-state PR searches on AlecKriebel/Math: `30002506` returned none; `Bohr` returned only unrelated PR 615 (Hamiltonian dynamics); `Lempert` returned none. No target duplicate was located. These are search results, not exhaustive proof against unindexed content.

## Decision

Proceed only as an open research attempt under the restored original assumptions. Do not mark solved from the projection-constant theorem or from classical ℓᵖ cases. No proof attempt, publication or queue modification was performed in this recovery gate. All downloaded source PDFs and extracted text are kept private; only this authored assessment and verification metadata are release candidates.
