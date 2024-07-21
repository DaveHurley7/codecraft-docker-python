import subprocess
import sys
import os
from urllib.request import Request as ulreq, urlopen
import json
import tarfile

    
def get_docker_auth_token(image,tag):
    dauth_req = ulreq("https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/"+image+":pull")
    dauthf = urlopen(dauth_req)
    auth_body = dauthf.read().decode()
    dauthf.close()
    auth_resp = json.loads(auth_body)
    return auth_resp["token"]

def load_image(image_name):
    tag = "latest"
    if ":" in image_name:
        tag_sep = image_name.index(":")
        tag = image_name[tag_sep+1:]
        image_name = image_name[:tag_sep]
        del tag_sep
    auth_token = get_docker_auth_token(image_name,tag)
    dreg_req = ulreq("https://registry.hub.docker.com/v2/library/" + image_name + "/manifests/" + tag,
                    headers = {
                        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
                        "Authorization": "Bearer " + auth_token
                    })
    dregf = urlopen(dreg_req)
    dreg_resp = dregf.read().decode()
    dreg_body = json.loads(dreg_resp)
    dregf.close()
    layers = dreg_body["layers"]
    for layer in layers:
        imgrawf = open(image_name,"wb")
        dbin_req = ulreq("https://registry.hub.docker.com/v2/library/" + image_name + "/blobs/" + layer["digest"],
                        headers = {
                            "Authorization": "Bearer " + auth_token
                        })
        dbinf = urlopen(dbin_req)
        imgrawf.write(dbinf.read())
        imgrawf.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    #print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    image_name = sys.argv[2]
    command = sys.argv[3]
    args = sys.argv[4:]
    load_image(image_name)
    tmpdir = "_tempdir"
    if not os.path.isdir(tmpdir):
        os.mkdir(tmpdir)
    imgtar = tarfile.open(image_name,"r:gz")
    imgtar.extractall(tmpdir,filter="tar")
    os.chroot(tmpdir)
    os.unshare(os.CLONE_NEWPID)
    #command = "/"+os.path.basename(command)
    #print(command,*args)
    completed_process = subprocess.run([command, *args], capture_output=True)
    #sys.stdout.write()
    #sys.stderr.write(completed_process.stderr.decode("utf-8"))
    print(completed_process.stdout.decode("utf-8"),end="")
    print(completed_process.stderr.decode("utf-8"),end="",file=sys.stderr)
    quit(completed_process.returncode)


if __name__ == "__main__":
    main()
