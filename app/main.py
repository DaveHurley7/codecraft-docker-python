import subprocess
import sys
import os
import shutil
import ssl, socket as skt

def load_image(image_name):
    sk = skt.socket(skt.AF_INET,skt.SOCK_STREAM)
    sslctx = ssl.getdefaultcontext()
    s_sk = sslctx.wrap_socket(sk)
    s_sk.connect(("registry.hub.docker.com",443))
    s_sk.send("GET /v2/ HTTP/1.1".encode())
    resp = s_sk.recv(1024)
    print(resp)

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
    load_image(image_name):
    completed_process = subprocess.run([command, *args], capture_output=True)
    #sys.stdout.write()
    #sys.stderr.write(completed_process.stderr.decode("utf-8"))
    print(completed_process.stdout.decode("utf-8"),end="")
    print(completed_process.stderr.decode("utf-8"),end="",file=sys.stderr)
    quit(completed_process.returncode)


if __name__ == "__main__":
    main()
