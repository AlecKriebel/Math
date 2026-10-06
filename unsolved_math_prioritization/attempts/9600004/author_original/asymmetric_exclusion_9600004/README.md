# Step ASEP: exact four-site small-time certificate

This authored proof and dependency-free checker establish only a local partial result for problem 9600004 / AMR-095-0004. They do not solve the full problem and do not assert novelty.

For deterministic eta_0(x)=1{x<=0}, right rate p>0, and 0<=q<=p, the four occupation variables at {-1,0,1,2} are negatively associated for 0<=p*t<=1/10837981440.

Run with Python 3.9 or later:

    python check_certificate.py --cross-window
    python -O check_certificate.py --cross-window
    python -I -S check_certificate.py --cross-window
    python test_mutations.py

The checker recomputes all 174 disjoint increasing-event pairs with exact rational polynomials in r=q/p, verifies all lower terms vanish and all leading coefficients are negative constants, compares every case against certificate.json, and recomputes the explicit uniform remainder bound. It uses no network or third-party package. No check depends on Python assert statements.

PROOF.md explains infinite-volume validity, reduction from indicators to arbitrary increasing functions, and the exact remaining gap. LITERATURE_AUDIT.md separates the target from the inspected primary results. SOURCES.json contains source and public-corpus verification metadata. VALIDATION.json records author replay and mutation outcomes. The external ZIP manifest is kept outside the payload.
