"""Cross-check frozen libraries after independent construction was sealed."""
from pathlib import Path
import runpy,contextlib,io,sys,json,random,time,argparse
p=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):d=runpy.run_path(str(p/'independent_controls.py'))
parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,default=p.parent/'snapshot/unsolved_math_prioritization/attempts/6600013');args=parser.parse_args()
sys.path.insert(0,str(args.candidate.resolve()))
import thue_morse_language as candidate_tm,quadratic_rotation as candidate_st,rectangular_complex as candidate_complex,rational_linear as candidate_linear
checks={}
def ck(v,t):
 assert v,t
 checks[t]=checks.get(t,0)+1
for n in range(1,258):ck(set(d['tm'](n))==candidate_tm.language(n),'complete_TM_language')
for n in range(1,81):ck(set(d['st'](n))==candidate_st.language(n),'exact_Sturmian_language')
for n in range(1,7):
 cells,a,b,hs=d['complex'](n);cc,dd,hh=candidate_complex.complex(n)
 ck(cells==cc,'pattern_cell_lists');ck([a,b]==dd,'boundary_matrices');ck(hs==hh,'oriented_edge_partition')
for n,m in [(1,3),(2,4),(2,6),(1,5),(3,5),(4,6)]:
 small,ds,hs=candidate_complex.complex(n);large,dl,hl=candidate_complex.complex(m)
 ck(d['mapchain'](n,m)==candidate_complex.forgetting(n,m,small,large,hs,hl),'cropping_matrices')
rng=random.Random(3826600013)
for z in range(400):
 nr=rng.randrange(1,15);nc=rng.randrange(1,15);a=[[rng.randrange(-9,10) for j in range(nc)] for i in range(nr)]
 if z%3==0 and nr>1:a[-1]=[x*13 for x in a[0]]
 ck(d['rank'](a)==candidate_linear.rank(a),'rank_crosscheck')
print(json.dumps({'checks':sum(checks.values()),'categories':checks,'scope':'Cross-library agreement after independent mechanisms were sealed; finite exact QQ controls only'},sort_keys=True,indent=2))
