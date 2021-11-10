
from datetime import date
from django.shortcuts import render,redirect
from profiles.models import Profile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from profiles.forms import SignupForm
from profiles.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import smtplib
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Userw = User.objects.all().values()
# a = Profile.objects.all().values()
# print(Userw)
# x = Userw.objects.get(id=2)
# x = list(users.objects.filter(id=2).values())
# for i in x:
#     print(i)

def update_user_data(user):
    Profile.objects.update_or_create(user=user, defaults={'mob': user.profile.mob})

def login_view(request):
    error_message = None
    form = AuthenticationForm()
    
    if request.user.is_authenticated:
       
    
        return redirect('main-view')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username,password)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            today = date.today()
            profile1 = Profile.objects.get(user=request.user)
            profile1.get_date = today
            profile1.save()
            if request.GET.get('next'):
                # today = date.today()
                # profile1 = Profile.objects.get(user=request.user)
                # profile1.get_date = today
                # profile1.save()
                return redirect(request.GET.get('next'))
            else:
                return redirect('main-view')
        else:
            error_message = "Something Went wrong \n Create Account or retry "


    return render(request,'login.html',{'form':form,'error_message':error_message})


def logout_view(request):
    logout(request)
    return redirect('main-view')


pro = None

def signup_view(request):
    global pro
    pro = request.session.get('ref_profile')
    profile_id = request.session.get('ref_profile')
    # print('profile_id',profile_id)
    form = SignupForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('main-view')
    elif form.is_valid():
        if profile_id is not None:
            print("i ame here")
            recommended_by_profile = Profile.objects.get(id = profile_id) 
             
            ree = Profile.objects.filter(id=profile_id).values()
            x = list(ree[0].values())
            print(x,"print idhar------------------------------------------------------")
            # pack = Profile.objects.get(
            # print(recommended_by_profile,pack)
            instance = form.save()
            # instance.refresh_from_db()
            # newly added
            instance.profile.mob = form.cleaned_data.get('mob')
            update_user_data(instance)
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Profile.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            if x[4] is  None:
                registered_profile.save()
            else:
                recommended_by_profile1 = Profile.objects.get(id = x[4])
                registered_profile.recommended_by1 = recommended_by_profile1.user
                registered_profile.save()
            
            if x[5] is None:
                pass
            else:
                recommended_by_profile2 = Profile.objects.get(id = x[5])
                registered_profile.recommended_by2 = recommended_by_profile2.user
                registered_profile.save()
                messages.success(request, "Registered successfully")

                return redirect('main-view')
            messages.success(request, "Registered successfully")
            return redirect('main-view')     
            
        else:
            form.save()
            messages.success(request, "Registered successfully")
            return redirect('main-view')

    context = {'form':form}
    return render(request,'signup.html',context)

def main_view(request, **kwargs):
    code = str(kwargs.get('ref_code'))  
    if len(code) < 7:
        return render(request,'main.html')
    else:
        if len(code) > 7: 
            x = code
            profile = Profile.objects.get(code=x)
            request.session['ref_profile'] = profile.id
            return render(request,'main.html')
        
        elif request.user.is_authenticated:
            profilee = Profile.objects.get(user=request.user)
            aa = profilee.oneorzero
            cc = profilee.get_date
            cx = profilee.get_date2
            today = date.today()
            if str(today) == profilee.get_date:
                if profilee.get_date != profilee.get_date2:
                    profilee.oneorzero = 0
                    profilee.get_date2 = profilee.get_date
                    profilee.save()
            elif str(today) != profilee.get_date:
                profilee.get_date = str(today)
                profilee.oneorzero = 0
                profilee.get_date2 = profilee.get_date
                profilee.save()
                # print('id',profile.id)
            x = {"variable":earning_from_referral(request),"variab":earning_from_referral1(request),"vari": earning_from_referral2(request),
                "ad":10 - profilee.oneorzero ,"money":profilee.earn_from_ads}
            return render(request,'main.html',x)

        

    # else:
    #     return render(request,'main.html')

def earning_from_referral(request):
    # if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.package_active:
            my_recs = profile.get_recommened_profiles()
            # my_recs1 = profile.get_recommened_profiles1()
            # my_recs2 = profile.get_recommened_profiles2()

            a = 0
            for i in my_recs:
                if i.package_active and i.onee:
                # print(i.package_price,"ccc")
                    a += (int(i.package_price)/100)*10
                else:
                    pass
                # x = x + 0
           
            # context = {'my_recs': my_recs,'my_recs1':my_recs1,'my_recs2':my_recs2}
            return a#,my_recs1,my_recs2

        s = 0.0
        return s

def earning_from_referral1(request):
    # if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.package_active:
            # my_recs = profile.get_recommened_profiles()
            my_recs1 = profile.get_recommened_profiles1()
            # my_recs2 = profile.get_recommened_profiles2()
            a = 0
            for i in my_recs1:
                if i.package_active and i.twoo:
                # print(i.package_price,"ccc")
                    a += (int(i.package_price)/100)*5
                else:
                    pass
                # x = x + 0
           
            # context = {'my_recs': my_recs,'my_recs1':my_recs1,'my_recs2':my_recs2}
            return a#,my_recs1,my_recs2

        s = 0.0
        return s

def earning_from_referral2(request):
    # if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.package_active:
            # my_recs = profile.get_recommened_profiles()
            # my_recs1 = profile.get_recommened_profiles1()
            my_recs2 = profile.get_recommened_profiles2()

            a = 0
            for i in my_recs2:
                if i.package_active and i.threee:
                    a += (int(i.package_price)/100)*2.5
                else:
                    pass
            # context = {'my_recs': my_recs,'my_recs1':my_recs1,'my_recs2':my_recs2}
            return a#,my_recs1,my_recs2
        s = 0.0
        return s

def adds(request):
    xx = Profile.objects.get(user=request.user)
    z = xx.package_active
    a = xx.oneorzero < 10
    zzz = xx.package_price


    if request.method == "POST":
        zz = int(xx.oneorzero)+1
        xx.oneorzero = zz
        if zzz == 1000:
            print("iam ")
            xx.earn_from_ads = xx.earn_from_ads + 3
            xx.save()
            return redirect('main-view')
        elif zzz == 500:
            xx.earn_from_ads = xx.earn_from_ads + 1.5
            xx.save()
            return redirect('main-view')
        elif zzz == 250:
            xx.earn_from_ads = xx.earn_from_ads + 0.75
            xx.save()
            return redirect('main-view')
        

        
        # return redirect('main-view')
    return render(request,'daily-ads.html',{"package":z,"ads":a})
        


# def aaa(request):
#     xx = Profile.objects.get(user=request.user)
#     z = xx.package_active
#     a = xx.oneorzero < 10

#     if request.method == "POST":
#         zz = int(a)+1
#         xx.oneorzero = zz
#         xx.save()
#         return redirect('main-view')
#     return render(request,'da.html',{"package":z,"ads":a})

@login_required
def withdraw(request):
    flag = None
    use = Profile.objects.get(user=request.user)
    from_ads = use.earn_from_ads
    from_first = earning_from_referral(request)
    from_second = earning_from_referral1(request)
    from_third = earning_from_referral2(request)
    total = from_ads + from_first + from_second + from_third +1000
    price = use.package_price
    if use.package_price == 1000 and total >= 1000:
        flag = True
    elif use.package_price == 500 and total >= 500:
        flag = True
    elif use.package_price == 250 and total > 250:
        flag = True

    if request.method == "POST":
        if ("name" in request.POST and "dropd" in request.POST) and "number" in request.POST:
            payment_method = request.POST.get('dropd')
            acc_name = request.POST.get('name')
            acc_no =  request.POST.get('number')
            print(payment_method,acc_name,acc_no)
            # sender_email = 'ali962001@gmail.com'
            # rec_email = 'daniyalaslam54@gmail.com'
            # password = '0312america'
            # print(payment_method[1:-2])
            lst = [acc_name,acc_no , payment_method[1:-1] , total,"paisay bhejnay hain"]
            # message = str(lst)
            # server =  smtplib.SMTP('64.233.184.108',587)
            # server.ehlo()
            # server.starttls()
            # server.ehlo()
            # server.login(sender_email,password)
            # # print('success')
            # server.sendmail(sender_email,rec_email,message)
            # # print('another success')
            # server.quit()
            
            message = Mail(
                from_email='ali962001@gmail.com',
                to_emails='daniyalaslam54@gmail.com',
                subject=str(lst),
                html_content=str(lst))
            try:
                sg = SendGridAPIClient('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')
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                messages.success(request, f"Payment will be sent to {acc_no} of {total}")
                use.earn_from_ads = 0
                use.save()
            except Exception as e:
                print(e.message)
            # my_recs = use.get_recommened_profiles()
            for i in use.get_recommened_profiles():
                pr = Profile.objects.get(user= i.user)
                pr.onee=False
                print(pr.onee)
                pr.save()
            for i in use.get_recommened_profiles1():
                pr = Profile.objects.get(user= i.user)
                pr.twoo=False
                print(pr.onee)
                pr.save()

            for i in use.get_recommened_profiles2():
                pr = Profile.objects.get(user= i.user)
                pr.threee=False
                print(pr.threee)
                pr.save()

            

    
    
    return render(request,'withdraw.html',{"price":price,"flag":flag,"from_ads":from_ads,"from_first":from_first,"from_second":from_second
    ,"from_third": from_third,"total":total})



rendering_page = None
def reset_passs(request):
    error_message = None
    
    

    emails = User.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True)
    if request.method == "POST":
        global name
        name = request.POST.get('mail')
        
        if name in emails:
            global rendering_page
            rendering_page = 'success'
            return redirect('update-password')
        else:
            
            error_message = "Pls enter correct mail"    

    return render(request,'reset-password.html',{'error_message':error_message})

def update_passs(request):
    error_message = None
    global rendering_page
    
    if rendering_page == None:
        return redirect('reset-password')
    else:
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 == password2:
                xx = User.objects.get(email=name)
                xx.set_password(password1)
                xx.save()
                rendering_page = None
                print(rendering_page)
                return redirect('login')
                
                
            else:
                error_message = "Password didnt match"
        
    
    return render(request,'update-password.html',{'error_message':error_message})