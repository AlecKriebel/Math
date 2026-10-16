# Independent adversarial geometry review of PR585

Reviewed head: `0a94b2a7e8d682af7d51a3fba7fe8df4a36f6f27`, problem30001232. Review completed2026-10-15UTC. Verdict: **PASS for the complete stated counterexample family; no required mathematical repairs and no fatal gap found.** This is an internal AI verification, not human peer review, formal verification, or a priority certificate.

The strongest verified statement is that for every integer d>=7 there is a smooth integral complex projective surface S with ample canonical bundle, an ample integral line bundle L with L²=6, and an integral curve C through x with L.C=1 and multiplicity d-1. Its canonical square is 6(d-1)(d-3). Therefore epsilon(S,L;x)<=1/(d-1)<1/(2+(K²)^(1/4)). The degree-seven instance has canonical square144 and multiplicity6. I found no unresolved geometric gap in that assertion. Historical novelty remains outside this family's acceptance and requires the separate priority reviews.

## Independence and authenticated scope

The source-first `EARLY_CHECKPOINT.md` was written at2026-10-15T06:21:00.029142+00:00 before opening the candidate proof or previous audit. It records the exact target and a reconstruction of the global cover/ampleness mechanism from the assigned proposed construction, rather than from an older verdict. I subsequently read the complete frozen author proof, author README/source/log/result, release note/manifest, all executable verification sources, and only then the old audit/report/results/manifest. No original file was edited.

`ORIGINAL_GIT_AUTHENTICATION.json` checks all18 original files byte-for-byte, including sizes and SHA256, against their Git blobs at the pinned head. The current snapshot digest is included there. All18 files were checked unchanged after isolated execution. The original outer release manifest, author plain SHA256SUMS, audit-author bindings, and audit file bindings pass the actual original verification programs. This authenticates the packet under review; it does not make a self-supplied manifest a mathematical or novelty oracle.

## Exact target, not the catalogue variant

I inspected the complete primary OWR21/2009 printed page1124/PDF24, including its formula visually. Conjecture2 concerns minimal surfaces in the inherited smooth projective setting, arbitrary Picard number, ample line bundles, and arbitrary points. The additive2 lies outside the fourth root of |K²|. Preprint0711.0584p7 and Primer0810.0728v2p17 were independently read and visually checked as corroboration. This counterexample uses an ample bundle, not a very ample one, and a special point, not a very general one; both are permitted. It varies the underlying surface with d and does not claim vanishing of a lower bound on one fixed surface. No Picard-rank-one theorem is contradicted.

## Existence of a sufficiently good pencil

Although the separate pencil/local-algebra family studies this in more detail, the global argument relies on more than generic smoothness. I verified its prerequisite logically. The explicit degree-d homogeneous form is primitive and degree one in Z over C[X,Y], with coprime coefficients, so Gauss's lemma proves global irreducibility. The tangent cone at the specified point is square-free of degree d-1; the derivative calculation excludes other singularities.

For each positive factor split d=a+(d-a), the image of the projective multiplication map is closed and has dimension at most N_a+N_(d-a). Direct algebra gives N_d-(N_a+N_(d-a))=a(d-a)>=d-1. The finite union of these images includes all reducible and nonreduced forms. The join of this closed locus to the specified irreducible form has dimension at most N_d-(d-2), strictly below N_d for d>=3. Its complement is a nonempty open subset. A second pencil generator chosen there makes every pencil member integral, not merely its general member.

The full degree-d linear system is basepoint-free and separates first-order directions. Smoothness of the second generator, nonvanishing at the specified singular point, and transverse meeting with the smooth locus of the first curve are simultaneous nonempty open conditions. Their intersection with the previous complement is nonempty in the irreducible parameter space. Bezout gives exactly d² distinct transverse basepoints. At each one the two generators form regular parameters; one blowup resolves the pencil, the exceptional curve maps isomorphically to the base, and each strict-transform member is the entire fibre. There is no remaining exceptional vertical component or infinitely near basepoint.

Bauer1999 Proposition3.3 is classical provenance for this polarization mechanism. Its d=m+1 sentence on preprintp13 is explicitly asymptotic. I did not use that sentence as a finite-d7 certificate: the preceding elementary parameter-space argument supplies that finite degree independently. The candidate and release note make the distinction.

## Ampleness of the intermediate polarization

On Y, F is the pullback of O(1) from the pencil base and hence nef. For A=2F+E1, direct intersections give A²=3, A.E1=1, A.F=1. Let D be any other integral curve. If F.D>0, then E1.D>=0 because D and E1 are distinct effective curves on a smooth surface, so A.D>0. If F.D=0, the restriction of the map to D is constant: a nonconstant morphism of proper integral curves has positive pullback degree. Thus D is contained in a fibre. Because every fibre is reduced integral, D is the entire fibre, and A.D=1. This accounts for every curve, including all other exceptional sections. Nakai-Moishezon now proves ampleness.

The all-integral-fibres condition is essential. A vertical component missed by E1 would have zero A-degree. The candidate proves its exclusion rather than silently applying Bertini to all pencil members.

## Finite flat double cover and smoothness

Choose four distinct smooth fibre values, all different from the specified singular fibre value. The nonsmooth-fibre values form a finite subset: properness makes the critical image closed, and the pencil has smooth general fibre. There remain arbitrarily many permissible values. A square-free quartic in a coordinate avoiding infinity gives a connected double cover B of P1 with those four simple branch points; its smooth projective completion has genus one by Riemann-Hurwitz.

The base change S=Y×P1B is finite flat of rank two over Y, since this property survives base change. Concretely the cover is Spec_Y(O_Y direct-sum O_Y(-2F)), where multiplication is determined by the section with divisor the four smooth fibres. This confirms both flatness and the exact square-root line bundle, without assuming normalization repairs anything.

Away from the branch fibres the base change is etale over smooth Y, including over the singular points of the selected bad fibre. At a branch point, f is smooth; analytic or completed local coordinates give t=v² together with an independent surface coordinate. Thus S is already smooth. The branch divisor may be disconnected: four disjoint smooth fibres form a smooth reduced divisor, and connectedness of that divisor is not required.

The function-field cover cannot split. In a local rational trivialization its defining square class has valuation one along any branch fibre. A rational square has even valuation, so the generic quadratic extension is a field. The rank-two locally free algebra injects into that generic algebra; together with smoothness this proves integrality. Alternatively, the proper map S->B has connected fibres inherited from the integral pencil fibres and connected base; a disconnection of S would give a disconnection of B through the disjoint closed images, impossible. A connected smooth scheme over C is integral here. This also rules out accidentally obtaining two copies of Y globally.

Since Y and B are projective, their fibre product over P1 is projective. Equivalently, finite over projective Y is projective in this setting. There is no hidden resolution, contraction, singular-surface convention, or analytic-only construction.

## Canonical line bundle, minimality and general type

The differential relation dt=2v dv gives ramification multiplicity one along the smooth ramification fibres. The cover construction identifies O(R)=pi*O_Y(2F), so the Hurwitz formula is the line-bundle equality K_S=pi*(K_Y+2F), not merely a numerical guess. This agrees with the author-primary Pardini cover formulas and smoothness criterion. There are no extra terms from other singular fibres because the cover is etale there.

Write N=K_Y+2F=(d-3)H+F. Both H and F are nef. Every exceptional curve has N.Ei=1. Every nonexceptional integral curve has positive plane degree e=H.D, so N.D>=(d-3)e>0 for d>=4. Its square is 3(d-1)(d-3)>0. Nakai-Moishezon therefore gives N ample. This also verifies the candidate's alternate Bezout proof: choosing a different smooth pencil member gives sum r_i<=de, with the same positive lower bound.

Finite-surjective pullback preserves ampleness, as checked in Stacks Lemma30.17.2. Consequently K_S is ample and L=pi*A is ample. An ample canonical bundle is big, hence S is of general type. A smooth rational (-1)-curve would have K-intersection -1 by adjunction, contradicting ampleness, so S is minimal. The original exceptional sections become elliptic curves isomorphic to B, with self-intersection -2 and canonical degree2; they are not rational (-1)-curves. This directly answers the nonminimality concern raised by the intermediate blowup.

The degree-two projection formula gives K_S²=2N²=6(d-1)(d-3) and L²=2A²=6. These are not asymptotic estimates.

## Individual fibre splitting and multiplicity

At the selected unbranched value t0, the scheme-theoretic inverse image in B consists of two distinct reduced C-points b1,b2. Base change therefore gives pi^-1(C)=C×{b1,b2}, the disjoint union of two copies, each isomorphic to C as a scheme. This is stronger than merely knowing the total cover has degree two. A connected degree-two cover of the singular curve is not what occurs.

Choose one copy C' and x above its multiple point. The copy is integral; it retains multiplicity d-1 because it is isomorphic to C (and the ambient etale local maps preserve the relevant multiplicity). The projection formula on this individual copy gives L.C'=A.C=1. In contrast, the total divisor pi*F consists of two fibres and has L-degree2. Distinguishing the individual fibre from its total pullback is necessary and is correctly done.

In numerical classes on S, if Q is one fibre and T=pi*E1, then pi*F is numerically2Q, T²=-2, T.Q=1, and L is numerically4Q+T. Thus L²=6 and L.Q=1. Only numerical equivalence of different point fibres of the elliptic base is used; they need not be linearly equivalent. A rational normalization of the singular fibre causes no genus contradiction: its arithmetic genus is (d-1)(d-2)/2 and its ordinary (d-1)-fold point has exactly that delta invariant.

The Seshadri definition takes an infimum over all integral curves through x, so this one admissible curve gives the claimed upper bound. It is unnecessary to prove the exact value of epsilon. The strict comparison is equivalent, for d>=7, to (d-3)^3>6(d-1). It holds at7 and its successive difference is positive. For d=7, the particularly transparent check is144<4^4. Degrees4,5,6 do not meet this strict comparison for this four-branch construction and were retained as negatives.

## Reproduction and fresh falsification controls

The original author intersection program, author formula program, old independent program, release verifier, and integrity regression program were all executed in an isolated exact copy, using Python3.9.6/SymPy1.14.0. All three saved mathematical output files matched byte-for-byte. The original release replay checks all17 manifest payload entries; the integrity program rejects its8 recorded corruptions, including changed/missing/extra/symlink/traversal/duplicate/optimized execution. Original and isolated inventories remained unchanged. Full receipts are in `ORIGINAL_REPRODUCTION.json`.

The new `geometry_controls.py` tests a materially distinct cover-algebra and failure-mode family. Its1183 deterministic checks cover monic quadratic rank-two reductions, a square-free quartic's four branch points, CRT splitting at a chosen unbranched bad value, smooth-branch local equations, and the local failure caused by branching at a singular fibre. It separately checks the single-fibre/section lattice, adjunction, the d=6 negative threshold, canonical degree failure with only two branch fibres, the vertical-component obstruction, and failure of direct polarization descent under blowdown. It does not instantiate a random pencil or substitute finite algebra for the existence proof.

The complete new JSON output is byte-exact under the root's isolated Python3.14/SymPy1.14.0 environment as well. Optimized execution is explicitly rejected. `FRESH_CONTROL_REPLAY.json` records that independent runtime comparison. The count is a number of controls of formulas and failure modes, not a number of independent geometric proofs.

## Disposition and limits

No theorem, constant, hypothesis, global construction step, or mathematical repair is required by this audit. A future paper should retain the short identity N=(d-3)H+F, explicitly credit the classical Miranda/Bauer mechanism, explain the individual fibre splitting, and avoid treating Bauer's asymptotic citation as the finite-degree proof. These are already present in the complete candidate or its release clarification and are not unresolved findings.

This review does not establish historical novelty, present open status, or lack of a previously published counterexample. Its source reading was scoped, as recorded precisely in `SOURCE_LEDGER.json`; no full-reading claim is made for the full OWR report, survey, Pardini talk, or general ampleness literature. Primary source bytes, text extractions and renders remain only in ignored `.cache` and are not publication payloads. No outside individual or other shard was contacted, no remote write or Git mutation was performed, and the open editor was untouched.
