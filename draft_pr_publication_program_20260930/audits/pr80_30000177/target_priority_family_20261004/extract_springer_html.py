from html.parser import HTMLParser
import pathlib
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.skip=0; self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']: self.skip+=1
    def handle_endtag(self,tag):
        if tag in ['script','style'] and self.skip: self.skip-=1
    def handle_data(self,data):
        if not self.skip and data.strip(): self.parts.append(data.strip())
root=pathlib.Path(__file__).resolve().parent
parser=Text(); parser.feed((root/'process_evidence'/'download_yuan2011_springer'/'stdout.bin').read_text())
out=root/'private'/'yuan2011_springer_html.txt';out.write_text('\n'.join(parser.parts)+'\n')
print(out, out.stat().st_size)
