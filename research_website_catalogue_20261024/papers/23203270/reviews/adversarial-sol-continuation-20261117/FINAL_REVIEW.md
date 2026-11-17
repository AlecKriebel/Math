# Adversarial continuation: record 23203270

This is a finite scientific review record for the root's later disposition. It does not publish, promote, or revise the manuscript. The original-only reconstruction remains frozen in the separate INITIAL lane. No other family's or root's mathematical report was read, and no scientific mechanisms or assessments were disclosed in messages while the root's original-reading gate remained active.

The exact target remains the full original claim: the specified complex algebra A is a smooth integral fourfold, the explicit polynomial maps split inside C^[5], their five displayed components define an idempotent, and the image is nonpolynomial. There is no substitution of a conditional, localized, generic-fiber, field-changed, or lower-dimensional claim.

## Evidence state

The original-only hand derivation established the algebraic coordinates and maps before any supporting opinion was opened. After RESUME, I acquired the ten actual upstream TeX files at the exact commit adc7f1241b42e322a6451854ab7e4b4c146bf78a through read-only connected GitHub file retrieval. All ten SHA-256 hashes agree with the deposited manuscript-source pins. I personally read all ten complete files, including all proof bodies in Sections 3-6. Thus the nonpolynomiality review below rests on the actual primary proof, rather than a theorem statement, declared audit, formal model, or search result.

The package's two Python bodies, relevant author audits, claimed data outputs, dependency ledger, and selected actual Lean proof bodies were read. The latter were Model, Main, PositiveInvariant, ReesReduction and EquivariantLift. The entire 55-module formal proof closure was not independently read or built in this lane, and no kernel certification is inferred. The source bytes for the complete package were authenticated, which is distinct from semantic inspection of every file.

The exact one-route execution outcome is **DEFER for native reproducibility**: the ordinary isolated invocation of the unchanged check_stabilization.py exited 1 at its SymPy import with ModuleNotFoundError. No mathematical check was reached. stdout is the literal empty byte stream; stderr is retained as 295 literal bytes. The receipt records 0.06187079200753942 seconds, the command, start/end UTC, exact entrypoint hashes and full before/after guards. There was no installation, interpreter switch, repair, second native route or retry. The deposited PASS result with 32 identities and seven rational checks remains an author-supplied historical result, not a result reproduced here. The written map proof and imported proof were evaluated independently of that result; the failed native attempt is not reported as a successful weaker check.

## Closure of the INITIAL imported interfaces

### 1. The valuation and exact associated graded algebra

Primary source: imported-primary/sections/03-degeneration.tex, full file; key labels deg:valuation, prop:graded, lem:induced-lnd and prop:positive-invariant.

The source proves the missing coefficient-ring interface. S=C[p,x,y,z,u]/(xy-z(z+1)-p^3u) is a domain and embeds in A because localization at p is an isomorphism. Its p-quotient R is a smooth domain. S localized at its prime ideal pS has principal maximal ideal p and is a DVR; the source supplies a direct ascending-chain proof that division by p terminates. Global divisibility descends from this localization by primality of pS, repeatedly. Therefore valuation coefficients of elements of S[p^(-1)] actually lie in R, not merely Frac(R).

I checked the potential negative-weight failure explicitly. The kernel of the substitution of the five initial generators is the principal prime (H_top), obtained by localization and p-saturation in the original polynomial UFD. If a representative's leading terms cancel, subtracting H times a homogeneous quotient reduces the maximum presentation weight from M to below M, with replacement term of weight M-3. The fixed valuation degree of the represented nonzero element is a lower bound. The iteration terminates despite the generator p having negative weight. Thus this is an exact graded presentation; it is not an unsupported claim that initial generators always generate associated graded rings.

The generator maximum for a derivation shift now bounds its value on every exact-weight representative. The induced top derivation is nonzero because a generator attains that maximum, and its iterates are the prescribed graded classes of the original iterates, even following an intermediate degree drop. The source thereby proves local nilpotence for either sign of shift. Under hypothetical arbitrary polynomial coordinates on A, at least one coordinate has positive valuation degree because F has degree two and the nonpositive part is a proper subalgebra. A partial derivative in another coordinate fixes it. This establishes the required positive invariant without assuming that a polynomial isomorphism preserves R or the presented weights.

No unfilled central implication was found in this interface. The standard UFD, noetherian, DVR and Jacobian facts have the required domain/characteristic hypotheses here.

### 2. Principalization and normalized lifting

Primary source: imported-primary/sections/04-bundle.tex, full file; prop:principalization, prop:linearization and prop:homogeneous-lift.

The two charts D(z+1) and D(z) cover the base, with Laurent fiber coordinates a and d respectively. On their overlap d=(y/(z+1))a, and the transition unit is inverted by x/z because xy=z(z+1). These checks include the chart boundaries, rather than inverting a or d globally. They establish the line-bundle-complement description and faithful flatness. The exact principalization identities agree with the independent INITIAL derivation. Flat base change is applied to the actual coefficient inclusion R -> G. The proof of the single relation tau^2 V=v includes a tau-nonzerodivisor argument before using localization, so no hidden torsion is lost.

I separately tested the general lifting argument. For regular integral affine C, the Picard homotopy proof first removes horizontal divisors using the PID Frac(C)[t]. A residual height-one prime with nonzero contraction contains q[t] for a height-one q of C; equality follows because the ambient prime has height one. The pulled-back multiplicity is one, by the DVR uniformizer. Evaluation at zero supplies injectivity. These are legitimate uses of regular-local factoriality and divisor/Picard identification. The argument does not assume C itself is factorial.

An isomorphism between the two pullback line bundles is then normalized at the identity. Its possible ratios are units in C[t], and every such unit belongs to C because C is a domain. Normalization forces their ratio to be one, including when C has nonconstant units. The same argument over C[s,t] proves the action cocycle. The resulting additive action is algebraic and linear on fibers; on the affine complement its polynomial coaction gives a locally nilpotent derivation in characteristic zero. This checks existence, uniqueness and nilpotence rather than assuming an infinitesimal lift can be integrated.

For the degree assertion, the separate valuation torus fixes R and hence has a pullback lift extending linearly over the zero section. Conjugation and parameter rescaling are two normalized linear lifts of the same base action, so uniqueness identifies them. It follows that the lifted derivation has the original valuation shift and fiber shift zero. The additive action need not preserve R or the determinant coefficient ring. I found no coefficient-preservation assumption hidden in this step.

As a distinct hand control, the source's coefficient-moving LND on G has the explicit lift on the determinant presentation

    delta(a)=delta(d)=delta(b)=delta(c)=delta(tau)=0,
    delta(u)=-tau^2, delta(V)=3a^2u^2.

It preserves tau^2V-v and is locally nilpotent (delta^4(V)=0, delta^2(u)=0). It has valuation shift -2 and fiber shift zero while moving u out of the coefficient ring. It does not fix V, so it cannot have the positive-degree invariant needed for the extraction. This control tests the actual hypothesis distinction rather than trying to impose coefficient preservation.

### 3. Extraction with a moving parameter

Primary source: imported-primary/sections/05-reduction.tex, full file; red:pieces and prop:extracted-lnd, particularly the moving-tau case at lines 167-225.

The monomial reduction tau^2V=v gives exact degree components with unique coefficients in the determinant domain. Every positive component contains V. Since the kernel of an LND on a characteristic-zero domain is factorially closed by additivity of its order, the positive invariant forces delta(V)=0.

When tau is fixed, localization at tau preserves local nilpotence and coefficient extraction gives E with fiber shift zero and E(v)=0. When tau moves, delta(tau) cannot be divisible by tau. The exact degree pieces therefore force j=2ell+1, ell>=0. For every r in the determinant ring, delta(r)=tau V^(ell+1) E(r) with E(r) in that ring before any iteration is considered. Cancellation proves the derivation rule. The multiplier has fiber weight 2(ell+1), so the extracted shift is negative.

The subtle nilpotence test passes: writing m=nu_delta(tau)>=1, order additivity gives nu_delta(E(r))=nu_delta(r)-1-m whenever E(r) is nonzero. Every iterate remains in the coefficient ring and has nonnegative order, so this descent proves local nilpotence without localizing at a moving tau. Since nu_delta(v)=2m, a nonzero second E-iterate of v would have order -2. Thus E^2(v)=0. Nonzeroness is checked in both cases. This closes the precise central sign and nilpotence interface left open in INITIAL.

### 4. Highest part and rigidity

Primary source: imported-primary/sections/06-rigidity.tex, full file; prop:rigidity. The source's full Wronskian proof and one-variable LND lemma were also read.

The highest auxiliary component argument works with negative degrees because each derivation has finitely many shifts on the finite homogeneous generating set. In a highest-degree iterate every contributing shift is maximal, so local nilpotence passes to the nonzero top component. Commuting gradings preserve its fiber shift. The degree gap between a^3b and d^2+a^2u^3 ensures that E'^2(v)=0 gives E'^2(d^2+a^2u^3)=0; the lower term cannot contribute at the higher selected degree.

The orbit-polynomial argument agrees with the independent INITIAL reconstruction. The sum of the two nonzero orbit polynomials has degree at most one, so a common root of the summands would force an impossible double root. This proves the pairwise coprimality required by polynomial abc. The inequality forces the orbit of u to be constant. If the other orbits were nonconstant, cancellation of leading coefficients would make -u^3 a square in the original field C(a,d,b)(u). Its u-order is odd, so this is impossible. Passing to an algebraic closure was used solely for root counts; it does not supply a square root in the original coefficient field.

After a,d,u are fixed, the determinant identity gives the global, division-free coefficient h=cE'(b)-bE'(c), with E'(b)=ah and E'(c)=dh. Localization at invariant nonzero elements of C[a,d,u] and the one-variable lemma put h in C(a,d,u). Intersecting the a and d coefficient charts removes all denominators, so h belongs to C[a,d,u]. Nonzero E' implies nonzero h, but its fiber degree is e-2<0; that polynomial coefficient ring has no such nonzero homogeneous element. This is a complete terminal contradiction under the hypotheses furnished by the preceding steps.

The boundary controls remain necessary: the positive-root LND has shift +2 and E_+^2(v)=0, so omitting the nonpositive sign would be false. The negative-root LND has shift -2 but its second value is 6ab^3-2b^2u^3-2c^2, nonzero (for example at a=c=1,b=d=u=0). Characteristic zero and the odd exponent three are used essentially. Neither this proof nor the conclusion was transferred to characteristic p, an even exponent, or a real form.

## Relation to formal and computational claims

The exact actual Lean Model and Main have the manuscript's quotient over C, ordinary C-algebra equivalences and nonpolynomiality conclusion, rather than a grading-preserving or localized substitute. The selected full proof bodies show the alternative invariant-replica lift used by Main: it may rescale the original derivation by a nonzero invariant and then takes a highest valuation component. This differs from the printed normalized lift of the same derivation. It cannot be cited as formal certification of every printed intermediate proposition. No full kernel build or axiom report was produced here, and the original disclaims such reproduction. That disclosure is consistent with the evidence inspected.

The package's check_nonpolynomiality_certificates.py tests only explicit relations and positive/negative-root examples. It does not computationally certify the universal LND obstruction, and I did not run it. The hand proof above is the evidence for that universal statement. The stabilization script similarly certifies compositional identities rather than a fully expanded universal rho substitution; its seven rational samples cannot prove idempotence. The original proof correctly uses inverse maps and splitting for that purpose.

## Scope, remaining limits, and root disposition

No central mathematical defect or unsupported equivalent central conjecture was identified in this finite full-primary-proof reconstruction. The strongest supported scientific assessment is that the original explicit retract construction and its inherited exact complex nonpolynomiality argument withstand the adversarial tests recorded here and in INITIAL. This is an independently checkable written-proof assessment, with the native execution limitation stated above; it is not a new cancellation result or a machine-verification claim.

Native reproducibility is explicitly DEFERRED at the missing dependency, with no repair or quieter fallback. Full formal kernel verification and an exhaustive novelty determination were not performed. The historical audit was treated as bounded author evidence; no firstness conclusion was inferred from a failed search. The original assigns the general reduction to earlier literature and the cancellation breakthrough to OpenAI, and makes no ambient-four assertion. Its native API's absent version field remains separate from its printed manuscript date, published status, HTML v1 label and relation index.

No final catalogue, website, spreadsheet, release or publication disposition is assigned by this lane. That decision belongs to the root. Follow-up is null by default. No external contact or prepared outreach occurred. Source and frozen INITIAL bytes, modes and topology are guarded before/after the one native attempt and again at final closure.

Completion estimates at final closure: authorized finite adversarial review procedure 100%; broader independent scientific assessment 90%, reflecting the expressly deferred native replay, unreproduced full formal build and unestablished global priority. These estimates measure coverage, not mathematical confidence or proof probability.
