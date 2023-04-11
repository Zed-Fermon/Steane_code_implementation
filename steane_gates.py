from qiskit import QuantumCircuit, QuantumRegister


def get_steane_op(op: str):
	return gate_map[op]


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

	logCNOT = QuantumCircuit(QuantumRegister(size = 7, name = "control"), 
		QuantumRegister(size = 7, name = "target"), name='logical_CNOT')

	logCNOT.cx(range(7), range(7, 14))

	logCNOT.to_gate()
	return logCNOT


def steane_cz():

	logCZ = QuantumCircuit(QuantumRegister(size = 7, name = "control"), 
		QuantumRegister(size = 7, name = "target"), name='logical_CZ')

	logCZ.cz(range(7), range(7, 14))

	logCZ.to_gate()
	return logCZ


gate_map = {
	'x': steane_x(),
	'z': steane_z(),
	'h': steane_h(),
	'cx': steane_cx(),
	'cz': steane_cz()
}