import unittest
import os
from xmlasdict import parse
from util4tests import run_single_test


class TestTemplateFitness(unittest.TestCase):
    """ Particularly tests some expectations we have inside the pysubyt project for dealing with xml
    """

    def test_fitness(self):
        fitnessfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'inputs', '02-fitness.xml')
        _ = parse(fitnessfile)

        assert f"{_.Element1.B}" == "en", "simple access should yield string content"
        assert f"{_.Element1.empty}" == "", "emtpy elements should evalute to ''"
        assert not(_.Element1.empty), "empty elements evaluate as False"
        assert f"{_.Element1.A}" == """<child1>
      <child1_a>text</child1_a>
      <child1_b>text</child1_b>
    </child1>
    <child2>text</child2>
    <child3>example@email.org</child3>""", "should keep whitespace and serialize the mixed content"
        assert f"{_.Element1.C.para}" == "Something a <bit> more unusual.", "CDATA content should be expanded"
        assert f"{_.Element1.C}" == "<para>Something a &lt;bit&gt; more unusual.</para>", "CDATA round-trip is not supported"

        expected_D_child1 = list()
        D_names = ['A', 'B']
        for i, d in enumerate(_.Element1.D):
            D_name = D_names[i]
            for j, dchild in enumerate(d.D_child1):
                expected = f"keyword{D_name}{(j+1)}"
                assert str(dchild) == expected, "the order of elements should be preserved when looping"
                expected_D_child1.append(expected)

        assert [f"{n}" for n in _['.//D_child1']] == expected_D_child1, "we should support deep listing of matching elements"
        assert [f"{n}" for n in _['.//D_child_source']] == ['ASFA', 'BSFA'], "idem"

        assert [f"{n}" for d in _.Element1.D for n in d.D_child1 if str(d.D_child_source) == 'ASFA'] == ['keywordA1', 'keywordA2']

        expected = ''.join(('Start of sentence <ulink url="http://example.org/path">',
                           '<Ee> Example link</Ee></ulink> and now there is the end of the sentence.'))
        assert f"{_.Element1.E.para}" == expected
        assert f"{_.Element1.E.para.ulink['@url']}" == 'http://example.org/path'

        assert f"{_.Element1.F.F_child1[0].F_child1_elements.Elem1}" == ""
        assert not(_.Element1.F.F_child1[0].F_child1_elements.Elem1)


if __name__ == '__main__':
    run_single_test(__file__)
