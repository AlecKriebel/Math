from pathlib import Path
import sys
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'math_algebra_family_01/runtime_packages'))
which=sys.argv[1]
source=root.parent/'publication_package_v1/materials/verification'/which
text=source.read_text()
if which=='exact_certificates.py':
    old='s.cancel(H-fact)==0';new='s.cancel(H-fact)==1'
else:
    old='if not sp.expand(expression - (1 - kappa * S) * (U * U - kappa * V * V * S)) == 0'
    new=old[:-1]+'1'
if text.count(old)!=1:raise RuntimeError('mutation target identity mismatch')
text=text.replace(old,new,1)
sys.argv=[str(source),'--output-dir',str(root/('mutation_output_'+which.removesuffix('.py')))]
exec(compile(text,str(source),'exec'),{'__name__':'__main__','__file__':str(source)})
