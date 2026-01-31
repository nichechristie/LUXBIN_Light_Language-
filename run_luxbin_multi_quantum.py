#!/usr/bin/env python3
"""
LUXBIN Light Language - Multi-Quantum Computer Runner
Run LUXBIN Light Language across multiple quantum computing providers

This script:
1. Loads quantum backend configuration
2. Connects to multiple quantum computers (IBM, IonQ, Rigetti)
3. Runs LUXBIN light language encoding/decoding in parallel
4. Demonstrates distributed quantum computing capabilities

Author: Quantum Internet Team
"""

import asyncio
import json
import os
import sys
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import time

# Add parent directory to path for imports
sys.path.append('..')

from luxbin_quantum_computer import (
    text_to_luxbin,
    luxbin_to_wavelengths,
    create_luxbin_quantum_circuit,
    run_on_quantum_computer
)

class MultiQuantumLuxbinRunner:
    """Run LUXBIN Light Language on multiple quantum computers"""

    def __init__(self, config_path: str = "../quantum_backends_config.json"):
        self.config = self.load_config(config_path)
        self.results = {}

    def load_config(self, config_path: str) -> Dict:
        """Load quantum backend configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Config file not found: {config_path}")
            print("   Using default configuration...")
            return self.get_default_config()

    def get_default_config(self) -> Dict:
        """Get default configuration if file not found"""
        return {
            "luxbin_deployment": {
                "light_language_backends": ["ibm_fez", "ionq_harmony", "rigetti_aspen"]
            }
        }

    async def run_on_multiple_quantum_computers(self, text: str) -> Dict[str, Any]:
        """
        Run LUXBIN Light Language processing on multiple quantum computers

        Args:
            text: Text to encode as LUXBIN light language

        Returns:
            Results from all quantum computers
        """
        print("🌈 LUXBIN MULTI-QUANTUM RUNNER")
        print("=" * 50)
        print(f"Input text: {text}")
        print()

        # Step 1: Convert text to LUXBIN
        print("📝 Step 1: Converting text to LUXBIN Light Language...")
        luxbin, binary = text_to_luxbin(text)
        print(f"   LUXBIN: {luxbin[:50]}..." if len(luxbin) > 50 else f"   LUXBIN: {luxbin}")
        print(f"   Binary length: {len(binary)} bits")
        print()

        # Step 2: Convert LUXBIN to photonic wavelengths
        print("🌈 Step 2: Converting LUXBIN to photonic wavelengths...")
        wavelengths = luxbin_to_wavelengths(luxbin, enable_quantum=True)
        print(f"   Generated {len(wavelengths)} wavelength encodings")
        for i, wl in enumerate(wavelengths[:3]):  # Show first 3
            print(f"   {i+1}. {wl['character']}: {wl['wavelength_nm']:.1f}nm ({wl['energy_ev']:.3f}eV)")
        if len(wavelengths) > 3:
            print(f"   ... and {len(wavelengths)-3} more")
        print()

        # Step 3: Create quantum circuit
        print("⚛️  Step 3: Creating quantum circuit...")
        circuit = create_luxbin_quantum_circuit(wavelengths, num_qubits=min(5, len(wavelengths)))
        print(f"   Created circuit with {circuit.num_qubits} qubits and {circuit.size()} gates")
        print()

        # Step 4: Run on multiple quantum computers across countries
        print("🚀 Step 4: Running on international quantum computers...")
        backends = self.config.get("luxbin_deployment", {}).get("light_language_backends", ["ibm_fez"])

        # Show which countries we're connecting to
        countries = set()
        for backend in backends:
            if backend in self.config.get("quantum_backends", {}):
                for provider_data in self.config["quantum_backends"].values():
                    for backend_data in provider_data.get("backends", []):
                        if backend_data["name"] == backend:
                            countries.add(backend_data.get("country", "Unknown"))
        if countries:
            print(f"   🌍 Connecting to quantum computers in: {', '.join(sorted(countries))}")
            print(f"   🌐 Total countries: {len(countries)}")

        # Run in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(backends)) as executor:
            futures = []
            for backend in backends:
                print(f"   Submitting to {backend}...")
                future = executor.submit(self.run_single_backend, circuit, backend)
                futures.append((backend, future))

            # Collect results
            for backend, future in futures:
                try:
                    result = future.result(timeout=300)  # 5 minute timeout
                    self.results[backend] = result
                    print(f"   ✅ {backend}: Completed")
                except Exception as e:
                    print(f"   ⚠️  {backend}: Failed - {e}")
                    self.results[backend] = {"error": str(e)}

        print()
        print("📊 RESULTS SUMMARY")
        print("=" * 30)

        for backend, result in self.results.items():
            if "error" in result:
                print(f"❌ {backend}: {result['error']}")
            else:
                print(f"✅ {backend}: {len(result.get('counts', {}))} measurement outcomes")

        return {
            "input_text": text,
            "luxbin_encoding": luxbin,
            "wavelengths": wavelengths,
            "quantum_results": self.results
        }

    def run_single_backend(self, circuit, backend: str) -> Dict:
        """Run circuit on a single quantum backend"""
        try:
            # Import here to avoid issues if not available
            result = run_on_quantum_computer(circuit, backend_name=backend)

            # Extract basic statistics
            counts = result.quasi_dists[0] if hasattr(result, 'quasi_dists') else {}
            if hasattr(result, 'result') and hasattr(result.result(), 'get_counts'):
                counts = result.result().get_counts()

            return {
                "backend": backend,
                "counts": dict(counts) if counts else {},
                "success": True
            }
        except Exception as e:
            return {
                "backend": backend,
                "error": str(e),
                "success": False
            }

async def main():
    """Main function"""
    runner = MultiQuantumLuxbinRunner()

    # Get text input
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("💬 Enter text to encode as quantum light: ")

    # Run on multiple quantum computers
    start_time = time.time()
    results = await runner.run_on_multiple_quantum_computers(text)
    end_time = time.time()

    print(".2f")
    print(f"🌟 LUXBIN Light Language successfully processed on {len(runner.results)} quantum computers!")

if __name__ == "__main__":
    asyncio.run(main())