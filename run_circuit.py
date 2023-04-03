from qiskit import QuantumCircuit, Aer, transpile, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

from steane_state_prep import encode_qubit, reverse_encoding
from steane_gates import steane_x, steane_z, steane_h, steane_cx



num_qubits = 3
qc = QuantumCircuit()

#list storing size-7 quantum registers, each holding 1 logical qubit
log_qubits = list()

#list of classical registers corresponding to logical qubits
log_readouts = list()

def main():

	for qub in range(num_qubits):

		# add registers to quantum circuit
		log_qubits.append(QuantumRegister(size = 7, name = "Logical "+str(qub)))
		log_readouts.append(ClassicalRegister(size = 7, name = "Logical "+str(qub)+" readout"))
		qc.add_register(log_qubits[qub])
		qc.add_register(log_readouts[qub])

		# add encoding step (maps from repetition basis to Steane code basis)
		qc.append(encode_qubit(), log_qubit(qub))


	qc.barrier()

	qc.append(steane_h(), log_qubit(0))
	qc.append(steane_cx(), [log_qubit(0), log_qubit(1)])

	qc.barrier()

	for i in range(num_qubits):
		qc.append(reverse_encoding(), log_qubit(i))
		qc.measure(log_qubits[i], log_readouts[i])

	run_circuit(qc)




def run_circuit(qc: QuantumCircuit):

	print(qc.draw())

	# Use Aer's qasm_simulator
	backend_sim = Aer.get_backend('qasm_simulator')

	# Execute the circuit on the qasm simulator.
	# We've set the number of repeats of the circuit
	# to be 1024, which is the default.
	job_sim = backend_sim.run(transpile(qc, backend_sim), shots=1024)

	# Grab the results from the job.
	result_sim = job_sim.result()

	counts = result_sim.get_counts(qc)
	print([x[::-1] for x in counts.keys()])


def log_qubit(q):
	# Returns the QuantumRegister representing the q'th logical qubit

	return log_qubits[q]




if __name__ == '__main__':
	main()