import numpy as np
from dedalus import public as de
from dedalus.tools import post
import logging

dtype = np.float64


logger = logging.getLogger(__name__)

# Parameters
Lx, Ly, Lz = (2*np.pi, 2*np.pi, 2*np.pi)
nx, ny, nz = (64, 64, 64)
Re = 1600
stop_sim_time = 10

domain = de.CartesianCoordinates('x', 'y', 'z')
bases = de.Fourier(domain, size=(nx, ny, nz), bounds=((0, Lx), (0, Ly), (0, Lz)),dtype=dtype)

# Navier-Stokes equations with incompressibility
problem = de.IVP(domain, variables=['u', 'v', 'w', 'p'], time='t')
problem.parameters['Re'] = Re

problem.add_equation("dt(u) + dx(p) = (1/Re)*lap(u) - (u*dx(u) + v*dy(u) + w*dz(u))")
problem.add_equation("dt(v) + dy(p) = (1/Re)*lap(v) - (u*dx(v) + v*dy(v) + w*dz(v))")
problem.add_equation("dt(w) + dz(p) = (1/Re)*lap(w) - (u*dx(w) + v*dy(w) + w*dz(w))")
problem.add_equation("dx(u) + dy(v) + dz(w) = 0")

# Build solver
solver = problem.build_solver(de.timesteppers.RK443)
logger.info('Solver built')

# Initial conditions
x, y, z = bases.local_grids(scales=1)
u = solver.state['u']
v = solver.state['v']
w = solver.state['w']

u['g'] = np.sin(x) * np.cos(y) * np.cos(z)
v['g'] = -np.cos(x) * np.sin(y) * np.cos(z)
w['g'] = 0

# CFL
CFL = de.CFL(solver, initial_dt=0.01, cadence=10, safety=0.5, max_change=1.5, min_change=0.5, max_dt=0.1)
CFL.add_velocities(('u', 'v', 'w'))

# Analysis
snapshots = solver.evaluator.add_file_handler('taylor_green_snapshots', sim_dt=0.5, max_writes=50)
snapshots.add_task('u', scales=1)
snapshots.add_task('v', scales=1)
snapshots.add_task('w', scales=1)
snapshots.add_task('p', scales=1)

# Main loop
try:
    logger.info('Starting loop')
    while solver.proceed and solver.sim_time < stop_sim_time:
        dt = CFL.compute_dt()
        solver.step(dt)
        if (solver.iteration - 1) % 10 == 0:
            logger.info('Iteration: %i, Time: %e, dt: %e', solver.iteration, solver.sim_time, dt)
except Exception as e:
    logger.error('Exception raised during solver loop:', exc_info=e)
finally:
    solver.log_stats()
