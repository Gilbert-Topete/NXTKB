from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import xml.etree.ElementTree as ET
import json


#input_file = "report.xml"
#output_file = "test_output.json"

def kbArticleGenerator(input_file, output_file):
    template = """
    From the following service ticket discussion, can you create a knowledgebase article
    with its corresponding ticket number so we know where to place them?

    If you cannot generate a knowledgebase article because there's too little information to go off of, 
    you can safely ignore it.

    Please replace any names found with 'user'.

    Report: {service_ticket_report}
    """
    #Reads XML
    tree = ET.parse(input_file)
    xml_root = tree.getroot()
    service_ticket_root = xml_root[0][0]
    service_tickets = []
    service_ticket_reports = []

    #Gathers ticket numbers and their corresponding notes and places them in service_tickets
    for service_ticket in service_ticket_root:
        ticket_dict = {}
        ticket_dict['ticketNumber'] = service_ticket.get('TicketNbr')
        ticket_dict['ticketSummary'] = service_ticket.get('Summary')
        ticket_notes = []
        for notes in service_ticket[0][0][0]:
            ticket_notes.append(notes.get('Textbox112')) #'Textbox112' refers to each note added to a service ticket
        ticket_dict['ticketNotes'] = ticket_notes
        service_tickets.append(ticket_dict)

    #Stores ticket numbers and their corresponding ticket notes
    for ticket in service_tickets:
        service_ticket_report = ''''''
        service_ticket_report += f'Start of ticket number {ticket.get('ticketNumber')}...\n\n'
        service_ticket_report += f'Summary: {ticket.get('ticketSummary')}\n'
        service_ticket_report += 'Discussion notes: \n'
        for note in ticket.get('ticketNotes'):
            service_ticket_report += f'{note} \n'
        service_ticket_report += f"\nEnd of service ticket {ticket.get('ticketNumber')}...\n\n\n"
        service_ticket_reports.append(service_ticket_report)
        #print(service_ticket_report)


    model = OllamaLLM(model='llama3')
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    for i in range(len(service_ticket_reports)):
        kb_article = ''''''
        kb_article += chain.invoke({'service_ticket_report': service_ticket_reports[i]})
        kb_article += '\n\n\n\n'
        service_tickets[i]['kbArticle'] = kb_article
        del service_tickets[i]['ticketNotes'] #Removes notes from JSON, as we're only focused on the KB articles

    with open(output_file, "w") as json_file:
        json.dump(service_tickets, json_file, indent=4)

    print("KB article successfully generated!")
    return True

#kbArticleGenerator(input_file, output_file)