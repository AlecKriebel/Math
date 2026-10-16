# Direct geometry adversary research log

- 2026-10-12 11:39:06 UTC — Checkpoint 1, 10% complete. Independent plan and
  ray/tangent/normal Cartesian derivation frozen before reading submitted proof
  or old verdicts. Exact rational axis four-period control derived by hand.
  Family mechanism: physical billiard reflection and line intersections;
  evidence: independent formulas and exact N=4 vertices; gap: universal mean
  identity, real finiteness, star controls, and source repeated-period scope.
  Independence limitation: inspected only permitted source/metadata/README;
  overbroad first inventory exposed unrelated file names but no arguments.

- 2026-10-12 11:43:54 UTC — Checkpoint 2, 45% complete. Still no submitted
  proof/code or old verdict read. Completed 75 primitive even direct ray cases
  at 70 digits (five aspect ratios, 15 period/winding pairs, six phases each),
  and nine difficult stability cases at 140 digits including a/b=100 and
  N=30,p=13. No real determinant failure. Largest scaled phase variation:
  1.06e-38 at 70 digits, 5.51e-87 at 140 digits; challenging star cases are
  highly conditioned. N4 mean zero is supported. Exact triangle counterexample
  is certified by all-zero quotient-ring boundary/caustic/reflection residuals:
  a=5,b=3,t=(sqrt(481)-9)/16, lambda=225(sqrt(481)-17)/128; a triangle and
  its central reflection have mean x approximately 25.8302465064 and
  -0.685528166 about M=(4,0). Repeating either twice retains its mean and
  nominally gives N=6. Hence even-list extension is false. Strongest exact
  result so far: rational N4 control and repeated-odd counterexample.
  Universal primitive-even argument and source wording remain to audit.

- 2026-10-12 11:47:52 UTC — Correction and checkpoint, 60% complete.
  After the pre-proof freeze, read the full submitted PROOF.md and author
  verification scripts (no old reviewer verdicts/code or other family
  derivation read). Manual line-by-line audit found the original-focus
  tangent identity, real determinant, four singularity classes, residue
  quartet and rectangle argument consistent. Source Table 5 supplies constancy
  and an unspecified value, not a direction sign; submitted theorem asserts
  C(-M)=-C(M), not C(M)_x<0 for M positive. My initial plan treated negativity
  as an extra hypothesis and my earlier message inaccurately said numerics
  supported it before aggregating the stored sign flags. Root provided an
  adversarial k=.63,N8,p3 sign test; upon checking my own already-frozen
  data, 30 primitive even families have positive mean x. For example
  a=1.0001,b=1,N8,p3 gives x=0.03415706398 and a=1.2,b=1,N8,p3 gives
  x=3.66251922. The extra universal direction-sign hypothesis is falsified;
  the submitted theorem is unaffected. No sign claim will be promoted.
  Primary sources were browsed (arXiv v11, final Table 5, Stachel Theorem4.3,
  DLMF22.4/22.8); no literal primitive/gcd qualifier found in the two target
  papers' text, while Stachel explicitly requires gcd(N,tau)=1. Root's own
  alternate exact odd witness details remain unread to preserve provenance.

- 2026-10-12 11:51:17 UTC — Checkpoint 4, 80% complete. Independently derived
  a purely real Euclidean lemma proving all antipedal intersections finite
  for every strict elliptic-caustic orbit and every strictly interior M;
  no parity is needed for finiteness. Post-freeze actual tangent/normal
  intersections also checked five canonical families at 120 digits,
  including star k=.63,N8,tau3 suggested by root. Independently re-solving
  the physical caustic and tracing reflected rays at three phases gives
  x=1.780146638544216006266687370922135277466 for that star, explicitly
  falsifying any universal direction inequality. No post-freeze failures.
  Removable focal/dn/midpoint singularities, genuine endpoint poles and
  entire cyclic pole neighborhoods were tested through eps=1e-36;
  largest normalized complete cancellation residual was 6.51e-48.
  DLMF verifies the submitted shifts; Stachel's printed dn(u+2K) sign is
  erroneous, but PROOF.md uses the correct DLMF dn period 2K and does not
  inherit that error. Strongest verified claim remains primitive even
  constancy via reviewed analytic proof plus independent geometry controls;
  no mathematical defect found. Source least-period qualification must be
  explicit because the even repeated-odd extension has an exact counterexample.

- 2026-10-12 11:55:45 UTC — Final checkpoint, 100% of assigned family audit
  complete. REPORT.md gives full assumptions, evidence provenance, each
  submitted proof step, exact rational N4 and odd-repeat controls, direct
  Euclidean finiteness lemma, primary-source locators, limits, and reproduction
  instructions. No scoped theorem defect found. Exact even-list extension is
  false and must remain qualified by even least period. Opposite-focus
  negation is verified; a fixed direction inequality is false and was not
  submitted. No priority/novelty/publication verdict attempted. Final manifest
  verifies all 26 frozen submitted bodies read-only against INTAKE.json and
  pins this family's own complete evidence; source PDFs/full texts and caches
  are excluded from public selection. No outside individual contact, Git
  action, provider write, frozen-input modification, or shared control edit.
