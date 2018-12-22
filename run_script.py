import subprocess
import sys


def main(argv):
    if argv == 'all':
        run_all()
    else:
        run_one(argv)


def run_all():
    print('cos')


def run_one(filename):
    if 'K' in filename:
        result = 'K'
    else:
        result = 'M'

    proc = subprocess.Popen(['python3', 'HPS.py', filename], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output = proc.communicate()[0][2:-2]
    proc.kill()

    print(output)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print('None arguments exception!')
