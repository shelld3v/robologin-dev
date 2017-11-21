from difflib import SequenceMatcher
import re


class RatioDiffCalc:
    def get_regexp_from_diff(self, first_string, second_string):
        if first_string is None or second_string is None:
            return None

        matcher = SequenceMatcher(None, first_string, second_string)
        marks = []
        for blocks in matcher.get_matching_blocks():
            i = blocks[0]
            n = blocks[2]
            # empty block
            if n == 0:
                continue
            mark = first_string[i:i + n]
            marks.append(mark)
        regexp = '^.*{0}.*$'.format('.*'.join(map(re.escape, marks)))
        return regexp


    def get_quick_ratio(self, first_string, second_string):
        matcher = SequenceMatcher(None, first_string, second_string)
        matcher.set_seq1(first_string)
        matcher.set_seq2(second_string)
        ratio = matcher.quick_ratio()
        return ratio

    def find_marks_from_diff(self, first_string, second_string, min_matching_block=32):
        marks = []

        blocks = list(SequenceMatcher(None, first_string, second_string).get_matching_blocks())

        # Removing too small matching blocks
        for block in blocks[:]:
            (_, _, length) = block

            if length < min_matching_block:
                blocks.remove(block)

        # Making of dynamic markings based on prefix/suffix principle
        if len(blocks) > 0:
            blocks.insert(0, None)
            blocks.append(None)

            for i in range(len(blocks) - 1):
                prefix = first_string[blocks[i][0]:blocks[i][0] + blocks[i][2]] if blocks[i] else None
                suffix = first_string[blocks[i + 1][0]:blocks[i + 1][0] + blocks[i + 1][2]] if blocks[i + 1] else None

                if prefix is None and blocks[i + 1][0] == 0:
                    continue

                if suffix is None and (blocks[i][0] + blocks[i][2] >= len(first_string)):
                    continue

                marks.append((re.escape(prefix[int(-min_matching_block / 2):]) if prefix else None,
                                     re.escape(suffix[:int(min_matching_block / 2)]) if suffix else None))

        return marks

    def remove_marks(self, string, marks):
        """
        Removing dynamic content from supplied page basing removal on
        precalculated dynamic markings
        """
        if string:
            for item in marks:
                prefix, suffix = item

                if prefix is None and suffix is None:
                    continue
                elif prefix is None:
                    string = re.sub(r'(?s)^.+{0}'.format(re.escape(suffix)), suffix.replace('\\', r'\\'), string)
                elif suffix is None:
                    string = re.sub(r'(?s){0}.+$'.format(re.escape(prefix)), prefix.replace('\\', r'\\'), string)
                else:
                    string = re.sub(r'(?s){0}.+{1}'.format(re.escape(prefix), re.escape(suffix)), "{0}{1}".format(prefix.replace('\\', r'\\'), suffix.replace('\\', r'\\')), string)

        return string