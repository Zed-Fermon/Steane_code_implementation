from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import Barrier



def get_steane_op(op: str):
	return gate_map[op]



def steane_x():

	logX = QuantumCircuit(7, name='X')

	logX.x(range(7))

	return logX.to_instruction()



def steane_y():

	logY = QuantumCircuit(7, name = 'Y')

	logY.y(range(7))

	return logY.to_instruction()



def steane_z():

	logZ = QuantumCircuit(7, name='Z')

	logZ.z(range(7))

	return logZ.to_instruction()



def steane_h():

	logH = QuantumCircuit(7, name='H')

	logH.h(range(7))

	return logH.to_instruction()



def steane_s():

	logS = QuantumCircuit(7, name = 'S')

	logS.s(range(7))

	return logS.to_instruction()



def steane_sdg():

	logS_inv = QuantumCircuit(7, name = 'Sdg')

	logS_inv.sdg(range(7))

	return logS_inv.to_instruction()



def steane_cx():

	logCNOT = QuantumCircuit(QuantumRegister(size = 7, name = "control"), 
		QuantumRegister(size = 7, name = "target"), name='CX')

	logCNOT.cx(range(7), range(7, 14))

	return logCNOT.to_instruction()



def steane_cz():

	logCZ = QuantumCircuit(QuantumRegister(size = 7, name = "control"), 
		QuantumRegister(size = 7, name = "target"), name='CZ')

	logCZ.cz(range(7), range(7, 14))

	return logCZ.to_instruction()



gate_map = {
	'x': steane_x(),
	'y': steane_y(),
	'z': steane_z(),
	'h': steane_h(),
	's': steane_s(),
	'sdg': steane_sdg(),
	'cx': steane_cx(),
	'cz': steane_cz(),
	'barrier': Barrier(0)
}