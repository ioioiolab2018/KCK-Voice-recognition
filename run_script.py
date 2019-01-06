import glob
import os
import subprocess
import sys


def main(argv):
    algorithm = glob.glob('HPS.py')
    if argv == 'all':
        run_all(algorithm[0])
    else:
        run_one(argv, algorithm[0])


def run_all(algorithm):
    print(algorithm)
    os.chdir('train/')
    files = glob.glob('*.wav')
    result = 0
    for file in files:
        run_one('train/' + str(file), algorithm)
        # if run_one('train/' + str(file)):
        #     result += 1
    print(str(result) + "/" + str(len(files)))


def run_one(filename, algorithm):
    if 'K' in filename:
        result = 'K'
    else:
        result = 'M'

    proc = subprocess.Popen(['python3', algorithm, filename], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, universal_newlines=True)
    output, error = proc.communicate()

    value = output.splitlines()[0]
    print(filename + ' -> ' + value + '/' + result)
    if value == result:
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except:
        print('None arguments exception!')
