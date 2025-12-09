from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

n = 10
s = '1010'

qc = QuantumCircuit(n+1, n)

# last qubit is output qubit, initiate it to /1>
qc.x(n)
qc.h(n)

# put input qubit in superposition
for i in range(n):
    qc.h(i)

# Oracle for f(x) = s.x mod 2
for i, bit in enumerate(s):
    if bit == '1':
        qc.cx(i, n)

# Hadamard again on input qubit
for i in range(n):
    qc.h(i)

# Measure input qubit (they will contain s)
for i in range(n):
    qc.measure(i, i)

print(qc.draw())

backend = Aer.get_backend('qasm_simulator')
transpiled_qc = transpile(qc, backend)
job = backend.run(transpiled_qc, shots = 1)
results = job.result()
counts = results.get_counts()

print(counts)