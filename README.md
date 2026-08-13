# Lanchester's Law CLI Tool

## Description
A python command‑line application that simulates force attrition using lanchester's linear/quadratic models and probabilistic markov chain extensions.

---

## Installation

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lanchesters-law-cli.git
   cd lanchesters-law-cli
   ```
---

## Usage

### Basic Syntax
```bash
python lanchester.py [options]
```

### Command-Line Arguments
| Option | Type | Description |
|--------|------|-------------|
| `--a` | Float | Constant `a` parameter |
| `--b` | Float | Constant `b` parameter |
| `--A` | Float | Constant `A` parameter |
| `--B` | Float | Constant `B` parameter |
| `--type` | String | Model type: `linear`, `quadratic`, `markov_linear`, `markov_quadratic` |
| `--n` | Int | Number of simulations (Markov only) |
| `--end_t` | Int | End time of simulation |
| `--dt` | Float | Time step for differential equation approximation (linear/quadratic only) |
| `--output` | File | Output CSV file |
---

## Parameters

- **`a`, `b`**: Constants in the differential equation for quality value of different armies
- **`A`, `B`**: Constants in the differential equation for starting number of units for different armies
- **`type`**: Choose simulation type:
  - `linear`: Deterministic ODE solution
  - `quadratic`: Deterministic ODE solution
  - `markov_linear`: Probabilistic Markov chain with `n` simulations (with a / (a + b) probability side B loses one unit else side A loses one unit)
  - `markov_quadratic`: Probabilistic Markov chain with `n` simulations (with (A * a) / (A * a + B * b) probability side B loses one unit else side A loses one unit)
- **`end_t`**: Total simulation time.
- **`dt`**: Time step for numerical integration (linear/quadratic only).
- **`--output`**: Specify CSV output file (overwritten for Markov types).


## Running Tests

### Prerequisites
- Python
- `pytest` installed

### Test Execution
```bash
pytest
```

## Example Commands

```bash
python lanchester.py \
  --a 1 --b 1 --A 5 --B 3 \
  --type quadratic --end_t 100 --dt 0.001
```

### Markov Quadratic Simulation
```bash
python lanchester.py \
  --a 1 --b 1 --A 5 --B 3 \
  --n 10000 --type markov_quadratic --end_t 100 --dt 0.001
```

---

## Project Structure

```
lanchesters/
├── lanchester.py      # Main CLI entry point
├── test_lanchester.py  # Pytest suite
├── README.md
└── LICENSE
```

---

