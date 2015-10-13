import sonnet
import pytest


class TestSonnet(object):
    VALID_SONNET = """\
They that have power to hurt, and will do none,
That do not do the thing, they most do show,
Who moving others, are themselves as stone,
Unmoved, cold, and to temptation slow:
They rightly do inherit heaven's graces,
And husband nature's riches from expense,
Tibey are the lords and owners of their faces,
Others, but stewards of their excellence:
The summer's flower is to the summer sweet,
Though to it self, it only live and die,
But if that flower with base infection meet,
The basest weed outbraves his dignity:
For sweetest things turn sourest by their deeds,
Lilies that fester, smell far worse than weeds.
"""

    def test_rhyming(self):
        assert sonnet.check_rhyme('cool', 'fool')
        assert sonnet.check_rhyme('cat', 'hat')
        assert sonnet.check_rhyme("cat's", 'hats:')
        assert sonnet.check_rhyme('cats.', "...hats!?")

        assert not sonnet.check_rhyme('cats', 'pajamas')
        assert not sonnet.check_rhyme("cat's", 'pajamas')

        assert not sonnet.check_rhyme('cool', 'beans')
        assert sonnet.check_rhyme('fortuitous', 'conspicuous')
        assert not sonnet.check_rhyme('fabulous', 'cat')

    def test_multi_line_rhyming(self):
        assert sonnet.sonnet_rhyming_score('ababcdcdefefgg') == 1.0
        assert sonnet.sonnet_rhyming_score('ababcdcdefefeg') == 6.0 / 7.0

    @pytest.mark.skipif(reason='TODO')
    def test_legitimate_sonnet(self):
        assert sonnet.sonnet_rhyming_score(
            map(lambda s: s.split(), self.VALID_SONNET.lower().splitlines(False))) == 1.0

    @pytest.mark.skipif(reason='TODO')
    def test_syllables(self):
        assert sonnet.num_syllables('cat in the hat'.split()) == 4
        assert sonnet.num_syllables('luxurious bat demon calipers'.split()) == 10
