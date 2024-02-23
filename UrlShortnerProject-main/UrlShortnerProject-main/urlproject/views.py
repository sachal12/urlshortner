from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import HttpResponse
from .models import LongToShort
from ip2geotools.databases.noncommercial import DbIpCity
# from django.shortcuts import get_client_ip
def home(request):
    form={
        "submitted":False,
        "error":False
        } #by default value is false when user not fill the form

    if request.method =='POST':
        longurl=request.POST['longurl']
        shorturl=request.POST['custom_name']
        
        try:
        # create operation
            obj=LongToShort(
                longurl=longurl,
                shorturl=shorturl,
                country="",
                country_count="",
                clicks=0,
                dclicks=0,
                mclicks=0
                )
            obj.save()

            date=obj.date
            clicks=obj.clicks

            form["longurl"]=longurl
            form["submitted"]=True #when user fill the form then urls shown
            form["shorturl"]=request.build_absolute_uri()+shorturl
            form["date"]=date
            form["clicks"]=clicks
        except:
          form['error']=True 
    return render(request,'index.html',form)

def redirect_url(request,shorturl):
    row=LongToShort.objects.filter(shorturl=shorturl) 
    if len(row) == 0:
        return HttpResponse("No such short url here")
    obj=row[0]
    longurl=obj.longurl 


    obj.clicks=obj.clicks+1
    obj.save()
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    if 'mobile' in user_agent:
       obj.mclicks=obj.mclicks+1
       obj.save()
    else:
       # The request is from a laptop or desktop
       obj.dclicks=obj.dclicks+1
       obj.save()

    ip = get_client_ip(request)
    response = DbIpCity.get(ip, api_key='free')

    # country = obj.country
    # country_count = obj.country_count

    # country_list = country.split(',') if country else []
    # country_count_list = str(country_count).split(',') if country_count else []

    # if response.country in country_list:
    #     index = country_list.index(response.country)
    #     country_count_list[index] = str(int(country_count_list[index]) + 1)
    # else:
    #     country_list.append(response.country)
    #     country_count_list.append(1)

    # obj.country = ','.join(country_list)
    # obj.country_count = ','.join(str(i) for i in country_count_list)
    # obj.save()    
    country = obj.country
    country_count = obj.country_count

    country_list = str(country).split(',') if country else []
    country_count_list = str(country_count).split(',') if country_count else []

    if response.country in country_list:
        index = country_list.index(response.country)
        country_count_list[index] = str(int(country_count_list[index]) + 1)
    else:
        country_list.append(response.country)
        country_count_list.append('1')

    obj.country = ','.join(country_list)
    obj.country_count = ','.join(country_count_list)
    obj.save()
        


    # c_obj = LongToShort.objects.filter(country=response.country)
    # if c_obj.exists():
    #     first = c_obj.first()
    #     first.country_count = first.country_count + 1
    #     first.save()
    # else :
    #     obj.country = response.country
    #     obj.country_count = obj.country_count + 1

    #     obj.save()
    return redirect(longurl)



def all_analytics(request):
    row=LongToShort.objects.all()
    context={"row":row}
    return render(request,"all-analytics.html",context)

def analytic(request, id):
    pk= int(id)
   
    item_row = get_object_or_404(LongToShort, pk=pk)
    # countries = item_row.country.split(',')
    # country_counts = item_row.country_count.split(',')

    countries = str(item_row.country).split(',') if item_row.country else []
    country_counts = str(item_row.country_count).split(',') if item_row.country_count else []
    
    country_counts = [int(i) for i in country_counts]


    context = {"item_row": item_row, "countries":countries, "country_counts":country_counts}
    return render(request,'analytics.html', context)

            # Testing the geo-agent function
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(request):
    response = DbIpCity.get(get_client_ip(request), api_key='free')
    return HttpResponse('Request was made from: ' + response.country)
   
