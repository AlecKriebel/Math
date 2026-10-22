# Mathematical attempt record

## Attempt 1: extract the connected admissible-cover series from the 2025 divisor theorem

### Question and source correction

The 2023 question supplies a degree-two Hodge-integral series and asks for higher degree. The 2025 Iribar López–Pandharipande–Tseng divisor theorem is a relevant complete update. Its invariant counts possibly disconnected covers after the Hilb/Sym correspondence, so simply inserting its rational function into the original Hodge series would be incorrect.

### Calculation

1. Fix the factorial and phase from the original degree-two identity and the precise symmetric-product definition.
2. Use the target Hodge-line subbundle to prove λ_g=hλ_{g−1}, h²=0, and λ_gλ_{g−1}=0 on connected cover stacks.
3. Expand the equivariant Euler factor. Prove that at least two branched components contribute zero, while one branched component accompanied by ℓ unramified components contributes a factor 1+ℓ.
4. Sum the unramified covers. Their two weighted generating series are P(Q) and P(Q)log P(Q). The desired series is consequently obtained by dividing the disconnected expression by P(Q)(1+log P(Q)).
5. The 2025 theorem cancels the factor 1+log P(Q). Partition enumeration then replaces its trace by a divisor sum. Expanding the resulting cotangents gives the exact integral in every genus.

### Rejected shortcut

Equating the connected Hodge series directly to the normalized genus-one Hilbert-scheme divisor invariant gives wrong higher-degree answers. Already at d=3 it would add two copies of the degree-two series. Formula (13) of PROOF.md explicitly supplies this correction.

### Checks and outcome

The included verifier passed 248 exact assertions: degrees 1–10, the first eight branch-pair coefficients, the partition correction, degree-two normalization, degree-three and degree-four source examples, and the Euler-polynomial coefficients for genera 2–8. It also identifies a sign typo in the printed d=5 example of the source, without using that example in the proof.

Outcome: source-based resolution via an explicit corollary of the 2025 theorem. The mathematical statement is (1)–(3) of PROOF.md. Further attempts were unnecessary once this complete source-based deduction was obtained. No new-priority claim is made. The note remains AI-assisted and unrefereed.
