"""Portable standard-library baseline and wrong-science checks; Python >=3.10."""
from pathlib import Path
import ast,hashlib,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise ValueError(message)
def invoke(folder,name,optimized):
    driver="import sys,runpy;sys.path.insert(0,"+repr(str(folder))+");sys.argv=["+repr(name)+"];runpy.run_path("+repr(str(folder/name))+",run_name='__main__')"
    return subprocess.run([sys.executable,"-E","-S","-B","-P"]+(["-O"] if optimized else [])+["-c",driver],capture_output=True)
def replace_once(source,old,new):
    require(source.count(old)==1,"Mutation must replace exactly one intended expression: "+old)
    return source.replace(old,new,1)
def main():
    require(sys.version_info>=(3,11),"Use Python 3.11 or newer (-P required)")
    basenames=["check_certificate.py","check_half_turn.py","test_reconstruction.py","check_pinned_coordinates.py"]
    sources={n:(HERE/n).read_text() for n in basenames}
    for n in basenames[:2]:
        require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(sources[n]))),"Optimization-unsafe assertion remains")
    rows=[];stdout={}
    for n in basenames:
        for optimized in (False,True):
            r=invoke(HERE,n,optimized);require(r.returncode==0,"Baseline failed: "+n+" "+r.stderr.decode(errors="replace"))
            rows.append({"case":n,"optimized":optimized,"exit":r.returncode,"stdout_sha256":hashlib.sha256(r.stdout).hexdigest()})
            if not optimized:stdout[n]=r.stdout
            else:require(r.stdout==stdout[n],"Normal/optimized baseline output differs: "+n)
    cert=sources["check_certificate.py"];half=sources["check_half_turn.py"]
    variants=[
      ("wrong_squared_length","check_certificate.py",replace_once(cert,"K(F(307, 2), F(137, 2))","K(F(309, 2), F(137, 2))")),
      ("wrong_geometry","check_certificate.py",replace_once(cert,"C = K(F(-1, 2), F(1, 2))","C = K(F(-1, 2), F(1, 3))")),
      ("wrong_source_ray","check_certificate.py",replace_once(cert,"physical_ray = polys[-1][10] - end","physical_ray = polys[-1][10] - end\n    source_ray = physical_ray")),
      ("empty_edge_geometry","check_half_turn.py",replace_once(half,"edge_squared = 4 * ip * ip","edge_squared = K()")),
      ("wrong_pinned_coordinate","check_pinned_coordinates.py",replace_once(sources["check_pinned_coordinates.py"],"F(31,2),F(13,2)","F(33,2),F(13,2)"))]
    for label,filename,source in variants:
        with tempfile.TemporaryDirectory(prefix="dodecahedron-verification-") as tmp:
            folder=Path(tmp)
            for n,s in sources.items():(folder/n).write_text(source if n==filename else s)
            for optimized in (False,True):
                r=invoke(folder,filename,optimized)
                require(r.returncode!=0,"Wrong science falsely accepted: "+label)
                require(b"AssertionError" in r.stderr or b"ValueError" in r.stderr,"Unexpected failure type for "+label)
                rows.append({"case":label,"optimized":optimized,"exit":r.returncode,"rejected":True,"stderr_sha256":hashlib.sha256(r.stderr).hexdigest()})
    return {"status":"PASS","baselines":8,"meaningful_wrong_science_rejections":10,"results":rows,"limit":"Finite checks corroborate exact data and controls; the universal theorem is proved in the manuscript."}
if __name__=="__main__":print(json.dumps(main(),indent=2))

