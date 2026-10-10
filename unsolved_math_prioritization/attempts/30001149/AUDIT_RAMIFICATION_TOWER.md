# Independent audit of the weak almost-rational partial results

Date: 2026-10-10 UTC. Target: 30001149 / OWR-3388-008.

## Verdict

**Accept both audited candidates as partial theorems under their stated assumptions. No blocking mathematical error was found. Neither candidate proves a classification or the weak-to-strong implication.**

The characteristic-two restriction to the initial lower-break pairs `(1,3)` and `(1,5)` is valid. The orbit-field Galois descent is valid, including its application to the reverse degree-p projection for odd p. The genus formula and final-break obstruction are valid. The detailed checks below supply additional explanations for steps that could otherwise conceal a hypothesis or an indexing mistake.

This audit covers the mathematics of the two companion partial proofs identified below. It does not certify the separate order-four exclusion or bridge, which have their own full audit in [AUDIT_ORDER4_BRIDGE.md](AUDIT_ORDER4_BRIDGE.md). It is a mathematical validity audit, not a global novelty certificate or a formal proof-assistant verification.

## Distributed proof editions

- [RAMIFICATION_PARTIAL.md](RAMIFICATION_PARTIAL.md): 6,826 bytes; SHA-256 `f0831bbdb4288ee09d9465a9821a3387918c6ee2237bf2f40fdbe16819f0c721`.
- [ORBIT_TOWER_PARTIAL.md](ORBIT_TOWER_PARTIAL.md): 6,714 bytes; SHA-256 `7426828fffb45642676a9848c235ce72f53b09c1a4bc7f217f211ce8e939eaa4`.

The original proof arguments and the full mathematical audit are preserved. This edition updates status wording and report identities after acceptance; those editorial changes do not introduce a mathematical repair. The two separate original proof notes do not claim the later order-four bridge.

## 1. Precise hypothesis and source boundary

Throughout, k is algebraically closed of characteristic p>0, sigma is a k-automorphism of k[[t]] of exact finite order N=p^n with n>=2, and sigma(t) lies in a degree-p Artin–Schreier extension E0 of k(t) embedded in k((t)). There is no assumption about the location of the other iterates in E0.

The original source is Ted Chinburg's contribution, *Katz-Gabber covers with extra automorphisms*, in *The Arithmetic of Fields*, Oberwolfach Report 05/2009, pp.325–327, joint work credited there to Bleher, Poonen, Pop and Symonds. The ambient algebraic-closure assumption on p.325, Definition 1 on p.326, and Theorem 2 plus the closing question on p.327 were checked, including visual inspection of pp.326–327. Definition 1 constrains the single image; Theorem 2 separately assumes a common Artin–Schreier field for all powers. The concluding problem removes that additional hypothesis. [Publisher record](https://ems.press/journals/owr/articles/3388), [DOI](https://doi.org/10.4171/owr/2009/05).

The formulation using E0 is equivalent to the original normalized Artin–Schreier formulation in this setting. If beta in E0 subset k((t)) satisfies beta^p-beta=alpha in k(t), subtract the finite nonpositive Laurent part h in k[t^-1]. Then beta'=beta-h belongs to tk[[t]], and alpha'=alpha-(h^p-h) belongs to k(t) intersect tk[[t]]. The generator and extension degree are unchanged. The equation has its unique root in tk[[t]], obtained by the convergent Artin–Schreier power-series sum. Conversely, the original formulation directly supplies E0. Thus the candidates have not silently enlarged the relevant class through their notation.

The later Bleher–Chinburg–Poonen–Symonds paper, *Automorphisms of Harbater–Katz–Gabber curves*, Definition 1.1, requires the entire orbit field to have degree p. Its Theorem 1.2 is therefore not available for an arbitrary pair field here. Its Section 3.D supplies the standard ramification input: if u_j are the upper breaks, u_0 is positive and prime to p, u_j>=p u_(j-1), and a strict inequality requires p not dividing u_j. It also gives b_j=u_0+sum_(h=1)^j p^h(u_h-u_(h-1)). These are facts about cyclic local actions, independent of almost rationality. [Author manuscript](https://math.mit.edu/~poonen/papers/AutK.pdf), [DOI](https://doi.org/10.1007/s00208-016-1490-2).

The degree-equals-height observation is already present in Byszewski–Cornelissen–Tijsma, *Automata and finite order elements in the Nottingham group*, Proposition 9.2.1, printed pp.531–532. Its proof over F_p uses a finite stable orbit field and a tower-law comparison, so the same proof works here. The candidate correctly credits this input. The institutional PDF was inspected using the web text parser; this audit does not assert a new local download or byte identity for it. [Institutional primary copy](https://research-portal.uu.nl/ws/files/149368215/1_s2.0_S002186932200134X_main.pdf), [DOI](https://doi.org/10.1016/j.jalgebra.2022.03.019).

## 2. Common algebraic preliminaries

Write t_i=sigma^i(t), with indices modulo N, and L=k(t_0,...,t_(N-1)). Every t_i has valuation one, so it is transcendental over k. An algebraic equation for t_1 over k(t_0), transported repeatedly by sigma, shows that each next t_i is algebraic over the preceding coordinate field. Transitivity proves that L/k(t_0) is finite. The field L is stable under sigma; no pair-field stability is used.

If t_1 were in k(t_0), finite-order inclusion would give sigma(k(t_0))=k(t_0). Its restriction would still have order N: a power fixing t_0 fixes the entire formal power-series ring by continuity. It would therefore give an element of order p^n in PGL_2(k). Such an element has order at most p. Indeed, a semisimple projective element has eigenvalue ratio of order prime to p, whereas a nontrivial projective unipotent element has order p. This contradicts n>=2.

Thus E=k(t_0,t_1)=E0 and [E:k(t_0)]=p. The equality [L:k(t_0)]=[L:k(t_1)], followed by the tower law through E, gives [E:k(t_1)]=p. The minimal irreducible polynomial relation P(X,Y) consequently has degree p in each variable. This equality of projection degrees by itself says nothing about normality when p>2. The orbit note correctly waits until after its Galois descent to assert reverse cyclicity.

Because k is algebraically closed, all function fields used have constant field k. Their smooth projective models and the geometric genera in the statements therefore have their ordinary meanings without a hidden constant-field extension.

## 3. Audit of `RAMIFICATION_PARTIAL.md`

This section assumes p=2.

### 3.1 Bidegree and the finite-order hypothesis

The argument above gives an irreducible P(X,Y) of bidegree (2,2). Its bihomogenization is the equation of an integral curve C in P1 x P1. Exact degree two in each variable prevents an extra entire boundary fiber from being introduced in this closure. Its function field is E. No action of sigma on C is needed.

A 2-power-order automorphism has linear coefficient one, because k^* has no nontrivial 2-power torsion. Thus b_0=v_t(t_1-t_0)-1 is positive. Standard cyclic ramification identifies b_1=v_t(t_2-t_0)-1 as the second lower break, including when n>2.

### 3.2 Transpose argument

Let f(X)=sigma(X) and g(X)=sigma^-1(X), interpreted as substitution series. They are distinct because sigma has order at least four. Both have zero constant term. Substitution by sigma preserves t-adic valuation and sends sigma(t)-sigma^-1(t) to sigma^2(t)-t, so

    v_t(f(t)-g(t)) = b_1+1.

If C equaled its transpose C^T, both f(t) and g(t) would solve P(t,Y)=0. Write P(t,Y)=A(t)Y^2+B(t)Y+D(t). The coefficient B is nonzero because E/k(t) is separable. The root-sum formula gives f(t)+g(t)=B(t)/A(t). Since A and B are polynomials of degree at most two,

    v_t(B/A) = v_t(B)-v_t(A) <= 2.

Zeros of A at the origin only decrease this upper bound; no regularity of B/A was incorrectly assumed. On the other hand, the upper-break inequalities give b_1>=3b_0>=3, so v_t(f-g)>=4. This contradiction proves C!=C^T. Since both curves are integral, they have no common component.

The use of b_1>=3b_0 here is legitimate for all n>=2. It does not assume that sigma itself has order four, and it is not a consequence of the candidate being proved.

### 3.3 Local intersection, including a singular origin

The global intersection number is eight: the intersection pairing on P1 x P1 is (a,b).(c,d)=ad+bc. Therefore the local intersection multiplicity at (0,0) is at most eight.

Here is an independent local justification that avoids any smoothness or branch-reducedness concern. Put R=k[[X,Y]] and Q(X,Y)=P(Y,X). Formal division gives

    P in (Y-f(X)),       Q in (Y-g(X)).

Consequently

    (P,Q) subset (Y-f(X),Y-g(X)).

There is a surjection from R/(P,Q) to R/(Y-f,Y-g). The first quotient has finite length because the two algebraic curves have no common component. Completion preserves this local intersection length. The second quotient is isomorphic to k[[X]]/(f-g), of length b_1+1. Hence

    b_1+1 <= length R/(P,Q) = I_(0,0)(C,C^T) <= 8.

This proves the desired inequality at a singular point as well. The candidate's additive-branch proof is valid; the quotient-length proof is an optional simplification, not a repair of a false result. It neither treats the whole curve as its selected graph branch nor assumes that the pair field is invariant.

### 3.4 Ramification arithmetic

For p=2 the upper breaks satisfy u_0=b_0 and u_1=(b_1+b_0)/2. The input in Section 1 gives b_0 positive and odd, u_1>=2b_0, and u_1 odd if this inequality is strict. Thus b_1>=3b_0. Since b_1<=7, the only possible b_0 is one.

Integrality of u_1 makes b_1 odd. The remaining candidates are 3, 5 and 7. The value 7 gives u_1=4>2u_0 while 2 divides u_1, violating the strict-inequality condition. The candidates 3 and 5 give u_1=2 and 3 respectively and are not removed by these conditions.

**Accepted statement:** Under the exact weak hypothesis in characteristic two and any n>=2, (b_0,b_1) belongs to {(1,3),(1,5)}.

This is a necessary condition. It does not prove existence for (1,5), an order bound, pair-field invariance, uniqueness of conjugacy class, or any odd-characteristic classification.

## 4. Audit of the orbit-field theorem

This section allows every prime p.

### 4.1 Forward tower and the first stabilization

Set F_m=k(t_0,...,t_m). The extension F_m/F_(m-1) is generated by adjoining t_m from the cyclic degree-p extension k(t_(m-1),t_m)/k(t_(m-1)). A base change of a Galois extension remains Galois on the resulting field compositum; its degree divides p. Thus this step is trivial or cyclic of degree p.

If F_m=F_(m-1), sigma(F_(m-1))=k(t_1,...,t_m) is contained in F_(m-1). Applying successive powers of the finite-order automorphism makes a chain of inclusions returning to its starting field, so all inclusions are equalities. The field then contains the whole orbit. Hence there is no possibility of a trivial step followed by a nontrivial step.

The first step is nontrivial, while the step adjoining t_N=t_0 is trivial. Therefore 1<=r<=N-1 exists, the first r steps have degree p, F_r=L, and [L:k(t_0)]=p^r.

### 4.2 Interval degrees

For an interval [a,b] of length ell<=r+1, shifting F_(ell-1) by sigma^a gives

    [K[a,b]:k(t_a)] = p^(ell-1).

Also [L:k(t_j)]=p^r for every j because sigma acts on L. It follows that [L:K[a,b]]=p^(r-ell+1), and the tower law through any coordinate t_j in that interval gives [K[a,b]:k(t_j)]=p^(ell-1). This verifies the degree assertion even for an interior coordinate, where a forward-tower argument alone would not suffice.

### 4.3 Intersection step

For 1<=ell<=r-1, take

    C=K[a,b],  A=K[a-1,b],  B=K[a,b+1],  b-a+1=ell.

The interval formulas give [A:C]=[B:C]=p and [AB:C]=p^2. Thus A and B are distinct. Since A intersect B is an intermediate field of the prime-degree extension A/C, it is C or A. The latter would imply A subset B and then A=B, contradicting the compositum degree. Therefore A intersect B=C. No unproved normality of A/C or B/C is being smuggled into this step.

### 4.4 Descending Galois argument

For every interval of length r, L/K[a,b] is a shifted copy of the last nontrivial cyclic step and hence is cyclic of degree p. Length r+1 gives the trivial extension. For r=1 these statements already prove Galoisness over every coordinate field, so a nonexistent shorter interval is never needed.

For r>1, suppose L/A and L/B are Galois at one level of the descent. The finite group Gamma generated by Gal(L/A) and Gal(L/B) lies in Aut(L/C), which has at most [L:C] elements. Its fixed field is

    L^Gamma = L^Gal(L/A) intersect L^Gal(L/B) = A intersect B = C.

Artin's fixed-field theorem now implies L/C is Galois. This proves the induction down to single-coordinate fields. It is the crucial valid reason that the complete orbit extension is Galois; a tower of cyclic degree-p steps alone would not imply that conclusion.

Since [L:k(t_i)]=p^r, each resulting Galois group is a finite p-group. An adjacent pair field has degree p over either coordinate field. Its corresponding subgroup has index p in that p-group and is therefore normal. The quotient group has order p and is cyclic. The assertion that the reverse adjacent projection is cyclic Galois is thus justified for odd p as well as for p=2.

**Accepted statement:** Every assertion (a)–(e) of Theorem 1 holds under the stated weak hypothesis, with the exact interval ranges written in the candidate.

## 5. Geometric and genus consequences

### 5.1 The distinguished point and its stabilizers

Let X be the smooth projective curve with function field L. The valuation induced by L subset k((t)) has value group Z because t has value one, and residue field k. It defines the point x. Since k(t) is dense in k((t)), the completion of L at x is exactly k((t)); in particular, t is a uniformizer. Sigma preserves this valuation and fixes x, with its original exact order on the completion.

For H_i=Gal(L/k(t_i)), the quotient X/H_i is rational. At x the local parameter t_i also has value one, so the map to the t_i-line has ramification index one. The residue degree is one because k is algebraically closed. In a Galois cover the stabilizer is the decomposition group, of order equal to the product of these two local degrees. Hence H_i has trivial stabilizer at x. The assertion is only about this point; it does not say H_i acts freely everywhere on X.

An automorphism of L fixes K[a,b] precisely when it fixes every coordinate t_a,...,t_b. Therefore

    H_a intersect ... intersect H_b = Gal(L/K[a,b]).

The interval Galois theorem gives the stated order p^(r-ell+1). Neighboring groups consequently meet in index p, and r+1 consecutive groups have trivial intersection.

The same local argument applies on each neighboring pair curve. Its two cyclic degree-p quotient groups are distinct: equality would force equality of their rational fixed fields and make t_(i+1) rational in t_i, already excluded. Both act freely at the distinguished point. The pair curve has two generating degree-p rational coordinate subfields, so its genus is at most (p-1)^2.

### 5.2 Castelnuovo–Severi and the whole orbit field

The needed form of Castelnuovo–Severi is: if F=F_1 F_2 is a function field over a perfect field, with d_j=[F:F_j], then

    g(F) <= d_1 g(F_1)+d_2 g(F_2)+(d_1-1)(d_2-1).

The equality F=F_1 F_2 is essential. It holds here by construction at every step. For a primary published statement over perfect fields, see Khawaja–Siksek, *Primitive algebraic points on curves*, Theorem 14. Its alternative of a common factor map of degree greater than one is excluded precisely because the two subfields generate F. [Published theorem and proof](https://link.springer.com/article/10.1007/s40993-024-00543-4).

At step m<=r take F=F_m, F_1=F_(m-1), F_2=k(t_m). The indices are p and p^m; the second equality uses the interval-degree result and is not guessed from the number of generators. The second genus is zero. Thus

    g_m <= p g_(m-1)+(p-1)(p^m-1),    g_0=0.

To check the claimed closed form directly, put B_m=1+p^m(m(p-1)-1). Then B_0=0 and

    p B_(m-1)+(p-1)(p^m-1) = B_m.

Induction proves g_m<=B_m, including

    g(L) <= 1+p^r(r(p-1)-1).

All maps involved are separable: the forward steps are Artin–Schreier base changes, and the interval fields sit inside the already established Galois coordinate extension. No inseparability exception invalidates this application.

**Accepted statements:** Corollaries 2 and 3, with their original hypotheses and interpretation of freeness at the selected point, are valid.

## 6. Final-break and orbit-degree obstruction

For any j with sigma^j nonidentity, t_j-t_0 is a nonzero rational function on X. Each function t_i defines a map of degree [L:k(t_i)]=p^r to P1, so its pole divisor has degree p^r. The pole divisor of a difference is bounded by the sum of the two pole divisors. A nonzero principal divisor has degree zero, and therefore

    v_x(t_j-t_0) <= degree (t_j-t_0)_0
                  = degree (t_j-t_0)_infinity <= 2p^r.

Possible cancellation at a common pole improves the inequality; it cannot reverse it. The valuation at x uses t itself as a uniformizer, so it agrees with the original formal-series valuation without a missing ramification factor.

For the final lower break, expand the ramification formula explicitly. The upper-break inequalities imply u_0>=1, u_j>=p^j, and

    u_j-u_(j-1) >= (p-1)u_(j-1) >= (p-1)p^(j-1).

Consequently

    b_(n-1) = u_0 + sum_(j=1)^(n-1) p^j(u_j-u_(j-1))
             >= 1 + (p-1) sum_(j=1)^(n-1) p^(2j-1)
             = (p^(2n-1)+1)/(p+1).

The final break is realized by sigma^(p^(n-1)), an element of order p. The preceding pole bound therefore gives

    (p^(2n-1)+1)/(p+1) + 1 <= 2p^r.

The candidate's sentence about “successive increments” is safe when read as the upper-break increments u_j-u_(j-1), which occur with weights p^j in the lower-break formula. Displaying the sum above would remove any possible ambiguity. The final formula itself is correct.

The stated integer consequences also check:

- If p>=3 and r<=2n-3, the right side is at most 2p^(2n-3). The leading term p^(2n-1)/(p+1) already exceeds that quantity because p^2>2(p+1). Contradiction. Hence r>=2n-2.
- If p=2 and r<=2n-4, the right side is at most 2^(2n-3), strictly less than 2^(2n-1)/3. Contradiction. Hence r>=2n-3. For n=2 the claimed lower bound is also the already known r>=1.
- With r=1 and n>=2, odd p is excluded by r>=2n-2, and p=2 forces n=2 by r>=2n-3.

**Accepted statement:** Corollary 4, including its general inequality, the two stated lower bounds on r, and its r=1 consequence, is valid.

## 7. Exact remaining gap and prohibited inferences

For these hypotheses the following conditions are equivalent:

1. r=1.
2. L=E=k(t_0,t_1).
3. sigma(E)=E.
4. t_2 belongs to E.

The first three equivalences are immediate from the established degrees and orbit definition. For (4), sigma(E)=k(t_1,t_2) subset E; finite order turns that inclusion into equality. Pair-field stability then contains all iterates. Thus the bridge can be reduced to one additional membership statement, but neither candidate proves it.

The Galois theorem gives a p-group covering the t-line, not a proof that its order is p. Galoisness of both adjacent projections does not imply pair-field invariance under sigma. The genus bound grows with r and therefore is not by itself an elimination of larger orbit fields. The initial-break restriction does not constrain all later breaks. Arithmetic compatibility of `(1,5)` is not an existence proof. Conversely, absence of a recognized example is not an impossibility proof.

No assertion that X is an HKG curve is needed for either accepted candidate, and it would be unjustified to import such an assertion without its own proof. No abstract wording from the later classification overrides its whole-orbit definition. No finite truncation or finite-field scan is used in this audit as evidence of exact finite compositional order.

## 8. Disposition and optional editorial improvements

- Accept the two exact audited files as mathematically proved partial results.
- Keep the original weak problem marked unresolved unless a separate argument settles the residual cases or supplies a counterexample.
- Preserve the explicit distinction between the pair field E and the orbit field L.
- Optionally replace the branch-additivity paragraph by the quotient-length proof in Section 3.3.
- Optionally write out the weighted upper-to-lower-break sum from Section 6 and specify that X is the smooth projective model in Corollary 2.
- Retain credit for the original question, the later strong classification, the standard cyclic ramification constraints, and the prior degree-equals-height lemma. Castelnuovo–Severi, Artin's fixed-field theorem, prime-index normality in p-groups, and basic divisor/intersection facts are standard inputs, not newly established general theorems.

There is no mandatory correction to a theorem statement on the basis of this audit.
