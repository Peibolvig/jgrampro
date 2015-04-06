"""
jgram.conf.global_settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

Global configuration data for jgram project

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez
                <pablo.vazquez.dev@gmail.com>. See AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
    :Version: 0.1(alpha)
"""
import sys 
import os 

# jgram parent dir
curdir = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_DIR = os.path.dirname(curdir) 

sys.path.insert(0, PROJECT_DIR) 

