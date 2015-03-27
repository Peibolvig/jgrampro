"""
test.mecab_test
~~~~~~~~~~~~~~~

Tests for the mecab wrapper

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez <pablo.vazquez.dev@gmail.com>
                see AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
    :Version: 0.1(alpha)
"""
from jgram.tools import mecab


def test_processing_japanese_raw_input_default():
    # Default option is ipadic
    pass

# def test_processing_japanese_raw_input_unidic():
    pass
#     # Using unidic dictionary
#     assert mecab.jap_text_info('これは本です', 'unidic') == [
#         {
#             'morpheme':'これ', 
#             'pronuntiation':'コレ', 
#             'lexemeReading':'コレ', 
#             'lexemeWriting':'此れ',  
#             'partOfSpeech':'代名詞', 
#             'inflectionType':'', 
#             'inflectionForm':'', 
#             'accentModel':'0' 
#         }, 
#         {
#             'morpheme':'は', 
#             'pronuntiation':'ワ', 
#             'lexemeReading':'ハ', 
#             'lexemeWriting':'は',  
#             'partOfSpeech':'助詞-係助詞', 
#             'inflectionType':'', 
#             'inflectionForm':'', 
#             'accentModel':'' 
#         }, 
#         {
#             'morpheme':'本', 
#             'pronuntiation':'ホン', 
#             'lexemeReading':'ホン', 
#             'lexemeWriting':'本',  
#             'partOfSpeech':'名詞-普通名詞-一般', 
#             'inflectionType':'', 
#             'inflectionForm':'', 
#             'accentModel':'1' 
#         }, 
#         {
#             'morpheme':'です', 
#             'pronuntiation':'デス', 
#             'lexemeReading':'デス', 
#             'lexemeWriting':'です',  
#             'partOfSpeech':'助動詞', 
#             'inflectionType':'助動詞-デス', 
#             'inflectionForm':'終止形-一般', 
#             'accentModel':'' 
#         } 
#     ]
