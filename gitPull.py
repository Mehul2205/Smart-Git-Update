import os
from git import Repo, cmd
from termcolor import colored, cprint
import re
import colorama

colorama.init()
def cPrint(output, color, indentation):
    fo = indentation*" " + output
    print(colored(fo, color))

def updateGG(repo, path, indentation):
    if not repo.bare:
        cPrint(str(repo.head.ref), 'green', indentation)
        if repo.is_dirty():
            changedFiles = [ item.a_path for item in repo.index.diff(None) ]
            cPrint("List of changed files - "+ ' '.join(changedFiles), 'red', indentation+4)
            cPrint("List of untracked files - "+ ' '.join(repo.untracked_files), 'red', indentation+4)
        else:
            if str(repo.head.ref) != "master":
                if(re.match(r"(.)*gitops", path)):
                    repo.git.checkout('unstable')
                else:
                    repo.git.checkout('master')
            g = cmd.Git(path)
            cPrint(g.pull(), 'yellow', indentation+4)
    cPrint("--- Task Ended ---", 'cyan', indentation + 12)
    return

def updateGitRepo(path, indentation):
    #cPrint(', '.join(os.listdir(path)), 'grey', indentation)
    for i in os.listdir(path):
        cPrint(i, "white", indentation)
        childPath = path + '/'+ i
        if(os.path.isfile(childPath) or re.match(r"\..*", i)):
            cPrint("Invalid", "blue", indentation + 4)
            continue
        try:
            repo = Repo(childPath)
            updateGG(repo, childPath, indentation + 4)
        except Exception:
            updateGitRepo(childPath, indentation + 4)
    return

def main():
    updateGitRepo(str(os.path.dirname(os.path.realpath('__file__'))), 0)

if __name__=="__main__":
    main()