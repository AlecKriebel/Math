# Verification controls and reproducibility

Run `python3 verify_exact_controls.py` from any directory and compare its JSON stdout with EXACT_CONTROLS.json. Only the Python standard library is used. No network, external package or source PDF is needed for replay.

The program passed 2,158 assertions using exact fractions. It checks seven rational parameters through generation six, compares depth-three recursion against enumeration of every one of the 2^7 gate assignments, checks submultiplicativity and the exact first/second-moment identities, and checks the decreasing-quantile moment inequality on 125 uniform five-atom laws. These finite tests do not establish the asymptotic theorem, compactness, Schauder's theorem, or a source result.

Five explicitly rejected shortcuts are retained:

1. Mean-only closure: at p=3/4, the laws X=1 and P(X=1/2)=P(X=3/2)=1/2 have equal mean one, but output means 7/4 and 27/16.
2. Reversed Jensen: m_1^2-m_2=p(1-p)^2>0 for 0<p<1, so the wrong reversed block inequality already fails at depth two.
3. Reciprocal second-moment bound: E X^2/(E X)^2>=1; replacing 1/(2p-1) by 2p-1 is false even for constant X and 1/2<p<1.
4. Constant eigenprofile: a deterministic unit input produces a two-atom law for 0<p<1 and cannot be a scalar multiple of itself.
5. Resistance substitution: two parallel unit edges have terminal distance one but effective resistance one half.

The universal proof is in PROOF_RECONSTRUCTION.md. Its proof dependencies are elementary probability, Jensen, the one-dimensional quantile/Wasserstein identity, Fekete, Helly/Vitali, and Schauder. The final critical-endpoint claim additionally invokes the precisely identified published Theorem 1. Those dependencies are distinguished from finite test coverage.
