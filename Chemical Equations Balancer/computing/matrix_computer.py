import unittest
import numpy as np
from numpy.linalg import LinAlgError

from computing.matrix_creator import MatrixCreator


class MatrixComputer:
    """
    A class for performing all the matrix related computations.
    See https://arxiv.org/ftp/arxiv/papers/1110/1110.4321.pdf for more details.
    """

    def compute_coefficients(self, matrix):
        """
        Computes the coefficients of a balanced chemical equation.

        :param matrix: the equation matrix
        :return: the coefficients
        :raises: ValueError upon the equation being skeletal
        """
        if len(matrix) > len(matrix[0]):
            matrix = np.delete(matrix, len(matrix) - 1, 0)
        if self.is_matrix_square(matrix):
            matrix = self.__handle_square_matrix_case(matrix)
        else:
            matrix = self.__handle_standard_case(matrix)
        try:
            matrix_inverse = np.linalg.inv(matrix)
        except LinAlgError:
            raise ValueError("Skeletal equation - cannot be balanced!")
        coefficients = matrix_inverse[:, len(matrix) - 1]
        return self.scale_the_coefficients(coefficients)

    def __handle_square_matrix_case(self, matrix):
        """
        Reduces the matrix to row-echelon form and augments it by
        replacing all-zeros vectors with nullity vectors.

        :param matrix: the equation matrix
        :return: the modified matrix
        """
        row_echelon_matrix = self.gaussian_elimination(matrix)
        total_molecules = len(matrix[0])
        nullity_vector = [0] * total_molecules
        nullity_vector[total_molecules - 1] = 1
        for i in range(len(row_echelon_matrix)):
            is_only_zeros = True
            for elem in row_echelon_matrix[i]:
                if not np.isnan(elem) and elem != 0:
                    is_only_zeros = False
            if is_only_zeros:
                row_echelon_matrix[i] = nullity_vector
        return row_echelon_matrix

    @staticmethod
    def __handle_standard_case(matrix):
        """
        Performs augmentation in standard case - when the equation
        matrix is not square to begin with.

        :param matrix: the equation matrix
        :return: the modified matrix
        """
        total_molecules = len(matrix[0])
        nullity_vector = [0] * total_molecules
        nullity_vector[total_molecules - 1] = 1
        for _ in range(abs(total_molecules - np.linalg.matrix_rank(matrix))):
            matrix = np.vstack([matrix, nullity_vector])
        return matrix

    @staticmethod
    def scale_the_coefficients(coefficients):
        """
        Scales the float coefficients so that the lowest of
        them equals 1 and the rest are integer in appropriate ratio.

        :param coefficients: the coefficients as float
        :return: the coefficients as integers
        """
        scale = 1
        for coefficient in coefficients:
            if not coefficient.is_integer():
                x = 1
                while x < 10000:
                    if (coefficient * x).is_integer():
                        if x >= scale:
                            scale = x
                            break
                    x += 1
        return [round(x) for x in coefficients * scale]

    @staticmethod
    def is_matrix_square(matrix):
        """
        Checks whether the matrix is square.

        :param matrix: the matrix
        :return: true if matrix is square, false otherwise
        """
        rows = len(matrix)
        return all(len(row) == rows for row in matrix)

    @staticmethod
    def gaussian_elimination(matrix):
        """
        Performs Gaussian elimination on the matrix to reduce
        it to row-echelon form.

        :param matrix: the matrix
        :return: the matrix reduced to row-echelon form
        """
        n = len(matrix)
        matrix_copy = matrix
        for k in range(n):
            for i in range(k, n):
                if abs(matrix_copy[i][k]) > abs(matrix_copy[k][k]):
                    matrix_copy[k], matrix_copy[i] = matrix_copy[i], matrix_copy[k]
                else:
                    pass
            for j in range(k + 1, n):
                q = 0
                if matrix_copy[k][k] != 0:
                    q = float(matrix_copy[j][k]) / matrix_copy[k][k]
                for m in range(k, n):
                    matrix_copy[j][m] -= q * matrix_copy[k][m]
        return matrix_copy


class MatrixComputerTest(unittest.TestCase):
    """
    A class for testing chemical equation coefficients computation.
    """

    matrix_computer = MatrixComputer()
    matrix_creator = MatrixCreator()

    def test_standard_cases(self):
        """
        Tests computations in standard cases - when the equation matrix
        is not square to begin with.
        """
        matrix = self.matrix_creator.create_equation_matrix("H2 + O2 -> H2O")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-2, -1, 2]))
        matrix = self.matrix_creator.create_equation_matrix("C7H16 + O2 -> CO2 + H2O")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-1, -11, 7, 8]))
        matrix = self.matrix_creator.create_equation_matrix("KMnO4 + HCl -> MnCl2 + Cl2 + KCl + H2O")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-2, -16, 2, 5, 2, 8]))
        matrix = self.matrix_creator.create_equation_matrix("KI + KClO3 + HCl -> I2 + H2O + KCl")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-6, -1, -6, 3, 3, 7]))
        matrix = self.matrix_creator.create_equation_matrix("CO2 + H2O -> C6H12O6 + O2")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-6, -6, 1, 6]))

    def test_square_matrix_cases(self):
        """
        Test computations in cases when the equation matrix
        is square to begin with.
        """
        matrix = self.matrix_creator.create_equation_matrix("CaO + N2O5 -> Ca(NO3)2")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-1, -1, 1]))
        matrix = self.matrix_creator.create_equation_matrix("PCl5 + H2O -> H3PO4 + HCl")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-1, -4, 1, 5]))
        matrix = self.matrix_creator.create_equation_matrix("AgI + Na2S -> Ag2S + NaI")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-2, -1, 1, 2]))
        matrix = self.matrix_creator.create_equation_matrix("Ba3N2 + H2O -> Ba(OH)2 + NH3")
        self.assertTrue(np.array_equal(self.matrix_computer.compute_coefficients(matrix), [-1, -6, 3, 2]))

    def test_skeletal_equation(self):
        """
        Tests computations in cases when the equation
        is skeletal - cannot be balanced.
        """
        matrix = self.matrix_creator.create_equation_matrix("FeS2 + HNO3 -> Fe2(SO4)3 + NO + H2SO4")
        self.assertRaises(ValueError, lambda: self.matrix_computer.compute_coefficients(matrix))
        matrix = self.matrix_creator.create_equation_matrix("CO + CO2 + H2 -> CH4 + H2O ")
        self.assertRaises(ValueError, lambda: self.matrix_computer.compute_coefficients(matrix))


if __name__ == '__main__':
    unittest.main()
