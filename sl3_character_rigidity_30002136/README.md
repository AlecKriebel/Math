# A partial rigidity result for universal SL3 trace equivalence

**The original problem remains unsolved.** This packet proves an infinite proper-subfamily exclusion; it gives neither a universally trace-equivalent nonconjugate pair nor a separation theorem for every pair. No novelty claim is made.

## Exact problem

Do fixed nonconjugate u,v in F2=<a,b> exist such that tr rho(u)=tr rho(v) for every homomorphism rho:F2→SL3(C)? This is Ilya Kapovich's Question0.1, Oberwolfach Report35/2012, printed p2195: https://ems.press/content/serial-article-files/46404 . The source calls this character equivalence but defines it through standard traces. The first proof explains its equivalence to characteristic-polynomial equality in this universal dimension-three setting.

## Supported partial theorem

If, in some free basis, a cyclically reduced representative of u contains either at most three total occurrences of one generator and its inverse with arbitrary signs, or at most five occurrences of that generator all of one sign, then every universally SL3(C)-trace-equivalent v in the whole F2 is conjugate to u. Exponents of the other generator are unrestricted.

The companion is arbitrary at the outset. Both unsigned cyclic counts and signed exponent sums are proved invariant before the companion is put into the same gap format. The proof includes zero, repeated, negative, and unbounded exponents, proper powers, and the identity. Nothing shows that every word can be moved into a covered family.

## Contents and checks

- proofs/01_universal_reductions.md: universal trace reductions and fixed-pair identity certification
- proofs/02_low_occurrence_rigidity.md: signed/unsigned counts and same-sign counts through four
- proofs/03_mixed_two.md: mixed-sign count two
- proofs/04_five_same_sign.md: same-sign count five
- proofs/05_mixed_three.md: mixed-sign count three and the combined theorem
- review/: independently implemented controls and scope-qualified reviews

Run python checks/check_1.py through python checks/check_5.py. Python3 and SymPy are needed; check_2.py uses only the standard library. Their saved exact outputs are checks/result_1.json through result_5.json. Run the three review/independent_*_controls.py scripts for independent controls. Run python verify_public.py for file-hash verification. Finite controls supplement the general coefficient arguments; they are not extrapolated to universal identities.

The independent audit passed the proper-subfamily theorem and required a terminology correction: the first two leading principal minors are s and st; the three LDU diagonal pivots are s,t,(st)^(-1). The correction is applied here. The corrected projection passed narrow independent confirmation; see review/NARROW_REVIEW.md. The original question remains unresolved, and no novelty claim is made.

## Prior credit and status

Lawton–Louder–McReynolds, Groups Geom. Dyn.11(2017),165–188, §§4.2–4.3, https://arxiv.org/abs/1312.1261 , credits Horowitz's letter-count restrictions, discusses known SL2 constructions and higher-dimensional obstructions, and leaves its positive-word reduction conjectural. Its reported finite search is prior work; this packet claims no improved search bound. GMU MEGL's Special Words project also receives credit: https://megl.science.gmu.edu/wp-content/uploads/2021/03/MEGL_Summer_2016_Final.pdf .

Aougab–Lahn–Loving–Miller, Math.Ann.392(2025),861–898, §1.2, describes the higher-dimensional trace-pair question as open: https://link.springer.com/article/10.1007/s00208-025-03103-y . Current-source checks on2026-10-03 located no later resolution, without claiming exhaustive literature coverage.

The source record is UnsolvedMath30002136 / OWR-12007-016, from ulamai/UnsolvedMath snapshot37e53eabe540fb458758e198be61634bd02ee008; source metadata is CC-BY-4.0 and original publications retain their terms. Both corpus files were checked against the repository-published provenance hashes before work.
