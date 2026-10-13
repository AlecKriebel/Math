# Harmonic circle fibrations for a freely chosen metric

Problem 30003375 / OWR-15208-029. Reviewed 13 October 2026.

## Accepted conclusion

For every closed connected smooth manifold M homeomorphic to S¹ × CP³ and either primitive class u in H¹(M; Z), there is a smooth Riemannian metric g for which the harmonic circle map in class u is a smooth fibration with connected fibres. The same constructed metric works for both signs of u. If a smooth bundle projection is already supplied, the construction makes that very projection harmonic.

This is **`already_solved` for the expressly adopted unrestricted existential-metric formulation E**, with result classification **`prior_result`**. Browder–Levine supplies smooth fibering. Calabi's intrinsic-harmonicity result, as recalled by Katz, supplies the classical metric-existence mechanism; the needed bundle case is also proved here by an explicit metric construction. No novelty or historical priority is claimed.

Farrell's source paragraph does not state the metric quantifier or the circle map's homotopy class. E and the primitive-class normalization are editorial choices. This reader does not authenticate the author's intent, settle every possible reading of the source, analyze arbitrary or supplied metrics, or resolve the neighbouring sectional-curvature questions.

## Read the result

1. [PROOF.md](PROOF.md) gives the exact accepted theorem, all hypotheses, the explicit construction, the harmonic-map argument, and scholarly references. It has not been edited in assembly.
2. [INDEPENDENT_MATHEMATICAL_AUDIT.md](INDEPENDENT_MATHEMATICAL_AUDIT.md) checks the topological input, connectedness, orientation, Moser sign and composition, bundle isomorphism, seam smoothness, fixed volume, Hodge star, and uniqueness. [ACCEPTANCE.json](ACCEPTANCE.json) records that audit's exact proof pin and qualified verdict.
3. [SOURCE_SCOPE_ACCEPTANCE.md](SOURCE_SCOPE_ACCEPTANCE.md) is the separate authored source-scope and prior-credit adjudication. Its accepted normalization and limits must accompany any use of the disposition.
4. [RESULT.json](RESULT.json) gives the scope and effort accounting in machine-readable form.

The mathematical proof, source-scope report, independent audit, acceptance, and both original check scripts and outputs are preserved byte-for-byte from their accepted versions. All links to scholarly sources are public; source PDFs, dataset contents, and private coordination material are not included.

## Reproduce the finite checks

Use Python 3 with the standard library. No package installation, network request, source PDF, dataset, repository checkout, or external input is needed. Python 3.12.14 was used for the included reproduction. From this directory run:

```sh
python3 -I -B verify_reader.py
```

The verifier checks every manifest-listed file's byte count and SHA256, rejects extra files and symlinks, then copies only the two scripts and their expected outputs into a fresh temporary directory. Each script runs there with a fresh Python process, `-I -B`, a minimal environment, and assertions enabled. The standard output must match its recorded JSON byte-for-byte. The successful verifier output is recorded in [REPRODUCIBILITY_RESULTS.json](REPRODUCIBILITY_RESULTS.json).

Do not redirect output into this directory: its complete file list is fixed by the manifest. To compare the verifier output, write to a temporary file outside the reader and compare it with REPRODUCIBILITY_RESULTS.json. No `-O` or `-OO` run is claimed; the verifier rejects those modes because the unchanged mathematical scripts use assertions.

The author checks 60 seeded exact-rational interpolation cases in fibre dimension six, including positive definiteness, pullback determinants, Jacobi's determinant derivative identity, and fixed-volume normalization. The independent script checks explicit algebraic witnesses for common errors involving normalization, density-weighted Jacobians, composition order, Moser's sign, endpoint jets, and total versus pointwise fibre volume. The examples' geometric interpretations are justified in the written audit; the scripts do not symbolically formalize those interpretations.

These are finite sanity checks. They do not prove Browder–Levine or Serre, verify infinite-dimensional existence or all seam jets, classify exotic smooth structures, formally check Hodge theory, or replace the written proof. Interpreter and working-directory isolation is reproducibility hygiene, not an operating-system security sandbox.

## Dependencies and integrity

The imported smooth-topological existence theorem is Browder–Levine's Theorem 1.4. Serre's finite-generation result and standard de Rham, Hodge, smooth-flow, and bundle theory are also used. Their relevant statements and application were checked; the complete imported proofs were not independently rederived. The special metric construction and its compatibility arguments are given in full. The original Calabi chapter was not directly inspected; attribution is explicitly through Katz.

[MANIFEST.json](MANIFEST.json) lists every other file in this reader, its byte count, and SHA256. The manifest excludes only itself to avoid a self-hash cycle. A separately supplied manifest hash pins the entire list; hashes establish byte identity, not theorem validity or source authorship.

One newly documented substantive proof-search pass is recorded. The lifetime count before that pass is unknown; source adjudication, independent auditing, finite-check reproduction, and reader assembly add no substantive pass.
