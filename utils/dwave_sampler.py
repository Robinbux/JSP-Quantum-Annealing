#
# Converting the QUBO to BQM and sample on D-Wave machine
#
import dimod
import neal
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

numr = 100  # Number of samples / quantum computations
chstr = 6  # Implementation parameter on the DWave QPU
annealing_time = 1000


def sample_on_dwave(Q, Quantum=False):
    bqm = dimod.BinaryQuadraticModel.from_numpy_matrix(Q)

    if Quantum:
        # Real
        sampler = EmbeddingComposite(DWaveSampler(solver={'qpu':True}))
        #sampler = DWaveSampler()
        return sampler.sample(bqm, chain_strength=chstr, 
        	num_reads=numr, annealing_time=annealing_time)

    # Simulated
    sampler = neal.SimulatedAnnealingSampler()
    return sampler.sample(bqm, num_reads=numr, num_sweeps=1000)
