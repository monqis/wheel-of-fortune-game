from flask import Flask, request, jsonify
import random
import qiskit
import math
import random
import numpy as np
import qiskit.quantum_info as qi
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Kraus, SuperOp
from qiskit.providers.aer import AerSimulator
from qiskit.tools.visualization import plot_histogram, plot_bloch_multivector

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, PillowWriter
from IPython.display import HTML

from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import QuantumError, ReadoutError
from qiskit.providers.aer.noise import pauli_error
from qiskit.providers.aer.noise import depolarizing_error
from qiskit.providers.aer.noise import thermal_relaxation_error, amplitude_damping_error

def noisy_circuit_model(integer, p):
    """ function which computes the probablity """
    if integer == 0:
        error_bitflip_1 = pauli_error([('X',p), ('I', 1 - p)])
        noise_bitflip_1 = NoiseModel()
        noise_bitflip_1.add_all_qubit_quantum_error(error_bitflip_1, ['u'])
        sim_noise = AerSimulator(noise_model = noise_bitflip_1)
    elif integer == 1:
        error_phaseflip_1 = pauli_error([('Z',p), ('I', 1 - p)])
        noise_phaseflip_1 = NoiseModel()
        noise_phaseflip_1.add_all_qubit_quantum_error(error_phaseflip_1, ['u'])
        sim_noise = AerSimulator(noise_model = noise_phaseflip_1)
    elif integer == 2:
        error_depolarizing_1 = depolarizing_error(p, 1)
        noise_depolarizing_1 = NoiseModel()
        noise_depolarizing_1.add_all_qubit_quantum_error(error_depolarizing_1, ['u'])
        sim_noise = AerSimulator(noise_model = noise_depolarizing_1)
    elif integer == 3:
        error_amp_damp_1 = amplitude_damping_error(p, 1)
        noise_amp_damp_1 = NoiseModel()
        noise_amp_damp_1.add_all_qubit_quantum_error(error_amp_damp_1, ['u'])
        sim_noise = AerSimulator(noise_model = noise_amp_damp_1)
    
    sim_ideal = AerSimulator()
    
    n_qubits = 1
    noise_circ = QuantumCircuit(n_qubits)
    noise_circ.h(0)
    noise_circ.u(math.pi/2, 0, math.pi/6, 0)
    noise_circ.x(0)
    noise_circ.save_density_matrix(label = 'density')
    noise_circ.measure_all()
  
    circ_tnoise = transpile(noise_circ, sim_noise)
    circ_ideal = transpile(noise_circ, sim_ideal)
    result_noise = sim_noise.run(circ_tnoise).result()
    result_ideal = sim_ideal.run(circ_ideal).result()
    density_ideal = np.asarray(result_ideal.data()['density'])
    density_noise = np.asarray(result_noise.data()['density'])

    a_ideal = density_ideal[0,0]
    b_ideal = density_ideal[1,0]
    x_ideal = 2.0*b_ideal.real
    y_ideal = 2.0*b_ideal.imag
    z_ideal = (2.0*a_ideal - 1.0).real
    
    a_noise = density_noise[0,0]
    b_noise = density_noise[1,0]
    x_noise = 2.0*b_noise.real
    y_noise = 2.0*b_noise.imag
    z_noise = (2.0*a_noise - 1.0).real
    
    length_noise = (x_noise**2 + y_noise**2 + z_noise**2)**(1/2)
    length_ideal = (x_ideal**2 + y_ideal**2 + z_ideal**2)**(1/2)

    counts_noise = result_noise.get_counts()
    numbers = [(0,0,0,x_ideal,y_ideal,z_ideal),(0,0,0,x_noise,y_noise,z_noise)]
    
    for i in range(2):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        r = 1
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = r * np.outer(np.cos(u), np.sin(v))
        y = r * np.outer(np.sin(u), np.sin(v))
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))

        # Plot the surface
        ax.plot_surface(x, y, z, color='linen', alpha=0.25)

        # plot circular curves over the surface
        theta = np.linspace(0, 2 * np.pi, 100)
        z = np.zeros(100)
        x = r * np.sin(theta)
        y = r * np.cos(theta)

        ax.plot(x, y, z, color='black', alpha=0.5)
        ax.plot(z, x, y, color='black', alpha=0.5)

        ## add axis lines
        zeros = np.zeros(1000)
        line = np.linspace(-1.5,1.5,1000)

        ax.plot(line, zeros, zeros, color='black', alpha=0.75)
        ax.plot(zeros, line, zeros, color='black', alpha=0.75)
        ax.plot(zeros, zeros, line, color='black', alpha=0.75)

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        ax.set_axis_off()
        ax.text(-0.1,0,1.6,'|0>',fontsize='xx-large',fontweight = 'medium')
        ax.text(-0.1,0,-1.9,'|1>',fontsize='xx-large',fontweight = 'medium')
        ax.text(-1.6,-0.2,0,'x',fontsize='xx-large',fontweight = 'medium')
        ax.text(0.1,-1.95,0,'y',fontsize='xx-large',fontweight = 'medium')
        ax.text(-0.4,0,-2.6,'$1000',fontsize='xx-large',fontweight = 'bold')
        
        ax.quiver(*numbers[i], normalize = True, color = 'red', lw = 3)
        
        plt.savefig(f'./animation{i}.png', dpi = 300)
    
    
    #Outcome of playing the game - win/lose
    result_prob = random.choices([0,1],(counts_noise['0'],counts_noise['1']))
    
    
    #plot_bloch_multivector(result.data(0)['density']).savefig('./bloch_vector.png')
    plot_histogram(counts_noise).savefig('./histogram.png', dpi = 300)
    
    return result_prob[0]

app = Flask(__name__)

data = {
    "message": "hi"
}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/data', methods=['GET'])
def data():
    # name = request.args.get('name')
    x =noisy_circuit_model(0, 0.8)
    return jsonify({
        "message": x
    })

