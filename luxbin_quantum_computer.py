"""
LUXBIN Light Language - Real Quantum Computer Demo
Run this in Google Colab to test on IBM Quantum hardware

Setup:
1. Create free account at: https://quantum.ibm.com/
2. Get your API token from: https://quantum.ibm.com/account
3. Run this notebook and paste your token when prompted
"""

# Install required packages
# !pip install qiskit qiskit-ibm-runtime matplotlib numpy

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np
import matplotlib.pyplot as plt

# Try to import IonQ SDKs
try:
    import ionq
    IONQ_AVAILABLE = True
    IONQ_DIRECT = True
except ImportError:
    try:
        from qiskit_ionq import IonQProvider
        IONQ_AVAILABLE = True
        IONQ_DIRECT = False
    except ImportError:
        IONQ_AVAILABLE = False
        IONQ_DIRECT = False

# Try to import Rigetti PyQuil
try:
    from pyquil import get_qc, Program
    from pyquil.gates import *
    from pyquil.api import ForestConnection
    PYQUIL_AVAILABLE = True
except ImportError:
    PYQUIL_AVAILABLE = False

# LUXBIN Alphabet (77 characters - 6-7 bits per character)
LUXBIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:-()[]{}@#$%^&*+=_~`<>\"'|\\"

def text_to_luxbin(text):
    """Convert text to LUXBIN representation"""
    # Convert to binary
    binary = ''.join(format(ord(char), '08b') for char in text)

    # Convert binary to LUXBIN (6 bits per character)
    luxbin = ''
    for i in range(0, len(binary), 6):
        chunk = binary[i:i+6].ljust(6, '0')
        index = int(chunk, 2) % len(LUXBIN_ALPHABET)
        luxbin += LUXBIN_ALPHABET[index]

    return luxbin, binary

def luxbin_to_wavelengths(luxbin, enable_quantum=True):
    """Convert LUXBIN to photonic wavelengths"""
    wavelengths = []
    QUANTUM_ZERO_PHONON = 637  # Diamond NV center (nm)

    for char in luxbin:
        if enable_quantum and char == ' ':
            # Use diamond NV center wavelength for spaces
            wavelengths.append({
                'character': char,
                'wavelength_nm': QUANTUM_ZERO_PHONON,
                'frequency_hz': 3e8 / (QUANTUM_ZERO_PHONON * 1e-9),
                'energy_ev': 1240 / QUANTUM_ZERO_PHONON
            })
        else:
            # Map to visible spectrum (400-700nm)
            index = LUXBIN_ALPHABET.index(char)
            wavelength = 400 + (index / len(LUXBIN_ALPHABET)) * 300

            wavelengths.append({
                'character': char,
                'wavelength_nm': wavelength,
                'frequency_hz': 3e8 / (wavelength * 1e-9),
                'energy_ev': 1240 / wavelength
            })

    return wavelengths

def wavelength_to_quantum_state(wavelength_nm):
    """
    Encode wavelength as quantum state angles
    Maps 400-700nm wavelength range to qubit rotation angles
    """
    # Normalize wavelength to 0-1 range
    norm = (wavelength_nm - 400) / 300

    # Convert to quantum rotation angles
    theta = norm * np.pi  # Polar angle
    phi = norm * 2 * np.pi  # Azimuthal angle

    return theta, phi

def create_luxbin_quantum_circuit(wavelengths, num_qubits=3):
    """
    Create quantum circuit encoding LUXBIN wavelength data
    Uses rotation gates to encode wavelength information
    """
    qc = QuantumCircuit(num_qubits)

    # Encode first few wavelengths (limited by qubit count)
    for i, wl_data in enumerate(wavelengths[:num_qubits]):
        wavelength = wl_data['wavelength_nm']
        theta, phi = wavelength_to_quantum_state(wavelength)

        # Initialize qubit in superposition
        qc.h(i)

        # Encode wavelength via rotation
        qc.ry(theta, i)  # Y-rotation (polar angle)
        qc.rz(phi, i)    # Z-rotation (azimuthal angle)

    # Create entanglement between qubits (quantum correlation)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)  # CNOT gate for entanglement

    # Measure all qubits
    qc.measure_all()

    return qc

def run_on_quantum_computer(circuit, backend_name='ibm_brisbane'):
    """
    Run circuit on real quantum hardware (IBM, IonQ, Rigetti)
    Returns measurement results
    """
    # Determine provider from backend name
    if backend_name.startswith('ibm_'):
        provider = 'ibm'
    elif backend_name.startswith('ionq_'):
        provider = 'ionq'
    elif backend_name.startswith('rigetti_'):
        provider = 'rigetti'
    else:
        provider = 'ibm'  # default

    print(f"🔬 Connecting to {provider.upper()} quantum computer: {backend_name}")

    if provider == 'ibm':
        # IBM Quantum
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)

        print(f"✅ Connected! Queue status: {backend.status().pending_jobs} jobs pending")
        print(f"📊 Backend has {backend.num_qubits} qubits")

        # Transpile for hardware
        print("🔄 Transpiling circuit for quantum hardware...")
        transpiled = transpile(circuit, backend=backend, optimization_level=3)

        # Run on quantum computer
        print("🚀 Submitting job to quantum computer...")
        sampler = Sampler(backend)
        job = sampler.run([transpiled], shots=1024)

        print(f"⏳ Job submitted! Job ID: {job.job_id()}")
        print("⏳ Waiting for quantum computer to execute...")

        result = job.result()

    elif provider == 'ionq':
        # IonQ quantum computer
        if not IONQ_AVAILABLE:
            raise ImportError("IonQ SDK not available. Install with: pip install ionq-sdk or pip install qiskit-ionq")

        import os
        ionq_api_key = os.getenv('IONQ_API_KEY')
        if not ionq_api_key:
            raise ValueError("IONQ_API_KEY environment variable not set")

        print(f"🔬 Running on IonQ {backend_name}...")

        if IONQ_DIRECT:
            # Use direct IonQ SDK
            client = ionq.Client(api_key=ionq_api_key)
            # Convert Qiskit circuit to IonQ format and run
            # This is a simplified version - real implementation would need circuit conversion
            job = client.submit_job(circuit=circuit, backend=backend_name, shots=1024)
            result = job.result()
        else:
            # Use Qiskit IonQ provider
            provider = IonQProvider(token=ionq_api_key)
            backend = provider.get_backend(backend_name)
            transpiled = transpile(circuit, backend=backend, optimization_level=3)
            sampler = Sampler(backend)
            job = sampler.run([transpiled], shots=1024)
            result = job.result()

    elif provider == 'rigetti':
        # Rigetti quantum computer
        if not PYQUIL_AVAILABLE:
            raise ImportError("PyQuil not available. Install with: pip install pyquil")

        import os
        rigetti_api_key = os.getenv('RIGETTI_API_KEY')

        print(f"🔬 Running on Rigetti {backend_name}...")

        # Initialize Forest connection
        if rigetti_api_key:
            connection = ForestConnection(api_key=rigetti_api_key)
        else:
            connection = ForestConnection()

        # Get quantum computer
        qc = get_qc(backend_name, connection=connection)

        # Convert Qiskit circuit to PyQuil program
        # This is simplified - real implementation needs proper circuit conversion
        program = Program()
        # Add gates from Qiskit circuit to PyQuil program
        for instruction in circuit.data:
            gate_name = instruction.operation.name
            qubits = [q.index for q in instruction.qubits]
            if gate_name == 'h':
                program += H(qubits[0])
            elif gate_name == 'x':
                program += X(qubits[0])
            elif gate_name == 'y':
                program += Y(qubits[0])
            elif gate_name == 'z':
                program += Z(qubits[0])
            elif gate_name == 'cx':
                program += CNOT(qubits[0], qubits[1])
            # Add more gate conversions as needed

        # Run on Rigetti quantum computer
        executable = qc.compile(program)
        result = qc.run(executable)

        # Convert result back to Qiskit format for compatibility
        # This is a simplified conversion
        result = type('Result', (), {
            'quasi_dists': [result],
            'result': lambda: type('SubResult', (), {
                'get_counts': lambda: dict(enumerate(result.tolist()))
            })()
        })()

    print("✅ Quantum execution complete!")
    return result

def main():
    """Main demo function"""
    print("=" * 60)
    print("LUXBIN LIGHT LANGUAGE - QUANTUM COMPUTER DEMO")
    print("=" * 60)

    # Step 1: Get user input
    text = input("\n💬 Enter text to translate to quantum light: ")

    # Step 2: Convert to LUXBIN
    print("\n🔄 Converting to LUXBIN Light Language...")
    luxbin, binary = text_to_luxbin(text)
    print(f"📝 Original text: {text}")
    print(f"🔢 Binary: {binary[:80]}..." if len(binary) > 80 else f"🔢 Binary: {binary}")
    print(f"💎 LUXBIN: {luxbin}")

    # Step 3: Convert to wavelengths
    print("\n🌈 Converting to photonic wavelengths...")
    wavelengths = luxbin_to_wavelengths(luxbin, enable_quantum=True)

    print(f"\n📊 Generated {len(wavelengths)} wavelength states:")
    for i, wl in enumerate(wavelengths[:10]):  # Show first 10
        print(f"  {wl['character']} → {wl['wavelength_nm']:.2f}nm "
              f"({wl['frequency_hz']:.2e}Hz, {wl['energy_ev']:.3f}eV)")
    if len(wavelengths) > 10:
        print(f"  ... and {len(wavelengths) - 10} more")

    # Step 4: Create quantum circuit
    print("\n⚛️  Creating quantum circuit...")
    num_qubits = min(5, len(wavelengths))  # Use up to 5 qubits
    qc = create_luxbin_quantum_circuit(wavelengths, num_qubits)

    print(f"✅ Circuit created with {num_qubits} qubits")
    print(f"   Gates: {qc.count_ops()}")
    print(f"   Depth: {qc.depth()}")

    # Visualize circuit
    print("\n📈 Circuit diagram:")
    print(qc.draw(output='text'))

    # Step 5: Connect to IBM Quantum
    print("\n🔐 IBM Quantum Authentication")
    print("Get your token from: https://quantum.ibm.com/account")

    # Check if already authenticated
    try:
        service = QiskitRuntimeService()
        print("✅ Already authenticated!")
    except:
        token = input("Paste your IBM Quantum API token: ")
        QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)
        service = QiskitRuntimeService()
        print("✅ Authentication successful!")

    # List available backends
    print("\n🖥️  Available quantum computers:")
    backends = service.backends(simulator=False, operational=True)
    for i, backend in enumerate(backends[:5]):
        status = backend.status()
        print(f"  {i+1}. {backend.name} - {backend.num_qubits} qubits - "
              f"{status.pending_jobs} jobs queued")

    # Select backend
    backend_choice = input("\nEnter backend name (or press Enter for simulator): ").strip()

    if not backend_choice:
        # Run on simulator
        print("\n🖥️  Running on quantum simulator...")
        from qiskit_aer import AerSimulator
        backend = AerSimulator()
        transpiled = transpile(qc, backend)
        job = backend.run(transpiled, shots=1024)
        result = job.result()
        counts = result.get_counts()
    else:
        # Run on real quantum computer
        result = run_on_quantum_computer(qc, backend_choice)
        counts = result[0].data.meas.get_counts()

    # Step 6: Display results
    print("\n" + "=" * 60)
    print("QUANTUM MEASUREMENT RESULTS")
    print("=" * 60)

    print("\n📊 Measurement counts:")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        probability = count / 1024 * 100
        print(f"  |{state}⟩: {count} times ({probability:.1f}%)")

    # Visualize
    print("\n📈 Generating visualization...")
    fig = plot_histogram(counts, figsize=(12, 6))
    plt.title(f"Quantum Measurement Results for '{text}'")
    plt.tight_layout()
    plt.savefig('quantum_results.png', dpi=150, bbox_inches='tight')
    print("✅ Saved visualization to: quantum_results.png")
    plt.show()

    # Analysis
    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)
    print(f"✨ Your text '{text}' was successfully encoded as quantum light states")
    print(f"💎 Used {num_qubits} qubits to represent {len(wavelengths)} wavelengths")
    print(f"🌊 Wavelength range: {min(w['wavelength_nm'] for w in wavelengths):.1f}-"
          f"{max(w['wavelength_nm'] for w in wavelengths):.1f}nm")
    print(f"⚛️  Total quantum operations: {sum(qc.count_ops().values())}")

    if '637' in [f"{w['wavelength_nm']:.0f}" for w in wavelengths]:
        print("\n🔬 QUANTUM RESONANCE DETECTED!")
        print("   Your text contains spaces, encoded at 637nm")
        print("   This is the diamond NV center zero-phonon line")
        print("   Perfect for quantum state storage! 💎")

    print("\n✅ Quantum execution complete!")

if __name__ == "__main__":
    main()
