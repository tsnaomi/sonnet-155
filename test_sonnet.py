import sonnet


class TestSonnet(object):

    def test_rhyming(self):
        assert sonnet.check_rhyme('cool', 'fool')
        assert sonnet.check_rhyme('cat', 'hat')
        assert not sonnet.check_rhyme('cool', 'beans')
        assert sonnet.check_rhyme('fortuitous', 'conspicuous')
        assert not sonnet.check_rhyme('fabulous', 'cat')

    def test_multi_line_rhyming(self):
        assert not sonnet.validate_sonnet_rhyming(
            [
                'unique new york',
                'how now brown cow'
            ]
        )
        assert sonnet.validate_sonnet_rhyming(
            [
                'rhyming scheme',
                'steel beam'
            ]
        )
