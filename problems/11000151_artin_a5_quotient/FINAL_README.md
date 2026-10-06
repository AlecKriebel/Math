# Reproduction

Run check_turn_1.py, check_turn_2.py, check_turn_3.py and check_turn_4.py using Python's standard library. Compare complete stdout to TURN_n_CHECKS.json. The second checker reuses the first's exact free-group functions. The third generates the ten-line survivor list if absent and otherwise verifies its exact bytes.

Then run verify_turn_4_cpp.py with an installed g++ supporting C++17. It compiles the second exact implementation in a temporary directory, hashes its full state-action stream and compares it with the Python receipt. No large stream file is retained. Running the compiled checker with --stream regenerates the complete90921-record certificate. Both programs compare full reduced words before hashing.

Read the written completeness proof and source scope; finite computations alone do not replace the classical topological and braid-group inputs. No external group solver or downloaded executable is used. Raw source files and exploratory work are not public artifacts. Earlier frozen proof/checker bytes are preserved.
