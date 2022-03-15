#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import silabeador


class transcription:
    def __init__(self, sentence, mono=False):
        self.sentence = self.__letters(self.__clean(sentence.lower()))
        self.phonology = self.transcription_fnl(self.sentence, mono)
        self.phonetics = self.transcription_fnt(
            ' '.join(self.phonology['sentence']), mono)
        self.ascii = self.ipa2ascii(self.phonetics)

    def ipa2ascii(self, sentence):
        words = ' '.join(sentence['sentence'])
        syllables = ' '.join(sentence['syllables'])
        translation = {'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u',
                       'j': 'j', 'w': 'w',
                       'b': 'b', 'β': 'B', 'd': 'd', 'ð': 'D',
                       'g': 'g', 'ɣ': 'G',
                       'p': 'p', 't': 't', 'k': 'k',
                       'l': 'l', 'ʎ': 'L', 'r': 'R', 'ɾ': 'r',
                       'm': 'm', 'ɱ': 'M', 'n': 'n', 'ŋ': 'N', 'ɲ': '9',
                       'tʃ': 'X', 'ʝ': 'y', 'x': 'x', 'χ': '4',
                       'f': 'f', 's': 's', 'z': 'z', 'θ': 'Z'}
        for phoneme in translation:
            words = words.replace(phoneme, translation[phoneme])
            syllables = syllables.replace(phoneme, translation[phoneme])
        return {'sentence': words, 'syllables': syllables}

    @staticmethod
    def __clean(sentence):
        symbols = ['(', ')', '—', '…', ',', ';', ':', '?', '!', "'", '.',
                   '«', '»', '–', '—', '“', '”', '‘', '’', '"', '-', '(', ')']
        letters = {'õ': 'o', 'æ': 'ae',
                   'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u'}
        for x in symbols:
            if x in sentence:
                sentence = sentence.replace(x, '')
        for x in letters:
            if x in sentence:
                sentence = sentence.replace(x, letters[x])
        return sentence

    def __splitvariables(self, sentence, ipa, mono):
        stressed = {'': '', '': '', '': ''}
        syllabic = []
        wordy = []
        for word in sentence.split():
            if len(word) > 5 and word.endswith('mente'):
                syllabification = silabeador.syllabification(
                    word.strip('mente'), True, ipa)
                syllables = syllabification.syllables + ['ˌmen', 'te']
                stress = syllabification.stress - 2
                word.replace('mente', 'ˌmente')
            else:
                syllabification = silabeador.syllabification(word, True, ipa)
                syllables = syllabification.syllables
                stress = syllabification.stress
            conta = 0
            diph = self.__diphthongs(word, syllables)
            word = diph['word']
            syllables = diph['syllables']
            syllables[stress] = f"'{syllables[stress]}"
            for slb in syllables:
                for char in slb:
                    if char == "'":
                        word = word[:conta] + "'" + word[conta:]
                    else:
                        conta += 1
            for idx, syllable in enumerate(syllables):
                if mono and len(syllables) == 1:
                    syllable = syllable.strip("'")
                for stress in stressed:
                    syllable = syllable.replace(stress, stressed[stress])
                syllabic += [syllable]
            if len(syllabic) == 1:
                word = word.replace("'", '')
            wordy += [word]
        return {'sentence': wordy, 'syllables': syllabic}

    @staticmethod
    def __letters(sentence):
        letters = {'b': 'be', 'c': 'ce', 'd': 'de', 'f': 'efe', 'g': 'ge',
                   'h': 'hache', 'j': 'jota', 'k': 'ka', 'l': 'ele',
                   'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'ku',
                   'r': 'erre', 's': 'ese', 't': 'te', 'v': 'ube',
                   'w': 'ubedoble', 'x': 'ekis', 'z': 'ceta', 'ph': 'peache'}
        for letter in letters:
            sentence = re.sub(rf'\b{letter}\b', 'letters[letter]', sentence)
        return sentence

    def transcription_fnl(self, sentence, mono):
        diacritics = {'á': 'a', 'à': 'a', 'ä': 'a',
                      'é': 'e', 'è': 'e', 'ë': 'e',
                      'í': 'i', 'ì': 'i', 'ï': 'i',
                      'ó': 'o', 'ò': 'o', 'ö': 'o',
                      'ú': 'u', 'ù': 'u', 'ü': 'u'}

        consonants = {'w': 'b', 'v': 'b', 'z': 'θ', 'x': 'ks', 'j': 'x',
                      'ñ': 'ɲ', 'qu': 'k', 'll': 'ʎ', 'ch': 'tʃ',
                      'r': 'ɾ', 'R': 'r',
                      'ce': 'θe', 'cé': 'θe', 'cë': 'θë',
                      'ci': 'θi', 'cí': 'θí', 'cï': 'θï', 'cj': 'θj',
                      'c': 'k', 'ph': 'f', 'h': ''}
        sentence = re.sub(r'(?:([nls])r|rr|\br)', r'\1R', sentence)
        sentence = sentence.replace('r', 'ɾ')
        for consonant in consonants:
            if consonant in sentence:
                sentence = sentence.replace(consonant, consonants[consonant])
        if 'y' in sentence:
            sentence = re.sub(r'y', 'ʝ', sentence)
            sentence = re.sub(r'ʝ\b', 'i', sentence)
        if 'g' in sentence:
            for reg in [
                [r'g([eiéíiëï])', rf'x\1'],
                    [r'g[u]([eiéíëï])', rf'g\1']]:
                sentence = re.sub(reg[0], reg[1], sentence)
            if 'gü' in sentence:
                sentence = sentence.replace('gü', 'gw')
        transcription = self.__splitvariables(sentence, False, mono)
        words = transcription['sentence']
        syllables = transcription['syllables']
        for letter in diacritics:
            words = [word.replace(letter, diacritics[letter])
                     for word in words]
            syllables = [syllable.replace(letter, diacritics[letter]) for
                         syllable in syllables]
        return {'sentence': words, 'syllables': syllables}

    def transcription_fnt(self, sentence, mono):
        sentence = sentence.replace(
            'b', 'β').replace(
            'd', 'ð').replace(
            'g', 'ɣ').replace("'", '').replace('ˌ', '')
        sentence = re.sub(r'([mnɲ ^])β', r'\1b', sentence)
        sentence = re.sub(r'([mnɲlʎ ^])ð', r'\1d', sentence)
        sentence = re.sub(r'([mnɲ ^])ɣ', r'\1g', sentence)
        sentence = re.sub(r'θ([bdgβðɣmnɲlʎrɾ])', r'ð\1', sentence)
        sentence = re.sub(r's([bdgβðɣmnɲlʎrɾ])', r'z\1', sentence)
        sentence = re.sub(r'f([bdgβðɣmnɲʎ])', r'v\1', sentence)
        allophones = {'nb': 'mb', 'nf': 'ɱf',
                      'nk': 'ŋk', 'ng': 'ŋg', 'nx': 'ŋx',
                      'xu': 'χu', 'xi': 'χi',
                      }
        if any(allophone in sentence for allophone in allophones):
            for allophone in allophones:
                sentence = sentence.replace(allophone, allophones[allophone])
        transcription = self.__splitvariables(sentence, True, mono)
        return {'sentence': transcription['sentence'],
                'syllables': transcription['syllables']}

    @staticmethod
    def __replace_ocurrence(string, origin, to, num):
        strange_char = '$&$@$$&'
        if string.count(origin) < 0:
            return string
        elif string.count(origin) > 1:
            return string.replace(origin, strange_char, num).replace(
                strange_char, origin, num-1).replace(to, strange_char, 1)
        else:
            return string.replace(origin, to)

    def __diphthongs(self, word, syllables):
        i = 0
        j = 0
        for idx, syllable in enumerate(syllables):
            if re.search('[aeiouáéíóú]{2,}', syllable):
                i += 1
                syllable = re.sub(r'([aeoáééó])i', rf'\1j', syllable)
                syllable = re.sub(r'([aeoáééó])u', rf'\1w', syllable)
                word = self.__replace_ocurrence(word,
                                                syllables[idx],
                                                syllable, i)

            if re.search('[ui][aeiouáééiíóú]', syllable):
                j += 1
                syllable = re.sub(r'i([aeouáééiíóú])', rf'j\1', syllable)
                syllable = re.sub(r'u([aeioáééiíóú])', rf'w\1', syllable)
                word = self.__replace_ocurrence(word,
                                                syllables[idx],
                                                syllable, j)
            syllables[idx] = syllable

        return {'word': word, 'syllables': syllables}

    def transcribe(frase):
        frase = self.__letras(frase.lower())
        t_fonologica = fonologica(frase)
        t_fonetica = fonetica(t_fonologica)
        silabas_des = silabeador.silabas(frase)
        silabas = silabas_des.silabas
        for idx, silaba in enumerate(silabas):
            if re.search('[aeiouáéíóú]{2,}', silaba):
                silaba = re.sub(r'([aeiouáééó])i', rf'\1j', silaba)
                silaba = re.sub(r'([aeiouáééó])u', rf'\1w', silaba)
            if re.search('[ui][aeiouáééiíóú]', silaba):
                silaba = re.sub(r'i([aeouáééiíóú])', rf'j\1', silaba)
                silaba = re.sub(r'u([aeioáééiíóú])', rf'w\1', silaba)
            for letra in diacriticos:
                if letra in silaba:
                    silaba = silaba.replace(letra, diacriticos[letra])
            silabas[idx] = silaba
        if silabas[0].startswith('ɾ'):
            silabas[0] = re.sub('^ɾ', 'r', silabas[0])
        silabas[silabas_des.tonica] = f"'{silabas[silabas_des.tonica]}"
        return silabas
