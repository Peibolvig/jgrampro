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
from jgram.tools import mecab

class GrammarRuleProcessor:

    def __init__(self, rule='', sentence='。'):
        # Sentence_and_morphs_info contains the original sentence plus a
        # list of dictionaries, where each dictionary will be a morpheme 
        # with its info fields.
        self.set_sentence(sentence)
        self.rule = rule
        self.regexp_rule = ''
   
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

    def _process_placeholder(self): 
        # When the 〜 is at the beginning or ending, use '.+' regexp
        self.regexp_rule = re.sub(r'^〜|〜$', r'.+', self.regexp_rule)
        
        # When the 〜 is in between rule items, use '[。]+' 
        self.regexp_rule = re.sub(r'〜', r'[^。]+', self.regexp_rule)

    def _process_parenthesis(self):
        # The regexp can't contain the parenthesis of the rule, as it's
        # only to do the first check: "Structure matches the sentence"
        self.regexp_rule = re.sub(r'\(.+?\)', '', self.regexp_rule)

        # Get list of rule items
        trimmed_rule = re.sub(r'\s', '', self.rule)

        # Split and get the items
        rule_items = re.split('(\(.+?\)|〜)', trimmed_rule)
        rule_items = [i+j for i,j in zip(rule_items[::2], rule_items[1::2])]

        return rule_items

    def _check_rule_compliance(self, rule_items):
        for item in rule_items:
            # Check if item is a placeholder (〜), 
            # a part-of-speech-only item (contains only parenthesis or
            # contains hiragana, kanji,... (i.e.: も(prt) )
            if item == '〜':
               pass 
            elif re.match('^\(.+?\)', item):
                assert re.match('^\(.+?\)', item) == 'asdfasdf'
            else:
                pass

    def process(self):
        """This method do the actual check of the rule against the sentence
        """
        # Process the rule to get the neccessary info to do the check
        rule_items_list = []
        if '(' in self.rule:
            rule_items_list = self._process_parenthesis()

        if '〜' in self.rule:
            self._process_placeholder()

        # Check if the sentence complies with the rule
        self._check_rule_compliance(rule_items_list)


        # Test the sentence against the regular expression and check if
        # the sentence complies with the whole rule.
        ## If every rule component gives a 'true' value, then the sentence
        ## complies with the rule. Return true, else return false.
        return True if re.match(self.regexp_rule, self.original_sentence) else False
