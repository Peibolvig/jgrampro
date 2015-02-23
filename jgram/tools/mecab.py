#
# INCLUDE LICENSE, AUTHOR, DATE, ETC...HERE
#

import sys
import os
curdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(curdir)
sys.path.insert(0, parentdir)

import subprocess

def jap_text_info(japanese_text):
    print(subprocess.check_output(['pwd']))
    ps = subprocess.Popen(['echo', japanese_text], stdout=subprocess.PIPE)
    output = subprocess.check_output(['mecab', '-d', os.path.join(parentdir, 'dic/unidic')], stdin=ps.stdout)
    ps.wait()
    print(output.decode())


if __name__ == "__main__":
    import sys
    jap_text_info(sys.argv[1])


# TODO RELLENAR README
# TODO DOCUMENTAR
# TODO CREAR TESTS
# TODO CREAR FICHERO DE SETTINGS
# TODO FLEXIBILIZAR jap_text_info (por ejemplo, que beba el diccionario desde el fichero de settings, o algo así y/o que se pueda pasar como argumento)

