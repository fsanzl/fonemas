import re
from silabeador import Syllabification
from dataclasses import dataclass


@dataclass
class Values:
    words: list
    syllables: list


class Transcription:
    def __init__(self, sentence, mono=False, exceptions=1,
                 epenthesis=False, aspiration=False, rehash=False,
                 stress='"'):
        self.sentence = self.__clean(sentence, epenthesis)
        self.__exceptions = exceptions
        if rehash:
            self.sentence = self.make_rehash(self.sentence)
        self.phonology = self.transcription_fnl(self.sentence, mono,
                                                aspiration)
        self.phonetics = self.transcription_fnt(self.phonology)
        self.sampa = self.ipa2sampa(self.phonetics, stress)

    @staticmethod
    def __clean(raw_sentence, epen):
        letters = {'b': 'be', 'c': 'θe', 'ch': 'ʧe', 'd': 'de', 'f': 'efe',
                   'g': 'ge', 'h': 'haʧe', 'j': 'jota', 'k': 'ka', 'l': 'ele',
                   'll': 'eʎe', 'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'ku',
                   'r': 'erre', 's': 'ese', 't': 'te', 'v': 'ube',
                   'w': 'ubedoble', 'x': 'ekis', 'z': 'θeta'}
        symbols = ['(', ')', '¿', '?', '¡', '!', '«', '»', '“', '”', '‘', '’',
                   '[', ']', '—', '…', ',', ';', ':', "'", '.', '–', '"', '-']
        diacritics = {'à': 'á', 'è': 'é', 'ì': 'í', 'ò': 'ó', 'ù': 'ú',
                      'æ': 'e', 'ä': '_a', 'ë': '_e', 'ï': '_i',  'ö': '_o',
                      'ã': 'á', 'õ': 'ó', 'â': 'a', 'ê': 'e', 'î': 'i',
                      'ô': 'o', 'û': 'u', 'ç': 'θ'}
        raw_sentence = raw_sentence.lower()
        for char in letters:
            if re.search(rf'\b{char}\b', raw_sentence):
                raw_sentence = re.sub(rf'\b{char}\b', letters[char],
                                      raw_sentence)
        for match in letters:
            raw_sentence = re.sub(rf'\b{match}\b', letters[char], raw_sentence)
        for char in symbols:
            if char in raw_sentence:
                raw_sentence = raw_sentence.replace(char, ' ')
        for char in diacritics:
            if char in raw_sentence:
                raw_sentence = raw_sentence.replace(char, diacritics[char])
        if epen:
            raw_sentence = re.sub(r'\bs((?![aeiouáéíóú]))', r'es\1',
                                  raw_sentence)
        return raw_sentence

    @staticmethod
    def make_rehash(sentence):
        vowels = 'aeioujwăĕŏ'
        for idx, syllable in enumerate(sentence):
            if idx > 0 and len(syllable) > 1:
                if syllable[0].lower() in vowels and \
                        sentence[idx-1][-1].lower() not in vowels:
                    sentence[idx] = sentence[idx - 1][-1] + syllable
                    sentence[idx - 1] = sentence[idx - 1][:-1]
        return sentence

    def transcription_fnl(self, sentence, mono, aspiration):
        diacritics = {'á': 'a', 'à': 'a', 'ä': 'a',
                      'é': 'e', 'è': 'e', 'ë': 'e',
                      'ú': 'u', 'ù': 'u', 'ü': 'u',
                      'í': 'i', 'ì': 'i', 'ï': 'i',
                      'ó': 'o', 'ò': 'o', 'ö': 'o',
                      '_': ''}
        consonants = {'w': 'b', 'v': 'b', 'z': 'θ', 'ñ': 'ɲ', 'x': 'ks',
                      'j': 'x', 'r': 'ɾ', 'R': 'r', 'ce': 'θe', 'cé': 'θé',
                      'cë': 'θë', 'ci': 'θi', 'cí': 'θí', 'cï': 'θï',
                      'cj': 'θj', 'ch': 'ʧ', 'c': 'k', 'qu': 'k', 'll': 'ʎ',
                      'ph': 'f', 'h': ''}
        sentence = re.sub(r'(?:([nls])r|\br|rr)', r'\1R', sentence)
        if aspiration:
            sentence = re.sub(r'\bh', 'ʰ', sentence)
        for consonant in consonants:
            if consonant in sentence:
                sentence = sentence.replace(consonant, consonants[consonant])
        if 'y' in sentence:
            sentence = re.sub(r'\by\b', 'i', sentence)
            sentence = re.sub(r'uy\b', 'wi', sentence)
            sentence = re.sub(r'y\b', 'j', sentence)
            sentence = sentence.replace('y', 'ʝ')
            for key, value in diacritics.items():
                if key in 'áéíóú':
                    sentence = re.sub(rf'{value}ʝ\b', f'{key}i', sentence)
            sentence = re.sub(r'ʝ((?![aeiouáéíóú]))', r'i\1', sentence)
        if 'g' in sentence:
            for reg in [[r'g([eiéíiëï])', r'x\1'],
                        [r'g[u]([eiéíëï])', r'g\1']]:
                sentence = re.sub(reg[0], reg[1], sentence)
            sentence = re.sub(r'gü([eiéí])', r'gw\1', sentence, re.IGNORECASE)
            sentence = re.sub(r'gu([aoáó])', r'gw\1', sentence, re.IGNORECASE)
        transcription = self.__split_variables(sentence, mono)
        for key, value in diacritics.items():
            transcription.words = [word.replace(key, value)
                                   for word in transcription.words]
            transcription.syllables = [syllable.replace(key, value)
                                       for syllable in transcription.syllables]
        return transcription

    def __split_variables(self, sentence, mono):
        words = []
        syllables_sentence = []
        for word in sentence.split():
            if len(word) > 5 and word.endswith('mente'):
                syllabification = Syllabification(word=word[:-5],
                                                  exceptions=self.__exceptions,
                                                  ipa=True,
                                                  h=True)
                syllables = syllabification.syllables
                if len(syllables) > 1:
                    syllables = syllables + ['ˌmen', 'te']
                    stress = syllabification.stress - 2
                    word = word.replace('mente', 'ˌmente')
                else:
                    syllables = syllables + ['ˈmen', 'te']
                    stress = -2
            else:
                syllabification = Syllabification(word,
                                                  exceptions=self.__exceptions,
                                                  ipa=True,
                                                  h=True)
                syllables = syllabification.syllables
                stress = syllabification.stress
            syllables = self.__diphthongs(syllables)
            syllables[stress] = f'ˈ{syllables[stress]}'
            word = ''
            for syllable in syllables:
                if not mono and len(syllables) == 1:
                    syllable = syllable.strip('ˈ')
                syllables_sentence.append(syllable)
                word += syllable
            words.append(word)
        return Values(words, syllables_sentence)

    def __diphthongs(self, syllables):
        for idx, syllable in enumerate(syllables):
            if re.search(r'[aeiouáéó][ui]', syllable):
                syllable = re.sub(r'([aeouáéó])i', r'\1j', syllable)
                syllable = re.sub(r'([aeioáéó])u', r'\1w', syllable)
            if re.search(r'[ui][aeiouáéó]', syllable):
                syllable = re.sub(r'i([aeoáéó])', r'j\1', syllable)
                syllable = re.sub(r'u([aeoáéó])', r'w\1', syllable)
            syllables[idx] = syllable
        return syllables

    def transcription_fnt(self, phonology):
        words = ' '.join(phonology.words)
        syllables = '-'.join(phonology.syllables)
        return Values(self.__fsubstitute(words), self.__fsubstitute(syllables))

    @staticmethod
    def __fsubstitute(words):
        words = words.replace('b', 'β').replace('d', 'ð').replace('g', 'ɣ')
        words = re.sub(r'([mnɲ ^])(\-*)β', r'\1\2b', words)
        words = re.sub(r'([mnɲlʎ ^])(\-*)ð', r'\1\2d', words)
        words = re.sub(r'([mnɲ ^])(\-*)ɣ', r'\1\2g', words)
        words = re.sub(r'θ(\-*)([bdgβðɣmnɲlʎrɾ])', r'ð\1\2', words)
        words = re.sub(r's(\-*)([bdgβðɣmnɲlʎrɾ])', r'z\1\2', words)
        words = re.sub(r'f(\-*)([bdgβðɣmnɲʎ])', r'v\1\2', words)
        allophones = {'nb': 'mb', 'nˈb': 'mˈb', 'nf': 'ɱf', 'nˈf': 'ɱˈf',
                      'nk': 'ŋk', 'nˈk': 'ŋˈk', 'ng': 'ŋg', 'nˈg': 'ŋˈg',
                      'nx': 'ŋx', 'nˈx': 'ŋˈx', 'xu': 'χu', 'xo': 'χo',
                      'xw': 'χw', 'n-b': 'm-b', 'n-ˈb': 'm-ˈb', 'n-f': 'ɱ-f',
                      'n-ˈf': 'ɱ-ˈf', 'n-k': 'ŋ-k', 'n-ˈk': 'ŋ-ˈk',
                      'n-g': 'ŋ-g', 'n-ˈg': 'ŋ-ˈg', 'n-x': 'ŋ-x',
                      'n-ˈx': 'ŋ-ˈx'}
        if any(allophone in words for allophone in allophones):
            for key, value in allophones.items():
                words = words.replace(key, value)
        return words.replace('-', ' ').split()

    @staticmethod
    def ipa2sampa(ipa, sampastr):
        ipa = Values(ipa.words.copy(), ipa.syllables.copy())
        transliteration = {'β': 'B', 'ð': 'D', 'ɣ': 'G', 'ʎ': 'L', 'r': 'rr',
                           'ɾ': 'r', 'ɱ': 'M', 'ŋ': 'N', 'ɲ': 'J', 'ʧ': 'tS',
                           'ʝ': 'y', 'χ': '4', 'θ': 'T',
                           'ˈ': sampastr, 'ˌ': '%'}
        for key, value in transliteration.items():
            for idx, word in enumerate(ipa.words):
                ipa.words[idx] = word.replace(key, value)
            for idx, syllable in enumerate(ipa.syllables):
                ipa.syllables[idx] = syllable.replace(key, value)
        return ipa
