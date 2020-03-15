#
# Converting the QUBO to BQM and sample on D-Wave machine
#
import dimod
import neal
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

numr = 1000  # Number of samples / quantum computations
chstr = 200  # Implementation parameter on the DWave QPU

anneal_time = 1000.0
pause_duration = 500.0  # Must be greater than 0
pause_start = 0.4  # Must be between 0 and 1

schedule = [[0.0, 0.0], [pause_start * anneal_time, pause_start],
            [pause_start * anneal_time + pause_duration, pause_start], [anneal_time + pause_duration, 1.0]]


def sample_on_dwave(Q, Quantum=False):
    bqm = dimod.BinaryQuadraticModel.from_numpy_matrix(Q)

    if Quantum:
        # Real
        sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))
        # sampler = DWaveSampler()
        return sampler.sample(bqm=bqm,
                              chain_strength=chstr,
                              num_reads=numr
                              # annealing_time=anneal_time,
                              # anneal_schedule=schedule
                              )

    # Simulated
    sampler = neal.SimulatedAnnealingSampler()
    return sampler.sample(bqm=bqm, num_reads=numr)
