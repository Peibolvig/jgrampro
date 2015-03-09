from jgram.tools import mecab
from jgram.grammar_rules import GrammarRuleProcessor

class TestGrammarRuleProcessor:
    gr = GrammarRuleProcessor()

    def test_placeholder(self):
        self.gr.set_rule('〜は〜だ')

        # OK sentence
        self.gr.set_sentence('私は学生だ。')
        assert self.gr.process() == True

        # KO sentence
        self.gr.set_sentence('源氏物語をやっと読み終わった。')
        assert self.gr.process() == False
    
        # Tricky string with two sentences
        self.gr.set_sentence('私は源氏物語をやっと読み終わった。飲んだ。')
        assert self.gr.process() == False
    
        # Empty sentence
        self.gr.set_sentence('')
        assert self.gr.process() == False

    def test_parenthesis(self):
        # With description of grammatical items
        self.gr.set_rule('〜は(prt)〜だ(v)')

        self.gr.set_sentence('私は大きなだんごだ。')
        assert self.gr.process() == True

        self.gr.set_sentence('私は大きなだんごを食べた。')
        assert self.gr.process() == False

        # With deep description of grammatical items
    #    assert(gr.grammar_rule_processor('〜は(prt-bnd)〜だ(v-aux)', '私は学生です。')) == True

    def test_rule__wa_desu(self):
        pass

    def test_rule__wa_da(self):
        pass
