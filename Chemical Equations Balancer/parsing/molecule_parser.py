import re
import unittest

from collections import Counter, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    """
    A trick for creating Counter object that keeps order of insertion.
    """
    pass


class MoleculeParser:
    """ A class for extracting atoms and their counts from molecules. """

    def parse_molecule_into_atoms(self, molecule):
        """
        Creates a dictionary, where atom symbol is a key and its count is the value.
        :param molecule: the molecule
        :type molecule: string
        :return: the dictionary
        """

        self.validate_molecule_format(molecule)
        parts = filter(bool, re.split('([A-Z][a-z]*|\(|\))', molecule))
        stack = [[]]
        for part in parts:
            if part == '(':
                stack.append([])
            elif part == ')':
                stack[-2].append(stack.pop())
            elif part.isdigit():
                stack[-1].append(int(part) * stack[-1].pop())
            else:
                stack[-1].append([part])
        count = OrderedCounter()
        while stack:
            if isinstance(stack[0], list):
                stack.extend(stack.pop(0))
            else:
                count[stack.pop(0)] += 1
        return count

    @staticmethod
    def validate_molecule_format(molecule):
        """
        Checks whether given molecule meets format requirements
        :param molecule: the molecule
        :type molecule: string
        """

        if len(molecule) == 0:
            raise SyntaxError("Not a molecule nor atom")
        opening_brackets = [m.start() for m in re.finditer('\(', molecule)]
        closing_brackets = [m.start() for m in re.finditer('\)', molecule)]
        if len(opening_brackets) != len(closing_brackets):
            raise SyntaxError("Brackets do not match")


class MoleculeParserTest(unittest.TestCase):
    """ A class for testing parser correctness on molecules of different difficulty level """

    molecule_parser = MoleculeParser()

    def test_simple_molecules_parsing(self):
        water_parsing = self.molecule_parser.parse_molecule_into_atoms('H2O')
        self.assertEqual(water_parsing['H'], 2)
        self.assertEqual(water_parsing['O'], 1)
        self.assertRaises(SyntaxError, lambda: self.molecule_parser.parse_molecule_into_atoms('(H2O'))
        self.assertRaises(SyntaxError, lambda: self.molecule_parser.parse_molecule_into_atoms('H2O)'))

    def test_more_complicated_molecules_parsing(self):
        lactic_acid_parsing = self.molecule_parser.parse_molecule_into_atoms('CH3CH(OH)COOH')
        self.assertEqual(lactic_acid_parsing['C'], 3)
        self.assertEqual(lactic_acid_parsing['H'], 6)
        picric_acid_parsing = self.molecule_parser.parse_molecule_into_atoms('C6H2(NO2)3OH')
        self.assertEqual(picric_acid_parsing['C'], 6)
        self.assertEqual(picric_acid_parsing['H'], 3)
        self.assertEqual(picric_acid_parsing['N'], 3)
        self.assertEqual(picric_acid_parsing['O'], 7)

    def test_hardcore_molecules_parsing(self):
        hardcore_molecule_parsing = self.molecule_parser.parse_molecule_into_atoms('K4(ON(SO3)2)2')
        self.assertEqual(hardcore_molecule_parsing['K'], 4)
        self.assertEqual(hardcore_molecule_parsing['O'], 14)
        self.assertEqual(hardcore_molecule_parsing['N'], 2)
        self.assertEqual(hardcore_molecule_parsing['S'], 4)


if __name__ == '__main__':
    unittest.main()
