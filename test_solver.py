"""Tests for Solver — Optimization phase."""

import random
import unittest

from board import Board
from fleet import get_test_fleet
from solver import Solver


def _place_fleet_randomly(board, fleet, rng):
    for ship in fleet:
        while True:
            horizontal = rng.choice([True, False])
            if horizontal:
                row = rng.randint(0, board.grid_size - 1)
                col = rng.randint(0, board.grid_size - ship.size)
            else:
                row = rng.randint(0, board.grid_size - ship.size)
                col = rng.randint(0, board.grid_size - 1)
            try:
                board.place_ship(ship, row, col, horizontal)
                break
            except ValueError:
                continue


class SolverTest(unittest.TestCase):

    def test_should_sink_all_ships(self) -> None:
        board = Board(grid_size=6)
        fleet = get_test_fleet()
        board.place_ship(fleet[0], row=0, col=0, horizontal=True)
        board.place_ship(fleet[1], row=3, col=0, horizontal=True)
        solver = Solver(board)
        solver.solve()
        self.assertTrue(board.all_sunk(), "didn't sink all ships")
        self.assertEqual(
            len(solver.get_shots()),
            board.total_shots(),
            "shot count mismatch"
        )
        self.assertLess(board.total_shots(), 36, "too many shots on a 6x6 board")

    def test_shot_tracking(self) -> None:
        board = Board(grid_size=6)
        fleet = get_test_fleet()
        board.place_ship(fleet[0], row=0, col=0, horizontal=True)
        board.place_ship(fleet[1], row=3, col=0, horizontal=True)
        solver = Solver(board)
        solver.solve()
        self.assertGreater(len(solver.get_shots()), 0, "solver recorded no shots")
        self.assertEqual(
            len(solver.get_shots()),
            board.total_shots(),
            "shots list doesn't match board shot count"
        )

    def test_no_duplicate_shots(self) -> None:
        board = Board(grid_size=6)
        fleet = get_test_fleet()
        board.place_ship(fleet[0], row=0, col=0, horizontal=True)
        board.place_ship(fleet[1], row=3, col=0, horizontal=True)
        solver = Solver(board)
        solver.solve()
        shot_set = set(solver.get_shots())
        self.assertEqual(
            len(shot_set),
            len(solver.get_shots()),
            "solver fired duplicate shots"
        )

    def test_should_be_efficient(self) -> None:
        total_shots = 0
        trials = 20
        rng = random.Random(42)
        for _ in range(trials):
            board = Board(grid_size=10)
            fleet = get_test_fleet()
            _place_fleet_randomly(board, fleet, rng)
            solver = Solver(board)
            solver.solve()
            total_shots += board.total_shots()
        average = total_shots / trials
        self.assertLess(average, 50, f"averaged {average:.1f} shots, need < 50")


if __name__ == "__main__":
    unittest.main()
