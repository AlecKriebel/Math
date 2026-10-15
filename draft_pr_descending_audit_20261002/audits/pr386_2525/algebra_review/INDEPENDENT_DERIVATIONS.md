# Independent Turn 1–4 derivations (before previous-review comparison)

Inputs: PR386 frozen head 76d804cffb0cdbd2c88416dad1ead6e2a89989d6, bound by INPUT_BINDINGS.json. Primary Bergman pages 4–6 read first. All lengths include the empty word. In this note, bounded means a finite bound depending on the generating set.

## 1. Inverse cost and subgroup exhaustion

For genuine positive S, all l_S(g) are finite. Put D=sup_G l_S, R=sup_{s∈S}l_S(s^{-1}), and d=diameter for ±S. Always R≤D. If R<∞ and d<∞, replacing inverse letters gives D≤d max(1,R). Conversely D<∞ forces R<∞. For a CB group d exists for the fixed S, but that same-set finiteness alone does not suffice for the exhaustion argument.

A_n={g:l_S(g)≤n,l_S(g^{-1})≤n} is symmetric; its subgroup H_n is increasing and their union is G. If H_n=G, CB applied to A_n gives G=A_n^k and D≤nk. If G=<H_n∪F> for finite F, every f and f^{-1} lies in some common A_m, m≥n, so H_m=G. Conversely H_n=G gives finite supplementation with F=∅. Hence a CB/non-MB witness forces all H_n proper and not finitely supplementable; finite index would provide a finite set of right representatives whose addition generates G, contradiction. Repeated subgroups and n=0 cause no issue; the trivial group is immediate.

Finite generator orders bounded by e imply l_S(s^{-1})≤e−1. A bounded exponent is sufficient but stronger than required; torsion without a uniform bound is not sufficient for this proof. Identity-only S in the trivial group yields R=D=0. S empty is also legitimate only in the trivial group, and then one should define R=0 rather than a maximum over ∅.

The Z control S=N_0∪{−1} has l(n)=1 for n>0 and l(−n)=n, with d=1, H_1=Z. It demonstrates why CB must quantify over all generating sets: {1,−1} has infinite diameter.

## 2. Positive Schreier transport and a strong normal kernel

For arbitrary finite-index H≤G (normality unnecessary), right multiplication acts on right cosets Hg. Genuine positive generation makes this finite directed graph strongly connected. A shortest positive path to any coset has no repeated vertices and length≤m−1. Choose r_H=1, representatives r_C with lengths≤q, and c=max_C l(r_C^{-1}). The latter finite bound follows from finite many representatives and positive generation, not from m−1. T={r_C s r_{Cs}^{−1}} lies in H; following a positive word for h∈H telescopes into T letters with no T inverses. Thus T positively generates H and every T letter has ambient cost≤q+1+c. MB of H gives H=T^{≤k}; g=h r_C has cost≤k(q+1+c)+q.

Both CB and MB pass to quotients: lift each quotient letter and add all kernel elements as letters. For a strongly bounded subgroup N (CB plus condition (3)), E_n={x∈N:l(x),l(x^{-1})≤n} exhausts N. Condition (3) makes some <E_n>=N; CB of N then bounds ambient l on N. This does not require S∩N to generate N, N normal, or N finite; for symmetric ambient lengths the same argument works. Normality is needed to form the quotient and the final extension comparison.

For N◁G strongly bounded, C=sup_N l<∞. A shortest quotient word lifts to w and g=w n with n∈N. Therefore l_Q(gN)≤l(g)≤l_Q(gN)+C. Applying this to every positive/symmetric generating set proves G has MB/CB iff G/N has the respective property. Replacing strong boundedness by MB alone leaves the ambient-cost step unproved. This route remains blocked unless a new mechanism gives that bound.

## 3. Finite quotient versus genuine finite action

For H◁G with finite quotient Q and an arbitrary section r_1=1, define alpha_q(h)=r_q h r_q^{-1} and c(q,t)=r_q r_t r_{qt}^{−1}. In general alpha is not an action: alpha_q alpha_t=Inn(c(q,t)) alpha_{qt}. Section defects obey c(q,t)c(qt,u)=alpha_q(c(t,u))c(q,tu). A general finite extension must retain these constants; Q finiteness is not finiteness of the induced collection of automorphisms under composition.

With S positively generating H and W=S∪{r_q}, W positively generates G. Reading W in state h r_q emits alpha_q(s) or c(q,t) and ends with r_1 for h∈H. Thus l_T(h)≤l_W(h), T=∪alpha_q(S)∪{c(q,t)}. Since b=max l_W(r_q^{-1}) is finite, each T letter has W cost≤2+b and l_W(h)≤(2+b)l_T(h). This is a metric comparison for this W, not an equivalence with Q-invariant sets for an arbitrary nonsplit extension.

For a split semidirect product, alpha is an actual Q-action and c=1. The section inverses are section letters, so B=3. If S is invariant, moving section letters right turns any W word for h∈H into an S word with no greater length; inclusion gives equality l_W(h)=l_S(h), and the symmetric analogue. For arbitrary positive X generating G, positive Schreier T generates H and has X cost≤a+1+b. Its Q-saturation has X cost≤2a+2b+1 and still positively generates H. MB_Q(H) bounds H in this invariant set and the finite final section costs bound G. The same argument with symmetric lengths proves CB_Q. Forward directions use exact metric equality for invariant S. Hence CB(G)⇔CB_Q(H) and MB(G)⇔MB_Q(H) for finite semidirect products only as stated. Faithfulness of the action is not required; Q=1 reduces to the original properties, and H=1 is finite.

In the infinite dihedral control, S=N_0 rotations plus r^{-1}; inversion saturation is every rotation. W=S∪{t} has rotations of cost≤3 and reflections≤2. A two-letter rotation either has exponent≥−2 from S+S or is t²=1; r^{-3} costs exactly3. This is a genuine infinite computation. The standard finite generating set gives unbounded symmetric length, so it supplies no CB example. Finite cyclic wrap-around cannot replace this proof. TURN_3_CONTROL_CLARIFICATION correctly distinguishes its integer normal-form windows from finite subset scans; Turn4's finite checks concern only the local r^{-3} equality.

## 4. Finite normal generation and uniform conjugator costs

If finite F normally generates a CB group, U=conjugates of F∪F^{-1} is symmetric and group generates G. CB gives G=U^{≤b}. For conjugation-invariant positive S, conjugating a shortest word and conjugating back proves l(hgh^{-1})=l(g). Genuine generation gives finite C=max_F(l(f),l(f^{-1})); every U letter costs≤C and D≤bC. More generally l(hsh^{-1})≤K for all h and s∈S gives D≤bKC by conjugating fixed positive words for f and f^{-1}. A separating witness in this class must have unbounded positive costs in at least one conjugacy family for every finite normally generating F. Full saturation may reduce costs and cannot certify the original S.

If each s^{-1} is a product of≤k conjugates of positive S letters using a fixed finite conjugator set F, let C=max_{f∈F}(l(f),l(f^{-1})); each factor costs≤2C+1. Thus R≤k(2C+1) and D≤d max(1,k(2C+1)). The same reasoning handles finitely many exceptional generators. F=∅ only allows the empty product and identity generators, so C=0 and the trivial case is harmless. A finite relation length alone, with unbounded-cost conjugators, does not suffice; individual finite-order or generalized-torsion relations without uniform constants do not suffice.

## Initial independently reconstructed judgment

No invalid deduction found in Turn1–4 under their explicit hypotheses. These are scoped reductions. All CB/non-MB existence, all-invariant-set classification, arbitrary MB-kernel extension closure, and uncontrolled conjugacy routes remain unsupported. No finite checker certifies CB in an infinite group. Independent adversarial controls and checker-scope inspection are still pending. Prior final_review and verdict metadata have not been read.
