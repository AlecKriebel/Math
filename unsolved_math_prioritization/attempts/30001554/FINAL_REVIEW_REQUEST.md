# Request for independent full source/proof review

Target30001554 / OWR-4425-009. Original unresolved, five genuine author turns complete. Please audit all mathematical claims and complete computational certificates, not only RESULT.md. Do not undertake an additional author search.

## Source and credit

Read SOURCE_NORMALIZATION.md, READINESS.json, PRIOR_GATE.json and SOURCE_MANIFEST.json. The exact source is OWR37/2010, contribution “Word periods under involution,” printed pp.2219–2222; Conjecture27 on p.2222. Four primary PDFs are hash-bound but not redistributed. Kari–Mahalingam Definition2(12) fixes the nonempty theta-border convention. The Holub–Nowotka ordinary theorem is a credited external input to Turn1's orbit-period statement only. Turn2 supplies its own proof of the source's signed Fine–Wilf assertion. The catalog's contemporaneous Bischoff2010 thesis returned502 and was not read; no novelty certification is requested.

## Sensitive proof points

- Morphic involution means a literal fixed-point/two-cycle letter permutation, not an antimorphism. Alternating negative shifts differ from arbitrary block-choice theta-periods
- Turn2: modular cycle parity including odd cycles forcing fixed letters; common-translation extension and gluing; finite-window reduction for all lengths; completeness of canonical fixed/pair orbit generation and the first-new-orbit restriction
- Turn3: parity-adjustment of factors at odd starting positions; exact ordinary and complementing periods of three runs; every possible unbordered factor; source family and symmetric n=3tau−4 examples remain below threshold
- Turn4: why the completion is primitive in the nonfixed case, least-rotation ordinary unborderedness, transferring its first half into the actual finite word, and the use of minimum tau when extracting a3tau-length counterexample
- Turn5: suffix-mask recurrence, complete terminal-stream identity, canonical periodic-completion counting without promoting subset counts to inclusion, exact all-length threshold proof from per-depth enumeration, and lower-witness actual tau values

## Replay

Run from this directory (Python3, standard library):

    python verify_turn1.py > /tmp/turn1.json
    cmp TURN_1_CHECKS.json /tmp/turn1.json
    python finite_window.py --max-t 7 > /tmp/enum7.json
    cmp TURN_2_ENUMERATION.json /tmp/enum7.json
    python verify_turn2.py > /tmp/turn2.json
    cmp TURN_2_CHECKS.json /tmp/turn2.json
    python verify_turn3.py > /tmp/turn3.json
    cmp TURN_3_CHECKS.json /tmp/turn3.json
    python verify_turn4.py > /tmp/turn4.json
    cmp TURN_4_CHECKS.json /tmp/turn4.json
    python finite_window_fast.py --t 8 > /tmp/enum8.json
    cmp TURN_5_ENUMERATION_T8.json /tmp/enum8.json
    python verify_turn5.py > /tmp/turn5.json
    cmp TURN_5_CHECKS.json /tmp/turn5.json

The t8 run may take a few minutes; it is uncapped and produces a short count/hash receipt. Its487,930 terminal stream objects are hashed online. The fast checker also replays t1,...,7 against the frozen literal implementation's receipt.

Optional separately written C++17 direct-border implementation:

    g++ -O3 -std=c++17 crosscheck_windows.cpp -o /tmp/windows_check
    set -o pipefail
    /tmp/windows_check 8 2> /tmp/t8_cpp.json | sha256sum
    cmp TURN_5_CPP_T8.json /tmp/t8_cpp.json

The digest must be85fe35ef00d0592f766e4c150292a6b8f9bfa09f9c869e65fcff61e13c1a87f1. No large stream is included. Check all historical manifest hashes and the final manifest before issuing a verdict. A qualified scoped PASS must leave the unbounded original unresolved and make all external-credit/access limits explicit.
