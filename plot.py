import numpy as np
import matplotlib.pyplot as plt
import csv

def plotData(fileName):
    def getSec(time_str):
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + float(s)

    t = np.array([])
    MF_LF = np.array([])
    T_CORI = np.array([])
    MF_CORI = np.array([])
    RHO_CORI = np.array([])
    P_DP = np.array([])


    with open(fileName) as file:
        csvFile = csv.reader(file, delimiter=',')
        for i, line in enumerate(csvFile):
            if i == 0:
                continue

            t = np.append(t, getSec(line[0]))
            MF_LF = np.append(MF_LF, float(line[1]))
            T_CORI = np.append(T_CORI, float(line[2]))
            MF_CORI = np.append(MF_CORI, float(line[3]))
            RHO_CORI = np.append(RHO_CORI, float(line[4]))
            P_DP = np.append(P_DP, float(line[5]))
            # Pin_DP = np.append(Pin_DP, float(line[6]))
            # Pout_DP = np.append(Pout_DP, float(line[7]))
    t = t - t[0]

    plt.plot(t, MF_LF, label='LF')
    plt.plot(t, MF_CORI, label='CORI')
    plt.title('mass flow')
    plt.xlabel('t [s]')
    plt.ylabel('flow [g/h]')
    plt.legend()

    plt.figure()
    plt.plot(t, RHO_CORI)
    plt.title('density')
    plt.xlabel('t [s]')
    plt.ylabel('$\\rho$ [kg/m^3]')

    plt.figure()
    plt.plot(t, T_CORI)
    plt.title('temperature')
    plt.xlabel('t [s]')
    plt.ylabel('T [degC]')

    plt.figure()
    plt.plot(t, P_DP)
    plt.title('pressure')
    plt.xlabel('t [s]')
    plt.ylabel('dp [mbar]')

    plt.show()