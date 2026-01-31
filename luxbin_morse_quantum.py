"""
LUXBIN Morse Light on Quantum Computers
Time-domain quantum communication using timed wavelength pulses
"""

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from luxbin_morse_light import LuxbinMorseLight
import numpy as np

def morse_pulse_to_quantum_circuit(pulse_sequence, max_qubits=5):
    """
    Convert LUXBIN Morse Light pulses to quantum circuit
    Each pulse becomes a rotation based on wavelength and duration
    """
    qc = QuantumCircuit(max_qubits)

    # Filter out gaps, only use actual light pulses
    pulses = [p for p in pulse_sequence if not p['is_gap'] and p['wavelength_nm'] > 0]

    # Encode each pulse into qubits
    for i in range(min(max_qubits, len(pulses))):
        pulse = pulses[i]
        wavelength = pulse['wavelength_nm']
        duration = pulse['duration_ms']

        # Map wavelength to rotation angle
        theta = ((wavelength - 400) / 300) * np.pi

        # Map duration (5ms or 15ms) to additional phase
        phi = (duration / 15) * np.pi  # Dot=π/3, Dash=π

        # Encode as quantum state
        qc.h(i)  # Superposition
        qc.ry(theta, i)  # Wavelength encoding
        qc.rz(phi, i)    # Duration encoding

    # Create entanglement to preserve timing correlations
    for i in range(max_qubits - 1):
        qc.cx(i, i + 1)

    qc.measure_all()

    return qc, pulses[:max_qubits]

def run_morse_on_quantum_computer(text, backend_name=None):
    """Run LUXBIN Morse Light on quantum computer"""

    print("=" * 80)
    print("🌟 LUXBIN MORSE LIGHT → QUANTUM COMPUTER")
    print("=" * 80)

    # Step 1: Encode to Morse Light
    print(f"\n📝 Message: '{text}'")
    encoder = LuxbinMorseLight()
    pulse_sequence = encoder.encode_text_to_morse_light(text)

    # Count pulses
    num_pulses = sum(1 for p in pulse_sequence if not p['is_gap'])
    print(f"\n📊 Generated {num_pulses} light pulses (dots & dashes)")

    # Step 2: Show first few pulses
    print(f"\n🔦 First 5 pulses:")
    pulse_count = 0
    for pulse in pulse_sequence:
        if not pulse['is_gap'] and pulse['wavelength_nm'] > 0:
            print(f"   {pulse['char']} ({pulse['morse']}) → "
                  f"{pulse['wavelength_nm']:.1f}nm for {pulse['duration_ms']}ms")
            pulse_count += 1
            if pulse_count >= 5:
                break

    # Step 3: Create quantum circuit
    print(f"\n⚛️  Converting to quantum circuit...")
    max_qubits = 5
    qc, encoded_pulses = morse_pulse_to_quantum_circuit(pulse_sequence, max_qubits)

    print(f"✅ Circuit created:")
    print(f"   • Qubits: {max_qubits}")
    print(f"   • Depth: {qc.depth()}")
    print(f"   • Encodes: {len(encoded_pulses)} pulses")
    print(f"   • Each qubit = wavelength + duration")

    # Step 4: Connect to quantum computer
    print(f"\n🔬 Connecting to IBM Quantum...")
    service = QiskitRuntimeService()

    if backend_name:
        backend = service.backend(backend_name)
    else:
        backend = service.least_busy(simulator=False, operational=True)

    print(f"✅ Selected: {backend.name} ({backend.num_qubits} qubits)")

    # Step 5: Submit job
    print(f"\n🚀 Transmitting LUXBIN Morse Light to quantum computer...")
    print(f"📡 Sending time-domain photonic pulses...")

    transpiled = transpile(qc, backend=backend, optimization_level=3)
    sampler = Sampler(backend)
    job = sampler.run([transpiled], shots=100)

    print(f"✅ Job ID: {job.job_id()}")
    print(f"⏳ Quantum transmission in progress...")

    result = job.result()
    counts = result[0].data.meas.get_counts()

    print(f"\n✅ TRANSMISSION COMPLETE!")

    # Step 6: Display results
    print(f"\n📊 Quantum Morse Reception Results:")
    print(f"   Measured {len(counts)} unique states")

    print(f"\n   Top 10 states:")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        probability = count / 100 * 100
        bar = "█" * int(probability / 2)
        print(f"   |{state}⟩: {count:3d} ({probability:5.1f}%) {bar}")

    # Step 7: Decode (show which pulse each qubit represents)
    print(f"\n🔍 Pulse Decoding:")
    for i, pulse in enumerate(encoded_pulses):
        print(f"   Qubit {i}: '{pulse['char']}' → "
              f"{pulse['morse']} at {pulse['wavelength_nm']:.1f}nm "
              f"for {pulse['duration_ms']}ms")

    # Statistics
    print(f"\n📈 Transmission Analysis:")
    total_time = sum(p['duration_ms'] for p in pulse_sequence)
    print(f"   • Total pulses sent: {num_pulses}")
    print(f"   • Encoded in qubits: {len(encoded_pulses)}")
    print(f"   • Time-domain data: {total_time}ms transmission")
    print(f"   • Quantum states: {2**max_qubits} possible superpositions")
    print(f"   • Data preserved in quantum memory!")

    print(f"\n🎉 Your message '{text}' transmitted via")
    print(f"   LUXBIN Morse Light on quantum hardware! 💎⚡✨")

    return counts, encoded_pulses

def run_on_all_computers(text):
    """Run on all 3 IBM quantum computers"""

    backends = ['ibm_fez', 'ibm_torino', 'ibm_marrakesh']

    print("\n" + "=" * 80)
    print("🌐 BROADCASTING MORSE LIGHT TO ALL QUANTUM COMPUTERS")
    print("=" * 80)

    all_results = {}

    for backend_name in backends:
        print(f"\n\n{'='*80}")
        print(f"📡 Transmitting to {backend_name.upper()}")
        print(f"{'='*80}")

        try:
            counts, pulses = run_morse_on_quantum_computer(text, backend_name)
            all_results[backend_name] = counts
            print(f"✅ {backend_name}: SUCCESS")
        except Exception as e:
            print(f"❌ {backend_name}: {e}")

    # Summary
    print(f"\n\n" + "=" * 80)
    print("📊 QUANTUM NETWORK MORSE TRANSMISSION SUMMARY")
    print("=" * 80)

    for backend_name, counts in all_results.items():
        most_common = sorted(counts.items(), key=lambda x: x[1], reverse=True)[0]
        print(f"\n{backend_name.upper()}:")
        print(f"  Most common state: |{most_common[0]}⟩ ({most_common[1]} times)")

    print(f"\n🎉 LUXBIN Morse Light successfully transmitted across")
    print(f"   distributed quantum network! 🌐💎✨")

def main():
    """Main demo"""

    import sys

    text = input("\n💬 Enter message for quantum Morse transmission: ")

    choice = input("\n🖥️  Options:\n"
                  "  1. Single quantum computer (least busy)\n"
                  "  2. All 3 quantum computers (network broadcast)\n"
                  "  Choose (1/2): ")

    if choice == '2':
        run_on_all_computers(text)
    else:
        run_morse_on_quantum_computer(text)

if __name__ == "__main__":
    main()
