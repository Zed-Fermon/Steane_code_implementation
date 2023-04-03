from qiskit import QuantumCircuit


def steane_x():

	logX = QuantumCircuit(7, name='logical_X')

	logX.x(range(7))

	logX.to_gate()
	return logX



def steane_z():

	logZ = QuantumCircuit(7, name='logical_Z')

	logZ.z(range(7))

	logZ.to_gate()
	return logZ


def steane_h():

	logH = QuantumCircuit(7, name='logical_Hadamard')

	logH.h(range(7))

	logH.to_gate()
	return logH


def steane_cx():

	logCNOT = QuantumCircuit(14, name='logical_CNOT')

	logCNOT.cx(range(7), range(7, 14))

	logCNOT.to_gate()
	return logCNOT