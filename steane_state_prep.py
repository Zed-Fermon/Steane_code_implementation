from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Qubit


def main():
	encoded_qubit = QuantumCircuit(7, name='encode_logical_qubit')
	#encoded_qubit.barrier()

	# [0, 1, 3] stay in h
	encoded_qubit.h(range(7))

	# q2 = q0 XOR q1
	encoded_qubit.cz([0, 1], [2, 2])
	encoded_qubit.h(2)

	# if q3=1, NOT [q4, q5, q6]
	encoded_qubit.cz([3, 3, 3], [4, 5, 6])
	encoded_qubit.h([4, 5, 6])

	# [q4, q5, q6] = +-[q0, q1, q2]
	encoded_qubit.cx([0, 1, 2], [4, 5, 6])

	rev = QuantumCircuit(7, name='reverse_logical_encoding')

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

	print("Qubit encoding circuit: \n")
	print(encoded_qubit.draw())
	print()
	print("Qubit un-encoding circuit: \n")
	print(rev.draw())





def encode_qubit(q = None):

	# q is the base qubit, defaults to |0> state
	# function returns a 7-qubit gate which rotates a |0>^7 state to the logical q state

	encoded_qubit = QuantumCircuit(2, name='encode_logical_qubit')
	if(q is None): q = Qubit()
	encoded_qubit.add_bits([q, Qubit(), Qubit(), Qubit(), Qubit()])

	encoded_qubit.cx([2, 2], [4, 5])
	encoded_qubit.h([0, 1, 3])
	encoded_qubit.cx([0, 0, 0], [2, 4, 6])
	encoded_qubit.cx([1, 1, 1], [2, 5, 6])
	encoded_qubit.cx([3, 3, 3], [4, 5, 6])

	return encoded_qubit.to_gate()



def reverse_encoding():

#===== 0 Basis =================== 1 Basis =================
#
# 0000000	0001111			1111111		1110000
# 0110011	0111100			1001100		1000011
# 1010101	1011010			0101010		0100101
# 1100110	1101001			0011001		0010110
# 
# even cx(even)					odd cx(even)
#===========================================================

	rev = QuantumCircuit(7, name='reverse_logical_encoding')

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


if __name__ == '__main__':
	main()