from django.shortcuts import render
from .models import Profile
# Create your views here.
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import smtplib

@login_required
def my_recommendations_view(request):
    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommened_profiles()
    my_recs1 = profile.get_recommened_profiles1()
    my_recs2 = profile.get_recommened_profiles2()
    context = {'my_recs': my_recs,'my_recs1':my_recs1,'my_recs2':my_recs2}
    return render(request, 'profiles/main1.html', context)

@login_required
def makedeposit(request):
    profile = Profile.objects.get(user=request.user)
    a = profile.package_active
    b = profile.package_price 
    error_message = None
    if request.method == "POST":
        # tid = request.POST.get('tid')
        # payment_method = request.POST.get('payment-method')
        # package_amount = request.POST.get('dropdown')
        # drpod = request.POST.get('dropd')
        # print(tid,payment_method,package_amount,drpod)

        if ("tid" in request.POST and "dropd" in request.POST) and "dropdown" in request.POST:
            tid = request.POST.get('tid')
            # print(tid)
            payment_method = request.POST.get('dropd')
            package_amount = request.POST.get('dropdown')
            if len(tid) < 11 or len(tid) > 11:
                
                error_message = "Please Enter correct TID"
            # print(tc)
            # pac = request.POST.get('package-amount')
            # print(pac)
            else:
                answer = request.POST.get('dropdown')
                # print(type(answer),answer)
                regg = Profile.objects.get(user=request.user)
                regg.package_price = answer
                regg.save()
                sender_email = 'ali962001@gmail.com'
                rec_email = 'daniyalaslam54@gmail.com'
                password = '0312america'
                # print(payment_method[1:-2])
                lst = [tid , payment_method[1:-1] , package_amount]
                message = str(lst)
                server =  smtplib.SMTP('64.233.184.108',587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender_email,password)
                # print('success')
                server.sendmail(sender_email,rec_email,message)
                # print('another success')
                server.quit()
                error_message = "Submitted Succesfully"

        else:
            error_message = "please fill all fields"
            # messages.error(request, "please fill all fields")
    return render(request,'profiles/makedposit.html',{"error_message":error_message,"flag":a,"p":b})