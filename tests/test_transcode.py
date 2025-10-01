
from redbetter import transcode


def test_get_suitable_basename_ascii():
    name = 'Artist - Album (2000) [FLAC]'
    expected = name
    actual = transcode.get_suitable_basename(name)
    assert expected == actual


def test_get_suitable_basename_japanese():
    name = u'Nihon Kogakuin College (日本工学院専門学校) - (1985) Pink Papaia {NKS MD8503A 24-96 Vinyl} [FLAC]'
    expected = name
    actual = transcode.get_suitable_basename(name)
    assert expected == actual


def test_get_suitable_basename_illegal_characters():
    name = 'fi:l*e/p\\\"a?t>h|.t<xt \\0_abc<d>e%f/(g)h+i_0.txt'
    expected = 'fi,lep,ath.txt ,0_abcde%f(g)h+i_0.txt'
    actual = transcode.get_suitable_basename(name)
    assert expected == actual
