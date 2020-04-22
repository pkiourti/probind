#!"C:\Users\xsmil\Documents\School\BU ENG 2018-2020\Spring 2020\EC 552\Project\synbio_project\gui\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'future==0.18.2','console_scripts','pasteurize'
__requires__ = 'future==0.18.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('future==0.18.2', 'console_scripts', 'pasteurize')()
    )
