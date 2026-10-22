"""Physical controls for review01's own external-pin checker; copies only."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,tempfile
def need(c,m):
    if not c:raise ValueError(m)
def main():
    a=argparse.ArgumentParser();a.add_argument("--input-root",required=True,type=Path)
    a.add_argument("--expected-manifest-sha256",required=True);a.add_argument("--expected-checker-sha256",required=True)
    a.add_argument("--scratch",required=True,type=Path);x=a.parse_args();own=Path(__file__).absolute().parent;rows=[]
    for optimized in [False,True]:
        for case in ["baseline","content","missing","extra","symlink","fifo","directory","manifest_fifo","wrong_pin","checker","input"]:
            with tempfile.TemporaryDirectory(prefix="pr786-own-custody-",dir=x.scratch) as temp:
                b=Path(temp);packet=b/"packet";shutil.copytree(own,packet);inputs=x.input_root
                target=packet/"REPORT.md";pin=x.expected_manifest_sha256
                if case=="content":target.write_bytes(target.read_bytes()+b"X")
                elif case=="missing":target.unlink()
                elif case=="extra":(packet/"extra.json").write_bytes(b"{}")
                elif case=="symlink":
                    d=target.read_bytes();target.unlink();f=b/"sentinel";f.write_bytes(d);target.symlink_to(f)
                elif case=="fifo":target.unlink();os.mkfifo(target)
                elif case=="directory":target.unlink();target.mkdir()
                elif case=="manifest_fifo":f=packet/"MANIFEST.json";f.unlink();os.mkfifo(f)
                elif case=="wrong_pin":pin="0"*64
                elif case=="checker":
                    f=packet/"verify_custody.py";f.write_bytes(f.read_bytes()+b"\n# changed checker\n")
                elif case=="input":
                    inputs=b/"inputs";shutil.copytree(x.input_root,inputs)
                    f=inputs/"paper.tex";f.write_bytes(f.read_bytes()+b"X")
                cmd=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])+[str(packet/"verify_custody.py"),
                    "--input-root",str(inputs),"--expected-manifest-sha256",pin,
                    "--expected-checker-sha256",x.expected_checker_sha256]
                v=subprocess.run(cmd,capture_output=True,text=True,timeout=8)
                need((v.returncode==0)==(case=="baseline"),"Wrong outcome:"+case)
                rows.append({"case":case,"optimized":optimized,"returncode":v.returncode,
                             "result":json.loads(v.stdout)["result"]})
    print(json.dumps({"result":"PASS","case_count":len(rows),"cases":rows},indent=2))
if __name__=="__main__":main()
