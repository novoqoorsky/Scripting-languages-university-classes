from chembal_logging.logger import Logger
from parsing.molecule_parser import MoleculeParser


class BalancingValidator:
    """
    A class for validating balancing correctness.
    """

    def __init__(self, logging=True):
        self.logger = Logger(active=logging)
        self.molecule_parser = MoleculeParser()

    def validate_balancing(self, left_side_molecules, right_side_molecules, equation_coefficients):
        """
        Calculates number of atoms in both sides and compares it.

        :param left_side_molecules: the molecules in left side of the equation
        :param right_side_molecules: the molecules in right side of the equation
        :param equation_coefficients: the calculated coefficients
        :return: true if numbers of atoms match, false otherwise
        """
        self.logger.info("Validating balancing correctness...")
        left_side_atoms = self.calculate_side_molecules(left_side_molecules,
                                                        [-int(x) for x in equation_coefficients if x < 0])
        self.logger.info("Left side atoms: ", args=left_side_atoms)
        right_side_atoms = self.calculate_side_molecules(right_side_molecules,
                                                         [int(x) for x in equation_coefficients if x > 0])
        self.logger.info("Right side atoms: ", args=right_side_atoms)
        if left_side_atoms == right_side_atoms:
            self.logger.info("The equation is balanced correctly :)")
            return True
        self.logger.info("Wooops, something went wrong :(")
        return False

    def calculate_side_molecules(self, side_molecules, coefficients):
        side_atoms = {}
        for i in range(len(side_molecules)):
            molecule_atoms = self.molecule_parser.parse_molecule_into_atoms(side_molecules[i])
            for atom in molecule_atoms:
                if atom in side_atoms:
                    side_atoms[atom] += abs(coefficients[i]) * molecule_atoms[atom]
                else:
                    side_atoms[atom] = abs(coefficients[i]) * molecule_atoms[atom]
        return side_atoms
