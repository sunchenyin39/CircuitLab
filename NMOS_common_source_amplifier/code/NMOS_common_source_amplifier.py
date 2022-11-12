import numpy as np
import matplotlib.pyplot as plt
import csvfun


def main():
    un_cox = 50e-6
    W_L = 10
    v_th = 0.3
    t_interval = 1e-6
    t_raise = 100e-6
    t_max = 200000e-6
    t_start_ac = 5000e-6
    init_zero_num = 1
    v3_amplitude = 16
    v1_amplitude_dc = 2.3
    v1_amplitude_ac = 0.1
    omega1_ac = 2*np.pi*100
    v3_source = voltage_generator_dc(
        t_raise, t_max, t_interval, v3_amplitude, init_zero_num)
    v1_source = voltage_generator_dc_and_ac(
        t_raise, t_max, t_interval, t_start_ac, v1_amplitude_dc, v1_amplitude_ac, omega1_ac, init_zero_num)
    R1 = 10000
    R2 = 10000
    A = np.array([[0, 1, 1, -1], [1, 0, -R2, 0], [1, 0, 0, R1], [0, 1, 0, 0]])

    t = [0.0]
    v2 = [0.0]
    i1 = [0.0]
    i2 = [0.0]
    i3 = [0.0]
    for i in range(int(t_max/t_interval)+1):
        b = np.zeros([4, 1])
        b[2][0] = v3_source[i+1]
        if v1_source[i] < v_th:
            b[3][0] = 0
        else:
            if v2[i] < v1_source[i]-v_th:
                b[3][0] = un_cox*W_L*((v1_source[i]-v_th)
                                      * v2[i]-0.5*v2[i]*v2[i])
            else:
                b[3][0] = 0.5*un_cox*W_L * \
                    (v1_source[i]-v_th)*(v1_source[i]-v_th)
        x = np.linalg.solve(A, b)
        t.append(i*t_interval)
        v2.append(x[0][0])
        i1.append(x[1][0])
        i2.append(x[2][0])
        i3.append(x[3][0])
    t = t[1:]
    v2 = v2[1:]
    i1 = i1[1:]
    i2 = i2[1:]
    i3 = i3[1:]
    v1_source = v1_source[1:]
    v3_source = v3_source[1:]
    csvfun.data_to_csv('NMOS_common_source_amplifier.csv', [
                       't', 'V1_source', 'V2'], [t, v1_source, v2])

    t = t[int((t_start_ac+t_raise)/2/t_interval):]
    v1_ac = (np.array(v1_source) -
             v1_amplitude_dc).tolist()[int((t_start_ac+t_raise)/2/t_interval):]
    v2_ac = (np.array(v2)-v2[int((t_start_ac+t_raise)/2/t_interval)]
             ).tolist()[int((t_start_ac+t_raise)/2/t_interval):]
    plt.plot(t,v1_ac,label='Vin')
    plt.plot(t,v2_ac,label='Vout')
    plt.title("NMOS_common_source_amplifier")
    plt.ylabel("Voltage(V)")
    plt.xlabel("t(s)")
    plt.legend(loc = 'upper right')
    plt.show()


def voltage_generator_dc(t_raise, t_max, t_interval, v_amplitude, init_zero_num):
    """DC voltage generator generates DC voltage signal.

    Args:
        t_raise (float): The time point when the voltage signal starts to raise.
        t_max (float): The maximun time to simulate.
        t_interval (float): The interval time to simulate.
        v_amplitude (float): DC voltage signal amplitude.
        init_zero_num (int): The number of initial 0.0s in voltage list.

    Returns:
        list[float]: Voltage list.
    """
    voltage_list = []
    for i in range(init_zero_num):
        voltage_list.append(0.0)
    for i in range(int(t_max/t_interval)+1):
        if (i*t_interval < t_raise):
            voltage_list.append(v_amplitude/t_raise*t_interval*i)
        else:
            voltage_list.append(v_amplitude)
    return voltage_list


def voltage_generator_dc_and_ac(t_raise_dc, t_max, t_interval, t_start_ac, v_amplitude_dc, v_amplitude_ac, omega_ac, init_zero_num):
    """DC+AC voltage generator generates superposition signal of DC voltage signal and AC sinusoidal voltage signal.

    Args:
        t_raise_dc (float): The time point when the DC voltage signal starts to raise.
        t_max (float): The maximun time to simulate.
        t_interval (float): The interval time to simulate.
        t_start_ac (float): The time point when the AC sinusoidal voltage signal starts.
        v_amplitude_dc (float): DC voltage signal amplitude.
        v_amplitude_ac (float): AC voltage signal amplitude.
        omega_ac (float): AC voltage signal circular frequency.
        init_zero_num (int): The number of initial 0.0s in voltage list.

    Returns:
        list[float]: Voltage list.
    """
    voltage_list = []
    for i in range(init_zero_num):
        voltage_list.append(0.0)
    for i in range(int(t_max/t_interval)+1):
        if (i*t_interval < t_raise_dc):
            voltage_list.append(v_amplitude_dc/t_raise_dc*t_interval*i)
        elif i*t_interval < t_start_ac:
            voltage_list.append(v_amplitude_dc)
        else:
            voltage_list.append(v_amplitude_dc+v_amplitude_ac *
                                np.sin(omega_ac*(i*t_interval-t_start_ac)))
    return voltage_list


if __name__ == "__main__":
    main()
