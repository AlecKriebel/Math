from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parent
original=(base/'private/extracted/verify_even_calculus.py').read_text()
needle='def shift(w): return tuple((t, i + 1, e) for t, i, e in w)'
assert original.count(needle)==1
mutant=original.replace(needle,'def shift(w): return tuple((t, i, e) for t, i, e in w)')
dest=base/'private/zero_shift_mutant.py'
assert not dest.exists()
dest.write_text(mutant)
print(json.dumps({'original_sha256':hashlib.sha256(original.encode()).hexdigest(),
 'mutant_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'only_change':'shared shift helper adds zero rather than one','actual_mutant_execution_pending':True},indent=2))
