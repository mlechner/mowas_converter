import sys

PYENV_DIR = '/opt/mowas_converter/venv'
PROJECT_DIR = '/opt/mowas_converter/'

activate_this = PYENV_DIR + '/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from mowas_converter import app as application
