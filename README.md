# Password Cracker Demo

This is an educational demonstration tool that showcases password cracking techniques using a dictionary-based approach with parallel processing capabilities. The tool is designed for learning and testing purposes only.

## Features

- Multi-process password cracking utilizing all available CPU cores
- Support for multiple hash algorithms (SHA-256 and SHA-512)
- Dictionary-based attack with word combinations
- Performance tracking and visualization
- Interactive command-line interface
- Real-time attempt counting and timing measurements

## Requirements

- Python 3.6+
- matplotlib
- numpy
- multiprocessing (standard library)
- hashlib (standard library)
- typing (standard library)

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
```bash
pip install matplotlib numpy
```

## Usage

1. Prepare a dictionary file (dictionary.txt) with potential password words, one per line. If no dictionary file is found, the program will create a sample one with basic words.

2. Run the program:
```bash
python password_cracker.py
```

3. Enter passwords to test when prompted. The program will attempt to crack each password using both SHA-256 and SHA-512 hashing algorithms.

4. Enter 'q' to quit the program and display the performance visualization.

## How It Works

The PasswordCracker class implements these key features:

1. Dictionary Loading:
   - Reads words from the dictionary file
   - Organizes words by length for efficient access
   - Uses sets for faster word lookups

2. Parallel Processing:
   - Creates worker processes based on available CPU cores
   - Distributes workload across processes using queues
   - Implements poison pill pattern for graceful shutdown

3. Password Cracking Strategy:
   - Tries single words from the dictionary
   - Generates combinations of words
   - Computes hashes using specified algorithm
   - Compares against target hash

4. Performance Visualization:
   - Plots cracking times for each password
   - Compares SHA-256 vs SHA-512 performance
   - Displays interactive bar chart

## Performance Considerations

- Uses multiprocessing for parallel execution
- Implements efficient word storage using sets
- Organizes dictionary by word length to optimize combinations
- Includes timeout mechanisms to prevent hanging
- Terminates processes cleanly after completion

## Limitations

- Only supports dictionary-based attacks
- Limited to SHA-256 and SHA-512 hash algorithms
- Performance depends on dictionary size and password complexity
- Designed for educational purposes, not optimized for real-world use

## Security Notice

This tool is intended for educational and testing purposes only. It should not be used to:
- Crack passwords without authorization
- Test production systems without permission
- Conduct security assessments without proper approval

## Contributing

Contributions are welcome! Some areas for potential improvement:

- Additional hash algorithm support
- More advanced password cracking techniques
- Enhanced visualization options
- Improved error handling
- Memory optimization for large dictionaries

## License

This project is intended for educational use only. Please use responsibly and in accordance with applicable laws and regulations.
