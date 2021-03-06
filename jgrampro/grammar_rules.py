"""
jgrampro.grammar_rules
~~~~~~~~~~~~~~~~~~~

Implements the grammar analysis of sentences given the grammar rule

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez
                <pablo.vazquez.dev@gmail.com>. See AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
    :Version: 0.1.1a
"""
import re
import json

from jgrampro.conf import global_settings as gs
from jgrampro.tools import mecab


class GrammarRuleProcessor:

    def __init__(self, rule='', sentence='。'):
        # Initialization
        self.set_sentence(sentence)
        self.rule = rule
        self.regexp_rule = ''
        self.definitions = dict()
        self.original_sentence = ''
        self.sentence_info = ''

        self.jap_rel = ''
        self.gram_rel = ''

        jap_path = (gs.PROJECT_DIR+'/grammar/'
                                   'jap_abbreviation_relationships.json')
        gram_path = (gs.PROJECT_DIR+'/grammar/'
                                    'grammar_relationships.json')

        with open(gram_path) as gram_relationships:
            self.gram_rel = json.loads(gram_relationships.read())

        with open(jap_path) as jap_relationships:
            self.jap_rel = json.loads(jap_relationships.read())

        # Mecab returns japanese language only, so this is a "translation" of
        # the grammar rules defined in grammar_relationships.json into
        # japanese, using jap_abbreviation_relationships.json file to do so
        for gram_key in self.gram_rel.keys():
            temp_list = []
            for gram_rel_item in self.gram_rel[gram_key]:
                temp_list.append(self.jap_rel[gram_rel_item])
            self.definitions[gram_key] = temp_list[:]

    def set_rule(self, text):
        """Sets the rule as a string, to check against a sentence
        """
        self.rule = text
        self.regexp_rule = text

    def set_sentence(self, sent):
        """Sets the sentence as a string, to check against the rule
        """
        sent_mecab_info = mecab.jap_text_info(sent)
        self.original_sentence = sent_mecab_info[0]
        self.sentence_info = sent_mecab_info[1]

    def set_data(self, rule, sent):
        """Sets the rule and the sentence to check
        """
        self.set_rule(rule)
        self.set_sentence(sent)

    # Replaces multiple items in a string using a dict as replacement guide
    @staticmethod
    def _multiple_replace(text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))

        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)

    def _build_regexp(self, grammar_rule):
        # If there is a  〜 at the beginning or ending, match any: '.+'
        regexp_of_rule = re.sub(r'^〜|〜$', r'.+', grammar_rule)

        # If there is a 〜 between rule items, match any but dot '[^。]+' 
        regexp_of_rule = re.sub(r'〜', r'[^。]+', regexp_of_rule)

        # Process parentheses
        if '(' in grammar_rule:
            # Get set of every parentheses items in the rule
            p_item = set(re.findall('\((.+?)\)', grammar_rule))

            # Replace each parenthesis using the gram_rel relationship and
            # merge them into the regexp
            for item in p_item:
                item_def_string = ('\({}\)'
                                   .format('\)|\('
                                           .join(self.gram_rel[item])))
                # Items with more than one definition should include itself
                # i.e. v --> (v)|(v-gen)|(v-aux)
                if len(self.gram_rel[item]) > 1:
                    item_def_string = '\('+item+'\)|' + item_def_string

                item_def_string = '(' + item_def_string + ')'

                regexp_of_rule = re.sub('\('+item+'\)',
                                        item_def_string,
                                        regexp_of_rule)

        return regexp_of_rule

    def _split_rule_items(self):
        # Get list of rule items
        trimmed_rule = re.sub(r'\s', '', self.rule)

        # Split and get the grammatical units of the rule
        symbols = ['〜', '。', '、', '「', '」', '｛', '｝']
        separators = '\(.+?\)|' + '|'.join(symbols)
        rule_items = re.split('(' + separators + ')', trimmed_rule)
        rule_units_list = []

        last_item_type = ''
        for item in rule_items:
            if item == '':
                continue

            # Discern between:
            # - Alone grammar rule between parentheses: (x)
            # - Complete grammar rule item: です(v),...
            # - Symbols: 〜,...
            if item[0] == '(':
                if last_item_type not in ['parentheses', '', 'symbol']:
                    rule_units_list[-1] += item
                else:
                    rule_units_list.append(item)
                last_item_type = 'parentheses'
            elif item[0] in symbols:
                rule_units_list.append(item)
                last_item_type = 'symbol'
            else:
                rule_units_list.append(item)
                last_item_type = 'kana_or_placeholder'

        return rule_units_list

    # Get list with the places where the PartOfSpeech (POS) match 
    # within the original sentence and the relative weight or precedence
    # being 0 if empty, and +1 for each alone grammar and +50 for kana/kanji 
    # in the pos tag:
    # - Empty: 0 
    # - Alone grammar rule between parentheses - (x): 1
    # - Complete grammar rule item - です(v),... : 51
    # - TO IMPLEMENT complex grammar - (v,com,5vsa): 3 
    # - TO IMPLEMENT complex kana+grammar - 無くし(v,com,5vsa): 53 
    def _get_grammar_item_positions_and_tag(self, pos_tag):
        tag_and_positions = {'tag': '', 'weight': 0, 'positions': []}
        has_kana = False
        # Getting the japanese version of the POS.
        # This is a list because the POS can be generic.
        # i.e.: (adj) will include any of (adj-i) and (adj-na)

        # Keep the original pos_tag
        tag_and_positions['tag'] = pos_tag
        tag_without_parentheses = re.sub(r'\(.+\)$', '', pos_tag)

        # If pos_tag is kana with parentheses
        pos_tag_gram = ''
        if '(' in pos_tag and pos_tag[0] != '(':
            has_kana = True
            # If the pos_tag contains kana or kanji plus parentheses, 
            # get the text inside the parentheses, omitting them
            # as pos_tag_gram
            pos_tag_gram = re.sub(r'^[^\(\)]+', '', pos_tag)
            pos_tag_gram = re.sub(r'\(|\)', '', pos_tag_gram)
            # Weight for xx(x) rule
            # The parentheses weigh +1 for each element
            pos_tag_gram_weight = len(re.split(r'[,-]', pos_tag_gram))
            kana_weight = 50
            tag_and_positions['weight'] = kana_weight + pos_tag_gram_weight

        elif pos_tag:
            # Keep the original pos_tag and get tag without parentheses
            pos_tag_gram = re.sub(r'\(|\)', '', pos_tag)
            pos_tag_gram_weight = len(re.split(r'[,-]', pos_tag_gram))
            tag_and_positions['weight'] = pos_tag_gram_weight

        japanese_pos_taglist = []
        if '(' in pos_tag:
            # Get the japanese equivalent tags for POS if rule requests them
            japanese_pos_taglist = self.definitions[pos_tag_gram]

        # Check POS within the sentence and build a list with their index
        for index, sentence_info_morpheme in enumerate(self.sentence_info):
            # Each tag is a list to test against each morpheme, because one 
            # tag can include several tags. i.e.(adj) = (adj-i) + (adj-na)
            is_tag_match = any(
                tag in sentence_info_morpheme.values()
                for tag in japanese_pos_taglist
            )
            # If rule has kana, check that kana matches
            # within the sentence also
            if has_kana and is_tag_match:
                is_tag_match = (tag_without_parentheses ==
                                sentence_info_morpheme['surface'])

            if is_tag_match:
                tag_and_positions['positions'].append(index)

        return tag_and_positions

    def _build_mock_sentence(self, rule_items):
        # Build a mock "sentence" where every char is 'x' respecting the 
        # punctuation and putting the chars or single tags that match 
        # with any of the items of the rule in their places. i.e.:
        # *rule => 〜と(prt)(adj)〜
        # *sentence => 私は小さいだんごと冷たいチェリイと飯を食べた。
        # *x-sentence => xx(adj)xと(adj)xとxxxx。
        gram_symbols = ['空白', '補助記号', '記号']

        # Empty mock sentence with punctuation
        mock_sentence = [
            info['surface'] if info['pos1_macrotaxonomy'] in gram_symbols
            else 'x'
            for info in self.sentence_info
        ]
        # Empty mock sentence initial weights
        mock_sentence_weights = [
            100 if info['pos1_macrotaxonomy'] in gram_symbols else 0
            for info in self.sentence_info
        ]

        for rule_tag in rule_items:
            if rule_tag != '〜':
                tag_and_positions = (
                    self._get_grammar_item_positions_and_tag(rule_tag))
                cur_tag = tag_and_positions['tag']
                cur_positions = tag_and_positions['positions']
                cur_weight = tag_and_positions['weight']

                for position in cur_positions:
                    if cur_weight > mock_sentence_weights[position]:
                        mock_sentence[position] = cur_tag
                        mock_sentence_weights[position] = cur_weight

        mock_sentence = ''.join(mock_sentence)

        return mock_sentence

    def _check_rule_compliance(self, rule_items):
        complies = False

        # Checking the grammatical compliance
        mock_sentence = self._build_mock_sentence(rule_items)

        # Check mock sentence against regexp of the rule
        if re.match(self.regexp_rule, mock_sentence):
            complies = True

        return complies

    def process(self):
        """This method does the actual check of the rule against the sentence
        """
        # Process the rule to get the necessary info to do the check
        rule_items_list = self._split_rule_items()

        self.regexp_rule = self._build_regexp(self.regexp_rule)

        # Check if the sentence complies with the rule
        complies_with_rule = self._check_rule_compliance(rule_items_list)

        return complies_with_rule


if __name__ == '__main__':
    # ## TO PUT A BREAKPOINT FOR DEBUG:  import ipdb; ipdb.set_trace()
    import sys

    gr = GrammarRuleProcessor()
    # gr.set_rule('〜は(prt)〜だ')
    # gr.set_sentence('私は大きなだんごを食べた。だ')
    # gr.set_rule('〜は(prt)だ(prt)')
    # gr.set_sentence('私はだ学生だ。')
    # gr.set_rule('〜は(prt)〜(v)〜だ(v)。')
    # gr.set_sentence('私はジョンです。彼女はテレサです。')
    # gr.set_rule('(v)。〜です(v)')
    if len(sys.argv) == 3:
        gr.set_data(sys.argv[1], sys.argv[2])
        if gr.process():
            print('The sentence: ', sys.argv[2],
                  ' complies with the rule: ', sys.argv[1])
        else:
            print('The sentence: ', sys.argv[2],
                  ' DOES NOT comply with the rule: ', sys.argv[1])
    else:
        print('Usage:\npython grammar_rules.py "<rule>" "<sentence>"')
