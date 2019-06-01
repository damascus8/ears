from twilio.rest import Client


def sendMessage(link):
    location = "Pune-1"
    City = "mumbai"
    allContact = ["+919970116612", "+917218386138"]
    account_sid = "ACff214dceea622fbd0f54cde1e2afc542"
    auth_token = "443b8949cc31d3e9af267f549b09d64c"
    client = Client(account_sid, auth_token)
    # for contact in allContact:
    if location == "Pune-1":
        contact = "+919970116612"
    elif location == "Pune-2":
        contact = "+917218386138"
    else:
        contact = "+919359110403"
    message = client.messages.create(
        body="Accident has been occurred at " + location + ", Need Help!\n Click to see accident video " + link,
        to=contact, from_="+17609744184")
    print("Message sent to " + contact)
# for sms in client.messages.list():
#    print(sms.to)
