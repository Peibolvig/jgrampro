from jgram.tools import mecab
from jgram.grammar_rules import GrammarRuleProcessor

class TestGrammarRuleProcessor:
    gr = GrammarRuleProcessor()

    def test_multiple_replace(self):
        mr = self.gr._multiple_replace
        assert mr('abcdefghijklmnop', {'a':'XX', 'f':'F F','o':'OO'}) == 'XXbcdeF FghijklmnOOp'

    def test_build_regexp(self):
        br = self.gr._build_regexp
        assert br('') == ''
        assert br('〜は(prt)〜だ(v)。') == '.+は(\(prt\))[^。]+だ(\(v\)|\(v-gen\)|\(v-aux\))。'
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
        def ggipt(sentence, tag):
            self.gr.set_sentence(sentence)
            return self.gr._get_grammar_item_positions_and_tag(tag)

        sentence = '私は時計とめがねとベルトを無くした。これはあなたのケイタイです。'
        assert ggipt('', '') == {'tag':'', 'weight': 0, 'positions':[]} 
        assert ggipt(sentence, '') == {'tag':'', 'weight':0, 'positions':[]} 
        assert ggipt(sentence, 'は(prt)') == {'tag':'は(prt)', 'weight':51, 'positions':[1, 12]} 
        assert ggipt(sentence, 'です(v-aux)') == {'tag':'です(v-aux)', 'weight':52, 'positions':[16]} 
        assert ggipt(sentence, '(v)') == {'tag':'(v)', 'weight': 1, 'positions':[8, 9, 16]} 
        
    def test_build_mock_sentence(self):
        def bms(rule, sentence):
            self.gr.set_data(rule, sentence)
            rule_items = self.gr._split_rule_items()
            return self.gr._build_mock_sentence(rule_items)
        
        sentence = 'これはあなたのケイタイです。私は時計とめがねとベルトを無くした。'
        assert bms('(v)', sentence) == 'xxxxx(v)。xxxxxxxx(v)(v)。'
        assert bms('です(v)〜(v)', sentence) == 'xxxxxです(v)。xxxxxxxx(v)(v)。'


    def test_check_rule_compliance(self):
        def crc(rule, sentence):
            self.gr.set_data(rule, sentence)
            rule_items = self.gr._split_rule_items()
            self.gr.regexp_rule = self.gr._build_regexp(self.gr.regexp_rule)
            return self.gr._check_rule_compliance(rule_items)

        sentence = '私はジョンです。彼女はテレサです。' 
        assert crc('', '') == True
        assert crc('', sentence) == True
        assert crc('(adj)。〜(adj-i)', '静か。食べ物をおいしいです。') == True
        assert crc('〜(v)。〜です(v)', sentence) == True
        assert crc('〜(v)。〜です(v-aux)', sentence) == True
        assert crc('〜です(v)。〜です(v-aux)', sentence) == True

#    def test_placeholder(self):
#        self.gr.set_rule('〜は〜だ')
#
#        # ok sentence
#        self.gr.set_sentence('私は学生だ。')
#        assert self.gr.process() == True
#
#        # ko sentence
#        self.gr.set_sentence('源氏物語をやっと読み終わった。')
#        assert self.gr.process() == False
#    
#        # tricky string with two sentences
#        self.gr.set_sentence('私は源氏物語をやっと読み終わった。飲んだ。')
#        assert self.gr.process() == False
#    
#        # empty sentence
#        self.gr.set_sentence('')
#        assert self.gr.process() == False






#    def test__get_grammar_item_positions_and_tag(self):
#        self.gr.set_rule('〜は(prt)〜(adj)')
#        self.gr.set_sentence('私は小さいでも好きなだんごを食べた。')
#        assert self.gr._get_grammar_item_positions_and_tag('(adj)') == {'tag':'(adj)', 'positions':[2, 5]}
#        assert self.gr._get_grammar_item_positions_and_tag('は(prt)') == {'tag':'は', 'positions':[1]}
#        assert self.gr.process() == true
#
#    def test_rules_with_parentheses(self):
#        # with description of grammatical items
#        self.gr.set_rule('〜は(prt)〜だ(v)')
#
#        self.gr.set_sentence('私は大きなだんごだ。')
#        assert self.gr.process() == true
#
#
#        self.gr.set_sentence('私は大きなだんごを食べた。')
#        assert self.gr.process() == false

        # With deep description of grammatical items
    #    assert(gr.grammar_rule_processor('〜は(prt-bnd)〜だ(v-aux)', '私は学生です。')) == True

    def test_rule__wa_desu(self):
        pass

    def test_rule__wa_da(self):
        pass
