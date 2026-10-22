# Audited investigation: topological invariance of helicity

Problem 30006363 / OWR-14299512-001, rank 557.

**Unresolved after five substantive approaches.** This package does not claim
a counterexample, a full solution, or mathematical priority.

Start with [the mathematical packet](public/README.md) and its
[proofs and explicit gaps](public/PROOF.md). The [independent audit](audit/AUDIT.md)
accepts publication as a restricted-results investigation. It reproduces all
38 submitted checks, independently reimplements those 38 controls, and adds
12 further exact controls.

The source requires orientation- and volume-preserving conjugacy with the
same time parameter. The proved sufficient conditions additionally require
either bi-Lipschitz conjugacy, or smoothness away from finitely many zeroes
together with the stated boundary-growth bound. The general rough-conjugacy,
singular-field case remains unresolved.

The frozen proof and audit files are unmodified. See
[PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md) for an additive correction to
queue-blob provenance, and PUBLICATION_MANIFEST.json for the exact payload.

From this directory, with Python 3.11+ and SymPy 1.14.0 available:

    python audit/independent_checks.py
    (cd public && sha256sum --check SHA256SUMS)
    (cd audit && sha256sum --check SHA256SUMS)

These computational controls verify explicit examples and algebra. They do
not settle the unrestricted question.
