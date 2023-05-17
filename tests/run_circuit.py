from qiskit import QuantumCircuit, Aer, transpile, QuantumRegister, ClassicalRegister, AncillaRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel

import random
import re

from basic_noise_model import apply_random_error, get_noise_model

from circuit_encoder.EncodedCircuit import EncodedCircuit


def main():

	nm = get_noise_model(.001, .0001)

	num_qb = 2

	qc = QuantumCircuit(num_qb, num_qb)
	qc.h(0)
	qc.cx(0, 1)
	qc.z(0)

	#for tmp in range(100):
	#	qc.z(0)
	#	qc.x(1)
	qc.measure(range(num_qb), range(num_qb))

	faulty_counts = run_circuit(qc, nm)
	print_counts(faulty_counts)


	enc_qc = EncodedCircuit(qc)
	enc_counts = run_circuit(enc_qc.get_circuit(), nm)
	print_encoded_counts(enc_counts, num_qb)



def run_circuit(qc: QuantumCircuit, nm: NoiseModel = None):

	#print(qc.draw())

	if(nm is None): nm = get_noise_model(0, 0)

	# Use Aer's built-in simulator
	backend_sim = AerSimulator(noise_model = nm)

	# Execute the circuit on the aer simulator.
	
	# How many times to run the circuit
	num_shots = 1024
	job_sim = backend_sim.run(transpile(qc, backend_sim), shots = num_shots)

	# Grab the results from the job.
	result_sim = job_sim.result()

	counts = result_sim.get_counts(qc)

	return counts



def print_encoded_counts(counts, num_qubits):

	num_shots = counts.shots()
	num_successful = 0

	success_check = re.compile('(0{3} (0{7}|1{7}) *){'+f'{num_qubits}'+'}')
	success_items = list()

	for bitStr in counts.keys():
		# Check if bitstring is in codespace
		bS_check = re.fullmatch(success_check, bitStr)

		# Get all results without errors
		if(bS_check is not None):
			# Count successfull runs to determine circuit success rate
			num_successful += counts.get(bitStr)

			# Clean bitstring by removing ancillas and collapsing logical qubits
			clean_bitStr = bitStr.replace('0000000', '0')
			clean_bitStr = clean_bitStr.replace('1111111', '1')
			clean_bitStr = clean_bitStr.replace('000', '')
			clean_bitStr = clean_bitStr.replace(' ', '')
			clean_bitStr = clean_bitStr[::-1]


			success_items.append((bitStr, counts.get(bitStr), clean_bitStr))

	get_item_count = lambda item: item[1]
	success_items.sort(key = get_item_count, )
	perc_succ = num_successful / num_shots
	print("Percent successful runs:", perc_succ)
	print()

	for succ_item in success_items:
		print(succ_item[2]+": "+str(succ_item[1]))


	

	

def print_counts(counts):

	num_shots = counts.shots()

	for _ in range(len(counts.keys())):
		# Get the most frequent results (which should be all 0 or all 1) and prints 
		# them first
		# Ties result in an error, and they always happen for low counts, so if an 
		# error occurs I just use the key iterable as the default value
		try:
			mostFreq = counts.most_frequent()
		except:
			continue
		freq = counts.pop(mostFreq)
		perc = freq/num_shots

		print(mostFreq[::-1]+": ", str(freq)+"  ", perc)
	print()



if __name__ == '__main__':
	main()