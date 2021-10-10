import json
import smtplib
import random
import argparse

# Added to .gitignore to avoid putting this on the internet
with open("secure_santa_settings.json") as f:
    settingsD = json.load(f)
    person_to_emailD = settingsD["personToEmail"]
    login_username = sender_email = settingsD["senderEmail"]
    password = settingsD["senderPassword"]
    christmas_list_link = settingsD["christmasListLink"]
    last_year_santa_mapping = settingsD["lastYearsSantas"] # This is added to the exclude list (separated for ease of  use)
    santa_to_excludeL_map = settingsD["santaToExcludeList"]

for santa_name, receiver_name in last_year_santa_mapping.items():
    santa_to_excludeL_map[santa_name].append(receiver_name)

# Convert exclude lists to a set (to speed things up [maybe?])
for santa_name, excludeL in santa_to_excludeL_map.items():
    santa_to_excludeL_map[santa_name] = set(excludeL)

email_message_template = """\
From: {sender_email}
To: {recipient}
Subject: Your Secret Santa!!

Hi {santas_name},

This is an automated email to tell you who you are the secret santa for.  You are the secret santa for...

{recievers_name}

The christmas spreadsheat is available through the following link:

{christmas_list_link}

Please fill out your address and the presents you want and once you buy a gift for someone add an entry in the tab with the recipient's name on it to let people know that you've bought that gift.  

Merry Christmas!!
"""

def connect_to_email_server():
    conn = smtplib.SMTP(host='smtp.gmail.com', port=587)
    
    conn.starttls()
    conn.ehlo()
    conn.login(login_username, password)
    
    return conn

def send_email(conn, sender_email, recipientL, message_str):
    return conn.sendmail(sender_email, recipientL, message_str)

def build_sender_reciever_list():
    """ This function generates the list of santa's by brute force: retrying if it's random config doesn't match the constraints """
    # random.seed("2020ChristmasSecretSanta") # Seed the random generator in case we need to retrieve the list of secret santas later
    random.seed("2021ChristmasSecretSanta") # Seed the random generator in case we need to retrieve the list of secret santas later
    
    found_pairings = False
    santa_to_person_mapping = {}
    for _ in range(10):
        people_without_santas = list(santa_to_excludeL_map.keys())
        santas_without_people = list(santa_to_excludeL_map.keys())
        santa_to_person_mapping = {}
        
        for _ in range(len(people_without_santas)):
            santa = person = None
            for i in range(10): # 10 tries
                person = random.choice(people_without_santas)
                santa = random.choice(santas_without_people)
                
                if santa != person and person not in santa_to_excludeL_map[santa]:
                    santa_to_person_mapping[santa] = person
                    people_without_santas.remove(person)
                    santas_without_people.remove(santa)
                    break
            
            if not santa:
                break
        
        if len(santa_to_person_mapping) == len(santa_to_excludeL_map):
            found_pairings = True
            break
    
    if found_pairings:
        return santa_to_person_mapping
    else:
        raise Exception("Could not find pairing!!!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Secret Santa Email Sender.')
    parser.add_argument('--dry-run',  action='store_true', help="Don't send the emails.  Just print the contents of the emails.  ")
    parser.add_argument('--print-emails',  action='store_true', help="Print the contents of the emails")
    parser.add_argument('--confirm',  action='store_true', help='Confirm email sending')
    args = parser.parse_args()

    santa_to_person_mapping = build_sender_reciever_list()
    
    # Print the mapping
    santa_mapping = {}
    for santas_name, reciever_name in santa_to_person_mapping.items():
        santa_mapping[santas_name] = reciever_name
        print("%s has %s" % (santas_name, reciever_name))
    # print(json.dumps(santa_mapping, indent=4))

    if not args.confirm:
        if input("Does this look ok? ").lower().strip() != "y":
            print("Exiting")
            exit()

    if not args.dry_run:
        conn = connect_to_email_server()
    
    sender_email_str = 'Santa Claus <%s>' % sender_email
    for santas_name, reciever_name in santa_to_person_mapping.items():
        recipientL = [ person_to_emailD[santas_name] ]
        message_str = email_message_template.format(sender_email=sender_email_str, recipient=", ".join(recipientL), santas_name=santas_name, recievers_name=reciever_name, christmas_list_link=christmas_list_link)
        if args.print_emails:
            print("-"*80)
            print(message_str)
        if not args.dry_run:
            print(send_email(conn, sender_email_str, recipientL, message_str))
