# Final five-turn partial packet: primitive root3 for p=16q^4+1

Problem3356 / OPG-37396. Original universal conjecture remains **unsolved** after five substantive author turns. No sixth search, complete proof, original counterexample or novelty claim is implied. Separate scoped review is requested before a final unresolved draft.

## Proven and finite results

- The original quadratic-reciprocity/qth-residue reduction is credited to the anonymous2012 Open Problem Garden comment
- Order16 is impossible; residual orders are16q,16q^2,16q^3 versus the desired16q^4
- Exact, dependency-free finite proof for every prime3<q<=100,000,000:418,013 prime p values, each with3 a certified primitive root; all other5,343,440 values certified composite
- Kummer–Chebotarev compatibility theorem for a larger fixed-q arithmetic progression; explicitly does not decide the diagonal value16q^4+1
- An exact exponent42 neighboring-family counterexample, not a counterexample to exponent4
- A proved quartic identity3^(4q^4)=-4q^2 modp, with exact residual sign test at exponent4q^3
- A complete Frobenius-algebra split/irreducible dichotomy, and explicit reasons the discriminant and determinant invariants fail to choose the desired branch

Read TURN_1.md through TURN_5.md for arguments, source attribution and the exact unproved remainder. The universal octic sign in TURN_3.md is only a finite observation and is not used as a theorem.

## Reproduction

All final checkers use only Python's standard library:

    python certify_turn1.py --bound 1000000 --output replay1.json
    python verify_turn2.py
    python verify_turn3.py
    python scan_turn4.py --bound 100000000 --segment 1000000 --output replay4.json
    python verify_turn5.py

The100-million bound run took about69 seconds on the original executor; runtime is not a result or required match. Exact mathematical totals, example certificates and certificate-stream hash must match. The full per-q row streams are not retained remotely. The first-turn6.2MB uncompressed row file can be regenerated with --rows; its hash is recorded in REMOTE_MANIFEST.json. The fourth-turn stream is generated and hashed online by scan_turn4.py. Do not describe a digest alone as a remotely stored full certificate stream.

The finite verification does not extrapolate beyond its stated bound. It proves that any original counterexample has q>100,000,000. The exact universal remaining statement is the exclusion of3^(16q^3)=1 mod(16q^4+1) for those larger q whose indicated modulus is prime. No complete argument excludes this case.

AI-assisted research; separate AI scoped review does not constitute human peer review or a proof-assistant certificate. No external researcher contact, merge, release, DOI or journal submission is included.
