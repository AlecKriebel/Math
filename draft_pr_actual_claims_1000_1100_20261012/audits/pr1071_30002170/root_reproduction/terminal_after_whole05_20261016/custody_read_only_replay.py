from pathlib import Path
import json
F=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/finalization/terminal_admin_after_whole05_20261016')
O=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/root_reproduction/terminal_after_whole05_20261016/custody')
original=Path.write_text
def redirected(self,*a,**kw):
 if self.is_relative_to(F):
  target=O/self.relative_to(F);target.parent.mkdir(parents=True,exist_ok=True);return original(target,*a,**kw)
 raise RuntimeError("Unexpected custody output "+str(self))
Path.write_text=redirected
p=F/"custody.py"
exec(compile(p.read_text(),str(p),"exec"),{"__file__":str(p),"__name__":"__main__"})
