#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
cp=subprocess.run([sys.executable,'-m','pytest','-q',str(root/'tests/test_mutations.py')],cwd=root,text=True,capture_output=True)
(root/'logs/mutation_tests.stdout.txt').write_text(cp.stdout)
(root/'logs/mutation_tests.stderr.txt').write_text(cp.stderr)
print(cp.stdout,end='');print(cp.stderr,end='',file=sys.stderr)
raise SystemExit(cp.returncode)
