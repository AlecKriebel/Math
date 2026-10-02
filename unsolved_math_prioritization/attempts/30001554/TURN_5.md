# Turn 5: exact saturation thresholds through tau=8

Final author turn. The original conjecture remains unresolved; author search stops after this freeze. This turn supplies a faster exact enumeration with a proved update rule, an independent literal C++ stream comparison, a combinatorial count of periodic completions, and sharp all-length conclusions for bounded tau.

## 1. Incremental negative-period masks

For each suffix w[i:m] of the current prefix, store a bitmask whose bit p is1 exactly when p is a negative period of that suffix. The full suffix length is included as a vacuous period. Suppose the next letter is a at position m. Define a match mask M whose bit p is1 precisely when a=theta(w[m−p]), for1<=p<=m.

For a suffix of previous length ell=m−i, the new mask is

    (old_mask AND M) OR (1 shifted left by ell+1).     (5.1)

Indeed, each old negative-period condition adds just the comparison involving the new last letter, encoded by M. The only newly available positive period is ell+1, which is vacuous. A new one-letter suffix has only period1. Therefore a newly completed suffix longer than t is unbordered exactly when its proper-period part old_mask AND M vanishes.

This proves the update rule in finite_window_fast.py. Together with Turn2's canonical generation and first-orbit lemma, it enumerates exactly the same accepted prefix tree, with no cap or randomization. The code does not import the earlier literal-border enumerator.

## 2. Full tau=8 certificate and independent agreement

At t=8, the word length is24. The complete enumeration has487,930 terminal canonical representatives, every one with a negative period<=8. TURN_5_ENUMERATION_T8.json contains all per-depth counts and the canonical terminal stream's digest:

    85fe35ef00d0592f766e4c150292a6b8f9bfa09f9c869e65fcff61e13c1a87f1

The stream encoding is exactly Turn2's compact JSON [orbit_types,word] plus newline in recursion order. A separately written C++17 program, crosscheck_windows.cpp, uses direct prefix/suffix comparisons rather than masks and independently reproduces every node count, every nonperiodic-prefix count, all487,930 terminal objects, and the full stream digest. Its output is piped directly to sha256sum; no large stream file is needed or distributed.

Together with Turn2, this proves the original source implication for every finite alphabet, every morphic involution and every word length when actual tau<=8. It does not establish the family of all t.

## 3. An independent combinatorial count of the periodic subset

Let A_p count canonical p-letter words with fixed/pair orbit types recorded, and let B_p be the Bell number counting ordinary canonical words. A block of k occurrences of one theta-orbit has1 fixed realization or2^(k−1) paired orientations after normalizing its first orientation. Considering the orbit containing the first position gives

    A_0=B_0=1,
    A_(m+1)=sum_{k=0}^m binom(m,k)(1+2^k) A_(m−k),
    B_(m+1)=sum_{k=0}^m binom(m,k) B_(m−k).            (5.2)

Let F_p count fixed-support periodic completions of least ordinary period p, and N_p count nonfixed completions of least negative period p. A fixed-support completion has period p exactly when its least period divides p. A nonfixed completion of least negative period q has primitive ordinary block length2q, by Turn4. Its negative periods are exactly the odd multiples of q: two negative shifts differ by an ordinary period, and shift q acts by theta. Consequently

    F_p = B_p − sum_{d|p, d<p} F_d,
    N_p = A_p − B_p − sum_{d|p, d<p, p/d odd} N_d.     (5.3)

Equivariant canonical normalization is preserved under taking the shorter determining prefix and its alternating completion, so these are bijective decompositions rather than counts of labeled alphabets.

There are S_t=sum_{p=1}^t(F_p+N_p) distinct canonical infinite completions with a negative period<=t. Their prefixes of length3t are distinct. To justify this last point, if two completions agree on a segment of length at least p+q, extend the other's negative-period relation along period p using the same translation argument as Turn2's extension lemma. They then agree on the whole completion. Conversely every finite negative-p word determines its completion from its first p letters. Thus S_t also counts precisely the canonical3t-letter words with a negative period<=t.

The values S_1,...,S_8 are

    2, 8, 37, 199, 1196, 8026, 59814, 487930.

They agree with the exhaustive terminal counts. This is an additional independent count of the periodic subset. **The recurrence alone does not prove that all tau<=t words lie in this subset.** That inclusion is exactly what the complete finite enumeration checks for t<=8 and what remains unproved in general.

## 4. Exact small-tau saturation lengths

The full per-depth enumeration yields zero prefixes with tau<=t and period>t at the following window lengths L_t:

    t      4   5   6   7   8
    L_t    9  11  15  17  21

Each L_t>=2t+1. Turn2's gluing proof works unchanged with window length L_t in place of3t, and proves tau=period for every word of actual tau=t and length>=L_t, over every finite alphabet and involution.

These thresholds are optimal, as shown by the following binary-swap gap words, all checked from the definitions in verify_turn5.py:

- t=4: 01001101, length8, period5
- t=5: 0100011101, length10, period7
- t=6: 01010010110101, length14, period9
- t=7: 0101000101110101, length16, period11
- t=8: the inverse parity transform of0^7 1^6 0^7, length20, period13

Each has actual tau=t and length L_t−1, so no smaller universal saturation threshold can work. Even-t witnesses also follow from Turn3's all-parameter family; odd-t witnesses here are exact finite certificates, with no asserted unbounded odd-family formula.

For t=1,2,3, the accepted prefix trees have no period>t instances at any enumerated depth at least t. Finite checks through2t combined with the2t+1-window gluing show that **tau=period unconditionally when tau<=3**, with no length hypothesis. This statement also follows directly for t=1 from Turn1.

The possible least-tau source counterexample from Turn4 must now have t>=9. All other restrictions remain, including n=3t for a least-tau example and p>=ceil((3t+2)/2).

## 5. Replay and stopping scope

Python3 standard library:

    python finite_window_fast.py --t 8 > /tmp/t8.json
    cmp TURN_5_ENUMERATION_T8.json /tmp/t8.json
    python verify_turn5.py

The checker cross-replays the fast implementation at t=1,...,7 against the earlier exact receipts, tests mask updates against literal definitions, verifies the completion recurrence and all lower witnesses, and compares the t=8 Python/C++ receipts. It does not replace the separate full t=8 rerun.

Optional independent C++17 replay:

    g++ -O3 -std=c++17 crosscheck_windows.cpp -o /tmp/windows_check
    set -o pipefail
    /tmp/windows_check 8 2> /tmp/t8_cpp.json | sha256sum

Compare the digest with TURN_5_CPP_STREAM_SHA256.txt and the stderr JSON with TURN_5_CPP_T8.json. No specialized solver or package is required. A SHA256 digest binds equality of complete deterministic streams; it does not independently establish the canonical-generation proof.

The fifth turn is now complete. No solution to the unbounded original conjecture is claimed. Independent full source/proof review is required before a final disposition or publication.
