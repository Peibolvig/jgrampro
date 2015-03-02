"""
jgram.tools.mecab
~~~~~~~~~~~~~~~~~

Process japanese text and gives syntactic info of the elements

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez <pablo.vazquez.dev@gmail.com>
                see AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
"""

import subprocess

def jap_text_info(japanese_text, dictionary='ipadic'):
    print(subprocess.check_output(['pwd']))
    ps = subprocess.Popen(['echo', japanese_text], stdout=subprocess.PIPE)
    output = subprocess.check_output(['mecab', '-d', '../dic/'+dictionary], stdin=ps.stdout)
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

