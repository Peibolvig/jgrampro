"""
jgrampro.tools.mecab
~~~~~~~~~~~~~~~~~

Process japanese text and gives syntactic info of the elements

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez
                <pablo.vazquez.dev@gmail.com>. See AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
    :Version: 0.1(alpha)
"""

import subprocess

from jgrampro.conf import global_settings as gs

PROJECT_DIR = gs.PROJECT_DIR 


def jap_text_info(japanese_text, dictionary='unidic'):
    """Extract morphemes info from a given japanese sentence and return a list
    of dictionaries. Each item of the list is a dictionary containing every
    extracted info from a morpheme that builds the sentence.

    """
    # Extract morpheme info
    ps = subprocess.Popen(['echo', japanese_text], stdout=subprocess.PIPE)
    morphs_info = subprocess.check_output(
        ['mecab', '-d', PROJECT_DIR+'/dic/'+dictionary], stdin=ps.stdout
    )
    ps.wait()

    # Transform morpheme info into list of dictionaries
    morphs_list = str.split(morphs_info.decode(), '\n')
    
    info_columns_name = [
        'surface', 'pos1_macrotaxonomy', 'pos2_classword', 'pos3_smallclass',
        'pos4_detailedclass', 'conjugation_type', 'conjugated_form',
        'orthography', 'orthography_base', 'goshu_origin'
    ]

    processed_morphs_info = []
    sentence_and_morphs_info = ['', '']
    for current_morph_info in morphs_list:
        if current_morph_info == 'EOS': 
            break

        current_morph_info_list = current_morph_info.split('[#]')
        processed_morphs_info.append(dict(zip(info_columns_name,
                                              current_morph_info_list[:])))
        sentence_and_morphs_info = [japanese_text, processed_morphs_info]

    return sentence_and_morphs_info


if __name__ == "__main__":
    import sys
    out_test = jap_text_info(sys.argv[1])
    print(out_test)
