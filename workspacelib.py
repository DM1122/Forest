import os
import shutil


dirs = ['drawings']

verbose = True


def clear():
    '''
    Clears workspace folders.
    '''

    print('[workspacelib]: Clearing workspace') if verbose else False
    
    for dir in dirs:
        try:
            shutil.rmtree(dir)
        except:
            pass



if __name__ == '__main__':
    clear()