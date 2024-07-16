import subprocess
import sys
import os
import shutil

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    #print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[3]
    args = sys.argv[4:]
    #
    tmpdir = "_tempdir"
    if not os.path.isdir(tmpdir):
        os.mkdir(tmpdir)
    shutil.copy(command,tmpdir)
    os.chroot(tmpdir)
    os.unshare(CLONE_NEWPID)
    command = "/"+os.path.basename(command)
    completed_process = subprocess.run([command, *args], capture_output=True)
    #sys.stdout.write()
    #sys.stderr.write(completed_process.stderr.decode("utf-8"))
    print(completed_process.stdout.decode("utf-8"),end="")
    print(completed_process.stderr.decode("utf-8"),end="",file=sys.stderr)
    quit(completed_process.returncode)


if __name__ == "__main__":
    main()
