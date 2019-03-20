from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.exceptions import ObjectDoesNotExist



def mainMenu():
    response = "CON Welcome to Banking Ussd Portal \n"
    response += "1. Transfer Money \n"
    response += "2. Withdraw Money \n"
    response += "3. Deposit Money \n"
    response += "4. Account Balance \n"
    response += "00. End session"

    return response

@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        response = ""

        textArray = text.split('*')
        lastestInput = textArray[-1]
        
        #checking if it's a returning session or new session
        try:
            session = SessionLevel.objects.get(session_id = session_id)
            level = session.level

        except ObjectDoesNotExist:
            session = SessionLevel.objects.create(session_id=session_id,phone_number=phone_number)
            session.save()
            level = session.level
        
        #Checking if user is Registered
        bankUser = BankUser.objects.filter(phone_number=phone_number).first()
        if bankUser is not None:
            #bank account
            account = BankAccount.objects.get(bankUser=bankUser)

            if level == 0:
                if lastestInput == "":
                    response = mainMenu()

                elif lastestInput == "1":
                    response = "CON  How much do you want to transfer \n"
                    session.level = 5
                    session.save()
                
                elif lastestInput == "2":
                    response = "CON How much do you want to withdraw \n"
                    session.level = 5
                    session.save()
                
                elif lastestInput == "3":
                    response = "CON Input agent's number is none use default 250 \n"
                    session.level = 7
                    session.save()

                elif lastestInput == "4":
                    response = "CON Account your account balance \n"
                    response += str(account.balance) + " RWF \n"
                    response += "99. Back to the main menu \n"
                    response += "00. End session"

                elif lastestInput == "00":
                    response = "END Thanks for using this Ussd Banking Portal"

                else:
                    response = mainMenu()

            elif level == 5:
                try:
                    amount = int(lastestInput)

                    if (amount > account.balance):
                        response = "CON You only have "+str(account.balance)+" Enter valid funds"
                    else:
                        response = "CON Enter Recipient's Number +2507*** \n"
                        session.level = 6
                        session.save()

                except ValueError:
                    response = "CON Enter Valid Amount"

            elif level == 6:
                #level to make transaction
                receiver = textArray[len(textArray)-1]
                amount = int(textArray[len(textArray)-2])
                account.balance -= amount
                account.save() 
                transaction = BankTransaction.objects.create(From=bankUser,To=receiver,Amount=amount)
                transaction.save()

                response = "END You have successfully sent "+str(amount) + " to "+str(receiver)

            elif level == 7:
                try:
                    agentCode = int(lastestInput)

                    if agentCode == 250:
                        session.level = 8
                        session.save()
                        response = "CON How much do you wish to deposit \n"
                    
                    else:
                        response = "CON No such agent code try another or use 250"

                except ValueError:
                    response = "CON Input valid agent's number is none use default 250 \n"
            
            elif level == 8:
                try:
                    amount = int(lastestInput)
                    
                    if amount <= 0:
                        response = "CON "+ lastestInput + " is not valid deposit \n"
                        response += "Enter valid Deposit"

                    else:
                        agent = BankUser.objects.get(phone_number=250)

                        if agent is None:
                            response = "END Agent doesn't Exist"

                        else:
                            agentAccount = BankAccount.objects.get(bankUser=agent)
                            transaction = BankTransaction.objects.create(From=agent,To=phone_number,Amount=amount)
                            transaction.save()

                            agentAccount.balance -= amount
                            agentAccount.save()

                            account.balance += amount
                            account.save()

                            print("*** successfully ended")

                            response = "END successfully deposit " + lastestInput +" \n New Balance is "+ str(account.balance) 

                except ValueError:
                    response = "CON Enter valid amount to deposit "+lastestInput +" \n"


        else:
            #save new user
            print(" User ntawuhari")
            response = "END still working on saving new user"


        return HttpResponse(response)
