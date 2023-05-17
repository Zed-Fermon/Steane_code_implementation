from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import random
import qiskit_aer.noise as noise



def get_noise_model(p1: float, p2: float):
	noise_model = noise.NoiseModel(basis_gates = [
		'id', 'x', 'y', 'z', 'h', 's', 'sdg', 'cx', 'cz'])
	# p1 = 1 gate error rate
	# p2 = 2 gate error rate

	# depolarizing errors
	error_1 = noise.depolarizing_error(p1, 1)
	error_2 = noise.depolarizing_error(p2, 2)

	# add error to single-qubit gates
	noise_model.add_all_qubit_quantum_error(error_1, ['x', 'y', 'z', 'h', 's', 'sdg'])

	# add error to two-qubit gates
	noise_model.add_all_qubit_quantum_error(error_2, ['cx', 'cz'])

	return noise_model



def apply_random_error(qc: QuantumCircuit, pError: int = 1):

	randError = random.random()
	error_qubit = random.randint(0, 6)
	error_type = random.randint(0, 2)

	if(pError >= randError):

		if(error_type == 0):
			qc.x(error_qubit)
		elif(error_type == 1):
			qc.y(error_qubit)
		elif(error_type == 2):
			qc.z(error_qubit)

	return qc