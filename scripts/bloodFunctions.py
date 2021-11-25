import spidev
import time
import numpy as np
import matplotlib.pyplot as plt

########################################
#   Open, use and close SPI ADC
########################################

spi = spidev.SpiDev()


def initSpiAdc():
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    print("SPI for ADC have been initialized")


def deinitSpiAdc():
    spi.close()
    print("SPI cleanup finished")


def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1


########################################
#   Save and read data
########################################

def save(samples, start, finish):
    filename = 'blood-data {}.txt'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))

    with open(filename, "w") as outfile:
        outfile.write('- Blood Lab\n')
        outfile.write('- Date: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Duration: {:.2f} s\n\n'.format(finish - start))

        np.savetxt(outfile, np.array(samples).T, fmt='%d')


def read(filename):
    with open(filename) as f:
        lines = f.readlines()

    duration = float(lines[2].split()[2])
    samples = np.asarray(lines[4:], dtype=int)

    return samples, duration, len(samples)


def calibration(mm):
    print("Калибровка " + str(mm))
    begin = time.time()
    value_calibration = []
    x = []
    while time.time() - begin < 10:
        value_calibration.append(getAdc())
    for i in range(len(value_calibration)):
        x.append(i)
    duration_calibration = time.time() - begin
    value_calibration_str = [str(item) for item in value_calibration]
    with open(str(mm) + " mmHg.txt", "w") as mmHg:
        mmHg.write('- Blood Lab\n\n')
        mmHg.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        mmHg.write('- Experiment duration = {:.2f} s\n'.format(duration_calibration))
        mmHg.write('- Sampling period = {:.2f} us\n'.format(duration_calibration / len(value_calibration) * 1000000))
        mmHg.write('- Sampling frequency = {} Hz\n'.format(int(len(value_calibration) / duration_calibration)))
        mmHg.write('- Samples count = {}\n'.format(len(value_calibration)))
        mmHg.write("\n".join(value_calibration_str))
    plt.plot(x, value_calibration)
    plt.xlabel("Номер измерения")
    plt.ylabel("ADC")
    plt.savefig(str(mm) + ".png")
    plt.close()
    print("Калибровка завершена\n")


def experiment(mm):
    print("Эксперимент" + str(mm))
    begin = time.time()
    value_calibration = []
    x = []
    while time.time() - begin < 20:
        value_calibration.append(getAdc())
    for i in range(len(value_calibration)):
        x.append(i)
    duration_calibration = time.time() - begin
    value_calibration_str = [str(item) for item in value_calibration]
    with open(str(mm) + " mmHg.txt", "w") as mmHg:
        mmHg.write('- Blood Lab\n\n')
        mmHg.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        mmHg.write('- Experiment duration = {:.2f} s\n'.format(duration_calibration))
        mmHg.write('- Sampling period = {:.2f} us\n'.format(duration_calibration / len(value_calibration) * 1000000))
        mmHg.write('- Sampling frequency = {} Hz\n'.format(int(len(value_calibration) / duration_calibration)))
        mmHg.write('- Samples count = {}\n'.format(len(value_calibration)))
        mmHg.write("\n".join(value_calibration_str))
    plt.plot(x, value_calibration)
    plt.plot(linewidth="0.5")
    plt.xlabel("Номер измерения")
    plt.ylabel("ADC")
    plt.savefig(str(mm) + ".png")
    plt.close()
    print("Эксперимент завершен\n")


def file_read(file_path):
    f = open(file_path, "r")
    m = []
    for i in f:
        m.append(int(i))
    sr_znach = sum(m) / len(m)
    print(sr_znach)
    return int(sr_znach)


def calibration(sr_40, sr_60, sr_80, sr_160):
    fig = plt.figure(figsize=(10, 5), dpi=200)
    plt.axis([400, 1800, 0, 180])
    ax = plt.gca()
    ys = [sr_40, sr_60, sr_80, sr_160]
    xs = [40, 60, 80, 160]
    trend = np.polyfit(ys, xs, 1)
    plt.plot(ys, xs, 'o')
    trendpoly = np.poly1d(trend)
    plt.plot(ys, trendpoly(ys), label=f"$P={trend[0]:0.3f}\;N{trend[1]:+0.2f}$")
    print(trendpoly(xs))
    print(trend)
    ax.set_facecolor('white')
    plt.xlabel('Давление [Па]', fontsize=15)
    plt.ylabel('Отсчёты АЦП', fontsize=15)
    plt.title('Калибровочный график зависимости показаний АЦП от давления', fontsize=15, fontweight='bold')
    ax.minorticks_on()
    plt.grid(which="both", linewidth=1)
    plt.grid(which="minor", ls="--", linewidth=0.25)
    plt.legend(fontsize=13)
    plt.show()
    plt.savefig('pressure-calibration.png')
    return trend


def blood_pressure(file_path, file_name, trend, when):
    f = open(file_path, "r")
    m = []
    time = []
    tick = 66.27 / 1000000
    for i in f:
        m.append(int(i) * trend[0])
    for i in range(len(m)):
        time.append(tick * i)
    fig = plt.figure(figsize=(10, 5), dpi=200)
    plt.axis([0, 21, 60, 160])
    plt.plot(time, m, linewidth=0.3)
    ax = plt.gca()
    ax.set_facecolor('white')
    plt.xlabel('Время [с]', fontsize=15)
    plt.ylabel('Давление [мм.рт.ст]', fontsize=15)
    plt.title("Артериальное давление " + when + " физической нагрузки", fontsize=15, fontweight='bold')
    ax.minorticks_on()
    plt.grid(which="both", linewidth=1)
    plt.grid(which="minor", ls="--", linewidth=0.25)
    plt.legend(fontsize=13)
    plt.show()
    plt.savefig(file_name + '.png')


def pulse(file_path, file_name, trend, when):
    f = open(file_path, "r")
    m = []
    time = []
    time_m = []
    tick = 66.27 / 1000000
    for i in f:
        m.append(int(i)*trend[0])
    for i in range(len(m)):
        time.append(i*tick)
    print(len(m))
    print(len(time))
    pulsem = []
    for i in range(0,len(m),1000):
        if i+1000<len(m):
            pulsem.append((m[i+1000]-m[i])/(time[i+1000]-time[i]))
            time_m.append(tick * i)   
        else:
            break
    fig = plt.figure(figsize=(10, 5), dpi=200)
    plt.axis([0, 21, -20, 20])
    plt.plot(time_m, pulsem, linewidth=1)
    ax = plt.gca()
    ax.set_facecolor('white')
    plt.xlabel('Время [с]', fontsize=15)
    plt.ylabel('Изменение давления в артерии [мм.рт.ст]', fontsize=15)
    plt.title("Пульс " + when + " физической нагрузки", fontsize=15, fontweight='bold')
    ax.minorticks_on()
    plt.grid(which="both", linewidth=1)
    plt.grid(which="minor", ls="--", linewidth=0.25)
    plt.legend(fontsize=13)
    plt.savefig(file_name + '.png')
    plt.show()
