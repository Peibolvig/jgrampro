from jgram import grammar_rules as gr

def test_grammar_rule_processor():
    assert(gr.grammar_rule_processor('〜は(Prt.)〜だ(V.aux)', '私は学生です。')) == True
    assert(gr.grammar_rule_processor('〜は〜だ', '私は学生だ。')) == True
    assert(gr.grammar_rule_processor('〜は〜だ', '源氏物語をやっと読み終わった。')) == False
    assert(gr.grammar_rule_processor('〜は〜だ', '私は源氏物語をやっと読み終わった。')) == False
    assert(gr.grammar_rule_processor('〜は〜だ', '')) == False

def test_rule__wa_desu():
    pass

def test_rule__wa_da():
    pass
