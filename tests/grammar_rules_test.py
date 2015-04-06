"""
test.grammar_rules
~~~~~~~~~~~~~~~~~~

Tests for the grammar_rules.py file methods

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez
                <pablo.vazquez.dev@gmail.com>. See AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
    :Version: 0.1(alpha)
"""
from jgrampro.grammar_rules import GrammarRuleProcessor


class TestGrammarRuleProcessor:
    gr = GrammarRuleProcessor()

    def test_multiple_replace(self):
        mr = self.gr._multiple_replace
        text = 'abcdefghijklmnop'
        replacements_dict = {'a': 'XX', 'f': 'F F', 'o': 'OO'}
        assert mr(text, replacements_dict) == 'XXbcdeF FghijklmnOOp'

    def test_build_regexp(self):
        br = self.gr._build_regexp
        assert br('') == ''
        assert br('〜は(prt)〜だ(v)。') == (
            '.+は(\(prt\))[^。]+だ(\(v\)|\(v-gen\)|\(v-aux\))。')
        assert br('〜はだ(v)。') == '.+はだ(\(v\)|\(v-gen\)|\(v-aux\))。'
        assert br('〜は(prt)(v)。') == '.+は(\(prt\))(\(v\)|\(v-gen\)|\(v-aux\))。'

    def test_split_rule_items(self):
        def sri(rule_to_test):
            self.gr.set_rule(rule_to_test)
            return self.gr._split_rule_items()

        assert sri('') == []
        assert sri('〜は(prt)〜だ(v)。') == ['〜', 'は(prt)', '〜', 'だ(v)', '。']
        assert sri('〜はだ(v)。') == ['〜', 'はだ(v)', '。'] 
        assert sri('〜は(prt)(v)〜。') == ['〜', 'は(prt)', '(v)', '〜', '。']
        assert sri('(v)') == ['(v)']
        assert sri('(v)(prt)') == ['(v)', '(prt)']
        assert sri('(v)〜(prt)は(prt)') == ['(v)', '〜', '(prt)', 'は(prt)']
        
    def test_get_grammar_item_positions_and_tag(self):
        def ggipt(ggipt_sentence, tag):
            self.gr.set_sentence(ggipt_sentence)
            return self.gr._get_grammar_item_positions_and_tag(tag)

        sentence = '私は時計とめがねとベルトを無くした。これはあなたのケイタイです。'
        assert ggipt('', '') == {
            'tag': '', 'weight': 0, 'positions': []
        }
        assert ggipt(sentence, '') == {
            'tag': '', 'weight': 0, 'positions': []
        }
        assert ggipt(sentence, 'は(prt)') == {
            'tag': 'は(prt)', 'weight': 51, 'positions': [1, 12]
        }
        assert ggipt(sentence, 'です(v-aux)') == {
            'tag': 'です(v-aux)', 'weight': 52, 'positions': [16]
        }
        assert ggipt(sentence, '(v)') == {
            'tag': '(v)', 'weight': 1, 'positions': [8, 9, 16]
        }
        
    def test_build_mock_sentence(self):
        def bms(rule, bms_sentence):
            self.gr.set_data(rule, bms_sentence)
            rule_items = self.gr._split_rule_items()
            return self.gr._build_mock_sentence(rule_items)
        
        sentence = 'これはあなたのケイタイです。私は時計とめがねとベルトを無くした。'
        assert bms('(v)', sentence) == 'xxxxx(v)。xxxxxxxx(v)(v)。'
        assert bms('です(v)〜(v)', sentence) == 'xxxxxです(v)。xxxxxxxx(v)(v)。'

    def test_check_rule_compliance(self):
        def crc(rule, crc_sentence):
            self.gr.set_data(rule, crc_sentence)
            rule_items = self.gr._split_rule_items()
            self.gr.regexp_rule = self.gr._build_regexp(self.gr.regexp_rule)
            return self.gr._check_rule_compliance(rule_items)

        sentence = '私はジョンです。彼女はテレサです。' 
        assert crc('', '')
        assert crc('', sentence)
        assert crc('(adj)。〜(adj-i)', '静か。食べ物をおいしいです。')
        assert crc('〜(v)。〜です(v)', sentence)
        assert crc('〜(v)。〜です(v-aux)', sentence)
        assert crc('〜です(v)。〜です(v-aux)', sentence)
