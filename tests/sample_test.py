from jgram.tools import mecab


def test_prueba():
    assert mecab.jap_text_info('てと') == 'test'
