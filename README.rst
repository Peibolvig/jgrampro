.. .. contents:: Table of contents

============
Introduction
============
~~~~~~~~~~~~~~~~~
What is JGramPro?
~~~~~~~~~~~~~~~~~
JGramPro is an application to know which Japanese grammar rules a text complies with.

Given a source of grammar rules and a Japanese text, will return which of the given rules the text uses.

Right now, JGramPro is in a very 'alpha' state, so is not yet implemented in a comfortable way and it's likely to have many bugs.

To try JGramPro in this early state, go to `How to use JGramPro?`_

~~~~~~~~~~~~~
Why JGramPro?
~~~~~~~~~~~~~
JGramPro is made because I want to be able to answer the next questions without effort, and focus in learn and not wasting much time choosing materials to study or review what I've learn:

    * ¿Can I read this text?
    * ¿Can I watch this movie without subtitles or with them in Japanese?
    * ¿What do I need to learn to read/watch this book/movie?
    * ¿Is this text suitable for a JLPT5/4/3/2/1 learner?
    * I need sentences to review my material but I'm already bored of the same texts every time, ¿is there a way to get new material without effort?

This functionality could be amazing altogether with a vocabulary extractor (maybe JGramPro could have one in the future).

My mid-term goal for JGramPro is making it "good enough" to be functional.

==============
Using JGramPro
==============
~~~~~~~~~~~~~~~~~~~~~~~~
How to install JGramPro?
~~~~~~~~~~~~~~~~~~~~~~~~
JGramPro is tested only on Linux (Fedora). It's likely to work on other Linux distributions as well.
Future support for Windows is planned, but it's not a top priority right now.

Follow this steps to install:
    #. Clone the repository: 

        .. code::

            git clone https://github.com/Peibolvig/jgrampro.git

    #. Install mecab system wide:

        **Fedora / CentOS / RedHat**

        .. code::

            sudo yum install mecab

        **Debian / Ubuntu / Mint and derivatives**

        .. code::

            sudo apt-get install mecab

        **Installation from source**
        
        Download mecab-X.X.tar.gz from: 
        
        https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE
        
        and then:

        .. code::

            % tar zxfv mecab-X.X.tar.gz
            % cd mecab-X.X
            % ./configure 
            % make
            % make check
            % su
            # make install

    #. Prepare the environment (download dictionaries, patch dicrc,...):

        .. code::

           make setdevelop

~~~~~~~~~~~~~~~~~~~~
How to use JGramPro?
~~~~~~~~~~~~~~~~~~~~

Simple example
~~~~~~~~~~~~~~
Once you have JGramPro installed, dependencies included, there is no fancy way to use it yet.
Here is an example:

    Syntax is like: 
        *python grammar_rules.py "<rule>" "<sentence>"*

    .. code::

        cd jgrampro/
        python grammar_rules.py "〜は(prt)〜だ(v-aux)" "私はだ学生だ。"
         

~~~~~~~~~~~~~~~~~~~~~~~~~~
How to write grammar rules
~~~~~~~~~~~~~~~~~~~~~~~~~~
Grammar rules for JGramPro have 2 kinds of elements:

    * **Morpheme info [ ex. です(v-aux) ]**: 
    
        The morpheme to match and it's Part Of Speech(POS) tag. POS tags are always between parentheses.

        :Note: See :ref:`Part Of Speech Tags` for a list with the available POS tags
    * **Placeholder char [ 〜 ]** : Indicates that one or more chars (whatever they are) must match in the place it is within the rule.

So, if we take the rule "〜は(prt)〜だ(v-aux)", we are saying that to comply with it, the sentence has to:
    1. Match any amount of chars at the beginning of the sentence...
    2. ...followed by the text は, but only if it is a particle (prt)...
    3. ...followed by any amount of chars...
    4. ...and finally, followed by the text だ, but only if it is an auxiliary verb (v-aux).

~~~~~~~~~~~~~~~~~~~~~~
Running the test suite
~~~~~~~~~~~~~~~~~~~~~~
Just type **make test** in the root folder of the project.

==========================================
How to contribute to the JGramPro project?
==========================================
This is a personal project and I'm sharing it because I guess that somebody could use it.
Development depends on my free time and many other personal stuff.

If you want to contribute to the project you're welcome. You can do so in many ways; here are some examples of what you can do:

    * Providing grammar rules (Notice that grammar syntax is in early state, so it could change in the next releases). See `How to use JGramPro?`_ for more info on how to contribute with grammar rules.
    * Fix bugs
    * Beta test
    * If you implement some features you can share them
    * Translate documentation
    * Create new documentation
    * Share this project with other people interested
    * If the application improves your Japanese, please let me know, It'll make me very happy to hear success stories from you ;)

You can contact me in this email: pablo.vazquez.dev@gmail.com

=======
Credits
=======
.. For authors and contributors, see the AUTHORS file
.. include:: ../AUTHORS.rst


~~~~~~~~~~~~
Dependencies
~~~~~~~~~~~~
You can grab the licenses for each of the dependencies inside the
licenses folder: **licenses/<dependency_name>**

.. topic:: mecab v0.996

    :Authors:
        * Taku Kudo <taku@chasen.org>
        * Nippon Telegraph and Telephone Corporation
    :License: Released under any of the GPL v2, the LGPL v2.1 or the BSD Licenses.
    :Web: http://taku910.github.io/mecab/
    :Sources: https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE
    :Mirror: https://drive.google.com/uc?export=download&id=0B_NO47cRQb6_V0t2Ry0xMGU3Yzg

.. topic:: mecab-ipadic v2.7.0-20070801

    :Authors:
        * Taku Kudo <taku@chasen.org>
        * Masayuki Asahara <masayu-a@is.aist-nara.ac.jp>
        * Yuji Matsumoto <matsu@is.aist-nara.ac.jp>
        * Nara Institute of Science and Technology
    :License: Released under an open custom license by Nara Institute of Science and Technology
    :Web: http://taku910.github.io/mecab/
    :Sources: https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM
    :Mirror: https://drive.google.com/uc?export=download&id=0B_NO47cRQb6_TURCR29oX0h4dFE

.. topic:: mecab-juman v7.0-20130312:

    :Authors:
        * Taku Kudo <taku@chasen.org>
        * University of Tokyo
    :License: Released under a BSD License.
    :Web: http://taku910.github.io/mecab/
    :Sources: https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7X2pESGlLREpxdXM
    :Mirror: https://drive.google.com/uc?export=download&id=0B_NO47cRQb6_NHJXSm9vUndLY3c

.. topic:: unidic-mecab v2.1.2:

    :Authors: The Unidic Consortium
    :License: Released under any of the GPL v2, the LGPL v2.1 or the BSD Licenses.
    :Web: http://unidic.sourceforge.jp/
    :Sources: http://sourceforge.jp/projects/unidic/downloads/58338/unidic-mecab-2.1.2_src.zip
    :Mirror: https://drive.google.com/uc?export=download&id=0B_NO47cRQb6_WjE3d1lPQkwxWHM
