from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister



def correct_X(qc: QuantumCircuit, logQubit: list, ancQubits: list, ancReadout: AncillaRegister):

	qc.barrier()
	qc.append(parity_check(), logQubit+ancQubits)
	qc.measure([ancQubits[0], ancQubits[1], ancQubits[2]], [ancQubits[0], ancQubits[1], ancQubits[2]])

	qc.barrier()	
	with qc.if_test((ancReadout, 1)):
		qc.x(4)
	with qc.if_test((ancReadout, 2)):
		qc.x(5)
	with qc.if_test((ancReadout, 3)):
		qc.x(2)
	with qc.if_test((ancReadout, 4)):
		qc.x(6)
	with qc.if_test((ancReadout, 5)):
		qc.x(1)
	with qc.if_test((ancReadout, 6)):
		qc.x(0)
	with qc.if_test((ancReadout, 7)):
		qc.x(3)

	return qc



def correct_Z(qc: QuantumCircuit, logQubit: list, ancQubits: list, ancReadout: AncillaRegister):

	qc.barrier()
	qc.h(logQubit)
	correct_X(qc, logQubit, ancQubits, ancReadout)
	qc.h(logQubit)

	return qc



def correct_errors(qc: QuantumCircuit, logQubit: list, ancQubits: list, ancReadout: AncillaRegister):

	correct_X(qc, logQubit, ancQubits, ancReadout)
	correct_Z(qc, logQubit, ancQubits, ancReadout)
	qc.barrier()

	return qc



def parity_check():

	par_check = QuantumCircuit(10, name = "parity_check")

	par_check.cx([0, 0], [8, 9])
	par_check.cx([1, 1], [7, 9])
	par_check.cx([2, 2], [7, 8])
	par_check.cx([3, 3, 3], [7, 8, 9])
	par_check.cx(4, 7)
	par_check.cx(5, 8)
	par_check.cx(6, 9)

	return par_check.to_gate()