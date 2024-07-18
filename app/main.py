import subprocess
import sys
import os
import shutil
from urllib.request import Request as ulreq, urlopen
import json

#sslctx = ssl.create_default_context()
def initsocktohost(host,port):
    print("Attempting to connect:",host,port)
    sk = skt.socket(skt.AF_INET,skt.SOCK_STREAM)
    s_sk = sslctx.wrap_socket(sk,server_hostname=host)
    s_sk.connect((host,port))
    
def recv_token(sk):
    resp = sk.recv(1024).decode()
    req_h, body = resp.split("\r\n\r\n")
    json_res = None
    while True:
        try:
            json_res = json.loads(body)
            break
        except json.decoder.JSONDecodeError:
            body += sk.recv(1024).decode()
    return json_res["token"]
    
def get_docker_auth_token(image,tag):
    dauth_req = ulreq("auth.docker.io/token?service=registry.docker.io&scope=repository:library/"+image+":pull")
    dauthf = urlopen(dauthreq)
    auth_body = dauthf.read()
    print(auth_body)
    #dauth_sk = initsocktohost(,443)
    #dauth_sk.send(("GET ").encode())
    #resp = dauth_sk.recv(1024)
    #print(resp)

def load_image(image_name):
    tag = None
    if ":" in image_name:
        tag_sep = image_name.index(":")
        tag = image_name[tag_sep+1:]
        image_name = image_name[:tag_sep]
        del tag_sep
    auth_token = get_docker_auth_token(image_name,tag)
    #dreg_sk = initsocktohost(("registry.hub.docker.com",443))
    #dreg.send("GET /v2/ HTTP/1.1".encode())
    #change_host(s_sk,)
    #s_sk
    #auth_token = recv_token(s_sk)
    #change_host(s_sk,("registry.hub.docker.com",443))
    #s_sk.send(("GET /v2/library/" + image_name + "/manifests/" + (tag if tag else "latest") + " HTTP/1.1\r\nAuthorization: Bearer " + auth_token).encode())
    #resp = s_sk.recv(1024)
    #print(resp)  

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    #print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    image_name = sys.argv[2]
    command = sys.argv[3]
    args = sys.argv[4:]
    #
    tmpdir = "_tempdir"
    if not os.path.isdir(tmpdir):
        os.mkdir(tmpdir)
        shutil.copy(command,tmpdir)
    os.chroot(tmpdir)
    os.unshare(os.CLONE_NEWPID)
    command = "/"+os.path.basename(command)
    load_image(image_name)
    completed_process = subprocess.run([command, *args], capture_output=True)
    #sys.stdout.write()
    #sys.stderr.write(completed_process.stderr.decode("utf-8"))
    print(completed_process.stdout.decode("utf-8"),end="")
    print(completed_process.stderr.decode("utf-8"),end="",file=sys.stderr)
    quit(completed_process.returncode)


if __name__ == "__main__":
    main()
