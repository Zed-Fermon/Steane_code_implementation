# Steane_code_implementation

This is a Python library for creating and encoding Qiskit QuantumCircuits 
using the \[\[7, 1, 3\]\] Steane code and magic-state distillation, as described
in the following articles:

[Steane, Andrew (1996). "Multiple-Particle Interference and Quantum Error Correction". Proc. R. Soc. Lond. A. 452 (1954): 2551–2577.] ( https://arxiv.org/abs/quant-ph/9601029 )

[Bravyi, Sergey; Kitaev, Alexei (2005). "Universal quantum computation with ideal Clifford gates and noisy ancillas". Physical Review A. 71 (2): 022316.] ( https://arxiv.org/abs/quant-ph/0403025 )

[Knill, E. (2004). "Fault-Tolerant Postselected Quantum Computation: Schemes".] ( https://arxiv.org/abs/quant-ph/0402171 )

# Installation

Use pip to install package. Run the following command, you may need sudo/admin:

```
pip install -i https://test.pypi.org/simple/ Steane-code-implementation-Zed-Fermon==0.0.1
```

If you don't already have it installed, qiskit is also required:
```
pip install qiskit
```

# Usage

Import EncodedCircuit class with the following import line:
```
from circuit-encoder.EncodedCircuit import EncodedCircuit
```

Then create your QuantumCircuit as normal and pass it into an EncodedCircuit object (For example, this Bell state circuit):
```
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

qc.measure_all()

enc_circ_object = EncodedCircuit(qc)
```

Finally, call get_circuit() on the object to return the encoded realization of the passed circuit, and run it as you would a normal QuantumCircuit:

```
enc_qc = enc_circ_object.get_circuit()
```

# Roadmap

I want to build a new project that can work with Hamming codes more generally. I originally wanted to rebuild this project into that, but I think it will be more efficient to start from scratch with what I know now, so be on the lookout for a new project repo!


# Structure

