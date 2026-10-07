# Dependency ledger

Validation basis and exact hypotheses are being assembled. A catalogue entry or comparator sorry is not evidence of proof.

| ID | Precise dependency | Source/version | Validation basis/status | Exact remaining gap |
|---|---|---|---|---|
| D1 | For full-dimensional origin-symmetric K,L⊂R^n, n>=1, volume of W[h_K^(1-t)h_L^t] >= |K|^(1-t)|L|^t for 0<=t<=1 | OpenAI family091, pin adc7f1241b42e322a6451854ab7e4b4c146bf78a, introduction.tex Theorem1.1 | Exact statement read; manual and actual Lean audits underway | Verify tensor/density/moment proof, build and assumption closure |
| D2 | Smooth positive even Lp data has existence and, assuming the Lp-BM inequality, uniqueness for 0<=p<1 | He–Liu arXiv:2510.21530v1, Theorem4 and §3 | Actual proof under independent audit | Normalize ambient dimension; check existence; repair derivative algebra if needed |
| D3 | Smooth moment potential for compact ball target with centered smooth positive density, gradient diffeomorphism onto target interior | Berman–Berndtsson2013 Theorem1.1 | Original primary source audit underway | Check precise compact target/boundary assumptions |
| D4 | Moment Hessian cap 4/eps for target log-density Hessian >=eps I | Klartag arXiv:1309.2767v1 Prop3.1 and Remark3.5 | Original primary source audit underway | Verify cap and applicability to truncated balls |
| D5 | Nonsmooth Wulff first variation, log-BM=>log-Minkowski, Jensen=>Lp mixed-volume bound | BLZY2012 Lemma3.2; independent argument | Derivation underway | Verify first variation/equality without full-support assumption |
| D6 | Minkowski first mixed-volume inequality and equality precisely homothetic translates for full-dimensional bodies | Classical convex geometry, primary references to be recorded | To be checked | Apply only after support-ratio equality on dS_K |
| D7 | Smooth positive even Lp density admits positive-curvature C∞ symmetric body for 0<=p<1 | Established existence/regularity sources cited by He–Liu | To be checked | Do not infer smoothness from mere measure existence |

All follow-on claims will state exactly what is inherited and what is independently derived. No full follow-on Lean formalization is claimed.
