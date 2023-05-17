from qiskit.visualization import circuit_drawer

from EncodedCircuit import EncodedCircuit
from steane_state_prep import encode_qubit, reverse_encoding
from steane_parity_checks import parity_check


from qiskit import QuantumCircuit, QuantumRegister, AncillaRegister
import matplotlib.pyplot as plt
import matplotlib as mpl


def draw_circuit(qc):
	circuit_drawer(qc, output = 'mpl', fold = -1, cregbundle = True, interactive = True)

bell_circuit = QuantumCircuit(2, 2)
bell_circuit.h(0)
bell_circuit.cx(0, 1)

enc_bell_circuit = EncodedCircuit(bell_circuit).get_circuit()

log_qub_reg = QuantumRegister(7, name = 'Logical Qubit')

state_prep_circ = QuantumCircuit(log_qub_reg)
state_prep_circ.append(encode_qubit(), range(7))
state_prep_circ = state_prep_circ.decompose()

state_decomp_circ = QuantumCircuit(log_qub_reg)
state_decomp_circ.append(reverse_encoding(), range(7))
state_decomp_circ = state_decomp_circ.decompose()

parity_check_circ = QuantumCircuit(log_qub_reg, AncillaRegister(3, name = 'Ancilla Register'))
parity_check_circ.append(parity_check(), range(10))
parity_check_circ = parity_check_circ.decompose()

#draw_circuit(state_prep_circ)
#draw_circuit(state_decomp_circ)
#draw_circuit(parity_check_circ)
draw_circuit(enc_bell_circuit)

plt.show()