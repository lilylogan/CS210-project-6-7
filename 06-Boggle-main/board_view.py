"""Graphic display of Boggle board"""
from typing import Optional

import graphics.grid as grid_view

COLOR_UNUSED = grid_view.tile_background
COLOR_IN_USE = grid_view.tile_accent_background

VIEW: Optional[grid_view.Grid] = None

def display(board: list[list[str]],
            width: int = 500, height: int = 500,
            title="BOGGLER"):
    """Create a graphical representation of the Boggle board.
    We cache the model component (board) so we can reuse it when
    calls are made to occupy or leave a cell.
    """
    global VIEW
    VIEW = grid_view.Grid(len(board), len(board[0]), title="BOGGLER")
    for row_i in range(len(board)):
        for col_i in range(len(board[0])):
            VIEW.fill_cell(row_i, col_i, COLOR_UNUSED)
            VIEW.label_cell(row_i, col_i, board[row_i][col_i])

def mark_occupied(row: int, col: int):
    """Mark board[row][col] as occupied in display"""
    if VIEW:
        VIEW.fill_cell(row, col, color=COLOR_IN_USE)

def mark_unoccupied(row: int, col: int):
    """Mark board[row][col] as unoccupied (available)"""
    if VIEW:
        VIEW.fill_cell(row, col, color=COLOR_UNUSED)


def prompt_to_close():
    """Prompt the user before closing the display"""
    global VIEW
    if VIEW:
        input("Press enter to close display")
        VIEW.win.close()
        VIEW = None


