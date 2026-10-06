# Independent checkpoint 02 — direct numerical software

2026-10-05 12:32 UTC. Completion estimate 55%.

Official QPA manual chapter 12.3 declares `AreDerivedEquivalent(A,B)` returning true/false for gentle algebras over the same field. Pinned complete source `qpa-combinatorialmap.gi` implements marked ribbon map, winding of every face (including zero-marked faces), tree/cotree nonseparating curves, cutting handle pairs, gcd/parity/Arf comparison. GitHub primary history reports addition 13 June 2024 and bugfix 18 June 2024, exact commits retained in `qpa-map-history.json`. Native GAP unavailable in this environment (`command -v gap` exit 1 light read, no subprocess PID).

Adversarial caveat: current body has obvious suspicious logic: boundary comparison `IsSubset(boundA,boundB)` ignores multiplicity; parity loop intended for B instead repeats A, and parity mismatch is not separately rejected before the mod4 branch. Therefore documentation cannot establish an error-free decision implementation. Historical-source and mathematical algorithm checks still needed. Presence of these bugs does not erase earlier constructive homology/numerical method, but changes the legitimate assertion from a fully validated correct executable to prior published algorithms and implementation claims unless repaired/verified independently.

String Applet raw archive 2022 lacks homology/Arf methods, raw March 2025 archive has them. Thus author role/footer 2020 is not a feature date. Applet complete-feature publication bounded above by March 2025; QPA is potentially earlier decisive source.

Provisional priority: broad claim of first algorithm/open resolution is strongly threatened, exact verdict pending historical and correctness scope. Do not infer open in 2026 from workshop 2020 or APS remark 2023.
