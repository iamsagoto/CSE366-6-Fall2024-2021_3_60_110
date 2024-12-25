# agent.py
class Student:
    def __init__(self, student_id, availability, preference):
        self.id = student_id
        self.availability = availability
        self.preference = preference
        self.schedule = []

    def assign_class(self, time_slot, class_id):
        if time_slot in self.availability:
            self.schedule.append((time_slot, class_id))

    def clear_schedule(self):
        self.schedule = []
