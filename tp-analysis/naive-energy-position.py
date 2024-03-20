"""
Make an approximate calculation of dE/dx with
only TP information from a track-like TA.
"""

import trgtools

import click
import matplotlib.pyplot as plt
import numpy as np


COLLECTION_TO_CM = 0.51  # cm per channel.
COLLECTION_ALPHA = 0
TICK_TO_US = 0.016  # us per tick
DRIFT_VELOCITY = 0.16  # cm per us

#@plt.rcParams.update({
#@    "text.usetex": True,
#@    "font.family": "Helvetica"
#@})


def plot_ds(ds: list[float]) -> None:
    """
    Plot the TP ordered ds.
    """
    plt.figure(figsize=(6, 4))
    plt.grid(True)

    plt.plot(ds, '-xk')

    plt.title("TP Ordered ds")
    plt.xlabel(r"$TP_i$  - $TP_{i-1}$")
    plt.ylabel("ds (cm)")

    plt.tight_layout()
    plt.savefig("ds.svg")
    plt.close()


def plot_dE(dE: list[float]) -> None:
    """
    Plot the TP ordered dE.
    """
    plt.figure(figsize=(6, 4))
    plt.grid(True)

    plt.plot(dE, '-xk')

    plt.title("TP Ordered dE")
    plt.xlabel(r"$TP_i$  - $TP_{i-1}$")
    plt.ylabel("dE (ADC Count)")

    plt.tight_layout()
    plt.savefig("dE.svg")
    plt.close()


def plot_dE_per_tp(dE: np.ndarray, ds: float) -> None:
    plt.figure(figsize=(6, 4), dpi=200)
    plt.grid(True)

    plt.plot(dE / ds, '-ok')

    plt.title(r"TP Ordered $\frac{dE}{ds}$")
    plt.xlabel("TP")
    plt.ylabel(r"$\frac{dE}{ds}$")

    plt.tight_layout()
    plt.savefig("dEds.png")
    plt.close()


def energy_correction(adc_integral: np.ndarray) -> np.ndarray:
    """ Apply energy correction factors. """
    g = 7.5  # Electrons per ADC tick
    q_e = 1.602e-4  # fC per electron
    dQ = adc_integral * g * q_e  # fC

    W = 23.6e-6  # MeV per electron
    R = 0.6  # At 500 V per cm
    dE = dQ * W / q_e / R
    return dE


def plot_adc_integral(tps: np.ndarray) -> None:
    """
    Plot the TP ordered ADC integral.
    """
    plt.figure(figsize=(6, 4))
    plt.grid(True)

    plt.plot(tps['adc_integral'], '-xk')

    plt.title("TP Ordered ADC Integral")
    plt.xlabel("TP")
    plt.ylabel("ADC Integral")

    plt.tight_layout()
    plt.savefig("adc_integral.svg")
    plt.close()


def calculate_dtheta(tp0: np.ndarray, tp1: np.ndarray) -> float:
    """
    Calculate the relative theta between to TPs.

    Parameters:
        tp0, tp1 (np.ndarray): TriggerPrimitives to calculate on.

    Returns dtheta.
    """
    channel_diff = (tp1['channel'] - tp0['channel']) * COLLECTION_TO_CM
    height_diff = np.abs(tp1['time_start'].astype(int) - tp0['time_start'].astype(int)) * TICK_TO_US * DRIFT_VELOCITY
    return np.arctan2(channel_diff, height_diff)


def get_average_dtheta(ta: np.ndarray) -> float:
    """
    Calculate the average relative theta in this TA.

    Parameter:
        ta (np.ndarray): An array where each element is a TriggerPrimitive.

    Returns the average dtheta.
    """
    average_dtheta = 0
    for tp0, tp1 in zip(ta[:-1], ta[1:]):
        average_dtheta += calculate_dtheta(tp0, tp1)
    return average_dtheta / (len(ta) - 1)


def calculate_dphi(tp0: np.ndarray, tp1: np.ndarray) -> float:
    """
    Calculate the relative phi between to TPs.

    Parameters:
        tp0, tp1 (np.ndarray): TriggerPrimitives to calculate on.

    Returns dphi.
    """
#    channel_diff = (tp1['channel'] - tp0['channel']) * COLLECTION_TO_CM
#    if channel_diff == 0:
#        return 0
#    if channel_diff > 0:
#        return np.pi/2
#    return -np.pi/2
    return np.pi/4


def get_average_dphi(ta: np.ndarray) -> float:
    """
    Calculate the average relative phi in this TA.

    Parameter:
        ta (np.ndarray): An array where each element is a TriggerPrimitive.

    Returns the average dphi.
    """
    average_dphi = 0
    for tp0, tp1 in zip(ta[:-1], ta[1:]):
        average_dphi += calculate_dphi(tp0, tp1)
    return average_dphi / len(ta[:-1])


def get_u_x(theta: float, phi: float) -> float:
    return np.sin(theta) * np.cos(phi)


def get_u_y(theta: float, phi: float) -> float:
    return np.sin(theta) * np.sin(phi)


def cos_gamma(alpha: float, u_x: float, u_y: float) -> float:
    return np.abs(u_x*np.sin(alpha) + u_y * np.cos(alpha))


def get_ds(tp0: np.ndarray, tp1: np.ndarray) -> float:
    """
    Calculate the ds between these two TPs.
    """
    theta = calculate_dtheta(tp0, tp1)
    phi = calculate_dphi(tp0, tp1)
    u_x = get_u_x(theta, phi)
    u_y = get_u_y(theta, phi)
    return COLLECTION_TO_CM / cos_gamma(COLLECTION_ALPHA, u_x, u_y)


def get_dE(tp0: np.ndarray, tp1: np.ndarray) -> float:
    """
    Calculate the change in energy (ADC integral).
    """
    return tp1['adc_integral'].astype(int) - tp0['adc_integral'].astype(int)


@click.command()
@click.argument("file")
@click.option('-f', "--fragment", type=click.INT)
def main(file, fragment):
    data = trgtools.TAReader(file)
    fragment_path = data.get_fragment_paths()[fragment]

    _ = data.read_fragment(fragment_path)
    ta = data.ta_data[3]
    tps = data.tp_data[3][29:]

    plot_adc_integral(tps)

    phi = get_average_dphi(tps)
    print("Average phi:", phi)
    theta = get_average_dtheta(tps)
    print("Average theta:", theta)
    ds = get_ds(tps[0], tps[-1])
    dE = energy_correction(tps['adc_integral'])

    plot_dE(dE)
    print("Average ds:", ds)
    print("Average dE:", np.mean(dE))
    plot_dE_per_tp(dE, ds)


if __name__ == "__main__":
    main()
