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

############## THIS HAS TO BE HANDLED WITH INSTALLATION OF THE PROJECT BUT I
############# IMPORTING THE GLOBAL SETTINGS FILE BUT I DON'T KNOW HOW TO DO THAT YET
import sys 
import os 

# jgram parent dir
curdir = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_DIR = os.path.dirname(curdir) 
############################################################################

def jap_text_info(japanese_text, dictionary='unidic'):
    """Extract morphemes info from a given japanese sentence and return a list of
    dictionaries. Each item of the list is a dictionary containing every extracted
    info from a morpheme that builds the sentence.

    """
    # Extract morpheme info
    ps = subprocess.Popen(['echo', japanese_text], stdout=subprocess.PIPE)
    morphs_info = subprocess.check_output(['mecab', '-d', PROJECT_DIR+'/dic/'+dictionary], stdin=ps.stdout)
    ps.wait()

    # Transform morpheme info into list of dictionaries
    morphs_list = str.split(morphs_info.decode(), '\n')
    
    info_columns_name = [
            'surface', 'pos1_macrotaxonomy', 'pos2_classword', 'pos3_smallclass',
            'pos4_detailedclass','conjugation_type','conjugated_form','orthography',
            'orthograpy_base','goshu_origin'
    ]

    processed_morphs_info = []
    for current_morph_info in morphs_list:
        current_morph_info_list = []
        current_morph_info_list = current_morph_info.split('[#]') 
        processed_morphs_info.append(dict(zip(info_columns_name,current_morph_info_list[:])))
        sentence_and_morphs_info = [japanese_text, processed_morphs_info]

    return sentence_and_morphs_info


if __name__ == "__main__":
    import sys
    out_test = jap_text_info(sys.argv[1])
    print(out_test)


# TODO: RELLENAR README
# TODO: DOCUMENTAR
# TODO: CREAR TESTS
# TODO: CREAR FICHERO DE SETTINGS
# TODO: FLEXIBILIZAR. Hacer que los campos de la info para cada morfema (en forma de diccionario)
# se rellene de forma estándar aunque el diccionario utilizado sea diferente de unidic
# TODO: Averiguar cómo crear un instalable del proyecto, que luego pueda importar desde cualquier
#       fichero del proyecto haciendo--> import jgram.conf.... o lo que sea
