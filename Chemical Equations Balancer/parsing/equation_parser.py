import unittest
import re


class EquationParser:
    """ A class for parsing molecules out of complete equation """

    @staticmethod
    def parse_equation_into_two_sides(equation):
        """
        Splits equation to left and right side. Raises SyntaxError if the equation does not meet format requirements.
        :param equation: the equation
        :type equation: string
        :return: separated sides of the equation
        """
        sides = equation.split('->')
        if len(sides) != 2:
            raise SyntaxError("Check your equation syntax - it should contain precisely one -> sign")
        return sides

    @staticmethod
    def parse_side_to_molecules(equation_side):
        """
        Splits a side of equation to molecules list. Additionally, checks if such split molecule contains
        any not allowed characters.
        :param equation_side: a side of the equation
        :return: list of molecules
        """

        molecules = equation_side.replace(" ", "").split("+")
        for molecule in molecules:
            if not re.match("^[A-Za-z0-9()]*$", molecule):
                raise SyntaxError("Molecule " + molecule + " contains an invalid character")
        return molecules


class EquationParserTest(unittest.TestCase):
    """ A class for testing equation parser correctness """

    equation_parser = EquationParser()

    def test_splitting_into_sides(self):
        self.assertRaises(SyntaxError, lambda: self.equation_parser.parse_equation_into_two_sides("H2 + O2 H2O"))
        self.assertEqual(self.equation_parser.parse_equation_into_two_sides("H2 + O2 -> H2O"), ["H2 + O2 ", " H2O"])

    def test_parsing_sides(self):
        self.assertEqual(self.equation_parser.parse_side_to_molecules("H2O + O2 "), ['H2O', 'O2'])
        self.assertRaises(SyntaxError, lambda: self.equation_parser.parse_side_to_molecules("(H2_O + O2"))
        self.assertEqual(self.equation_parser.parse_side_to_molecules(
            self.equation_parser.parse_equation_into_two_sides("CaO + N2O5 -> Ca(NO3)2")[1]), ['Ca(NO3)2'])


if __name__ == '__main__':
    unittest.main()
