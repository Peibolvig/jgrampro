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
        self.processed_rule = ''
   
    def set_rule(self, text):
        self.rule = text

    def set_sentence(self, sent):
        sent_mecab_info = mecab.jap_text_info(sent)
        self.original_sentence = sent_mecab_info[0]
        self.sentence_info = sent_mecab_info[1]

    def set_data(self, rule, sent):
        self.set_rule(rule)
        self.set_sentence(sent)

    # Return string with escaped custom tags to use into regexps
    def _esc(self, tagged_text):
        esc_text = tagged_text
        esc_text = esc_text.replace('[[', '\[\[') 
        esc_text = esc_text.replace(']]', '\]\]') 
        return esc_text

    # Recipe to replace multiple items in a string using a dict as replace guide
    def _multiple_replace(self, text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))
        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)

    def _process_placeholder(self): 
        # When the 〜 is at the beginning or ending, use '.+' regexp
        self.processed_rule = re.sub(self._esc(r'^[[ph]]|[[ph]]$'), r'.+', self.processed_rule)
        
        # When the 〜 is in between rule items, use '[。]+' 
        self.processed_rule = re.sub(self._esc(r'[[ph]]'), r'[^。]+', self.processed_rule)

    def _process_plus(self):
        pass

    def _process_braces(self):
        pass

    def _process_parenthesis(self):
        pass

    def _process_empty(self):
        pass

    def process(self):
        # To avoid problems with regexp, because of some symbols used in the
        # grammar "minilanguage" as the '+' plus sign, every sign is converted
        # into a textcode. As follows:
        repdict = {
                    '〜':'[[ph]]', 
                    '+':'[[pl]]', 
                    '{':'[[bo]]', 
                    '}':'[[bc]]', 
                    '(':'[[po]]', 
                    ')':'[[pc]]', 
                    '∅':'[[em]]', 
                    '/':'[[sl]]'
        } 
        self.processed_rule = self._multiple_replace(self.rule, repdict)

        # Transform the rule into a regular expression
        if '〜' in self.rule:
            self._process_placeholder()

        if '+' in self.rule:
            # Process plus signs
            self._process_plus()

        if '{' in self.rule:
            # Process braces
            self._process_braces()

        if '(' in self.rule:
            # Process braces
            self._process_parenthesis()

        if '∅' in self.rule:
            # Process empty set
            self._process_empty()


        # Test the sentence against the regular expression and check if
        # the sentence complies with the whole rule.
        ## If every rule component gives a 'true' value, then the sentence
        ## complies with the rule. Return true, else return false.
        return True if re.match(self.processed_rule, self.original_sentence) else False
