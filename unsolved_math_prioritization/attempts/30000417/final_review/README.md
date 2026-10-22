# Replaying this independent review

Read ADVERSARIAL_REVIEW.md for the full source/proof verdict and additive Python runtime qualification. INTEGRITY.json and REMOTE_BINDING.json bind the exact reviewed author packet. AUTHOR_REPLAY.json records the full byte-matched author outputs; CPP_REPLAY.txt records the independently rerun optional packed closure.

Run:

    python check_independent.py --packet /path/to/frozen/author/checkpoint

Its stdout must match INDEPENDENT_CHECKS.json. Only standard-library Python is required. The checker reads frozen anchor_solver.py and TURN_4_CERTIFICATE.json in the supplied author directory. The complete author closure replay instructions remain in FINAL_REVIEW_REQUEST.md; turn5 may take around two minutes and several hundred megabytes.

The optional compiled C++ replay used g++ -O3 -std=c++17 crosscheck_turn5.cpp and arguments9 6 2 8000000 with a local binary output path. It completed, rather than hitting the cap. The large generated state binary is not included; its exact byte count and SHA256 are in INTEGRITY.json. No source PDFs or private notes are included.
