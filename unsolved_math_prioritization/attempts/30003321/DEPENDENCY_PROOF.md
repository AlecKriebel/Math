# Detailed initial-group characterization dependency proof

Current17October2026 edition, problem30003321. The characterization is credited to Ehrlich–Kaplan2018 Theorem5.1, not claimed as new. This authored supplement proves its sufficiency without the bounded-stage exhaustion or unavailable dyadic-option assumptions; the statement is not refuted. It is a source-dependency repair, not a change to the downstream sign-map construction.

The only substantive imported surreal facts are the canonical normal-form isomorphism, the usual recursive addition/negation rules and simplicity theorem, the leader cut, the pure-real-multiple cuts in source Lemma 3.1(ii)–(iii), the normal-form limit cut in Proposition 3.2(iii), and the necessity facts in Proposition 3.2(i)–(ii), Lemma 3.1(i),(iv). These are expressly identified imports, not rederived normal-form theory.


## 1. Independent initial-subgroup extension argument

Write `u ⪯s v` when u is v or an initial sign-sequence segment of v. Two elementary tree facts will be used.

1. If z ≺s q and z < t < q, then z ≺s t; similarly if q < t < z. Equality t=z is allowed with ⪯s. This follows directly from lexicographic comparison of sign sequences: to lie between a sequence and one of its extensions on a specified side, t must extend the shorter sequence.
2. Suppose q={L|R}, and every member of L∪R belongs to an initial class M. Then every proper predecessor z of q is in M. Indeed, z cannot lie strictly between L and R, by simplicity of q. If z<q, some l∈L satisfies z≤l<q; if z>q, some r∈R satisfies q<r≤z. Fact 1 and initiality of M give z∈M. No membership assumption q∈M is needed. The cuts used below have sets of options.

**Sum lemma.** If S,T are initial subclasses of No, then S+T is initial. Prove, for each pair (s,t), that every predecessor of s+t lies in S+T, by induction on the natural/Hessenberg sum of their birthdays. Recursive surreal addition writes s+t as the simplest element between the options s^L+t, s+t^L and s^R+t, s+t^R. Every such option has an operand of strictly smaller birthday, so the induction applies to that pair. If z≺s(s+t), simplicity gives an option between z and s+t on the relevant side, and Fact 1 says that z is that option or a predecessor of it. It is in S+T by membership or induction. This argument remains valid when a displayed arithmetic option has greater birthday than the final sum: the induction is on operand birthdays, not on result birthdays.

Negation reverses every sign and preserves the predecessor relation, so -S is initial when S is. Therefore, if S is initial and contains 0, its additive subgroup closure is initial: it is the increasing union of the finite sums of S∪(-S), each initial by the sum lemma.

**Z-extension lemma.** If M is an initial additive subgroup and b is simplest between sets of options from M, then M+Zb is initial. Fact 2 makes M∪{b} initial; take its additive subgroup closure. This independently proves exactly the specialization of manuscript Lemma 4.1 used here. It does not assert or rely on the general K-module version or predecessor [15], Theorem 6.

For comparison with the source's partition language: if b∉M, L_M={m∈M:m<b}, R_M={m∈M:b<m} partition all of M. The original option sets lie on their respective sides. Since the interval defined by the full partition is contained in that of the known b-cut and still contains b, b is its simplest member. For set M both partition sides are sets. Thus the cut and full-partition hypotheses of Lemma 4.1 are satisfied whenever it could replace this independent Z-extension lemma. A chain union of initial subgroups is initial, since each predecessor of each member is already in the subgroup containing that member.

## 2. All finite monomial sums, without any support-limit assumption

Assume E⊆No is a **set** that is initial. Let A be the canonical image of the given subgroup with exponents E. Thus A is a set. For y∈E, R_y contains 1 by cross sectionality and is an initial subgroup of the real surreal subtree.

Well order E by nondecreasing birthday, with arbitrary well order within each birthday. Every proper predecessor exponent of y occurs before y. Start with M={0}; at an exponent stage y, assume M contains the pure terms at all earlier exponent stages and is initial. Adjoin the following elements, skipping any already present.

* First adjoin ω^y. Its leader cut has left options 0 and nω^{y^L}, and right options 2^{-n}ω^{y^R}. Every y^L,y^R is an earlier exponent. The integer left coefficients belong to earlier coefficient groups by cross sectionality. For right options, the theorem's condition (iii), applied with x=y and exponent y^R, gives D⊆R_{y^R}. All options belong to M. The Z-extension lemma applies, and automatically includes every integer multiple of ω^y.
* Then adjoin all noninteger pure terms rω^y for r∈R_y in nondecreasing **real** birthday. Any real predecessor r' of r is in R_y by initiality; if noninteger it occurs earlier, while all integer terms are already included. For r nondyadic, or r dyadic with L_s(y)=∅, the cut from Lemma 3.1(ii) consists of the earlier pure predecessor terms. For r noninteger dyadic with L_s(y)≠∅, Lemma 3.1(iii) uses sums of earlier pure predecessor terms with ±nω^{y^L}; these also lie in M. Apply the same extension lemma.

At limits take unions. These are unions of explicitly built groups, not assertions that every series over an initial exponent segment has already occurred. At the end the resulting initial subgroup F is precisely the subgroup generated by all allowed pure terms: every element adjoined is pure, and closure is additive. Consequently F contains every finite-support member of A.

## 3. Unit perturbations at every infinite limit support

Let x=Σ_{μ<λ}r_μω^{y_μ}∈A have nonzero coefficients and strictly decreasing exponents, with λ an infinite limit ordinal. Let s_η=Σ_{μ<η}r_μω^{y_μ} for η≤λ. For each μ<λ define

    l_μ = s_{μ+1} - ω^{y_μ},      u_μ = s_{μ+1} + ω^{y_μ}.

The leading coefficient of x-l_μ at y_μ is 1, and that of u_μ-x is 1. Hence l_μ<x<u_μ. **Each option is in A:** s_{μ+1} is a proper truncation because μ+1<λ, and ω^{y_μ} is in A by cross sectionality. No fractional coefficient is used. Cancellation when r_μ=±1 simply removes a term and causes no problem.

These options define x as their simplest separator. To verify this using the imported usual limit-series cut, fix one of its lower options s_{μ+1}-2^{-n}ω^{y_μ}. Choose ν with μ<ν<λ. Lexicographic normal-form comparison gives

    s_{μ+1}-2^{-n}ω^{y_μ} < l_ν < x < u_ν < s_{μ+1}+2^{-n}ω^{y_μ}.

For the left comparison the first nonzero difference is +2^{-n} at y_μ; the right comparison is analogous. Thus every number between all the unit options is between all options of the standard limit cut; x lies between all unit options. The simplicity theorem for the standard cut therefore makes x the simplest element between the unit options as well. We do **not** need to assume that each displayed unit option is itself a predecessor of x.

## 4. Exhaustion by support length

Well order the **set** of all members of A of infinite limit support length, first by increasing support length and arbitrarily within a fixed length. Start with F, and adjoin these members one by one using additive subgroup closure. Suppose a member x of length λ is next. All series in A of strictly smaller support length already lie in the current subgroup M: any ordinal α has the form δ+n, where n<ω and δ is zero or a limit ordinal. A series of length α is its prefix of length δ plus n pure monomials; if δ=0 it is a finite sum, and otherwise its limit-length prefix was adjoined earlier. Every unit option for x has support length at most μ+1<λ, so is in M. Section 3 gives its cut, Section 1 gives the extension. At limit stages take chain unions.

The resulting group is initial and equals A: the same δ+n decomposition expresses **every** member of A as a previously adjoined limit-length series plus finitely many pure terms. This covers arbitrary set supports, including supports cofinal in the entire exponent enumeration, and coefficients in discrete groups 2^{-m}Z. Normalization of the first coefficient to 1 is unnecessary because we adjoin all actual limit-length members of A.

## 5. Proper classes by actual set-sized initial exponent restrictions

Now let Γ be a class satisfying the theorem and x∈A. Its support S is a set, even when Γ is a proper class. Define

    E = ⋃_{y∈S}({y} ∪ pr_No(y)).

Every predecessor collection is a set, so Replacement and Union make E a set. Since Γ is initial, E⊆Γ. Transitivity of the predecessor relation makes E initial in No. Set E=∅ for x=0 if desired.

Restrict the **given group**, rather than inventing a new Hahn group:

    A_E = {a∈A : supp(a)⊆E}.

The class A_E is a set, as it is a subclass of the set of all real-coefficient Hahn series over E (encoded by subsets of E×R). It is an additive subgroup, truncation closed, and cross sectional over E. Its coefficient group at any y∈E is exactly the original R_y. Condition (iii) is inherited for pairs x',y∈E. It therefore satisfies all hypotheses of the set-exponent proof, so A_E is initial. In particular every predecessor of the original x belongs to A_E⊆A. Since x was arbitrary, A is initial. There is no class-sized cut, class-length support, bounded-support assumption, or unproved class recursion in this passage.

## 6. Necessity and precise strength

Initiality gives truncation closure by the normal-form predecessor property. Subtracting two consecutive prefixes gives each individual pure term. Taking its absolute value and using 1⪯s|r| together with Lemma 3.1(i) gives its leader ω^y; thus Γ is exactly the available support exponents. Proposition 3.2(i) makes Γ initial. Lemma 3.1(i) makes each R_y initial, and Lemma 3.1(iv) forces every 2^{-n} at a right-predecessor exponent. Additive closure gives D there. These arguments, with the stated imported normal-form facts, verify the other direction without the erroneous outer union.

Strongest result independently established here: the full set/proper-class canonical Hahn-image characterization in the sealed claim, modulo precisely the explicitly listed standard normal-form and surreal-recursion imports. The alleged exponent-union and dyadic-option steps are unnecessary and in fact fail as written; the theorem itself is repaired. This is a transparent dependency check, not a proof of the downstream discrete-group-to-Oz claim and not a priority search.
