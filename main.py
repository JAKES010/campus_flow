from campusflow.tickets import TicketCategory, Ticket

jakesticker = Ticket(id="1", title="Jakes Network", priority="very", category=TicketCategory.Network , urgency="critical",  affected_users=10, status="urgent", assigned_to="Monica")
mubarakticker = Ticket(id="2", title="Jakes Network", priority="very", category=TicketCategory.Software, urgency="critical",  affected_users=10, status="urgent", assigned_to="Monica")

print(mubarakticker.id)
