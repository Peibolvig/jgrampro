from jgram.tools import mecab
from jgram.grammar_rules import GrammarRuleProcessor

class TestGrammarRuleProcessor:
    gr = GrammarRuleProcessor()

    def test_placeholder(self):
        # OK sentence
        self.gr.set_data('〜は〜だ', '私は学生だ。')
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
    #    assert(gr.grammar_rule_processor('〜は(prt)〜だ(v)', '私は学生です。')) == True
    #    assert(gr.grammar_rule_processor('〜は(prt-bnd)〜だ(v-aux)', '私は学生です。')) == True

    def test_rule__wa_desu(self):
        pass

    def test_rule__wa_da(self):
        pass
