from datetime import datetime

import json
# from django.db.models.query import QuerySet
from django.db.models.query_utils import Q

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from django.views.decorators.csrf import csrf_exempt

from .models import StudentData
# from django.utils.dateparse import parse_date, parse_datetime


def HomePage(request):
    if request.method=="POST":
        name=request.POST.get("studentName") 
        email=request.POST.get("studentName")
        gender=request.POST.get("gender")
        
        str_date=request.POST.get("start_at","")
        end_date=request.POST.get("end_at","")

        
        # filter_data = {}
        # if name: 
        #     print("name", name)
        #     filter_data['name'] = name  
        # elif str_date:
        #     startdate= datetime.strptime(str_date, "%Y-%m-%d")
        #     filter_data['created_at__gte'] = startdate 
        # elif end_date:
        #     enddate=datetime.strptime(end_date,"%Y-%m-%d")
        #     filter_data['created_at__lte'] = enddate
        # elif gender: 
        #     filter_data['gender'] = gender

        # students = StudentData.objects.filter(**filter_data)
        # date=parse_datetime(studentdate)
        # print(date)
        # students = StudentData.objects.filter(Q(name__icontains = name)|Q(email__icontains = name)|Q(created_at__date=date))
        q = Q()
        if name or email:
            q &= Q(name__icontains=name)|Q(email__icontains = email)
            print(q)
            # students = StudentData.objects.filter(Q(name__icontains=name)|Q(email__icontains = email))
        # if str_date:
        #     startdate= datetime.strptime(str_date, "%Y-%m-%d")
        # else:
        #     startdate =""
        # if end_date:
        #     enddate=datetime.strptime(end_date,"%Y-%m-%d")
        # else:
        #     enddate =""

        # elif name or email or str_date or end_date:
        #     startdate= datetime.strptime(str_date, "%Y-%m-%d")
        #     enddate=datetime.strptime(end_date,"%Y-%m-%d")
        #     students = StudentData.objects.filter(Q(name__icontains=name)|Q(email__icontains = email) |Q(created_at__date__gte=startdate ,created_at__date__lte=enddate))
        
        elif str_date or end_date :
            startdate= datetime.strptime(str_date, "%Y-%m-%d")
            enddate=datetime.strptime(end_date,"%Y-%m-%d")
            print(startdate)
            print(enddate)
        #     # q = Q(created_at__gte=startdate , created_at__lte=enddate)
            q &= Q(created_at__date__range=[startdate,enddate])
            # print(q)
            # students = StudentData.objects.filter(created_at__date__gte=startdate ,created_at__date__lte=enddate)
        # else:
        #     print("Else")
        #     students = StudentData.objects.all()
        elif gender:
            q &= Q(gender=gender.title())
            # print('gender',students)
                 
        students = StudentData.objects.filter(q)
        print(students)
        print('student counter::: ',students.count())
        context={
            "students":students,
            "name":name,
            "gender":gender,
            "str_date":str_date,
            "end_date":end_date
        }
        return render(request,"employee_list/home.html", context)
    
    else:
       context={
           "students":StudentData.objects.all()
          
       }  

    return render(request,"employee_list/home.html", context)  



    # myFilter=infoFilter(request.GET, queryset = students)
    # students = myFilter.qs
    # context={
    #     "students":students,
    #     "myFilter":myFilter
    # }
    # return render(request,"employee_list/home.html", context)

@csrf_exempt
def InsertStudent(request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    gender=request.POST.get("gender")

    try:
        student=StudentData(name=name,email=email,gender=gender)
        student.save()
        stuent_data={
            "id":student.id,"created_at":student.created_at,
            "error":False,"errorMessage":"Student Added Successfully"
        }
        return JsonResponse(stuent_data,safe=False)
    except:
        stuent_data={"error":True,"errorMessage":"Failed to Add Student"}
        return JsonResponse(stuent_data,safe=False)

@csrf_exempt
def update_all(request, id):
    data=request.POST.get("data")
 
    dict_data=json.loads(data)
    print(dict_data)
    try:
        for dic_single in dict_data:
            student=StudentData.objects.all(id)
            student.name=dic_single['name']
            student.email=dic_single['email']
            student.gender=dic_single['gender']
            student.save()
        stuent_data={"error":False,"errorMessage":"Updated Successfully"}
        return JsonResponse(stuent_data,safe=False)
    except:
        stuent_data={"error":True,"errorMessage":"Failed to Update Data"}
        return JsonResponse(stuent_data,safe=False)

@csrf_exempt
def delete_data(request):
    id=request.POST.get("id")
    try:
        student=StudentData.objects.get(id=id)
        student.delete()
        stuent_data={"error":False,"errorMessage":"Deleted Successfully"}
        return JsonResponse(stuent_data,safe=False)
    except:
        stuent_data={"error":True,"errorMessage":"Failed to Delete Data"}
        return JsonResponse(stuent_data,safe=False)
        


# @csrf_exempt
# def student_list(request):
#     data=StudentData.objects.all()
#     return render(request,'home.html',{'data':data})


# def get_data(request,gender):
#     student=get_object_or_404(StudentData, pk=request.get("id"))

#     data_quary = Q()

#     created_at=request.POST.get('create_at','')



    

# DrafCode for understanding filtaring

# @csrf_exempt
# def get_pi_for_dataTable(request, pi_status=''):
#     user            = get_object_or_404(Users, pk=request.session.get("id"))
#     pi_query        = Q()
#     start_date      = request.POST.get('start_date', '')
#     end_date        = request.POST.get('end_date', '')
#     if start_date or end_date:
#         end_date    = datetime.strptime(end_date, "%Y-%m-%d")
#         end_date    = end_date + timedelta(days=1)
#         pi_query   &= Q(created_at__gte=start_date, created_at__lt=end_date)
#     supplier        = request.POST.get('supplier', '')
#     if supplier     : pi_query &= Q(supplier_id=supplier)
#     status_text     = request.POST.get('status', '')
#     if status_text  :
#         if status_text == "local"       : pi_query &= Q(wo__wo_type=True)
#         elif status_text == "foreign"   : pi_query &= Q(wo__wo_type=False)
#     company         = request.POST.get('company', '')
#     if company      : pi_query &= Q(wo__company_id=company)
#     search_text     = request.POST.get('search_text', '').strip()
#     req_status      = request.POST.get('req_list_status', '')
#     if search_text or req_status:
#         pi_wos = SCWO.objects.filter(pi_generated=True)
#         wo_query = Q(wo__in=pi_wos)
#     if search_text:
#         wo_query    &= Q(ebs_bl_dp_wo.wo_query(search_text) | ebs_bl_cs_wo.wo_query(search_text))
#         item_wise_wo_list = SCWOItem.objects.filter(wo_query).values("wo")
#         pi_query    &= Q(
#                         Q(wo__in=item_wise_wo_list)|
#                         Q(pi_no__icontains=search_text)|
#                         Q(wo__wo_no__icontains=search_text)|
#                         Q(wo__cs__cs_no__icontains=search_text)|
#                         Q(wo__cs__pr__req_code__icontains=search_text)
#                     )
#     if req_status :
#         if int(req_status) == 1    : wo_query &= Q(Q(cs_item__pr_item__req__bom__isnull=True),Q(req_item__req__bom__isnull=True)) # In-Direct
#         elif int(req_status) == 2  : wo_query &= Q(Q(cs_item__pr_item__req__bom__isnull=False)|Q(req_item__req__bom__isnull=False)) # Direct
#         item_wise_wo_list = SCWOItem.objects.filter(wo_query).values("wo")
#         pi_query &= Q(wo__in=item_wise_wo_list)
#     if request.session['role_text'] == "Audit": 
#         pi_query &= Q(rejected_reason__iexact='')
#         # Garments_CEO declared in supplychain.views
#         companies = Company.objects.filter(ceo=user.company.ceo).values_list('id', flat=True)
#         if user.company.ceo_id == Garments_CEO          : pi_query &=  Q(created_by__company_id__in=companies)
#         else                                            : pi_query &= ~Q(created_by__company_id__in=companies)
#     elif request.session['role_text'] == "Procurer"     : pi_query &=  Q(created_by=user)
#     elif request.session['role_text'] in ["Finance", "Commercial"] : pi_query &=  Q(audited_at__isnull=False)
#     elif request.session['role_text'].lower() in ['sc head', 'admin', 'management', 'super admin']: pi_query &= Q()
#     else                                                : pi_query = Q(False)
#     if pi_status == 'draft'    : pi_query &= Q(status__in=[Status.name("Started"), Status.name("Rejected")])
#     elif pi_status == 'raised' : pi_query &= Q(status=Status.name("Raised"))
#     elif pi_status == 'checked': pi_query &= Q(status=Status.name("Checked"))
#     start            = int(request.POST.get('start', 0))
#     pi_list          = SCWOPI.objects.filter(pi_query).order_by("-id").distinct()[start:start+20]
#     data_list        = []
#     for pi in pi_list:
#         pi_no = ebs_bl_common.text_url(pi.get_absolute_url(), pi.pi_no)
#         wos = ''
#         for wo in pi.wo.all():
#             wos    += ebs_bl_common.text_url(wo.get_absolute_url(), wo.wo_no) + ' , <br>'
#         supplier    = ebs_bl_common.supplier_html(pi.supplier)
#         created_by  = ebs_bl_common.user_html(pi.created_by)
#         roles = ['sc head', 'admin', 'commercial', 'finance', 'management', 'super admin']
#         if not pi.rejected_reason                           : action = ebs_bl_common.action_html(pi.get_absolute_url(), icon="icon-eye")
#         elif request.session['role_text'].lower() in roles  : action = ebs_bl_common.action_html(pi.get_absolute_url(), icon="icon-eye")
#         else                                                : 
#             edit_url = reverse('sc:edit_pi', kwargs={'pi_id':pi.id})
#             action = ebs_bl_common.action_html(action_url=edit_url, color_text='text-success', icon="ti-pencil-alt")
#         if pi.status == Status.name("Checked"):
#             status = "Checked by " + ebs_bl_common.user_html(pi.audited_by, 12)
#             print_url = pi.get_absolute_url()+"?print=print"
#             action += ebs_bl_common.action_html(action_url=print_url, color_text="text-warning", icon="ti-printer")
#         elif pi.status == Status.name("Rejected"):
#             time = ebs_bl_common.date_time_format(pi.audited_at, 'datetime')
#             status = '<a href="#noteModal" data-toggle="modal" data-pi="'+str(pi.pi_no)+'" data-audit="'+str(pi.audited_by.name)+'" data-time="'+time+'" data-note="'+str(pi.rejected_reason)+'" class="note_info text-info" data-target="#noteModal">Rejected by Audit</a>'
#         elif pi.status == Status.name("Raised"): status = "Pending for Audit Check"
#         else: 
#             status = "Saved as Draft"
#             edit_url = reverse('sc:edit_pi', kwargs={'pi_id':pi.id})
#             action = ebs_bl_common.action_html(action_url=edit_url, icon="ti-pencil-alt")
#         status = ebs_bl_common.datatable_center_td(status)
#         created_at = ebs_bl_common.date_time_format(pi.created_at, 'datetime')
#         action = ebs_bl_common.datatable_center_td(action)
#         data = [pi_no, wos, supplier, created_by, status, created_at, action]
#         data_list.append(data)
#     return JsonResponse(data_list, safe=False)


#  For auto search
@csrf_exempt
def get_student_for_datatable(request):
    data_list = [] 
    start       = int(request.POST.get('start', 0))
    # company     = request.POST.get('company','')
    # buyer       = request.POST.get('buyer','')
    # start_date  = request.POST.get('start_date', '')
    # end_date    = request.POST.get('end_date', '')
    # merchant    = request.POST.get('merchant','')
    name      =request.POST.get('name','')
    email     =request.POST.get('email','')
    created_at =request.POST.get('created_at','')
    student_list = StudentData.objects.all()

    # print(student_list)

    if name: student_list = student_list.filter(name=name)
    if email: student_list = student_list.filter(email=email)

    if  created_at:
        student_list = student_list.filter( created_at=created_at)


    student_list = student_list[start:start + 20]
    for student in student_list:
        # view_url = reverse('mnm:student_view', kwargs={'id': student.id})
        StudentName = student.name
        Email = student.email
        CreateDate = student.created_at

        # print(student)


        
        data = [StudentName, Email, CreateDate]
        data_list.append(data)

        print(data_list)

    return JsonResponse(data_list, safe=False)
