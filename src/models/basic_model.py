import numpy as np
import matplotlib.pyplot as plt


class BasicElevatorModel:
    def __init__(self) -> None:
        self.arrival_rate = 10
        self.stoppage = 1
        self.service_rate = 2
        self.num_floors = 11
        self.num_channels = 2
        self.capacity = 10
        self.simulation_time = 720
        self.wrong_button_prob = 0.7

    def calculate_floor_weights(self):
        """Calculates the weights of traffic intensity for each floor."""
        floor_weights = {
            0: 0.25,
            1: 0.25,
            2: 0.25,
            3: 0.20,  # MZ floor in the building
            4: 0.15,
            5: 0.05,
            6: 0.05,
            -1: 0.01,
            -2: 0.01,
            -3: 0.01,
            -4: 0.01,
        }

        total_weights = sum(floor_weights.values())
        for floor in floor_weights:
            floor_weights[floor] /= total_weights

        return floor_weights

    def simulate_arrivals(self):
        """Simulate the arrivals of people to each floor using Poisson distribution."""
        floor_weights = self.calculate_floor_weights()
        arrival_rates = {
            floor: weight * self.arrival_rate for floor, weight in floor_weights.items()
        }
        arrivals_per_floor = {}

        for floor, rate in arrival_rates.items():
            arrivals_per_floor[floor] = np.random.poisson(rate)

        return arrivals_per_floor

    def handle_wrong_button_press(self, floor):
        """
        Simulate the scenario where a person presses the wrong button.
        If a person presses the wrong button, they effectively increase the queue size for that floor.
        """
        if np.random.rand() < self.wrong_button_prob:
            # Person pressed the wrong button, they cause a delay by waiting longer
            # This delay could be reflected by increasing their waiting time or blocking the elevator
            return (
                1  # Adding an extra person to the queue (simulating the inefficiency)
            )
        return 0

    def calculate_floor_traffic_intensity(self):
        """Simulates and calculates the total and average traffic intensity for all floors over the entire simulation period."""
        total_traffic_intensity = {floor: 0 for floor in range(-4, 7)}

        for minute in range(self.simulation_time):
            arrivals = self.simulate_arrivals()

            for floor, arrival_rate in arrivals.items():
                floor_traffic_intensity = arrival_rate / (
                    self.num_channels * self.service_rate
                )
                total_traffic_intensity[floor] += floor_traffic_intensity

        avg_traffic_intensity = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity.items()
        }

        return avg_traffic_intensity

    def calculate_floor_traffic_intensity_with_wrong_button(self):
        """Simulates and calculates the total and average traffic intensity for all floors over the entire simulation period."""
        total_traffic_intensity = {floor: 0 for floor in range(-4, 7)}

        for minute in range(self.simulation_time):
            arrivals = self.simulate_arrivals()

            for floor, arrival_rate in arrivals.items():
                wrong_button_effect = sum(
                    self.handle_wrong_button_press(floor) for _ in range(arrival_rate)
                )

                floor_traffic_intensity = (arrival_rate + wrong_button_effect) / (
                    self.num_channels * self.service_rate
                )
                total_traffic_intensity[floor] += floor_traffic_intensity

        avg_traffic_intensity = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity.items()
        }

        return avg_traffic_intensity

    def calculate_floor_traffic_intensity_modified(self):
        """Simulates and calculates the total and average traffic intensity for all floors over the entire simulation period,
        factoring in wrong button presses."""
        total_traffic_intensity = {floor: 0 for floor in range(-4, 7)}

        for minute in range(self.simulation_time):
            arrivals = self.simulate_arrivals()

            for floor, arrival_rate in arrivals.items():

                wrong_button_effect = sum(
                    self.handle_wrong_button_press(floor) for _ in range(arrival_rate)
                )

                # Effective service rate decreases as wrong button presses increase
                # We introduce an inefficiency factor that reduces the effective service rate
                inefficiency_factor = 1 + (wrong_button_effect / max(arrival_rate, 1))

                # Adjusted service rate due to wrong button press inefficiency
                adjusted_service_rate = self.service_rate / inefficiency_factor

                # Calculate traffic intensity with the adjusted service rate
                floor_traffic_intensity = (arrival_rate + wrong_button_effect) / (
                    self.num_channels * adjusted_service_rate
                )
                total_traffic_intensity[floor] += floor_traffic_intensity

        avg_traffic_intensity = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity.items()
        }

        return avg_traffic_intensity

    def generate_direction_probabilities(self):
        """Generate probabilities for up/down movement based on floor position."""
        probs = {}
        for floor in range(-4, 7):
            if floor == 6:
                probs[floor] = 0.0
            elif floor == -4:
                probs[floor] = 1.0
            else:
                probs[floor] = 1 - (floor + 4) / 10
        return probs

    def calculate_and_plot_floor_traffic_intensity_separated(self):
        """Calculate traffic intensity with separate queues for up and down on each floor and plot the results."""
        total_traffic_intensity_up = {floor: 0 for floor in range(-4, 7)}
        total_traffic_intensity_down = {floor: 0 for floor in range(-4, 7)}

        direction_probs = self.generate_direction_probabilities()

        for minute in range(self.simulation_time):
            arrivals = self.simulate_arrivals()

            for floor, arrival_rate in arrivals.items():

                prob_up = direction_probs[floor]
                arrivals_up = np.random.binomial(arrival_rate, prob_up)
                arrivals_down = arrival_rate - arrivals_up

                if floor < 6:
                    floor_traffic_intensity_up = arrivals_up / self.service_rate
                    total_traffic_intensity_up[floor] += floor_traffic_intensity_up

                if floor > -4:
                    floor_traffic_intensity_down = arrivals_down / self.service_rate
                    total_traffic_intensity_down[floor] += floor_traffic_intensity_down

        avg_traffic_intensity_up = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity_up.items()
        }
        avg_traffic_intensity_down = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity_down.items()
        }

        floors = list(range(-4, 7))
        intensities_up = [avg_traffic_intensity_up[floor] for floor in floors]
        intensities_down = [avg_traffic_intensity_down[floor] for floor in floors]

        plt.figure(figsize=(12, 6))

        plt.bar(
            [x - 0.2 for x in floors],
            intensities_up,
            width=0.4,
            label="Up Queue",
            color="#FABC3F",
            alpha=0.7,
        )

        plt.bar(
            [x + 0.2 for x in floors],
            intensities_down,
            width=0.4,
            label="Down Queue",
            color="#E85C0D",
            alpha=0.7,
        )

        plt.xlabel("Floor")
        plt.ylabel("Average Traffic Intensity")
        plt.title("Average Traffic Intensity per Floor (Separated Up/Down Queues)")
        plt.xticks(floors)
        plt.legend()
        plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
        plt.savefig("plots/solution_separated.png", dpi=500)
        plt.close("all")

    def calculate_and_plot_floor_traffic_intensity_poisson(self):
        """Calculate traffic intensity with separate queues for up and down on each floor, using correct arrival rates."""
        total_traffic_intensity_up = {floor: 0 for floor in range(-4, 7)}
        total_traffic_intensity_down = {floor: 0 for floor in range(-4, 7)}
        total_traffic_intensity_combined = {floor: 0 for floor in range(-4, 7)}

        direction_probs = self.generate_direction_probabilities()

        for minute in range(self.simulation_time):
            arrivals = self.simulate_arrivals()

            for floor, arrival_rate in arrivals.items():

                prob_up = direction_probs[floor]
                arrivals_up = np.random.binomial(arrival_rate, prob_up)
                arrivals_down = arrival_rate - arrivals_up

                if floor < 6:
                    floor_traffic_intensity_up = arrivals_up / self.service_rate
                    total_traffic_intensity_up[floor] += floor_traffic_intensity_up

                if floor > -4:
                    floor_traffic_intensity_down = arrivals_down / self.service_rate
                    total_traffic_intensity_down[floor] += floor_traffic_intensity_down

                floor_traffic_intensity = arrival_rate / self.service_rate
                total_traffic_intensity_combined[floor] += floor_traffic_intensity

        avg_traffic_intensity_up = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity_up.items()
        }
        avg_traffic_intensity_down = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity_down.items()
        }
        avg_traffic_intensity_combined = {
            floor: total / self.simulation_time
            for floor, total in total_traffic_intensity_combined.items()
        }

        floors = list(range(-4, 7))
        intensities_up = [avg_traffic_intensity_up[floor] for floor in floors]
        intensities_down = [avg_traffic_intensity_down[floor] for floor in floors]
        intensities_combined = [
            avg_traffic_intensity_combined[floor] for floor in floors
        ]

        plt.figure(figsize=(12, 6))

        plt.bar(
            [x - 0.2 for x in floors],
            intensities_up,
            width=0.2,
            label="Up Queue",
            color="#FABC3F",
            alpha=0.7,
        )

        plt.bar(
            [x for x in floors],
            intensities_down,
            width=0.2,
            label="Down Queue",
            color="#E85C0D",
            alpha=0.7,
        )

        plt.bar(
            [x + 0.2 for x in floors],
            intensities_combined,
            width=0.2,
            label="Combined (Original)",
            color="#4CAF50",
            alpha=0.7,
        )

        plt.xlabel("Floor")
        plt.ylabel("Average Traffic Intensity")
        plt.title("Average Traffic Intensity per Floor (Corrected Model)")
        plt.xticks(floors)
        plt.legend()
        plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
        plt.savefig("plots/solution_poisson.png", dpi=500)
        plt.close("all")

    def plot_traffic_intensities_without_wrong_button(self):
        traffic_intensisties = self.calculate_floor_traffic_intensity()
        floors = list(traffic_intensisties.keys())
        intensities = list(traffic_intensisties.values())

        plt.figure(figsize=(12, 6))
        plt.bar(
            floors,
            intensities,
            width=0.6,
            label="Traffic Intensity",
            color="#FABC3F",
            alpha=0.7,
        )

        plt.xlabel("Floor")
        plt.ylabel("Traffic Intensity")
        plt.title(
            "Floors Average Traffic Intensities without pressing the wrong button"
        )
        plt.xticks(floors)
        plt.legend()
        plt.grid(linestyle="--", linewidth=0.5, alpha=0.9)
        plt.savefig("plots/traffic_intensity_without_wrong_button.png", dpi=400)
        plt.close("all")

    def plot_traffic_intensities_with_wrong_button_effect_1(self):
        traffic_intensities_without_wrong = self.calculate_floor_traffic_intensity()
        traffic_intensities_with_wrong = (
            self.calculate_floor_traffic_intensity_with_wrong_button()
        )

        floors = list(traffic_intensities_with_wrong.keys())
        intensites_1 = list(traffic_intensities_without_wrong.values())
        intensites_2 = list(traffic_intensities_with_wrong.values())

        plt.figure(figsize=(12, 6))

        plt.bar(
            [x - 0.2 for x in floors],
            intensites_1,
            width=0.4,
            label="Traffic Intensity without Wrong Button Effect",
            color="#FABC3F",
            alpha=0.7,
        )

        plt.bar(
            [x + 0.2 for x in floors],
            intensites_2,
            width=0.4,
            label="Traffic Intensity with Wrong Button Effect",
            color="#E85C0D",
            alpha=0.7,
        )

        plt.title("Comparing Traffic Intensity w/ and w/o Wrong Button Effect")
        plt.xlabel("Floor")
        plt.ylabel("Traffic Intensity")
        plt.xticks(floors)
        plt.grid(linestyle="--", linewidth=0.5, alpha=0.9)
        plt.legend()
        plt.savefig("plots/comparison_wbe_approach1.png", dpi=500)
        plt.close("all")

    def plot_traffic_intensities_with_wrong_button_effect_2(self):
        traffic_intensities_without_wrong = self.calculate_floor_traffic_intensity()
        traffic_intensities_with_wrong = (
            self.calculate_floor_traffic_intensity_with_wrong_button()
        )
        traffic_intnsities_with_wrong_2 = (
            self.calculate_floor_traffic_intensity_modified()
        )

        floors = list(traffic_intensities_with_wrong.keys())
        intensities_1 = list(traffic_intensities_without_wrong.values())
        intensities_2 = list(traffic_intensities_with_wrong.values())
        intensities_3 = list(traffic_intnsities_with_wrong_2.values())

        plt.figure(figsize=(12, 6))

        plt.bar(
            [x - 0.2 for x in floors],
            intensities_1,
            width=0.2,
            label="Without Wrong Button Press",
            color="#FABC3F",
            alpha=0.7,
        )

        plt.bar(
            [x for x in floors],
            intensities_2,
            width=0.2,
            label="With Wrong Button Press Approach 1",
            color="#E85C0D",
            alpha=0.7,
        )

        plt.bar(
            [x + 0.2 for x in floors],
            intensities_3,
            width=0.2,
            label="With Wrong Button Press Approach 2",
            color="#C7253E",
            alpha=0.7,
        )

        plt.title("Comparison of Traffic Inetnsity per floor")
        plt.xlabel("Floor")
        plt.ylabel("Traffic Intensity")
        plt.xticks(floors)
        plt.grid(linestyle="--", linewidth=0.5, alpha=0.9)
        plt.legend()
        plt.savefig("plots/three_bars.png", dpi=500)
        plt.close("all")

    def run(self):
        """Run the simulation and print results."""
        # self.plot_traffic_intensities_without_wrong_button()
        # self.plot_traffic_intensities_with_wrong_button_effect_1()
        # self.plot_traffic_intensities_with_wrong_button_effect_2()
        # self.calculate_and_plot_floor_traffic_intensity_separated()
        self.calculate_and_plot_floor_traffic_intensity_poisson()
