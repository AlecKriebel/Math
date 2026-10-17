# Independent acceptance: exact swap and cyclic-four ray-valued symbols

14 October 2026 UTC. Row1777 /30005572. Review within shared PASS4/5, with no additional mathematical pass. No author proof, ledger, queue, or remote was edited.

## Verdict and frozen inputs

ACCEPT the following corrected restricted results:

- `pass4_symbol_calibration/EXACT_SWAP_AND_CYCLIC_FOUR.md`, SHA-256 `66165ae9b3288126e9906221329a7d7f896afdd5e4808058fcb54998414e669f`.
- `pass4_symbol_calibration/CYCLIC_FOUR_RAY_FIELD_DESCENT.md`, SHA-256 `01ca846cb333132e0c6e31f24597940513b8b2b76563f0a3857faf3555fc3f9d`.

The second input supersedes the first note's earlier marked-field limitation only for its explicitly stated cyclic-four, fixed same-curve/principal-component construction. It does not supply the missing geometric absolute calibration or all-component assembly.

Accepted conclusions are: an exact constant-sensitive swap-cocycle formula with declared Gersten sign; the exact moved-primitive relation identifying the uncomputed shear transitions; a full relative theta map for the stated cyclic-four component from an explicit K2 cusp potential; actual ray-field coefficients obtained by descending K1 entries before forming symbols; and a nonzero relative value in the -23 example. The absolute restriction of that relative map is zero, and its equality to the independently constructed geometric absolute map is unproved. The original full construction remains UNSOLVED.

## 1. The swap equality genuinely removes constants

For Z={f(x),f(y)}, the displayed separated-variable Gersten expansion gives d_std Z=w eta−eta. This alone would only identify a residue. The additional transfer calculation is decisive: factor simultaneous alpha multiplication into the two separate-coordinate maps and use the projection formula twice. The norm in one coordinate acts on its own function entry, while the other entry is pulled back from the target. Thus

[alpha,alpha]_*Z={Norm_alpha f,Norm_alpha f}=Z

for alpha prime to the auxiliary ideal, with no extra degree factor.

This proves eventual trace invariance, and literal T5-invariance when the auxiliary is prime to5. The accepted uniqueness theorem therefore proves Z is exactly the normalized swap value, including constants. In the alternative unramified-five CM case, the already accepted unquotiented trace-fixed uniqueness applies even to auxiliary(5). These two ranges are correctly kept separate.

The formula for g followed by the swap follows from the actual cocycle equation and the row-coordinate pullback action. It does not create an automorphism swapping nonisomorphic factors; the product is E×E or has an explicitly chosen factor identification.

## 2. The repaired sign label matters for source calibration

The initial draft called u·div(v)−div(u)·v the reciprocal of the displayed standard tame symbol. That label was wrong: at a divisor of u, both formulas give a negative exponent onv. The final draft corrects the label and explicitly translates to Sharifi–Venkatesh equation(2.4).

With eta fixed, the inverse-tame source cocycle is the negative of the standard-tame cocycle. Thus the positive standard swap value is {f(x),f(y)}, and the corresponding source-sign value is its negative. These are not silently equated. The separate GERSTEN_SIGN_TRANSPORT_ADDENDUM gives the chain isomorphism and identifies the comparisons it affects.

This is not a cosmetic issue for a prescribed theta edge. The acceptance retains the fixed sign in every local symbol calculation and leaves the edge-to-cocycle orientation comparison as part of the unresolved calibration.

## 3. Only regular differences are specialized

When both lower coordinates are nonzero moduloN, the two entries of the translated product are units at(0,P). The difference Theta(gw)−Theta(g) is therefore regular and specializes to the stated genuine theta pair. Its separate summands need not be regular there.

Similarly the moved-primitive identity

Theta_(mu eta)(gamma)=Theta_eta(gamma mu)−Theta_eta(mu)

is exact, but it does not permit evaluating and cancelling Theta_eta(mu) separately at a point on its residue support. The draft explicitly retains the uncomputed elementary shear steps between general ordered bases. Knowing the swap transitions does not compute all those steps or the actual moved arithmetic cocycle.

## 4. The cyclic-four K2 potential is exact

When O/N=Z/4, the nonzero primitive orbit has two even theta values A=theta(P)=theta(−P) and B=theta(2P). The three admissible pair types are(A,A),(A,B),(B,A). Since2 is inverted, {A,A}=0. Their symbols are exactly0,Q,−Q for Q={A,B}.

Therefore the edge symbol is the difference of the endpoint potential epsilon(c)Q, where epsilon is0 on odd denominators and1 on denominator2. This is an equality in K2 itself, not just in a residue group or after a regulator.

A primitive O-vector representing a principal cusp is unique up to a global unit; those units have image±1 moduloN and preserveepsilon. Strict Gamma1 preserves the denominator moduloN, and adjoining central units does not changeepsilon. The potential is consequently well-defined on the represented allowed cusp orbits. The proof does not assume every cusp is represented.

Extending the potential to all allowed cusps and composing with the relative boundary produces an actual map on full H1(X,C;R). No generation theorem for unimodular edges is needed. The map vanishes on absolute homology because it factors through the boundary, while taking exactly the prescribed genuine theta values on the represented admissible edges. The remaining criterion for extending an independent absolute map is precisely its vanishing on represented balanced absolute chains, using the previously accepted saturated-edge criterion.

## 5. Ray-field coefficients are obtained before K2

The ray class exact sequence gives F(N)=H because the global units already surject onto(Z/4)^×. No class number or extension degree is divided.

For an H-model of the chosen CM class, all O-endomorphisms are H-defined. Hence Galois_H acts O-linearly on the rank-one O/N-module E[N], and carriesP only toP or−P. The concrete even rational function

g5=Delta^2/psi5

is defined overH. Therefore g5(P) and g5(2P) are literal elements ofH^×: x(P) is H-rational and2P is H-rational. The normalized comparison with the Robert/Kato function is the previously accepted one, including its harmless twelfth-root convention, not a fresh inference from matching divisors.

The definitions theta(P)=g5(P)/24 and theta(2P)=g5(2P)/24 in additive K1 tensor notation use only allowed division. Now Q={g5(P),g5(2P)}/576 is formed directly inK2(H) tensorR. No claim that Galois-invariant K2 classes automatically descend occurs anywhere in this argument.

Model independence follows from the equal weight24 scaling ofDelta² andpsi5 and the previously proved pointed CM functoriality. Replacing the primitive point by its only alternative−P has no effect. This does not compare different CM isomorphism classes or the distinct two factors of a general component E_r×E_1.

## 6. Nonzero ray-field value and the normalization factors

In the-23 example, N=q², w is2 moduloq², and the matrix with rows(0,−1),(1,w) has determinant1. Its endpoint denominator types are1 and2, hence its theta value isQ. Both endpoints are allowed and cannot be identified underGamma1 becauseepsilon is invariant.

The explicit H-valued g5 entries compare with the accepted good local model by O-linear model functoriality. Their equality is already an equality inK1 over the local baseK: one checks it in a common extension and uses injectivity of field-unit inclusion. There is no claim of K2 restriction injectivity. The known local tame symbol ofQ is j-bar² of order7, so the globalQ cannot be zero.

The finite factors and residue exponents check: raw576, mixed48, three-term624; their standard tame images overK are respectively j-bar⁴,j-bar⁵,j-bar². Passing to the ramified quadratic marked field squares these residues. The positive raw and smoothed edge values genuinely differ, but each is a multiple of the exact same potential, so their balanced cycle sums are both zero. This does not identify either cycle assignment with the geometric absolute map.

## 7. Reproducibility and scope boundary

The complete corrected main proof, ray-descent addendum, normalization-source addendum and retained local residue proof were inspected. The author's finite checker was read and replayed under ordinary Python,-O,and-OO; its explicit failure checks remain active and the outputs agree. Replays are retained in this audit directory. They check the Gersten coefficient expansion, cyclic-four pair table, unit/congruence invariance, finite graph telescoping and residue exponents; they do not certify K-theory transfer or global homology generation.

The source sign in Sharifi–Venkatesh(2.4), the LSSW shifted primitive and CM-model statement, and the previously verified Robert normalization were checked at their stated scope. Public sources: https://math.ucla.edu/~sharifi/eisensymbol.pdf and https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf .

No general CM divided-power construction has been revived. No odd-level unpowered triangle, all-component potential, arbitrary theta root, or full comparison with the source's auxiliary arithmetic map is asserted. The requested construction remains UNSOLVED.
