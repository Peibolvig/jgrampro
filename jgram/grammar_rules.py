"""
jgram.grammar_rules
~~~~~~~~~~~~~~~~~~~

Implements the grammar analysis of sentences given the grammar rule

    :Copyright: (c)2015 by Pablo Vázquez Rodríguez <pablo.vazquez.dev@gmail.com>
                see AUTHORS for details
    :License: GPLv3, see LICENSE or http://www.gnu.org/licenses/gpl-3.0.html
              for more details
"""
import re
import json

##TODO: Ask for the "pythonic" way to solve the path
import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(curdir)
PROJECT_DIR = parentdir+'/jgram'
sys.path.insert(0, parentdir)
#################################################

from jgram.tools import mecab

class GrammarRuleProcessor:

    def __init__(self, rule='', sentence='。'):
        # Initialization
        self.set_sentence(sentence)
        self.rule = rule
        self.regexp_rule = ''
        self.definitions = dict()
        with open(PROJECT_DIR+'/definitions.json','r') as json_definitions:
            self.definitions = json.loads(json_definitions.read())

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

    # Recipe to replace multiple items in a string using a dict as replace guide
    def _multiple_replace(self, text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))
        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)

    def _build_regexp(self, regexp): 
        # If there is a  〜 at the beginning or ending, match any: '.+'
        regexp_of_rule = re.sub(r'^〜|〜$', r'.+', regexp)
        
        # If there is a 〜 between rule items, match any but dot '[^。]+' 
        regexp_of_rule = re.sub(r'〜', r'[^。]+', regexp_of_rule)

        # Escape any parenthesis
        regexp_of_rule = re.sub(r'\(', '\(', regexp_of_rule)
        regexp_of_rule = re.sub(r'\)', '\)', regexp_of_rule)

        return regexp_of_rule

    def _split_rule_items(self):
        # Get list of rule items
        trimmed_rule = re.sub(r'\s', '', self.rule)

        # Split and get the grammatical units of the rule
        symbols = ['〜', '。', '、', '「', '」', '｛' ,'｝']
        separators = '\(.+?\)|' + '|'.join(symbols)
        rule_items = re.split('(' + separators + ')', trimmed_rule)
        rule_units_list = []
        for item in rule_items:
            if item == '':
                continue

            if item[0] == '(':
                if last_item_type != 'parenthesis':
                    rule_units_list[-1] = rule_units_list[-1] + item
                else:
                    rule_units_list.append(item)
                last_item_type = 'parenthesis'
            else:
                rule_units_list.append(item)
                last_item_type = 'kana_or_placeholder'

        return rule_units_list

    # Get list with the places where the PartOfSpeech (POS) match 
    # within the original sentence.
    def _get_grammar_item_positions_and_tag(self, pos_tag):
        tag_and_positions = {'tag':'', 'positions':[]}

        has_kana = False
        only_has_kana = False
        # Getting the japanese version of the POS.
        # This is a list because the POS can be generic.
        # i.e.: (adj) will include any of (adj-i) and (adj-na)

        # Keep the original pos_tag
        tag_and_positions['tag'] = pos_tag
        tag_without_parenthesis = re.sub(r'\(.+\)$' ,'', pos_tag)

        # If pos_tag is kana with parenthesis
        if '(' in pos_tag and pos_tag[0] != '(':
            has_kana = True
            # If the pos_tag contains kana or kanji plus parenthesis, 
            # get the text inside the parenthesis, ommiting them
            # as pos_tag_gram
            pos_tag_gram = re.sub(r'^[^\(\)]+' ,'', pos_tag)
            pos_tag_gram = re.sub(r'\(|\)', '', pos_tag_gram)
        elif '(' not in pos_tag:
            # If it's only kana/kanji
            only_has_kana = True

            # Keep the original pos_tag and get tag without parenthesis
            pos_tag_gram = re.sub(r'\(|\)', '', pos_tag)
        else: 
            # Keep the original pos_tag and get tag without parenthesis
            pos_tag_gram = re.sub(r'\(|\)', '', pos_tag)

        japanese_pos_taglist = []
        if '(' in pos_tag:
            # Get the japanese equivalent tags for POS if rule requests them
            japanese_pos_taglist = self.definitions[pos_tag_gram]

        # Check POS within the sentence and build a list with their index
        item_places_list = []
        for index, sentence_info_morpheme in enumerate(self.sentence_info):
            # Each tag is a list to test against each morpheme, because one 
            # tag can include several tags. i.e.(adj) = (adj-i) + (adj-na)
            is_tag_match = any(
                                tag in sentence_info_morpheme.values() 
                                for tag in japanese_pos_taglist
                            )
            # If rule has kana, check that kana matches within the sentence also
            if has_kana and is_tag_match:
                is_tag_match = tag_without_parenthesis == sentence_info_morpheme['surface']

            if only_has_kana:
                is_tag_match = tag_without_parenthesis == sentence_info_morpheme['surface']

            if is_tag_match:
                tag_and_positions['positions'].append(index)

        return tag_and_positions

    def _check_rule_compliance(self, rule_items):
        complies = False
        mock_sentence = ''
#        import ipdb; ipdb.set_trace()
        # First check: Check the structure compliance
        if(re.match(self.regexp_rule, self.original_sentence)):
            # Second check: Checking the grammatical compliance
            #
            # Build a mock "sentence" where every char is 'x' respecting the 
            # punctuation and putting the chars or single tags that match 
            # with any of the items of the rule in their places. i.e.:
            # *rule => 〜と(prt)(adj)〜
            # *sentence => 私は小さいだんごと冷たいチェリイと飯を食べた。
            # *x-sentence => xx(adj)xと(adj)xとxxxx。
            gram_symbols = ['空白', '補助記号', '記号']

            # Empty mock sentence with punctuation
            mock_sentence = [
                                info['surface'] 
                                if info['pos1_macrotaxonomy'] in gram_symbols else 'x' 
                                for info in self.sentence_info
                            ]
            for rule_tag in rule_items:
                if rule_tag != '〜':
                    tag_and_positions = self._get_grammar_item_positions_and_tag(rule_tag)
                    cur_tag = tag_and_positions['tag']
                    cur_positions = tag_and_positions['positions']

                    for position in cur_positions:
                        mock_sentence[position] = cur_tag

            mock_sentence = ''.join(mock_sentence)

        # Check mock sentence against regexp of the rule
        if(re.match(self.regexp_rule, mock_sentence)):
            complies = True

        return complies


    def process(self):
        """This method do the actual check of the rule against the sentence
        """
        # Process the rule to get the neccessary info to do the check
        rule_items_list = []
        rule_items_list = self._split_rule_items()

        self.regexp_rule = self._build_regexp(self.regexp_rule)

        # Check if the sentence complies with the rule
        complies_with_rule = self._check_rule_compliance(rule_items_list)
        return complies_with_rule 


if __name__ == '__main__':
    ### TO PUT A BREAKPOINT FOR DEBUG:  import ipdb; ipdb.set_trace()
    gr = GrammarRuleProcessor()
    #gr.set_rule('〜は(prt)〜だ')
    #gr.set_sentence('私は大きなだんごを食べた。だ')
    #gr.set_rule('〜は(prt)だ(prt)')
    #gr.set_sentence('私はだ学生だ。')
    #gr.set_rule('〜は(prt)〜(v)〜だ(v)。')
    gr.set_sentence('私は時計とめがねとベルトを無くした。これはあなたのケイタイです。')
    gr.set_rule('〜は〜した')
    gr.process()
