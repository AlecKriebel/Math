from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;A=R.parents[1]
mode='optimized' if sys.flags.optimize else 'normal'
if sys.argv[1]=='repair':
 p=A/'ops_repair_20261021/repair_controls.py'; out=R/('repair_'+mode)
else:
 p=A/'publication_operations_preparation/prior_review_02_full/publication_operations_preparation/offline_controls.py';out=R/('regression_'+mode)
out.mkdir(exist_ok=True)
code=p.read_text();old='HERE=Path(__file__).resolve().parent\nAUDIT=HERE.parent'
if code.count(old)!=1:raise RuntimeError('Unexpected redirect site')
code=code.replace(old,'HERE=Path('+repr(str(out))+')\nAUDIT=Path('+repr(str(A))+')')
exec(compile(code,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
