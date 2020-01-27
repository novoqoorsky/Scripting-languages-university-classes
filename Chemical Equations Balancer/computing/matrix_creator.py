import unittest
import numpy as np
from collections import OrderedDict

from parsing.equation_parser import EquationParser
from parsing.molecule_parser import MoleculeParser


class MatrixCreator:
    """
    A class for creating equation's matrix.
    The matrix is a N x M matrix, where N is the number of unique atoms in the whole equation
    and M is the number of reactants (molecules).
    """

    def __init__(self):
        self.equation_parser = EquationParser()
        self.molecule_parser = MoleculeParser()

    def create_equation_matrix(self, equation):
        """
        Creates the matrix for an equation.
        For the simplest example - water synthesis equation (H2 + O2 -> H2O), the matrix looks like:
                    H2  O2  H2O
        H           2   0   2
        O           0   2   1

        :param equation: the equation
        :return: the equation matrix
        """
        equation_sides = self.equation_parser.parse_equation_into_two_sides(equation)
        left_side_molecules = self.equation_parser.parse_side_to_molecules(equation_sides[0])
        right_side_molecules = self.equation_parser.parse_side_to_molecules(equation_sides[1])
        atoms_dictionary = self.create_atoms_dictionary(left_side_molecules, right_side_molecules)
        return np.array(list(atoms_dictionary.values()))

    def create_atoms_dictionary(self, left_side_molecules, right_side_molecules):
        """
        Creates a dictionary of atoms, where key is an unique atom and the value is a list of
        the atoms numbers in a particular molecule.

        :param left_side_molecules: molecules in left side of the equation
        :param right_side_molecules: molecules in right side of the equation
        :return: the dictionary
        """
        atoms_dictionary = OrderedDict()
        self.__parse_unique_atoms(atoms_dictionary, left_side_molecules)
        self.__add_side_molecules_atoms_to_dictionary(left_side_molecules, atoms_dictionary)
        self.__add_side_molecules_atoms_to_dictionary(right_side_molecules, atoms_dictionary)
        return atoms_dictionary

    def __add_side_molecules_atoms_to_dictionary(self, side_molecules, atoms_dictionary):
        for molecule in side_molecules:
            atoms_in_the_molecule = self.molecule_parser.parse_molecule_into_atoms(molecule)
            for unique_atom in atoms_dictionary:
                if unique_atom in atoms_in_the_molecule:
                    atoms_dictionary[unique_atom].append(atoms_in_the_molecule[unique_atom])
                else:
                    atoms_dictionary[unique_atom].append(0.0)

    def __parse_unique_atoms(self, atoms_dictionary, one_side_of_equation):
        for molecule in one_side_of_equation:
            atoms_in_the_molecule = self.molecule_parser.parse_molecule_into_atoms(molecule)
            for atom in atoms_in_the_molecule:
                atoms_dictionary[atom] = []


class MatrixCreatorTest(unittest.TestCase):
    """
    A class for testing atoms dictionary and matrix creation for equations of
    different difficulty level.
    """

    matrix_creator = MatrixCreator()

    def test_atoms_dictionary_creation(self):
        self.assertEqual(self.matrix_creator.create_atoms_dictionary(['H2', 'O2'], ['H2O']),
                         {'H': [2, 0, 2], 'O': [0, 2, 1]})
        self.assertEqual(self.matrix_creator.create_atoms_dictionary(['CaO', 'N2O5'], ['Ca(NO3)2']),
                         {'O': [1, 5, 6], 'Ca': [1, 0, 1], 'N': [0, 2, 2]})

    def test_simple_matrix_creation(self):
        simple_equation_matrix = self.matrix_creator.create_equation_matrix("H2 + O2 -> H2O")
        self.assertTrue((simple_equation_matrix[0] == [2, 0, 2]).all())
        self.assertTrue((simple_equation_matrix[1] == [0, 2, 1]).all())

    def test_complicated_matrix_creation(self):
        complicated_equation_matrix = self.matrix_creator.create_equation_matrix("KMnO4 + HCl -> Mn(Cl)2 + Cl2 + KCl + H2O")
        self.assertTrue(np.array_equal(complicated_equation_matrix[:, 0], [1, 1, 4, 0, 0]))
        self.assertTrue(np.array_equiv(complicated_equation_matrix[:, len(complicated_equation_matrix[0]) - 1],
                                       [0, 0, 1, 2, 0]))


if __name__ == '__main__':
    unittest.main()
