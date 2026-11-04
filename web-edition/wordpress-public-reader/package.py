"""Build the public reader delivery component from an already committed revision.

python web-edition/wordpress-public-reader/package.py OUTPUT_DIRECTORY [REVISION]
The package contains route code and a public-file integrity manifest only.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from hashlib import sha256
import json,re,subprocess,sys
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
revision=sys.argv[2]if len(sys.argv)>2 else git('rev-parse','HEAD').decode().strip();assert re.fullmatch('[0-9a-f]{40}',revision)
out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True);files={}
paths=git('ls-tree','-r','--name-only',revision,'--','docs/atlas/lectura').decode().splitlines()+['docs/atlas/mapa/grafo.json']
proc=subprocess.Popen(['git','-C',str(REPO),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
graph=None
for path in paths:
 proc.stdin.write((revision+':'+path+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split();body=proc.stdout.read(int(header[2]));assert proc.stdout.read(1)==b'\n'
 rel=path[len('docs/atlas/lectura/'):]if path.startswith('docs/atlas/lectura/')else'grafo.json'
 files[rel]={'source':path,'sha256':sha256(body).hexdigest(),'bytes':len(body)}
 if rel=='grafo.json':graph=body
proc.stdin.close();proc.wait();assert graph
manifest={'revision':revision,'graphSha256':sha256(graph).hexdigest(),'files':files}
package=out/('mind-atlas-public-reader-'+revision[:12]+'.zip')
with ZipFile(package,'w',ZIP_DEFLATED)as z:
 z.writestr('mind-atlas-public-reader/mind-atlas-public-reader.php',(HERE/'mind-atlas-public-reader.php').read_bytes());z.writestr('mind-atlas-public-reader/manifest.json',json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+'\n')
with ZipFile(package)as z:assert z.testzip()is None
print(json.dumps({'package':str(package),'resources':len(files),'sourceRevision':revision,'graphSha256':manifest['graphSha256']}))
