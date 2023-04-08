from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import random


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