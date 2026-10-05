# Exact target, proofs and finite certificates

## 1. Definitions and the full target

Let T_n have vertices all binary strings of lengths at most n. Its root is the empty string. Put W_0 = 1 and W_n = Aut(T_n), for n >= 1, with automorphisms fixing the root. Root restriction gives

W_n = (W_(n-1) x W_(n-1)) semidirect C2,

where the nonidentity element of C2 swaps the two factors. This is the imprimitive binary-tree wreath action, not the regular action of a large intermediate group. A word is a finite nonempty freely reduced string in x_1, x_1^-1, ..., x_k, x_k^-1. Its length counts individual letters, so powers are expanded. It is a law if every assignment of its variables to W_n evaluates to the identity. Coefficients from the group are not allowed.

Write L_(n,k) for the minimum law length in the free group F_k, and L_n = min_(k>=1) L_(n,k). Variables need not all occur. We distinguish these quantities because the original source does not specify a fixed rank, while the later formulation uses F_k. General results here hold for every finite rank. The depth-four exact computation is explicitly limited to F_2.

The target is to determine L_n, or at least its asymptotic growth, with the stronger proposed value L_n = 2^n. This report does not prove that equality for arbitrary n or a matching asymptotic lower bound.

## 2. Exponent and necessary conditions

**Proposition 1.** W_n has order 2^(2^n-1) and exponent exactly 2^n. Consequently L_n <= 2^n.

**Proof.** The order recurrence is a_n = 2 a_(n-1)^2, a_0 = 1, whose solution is stated. If g fixes the two root children, its order divides 2^(n-1) inductively. Otherwise g = (a,b)s and g^2 has sections ab and ba, both killed by 2^(n-1). Thus every element is killed by 2^n. Conversely choose a_(n-1) of order 2^(n-1). The root-swapping automorphism with sections (1,a_(n-1)) has square (a_(n-1),a_(n-1)) and hence has order 2^n. The power word x_1^(2^n) proves the upper bound. QED.

**Proposition 2.** If w is a law for W_n, then every exponent sum e_i(w) is divisible by 2^n. If also |w| < 2^n, all exponent sums are zero.

**Proof.** Assign an element of order 2^n to x_i and the identity to every other variable. The result is its e_i(w)-th power. The second assertion follows from |e_i(w)| <= |w|. QED.

In particular a law shorter than 2^n must have even length and each occurring variable appears at least twice. A shortest law can be chosen cyclically reduced: removing a nonempty conjugating prefix/suffix preserves lawhood and nontriviality while decreasing length. If L_n = 2^n it is also even, so L_n is even for all n >= 1. The natural embedding W_n -> W_(n+1) shows L_n <= L_(n+1). The propositions do not exclude words with every exponent sum zero, the main unresolved case.

## 3. Constructive linear lower bound

The following is Bradford's Proposition 6.4 with depth reindexed; the construction is replayed independently in `controls.py`.

**Proposition 3.** Every reduced word of length m has an assignment in W_m for which its m+1 prefix images of one leaf are distinct. Hence L_n > n.

**Proof.** Induct on m. Lift a separating assignment for the first m-1 letters by preserving a new final bit, initially zero. If the final image repeats, invert a variable if necessary so the last letter is x. Let v be the penultimate projected image. Modify x by swapping the two leaves above v immediately before its old action. Earlier positive x-edges never start at v. An earlier inverse x-edge can end at v only as the last prefix edge, forbidden by free reduction. Thus earlier images are unchanged, and the final image has last bit one. All images are distinct. QED.

For m <= n use the natural embedding W_m -> W_n. This lower bound is a known result, not claimed as new. For n >= 3 it combines with Section 5 to give L_n >= max(8, 2 ceil((n+1)/2)). No exponential lower bound is inferred.

## 4. Exact root-section criterion

Choose right actions. Write a variable assignment as

g_i : (b,v) -> (b xor epsilon_i, v acted on by h_(i,b)),

with epsilon_i in {0,1} and h_(i,0), h_(i,1) independently arbitrary in W_(n-1). For fixed epsilon and starting b, scan the letters of w while recording a state c, initially b:

- For x_i append the formal symbol h_(i,c), then replace c by c xor epsilon_i.
- For x_i^-1 first replace c by c xor epsilon_i, then append h_(i,c)^-1.

Freely reduce the resulting section word s_(epsilon,b). Its alphabet has up to 2k independent symbols.

**Proposition 4.** A word w is a law on W_n if and only if, for every epsilon in {0,1}^k and b in {0,1}, the final root state equals b and s_(epsilon,b) is a law on W_(n-1). Every word is a law on W_0.

**Proof.** Following a leaf through the product gives exactly the displayed state transition and the recorded section product. If all root states and sections are identities for arbitrary choices, the action fixes all leaves and therefore all vertices. Conversely, a changed root state already gives a counterevaluation, taking all sections to be identity. If a section is a nonlaw, choose its counterevaluation in W_(n-1), set unused sections to identity, and assemble the g_i. The lifted leaf is then moved. Independence of all 2k sections permits every such assignment. QED.

Free reduction and signed generator renaming preserve lawhood. The implementation memoizes those normal forms, tests all root bits when certifying a law, and recursively constructs a portrait when rejecting one. A nonlaw certificate is verified by separate leaf-permutation multiplication, without trusting the Boolean law result.

This exact recurrence does not itself prove the desired asymptotic. Section length need not decrease. For w = x y x^-1 y^-1, all eight formal sections, for the four choices of root bits and two starting bits, remain reduced of length four. For example, root bits (0,1) give x_0 y_0 x_1^-1 y_0^-1. Thus the unrestricted assertion that some literal nonempty section always has length at most |w|/2 is false. Further specializing sections can shorten words, but a general specialization preserving nontriviality and sufficient quantitative control has not been proved here.

## 5. Finite exact claims and coverage

**Proposition 5.** L_1 = 2, L_2 = 4, and L_3 = 8, allowing arbitrarily many variables.

The upper bounds are Proposition 1. Length one is not a law in any nontrivial group. For W_2 a shorter law would have zero exponent sums and positive even cyclically reduced length less than four. No such word exists. For W_3 the only remaining lengths are four and six, and at most three variables can occur.

Here is a complete signed-renaming enumeration of balanced cyclically reduced words at those lengths. Capitals denote inverses. A signed renaming assigns the first occurring variable x, the next new variable y, etc., and makes every variable's first occurrence positive.

| Word | Portraits for x,y,z (omit unused entries) |
| --- | --- |
| xyXY | 8,2 |
| xxyXXY | 48,1 |
| xyXXYx | 48,1 |
| xyXzYZ | 0,8,2 |
| xyyXYY | 8,17 |
| xyzXYZ | 0,8,2 |
| xyzXZY | 8,0,2 |
| xyzYXZ | 8,0,2 |

The leaf labels are 0,...,7 in binary order. Portraits are defined recursively in the code: root bit, left subtree block, right subtree block. For transparent hand checking, the permutations for the codes used are:

- 0: identity
- 1: (0 4)(1 5)(2 6)(3 7)
- 2: (0 2)(1 3)
- 8: (2 3)
- 17: sends (0,1,2,3,4,5,6,7) to (4,5,6,7,2,3,0,1)
- 48: sends (0,1,2,3,4,5,6,7) to (0,1,2,3,7,6,4,5)

Each listed evaluation moves 0 to 1. These are all tree automorphisms, as is also checked by recursive portrait reconstruction. Completeness of the list can be checked by appending an existing signed variable other than the inverse of the previous letter, or a new positive variable; retain exactly zero exponent sums and prohibit inverse first/last letters. This finite enumeration is implemented without heuristics. There is one word of length four and seven of length six. Together with the exponent and cyclic-reduction reductions, this proves the claim.

**Proposition 6 (computer-assisted finite claim).** L_(4,2) = 16.

For a hypothetical shorter two-variable law, cyclic reduction and Proposition 2 leave balanced words of even lengths 4,6,...,14. Signed-renaming enumeration produces respectively 1,3,27,190,1510,11851 words, a total of 13582. The program constructs an exact W_4 counterevaluation for every one, then independently verifies that its permutation on the 16 leaves is nonidentity. The canonical enumeration visits every remaining word, with no probabilistic pruning. The exponent gives the matching upper bound. The witness stream has a pinned SHA-256 in `CONTROL_RESULTS.json`; rerunning reconstructs it. No all-rank depth-four assertion or assertion for n >= 5 follows from this finite result.

For calibration, the recursive criterion is compared against direct exhaustive evaluation on all 64 ordered pairs in W_2, for every reduced F_2 word of lengths 1 through 6 (1456 words; rejection can stop at its first explicit counterexample). The separated-prefix construction is also checked on all those 1456 words. Every portrait of depths 1,2,3 is checked for inversion, permutation reconstruction and the power identity. These checks supplement, rather than replace, the proofs.

Two independent enumeration controls check coverage: brute-force reduced words on three fixed variables reproduce the eight depth-three canonical candidates, and a fixed-alphabet dynamic program reproduces every depth-four candidate count. In the latter check, the eight signed permutations of two variables act freely on balanced nonempty reduced words; fixing the first letter leaves a factor of two between the dynamic-program count and canonical count.

## 6. Central powers and a near-bound upper construction

Let z_n swap both leaves of every bottom sibling pair. Then z_1 is the nonidentity element of C2 and z_n = (z_(n-1), z_(n-1)). It is central: it commutes with each section by induction and with the root swap because its sections agree.

**Proposition 7.** For every g in W_n, g^(2^(n-1)) belongs to {1,z_n}.

**Proof.** For n=1 the assertion is immediate. If g fixes the root children, the exponent bound on its sections makes the indicated power identity. If g=(a,b)s, its square has sections ab and ba. Inductively their 2^(n-2)-nd powers lie in {1,z_(n-1)}. Since ab and ba are conjugate and those two values are central, the values agree. This gives either (1,1) or (z_(n-1),z_(n-1)), as asserted. QED.

Consequently x^(2^(n-1)) y x^(-2^(n-1)) y^-1 is a nonempty reduced law of length 2^n+2. This explicit commutator construction misses the power-law upper bound by two letters and cannot disprove its optimality. The controls verify the power conclusion on all 32906 portraits at depths one through four and check the resulting law by the exact recursive criterion.

Solvability alone also does not close the gap. Inductively W_n has derived length at most n: its quotient by W_(n-1)^2 is abelian. The balanced derived word delta_0=x and delta_(j+1)=[delta_j on one variable block, delta_j on a disjoint block] is nontrivial, has length 4^(j+1), and takes values in the (j+1)-st derived subgroup. Thus delta_n is a law of length 4^n, larger than 2^n. These are upper constructions only.

## 7. Exact remaining gap

The unproved assertion is that every nonempty reduced balanced word of length less than 2^n admits a counterevaluation in W_n, uniformly in n and the number of variables, or some replacement lower bound determining the asymptotic. The recursive criterion characterizes that requirement exactly but does not bound the length of its first law sharply. The finite computations and central-power structure do not supply this missing uniform argument. No full solution or novel general bound is claimed.
