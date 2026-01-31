import { NextRequest, NextResponse } from 'next/server';

const LUXBIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:-()[]{}@#$%^&*+=_~`<>\"'|\\";

// Morse code timing (in milliseconds)
const DOT_DURATION = 5;      // Short pulse
const DASH_DURATION = 15;    // Long pulse (3x dot)
const INTRA_CHAR_GAP = 5;    // Gap between dots/dashes
const CHAR_GAP = 15;         // Gap between characters
const WORD_GAP = 35;         // Gap between words

// LUXBIN to Morse mapping
const LUXBIN_TO_MORSE: { [key: string]: string } = {
  'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
  'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
  'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
  'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
  'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
  'Z': '--..',
  '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
  '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
  ' ': ' ',     '.': '.-.-.-', ',': '--..--', '!': '-.-.--', '?': '..--..',
  ';': '-.-.-.', ':': '---...', '-': '-....-', '(': '-.--.', ')': '-.--.-',
  '[': '-.--.',  ']': '-.--.-', '{': '-.--.',  '}': '-.--.-', '@': '.--.-.',
  '#': '....--', '$': '...-..-', '%': '.--.--', '^': '.-...', '&': '.-...',
  '*': '-..-',   '+': '.-.-.',  '=': '-...-',  '_': '..--.-', '~': '.--..',
  '`': '.----.',  '<': '.-..-',  '>': '.-..-.', '"': '.-..-.', "'": '.----.',
  '|': '-..-.',  '\\': '.----'
};

interface MorsePulse {
  wavelength_nm: number;
  duration_ms: number;
  character: string;
  morse_symbol: string;
  is_gap: boolean;
  start_time_ms: number;
  color: string;
}

function textToLuxbin(text: string): string {
  const binary = text.split('').map(char =>
    char.charCodeAt(0).toString(2).padStart(8, '0')
  ).join('');

  let luxbin = '';
  for (let i = 0; i < binary.length; i += 6) {
    const chunk = binary.substr(i, 6).padEnd(6, '0');
    const index = parseInt(chunk, 2) % LUXBIN_ALPHABET.length;
    luxbin += LUXBIN_ALPHABET[index];
  }

  return luxbin;
}

function luxbinToWavelength(char: string, enableQuantum: boolean = true): number {
  if (enableQuantum && char === ' ') {
    return 637; // Diamond NV center
  }

  const index = LUXBIN_ALPHABET.indexOf(char);
  if (index === -1) return 500; // Default wavelength

  return 400 + (index / LUXBIN_ALPHABET.length) * 300;
}

function encodeToMorseLight(text: string, enableQuantum: boolean = true): MorsePulse[] {
  const luxbin = textToLuxbin(text);
  const pulses: MorsePulse[] = [];
  let currentTime = 0;

  for (let i = 0; i < luxbin.length; i++) {
    const char = luxbin[i];
    const wavelength = luxbinToWavelength(char, enableQuantum);

    if (char === ' ') {
      // Space = gap with quantum wavelength
      pulses.push({
        wavelength_nm: 637,
        duration_ms: WORD_GAP,
        character: char,
        morse_symbol: 'SPACE',
        is_gap: true,
        start_time_ms: currentTime,
        color: 'hsl(0, 100%, 50%)'
      });
      currentTime += WORD_GAP;
    } else {
      const morsePattern = LUXBIN_TO_MORSE[char] || '....';

      for (let j = 0; j < morsePattern.length; j++) {
        const symbol = morsePattern[j];
        const duration = symbol === '.' ? DOT_DURATION : DASH_DURATION;
        const hue = ((wavelength - 400) / 300) * 360;

        pulses.push({
          wavelength_nm: parseFloat(wavelength.toFixed(2)),
          duration_ms: duration,
          character: char,
          morse_symbol: symbol,
          is_gap: false,
          start_time_ms: currentTime,
          color: `hsl(${hue.toFixed(0)}, 70%, 60%)`
        });

        currentTime += duration;

        // Add intra-character gap
        if (j < morsePattern.length - 1) {
          pulses.push({
            wavelength_nm: 0,
            duration_ms: INTRA_CHAR_GAP,
            character: '',
            morse_symbol: '',
            is_gap: true,
            start_time_ms: currentTime,
            color: 'black'
          });
          currentTime += INTRA_CHAR_GAP;
        }
      }

      // Add gap between characters
      if (i < luxbin.length - 1 && luxbin[i + 1] !== ' ') {
        pulses.push({
          wavelength_nm: 0,
          duration_ms: CHAR_GAP,
          character: '',
          morse_symbol: '',
          is_gap: true,
          start_time_ms: currentTime,
          color: 'black'
        });
        currentTime += CHAR_GAP;
      }
    }
  }

  return pulses;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { text, enable_quantum = true } = body;

    if (!text || typeof text !== 'string') {
      return NextResponse.json(
        { success: false, error: 'Invalid input: text is required' },
        { status: 400 }
      );
    }

    // Convert to LUXBIN
    const luxbinRepresentation = textToLuxbin(text);

    // Encode to Morse Light
    const morsePulses = encodeToMorseLight(text, enable_quantum);

    // Calculate statistics
    const totalDuration = morsePulses[morsePulses.length - 1]?.start_time_ms +
                         morsePulses[morsePulses.length - 1]?.duration_ms || 0;
    const numPulses = morsePulses.filter(p => !p.is_gap).length;
    const uniqueWavelengths = new Set(
      morsePulses.filter(p => p.wavelength_nm > 0).map(p => p.wavelength_nm)
    ).size;

    const response = {
      success: true,
      original_text: text,
      luxbin_representation: luxbinRepresentation,
      morse_light: {
        pulse_sequence: morsePulses,
        statistics: {
          total_pulses: numPulses,
          unique_wavelengths: uniqueWavelengths,
          total_duration_ms: totalDuration,
          total_duration_seconds: (totalDuration / 1000).toFixed(2),
          data_rate_chars_per_second: (text.length / (totalDuration / 1000)).toFixed(2),
          transmission_type: 'Time-domain photonic communication'
        }
      },
      timing: {
        dot_duration_ms: DOT_DURATION,
        dash_duration_ms: DASH_DURATION,
        char_gap_ms: CHAR_GAP,
        word_gap_ms: WORD_GAP
      },
      physics: {
        mode: 'LUXBIN Morse Light',
        description: 'Combines Morse code timing with LUXBIN wavelength encoding',
        wavelength_range: '400-700nm (visible spectrum)',
        quantum_feature: enable_quantum ? '637nm for spaces (diamond NV center)' : 'disabled',
        application: 'Time-domain quantum communication for satellites and fiber optics'
      }
    };

    return NextResponse.json(response, { status: 200 });
  } catch (error: any) {
    console.error('Morse Light encoding error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  return NextResponse.json({
    service: 'LUXBIN Morse Light Language API',
    version: '1.0.0',
    endpoints: {
      POST: '/api/v1/translate-morse'
    },
    description: 'Encodes text as time-domain photonic pulses combining Morse code timing with LUXBIN wavelengths',
    example: {
      input: { text: 'SOS', enable_quantum: true },
      output: 'Time-sequenced light pulses with specific wavelengths and durations'
    }
  });
}
