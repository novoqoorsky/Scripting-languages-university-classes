import sys

from computing.balancing_validator import BalancingValidator
from computing.matrix_computer import MatrixComputer
from computing.matrix_creator import MatrixCreator
from chembal_logging.logger import Logger
from parsing.equation_parser import EquationParser


class Balancer:
    """
    A class for performing all of the balancing operations.
    """

    def __init__(self, logging=True):
        """
        Sets up all the components.

        :param logging: whether to print logs or not
        """
        self.matrix_creator = MatrixCreator()
        self.matrix_computer = MatrixComputer()
        self.equation_parser = EquationParser()
        self.balancing_validator = BalancingValidator(logging=logging)
        self.logger = Logger(active=logging)

    def balance_equation(self, equation):
        """
        Computes the coefficients and prints the balanced equation.

        :param equation: the equation to be balanced
        :return: whether equation was successfully balanced or not
        :raises ValueError if the equation could not be balanced
        """
        left_side_molecules, right_side_molecules = self.__get_molecules(equation)
        self.logger.info("Parsing the equation...")
        equation_matrix = self.matrix_creator.create_equation_matrix(equation)
        self.logger.info("Creating the equation matrix...", args=equation_matrix)
        try:
            equation_coefficients = self.matrix_computer.compute_coefficients(equation_matrix)
        except ValueError as ex:
            self.logger.error("Coefficients computing error: ", ex)
            return False
        self.logger.info("Computed the coefficients:", args=equation_coefficients)
        self.__print_results(left_side_molecules, right_side_molecules, equation_coefficients)
        return self.balancing_validator.validate_balancing(
            left_side_molecules, right_side_molecules, equation_coefficients)

    def __get_molecules(self, equation):
        try:
            sides = self.equation_parser.parse_equation_into_two_sides(equation)
            left_side_molecules = self.equation_parser.parse_side_to_molecules(sides[0])
            right_side_molecules = self.equation_parser.parse_side_to_molecules(sides[1])
            return left_side_molecules, right_side_molecules
        except SyntaxError as ex:
            self.logger.error("Equation parsing error: ", ex)
            sys.exit(1)

    @staticmethod
    def __print_results(left_side_molecules, right_side_molecules, coefficients):
        print("")
        left_side_coefficients = [-int(x) for x in coefficients if x < 0]
        right_side_coefficients = [int(x) for x in coefficients if x > 0]
        for i in range(len(left_side_molecules)):
            print(left_side_coefficients[i], left_side_molecules[i], " ", end="")
            if i != len(left_side_molecules) - 1:
                print("+ ", end="")
        print("-> ", end="")
        for i in range(len(right_side_molecules)):
            print(right_side_coefficients[i], right_side_molecules[i], " ", end="")
            if i != len(right_side_molecules) - 1:
                print("+ ", end="")
        print("")
