import csv
import re
from collections import defaultdict
from pprint import pprint

def format_phone(phone):
    pattern = r'(\+7|8)?[\s\-]?\(?(\d{3})\)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})(\s?доб\.\s?\d{4})?'
    match = re.match(pattern, phone)
    if match:
        groups = match.groups()
        formatted_phone = f"+7({groups[1]}){groups[2]}-{groups[3]}-{groups[4]}"
        if groups[5]:
            formatted_phone += f" доб.{groups[5].split()[-1]}"
        return formatted_phone
    return phone

def normalize_contact(contact):
    lastname = contact[0].strip()
    firstname = contact[1].strip()
    surname = contact[2].strip()
    if not firstname or not surname:
        name_parts = lastname.split() + firstname.split()
        if len(name_parts) == 3:
            lastname, firstname, surname = name_parts
        elif len(name_parts) == 2:
            lastname, firstname = name_parts
            surname = ""
        elif len(name_parts) == 1:
            firstname = ""
            surname = ""

    phone = format_phone(contact[5])

    return [lastname, firstname, surname, contact[3], contact[4], phone, contact[6]]

def merge_contacts(contacts):
    merged_contacts = defaultdict(lambda: ["", "", "", "", "", "", ""])
    for contact in contacts:
        normalized_contact = normalize_contact(contact)
        key = (normalized_contact[0], normalized_contact[1],
               normalized_contact[2])
        for i, value in enumerate(normalized_contact):
            if not merged_contacts[key][i]:
                merged_contacts[key][i] = value
            elif i == 6 and value and merged_contacts[key][i] != value:
                merged_contacts[key][i] += f", {value}"
    return list(merged_contacts.values())

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
contacts_list = contacts_list[1:]
contacts_list = merge_contacts(contacts_list)
contacts_list.insert(0, header)

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

pprint(contacts_list)