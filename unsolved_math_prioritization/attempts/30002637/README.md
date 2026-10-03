# Compact Ricci-soliton instability: audited partial results

**Original problem unsolved. Five substantive attempts completed, 5/5; budget exhausted.**

Problem 30002637 / OWR-13106-010 asks whether every compact smooth non-Einstein Ricci soliton has a positive eigenvalue of Perelman's ν-entropy Hessian modulo diffeomorphisms and scaling, in all dimensions. This packet does not resolve that question and makes no novelty claim.

## Audited conditional criterion

Let (M,g,f) be a smooth, connected, closed, non-Einstein gradient shrinker, normalized by Ric+Hess f=g. Let λ_f be the first positive eigenvalue of −Δ_f for e^−f dV and λ_Ric the first positive scalar gap for |Ric|²e^−f dV. Then

ν-linear stability implies λ_Ric ≥ λ_f.

Thus λ_Ric < λ_f is a sufficient condition for genuine quotient instability. In the normalized stability operator N, there is then a positive eigenvalue at least 1−λ_Ric/2. The numerical lower bound is for N; the ν-Hessian itself includes its conventional positive prefactor. A multiplicity version and exact tensor/conformal quadratic forms are included.

The universal strict gap decrease is not proved and is not asserted necessary for instability. No stable compact non-Einstein counterexample was found. The full source target remains unsolved.

## Proof, review, and retained record

- [Full conditional proof](frozen/TURN5_RIGIDITY.md), including nongradient gauge modes and the Ricci ground-state transform
- [Independent mathematical audit](review/INDEPENDENT_AUDIT.md): PASS for the actual partial claims, no required repairs; the original problem remains unresolved
- [Five-attempt endpoint](frozen/FINAL_STATUS.md) and [turn ledger](frozen/TURN_LEDGER.json)
- [Potential-Ricci test](frozen/TURN1_RICCI_MULTIPLIER.md), [conformal calculations](frozen/TURN2_CONFORMAL.md), [coupled tensor pencil](frozen/TURN3_COUPLED_POTENTIAL.md), and [finite-quotient investigation](frozen/TURN4_FINITE_QUOTIENTS.md)
- [Source and omission provenance](PROVENANCE.md)

The frozen files are preserved byte-for-byte. Their historical “unreviewed” or “pending” labels describe their state before the accompanying audit; this README and the separate review record report the current disposition. No mathematical revision has been made after the audit.

## Portable verification

Requires Python 3 and SymPy (the replay used Python 3.12.14 and SymPy 1.14.0; see requirements.txt for the exact packaged dependency).

Run: python verify_packet.py

This verifies the complete packet inventory and SHA-256 hashes, the original eleven-file frozen manifest, the audit binding, and both algebra replays (9 author identities and 8 independent audit identities). Algebra replay is a consistency check, not a proof of a geometric existence theorem or the missing universal sign. The written independent audit checks the analytic and geometric arguments.

## Primary references

- K. Kröncke, *Stability and Instability of Ricci Solitons*, Oberwolfach Reports 11 (2014), pp. 2017–2019, [DOI 10.4171/OWR/2014/36](https://doi.org/10.4171/OWR/2014/36)
- H.-D. Cao and M. Zhu, *Linear Stability of Compact Shrinking Ricci Solitons*, [arXiv:2304.01453v4](https://arxiv.org/abs/2304.01453v4)
- S. J. Hall and T. Murphy, *On the Linear Stability of Kähler–Ricci Solitons*, [arXiv:1008.1023](https://arxiv.org/abs/1008.1023)

Existing quotient criteria and Kähler special cases are prior credit. Noncompact stable shrinkers are outside this compact target. The literature checks were bounded; the audit does not certify novelty or exhaustive current literature coverage.
