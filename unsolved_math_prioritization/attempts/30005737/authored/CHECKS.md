# Exact finite algebra diagnostics

Run:

    python3 check_algebra.py
    python3 -O check_algebra.py

Both runs produced the byte-identical CHECK_RESULTS.json. The script uses only Python's standard library and exact rational arithmetic; explicit RuntimeError checks remain active with optimization. It performs 2,896 individual conditions across the following small examples.

1. Target sl2(C), R=0 and R=−I: verify all post-Lie identities on basis triples, both homomorphisms j1=R+I and j2=R, perfectness and trace zero. At 17 rational SL2 group elements the global determinant is one.
2. Target sl2(C), R equal to minus the projection onto span(e,h): verify the post-Lie identities and homomorphisms. The source is nonunimodular, with trace(ad h)=−2. For p=[[a,b],[c,d]] of determinant one, the determinant in the proof equals a². The tested identity element has determinant one, whereas the Weyl element has determinant zero. Full matrix covariance is verified at 51 rational action/group-point combinations, retaining the nontrivial source modular factor. This illustrates precisely why the unimodularity hypothesis cannot be dropped.
3. Target sl2(C)⊕sl2(C), R(a,b)=(0,a): R is nonzero with R²=0; j1=I+R identifies the derived source with the semisimple target. Verify all post-Lie identities, the two homomorphisms, the covariance formula, and constant determinant at 17 rational group/action combinations. This is a nonsplitting semisimple positive control.
4. Target sl2(C)⊕C², source sl2(C)⋉C², with the natural action used for the post-Lie product: verify perfectness, trace zero, all identities, and the nonzero abelian radical. This credited boundary example (Burde–Dekimpe–Monadjem, Example 3.13) confirms that replacing semisimple target by reductive target would be false.
5. The invalid choice R=I on sl2(C) is detected by failure of the Lie-homomorphism condition.

These are diagnostic consistency and negative controls, not a proof of the general statement, a search over all post-Lie products, or computational verification of integration, covering theory, analytic continuation, or homology. They are not additional substantive author approaches.
