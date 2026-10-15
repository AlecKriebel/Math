--- original four-fifths mathematical candidate
+++ accepted corrected four-fifths mathematics
@@ -1,6 +1,6 @@
 # A four-fifths retention obstruction for canonical Bose–Chowla lifts
 
-12 October 2026. New candidate construction-specific theorem, frozen for independent audit. No novelty claim. No publication or repository mutation.
+12 October 2026. Independently audited correction edition of a construction-specific theorem. The source candidate is preserved unchanged; see AUDIT_REPORT.md for the corrections and acceptance scope. No novelty claim. No publication or repository mutation is part of this packet.
 
 ## Main theorem and scope
 
@@ -10,7 +10,7 @@
 
 The error is uniform over translations, unit dilations, and the two lift conventions separately. Since 4/5<sqrt(2/3), this passes that benchmark for this specific construction. It proves no bound for arbitrary Sidon sets, noncanonical lifts, longer ambient intervals, or mixed lattice cosets, and does not resolve Erdős 864. No effective field-order threshold is claimed.
 
-The proof has two established external inputs: polynomial Dirichlet L-function RH, already used in the accepted carry proof copied as DEPENDENCY_CARRY_PROOF.md; and tame rank-one character-sum RH on curves, applied through tensor induction as precisely described in Part I. These are established theorems, not unproved hypotheses. The new argument and its use of those inputs have not yet received independent acceptance.
+The proof has two established external inputs: polynomial Dirichlet L-function RH, already used in the accepted carry proof copied as DEPENDENCY_CARRY_PROOF.md; and tame rank-one character-sum RH on curves, applied through tensor induction as precisely described in Part I. These are established theorems, not unproved hypotheses. The new argument and its use of those inputs are independently accepted in the accompanying audit report, subject to its precise construction-specific scope.
 
 Part I proves all conditional source/target laws, enumerates the exceptional fibers and character resonances, and establishes uniform weighted incidence bounds. Part II gives an explicit smoothed coupling with mass approaching 1/5 and aggregate degree at most one. It applies directly to arbitrary deleted subsets; no geometric model or equidistribution is assumed for the deletion pattern. The same coupling and a dual certificate show that 1/5 is the exact optimum of this continuum fractional first-moment method, without claiming optimality for actual subsets.
 
@@ -146,7 +146,7 @@
 
 For a fixed target of normalized value X, its first two source coordinates y,z determine the third coordinate modulo one. Genuine equality occurs exactly on y+z<X, apart from seams and boundaries. Its area is X²/2.
 
-The half coset introduces only constant phases and the already-correct algebraic parameter μ=λ²g; none of the character arguments divide by two modulo q. For the integer lift, the one possible zero-residue point is represented by 1 rather than 0. On a nonexceptional source fiber, fixing either free source to this point leaves at most one solution, while fixing the target to this point leaves at most two by strong Sidonicity. Thus its seam correction is O(1). On any fixed-target fiber, fixing one source to the seam point leaves at most two ordered pairs, hence the total seam correction is O(1). Exceptional source fibers were already handled exactly. The value X=1 is therefore included: source count zero and target limiting count p/2.
+The half coset introduces only constant phases and the already-correct algebraic parameter μ=λ²g; none of the character arguments divide by two modulo q. For the integer lift, the one possible zero-residue point is represented by 1 rather than 0. On a nonexceptional source fiber, fixing either free source to this point leaves at most one solution, while fixing the target to this point leaves at most two by strong Sidonicity. Thus its seam correction is O(1). On any fixed-target fiber, fixing one source to the seam point leaves at most two ordered pairs, hence the total seam correction is O(1). Exceptional source fibers were already handled exactly. The value X=1 is therefore included: the source count is zero; the target count is p/2+o(p) at a nonexceptional target and is at most two at the possible exceptional target. In all cases the uniform target upper bound remains valid.
 
 These observations prove all the stated uniform conditional incidence laws and their upper-bound versions.
 
@@ -186,7 +186,7 @@
 
 # Exact one-fifth weighted deletion certificate
 
-12 October 2026. Authored exact continuum coupling certificate; not independently audited. This file proves the continuum weight construction and its arbitrary-subset covering consequence. The full uniform weighted per-point source and target incidence laws are proved in Part I. No publication or repository mutation is part of this file.
+12 October 2026. Authored exact continuum coupling certificate, independently audited in this correction edition. This file proves the continuum weight construction and its arbitrary-subset covering consequence. The full uniform weighted per-point source and target incidence laws are proved in Part I. No publication or repository mutation is part of this file.
 
 ## Application of the proved weighted incidence input
 
@@ -207,9 +207,9 @@
 The needed input is:
 
 - The total weighted number of ordered zero-carry equations is p²(M+o(1)).
-- At a seed vertex b whose normalized coordinate is t=b/q, the sum of its four weighted role incidences is p(D_W(t)+o(1)), uniformly in b and the allowed seed choices.
-
-It suffices to allow O(1) exceptional vertices with O(p) total weighted incidence each, or more generally errors whose sum over all p seed vertices is o(p²). The constants may depend on the fixed W. In particular, no uniformity over a shrinking smoothing parameter is required.
+- At a seed vertex b whose normalized coordinate is t=b/q, the sum of its four weighted role incidences is at most p(D_W(t)+o(1)), uniformly in b and the allowed seed choices.
+
+Part I proves this upper bound at every vertex, including the explicit exceptional fibers. More generally, O(1) exceptional vertices with O(p) total weighted incidence each would suffice, as would errors whose sum over all p seed vertices is o(p²). The constants may depend on the fixed W. In particular, no uniformity over a shrinking smoothing parameter is required.
 
 For any deleted set D_B whose complement has no zero-carry equation, weighted coverage gives
 

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
