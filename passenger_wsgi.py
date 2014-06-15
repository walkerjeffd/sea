import sys, os
INTERP = os.path.join(os.environ['HOME'], 'sea.walkerjeff.com', 'env', 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'app'))
 
from manage import app as application
