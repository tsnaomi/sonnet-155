import sonnet


class TestSonnet(object):
    ACTUAL_SHAKESPEARE = """\
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
""".lower().splitlines(False)

    def test_rhyming(self):
        assert sonnet.check_rhyme('cool', 'fool')
        assert sonnet.check_rhyme('cat', 'hat')
        assert not sonnet.check_rhyme('cool', 'beans')
        assert sonnet.check_rhyme('fortuitous', 'conspicuous')
        assert not sonnet.check_rhyme('fabulous', 'cat')

    def test_multi_line_rhyming(self):
        assert sonnet.sonnet_rhyming_score([
            'unique new york'.split(),
            'how now brown cow'.split()
        ]) == 0.0

        assert sonnet.sonnet_rhyming_score([
            'rhyming scheme'.split(),
            'steel beam'.split()
        ]) == 1.0
