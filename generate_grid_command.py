#!/usr/bin/env python3
"""
Generate LUXBIN photonic encoded data for Energy Grid Control contract
Developed by Nicheai - For integration with luxbin-chain smart contracts

Usage: python generate_grid_command.py "REDUCE_LOAD_15%" "north_america"
Output: Hex-encoded photonic data for blockchain storage
"""

import sys
import json
from luxbin_light_converter import LuxbinLightConverter

def generate_grid_photonic_data(command: str, region: str) -> str:
    """
    Generate photonic encoded data for a grid command

    Args:
        command: Energy command (e.g., "REDUCE_LOAD_15%")
        region: Geographic region

    Returns:
        Hex-encoded photonic data
    """
    # Initialize converter with satellite support for grid distribution
    converter = LuxbinLightConverter(enable_satellite=True)

    # Create the photonic grid command
    grid_show = converter.create_energy_grid_control_show(command, region)

    # Extract the photonic data (first light sequence item for simplicity)
    # In production, you'd use the full sequence
    if grid_show['light_sequence']:
        # For contract storage, we'll use the raw bytes of the command + region
        command_data = f"{command}:{region}".encode('utf-8')
        photonic_encoded = converter.binary_to_luxbin_chars(command_data)

        # Convert to hex for blockchain storage
        hex_data = command_data.hex()

        return hex_data
    else:
        raise ValueError("No photonic data generated")

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_grid_command.py <command> <region>")
        print("Example: python generate_grid_command.py 'REDUCE_LOAD_15%' 'north_america'")
        sys.exit(1)

    command = sys.argv[1]
    region = sys.argv[2]

    try:
        hex_data = generate_grid_photonic_data(command, region)

        # Output in format suitable for contract calls
        output = {
            "command": command,
            "region": region,
            "photonicData": f"0x{hex_data}",
            "contractCall": f"proposeCommand('{command}', '{region}', 0x{hex_data})"
        }

        print(json.dumps(output, indent=2))

    except Exception as e:
        print(f"Error generating photonic data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()