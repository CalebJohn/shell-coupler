import os
import subprocess
import sys

from coupler.app import App


def main():
    piped_in = []
    if not sys.stdin.isatty():
        piped_in = sys.stdin.readlines()
    elif len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            piped_in = f.readlines()

    piped_in = list(map(lambda s: s.strip(), piped_in))

    # The prompt-toolkit library depends on having access a tty
    # and unfortunately won't accept a generic handle from open
    # The trick here is to use os.open to get a lower level file handle
    # and then swap that into stdin
    f = os.open("/dev/tty", os.O_RDWR)
    os.dup2(f, sys.stdin.fileno())

    final_script = App(piped_in).start()

    os.close(f)

    subprocess.run(["python", final_script.name])
    final_script.close()


if __name__ == "__main__":
    main()
