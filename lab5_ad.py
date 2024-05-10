import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from scipy.signal import butter, filtfilt


def harmonic_with_noise(time, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    signal = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(time))

    if show_noise:
        return signal + noise
    else:
        return signal


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonic with Noise")

        self.amplitude = tk.DoubleVar(value=1.0)
        self.frequency = tk.DoubleVar(value=0.5)  # Частота змінена на 0.5
        self.phase = tk.DoubleVar(value=0.0)
        self.noise_mean = tk.DoubleVar(value=0.0)
        self.noise_covariance = tk.DoubleVar(value=0.1)
        self.show_noise = tk.BooleanVar(value=False)
        self.cutoff_frequency = tk.DoubleVar(value=5.0)
        self.filter_type = tk.StringVar(value="lowpass")
        self.show_filtered_harmonic = tk.BooleanVar(value=False)

        self.initUI()

    def initUI(self):
        # Create the plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create sliders and checkboxes
        self.create_slider("Amplitude", self.amplitude, 0, 10)
        self.create_slider("Frequency", self.frequency, 0, 10)
        self.create_slider("Phase", self.phase, 0, 2*np.pi)
        self.create_slider("Noise Mean", self.noise_mean, -1, 1)
        self.create_slider("Noise Covariance", self.noise_covariance, 0, 1)
        self.create_slider("Cutoff Frequency", self.cutoff_frequency, 0, 10)

        show_noise_checkbox = tk.Checkbutton(self.root, text="Show Noise", variable=self.show_noise,
                                             command=self.update_plot)
        show_noise_checkbox.pack()

        show_filtered_checkbox = tk.Checkbutton(self.root, text="Show Filtered Harmonic",
                                                variable=self.show_filtered_harmonic, command=self.update_plot)
        show_filtered_checkbox.pack()

        filter_type_label = tk.Label(self.root, text="Filter Type:")
        filter_type_label.pack()
        lowpass_radio = tk.Radiobutton(self.root, text="Lowpass", variable=self.filter_type, value="lowpass",
                                       command=self.update_plot)
        lowpass_radio.pack(anchor=tk.W)
        highpass_radio = tk.Radiobutton(self.root, text="Highpass", variable=self.filter_type, value="highpass",
                                        command=self.update_plot)
        highpass_radio.pack(anchor=tk.W)

        # Create Reset button
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_parameters)
        reset_button.pack()

        self.update_plot()

    def create_slider(self, label, variable, min_val, max_val):
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(fill=tk.X, padx=5, pady=5)
        label_widget = tk.Label(slider_frame, text=label)
        label_widget.pack(side=tk.LEFT)
        slider_widget = tk.Scale(slider_frame, from_=min_val, to=max_val, resolution=0.01, orient=tk.HORIZONTAL,
                                 variable=variable, command=self.update_plot)
        slider_widget.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def update_plot(self, *args):
        self.ax.clear()
        time = np.linspace(0, 10, 1000)
        signal = harmonic_with_noise(time, self.amplitude.get(), self.frequency.get(), self.phase.get(),
                                      self.noise_mean.get(), self.noise_covariance.get(), self.show_noise.get())

        self.ax.plot(time, signal, label='Harmonic', color='green')  # зелений графік

        if self.show_filtered_harmonic.get():
            filtered_signal = self.apply_filter(signal)
            self.ax.plot(time, filtered_signal, label='Filtered Harmonic', color='purple')  # фіолетовий графік

        self.ax.legend(loc='upper right')  # переміщення легенди у правий верхній куток
        self.canvas.draw()

    def apply_filter(self, signal):
        fs = 1000  # Згідно з використовуваною частотою в time
        cutoff = self.cutoff_frequency.get()  # значення частоти з ползунка
        b, a = butter(4, cutoff, btype=self.filter_type.get(), fs=fs)
        return filtfilt(b, a, signal)

    def reset_parameters(self):
        self.amplitude.set(1.0)
        self.frequency.set(0.5)  # Частота встановлена на 0.5
        self.phase.set(0.0)
        self.noise_mean.set(0.0)
        self.noise_covariance.set(0.1)
        self.show_noise.set(False)
        self.cutoff_frequency.set(5.0)
        self.filter_type.set("lowpass")
        self.show_filtered_harmonic.set(False)
        self.update_plot()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
