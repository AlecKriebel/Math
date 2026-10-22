"""Physical copy controls for the review's own pinned checker, normal and -O."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,tempfile
def need(c,m):
    if not c:raise ValueError(m)
def main():
    a=argparse.ArgumentParser();a.add_argument("--expected-manifest-sha256",required=True)
    a.add_argument("--input-root",type=Path,required=True);a.add_argument("--scratch",type=Path,required=True);x=a.parse_args()
    own=Path(__file__).absolute().parent;rows=[]
    for optimized in [False,True]:
        for case in ["baseline","content","missing","extra","symlink","fifo","directory","manifest","manifest_fifo","input"]:
            with tempfile.TemporaryDirectory(prefix="review01-custody-",dir=x.scratch) as temp:
                b=Path(temp);packet=b/"packet";shutil.copytree(own,packet);inputs=x.input_root
                target=packet/"REPORT.md"
                if case=="content":target.write_bytes(target.read_bytes()+b"X")
                elif case=="missing":target.unlink()
                elif case=="extra":(packet/"extra.txt").write_bytes(b"X")
                elif case=="symlink":
                    raw=target.read_bytes();target.unlink();sent=b/"sentinel";sent.write_bytes(raw);target.symlink_to(sent)
                elif case=="fifo":target.unlink();os.mkfifo(target)
                elif case=="directory":target.unlink();target.mkdir()
                elif case=="manifest":f=packet/"MANIFEST.json";f.write_bytes(f.read_bytes()+b" ")
                elif case=="manifest_fifo":f=packet/"MANIFEST.json";f.unlink();os.mkfifo(f)
                elif case=="input":
                    inputs=b/"inputs"; bindings=json.loads((packet/"INPUTS.json").read_text())
                    for name in bindings["files"]:
                        dest=inputs/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((x.input_root/name).read_bytes())
                    f=inputs/"paper.tex";f.write_bytes(f.read_bytes()+b"X")
                cmd=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])+[str(packet/"verify_custody.py"),"--input-root",str(inputs),"--expected-manifest-sha256",x.expected_manifest_sha256]
                v=subprocess.run(cmd,capture_output=True,text=True,timeout=8)
                need((v.returncode==0)==(case=="baseline"),"Wrong outcome:"+case)
                rows.append({"case":case,"optimized":optimized,"returncode":v.returncode,"result":json.loads(v.stdout)["result"]})
    print(json.dumps({"result":"PASS","cases":rows,"case_count":len(rows)},indent=2))
if __name__=="__main__":main()
