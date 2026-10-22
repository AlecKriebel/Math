# Prime-power residues, integral target components, and the remaining cusp identity

Shared PASS2/5, absolute-integrality lane. Row 1777 / 30005572. 14 October 2026 UTC.

## Status and scope

This is a proved restricted integrality theorem and an exact reduction of the remaining arithmetic obligation. It does not construct the original map. We use the existing LSSW auxiliary maps over R5 = Z[1/30], or their existing p-components for p >= 7. None of the results supplies the missing 5-primary construction, the full relative theta prescription, the bad-level Hecke identity, or unrestricted compactification.

The main additional conclusion is stronger than the observation that a finite residue-field unit group has order prime to its characteristic:

> At level N = q^n, the entire arithmetic residue module is canonically the residue module of the Hilbert class field at q. It is independent of n. Its exponent is (Nq)^f - 1, where f is the order of the ideal class [q] in Cl(F). Its possible LSSW prime-to-p character support consists exactly of characters chi descending to Cl(F) with chi([q]) congruent to Nq modulo p. The full p-group module structure is retained.

Thus the actual existing maps have the integer-ring target on every component outside this explicitly identified support. The surviving support is a real nonzero quotient of K2 of the localized ring in examples, but we do not prove that the LSSW map hits it.

All h class-group components of the Bianchi source are retained. The prime ideal q need not be principal. The expression [q] below is an ordinary ideal class, never the nonexistent ray-class ideal q at modulus q^n.

## 1. Conventions and source inputs

Let F be an imaginary quadratic field, O its maximal order, H its Hilbert class field, q a nonzero prime ideal, and N = q^n with n >= 1. Put

- Q = Nq = |O/q|, and ell = char(O/q);
- L = F(N), A = O_L, A_S = O_L[1/q];
- G = Gal(L/F), C = Gal(H/F) = Cl(F);
- I the inertia subgroup in G at any prime over q;
- f = ord_C([q]);
- T_q(L) = direct sum over v|q of k_v^times, with its natural G-action.

Since G is abelian, I is independent of the selected v. We use additive notation for T when treating it as a module, and multiplicative notation for individual tame symbols.

Arithmetic Frobenius acts on k_v as x -> x^Q. Write kappa_q for the arithmetic Frobenius in C at q. Under arithmetic Artin reciprocity kappa_q corresponds to [q]. If eta in a decomposition group D_v is any lift of kappa_q, then eta acts on k_v as x -> x^Q; changing eta by I has no effect. We do not write R_N(q).

The LSSW convention matches this orientation. In §4.3, author PDF p.34, the cyclotomic character composed with R_N is explicitly identified modulo p with the norm character. The chi-component there is the quotient imposing g = chi(g), not g = chi(g)^(-1). The K2 action in Proposition 5.1.2 is the direct field-automorphism action R_N(a). Lemma 3.1.4 likewise uses R(d)P = [d]P. Our support condition is therefore chi(kappa_q) = Q modulo p. If one rewrites all notation using inverse Artin reciprocity, the ideal-class argument of chi must be inverted.

We use these established inputs, not newly proved claims about the intended construction:

1. LSSW Proposition 4.2.4 and §5.1 provide the actual auxiliary map cPi_N: H1(Y1(N), R5) -> K2(A_S) tensor R5, when O^times -> (O/N)^times is injective. Its domain includes all h components.
2. LSSW Theorem 4.3.3 and (5.2) provide the unaugmented p-character maps where their hypotheses hold, with the stated smoothing calibration. Compactification, when needed, is a separate use of Theorem 5.2.9.
3. The number-ring K2 localization sequence, finite-field K2 vanishing, and SK1(A) = 0 give the exact sequence in §2. These standard facts are recorded respectively in Weibel, III.6.5, III.6.1.1, and III.1.3.6.
4. Class field theory identifies the ray kernel with local inertia. The ray exact sequence is Milne, V.1.7; local reciprocity and its compatibility with global reciprocity identify the image of O_q^times with I. Alternatively, I = Gal(L/H) follows directly from the maximal-unramified-field argument in §3.

Primary-source and author-hosted references are listed in SOURCES_AND_VERIFICATION.md. Existing LSSW assertions are used at their advertised scope, not independently re-proved here.

## 2. The exact target obstruction

### Proposition 2.1 (arithmetic localization)

There is a natural G-equivariant short exact sequence

0 -> K2(A) -> K2(A_S) --tau_S--> T_q(L) -> 0.                 (2.1)

The same remains exact after tensoring with Z[1/6], R5, or Z_p. In particular, for any module B over one of these flat coefficient rings R and any map Phi: B -> K2(A_S) tensor R, there is a unique lift

Phi_int: B -> K2(A) tensor R

if and only if (tau_S tensor R) Phi = 0.

Proof. The localization sequence for the closed set S contains

sum_v K2(k_v) -> K2(A) -> K2(A_S) -> sum_v K1(k_v) -> K1(A) -> K1(A_S).

Each K2(k_v) is zero and K1(k_v) = k_v^times. For number rings and their localizations, K1 is the unit group, so K1(A) -> K1(A_S) is injective. This proves (2.1). All three coefficient rings are flat over Z. Exactness gives both the lift criterion and uniqueness. Naturality of valuations gives G-equivariance. QED.

Our tame-symbol convention is

tau_v{a,b} = (-1)^(v(a)v(b)) overline(a^(v(b))/b^(v(a))).    (2.2)

Inverting this convention inverts every displayed multiplicative residue and does not change a kernel, support condition, or vanishing claim.

A compactified map valued in K2(A_S) does not automatically have zero residue. Compactification kills a topological boundary subgroup in the source; (2.1) measures a different, arithmetic boundary in the target. A bridge between these boundaries is additional mathematics, isolated in §7.

## 3. The Hilbert-class-field residue theorem

### Theorem 3.1

For every n >= 1,

(a) I = Gal(L/H), and every prime of H above q is totally ramified in L/H.

(b) Reduction induces canonical identifications k_w = k_v for the unique v of L above each w|q in H. Each has Q^f elements. Consequently there is a canonical G-equivariant isomorphism

T_q(L) = inflation_C^G T_q(H),                             (3.1)

and, as C-modules,

T_q(H) = Ind_<kappa_q>^C F_(Q^f)^times,                    (3.2)

where kappa_q acts on F_(Q^f)^times by x -> x^Q.

(c) The exponent of T_q(L) is exactly m_q = Q^f - 1. There are h/f cyclic summands of that order. In particular the residue module, including its action through C, is independent of n.

Proof. The ray field L is unramified away from q. Since L/F is abelian, inertia at all primes over q is the same subgroup I. The field L^I is therefore unramified at q and at all other finite primes. F has no real primes. Hence L^I is contained in H, the maximal everywhere-unramified abelian extension of F. Conversely H is contained in L, and I acts trivially on H because H/F is unramified. Thus L^I = H and I = Gal(L/H).

The decomposition subgroup D_v contains I. The inertia subgroup for L/H is therefore all of Gal(L/H), so a prime of H has just one prime above it in L and the extension there is totally ramified. Their residue fields agree canonically.

In H/F, q is unramified with decomposition subgroup generated by its arithmetic Frobenius kappa_q. Its order is f, so the residue extension has degree f and residue cardinality Q^f. Its h/f conjugate primes give (3.2): the stabilizer acts on the field unit group through the indicated Frobenius, and the rest of C transports the summands. The multiplicative group of a finite field is cyclic. This proves (b) and (c). QED.

This proof uses no generator of q, no choice of principal representative for [q], and no class-number-one assumption. A chosen local uniformizer is also unnecessary.

After choosing a generator of the multiplicative group of one residue field, (3.2) also gives the noncanonical but explicit presentation

T_q(L) = Z[C] / (kappa_q - Q), inflated to G.              (3.3)

Indeed, the relation kappa_q = Q around its length-f orbit imposes Q^f - 1 = 0. Choosing representatives for C/<kappa_q> leaves h/f independent cyclic summands, exactly those of (3.2). Only this presentation's choice of cyclic generator is noncanonical; the residue identifications (3.1) remain canonical.

### Corollary 3.2 (integer target away from the finite obstruction)

For p not dividing m_q,

K2(A) tensor Z_p -> K2(A_S) tensor Z_p

is an isomorphism. More generally, it is an isomorphism after coefficient localization inverting all prime factors of m_q. In particular it is an isomorphism on the ell-primary part.

Over R5, the obstruction has exponent equal to the largest divisor of m_q prime to 30. Over R = Z[1/6], its exponent is the largest divisor prime to 6. Thus equality over R5 does not certify equality over R when 5 divides m_q.

Proof. Tensor (2.1) and use Theorem 3.1. Since Q is an ell-power, ell does not divide Q^f - 1. QED.

Corollary 3.2 applies to every homomorphism into the localized group, including the existing auxiliary map on Y, before making any compactification assertion.

## 4. Exact prime-to-p character support

Fix an odd prime p != ell. Write G = G_p times G', with G' of order prime to p. Let chi: G' -> O_chi^times be a p-adic character, extended trivially to G_p as in LSSW §4.3. Its component means the quotient by g = chi(g) on G'. Write bar_chi for reduction modulo p. Set a = v_p(Q^f - 1).

### Theorem 4.1

If a = 0, then T_q(L)^(chi) tensor Z_p = 0 for every chi. If a > 0, then

(T_q(L) tensor Z_p)^(chi) != 0                            (4.1)

if and only if both of the following hold:

1. chi is trivial on I (equivalently on I intersect G'), and hence descends to a character chi_C of C;
2. bar_chi_C(kappa_q) = Q in the residue field of O_chi.

This criterion concerns the actual direct Galois action on the target. There is no inversion of chi.

Proof. Equation (3.1) shows that I acts trivially. If chi is nontrivial on I intersect G', choose i there with chi(i) != 1. The scalar chi(i) - 1 is a p-adic unit, since chi(i) is a nontrivial prime-to-p root of unity. In the chi-quotient, this scalar kills the module; hence the quotient is zero.

Now suppose chi descends to C, and use (3.2). Put C = C_p times C', J = <kappa_q> = J_p times J', and f = p^b f_0 with p not dividing f_0. The p-part of F_(Q^f)^times is a cyclic group V of order p^a. The generator kappa_q acts on V by multiplication by Q, when V is written additively.

Over O_chi, V becomes O_chi/p^a. A generator of J' acts on this module by a prime-to-p-order scalar. Such a scalar is uniquely determined by its residue modulo p, since reduction is injective on prime-to-p torsion in (O_chi/p^a)^times. The restriction of chi to J' either equals this action, or differs by a unit on some element and kills the quotient.

The p-part J_p acts trivially modulo p. Consequently agreement on J' is equivalent to bar_chi_C(kappa_q) = Q modulo p. If they agree, no relation from J' kills V. Induction from J_p to C_p is nonzero (it is free on a coset set over V), so the chi-component is nonzero. Conversely, disagreement forces it to be zero. QED.

For precision, in the nonzero case the underlying O_chi-module is

(O_chi/p^a)^(|C_p| / |J_p|).                              (4.2)

Its C_p-action is the induction of the actual action of J_p on V; it need not be trivial. Formula (4.2) follows by choosing coset representatives in the preceding proof. We have not silently averaged over the p-part of the class group.

Important scope: chi here is a character of G', not an arbitrary p-adic character of all of G. The theorem does not assert vanishing from ramification only through p-power inertia. The scalar zeta_p - 1 is not a p-adic unit. For example, let I = C_p act trivially on M = F_p and twist by a faithful character with value zeta_p over O = Z_p[zeta_p]. Then

M tensor_(Z_p[I]) O = O/(p,zeta_p-1) = F_p,

which is nonzero. The integral support theorem uses only the source's prime-to-p character summands and preserves the possible nontrivial p-group action.

### Corollary 4.2 (restricted integrality of the actual maps)

Assume the hypotheses under which the existing LSSW auxiliary map is defined. For p >= 7, projection of cPi_N to the chi-component has a unique lift to

(K2(O_L) tensor Z_p)^(chi)

whenever p does not divide Q^f - 1, or the fixed prime-to-p character chi is nontrivial on I intersect G', or its unramified descent satisfies bar_chi_C([q]) != Q.

The same assertion holds for any existing unaugmented map satisfying the LSSW hypotheses and for an existing compactified map if its compactification has separately been justified. The proof does not establish compactification.

Proof. The relevant residue target is zero by Corollary 3.2 or Theorem 4.1; apply Proposition 2.1. All h source components remain in the map. QED.

At p = ell the entire residue target is zero, independently of characters, although the existence and compactification of the unaugmented ell-component may have other restrictions. At p = 5 the module calculation remains valid, but the cited auxiliary construction over R5 cannot supply a 5-primary map.

The lifted maps retain every good-prime Hecke relation, Galois compatibility, and smoothing identity already established for the localized maps. The inclusion of the integer-ring target is injective and equivariant, so equality after that inclusion implies equality before it. This supplies no new bad-prime identity.

### Proposition 4.3 (actual diamond-coinvariant factorization)

Let r_c = tau_S cPi_N over R5. For d in (O/N)^times and the diamond operator in LSSW Proposition 5.1.2,

r_c(<d>x) = r_c(x).                                      (4.3)

Consequently r_c factors through the quotient of H1(Y1(N),R5) by the submodule generated by all (<d>-1)x. The same holds for any calibrated unaugmented map for which the source's diamond identity is known.

Proof. Proposition 5.1.2 gives cPi_N <d> = R_N(d)cPi_N. The ray class of a principal ideal representing d lies in the kernel of G -> C, which is I. By (3.1), its action on T_q(L) is trivial. Apply the equivariant residue map. QED.

This is an actual factorization of the existing cocycle residue, but it is a diamond-coinvariant factorization. It is not the cusp-boundary factorization needed in §7. In particular, at p dividing the diamond-group order, we do not identify these coinvariants with the homology of a lower-level quotient by an unjustified averaging argument.

## 5. A single honest smoothing reduction away from the level characteristic

This section supplies an explicit permissible inverse, not division by a possibly nonunit in a finite K2-group.

### Proposition 5.1

For p >= 7 with p != ell, there exists an ordinary positive integer t > 1 such that

- t is prime to N and t = 1 modulo N;
- t^4 - 1 is a p-adic unit;
- for the proper principal auxiliary ideal c = (t), R_N(c) = 1 and (Nc)^2 = t^4.

For any unaugmented homology map Pi_N with the prescribed calibration,

cPi_N = (t^4 - 1) Pi_N,                                  (5.1)

and hence tau_S Pi_N = 0 if and only if tau_S cPi_N = 0 on the p-component. This is valid on all class-group components at once.

Proof. Let d be a positive integer in N, chosen to have no prime divisors other than ell (a sufficiently large power of ell works). Since p does not divide d and p >= 7, choose u in F_p^times with u^4 != 1. Chinese remaindering gives t = 1 modulo d and t = u modulo p. Add a positive multiple of dp to arrange t > 1. Thus t = 1 modulo N and is prime to N. The ideal (t) is ray-principal and has norm t^2 because [F:Q] = 2. Calibration gives (5.1). Its scalar is a unit in Z_p, so its inverse is an ordinary valid coefficient-ring inverse. Naturality of tau_S proves the equivalence. QED.

The same t can be selected simultaneously for the finitely many primes p >= 7 dividing m_q. Thus, over R5, one principal auxiliary ideal makes its smoothing factor invertible on the whole arithmetic residue module, even if it is not invertible on the entire K2 group. This reduces integrality of any calibrated unaugmented map to the arithmetic residue identity for one actual auxiliary map.

This device does not eliminate the 5-primary difficulty: every t prime to 5 satisfies t^4 = 1 modulo 5. It also does not prove that the residue in (5.1) vanishes.

## 6. Concrete checks: why the class group cannot be omitted

### 6.1 Class number one

For F = Q(i), take q = (5 + 2i), of norm 29. Then f = 1 and the residue module is cyclic of order 28, independently of n. Over R5 it is cyclic of order 7 with trivial ray-class action. Thus only the unramified trivial character can carry a 7-primary residue, but that component is a genuine nonzero quotient in (2.1). We have not computed the image of cPi_N in it.

For q = (3 + 2i), of norm 13, the residue order is 12 and vanishes over Z[1/6]. Therefore the existing R5 auxiliary map already has an integer-ring target at every q-power level covered by the source assumptions.

For the inert ideal (11) in Q(i), Q = 121 and f = 1. The residue order is 120. It vanishes over R5 but retains a cyclic 5-part over Z[1/6]. This is a target-localization issue distinct from construction of the 5-primary cocycle.

### 6.2 A nonprincipal level prime with a nontrivial class character

Let F = Q(sqrt(-23)), w = (1 + sqrt(-23))/2, and q = (2,w). Then Q = 2. The norm form is

Norm(a + bw) = a^2 + ab + 6b^2.

There is no element of norm 2, so q is not principal. Also Norm(2-w) = 8, and 2-w lies in q but not in its conjugate: modulo q, w = 0, while modulo the conjugate, w = 1. Therefore (2-w) = q^3. Thus [q] has order exactly 3, without any assumption that q has a generator.

Consequently f = 3 and m_q = 2^3 - 1 = 7. The reduced positive definite forms of discriminant -23 are (1,1,6), (2,-1,3), and (2,1,3), so h = 3 and T_q(L) is a single cyclic group of order 7. Its class-group generator kappa_q acts by multiplication by 2 modulo 7.

For p = 7, the residue is supported on the cubic p-adic character whose value on kappa_q reduces to 2. The trivial character and the other cubic character (reduction 4) have zero residue target. Thus replacing f by 1, considering only (O/N)^times, or discarding the nonprincipal components would miss the entire obstruction in this example.

Take n >= 2 to satisfy the existing source's unit-injectivity hypothesis: O^times = {+1,-1}, and v_q(2) = 1, so -1 is not congruent to 1 modulo q^n. These examples verify the size and character support of the ambient localization obstruction; none proves nonzero image of the intended map.

## 7. The exact connection to cusp boundaries

### 7.1 Relative maps: a genuine equivalence

Let X be the compactified Bianchi space with all connected components, C_N the specified finite allowed cusp set, R one of the coefficient rings above, and write

A_X = H1(X;R), B_X = H1(X,C_N;R),
D_X = ker(H0(C_N;R) -> H0(X;R)).

Then 0 -> A_X -> B_X --boundary--> D_X -> 0 is exact. Suppose, as an additional hypothesis, that an actual relative map F_rel: B_X -> K2(A_S) tensor R has already been constructed. Then its absolute restriction is integer-ring valued if and only if there is a homomorphism

beta: D_X -> T_q(L) tensor R

such that

tau_S F_rel = beta boundary.                              (7.1)

Proof. Proposition 2.1 makes integer-ring valuation equivalent to vanishing of tau_S F_rel on A_X. Exactness then gives precisely the factorization through D_X, uniquely. QED.

Equivalently choose a base cusp in each component meeting C_N. Assign a potential b(c) in T_q(L) tensor R to each cusp, with base potential zero. For a genuine path e from c to d, equation (7.1) says

tau_S F_rel(e) = b(d) - b(c).                              (7.2)

The potentials on different connected components are independent. This accounts for the full cusp and class-group sets without assuming principal cusp representatives.

### 7.2 Prescribed edges: the exact finite graph test

For already defined proposed values t_e in K2(A_S) tensor R on genuine oriented cusp edges, put r_e = tau_S(t_e). A cusp potential exists on their endpoint graph if and only if every finite endpoint-balanced combination of edges has sum of residues zero. Equivalently, every oriented graph cycle has residue sum zero. A spanning forest then constructs the potential by summing along its unique paths.

Proof. Necessity is telescoping. For sufficiency define the potential along a spanning forest from a base in each graph component. Adding any remaining edge produces a unique graph cycle, whose zero sum makes that edge agree with the potential. The construction is valid over an arbitrary abelian target; no division is used. It is the incidence-lattice saturation from accepted PASS1 in explicit residue form. QED.

This test on prescribed edges does not by itself supply a global relative homology map or control absolute cycles outside the subgroup generated by those edge combinations. The existence of F_rel and its agreement with the actual auxiliary cocycle remain essential.

### 7.3 The missing arithmetic identity, correctly smoothed

For a field automorphism sigma, m = Nc, and u,v in L^times, put a = u^m/(sigma u), b = v^m/(sigma v). The accepted PASS1 identity is

(m^2 - sigma){u,v} = {a,b} + {a,sigma v} + {sigma u,b}.     (7.3)

Applying the equivariant vector residue map yields

(m^2 - sigma) tau_S{u,v}
 = tau_S{a,b} + tau_S{a,sigma v} + tau_S{sigma u,b}.        (7.4)

Equation (7.4) is an exact identity for genuine field-valued units; if theta roots lie only in an extension, descent is an additional requirement. It cannot be replaced by the residue of {a,b} alone. In a local presentation u = pi^r u0 and v = pi^s v0,

tau_v{u,v} = (-1)^(rs) overline(u0)^s / overline(v0)^r.    (7.5)

These formulas reduce a proposed cusp-potential claim to explicit valuation and angular-component identities, without assuming that a generic auxiliary theta pair is a cocycle. PASS1 proved that its generic triangle identity fails.

For the actual LSSW map the unresolved condition is especially sharp. After the support reductions above, only the following must still be computed at p >= 7, p != ell:

- choose an unramified chi with bar_chi_C(kappa_q) = Q;
- choose t from Proposition 5.1 and c = (t);
- for every class-group component r and every gamma in Gamma1(N)_r, prove

  projection_chi tau_S(cTheta_(r,1),N(gamma)) = 0.         (7.6)

A finite set of homology generators suffices because the specialized cocycle restricts to a homomorphism on Gamma1, and the residual target is the explicit finite module of Theorem 4.1. If a genuine relative formula is first established, (7.6) is equivalent on represented cycles to telescoping the correctly smoothed residues in (7.4), provided the comparison with cTheta is proved.

No identity (7.6) in the surviving components is established here. Proving it, or producing a specific nonzero evaluated residue of the actual cocycle, is the remaining arithmetic step. A nonzero ambient group in §6 is not such a computation.

## 8. Acceptance boundary

Proved here:

- the complete, all-class-group localization obstruction and its independence of prime-power depth;
- its exact exponent and exact prime-to-p character support, with the direct arithmetic Frobenius convention;
- unique integral lifts for the existing actual maps off that support;
- an explicit scalar-unit smoothing reduction at every p >= 7 away from the level characteristic;
- the exact equivalence between integral absolute values and cusp factorization, conditional on an actual relative map;
- finite graph and Steinberg residue tests that identify the unproved arithmetic identity.

Not proved here:

- vanishing of the actual cocycle residue on the surviving unramified class-group characters;
- any new compactification theorem or bad-U identity;
- the normalized integral relative theta construction or its comparison to the geometric cocycle;
- the original R = Z[1/6] construction, including its 5-primary part.

The original row remains UNSOLVED. No queue, accepted-file, repository, or publication changes were made in this lane.
