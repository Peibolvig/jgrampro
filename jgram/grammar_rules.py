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

def grammar_rule_processor(rule, sentence_and_morphs_info):
    # Sentence_and_morphs_info contains the original sentence plus a
    # list of dictionaries, where each dictionary will be a morpheme 
    # with its info fields.
    original_sentence, sentence_info = sentence_and_morphs_info

    # Transform the rule into a regular expression
    rule_regexp = re.compile(rule.replace('〜', '.+'))

    # Test the sentence against the regular expression and check if
    # the sentence complies with the whole rule.
    ## If every rule component gives a 'true' value, then the sentence
    ## complies with the rule. Return true, else return false.
    return True if rule_regexp.match(original_sentence) else False

