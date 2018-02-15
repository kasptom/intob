from data import preprocessed_glyphs
from solver.lstm_solver import LstmSolver
from solver.softmax_solver import SoftmaxSolver
from utils.mappings.penchars_mapping_2 import mapping

glyphs = preprocessed_glyphs(mapping)
solver = LstmSolver(glyphs)
solver.train()
