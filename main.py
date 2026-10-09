from campusflow.tickets import TicketCategory, Ticket, TicketUrgency

jakesticker = Ticket(id="1", title="Jakes Network", priority="very", category=TicketCategory.Network , urgency=TicketUrgency.Low,  affected_users=10, status="urgent", assigned_to="Monica")
mubarakticker = Ticket(id="2", title="Jakes Network", priority="very", category=TicketCategory.Software, urgency=TicketUrgency.High,  affected_users=10, status="urgent", assigned_to="Monica")

print(mubarakticker.urgency)
