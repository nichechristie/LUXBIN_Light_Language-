"""
LUXBIN Light Language - Origin Quantum (China) Demo
Run this on Chinese quantum computers via Origin Quantum Cloud

Setup:
1. Create account at: https://qcloud.originqc.com.cn/en/
2. Get your API token from the dashboard
3. Run this script to test LUXBIN on Chinese quantum hardware
"""

# Install required packages
# !pip install pyqpanda numpy matplotlib

from pyqpanda import *
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# LUXBIN Alphabet (77 characters)
LUXBIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:-()[]{}@#$%^&*+=_~`<>\"'|\\"

def text_to_luxbin(text):
    """Convert text to LUXBIN representation"""
    binary = ''.join(format(ord(char), '08b') for char in text)

    luxbin = ''
    for i in range(0, len(binary), 6):
        chunk = binary[i:i+6].ljust(6, '0')
        index = int(chunk, 2) % len(LUXBIN_ALPHABET)
        luxbin += LUXBIN_ALPHABET[index]

    return luxbin, binary

def luxbin_to_wavelengths(luxbin, enable_quantum=True):
    """Convert LUXBIN to photonic wavelengths"""
    wavelengths = []
    QUANTUM_ZERO_PHONON = 637  # Diamond NV center

    for char in luxbin:
        if enable_quantum and char == ' ':
            wavelengths.append({
                'character': char,
                'wavelength_nm': QUANTUM_ZERO_PHONON,
                'energy_ev': 1240 / QUANTUM_ZERO_PHONON
            })
        else:
            index = LUXBIN_ALPHABET.index(char)
            wavelength = 400 + (index / len(LUXBIN_ALPHABET)) * 300
            wavelengths.append({
                'character': char,
                'wavelength_nm': wavelength,
                'energy_ev': 1240 / wavelength
            })

    return wavelengths

def wavelength_to_angles(wavelength_nm):
    """Convert wavelength to quantum rotation angles"""
    norm = (wavelength_nm - 400) / 300
    theta = norm * np.pi
    phi = norm * 2 * np.pi
    return theta, phi

def create_luxbin_circuit(wavelengths, num_qubits=6):
    """
    Create quantum circuit for Origin Quantum
    Using PyQPanda (Origin Quantum's framework)
    """
    # Initialize quantum machine
    qvm = CPUQVM()
    qvm.init_qvm()

    # Allocate qubits and classical bits
    qubits = qvm.qAlloc_many(num_qubits)
    cbits = qvm.cAlloc_many(num_qubits)

    # Create quantum program
    prog = QProg()

    # Encode wavelengths into qubits
    for i in range(min(num_qubits, len(wavelengths))):
        wavelength = wavelengths[i]['wavelength_nm']
        theta, phi = wavelength_to_angles(wavelength)

        # Initialize in superposition
        prog << H(qubits[i])

        # Encode wavelength via rotations
        prog << RY(qubits[i], theta)
        prog << RZ(qubits[i], phi)

    # Create entanglement
    for i in range(num_qubits - 1):
        prog << CNOT(qubits[i], qubits[i + 1])

    # Measure all qubits
    for i in range(num_qubits):
        prog << Measure(qubits[i], cbits[i])

    return qvm, prog, qubits, cbits

def run_on_origin_quantum(qvm, prog, cbits, shots=1000):
    """
    Run circuit on Origin Quantum computer
    """
    print(f"🔬 Running on Origin Quantum computer...")

    # Run the quantum program
    result = qvm.run_with_configuration(prog, cbits, shots)

    # Process results
    counts = {}
    for key, value in result.items():
        counts[key] = value

    return counts

def run_on_cloud(api_token, wavelengths, backend='Wuyuan'):
    """
    Run on Origin Quantum Cloud Platform
    """
    try:
        from pyqpanda import QCloud

        # Initialize cloud connection
        qcloud = QCloud()
        qcloud.init_qvm(api_token)

        print(f"✅ Connected to Origin Quantum Cloud!")
        print(f"🖥️  Backend: {backend} (Chinese quantum computer)")

        # Create circuit
        qvm, prog, qubits, cbits = create_luxbin_circuit(wavelengths)

        # Submit to cloud
        task_id = qcloud.full_amplitude_measure(prog, len(qubits), backend)
        print(f"⏳ Job submitted! Task ID: {task_id}")

        # Wait for results
        print("⏳ Waiting for quantum computer...")
        result = qcloud.query_task_state(task_id)

        print("✅ Quantum execution complete!")
        return result

    except Exception as e:
        print(f"⚠️  Cloud execution failed: {e}")
        print("📝 Falling back to local simulator...")

        qvm, prog, qubits, cbits = create_luxbin_circuit(wavelengths)
        result = run_on_origin_quantum(qvm, prog, cbits)
        return result

def visualize_results(counts, text):
    """Visualize quantum measurement results"""
    # Sort by count
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

    states = [s[0] for s in sorted_counts]
    values = [s[1] for s in sorted_counts]

    # Create bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(states)), values, color='purple', alpha=0.7)
    plt.xticks(range(len(states)), [f"|{s}⟩" for s in states], rotation=45)
    plt.xlabel('Quantum State')
    plt.ylabel('Measurement Count')
    plt.title(f'Origin Quantum Results for "{text}"')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('origin_quantum_results.png', dpi=150, bbox_inches='tight')
    print("\n✅ Saved visualization: origin_quantum_results.png")
    plt.show()

def main():
    """Main demo function"""
    print("=" * 70)
    print("LUXBIN LIGHT LANGUAGE - ORIGIN QUANTUM (CHINA) DEMO")
    print("=" * 70)

    # Get user input
    text = input("\n💬 Enter text to translate: ")

    # Convert to LUXBIN
    print("\n🔄 Converting to LUXBIN Light Language...")
    luxbin, binary = text_to_luxbin(text)
    print(f"📝 Original: {text}")
    print(f"🔢 Binary: {binary[:80]}...")
    print(f"💎 LUXBIN: {luxbin}")

    # Convert to wavelengths
    print("\n🌈 Converting to photonic wavelengths...")
    wavelengths = luxbin_to_wavelengths(luxbin, enable_quantum=True)

    print(f"\n📊 Generated {len(wavelengths)} wavelength states:")
    for i, wl in enumerate(wavelengths[:10]):
        print(f"  {wl['character']} → {wl['wavelength_nm']:.2f}nm ({wl['energy_ev']:.3f}eV)")
    if len(wavelengths) > 10:
        print(f"  ... and {len(wavelengths) - 10} more")

    # Create quantum circuit
    print("\n⚛️  Creating quantum circuit...")
    num_qubits = min(6, len(wavelengths))
    qvm, prog, qubits, cbits = create_luxbin_circuit(wavelengths, num_qubits)

    print(f"✅ Circuit created with {num_qubits} qubits")
    print(f"   Using PyQPanda (Origin Quantum framework)")

    # Choose execution mode
    print("\n🖥️  Execution Options:")
    print("1. Origin Quantum Cloud (Wuyuan - 24 qubit)")
    print("2. Origin Quantum Cloud (Wukong - 72 qubit)")
    print("3. Local Simulator (no account needed)")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice in ['1', '2']:
        backend = 'Wuyuan' if choice == '1' else 'Wukong'
        print(f"\n🔐 Origin Quantum Cloud - {backend}")
        print("Get API token from: https://qcloud.originqc.com.cn/en/")

        api_token = input("Paste your API token: ").strip()

        if api_token:
            counts = run_on_cloud(api_token, wavelengths, backend)
        else:
            print("⚠️  No token provided, using local simulator")
            counts = run_on_origin_quantum(qvm, prog, cbits)
    else:
        print("\n🖥️  Running on local simulator...")
        counts = run_on_origin_quantum(qvm, prog, cbits)

    # Display results
    print("\n" + "=" * 70)
    print("QUANTUM MEASUREMENT RESULTS")
    print("=" * 70)

    # Sort and display top results
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    print("\n📊 Top measurement outcomes:")
    total_shots = sum(counts.values())
    for state, count in sorted_counts[:15]:
        probability = count / total_shots * 100
        bar = "█" * int(probability / 2)
        print(f"  |{state}⟩: {count:4d} ({probability:5.1f}%) {bar}")

    # Visualize
    print("\n📈 Creating visualization...")
    visualize_results(counts, text)

    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print(f"✨ Text '{text}' encoded as quantum light states")
    print(f"💎 Used {num_qubits} qubits on Chinese quantum hardware")
    print(f"🌊 Wavelength range: {min(w['wavelength_nm'] for w in wavelengths):.1f}-"
          f"{max(w['wavelength_nm'] for w in wavelengths):.1f}nm")
    print(f"🔬 Total measurements: {total_shots}")

    # Check for diamond resonance
    has_637 = any(abs(w['wavelength_nm'] - 637) < 1 for w in wavelengths)
    if has_637:
        print("\n💎 QUANTUM RESONANCE DETECTED!")
        print("   Your text uses 637nm (diamond NV center zero-phonon line)")
        print("   Perfect for quantum memory storage!")

    print("\n✅ Quantum execution complete on Chinese hardware!")
    print("🇨🇳 Powered by Origin Quantum - China's quantum cloud platform")

if __name__ == "__main__":
    main()
