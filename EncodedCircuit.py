from typing import Union

from qiskit import (QuantumCircuit, QuantumRegister, AncillaRegister, ClassicalRegister,
	transpile)
from qiskit.circuit import Qubit
from steane_gates import get_steane_op
from steane_state_prep import encode_qubit, reverse_encoding
from steane_parity_checks import correct_errors, parity_check

class EncodedCircuit(QuantumCircuit):

#==========================================================================================
#
#								Constructor
#
#==========================================================================================
	
	def __init__(self, faultyQC: QuantumCircuit):

		(self.qc, self.regs) = self.define_encoded_circuit(faultyQC.num_qubits)

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
				(self.qc).append(parity_check(), (self.get_logical_qubit(opQubit)) +
					self.get_logical_ancilla(opQubit))

				(self.qc).measure(self.get_logical_ancilla(opQubit),
					self.get_logical_ancilla_readout(opQubit))

				(self.qc).append(reverse_encoding(), self.get_logical_qubit(opQubits[0]))
				(self.qc).measure(self.get_logical_qubit(opQubits[0]), 
					self.regs['log_readouts'][opClbits[0] - faultyQC.num_qubits])
				continue

			# As long as op isn't measurement, get the equivalent fault-tolerant op realization
			steaneOp = get_steane_op(faultyOp.name)

			# List of qubits indices used in operation
			opQubits = [faultyQC.find_bit(faultyQubit).index for faultyQubit in faultyQubits]

			(self.qc).append(steaneOp, self.get_logical_qubit(opQubits))

			for opQubit in opQubits:

				# Do decoding process
				correct_errors(self.qc, self.get_logical_qubit(opQubit), 
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

		if(type(qubs) == int): return (self.qc).qbit_argument_conversion(
			registers['log_qubits'][qubs])

		for q in qubs:
			for temp in (self.qc).qbit_argument_conversion(registers['log_qubits'][q]):
				
				# Double for() loop is to convert from list(QuantumRegister) to list(Qubit)
				
				logQubs.append(temp)

		return logQubs



	def get_logical_ancilla(self, qubs: Union[int, list], registers = None) -> [Qubit]:

		logAncillas = []
		if(self.regs is not None): registers = self.regs

		if(type(qubs) == int): return (self.qc).qbit_argument_conversion(
			registers['ancilla_qubits'][qubs])

		for q in qubs:
			for temp in (self.qc).qbit_argument_conversion(registers['ancilla_qubits'][q]):
				
				# Double for() loop is to convert from list(QuantumRegister) to list(Qubit)
				
				logAncillas.append(temp)

		return logAncillas



	def get_logical_ancilla_readout(self, qubs: Union[int, list], registers = None):

		ancReadouts = []
		if(self.regs is not None): registers = self.regs

		if(type(qubs) == int): return registers['ancilla_readouts'][qubs]

		if(len(qubs) == 1): return registers['ancilla_readouts'][qubs[0]]

		for q in qubs:
			for temp in (self.qc).cbit_argument_conversion(registers['ancilla_readouts'][q]):
				
				# Double for() loop is to convert from list(QuantumRegister) to list(Qubit)
				
				ancReadouts.append(temp)

		return ancReadouts

#==========================================================================================
#
#							Methods for Direct QC Manipulation
#
#==========================================================================================

	def draw(self):
		return (self.qc).draw()



	def get_circuit(self):
		return self.qc