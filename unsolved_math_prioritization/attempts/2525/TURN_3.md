# Turn 3: a complete finite-action reduction and a destroyed witness

## Direction

Khelif's announced CB group with a non-CB index-two subgroup does not itself answer the target. We examine exactly what happens to a positive generating witness on a subgroup when a finite symmetry is adjoined. The result is an exact characterization for finite semidirect products and an explicit example showing how a genuinely unbounded positive witness can disappear. No target example is obtained.

## 1. Positive normal forms in a finite extension

Let H normal in G have finite quotient Q. Fix representatives r_q, with r_1=1. Suppose S monoid-generates H and put W=S union {r_q:q in Q}. This monoid-generates G. Define

    alpha_q(s)=r_q s r_q^{-1},
    c(q,t)=r_q r_t r_{qt}^{-1},
    T=union_q alpha_q(S) union {c(q,t):q,t in Q}.

The set T is contained in H and monoid-generates H because it contains S. For h in H its positive word metrics satisfy

    l_T(h) <= l_W(h) <= B l_T(h),                 (1)

for some finite B depending on W and the chosen representatives.

For the first inequality, maintain a normal form h r_q while reading a W word. Multiplying by s in S replaces h by h alpha_q(s), with q unchanged. Multiplying by r_t replaces h by h c(q,t), with quotient state qt. At most one T letter is emitted per input letter. For a word ending in H the final quotient representative is1. This proves the lower bound, including identity letters and the empty word.

For the upper bound let b=max_q l_W(r_q^{-1}), which is finite because Q is finite and W positively generates G. Every displayed alpha or c has W length at most2+b. Thus B=2+b works. Every g=h r_q has l_W(g)<=l_W(h)+1. Consequently W has unbounded positive diameter on G exactly when T has unbounded positive diameter on H.

This is the precise missing test for a finite-extension construction: the witness must survive **all finite conjugate copies and the factor-set constants**. Its unboundedness for S alone is insufficient.

## 2. Finite semidirect products: necessary and sufficient properties

Now let a finite group Q act on H by automorphisms alpha, and let G=H semidirect Q. Use the subgroup transversal r_q=(1,q), so every c(q,t)=1. Write S^Q=union_q alpha_q(S). Formula(1) specializes to

    l_{S^Q}(h) <= l_{S union Q}(h) <= 3 l_{S^Q}(h),   (2)

because the inverse of each quotient letter is again one quotient letter. If S is Q-invariant, moving quotient letters to the right gives the stronger equality

    l_{S union Q}(h)=l_S(h),  h in H.             (3)

The analogous statement holds for group word lengths, using symmetric letters.

Define CB_Q(H) to mean: every Q-invariant group-generating subset of H has finite group-word diameter. Define MB_Q(H) using Q-invariant monoid-generating subsets and positive words. Then

    G is CB iff CB_Q(H);
    G is MB iff MB_Q(H).                         (4)

**Forward implications.** Given an invariant generating set S, adjoin Q. Finite diameter in G restricts to finite diameter in H by(3), in the respective positive or symmetric version.

**Reverse MB implication.** Let X be any monoid-generating set of G. All finitely many r_q and r_q^{-1} have finite X lengths, bounded respectively by a and b. Positive Schreier rewriting from turn2 yields a monoid-generating set

    T={r_q x r_{q pi(x)}^{-1}:q in Q,x in X}

of H, with every element having X length at most a+1+b. The Q-saturation T^Q is invariant, still positively generates H, and each of its elements has X length at most2a+2b+1. MB_Q(H) bounds H in this set; adjoining a final r_q bounds G in X. X was arbitrary.

**Reverse CB implication.** Apply the same argument to the symmetric generating set X union X^{-1}. The Schreier generators and their conjugates have uniformly bounded ordinary X length. CB_Q(H) bounds their symmetric word diameter and hence that of G. No uncountable-cofinality assumption is used in(4).

Thus the finite semidirect route is exactly the search for H,Q such that CB_Q(H) holds but MB_Q(H) fails. It cannot be justified by CB of the extension alone plus an arbitrary nonsaturated witness on H. This reduction does not assert existence of such an invariant witness.

## 3. An explicit witness destroyed by an involution

Let H=<r> be infinite cyclic. Let S={r^n:n>=0} union {r^{-1}}. Its positive length at r^{-m} is m, so it is unbounded, while its symmetric diameter is1. Let Q=C2 act by inversion and write the infinite dihedral extension as

    G=<r,t : t^2=1, t r t=r^{-1}>.

The saturated set S^Q is all of H. With W=S union {t}, every nonnegative rotation is one letter, every negative rotation is t r^m t (at most3 letters), every nonnegative reflection is r^m t (at most2), and every negative reflection is t r^m (at most2). Therefore W has diameter at most3; r^{-3} needs3 letters, since a two-letter rotation is either a sum of two S exponents (at least-2) or t^2=1. Its diameter is exactly3.

This is an actual infinite positive-generation calculation, not a finite cyclic approximation. G is not CB: the finite symmetric generating set {r,r^{-1},t} has finite balls and G is infinite. The example isolates the loss of the proposed witness without claiming a target solution. It also illustrates why freely adjoining inverse-producing symmetries tends to erase the required positive asymmetry.

## 4. Controls and remaining gap

The checker considers every positive generating subset of C_n for3<=n<=12, adjoins an inversion involution, constructs the dihedral multiplication table, verifies(2) for all rotations and(3) for every invariant generating set, and checks the uniform finite normal-form upper bound for all group elements. It additionally verifies the exact three-letter calculation in sufficiently large finite dihedral examples as a control of the stated infinite normal form. Finite cyclic wrap-around is never used to prove the infinite claim.

The finite-action criterion shifts the challenge to a Q-invariant genuinely positive witness while retaining the all-invariant-generating-set symmetric boundedness. We have neither constructed such a pair nor shown it impossible. Three genuine directions have now been completed; the next tests conjugacy and normal-generation routes which might force the missing inverse bounds.
