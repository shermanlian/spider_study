import argparse

#没用到
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-name','--NAME',type=str,default='craziejulia')
    parser.add_argument('-dir','--DIR',type=str,default='D:/爬虫学习/craziejulia')

    return parser.parse_args()
