
import re

if __name__ == '__main__':

    s = '_git_git_xx_git_xgangA_2020'

    pat = '[^^].*git_(.*)_2020$'
    print(re.findall(pat, s))
