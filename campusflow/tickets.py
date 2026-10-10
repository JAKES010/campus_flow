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
    
    def validate_title(value):
        if not isinstance(value, str):
            raise ValueError("title must be a string")

        title = value.strip()
        if not title:  
            raise ValueError("title must not be blank")

        return title

    def validate_affected_users(value):
        if isinstance(value, bool):
            raise ValueError("affected_users must be a positive integer")

        if isinstance(value, int):
            number = value
        elif isinstance(value, str):
            text = value.strip()
            if not text.isdigit(): 
                raise ValueError("affected_users must be a positive integer")
            number = int(text)
        else:
            raise ValueError("affected_users must be a positive integer")

        if number <= 0:
            raise ValueError("affected_users must be greater than zero")

        return number



class TicketCategory(Enum):
    Network=1
    Hardware=2
    Software=3
    Other=4

class TicketUrgency(Enum):
     Low=1
     Medium=2
     High=3

        
