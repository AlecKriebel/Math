# Unbounded Johnson-filtration multiplicities

This is an AI-assisted, unrefereed mathematical draft. Acceptance means an internal AI mathematical audit found the stated argument valid with the explicit standard imports; it is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Result and convention

For every fixed closed oriented surface of genus g >= 2 and every fixed k >= 3, the logarithmic pseudo-Anosov dilatation spectrum of I_g(k) has unbounded multiplicity when multiplicity counts conjugacy classes in the full orientation-preserving mapping class group Mod_g. Equivalently, for every positive N there is a common log dilatation represented by at least N ambient Mod_g-conjugacy classes in this one fixed I_g(k).

This gives a negative answer to Farb Question 7.6 under the ambient convention supplied by its source context. The lower central indexing is Gamma_0 = pi_1(S), Gamma_(j+1) = [Gamma_0,Gamma_j], and I_g(j) = ker(Mod_g -> Out(Gamma_0/Gamma_j)); I_g(1) is Torelli.

## Read the proof

- [PROOF.md](PROOF.md): complete construction and proof, with the full dependency ledger and fixed genus-two illustration.
- [AUDIT.md](AUDIT.md): complete independent internal mathematical audit, including Nielsen–Schreier/Hopf free-basis justification, the signed saddle-holonomy lattice, and the proper-power-safe finite-core conjugacy bound.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): exact mathematical scope and document bindings.
- [SOURCES.json](SOURCES.json): public bibliography, retained PDF hashes/sizes, retrieval and inspection history, and standard-import boundaries.
- [VERIFICATION.json](VERIFICATION.json): provenance and verification limits.
- [MANIFEST.json](MANIFEST.json): all eight filenames and hashes for the other seven; its own digest is pinned separately in the draft-PR body.

## Mechanism

A separating filling pair yields a unit-square half-translation surface. Signed saddle-connection holonomy places the entire disk-stabilizer derivative group in a conjugate of PSL_2(Z). A fixed two-generator free subgroup H deep in the Johnson filtration consists entirely of pseudo-Anosovs away from the identity. The fixed finite core of its derivative image bounds fusion of H-conjugacy classes under ambient mapping-class conjugacy by C = 6|V(Y)|. Horowitz's universal equal-trace families then give at least ceil(2^m/C) ambient classes with one common dilatation for every m.

## Scope cautions

Genus, depth, the filling pair and H are fixed before m varies. The spectral value may vary with m. The theorem does not assert infinite multiplicity at one fixed spectral value, primitive mapping classes, a uniform bound in g or k, or any answer to the separate simple-length-spectrum Question 7.7. The complete argument imports standard Teichmüller theory and Horowitz's theorem. Optional finite trace checks are illustrative only and do not prove the arbitrary-m or ambient-conjugacy conclusion.

Only authored mathematical prose and public verification/source metadata are distributed here. No copied third-party source documents, source code, raw experiment outputs, or source datasets are included.
