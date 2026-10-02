# Turn 3: exact three-run classification and near-threshold families

Original conjecture unresolved. This turn gives a symbolic all-parameter classification in a restricted binary family. Let theta interchange0 and1. For a binary word w, define its parity-adjusted word z by z[i]=w[i] XOR(i mod2). A negative period p of w is an ordinary period of z when p is odd, and a complementing period of z when p is even. This follows by substituting w[i]=z[i] XOR(i mod2) in w[i+p]=1−w[i]. A factor starting at an odd position differs from its own local transform by global complementation, which preserves all these properties.

## 1. Periods of two and three runs

For z=0^a1^b with a,b>=1, there is no proper ordinary border. A proper complementing period p exists exactly when max(a,b)<=p<a+b: the compared prefix is all0, the compared suffix all1, and their common length a+b−p fits in both runs. Thus proper negative periods of w are exactly the **even** integers in that interval. Such a factor is theta-unbordered precisely when min(a,b)=1 and max(a,b) is odd.

For z=0^a1^b0^c with a,b,c>=1, its ordinary borders are exactly0^k for1<=k<=min(a,c). To see there are no others, a border containing1 must start its suffix in the first0-run, since its first symbol is0 and a suffix starting in the last0-run contains no1. A positive shift within the first run changes the location of the first1, preventing equality.

A complementing period p must start its suffix in the1-run (its first symbol is opposite the prefix's0) and end its prefix in the1-run (its last symbol is opposite the suffix's0). Hence p>=a,c, and the compared words have forms0^a1^{h−a} and1^{h−c}0^c, where h=a+b+c−p. They are complements precisely when a=h−c, so h=a+c and p=b. This works exactly when a,c<=b.

Therefore the proper negative periods of the transformed word are

    {a+b+c−k : 1<=k<=min(a,c), a+b+c−k odd}
    union {b : b even and a,c<=b}.                    (3.1)

This exact formula also handles overlapping borders. The full word length is always a vacuous period.

## 2. Complete classification when the middle run is even

Fix an even integer L>=2, let z=0^a1^L0^c, and put M=max(a,c). Then the exact pair(tau_theta, pi_theta^alt) of its inverse transform w is

    (L,L),                                  if M<=L;
    (L+2,2L+1),                             if M=L+1;
    (M+L+1−(M mod2), same value),            if M>=L+2.     (3.2)

Here “same value” means the two parameters are equal.

**Least period.** Formula(3.1) gives the even period L when M<=L; all odd candidates are larger. Otherwise, there is no even candidate. The least odd candidate is M+L if M is odd, and M+L+1 if M is even. If the smaller outer run has length1 and the latter candidate is the full word length, this is precisely the vacuous period. These observations give all the period values in(3.2).

**Maximal unbordered factor.** A factor of z has zero, one or two run changes. Constant factors transform to alternating words and contribute only length1. A two-run factor is theta-unbordered exactly when one run has length1 and the other odd, by the previous section. The maximum contribution of such factors is the smallest even integer at least max(a,L,c), namely2 ceil(max(a,L,c)/2).

A three-run factor necessarily contains the entire middle1^L and has form0^r1^L0^s, with1<=r<=a and1<=s<=c. If min(r,s)>=2, the ordinary-border range in(3.1) contains an odd period, so it is bordered. If min(r,s)=1 and R=max(r,s), the single ordinary candidate is R+L, which is odd when R is odd. If R is even and R<=L, period L is available. The only unbordered three-run factors thus have min(r,s)=1 and **R even, R>L**; their length is R+L+1.

If M<=L, the maximum is L. If M=L+1, no even R>L is available and the maximum two-run contribution is L+2. If M>=L+2, choose R to be the largest even integer<=M and take one position from the opposite outer run. This gives length M+L+1−(M mod2), dominating the two-run contribution. This proves the tau formula and completes(3.2).

Thus the cases with tau strictly below the least alternating period are **exactly M=L+1** in this entire three-run/even-middle family.

## 3. Sharp length within this restricted family

When M=L+1, tau=L+2 and

    n=a+L+c <= 3L+2 = 3tau−4,

with equality precisely when a=c=L+1. Consequently, for every even L>=2 the inverse transform of

    0^(L+1) 1^L 0^(L+1)

has

    n=3L+2, tau=L+2, pi_alt=2L+1>tau.                 (3.3)

These are rigorous all-L examples one letter longer than the corresponding asymmetric source family. They lie four letters below the conjectural3tau threshold and are **not** counterexamples to the source conjecture. Their ratio tends to3 from below; hence no coefficient strictly smaller than3 can replace3 in a universal asymptotic implication.

For the source word w_i=(01)^i011(01)^i001(01)^i0, its parity transform is0^L1^L0^(L+1) with L=2i+2. Formula(3.2) therefore reproves the source's exact all-i values n=6i+7, tau=2i+4, pi_alt=4i+5, as well as n=3tau−5. The original report deserves credit for that family and the asymptotic coefficient. No priority claim is made for the symmetric refinement or classification; the inaccessible thesis was not checked for overlap.

A naive one-sided extension instead gives0^L1^L0^(L+2). It contains0 1^L0^(L+2), an unbordered three-run factor of length2L+3, so it does not preserve the small tau. The symmetric refinement is not justified by padding alone.

## 4. Checks and remaining scope

verify_turn3.py checks900 two-run and18,000 three-run period formulas,1,536 complete tau/period classifications, and the displayed families through L=80 (with direct all-factor tau replay through L=30). There are20,616 assertions. The all-parameter proof is the run analysis above, not extrapolation from these controls.

Words with more run changes, multiple involution orbits, or general tau are not classified by this theorem. The original conjecture remains unresolved, with the all-alphabet tau<=7 theorem from Turn2 unchanged.
