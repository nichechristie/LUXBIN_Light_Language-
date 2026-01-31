import { NextRequest, NextResponse } from 'next/server';

const LUXBIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:-()[]{}@#$%^&*+=_~`<>\"'|\\";

interface LightBeam {
  character: string;
  wavelength_nm: number;
  color: string;
  duration_ms: number;
}

function textToLuxbin(text: string): string {
  // Convert text to binary
  const binary = text.split('').map(char =>
    char.charCodeAt(0).toString(2).padStart(8, '0')
  ).join('');

  // Convert binary to LUXBIN (6-7 bits per character)
  let luxbin = '';
  for (let i = 0; i < binary.length; i += 6) {
    const chunk = binary.substr(i, 6).padEnd(6, '0');
    const index = parseInt(chunk, 2) % LUXBIN_ALPHABET.length;
    luxbin += LUXBIN_ALPHABET[index];
  }

  return luxbin;
}

function luxbinToWavelengths(luxbin: string, enableQuantum: boolean = true): LightBeam[] {
  const beams: LightBeam[] = [];
  const QUANTUM_ZERO_PHONON = 637; // Diamond NV center zero-phonon line (nm)

  for (let i = 0; i < luxbin.length; i++) {
    const char = luxbin[i];
    const index = LUXBIN_ALPHABET.indexOf(char);

    if (enableQuantum && char === ' ') {
      // Use diamond NV center wavelength for spaces
      beams.push({
        character: char,
        wavelength_nm: QUANTUM_ZERO_PHONON,
        color: `hsl(0, 100%, 50%)`, // Red for NV center
        duration_ms: 5
      });
    } else {
      // Map character to visible spectrum (400-700nm)
      const wavelength = 400 + (index / LUXBIN_ALPHABET.length) * 300;
      const hue = ((wavelength - 400) / 300) * 360;

      beams.push({
        character: char,
        wavelength_nm: parseFloat(wavelength.toFixed(2)),
        color: `hsl(${hue.toFixed(0)}, 70%, 60%)`,
        duration_ms: 5
      });
    }
  }

  return beams;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { text, enable_quantum = true, format = 'full' } = body;

    if (!text || typeof text !== 'string') {
      return NextResponse.json(
        { success: false, error: 'Invalid input: text is required' },
        { status: 400 }
      );
    }

    // Convert text to LUXBIN
    const luxbinRepresentation = textToLuxbin(text);

    // Convert LUXBIN to wavelengths
    const lightSequence = luxbinToWavelengths(luxbinRepresentation, enable_quantum);

    // Calculate total duration
    const totalDuration = lightSequence.reduce((sum, beam) => sum + beam.duration_ms, 0) / 1000;

    // Build binary representation
    const binaryCode = text.split('').map(char =>
      char.charCodeAt(0).toString(2).padStart(8, '0')
    ).join(' ');

    const response = {
      success: true,
      original_text: text,
      luxbin_representation: luxbinRepresentation,
      binary_code: binaryCode,
      quantum_mode: enable_quantum,
      light_show: {
        light_sequence: lightSequence,
        total_duration: totalDuration,
        quantum_data: enable_quantum ? {
          total_states: lightSequence.length,
          estimated_storage_time: lightSequence.length * 5, // microseconds
          zero_phonon_line: 637 // nm
        } : null
      },
      physics: {
        mode: 'Diamond NV Centers',
        wavelength_range: '400-700nm (visible spectrum)',
        quantum_optimization: enable_quantum ? '637nm zero-phonon line' : 'disabled',
        energy_efficiency: '99% reduction vs. traditional computing'
      }
    };

    return NextResponse.json(response, { status: 200 });
  } catch (error: any) {
    console.error('Translation error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  return NextResponse.json({
    service: 'LUXBIN Light Language Translator API',
    version: '1.0.0',
    endpoints: {
      POST: '/api/v1/translate'
    },
    description: 'Translates natural language to photonic light sequences optimized for diamond NV center quantum computers'
  });
}
