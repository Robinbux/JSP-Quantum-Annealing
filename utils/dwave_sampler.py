#
# Converting the QUBO to BQM and sample on D-Wave machine
#
import dimod
import neal
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

numr = 1000  # Number of samples / quantum computations
chstr = 150  # Implementation parameter on the DWave QPU


def sample_on_dwave(Q, Quantum=False):
    bqm = dimod.BinaryQuadraticModel.from_numpy_matrix(Q)

    if Quantum:
        # Real
        sampler = EmbeddingComposite(DWaveSampler())
        #sampler = DWaveSampler()
        return sampler.sample(bqm, chain_strength=chstr, num_reads=numr)

    # Simulated
    sampler = neal.SimulatedAnnealingSampler()
    return sampler.sample(bqm, num_read=numr)
