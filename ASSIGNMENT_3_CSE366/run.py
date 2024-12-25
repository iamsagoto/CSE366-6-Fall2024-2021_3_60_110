# run.py
from environment import Environment
from agent import Student
import random

def fitness(schedule, students):
    conflict_penalty = 0
    preference_penalty = 0

    for time_slot, classes in enumerate(schedule):
        for class_id, student_id in enumerate(classes):
            if student_id >= len(students):
                continue  # Skip invalid student IDs
            student = students[student_id]
            if time_slot not in student.availability:
                conflict_penalty += 1
            if time_slot not in student.preference:
                preference_penalty += 1 / (student.preference.count(time_slot) + 1)

    return conflict_penalty + preference_penalty

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(schedule):
    time_slot = random.randint(0, len(schedule) - 1)
    class_id = random.randint(0, len(schedule[time_slot]) - 1)
    if random.random() < 0.1:  # Mutation rate set to 0.1
        schedule[time_slot][class_id] = random.randint(0, len(schedule[time_slot]) - 1)

def main():
    num_classes = 6
    num_students = 6
    time_slots = 5

    students = [
        Student(
            i,
            random.sample(range(time_slots), random.randint(2, time_slots)),
            random.sample(range(time_slots), random.randint(2, time_slots)),
        )
        for i in range(num_students)
    ]

    env = Environment(num_classes, num_students, time_slots)

    max_fitness = float("inf")
    for generation in range(100):  # Number of generations set to 100
        fitness_scores = [(fitness(schedule, students), schedule) for schedule in env.population]
        fitness_scores.sort(key=lambda x: x[0])

        best_fitness = fitness_scores[0][0]
        max_fitness = min(max_fitness, best_fitness)
        print(f"Generation {generation}: Best Fitness = {best_fitness}")
        print(f"Population size: {len(env.population)}")

        env.visualize_schedule(fitness_scores[0][1], generation, best_fitness, max_fitness)

        new_population = []
        for _ in range(len(env.population) // 2):
            parent1 = random.choice(fitness_scores[:20])[1]
            parent2 = random.choice(fitness_scores[:20])[1]
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        while len(new_population) < len(env.population):
            new_population.append(env.generate_population(1)[0])

        env.population = new_population

if __name__ == "__main__":
    main()
