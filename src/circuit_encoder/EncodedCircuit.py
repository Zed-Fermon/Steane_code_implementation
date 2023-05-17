from typing import Union

from qiskit import (QuantumCircuit, QuantumRegister, AncillaRegister, ClassicalRegister,
	transpile)
from qiskit.circuit import Qubit, Barrier


class EncodedCircuit:

#==========================================================================================
#
#								Constructor
#
#==========================================================================================
	
	def __init__(self, faultyQC: QuantumCircuit):

		(self.encoded_circuit, self.regs) = self.define_encoded_circuit(faultyQC.num_qubits)

		self.parse_faulty_qc(faultyQC)



#==========================================================================================
#
#								Encoded Circuit Creation
#
#==========================================================================================

	def define_encoded_circuit(self, num_qubits: int) -> (QuantumCircuit, dict):
	# Generates an encoded QuantumCircuit and lists of registers for code implementation

		
		#list storing size-7 quantum registers, each holding 1 logical qubit
		log_qubits = list()

		#list of size 7 classical registers corresponding to logical qubits
		log_readouts = list()

		#list of size 3 quantum ancilla registers (used for parity checks)
		ancilla_qubits = list()

		#list of size 3 classical registers to read ancilla measurements
		ancilla_readouts = list()

		qc = QuantumCircuit()
		for qub in range(num_qubits):

			# add registers to quantum circuit
			log_qubits.append(QuantumRegister(size = 7, name = "Logical "+str(qub)))
			log_readouts.append(ClassicalRegister(size = 7, name = "Logical "+str(qub)+" readout"))
			ancilla_qubits.append(AncillaRegister(size = 3, name = "Log "+str(qub)+" ancillas"))
			ancilla_readouts.append(ClassicalRegister(size = 3, name = "Log "+str(qub)+" anc readout"))
			
			qc.add_register(log_qubits[qub])
			qc.add_register(log_readouts[qub])
			qc.add_register(ancilla_qubits[qub])
			qc.add_register(ancilla_readouts[qub])

			qc.append(encode_qubit(), log_qubits[qub])

		qc.barrier()

		regs = {
			'log_qubits': log_qubits,
			'log_readouts': log_readouts,
			'ancilla_qubits': ancilla_qubits,
			'ancilla_readouts': ancilla_readouts
		}

		return (qc, regs)



	def parse_faulty_qc(self, faultyQC: QuantumCircuit):

	# Used in constructor

		faultyQC = transpile(faultyQC, 
			basis_gates = ['id', 'x', 'y', 'z', 's', 'sdg', 'h', 'cx', 'cz'],
			optimization_level = 0)

			# TO DO: count non-clifford gates, add enough 
			# magic-state distillation ancillas to implement them
			# 
			# also figure out what "enough" means

		for instruction in faultyQC.data:
			# Loop over faulty circuit operations and implement the fault-tolerant
			# version of each operation
			(faultyOp, faultyQubits, faultyClbits) = instruction

			# List of qubits indices used in operation
			opQubits = [faultyQC.find_bit(faultyQubit).index for faultyQubit in faultyQubits]

			# List of classical bit indices used in operation
			opClbits = [faultyQC.find_bit(faultyClbit).index for faultyClbit in faultyClbits]

			# Check for measure op; can't be implemented as an instruction like the other gates
			if(faultyOp.name == 'measure'):

				# Final error check
				(self.encoded_circuit).append(parity_check(), (self.get_logical_qubit(opQubit)) +
					self.get_logical_ancilla(opQubit))

				(self.encoded_circuit).measure(self.get_logical_ancilla(opQubit),
					self.get_logical_ancilla_readout(opQubit))

				(self.encoded_circuit).append(reverse_encoding(), self.get_logical_qubit(opQubits[0]))
				(self.encoded_circuit).measure(self.get_logical_qubit(opQubits[0]), 
					self.regs['log_readouts'][opClbits[0] - faultyQC.num_qubits])
				continue

			# As long as op isn't measurement, get the equivalent fault-tolerant op realization
			steaneOp = get_steane_op(faultyOp.name)

			# List of qubits indices used in operation
			opQubits = [faultyQC.find_bit(faultyQubit).index for faultyQubit in faultyQubits]

			(self.encoded_circuit).append(steaneOp, self.get_logical_qubit(opQubits))

			for opQubit in opQubits:

				# Do decoding process
				correct_errors(self.encoded_circuit, self.get_logical_qubit(opQubit), 
					self.get_logical_ancilla(opQubit), 
					self.get_logical_ancilla_readout(opQubit))

#==========================================================================================
#
#							Get Methods for (Qu)Bit Groups
#
#==========================================================================================

	def get_logical_qubit(self, qubs: Union[int, list], registers = None) -> [Qubit]:

		logQubs = []
		if(self.regs is not None): registers = self.regs

		if(type(qubs) == int): return (self.encoded_circuit).qbit_argument_conversion(
			registers['log_qubits'][qubs])

		for q in qubs:
			for temp in (self.encoded_circuit).qbit_argument_conversion(registers['log_qubits'][q]):
				
				# Double for() loop is to convert from list(QuantumRegister) to list(Qubit)
				
				logQubs.append(temp)

		return logQubs



	def get_logical_ancilla(self, qubs: Union[int, list], registers = None) -> [Qubit]:

		logAncillas = []
		if(self.regs is not None): registers = self.regs

		if(type(qubs) == int): return (self.encoded_circuit).qbit_argument_conversion(
			registers['ancilla_qubits'][qubs])

		for q in qubs:
			for temp in (self.encoded_circuit).qbit_argument_conversion(registers['ancilla_qubits'][q]):
				
				# Double for() loop is to convert from list(QuantumRegister) to list(Qubit)
				
				logAncillas.append(temp)

		return logAncillas



	def get_logical_ancilla_readout(self, qubs: Union[int, list], registers = None):

		ancReadouts = []
		if(self.regs is not None): registers = self.regs

		if(type(qubs) == int): return registers['ancilla_readouts'][qubs]

		if(len(qubs) == 1): return registers['ancilla_readouts'][qubs[0]]

		for q in qubs:
			for temp in (self.encoded_circuit).cbit_argument_conversion(registers['ancilla_readouts'][q]):
				
				# Double for() loop is to convert from list(QuantumRegister) to list(Qubit)
				
				ancReadouts.append(temp)

		return ancReadouts

#==========================================================================================
#
#							Methods for Direct QC Manipulation
#
#==========================================================================================

	def draw(self):
		return (self.encoded_circuit).draw()



	def get_circuit(self):
		return self.encoded_circuit



#==========================================================================================
#
#								State Preparation Methods
#
#==========================================================================================

#===== 0 Basis =================== 1 Basis =================
#
# 0000000	0001111			1111111		1110000
# 0110011	0111100			1001100		1000011
# 1010101	1011010			0101010		0100101
# 1100110	1101001			0011001		0010110
# 
# even cx(even)					odd cx(even)
#===========================================================


def encode_qubit(q = None):
	# 
	# Returns a 7-qubit gate that transforms the 0000000 state to the 
	# logically encoded realization of the argument qubit

	# q is the base qubit, defaults to |0> state
	# function returns a 7-qubit gate which rotates a |0>^7 state to the logical q state

	encoded_qubit = QuantumCircuit(2, name='Encode qubit')
	if(q is None): q = Qubit()
	encoded_qubit.add_bits([q, Qubit(), Qubit(), Qubit(), Qubit()])

	encoded_qubit.cx([2, 2], [4, 5])
	encoded_qubit.h([0, 1, 3])
	encoded_qubit.cx([0, 0, 0], [2, 4, 6])
	encoded_qubit.cx([1, 1, 1], [2, 5, 6])
	encoded_qubit.cx([3, 3, 3], [4, 5, 6])

	return encoded_qubit.to_gate()



def reverse_encoding():

	# Used in define_encoded_circuit

	# Returns a gate that rotates an encoded logical qubit back to the standard 
	# basis {0000000, 1111111}


	rev = QuantumCircuit(7, name='Reverse encoding')

	# 0 basis [q0, q1, q1] = [q4, q5, q6], 1 basis [q0, q1, q2] = -1*[q4, q5, q6]
	# Removes any entanglement w q3
	rev.cx([3, 3, 3], [4, 5, 6])

	# 0 basis [q4, q5, q6] = 0, 1 basis [q4, q5, q6] = 1
	# Removes entanglement w q4, q5, q6
	rev.cx([0, 1, 2], [4, 5, 6])

	# 0 basis q3 = 0, 1 basis q3 = 1
	# Swaps q3 to appropriate phase then rotates back into computational basis
	rev.cz([0, 1, 2], [3, 3, 3])
	rev.h(3)

	# 0 basis [q0, q1, q2] = 0, 1 basis [q0, q1, q2] = 1
	# Detangles q2 = q0 XOR q1 into repetition code
	rev.h(2)
	rev.cz([1, 0], [2, 2])
	rev.h(range(3))
	rev.cx([2, 2], [0, 1])


	return rev.to_gate()


#==========================================================================================
#
#							Parity Check & Decoder Methods
#
#==========================================================================================


def correct_X(qc: QuantumCircuit, logQubit: list, ancQubits: list, 
	ancReadout: AncillaRegister):

	# Used in correct_errors

	# Adds the decoder operations to the passed QuantumCircuit on the passed 
	# registers to correct errors in the computational basis

	qc.barrier()
	qc.append(parity_check(), logQubit+ancQubits)
		
	qc.measure(ancQubits, ancReadout)

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



def correct_Z(qc: QuantumCircuit, logQubit: list, ancQubits: list, 
	ancReadout: AncillaRegister):

	# Used in correct_errors

	# Adds the decoder operations to the passed QuantumCircuit on the passed 
	# registers to correct errors in the Z basis 

	qc.barrier()
	qc.h(logQubit)
	correct_X(qc, logQubit, ancQubits, ancReadout)
	qc.h(logQubit)

	return qc



def correct_errors(qc: QuantumCircuit, logQubit: list, ancQubits: list, 
	ancReadout: AncillaRegister):

	# Add overall error correction step to passed QuantumCircuit on passed logical qubit
	# and respective registers

	correct_X(qc, logQubit, ancQubits, ancReadout)
	correct_Z(qc, logQubit, ancQubits, ancReadout)
	qc.reset(ancQubits)
	qc.barrier()

	return qc



def parity_check():

	# Used in correct_X

	# Returns a 10-qubit gate which performs the parity checking operation on the 
	# top 7 qubits, outputting to the lower 3 qubits

	par_check = QuantumCircuit(10, name = "parity_check")

	par_check.cx([0, 0], [8, 9])
	par_check.cx([1, 1], [7, 9])
	par_check.cx([2, 2], [7, 8])
	par_check.cx([3, 3, 3], [7, 8, 9])
	par_check.cx(4, 7)
	par_check.cx(5, 8)
	par_check.cx(6, 9)

	return par_check.to_gate()


#==========================================================================================
#
#							Logical Gate Realizations
#
#==========================================================================================

# All Steane code gates are transversal and return instruction sets for the gate
# realization

def get_steane_op(op: str):

	# Returns the function realizing the passed basis gate

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