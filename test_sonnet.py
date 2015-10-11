import train


class TestSonnet(object):

    def test_rhyming(self):
        assert train.check_rhyme('cool', 'fool')
        assert train.check_rhyme('cat', 'hat')
        assert not train.check_rhyme('cool', 'beans')
        assert train.check_rhyme('fortuitous', 'conspicuous')
        assert not train.check_rhyme('fabulous', 'cat')
