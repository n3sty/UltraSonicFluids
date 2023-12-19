import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

def getSec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def plotData(fileName, singleWindow=False):
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

    if singleWindow:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
        ax1.plot(t, MF_LF, label='LF')
        ax1.plot(t, MF_CORI, label='CORI')
        ax1.set_title('mass flow')
        ax1.set(xlabel='t [s]', ylabel='flow [g/h]')
        ax1.legend()

        ax2.plot(t, RHO_CORI)
        ax2.set_title('density')
        ax2.set(xlabel='t [s]', ylabel='$\\rho$ [kg/m^3]')

        ax3.plot(t, T_CORI)
        ax3.set_title('temperature')
        ax3.set(xlabel='t [s]', ylabel='T [degC]')

        ax4.plot(t, P_DP)
        ax4.set_title('pressure')
        ax4.set(xlabel='t [s]', ylabel='dp [mbar]')

        figManager = plt.get_current_fig_manager()
        figManager.full_screen_toggle()
    else:
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

if __name__ == '__main__':
    fileName = 'data/EXP_12-19_1032.csv'
    if len(sys.argv) == 1:
        plotData(fileName)
    else:
        plotData(sys.argv[1])
