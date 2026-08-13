import argparse
import csv
import random
import sys

class Solver:
    def __init__(self, a, b, A, B, end_t, type, dt=None):
        self.a = a
        self.b = b
        self.A = A
        self.B = B
        self.end_t = end_t
        self.dt = dt
        self.type = type
        self.is_markov = type in ["markov_linear", "markov_quadratic"]
        self.results_dict = {}
        
        # Basic validation
        if self.dt is None:
            self.dt = 0.1  # Default time step if not provided
            
        if not self.dt > 0:
            raise ValueError("dt (time step) must be a positive number.")
            
        if self.end_t <= 0:
            raise ValueError("end_t (end time) must be a positive number.")

        if self.end_t <= self.dt:
            self.end_t = self.dt
            
        if self.type not in ['linear', 'quadratic', 'markov_linear', 'markov_quadratic']:
            raise ValueError(f"Invalid type. Must be one of: linear, quadratic, markov_linear, markov_quadratic")

    def solve(self):
        self.results_dict = {}
        t = 0
        (a, b, A, B) = (self.a, self.b, self.A, self.B)
        while A > 0 and B > 0 and t < self.end_t:
            self.results_dict[t] = {'a': a, 'b': b, 'A': A, 'B': B}
            (delta_A, delta_B) = self._calculate_delta_AB(a, b, A, B)
            t += 1 if self.is_markov else self.dt
            A += delta_A
            B += delta_B

        if t < self.end_t and (A > 0 or B > 0) and self.is_markov:
            self.results_dict[t] = {'a': a, 'b': b, 'A': A, 'B': B}

    def get_results(self):
        return self.results_dict

    def get_end_state(self):
        real_end_t = sorted(list(self.results_dict.keys()), reverse=True)[0]
        return (real_end_t, self.results_dict[real_end_t]['A'], self.results_dict[real_end_t]['B'])

    def print_results(self):
        all_ts = sorted(list(self.results_dict.keys()))
        for t in all_ts:
            (A, B) = (self.results_dict[t]['A'], self.results_dict[t]['B'])
            t_title = "t"
            A_title = "A"
            B_title = "B"
            print(f"{t_title:<10}{A_title:<10}{B_title:<10}")
            print(f"{t:<10.5f}{A:<10.5f}{B:<10.5f}")

    def _calculate_delta_AB(self, a, b, A, B):
        if self.type == "linear":
            return self._linear_delta_AB(a, b, A, B)
        elif self.type == "quadratic":
            return self._quadratic_delta_AB(a, b, A, B)
        elif self.type == "markov_linear":
            return self._markov_delta_AB(a, b, A, B, True)
        elif self.type == "markov_quadratic":
            return self._markov_delta_AB(a, b, A, B, False)
        else:
            assert False

    def _linear_delta_AB(self, a, b, A, B):
        delta_A = -b * self.dt
        delta_B = -a * self.dt
        return (delta_A, delta_B)

    def _quadratic_delta_AB(self, a, b, A, B):
        delta_A = -b * B * self.dt
        delta_B = -a * A * self.dt
        return (delta_A, delta_B)

    def _markov_delta_AB(self, a, b, A, B, is_linear):
        weight_side_A_win = a if is_linear else a * A
        weight_side_B_win = b if is_linear else b * B
        prob_side_A_win = weight_side_A_win / (weight_side_A_win + weight_side_B_win)
        side_A_win = random.random() <= prob_side_A_win
        if side_A_win:
            (delta_A, delta_B) = (0, -1)
        else:
            (delta_A, delta_B) = (-1, 0)

        return delta_A, delta_B

    def __str__(self):
        return f"Solver(type={self.type}, a={self.a}, b={self.b}, A={self.A}, B={self.B}, end_t={self.end_t}, dt={self.dt})"

def write_to_file(path, t, A, B):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "A", "B"])
        for (t, A, B) in zip(t, A, B):
            writer.writerow([t, A, B])

def write_to_file_markov(path, t_end, A_end, B_end):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["t_end", "A_end", "B_end"])
        for (t, A, B) in zip(t_end, A_end, B_end):
            writer.writerow([t, A, B])

def run_markov(args):
    A_end = []
    B_end = []
    t_end = []

    for i in range(args.n):
        solver = Solver(
            a=args.a, 
            b=args.b, 
            A=args.A, 
            B=args.B, 
            end_t=args.end_t,
            type=args.type
        )
        solver.solve()
        (t, A, B) = solver.get_end_state()

        A_end.append(A)
        B_end.append(B)
        t_end.append(t)
    
    if args.output is not None:
        write_to_file_markov(args.output, t_end, A_end, B_end)

    print_markov(args, A_end, B_end, t_end)

def print_markov(args, A_end, B_end, t_end):
    A_wins = sum([1 if A_end[i] > 0 and B_end[i] <= 0 else 0 for i in range(args.n)])
    B_wins = sum([1 if B_end[i] > 0 and A_end[i] <= 0 else 0 for i in range(args.n)])
    draws = sum([1 if A_end[i] > 0 and B_end[i] > 0 else 0 for i in range(args.n)])

    perc_A_win = A_wins / args.n * 100
    perc_B_win = B_wins / args.n * 100
    perc_draw = draws / args.n * 100

    avg_A_survivors = sum(A_end) / len(A_end)
    avg_B_survivors = sum(B_end) / len(B_end)
    avg_len = sum(t_end) / len(t_end)

    print(f"{args.n} simulations were run.") 
    print(f"Side A won {perc_A_win:.1f}% of battles, Side B won {perc_B_win:.1f}% of battles, {perc_draw:.1f}% of battles were draws.")
    print(f"Average of {avg_A_survivors:.2f} side A units survived.")
    print(f"Average of {avg_B_survivors:.2f} side B units survived.")
    print(f"Average battle lasted {avg_len:.1f} rounds")

def run_lanchester(args):
    solver = Solver(
            a=args.a, 
            b=args.b, 
            A=args.A, 
            B=args.B, 
            end_t=args.end_t, 
            dt=args.dt, 
            type=args.type
        )
    solver.solve()
    results = solver.get_results()

    all_t = sorted(list(solver.results_dict.keys()))
    all_A = []
    all_B = []

    for t in all_t:
        all_A.append(results[t]['A'])
        all_B.append(results[t]['B'])

    if args.output is not None:
        write_to_file(args.output, all_t, all_A, all_B)

    solver.print_results()

def main(args_str=None):
    parser = argparse.ArgumentParser(
        description="Run a solver with parameters a, b, A, B, end_t, and optional dt."
    )
    
    # Required positional arguments
    parser.add_argument('--a', type=float, help='Parameter a', required=True)
    parser.add_argument('--b', type=float, help='Parameter b', required=True)
    parser.add_argument('--A', type=float, help='Parameter A', required=True)
    parser.add_argument('--B', type=float, help='Parameter B', required=True)
    parser.add_argument('--end_t', type=float,  default=1.0, help='End time')
    
    # Optional parameters
    parser.add_argument('--dt', type=float, default=0.1, help='Time step (default: 0.1) (ignored if markov)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--output', type=str, default=None, help='Simulation results file')
    parser.add_argument('--n', type=int, default=1, help='Number of simulations (Only for markov_linear and markov_quadratic)')
    
    # Required choice parameter (no -- type, but still a flag)
    parser.add_argument(
        '--type', 
        type=str, 
        required=False, 
        choices=['linear', 'quadratic', 'markov_linear', 'markov_quadratic'],
        default='quadratic',
        help='Solver type (default: quadratic)'
    )

    args = parser.parse_args(args_str)
    
    if args.seed is not None:
        random.seed(args.seed)

    if args.n <= 0:
        raise SystemExit("n (number of simulations) must be a positive number")

    if args.a <= 0 or args.b <= 0 or args.A <= 0 or args.B <= 0 or args.end_t <= 0:
        raise SystemExit("a, b, A, B and end_t must be a positive numbers")

    if args.type in ["markov_linear", "markov_quadratic"]:
        run_markov(args)
    else:
        run_lanchester(args)

if __name__ == '__main__':
    main()
