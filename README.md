[![License: LGPL](https://img.shields.io/github/license/fsanzl/fonemas)](https://opensource.org/licenses/LGPL-2.1)
[![Version: 2.0.16](https://img.shields.io/github/v/release/fsanzl/fonemas)](https://pypi.org/project/fonemas/)
[![Python versions: 3.5, 3.6, 3.7, 3.8, 3.9](https://img.shields.io/pypi/pyversions/fonemas)](https://pypi.org/project/fonemas/)


<h2 align="center">Fonemas</h2>
<h3 align="center">A Python phonologic transcription library for Spanish</h2>


*fonemas* is a Python library of methods and functions for phonologic and phonetic ranscription of Spanish words.

This library is part of the research project [Sound and Meaning in Spanish Golden Age Literature](https://soundandmeaning.univie.ac.at/). This library was originally intended to analyse only pohonological features relevant to verse scansion. It has expanded its functionality ever since to become a fully featured phonological and phonetic analyser with IPA and SAMPA support.

## Installation

```bash
pip3 install fonemas
```

## Use

The library provides the class  *transcription(sentence, mono, epenthesis, aspiration, rehash, sampastr)*. The class takes the obligatoy argument *sentence*, which is a string of characters with a Spanish word or words. It optionally takes two Boolean arguments *mono*,  *epenthesis* and *aspiration* set to False as default.

- *mono* sets whether the output shows graphic stresses for monosyllabic words

- *epenthesis* set the behaviour S bfore consonant in onset (spiritu -> es pi ri tu|spi ri tu)

- *aspiration* inserts an aspiration modifier 'ʰ' in onset. This may be useful when dealing with ambiguous verses in classic poetry to choose which synaloepha to break.

- *rehash* moves last consonan on last-syllable coda to next's words first-syllable onset if it begins with a vowel.

- *sampastr* allows an alternativestress symbol, as '"' to prevent issues e.g. when using in a CSV file.



The class *transcription()* has three dataclass attributes, each with two attributes *{words, syllables}* containing each a list of strings, which may be words or syllables, respectively.

- *phonology* for the phonological transcription (requires UNICODE support).

- *phonetics* for the phonetic transcription in IPA symbols (requires UNICODE support).

- *sampa* for the phonetic transcription SAMPA transliteration.


```python
>>> from fonemas import transcription
>>> object = transcription('Averigüéis')
>>> a.phonology.words
['abeɾiˈgwejs']
>>> a.phonology.syllables
['a', 'be', 'ɾi', 'ˈgwejs']
>>> a.phonetics.words
['aβeɾiˈɣwejs']
>>> a.phonetics.syllables
['a', 'be', 'ɾi', 'ˈɣwejs']
>>> a.sampa.words
['aBeri"Gwejs']
>>> a.sampa.syllables
['a', 'Be', 'ri', '"Gwejs']
```

## Description

The transcription is done according to the Spanish phonology and phonotactics described by Quilis (2019).

## Known issues

The phonetic transcription lacks allophones represented in IPA with diacritics. They require double characters, which need a workaround to be evaluated. It can be solved using hacks for 'special cases', which I will do until figure out a general solution.

Non-Spanish languages with different prosodic rules but same spelling will cause problems, e.g.(lat.  'amor', 'amabor', 'amabar', 'amer' vs sp. 'amor'. 'labor', 'acabar', 'temer').

## Contributions

Feel free to contribute using the [GitHub Issue Tracker](https://github.com/fsanzl/fonemas/issues) for feedback, suggestions, or bug reports.

## Changelog

* 2.0.16

Isolated consonants

## Licence

This project is under GNU LGPL 2.1. See [LICENCE](https://github.com/fsanzl/fonemas/LICENCE) for details.

## References

Quilis, Antonio, *Tratado de fonología y fonética españolas*. Madrid, Gredos, 2019.
