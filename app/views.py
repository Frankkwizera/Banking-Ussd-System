from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        response = ""

        print(text)
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
                    response = "CON Welcome to Banking Ussd Portal \n"
                    response += "1. Transfer Money \n"
                    response += "2. Withdraw Money \n"
                    response += "3. Deposit Money \n"
                    response += "4. Account Balance \n"
                    response += "00. End session"

                elif lastestInput == "1":
                    response = "CON  How much do you want to transfer \n"
                    session.level = 5
                    session.save()
                
                elif lastestInput == "2":
                    response = "CON How much do you want to withdraw \n"
                    session.level = 5
                    session.save()
                    
                elif lastestInput == "4":
                    response = "CON Account your account balance \n"
                    response += str(account.balance) + " RWF \n"
                    response += "99. Back to the main menu \n"
                    response += "00. End session"

                elif lastestInput == "00":
                    response = "END Thanks for using this Ussd Banking Portal"

                else:
                    response = "CON Welcome to Banking Ussd Portal \n"
                    response += "1. Transfer Money \n"
                    response += "2. Withdraw Money \n"
                    response += "3. Deposit Money \n"
                    response += "4. Account Balance \n"
                    response += "00. End session"

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
                    session.level = 5
                    session.save()
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
            
            #elif level == 7:
                #try:


        else:
            #save new user
            print(" User ntawuhari")
            response = "END still working on saving new user"


        return HttpResponse(response)
