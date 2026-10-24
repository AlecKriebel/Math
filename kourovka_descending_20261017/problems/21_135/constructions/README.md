# Kourovka 21.135: construction-family reproduction

No complete solution is claimed. Read approach_constructions.md for the exact mathematical exclusions and the remaining gap. The full target permits arbitrary finite groups and requires degree multiplicities.

The local, excluded-from-version-control tools directory contains GAP4.16.1 core plus CTblLib1.3.11, GAPDoc1.6.7, AtlasRep2.1.9, Utils1.01, and a local Sympy installation. Download URLs and hashes are in artifacts/toolchain_manifest.json. No global installation was changed. The core was configured with the existing CommandLineTools clang and explicit SDKROOT, because the default Xcode compiler wrapper was unavailable; no Xcode license or system configuration was changed.

Use a standard GAP4.16.1 installation with CTblLib1.3.11, or the local executable:

```
./tools/gap-4.16.1/gap -q --bare --quitonbreak scan_library.g
python3 product_scan.py
python3 set_near_misses.py
./tools/gap-4.16.1/gap -q --bare --quitonbreak check_diagonal_outer.g
./tools/gap-4.16.1/gap -q --bare --quitonbreak adversary/independent_library_check.g
python3 adversary/compare_library_inputs.py
python3 adversary/independent_product_check.py
```

The GAP script scans all 2678 named library entries and retains the 2157 ordinary tables of order at most 10^8. It derives each radical order from the full table. The independent GAP script traverses the table names in reverse and extracts degrees through Irr(table); it reproduces every retained row. Neither script enumerates all finite groups of those orders.

The Python product scan adds the explicit trivial-group spectrum, collapses identical spectra, and tests unordered pairs with product order at most 10^12. It uses exact multiplicative invariants of the spectra. The independent checker uses fewer invariants and explicitly convolves all remaining candidates. It finds no target collision after 443 complete exact comparisons. The verified finite scope includes 15441 radical-free spectrum pairs and 1237165 pairs containing a nontrivial-radical factor.

The exploratory scripts factor_radicalfree.py, factor_all.py, exploratory_factor_report.py require Sympy in tools/pythonlibs (or an ordinary installation after adjusting the import path). Every polynomial factorization is reconstructed exactly. The output is deliberately labelled exploratory: no independent irreducibility certificates were supplied, so a claimed arbitrary-product exclusion must not be inferred from it.

The two adversarial proof audits, independent computation scripts, exact results, input comparison, and hashes are in adversary/. The full original Kourovka problem remains unresolved.
