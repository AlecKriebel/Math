"""Replay actual positive and malformed-input controls for the research checker."""
import contextlib,io,json
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
    from verify import flags,check

def require(ok,why):
    if not ok:raise RuntimeError(why)
fs=flags(range(3))
result={'valid_triangle':check(fs,fs),'missing_facet':check(fs[:-1],fs),'duplicate_facet':check(fs+[fs[0]],fs),'malformed_facet':check([(fs[0][0],)*3]+fs[1:],fs),'disconnected_attachment':check([(1,2,3),(4,5,6)],[(1,2,3),(4,5,6)])}
require(result['valid_triangle']['valid'],'Valid triangle rejected')
require(all(not v['valid'] for k,v in result.items() if k!='valid_triangle'),'Negative control accepted')
# Empty, nonpure and unknown-label controls supplement the saved historical controls.
extra={'empty':check([],fs),'nonpure':check([fs[0][:-1]]+fs[1:],fs),'unknown_label':check([(999,)+fs[0][1:]]+fs[1:],fs)}
require(all(not v['valid'] for v in extra.values()),'Supplemental negative control accepted')
# Compare every field with the historical results, including the disconnected attachment.
saved=json.loads((Path(__file__).parent/'negative_controls.json').read_text())
require(result==saved,'Historical negative controls differ')
print(json.dumps({'historical':result,'supplemental':extra},indent=2))
(Path(__file__).parent/'research_control_results.json').write_text(json.dumps({'historical':result,'supplemental':extra},indent=2)+'\n')
