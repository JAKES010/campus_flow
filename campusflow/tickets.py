from enum import Enum


class Ticket:
    def __init__(self, id , title, category, urgency, affected_users, priority, status, assigned_to):
        self.id = id
        self.title = title
        self.category = category
        self.urgency = urgency
        self.affected_users = affected_users
        self.priority = priority
        self.status = status
        self.assigned_to = assigned_to

        

class TicketCategory(Enum):
    Network=1
    Hardware=2
    Software=3
    Other=4

        
