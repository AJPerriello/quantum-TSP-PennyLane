import numpy as standard_np
import pennylane as qml
from pennylane import numpy as np

def test_environment():
    # Initialize a 2-qubit simulator device
    dev = qml.device("default.qubit", wires=2)

    # Define a simple variational circuit
    @qml.qnode(dev)
    def circuit(params):
        qml.Hadamard(wires=0)
        qml.RX(params[0], wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.PauliZ(1))

    # Initialize a differentiable NumPy array using PennyLane's wrapped NumPy
    params = np.array([0.543], requires_grad=True)
    result = circuit(params)

    print("=== Environment Verification ===")
    print(f"PennyLane Version : {qml.__version__}")
    print(f"NumPy Version     : {standard_np.__version__}")
    print(f"Circuit Output    : {result:.4f}")
    print("================================")
    print("Environment check passed successfully!")

if __name__ == "__main__":
    test_environment()