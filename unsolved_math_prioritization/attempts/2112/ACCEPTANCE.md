# Acceptance of the fourth-power Hofstadter plateau bound

Status: accepted partial lower-bound theorem for EP423 / 2112. No mathematical
correction was required. The exact asymptotic remains unresolved by this work.

The classical seed is a_1=1, a_2=2. Each later a_n is the least integer strictly
larger than its predecessor expressible as a sum of at least two consecutive
earlier terms. For every integer n>=2, with all logarithms natural,

    a_n-n >= (log(log(n))-log(log(5)+log(2)/3))/log(4).

For a constant-deviation interval 3<=r<=s, put T=a_r and V=a_s.
The finite lemma proves V<Q<=2*T^2*(T-1)^2<2*T^4, where Q is the least
2*4^k strictly greater than T^2*(T-1)^2/2. The all-index deduction handles
both skipped deviation levels and nonempty plateaus, starting with M(0)=5.

This improves the specific log20 denominator displayed in Theorem 1.4 of
[Tang, arXiv:2603.09939v2](https://arxiv.org/abs/2603.09939v2), revised
23 March 2026. Tang's plateau and threshold-function strategy is explicitly
credited. The public manuscript is described as submitted; no journal
acceptance is asserted. The background upper bounds are credited prior work
and are not independently re-proved here.

The exact asymptotic, b_n=o(n), and even a_n=O(n) remain untouched. No global
novelty, priority, or optimality claim is made. Synthetic crossing examples
concern relaxed prefix lists; they are not established actual greedy prefixes
and cannot establish optimality of the plateau theorem or coefficient.

## Accepted identities and full-document preservation

The original candidate manifest SHA-256 is d8305c9503858d2e71313c6a3ce037b471641ddc29f720b94a393b8c4f0ca6e1.
The original proof is 6,624 bytes, SHA-256
afd65a9697245e62f25ee9ad9359b893e213d87d6bb46ad17724b73ccbb5297c.
The original independent audit manifest SHA-256 is cc4ab596fbc9b6eddd676d65fd48e1a2baf9c2b3ac777c2d99dcdc72df0b4b79.
The original full independent audit is 10,116 bytes,
SHA-256 5d97466ebdbe2b220d4495cac292273c41218b9dda61b47a552ba64ce3435a50.

The distributed proof is 7,566 bytes, SHA-256
6ff98a5240b1af8958c1e277bff40f5060d34d331629a6b6280c694a5ff8f84f.
The distributed full independent audit is 11,058 bytes,
SHA-256 db8e5b5d264d2a471191f605690c26609ed5bf7ef6e509f7049c627eb057ef7c.
Each original document is preserved byte-for-byte as the initial portion of
its public-edition file, followed only by the edition and review statement.
The original acceptance fields are retained in ACCEPTANCE.json with an added
edition note. These editorial additions do not change the theorem or audit.

## Verification interpretation

Historical independent exact checks used explicit exception guards and have
byte-identical reports under normal Python, -O and -OO. They include agreement
of separately implemented generators for 4,000 terms and agreement with the
candidate's complete through-value-200000 sequence hash. Ten package-integrity
negative mutations were rejected in each mode. The candidate's own
assertion-based verifier now rejects optimized Python. These are distinct
behaviors, not a claim that the candidate's mathematical assertions passed
under optimization. Finite checks supplement the written infinite proof.

## Edition and review statement

This prose-only edition preserves the complete substantive mathematical argument
and its qualifications. The AI-assisted work is unrefereed. Acceptance refers
only to the independent internal AI audit of this partial theorem; no external
human peer review, journal acceptance, or formal proof-assistant certification
is claimed. No mathematical correction was required.

The historical finite checks and scholarly-source inspection are described
for provenance. Preparing this edition added no mathematical test execution
and no scholarly-source retrieval or inspection. The original sealed candidate
and audit are unchanged. Programs, raw datasets, detailed execution receipts,
full computational certificates, copied source documents/text/images, and
private coordination material are not distributed. This is a mathematical
prose and verification-metadata edition, not an executable reproduction package.
