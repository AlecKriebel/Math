# Independent supplementary formula counterexample freeze

Recorded by the native writing process at 2026-10-04T07:15:19.731259+00:00. This is a post-ZIP finding; the two earlier independent freezes remain unchanged. Review object: the six input pins in inputs/PINS.json, including the frozen author ZIP, never repaired here.

Verdict for this issue: NEEDS_REPAIR. This does not invalidate the main manuscript theorem. It does invalidate the generic quantity named dual_kernel_formula in public controls/verify_intrinsic.py, which accepts arbitrary matrices and reports this quantity among its nonprime basis-change invariants.

Let k=F5[t]/(t^3+t+1). The cubic has no F5 root and is irreducible. sigma(x)=x^5, sigma^-1(x)=x^25. Encode a+b*t+c*t^2 by a+5b+25c. Then t=5, t^5=106, t^25=44; these last two are distinct.

For matrices A,B of sigma- and sigma^-1-semilinear operators, put C=A*sigma(A), D=B*sigma^-1(B). They represent the second powers with scalar twists sigma^2, sigma^-2. The dual first-power matrices are sigma(B)^T, sigma^-1(A)^T. Multiplying with the appropriate semilinear twists gives dual second-power image matrices sigma^2(D)^T and sigma^-2(C)^T. Consequently delta2(Mdual)=rank(C)+rank(D)-rank([sigma^2(D)^T | sigma^-2(C)^T]). The author helper instead uses rank(C)+rank(D)-rank([C^T | D^T]); individual ranks agree, while their union need not.

A minimal exact witness is P=I+t E_01 (zero-based indices). Starting with manuscript matrices A0,B0, whose squares are E_20,E_40, use A=P^-1*A0*sigma(P), B=P^-1*B0*sigma^-1(P). Then C=P^-1*E_20*sigma^2(P)=e2*(e0^T+t^25 e1^T), D=P^-1*E_40*sigma^-2(P)=e4*(e0^T+t^5 e1^T). Their image lines are distinct, so delta2(M)=0. Their untwisted row lines are distinct because t^25 differs from t^5, giving the author's quantity 0. Their actual semilinear kernels both equal P^-1<e1,...,e5>; their annihilators coincide, and the actual dual intersection has dimension1. Applying the opposite twists makes both displayed row lines e0^T+t e1^T, yielding the corrected quantity1.

The independently selected dense unitriangular basis (encoding above) is:
[[1, 42, 58, 38, 108, 107], [0, 1, 30, 64, 115, 89], [0, 0, 1, 10, 43, 111], [0, 0, 0, 1, 85, 98], [0, 0, 0, 0, 1, 94], [0, 0, 0, 0, 0, 1]]
Its full inverse, A,B,C,D matrices and helper results are frozen in native/adversarial/system_formula_probe.stdout. That process actually invokes the frozen author helper: delta2=0, dual_delta2=1, dual_kernel_formula=0; corrected formula=1. The bundled process gives byte-identical complete stdout. Independently written independent_controls.py uses polynomial triples, different elimination, no author imports, and obtains the same dense basis and quantities. Both interpreters pass139 substantive assertions and8 meaningful rejected mutants. These finite checks corroborate the exact minimal symbolic witness, rather than establish a universal assertion.

Mandatory repair: compute opposite squared-Frobenius twists in the generic helper, and include this minimal or dense nonprime basis as an equality regression. Restricting to prime-field matrices would abandon the public generic/nonprime-basis control scope. Rebuild derivative pins, manifests, expected streams and ZIP consistently, retaining historical original controls and SOURCE_IDENTITY derivation history. Do not edit sealed original audit controls. A subsequent reviewer must review the revised complete packet anew.

All genuine argv, executable/version, cwd, UTC start/end, exit statuses and complete streams are in native/adversarial. No shared source was changed. The formula probe has exit0 because the advertised defect is its expected successful falsification; its printed verdict remains NEEDS_REPAIR. Native PASS_OF_REPLAY_EXPECTATIONS is not scientific acceptance.
