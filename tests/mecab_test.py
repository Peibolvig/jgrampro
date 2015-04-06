"""
test.mecab_test
~~~~~~~~~~~~~~~

Tests for the mecab wrapper

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez
                <pablo.vazquez.dev@gmail.com>. See AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
    :Version: 0.1a
"""
from jgrampro.tools import mecab


def test_jap_text_info():
    assert mecab.jap_text_info('私はジョンです。', 'unidic') == ['私はジョンです。', [
        {
            'orthography': '私', 
            'pos4_detailedclass': '', 
            'pos2_classword': '', 
            'conjugated_form': '', 
            'pos1_macrotaxonomy': '代名詞', 
            'surface': '私', 
            'pos3_smallclass': '', 
            'conjugation_type': '', 
            'goshu_origin': '和', 
            'orthography_base': '私'
        }, 
        {
            'orthography': 'は', 
            'pos4_detailedclass': '', 
            'pos2_classword': '係助詞', 
            'conjugated_form': '', 
            'pos1_macrotaxonomy': '助詞', 
            'surface': 'は', 
            'pos3_smallclass': '', 
            'conjugation_type': '', 
            'goshu_origin': '和', 
            'orthography_base': 'は'
        }, 
        {
            'orthography': 'ジョン', 
            'pos4_detailedclass': '一般', 
            'pos2_classword': '固有名詞', 
            'conjugated_form': '', 
            'pos1_macrotaxonomy': '名詞', 
            'surface': 'ジョン', 
            'pos3_smallclass': '人名', 
            'conjugation_type': '', 
            'goshu_origin': '固', 
            'orthography_base': 'ジョン'
        }, 
        {
            'orthography': 'です', 
            'pos4_detailedclass': '', 
            'pos2_classword': '', 
            'conjugated_form': '終止形-一般', 
            'pos1_macrotaxonomy': '助動詞', 
            'surface': 'です', 
            'pos3_smallclass': '', 
            'conjugation_type': '助動詞-デス', 
            'goshu_origin': '和', 
            'orthography_base': 'です'
        }, 
        {
            'orthography': '。', 
            'pos4_detailedclass': '', 
            'pos2_classword': '句点', 
            'conjugated_form': '', 
            'pos1_macrotaxonomy': '補助記号', 
            'surface': '。', 
            'pos3_smallclass': '', 
            'conjugation_type': '', 
            'goshu_origin': '記号', 
            'orthography_base': '。'
        }]]
