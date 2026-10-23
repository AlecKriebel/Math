from pathlib import Path
import hashlib,sys
p=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/final_reconciliation_new_independent_adversary01/verify_actual_final_reconciliation05.py')
b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='05d0cbeab04c4b00a13b5ca8cc455e128945bf6b4376d9f2a8c34e4798fdc537'
sys.argv=[str(p),'--manifest-sha256','c7f0dd65921c241e0fa86f59fc910464752eebe4ca2a2e941628518b2f70c851']
exec(compile(b,str(p),'exec',optimize=0),{'__file__':str(p),'__name__':'__main__'})
