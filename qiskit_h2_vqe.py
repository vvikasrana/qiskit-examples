from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.algorithms.ground_state_solvers import GroundStateEigensolver

from qiskit_algorithms.minimum_eigensolvers import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_ibm_runtime import EstimatorV2 as Estimator
#from qiskit.primitives.base import BaseEstimatorV1

#define a tiny mulecule
driver = PySCFDriver(
    atom= "H 0 0 0; H 0 0 0.735",
    basis = "sto3g", charge=0, spin=0, unit=DistanceUnit.ANGSTROM
)

problem = driver.run()

# map the electric structure of the qubit
mapper = JordanWignerMapper()

ansatz = UCCSD(
    num_spatial_orbitals=problem.num_spatial_orbitals,
    num_particles=problem.num_particles,
    qubit_mapper=mapper,
    initial_state=HartreeFock(problem.num_spatial_orbitals, problem.num_particles, mapper)
)

vqe = VQE(Estimator(), ansatz, SLSQP(maxiter=500))
solver = GroundStateEigensolver(mapper, vqe)
result = solver.solve(problem)

print("Estimated total ground energy state:", result.total_energies[0])