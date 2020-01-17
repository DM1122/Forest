import os
import shutil


dirs = ['drawings']

verbose = True


def wd():
    '''
    Provides information regrading working directory
    '''

    cwd = os.getcwd()
    print('[workspacelib]: Working directory is', cwd)


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