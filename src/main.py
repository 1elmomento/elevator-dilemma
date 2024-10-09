from models.basic_model import BasicElevatorModel


def main():
    basic_model = BasicElevatorModel()
    basic_model.run()


if __name__ == "__main__":
    main()


# # import simpy
# # import numpy as np
# # import matplotlib.pyplot as plt

# # # Parameters
# # FLOORS = 10
# # SIMULATION_TIME = 300  # seconds
# # SERVICE_RATE = 0.1  # Average time an elevator takes to service one request (e.g., 10 passengers per second)

# # # Floor-specific arrival rates (passengers per second)
# # # Assume lower floors (e.g., lobby, ER) have higher arrival rates
# # arrival_rates = [0.3, 0.2, 0.15, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01, 0.005]


# # class HospitalElevatorSystem:
# #     def __init__(self, env, floors, arrival_rates):
# #         self.env = env
# #         self.floors = floors
# #         self.arrival_rates = arrival_rates
# #         self.queues = {
# #             floor: 0 for floor in range(floors)
# #         }  # Queue sizes for each floor
# #         self.waiting_times = {
# #             floor: [] for floor in range(floors)
# #         }  # Collect waiting times by floor

# #     def request_elevator(self, floor):
# #         # Passenger request on a floor
# #         self.queues[floor] += 1
# #         arrival_time = env.now
# #         service_time = np.random.exponential(1.0 / SERVICE_RATE)
# #         yield self.env.timeout(service_time)
# #         wait_time = env.now - arrival_time
# #         self.waiting_times[floor].append(wait_time)
# #         self.queues[floor] -= 1

# #     def passenger_arrival(self, floor):
# #         # Generate passengers according to Poisson process for this floor
# #         while True:
# #             inter_arrival_time = np.random.exponential(1.0 / self.arrival_rates[floor])
# #             yield self.env.timeout(inter_arrival_time)
# #             env.process(self.request_elevator(floor))


# # # Initialize simulation environment
# # env = simpy.Environment()

# # # Initialize hospital elevator system
# # elevator_system = HospitalElevatorSystem(env, FLOORS, arrival_rates)

# # # Start passenger arrival processes for each floor
# # for floor in range(FLOORS):
# #     env.process(elevator_system.passenger_arrival(floor))

# # # Run the simulation
# # env.run(until=SIMULATION_TIME)

# # # Analyze results: Average queue sizes and waiting times
# # average_queue_sizes = [
# #     np.mean(elevator_system.queues[floor]) for floor in range(FLOORS)
# # ]
# # average_waiting_times = [
# #     (
# #         np.mean(elevator_system.waiting_times[floor])
# #         if elevator_system.waiting_times[floor]
# #         else 0
# #     )
# #     for floor in range(FLOORS)
# # ]

# # # Plot average waiting times and queue sizes
# # floors = list(range(FLOORS))
# # plt.figure(figsize=(12, 6))

# # # Plotting average waiting times
# # plt.subplot(1, 2, 1)
# # plt.bar(floors, average_waiting_times, color="blue")
# # plt.title("Average Waiting Times by Floor")
# # plt.xlabel("Floor")
# # plt.ylabel("Average Waiting Time (seconds)")
# # plt.xticks(floors)

# # # Plotting average queue sizes
# # plt.subplot(1, 2, 2)
# # plt.bar(floors, average_queue_sizes, color="green")
# # plt.title("Average Queue Sizes by Floor")
# # plt.xlabel("Floor")
# # plt.ylabel("Average Queue Size")
# # plt.xticks(floors)

# # plt.tight_layout()
# # plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# import random

# # Constants
# NUM_FLOORS = 10  # 4 underground, 6 above
# ELEVATOR_CAPACITY = 10
# LAMBDA = 10  # Average arrival rate (people per minute)
# SIMULATION_TIME = 100  # Simulation runs for 100 minutes
# TRAVEL_TIME_PER_FLOOR = 2  # Time to move between adjacent floors
# STOP_TIME = 5  # Time spent stopping at each floor
# WRONG_BUTTON_PROB_INCREASE = 0.05  # Increase in wrong button probability as queue grows

# # Floor weights for arrivals (importance)
# floor_weights = {
#     0: 0.25,
#     1: 0.25,
#     2: 0.20,
#     3: 0.15,
#     4: 0.05,
#     5: 0.05,
#     6: 0.05,
#     -1: 0.01,
#     -2: 0.01,
#     -3: 0.01,
#     -4: 0.01,
# }

# # Normalize weights to sum to 1
# total_weight = sum(floor_weights.values())
# for floor in floor_weights:
#     floor_weights[floor] /= total_weight

# # Initialize queues for each floor
# queues = {floor: [] for floor in floor_weights}
# waiting_times = {floor: [] for floor in floor_weights}


# # Simulate arrivals based on Poisson distribution
# def simulate_arrivals():
#     arrivals = np.random.poisson(LAMBDA)
#     return arrivals


# # Assign people to floors based on weights
# def assign_arrival_floors(arrivals):
#     arrival_floors = np.random.choice(
#         list(floor_weights.keys()), size=arrivals, p=list(floor_weights.values())
#     )
#     return arrival_floors


# # Simulate elevator service time (including stops and travel between floors)
# def elevator_service_time(current_floor, destination_floors):
#     total_time = 0
#     for dest in destination_floors:
#         travel_time = abs(current_floor - dest) * TRAVEL_TIME_PER_FLOOR
#         total_time += travel_time + STOP_TIME
#         current_floor = dest  # Update the current floor of the elevator
#     return total_time


# # Main simulation loop
# def run_simulation():
#     elevators = [
#         {"current_floor": 0, "capacity": ELEVATOR_CAPACITY, "people": []}
#         for _ in range(2)
#     ]  # Two elevators

#     for minute in range(SIMULATION_TIME):
#         # Step 1: Simulate arrivals
#         arrivals = simulate_arrivals()
#         arrival_floors = assign_arrival_floors(arrivals)

#         # Add people to queues
#         for floor in arrival_floors:
#             # Simulate wrong button pressing as queue size grows
#             wrong_button_prob = min(1, WRONG_BUTTON_PROB_INCREASE * len(queues[floor]))
#             if random.random() < wrong_button_prob:
#                 # Press wrong button - randomly choose the wrong direction
#                 floor *= -1  # Reversing the sign to simulate wrong direction
#             queues[floor].append(minute)  # Add person to queue, record time of arrival

#         # Step 2: Serve the queues with the two elevators
#         for elevator in elevators:
#             if elevator["people"]:
#                 # Elevator is serving people, calculate service time
#                 destination_floors = [
#                     person["destination"] for person in elevator["people"]
#                 ]
#                 service_time = elevator_service_time(
#                     elevator["current_floor"], destination_floors
#                 )
#                 elevator["people"] = []  # After service, the elevator is empty

#             # Check floors for people waiting
#             for floor, queue in queues.items():
#                 if queue and len(elevator["people"]) < ELEVATOR_CAPACITY:
#                     # Pick up people from the floor
#                     pickup_count = min(
#                         ELEVATOR_CAPACITY - len(elevator["people"]), len(queue)
#                     )
#                     for _ in range(pickup_count):
#                         arrival_time = queue.pop(0)
#                         waiting_times[floor].append(
#                             minute - arrival_time
#                         )  # Calculate waiting time for this person
#                     elevator["current_floor"] = (
#                         floor  # Move the elevator to the pickup floor
#                     )

#         # Step 3: Update elevator state
#         for elevator in elevators:
#             if elevator["people"]:
#                 elevator["current_floor"] = elevator["people"][0][
#                     "destination"
#                 ]  # Update to next destination floor


# # Run the simulation
# run_simulation()


# # Plotting the results
# def plot_results():
#     avg_waiting_times = {
#         floor: np.mean(waiting_times[floor]) if waiting_times[floor] else 0
#         for floor in waiting_times
#     }
#     traffic_intensity = {floor: len(waiting_times[floor]) for floor in waiting_times}

#     # Plot waiting times
#     floors = list(avg_waiting_times.keys())
#     avg_times = list(avg_waiting_times.values())
#     traffic = list(traffic_intensity.values())

#     fig, ax1 = plt.subplots()

#     color = "tab:red"
#     ax1.set_xlabel("Floor")
#     ax1.set_ylabel("Average Waiting Time (minutes)", color=color)
#     ax1.bar(floors, avg_times, color=color)
#     ax1.tick_params(axis="y", labelcolor=color)

#     ax2 = ax1.twinx()
#     color = "tab:blue"
#     ax2.set_ylabel("Traffic Intensity (number of people served)", color=color)
#     ax2.plot(floors, traffic, color=color)
#     ax2.tick_params(axis="y", labelcolor=color)

#     plt.title("Average Waiting Time and Traffic Intensity by Floor")
#     fig.tight_layout()
#     plt.show()


# # Plot results
# plot_results()
