from qiskit import QuantumCircuit, Aer, transpile, QuantumRegister, ClassicalRegister, AncillaRegister
from qiskit_aer import AerSimulator

import random

from steane_state_prep import encode_qubit, reverse_encoding
from steane_gates import steane_x, steane_z, steane_h, steane_cx, steane_cz
from steane_parity_checks import correct_X, correct_Z, correct_errors
from basic_noise_model import apply_random_error



#list of basis vectors; first row*1/sqrt(8) is |0> basis, second row is |1> basis
basis_vecs = [
'0000000', '0110011', '1010101', '1100110', '0001111', '0111100', '1011010', '1101001',
'1111111', '1001100', '0101010', '0011001', '1110000', '1000011', '0100101', '0010110']


def main():
	for i in range(7):

		(qc, regs) = define_encoded_circuit(num_qubits = 1)


		#apply_random_error(qc)
		qc.append(steane_h(), log_qubit(0))
		qc.h(i)

		correct_errors(qc, log_qubit(0), anc_qubits(0), regs['ancilla_readouts'][0])
		
		measure_log_qubits(qc, regs)

		run_circuit(qc)

	qc.clear()




def run_circuit(qc: QuantumCircuit):

	#print(qc.draw())

	# Use Aer's qasm_simulator
	backend_sim = Aer.get_backend('aer_simulator')

	# Execute the circuit on the aer simulator.
	
	# How many times to run the circuit
	num_shots = 1024
	job_sim = backend_sim.run(transpile(qc, backend_sim), shots = num_shots)

	# Grab the results from the job.
	result_sim = job_sim.result()

	counts = result_sim.get_counts(qc)
	print("Vector  Anc ", " Count ", "Percent")

	for bVec in basis_vecs:
		if(bVec in str(counts.keys())):
			#print(bVec+": ", str(counts[bVec])+"  ", counts[bVec]/num_shots)
			#counts.pop(bVec)
			continue

	for x in counts.keys():
		print(str(x[::-1])+": ", str(counts[x])+"  ", counts[x]/num_shots)


def log_qubit(*qubs: int):
	# Returns a list representing the q'th logical qubit
	temp = list()
	for q in qubs:
		temp = temp+list(range(q*10, (q*10)+7))
	return temp


def anc_qubits(*qubs: int):
	# Returns a list representing the ancilla qubits of the q'th logical qubit
	temp = list()
	for q in qubs:
		temp = temp+list(range((q*10)+7, (q+1)*10))
	return temp



def define_encoded_circuit(num_qubits: int):
	# Generates an encoded QuantumCircuit and lists of registers for code implementation
	
	#list storing size-7 quantum registers, each holding 1 logical qubit
	log_qubits = list()

	#list of classical registers corresponding to logical qubits
	log_readouts = list()

	#list of quantum ancilla registers (used for parity checks)
	ancilla_qubits = list()

	#list of classical registers to read ancilla measurements
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

		qc.append(encode_qubit(), log_qubit(qub))

	qc.barrier()

	regs = {
		'log_qubits': log_qubits,
		'log_readouts': log_readouts,
		'ancilla_qubits': ancilla_qubits,
		'ancilla_readouts': ancilla_readouts
	}

	return (qc, regs)


def measure_log_qubits(qc: QuantumCircuit, regs: list):

	for (i, log_qubit) in enumerate(regs['log_qubits']):
		qc.append(reverse_encoding(), log_qubit)
		qc.measure(log_qubit, regs['log_readouts'][i])

	return qc



if __name__ == '__main__':
	main()