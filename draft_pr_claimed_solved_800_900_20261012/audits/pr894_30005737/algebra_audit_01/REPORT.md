# Algebraic audit: PR 894 / problem 30005737

Family: ALGEBRAIC POST-LIE / TRANSVERSE-PAIR. Frozen candidate head: 401f86e018e8cc5075e37a29bae9350eb9f89c36. Validation of the existing 1/5 candidate; no additional substantive proof-search turn.

## Decision

**PASS for this assigned algebraic family and exact target match.** No mathematical defect was found. The stronger unimodular-source transverse-pair theorem is correctly stated. Reading the full proof found a coherent global deduction, conditional only on the explicit classical inputs listed below. This algebra-focused audit does not replace an independent source verification of those global inputs. Novelty and exhaustive current literature status were not assessed.

Strongest independently verified statement: for finite-dimensional complex Lie brackets g and n on one vector space, with n semisimple, every post-Lie product has a unique linear R with x*y={R(x),y}; both R and R+I are homomorphisms g -> n and their difference is I. Perfectness of g implies unimodularity. Conversely, a homomorphism pair with invertible difference gives this construction after transport of the source bracket. There is **no remaining algebraic gap**.

## Source authentication and independence

Check 004 authenticated all 18 files against the external byte/SHA256 pins, recomputed their Git blob identities, and compared every file with the actual Git blob bytes; all Git subprocess return codes were zero. Manifest SHA256: 1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c. The complete native canonical pair matches 3524 bytes and SHA256 b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298.

TARGET_FREEZE.md and INDEPENDENT_APPROACH.md were saved at 2026-10-16T07:02:29.187306+00:00 before authored/PROOF.md was read in check 006. No historical audit verdict was read. The candidate algebra checker was inspected in successful retry 016 before replay 017. No Git refs, index, checkout, push, publication, or external communication was performed.

## Exact claim and conventions

The native target is nonexistence for perfect nonsemisimple complex source g and semisimple target n. The [official Oberwolfach report](https://ems.press/content/serial-article-files/48175), printed p.2689, presents the sl3 case and proposes the general semisimple extension, in the same source/target order. The surrounding discussion fixes a common vector space.

The [primary paper, Definition 2.5, Proposition 2.6 and Section 2](https://arxiv.org/html/2311.08985v1) confirms the signs, difference-map characterization, and finite-dimensional setting. The candidate explicitly states that setting, appropriately resolving the abbreviated native clean statement's omitted qualifier.

With [,] the source bracket and {,} the target bracket, the identities are
\[
x*y-y*x=[x,y]-\{x,y\},\qquad
L([x,y])=[L(x),L(y)],\qquad
L(x)\in\operatorname{Der}(n).
\]
These are exactly the candidate's convention.

## Independent algebraic verification

### Inner derivations, uniqueness and linearity

Target semisimplicity supplies its nondegenerate Killing form B and zero center. The inner-derivation input can be checked directly: for D a derivation, define z by
\[
B(z,x)=\operatorname{tr}(D\operatorname{ad}x).
\]
Since [D,ad(x)]=ad(Dx),
\[
B(Dx,y)=\operatorname{tr}([D,\operatorname{ad}x]\operatorname{ad}y)
=\operatorname{tr}(D\operatorname{ad}[x,y])
=B(z,[x,y])=B([z,x],y).
\]
Thus D=ad(z). Target centerlessness makes ad injective, so it is a linear isomorphism n -> Der(n) and
\[
R=\operatorname{ad}_n^{-1}\circ L
\]
is linear and unique. No centerless-source assumption occurs. Perfect sources with central radical directions remain covered.

### The two signs

The representation identity and injectivity of target ad imply
\[
R([x,y])=\{R(x),R(y)\}.
\]
The skew-product identity gives
\[
[x,y]=\{R(x),y\}+\{x,R(y)\}+\{x,y\}.
\]
Expanding the target bracket yields
\[
\{(R+I)x,(R+I)y\}=R([x,y])+[x,y]=(R+I)[x,y].
\]
Hence j1=R+I and j2=R are ordinary homomorphisms to n. The second factor has the usual bracket; R-I is generally incorrect. The inverse in the group action J1(h)pJ2(h)^(-1) is compatible with these two ordinary homomorphisms.

### Same vector space and transverse pairs

The combined map x -> (j1x,j2x) is injective, since its component difference is injective. Its image intersects the diagonal trivially and, by dimension, complements the diagonal in n direct-sum n.

For abstract maps with T=j1-j2 invertible, transfer the source bracket to n through T and put R=j2 T^(-1). Then j1 T^(-1)=R+I, and the two homomorphism equations plus Jacobi give all three post-Lie identities for {R(x),y}. This checks the common-vector-space identification exactly.

The theorem's equal-dimension clause is redundant once T is called an isomorphism, but it emphasizes the square determinant. Equal dimensions alone or an injective difference alone cannot replace invertibility.

### Unimodularity

The functional lambda(x)=tr(ad_g x) satisfies
\[
\lambda([x,y])=\operatorname{tr}([\operatorname{ad}x,\operatorname{ad}y])=0.
\]
Perfectness makes it zero everywhere. No semisimplicity of g was smuggled into this argument. The stronger theorem legitimately replaces perfectness by unimodularity and does not swap the two algebras.

## Exact falsification and boundary diagnostics

The independent standard-library checker uses integers and Fractions, testing every basis tuple in the multilinear post-Lie and Jacobi identities. Successful check 015: rc=0, output SHA256 20528434d13d618c0e07a9f381d8e1f30095cf49f7aaf6dc4e8f8c03662a7a48.

1. **Dropping nonsemisimplicity:** g=n=sl2 with zero product is post-Lie. The opposite source bracket with product minus the target bracket is also post-Lie and independently checks the minus sign.

2. **Dropping source unimodularity:** use n=sl2, basis (h,e,f), brackets {h,e}=2e, {h,f}=-2f, {e,f}=h. Let g have only [h,e]=2e and R=-P_f. Product {R(x),y} passes all identities. The source is solvable with tr(ad_g h)=2. R and R+I pass all homomorphism checks; R-I fails six ordered basis pairs. Exact matrix conjugation computes det(B_p) as 1 at the identity, 1/4 at diag(2,1/2), and 0 at a Weyl representative. Thus transversality at the identity alone does not imply global transversality.

3. **Weakening target to reductive:** let g=sl2 semidirect C^2 with its natural action and n=sl2 direct-sum central C^2. Product (a,u)*(b,v)=(0,av) passes all identities. Source derived rank is 5 and all adjoint traces vanish; its C^2 is a nonzero abelian ideal. This reproduces [the primary paper's Example 3.13](https://arxiv.org/html/2311.08985v1). On the target, ad has a kernel and derivations acting on the center need not be inner, explaining the precise failure of the reduction.

4. **Injective nonsurjective difference:** embed the same perfect nonsemisimple 5-dimensional g into sl3 by the trace-zero affine block matrix with 2x2 block A and final column u. Take j1 to be this embedding, j2=0. Every homomorphism check passes; difference rank is 5 into target dimension 8. This falsifies only the weakened injective-difference assertion.

5. **Equal dimensions and singular difference:** take g to be the 6-dimensional Takiff algebra sl2 semidirect sl2_ab, n=sl2 direct-sum sl2, j1 Levi projection into the first factor, j2=0. Checks give source derived rank 6, all adjoint traces zero, difference rank 3, and no homomorphism violations. The abelian second source copy is a nonzero ideal. Equal dimensions and perfectness therefore do not substitute for transversality.

No positive example satisfies all original hypotheses. Dimension zero is harmless: an invertible difference forces both algebras zero, which is semisimple by convention. No positive-characteristic, infinite-dimensional, or arbitrary-real-form extension was tested or inferred.

## Full-proof reading and remaining dependencies

The covariance identity
\[
B_{A_h(p)}=\operatorname{Ad}_{J_2(h)} B_p\operatorname{Ad}_{h^{-1}}
\]
has the correct source/target adjoints and inverse signs. Zero differential of each connected-group determinant character gives determinant one. Holomorphic constancy on the nonempty open orbit extends to connected N; all orbits being open then forces transitivity. No closed-image assumption is used.

The stabilizer is the actual closed identity preimage with zero Lie algebra, hence discrete. The proof identifies N=G/H before invoking the discrete-subgroup covering theorem. It does not use the false general implication that every surjective local diffeomorphism is a covering.

The solvable-group induction is valid: a nonzero solvable algebra has a codimension-one ideal containing its derived algebra, and each one-dimensional complement is a subalgebra. Integrating semidirect products reduces the dimension and gives a contractible radical group. Central radical directions pose no exception.

The exact imported inputs not independently source-verified in this assigned algebraic audit are:

- finite-dimensional complex simply connected integration and integration of homomorphisms;
- Levi decomposition and integration of semidirect products;
- compact real forms and polar decomposition for simply connected complex semisimple groups;
- closed-stabilizer homogeneous spaces, discrete-subgroup coverings, and top homology of compact connected orientable manifolds.

With these standard inputs in the stated scope, the final contradiction is valid. N has H_d=Z, d=dim_C n; if g has nonzero radical, G has the homotopy type of a compact Levi form of real dimension strictly below d and has H_d=0. The exact remaining review dependency is validation of these classical inputs, not a new unsupported algebraic theorem equivalent to the original conjecture.

## Candidate replay and preserved failures

After inspection, the author's checker replay 017 returned rc=0 and 2896 checks. Its output SHA256 2a0062610f5116c92c3689cbb2d12747260d0f42664a277cbb41aee3424046ff exactly matches the authenticated CHECK_RESULTS.json. These finite diagnostics do not replace the global proof.

Failed independent check 013 guessed two failing basis pairs for the deliberately invalid R-I map; the actual count is six. Correction 014 removed that unjustified exact-count expectation; 015 passed. This was an audit test-expectation error, not a candidate defect. The failed script hash and output are retained.

Intermittent ENOSPC caused one output-persistence failure and two recovery failures. Shell return codes and the unavailable original timestamp limitation are preserved in checks/010_failures.json. Only this audit's duplicate captures were removed, with prior hashes retained and the unchanged originals still available; primary-web captures were compressed. The initial directory listing lacked persisted metadata and was not used as mathematical evidence. A report-writing tool call also failed at JavaScript parsing before any subprocess ran; it did not modify files or produce a mathematical result.

Optional exposition repair: add the explicit formula R=ad_n^(-1) L for linearity. The candidate's existing assertion is already correct; no substantive repair is required. This audit does not endorse novelty, a PR-status change, publication, or an immutable release.
