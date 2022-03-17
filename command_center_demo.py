import argparse

def check():
    check_str = 'check ok'
    print(check_str)

def check_loop():
    check_time = 1
    while True:
        check_time += 1
        print(check_time)

parser = argparse.ArgumentParser()
# parser.add_argument('square', type=str, help='display a square of a given type')
parser.add_argument('-w', '--works', type=str, choices=['check', 'loop'])
args = parser.parse_args()
# print(args.e)
if args.works == 'check':
    check()
if args.works == 'loop':
    check_loop()

'''
example:
python .\test.py -w 'check'
'''