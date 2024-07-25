[Article link](OTM1_Roteamento_de_veículos_capacitados.pdf)

# CVRP Optimization

This project provides implementations of optimization algorithms for the Vehicle Routing Problem (CVRP). It includes:

- **Ant Colony Optimization**
- **Simplex Algorithm**

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

Ensure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/).

### Installation

Clone the repository:

   ```bash
   git clone https://github.com/HenriquePCR/CVRP_optimization.git
   cd CVRP_optimization
   ```
## Running the Algorithms

### Ant Colony Optimization

To run the Ant Colony Optimization algorithm, use the following command:

```bash
   python ant_main.py
```
You will be prompted to select one of the available datasets and specify the time period for the algorithm to run.

### Ant Colony Optimization

To run the Simplex Algorithm, follow these steps:

1. Navigate to the simplex_src directory:
```bash
   cd simplex_src
```

2. Execute the script:
```bash
   python main.py
```

## Dataset Naming
The dataset files follow the pattern E-nX-kY.txt, where:

- X represents the number of cities.
- Y represents the number of trucks.

Example files included in the datasets/ directory are:

- E-n16-k8.txt
- E-n19-k2.txt
- E-n22-k4.txt
- E-n33-k4.txt
