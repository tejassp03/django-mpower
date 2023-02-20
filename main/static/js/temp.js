//multiple skills

var count = 1;
            var radioCount = 2;
            var totalRadioCount = 2;
            var questionRadioCount = "2";
            var totalQuestionCount = 1;
            var latestQuestionID = 1;
            var questionRadioCountArray = [[1, 2]];
            var counta = 1;
            var radioCounta = 2;
            var totalRadioCounta = 2;
            var questionRadioCounta = "2";
            var totalQuestionCounta = 1;
            var latestQuestionIDa = 1;
            var questionRadioCountArraya = [[1, 2]];
            function addQuestion(targetval) {
                if(targetval=="skills")
                {
                    count++;
                    totalQuestionCount++;
                    latestQuestionID++;
                    radioCount = 1;
                    totalRadioCount++;
                    updateCountOnForm(count, "QuestionCount");
                    latestQuestionID = Math.max(latestQuestionID, totalQuestionCount);
                }
                else
                {
                    counta++;
                    totalQuestionCounta++;
                    latestQuestionIDa++;
                    radioCounta = 1;
                    totalRadioCounta++;
                    updateCountOnForm(counta, "QuestionCounta");
                    latestQuestionID = Math.max(latestQuestionIDa, totalQuestionCounta);
                }
                const questionDiv = document.createElement('div');
                const individualQuestion = document.createElement('div');
                const question = document.createElement('input');
                question.setAttribute('type', 'text');
                const deleteButton = document.createElement('a');
                deleteButton.setAttribute('class', 'btn delete_button');
                const deleteIcon = document.createElement('i');
                deleteButton.setAttribute('class', 'fa fa-close fa-2x');
                if(targetval=="skills")
                {
                    questionDiv.setAttribute('id', `sq${totalQuestionCount}`);
                    questionDiv.setAttribute('class', `single_question${totalQuestionCount} Ques col-6`);
                    individualQuestion.setAttribute('class', 'individualQuestion');
                    question.setAttribute('class', 'form-control specialInputQuestions');
                    question.setAttribute('placeholder', 'Skill');
                    question.setAttribute('id', `question${totalQuestionCount}`);
                    question.setAttribute('name', `skill`);
                    deleteButton.setAttribute('id', `${totalQuestionCount}`);
                    deleteButton.setAttribute('onclick', 'deleteQuestion(this.id, "sq")');
                }
                else
                {
                    questionDiv.setAttribute('id', `eq${totalQuestionCounta}`);
                    questionDiv.setAttribute('class', `single_question${totalQuestionCounta}a Ques`);
                    individualQuestion.setAttribute('class', 'individualQuestiona');
                    question.setAttribute('class', 'form-control specialInputQuestionsa');
                    question.setAttribute('placeholder', 'Experience (Role, company, timespan)');
                    question.setAttribute('id', `question${totalQuestionCounta}a`);
                    question.setAttribute('name', `experience`);
                    deleteButton.setAttribute('id', `${totalQuestionCounta}`);
                    deleteButton.setAttribute('onclick', 'deleteQuestion(this.id, "eq")');
                }
                deleteButton.appendChild(deleteIcon);
                individualQuestion.appendChild(question);
                individualQuestion.appendChild(deleteButton);
                questionDiv.appendChild(individualQuestion);
                var quest;
                if(targetval=="skills")
                {
                    updateRadioCountOnForm(totalRadioCount, "radioCount");
                    quest=document.getElementById('questioneer');
                    questionRadioCountArray.push([totalQuestionCount, radioCount]);
                    rdc(questionRadioCountArray, "rdc");
                }
                else
                {
                    updateRadioCountOnForm(totalRadioCounta, "radioCounta");
                    quest=document.getElementById('questioneera');
                    questionRadioCountArraya.push([totalQuestionCounta, radioCounta]);
                    rdc(questionRadioCountArraya, "rdca");
                }
                quest.appendChild(questionDiv);
            }
            function updateCountOnForm(count, targetval) {
                var countKeeper = document.getElementById(targetval);
                countKeeper.value = count; 
            }
            function updateRadioCountOnForm(totalRadioCount, targetval) {
                var countKeeper = document.getElementById(targetval);
                countKeeper.value = totalRadioCount; 
            }
            function rdc(questionRadioCountArray, targetval) {
                var questionRadioCountString = document.getElementById(targetval);
                questionRadioCountString.value = questionRadioCountArray;
            }
            function deleteQuestion(questionID, targetval) {
                var classNameOfQuestionToRemove = targetval + questionID;
                const element = document.getElementById(classNameOfQuestionToRemove);
                element.remove();
                questionID = parseInt(questionID);
                var firstArray = [];
                var firstArraya = [];
                if(targetval=="sq")
                {
                    count--;
                    updateCountOnForm(count, "QuestionCount");
                    totalRadioCount = totalRadioCount - radioCount;
                    updateRadioCountOnForm(totalRadioCount, "radioCount");
                    if (questionID == totalQuestionCount) {
                        totalQuestionCount--;
                    }
                    for (var i = 0; i < questionRadioCountArray.length; i++) {
                        firstArray.push(questionRadioCountArray[i][0]);
                    }
                    var index = firstArray.indexOf(questionID);
                    questionRadioCountArray.splice(index, 1);
                    latestQuestionID = parseInt(questionRadioCountArray[questionRadioCountArray.length-1][0]);
                    var double = questionRadioCountArray.pop();
                    double.push(radioCount);
                    questionRadioCountArray.push(double);
                    rdc(questionRadioCountArray, "rdc");
                }
                else
                {
                    counta--;
                    updateCountOnForm(count, "QuestionCounta");
                    totalRadioCounta = totalRadioCounta - radioCounta;
                    updateRadioCountOnForm(totalRadioCount, "radioCounta");
                    if (questionID == totalQuestionCounta) {
                        totalQuestionCounta--;
                    }
                    for (var i = 0; i < questionRadioCountArraya.length; i++) {
                        firstArraya.push(questionRadioCountArraya[i][0]);
                    }
                    var indexa = firstArraya.indexOf(questionID);
                    questionRadioCountArraya.splice(indexa, 1);
                    latestQuestionID = parseInt(questionRadioCountArraya[questionRadioCountArraya.length-1][0]);
                    var doublea = questionRadioCountArraya.pop();
                    doublea.push(radioCounta);
                    questionRadioCountArraya.push(doublea); 
                    rdc(questionRadioCountArray, "rdca");
                }
            }

        //     <div class="form-group fg_2">
        //     <input style="border: none; display: none;" id="QuestionCount" name="question_count" value=1>
        //     <input style="border: none; display: none;" id="radioCount" name="radio_count" value=2>
        //     <input style="border: none; display: none;" id="rdc" name="rdc">
        //     <section class="questionInput" class="container">
        //         <div id="questioneer" class="row">
        //             <div id="sq1" class="single_question1 Ques col-6">
        //                 <div class="individualQuestion">
        //                     <input class="form-control specialInputQuestions" type="text" placeholder="Skill" name="skill" id="question1">
        //                 </div>
        //             </div>
        //         </div>
        //         <button type="button" id="addQuestions" class="btn btn-primary" onclick="addQuestion('skills')" style="margin: 20px 20px">+</button>
        //     </section>
        // </div>
        // <div class="form-group fg_2">
        //     <input style="border: none; display: none;" id="QuestionCounta" name="question_counta" value=1>
        //     <input style="border: none; display: none;" id="radioCounta" name="radio_counta" value=2>
        //     <input style="border: none; display: none;" id="rdca" name="rdca">
        //     <section class="questionInputa" class="container">
        //         <div id="questioneera" class="row">
        //             <div id="eq1" class="single_question1a Ques">
        //                 <div class="individualQuestiona">
        //                     <input class="form-control specialInputQuestionsa" type="text" placeholder="Experience (Role, company, timespan)" name="experience" id="question1a">
        //                 </div>
        //             </div>
        //         </div>
        //         <button type="button" id="addQuestionsa" class="btn btn-primary" onclick="addQuestion('experience')" style="margin: 20px 20px">+</button>
        //     </section>
        // </div>




// Dynamic loading on candidates side

setInterval(temp, 2000);

 function temp(id)
 {
    $.ajax(
    {
        type:"GET",
        url: "fetchmess/",
        data:{
                employer: $('[name="employer"]').val()
        },
        success: function( data ) 
        {
            let mes=data['mess'];
            let ms=[];
            let tempele=$('.pxp-dashboard-inbox-messages-item-time');
            let flag=0;
            for (let i = 0; i < mes.length; i++) {
                if(JSON.parse(mes[i])[0])
                {
                    if(JSON.parse(mes[i])[0].msg_id_id==id)
                    {
                        JSON.parse(mes[i]).forEach(myFunction);
                        function myFunction(item, index) {
                            console.log(tempele[tempele.length-1].innerHTML)
                            if(item.date==tempele[tempele.length-1].innerHTML)
                            {
                                flag=1;
                            }
                            else
                            {
                                if(flag==1)
                                {
                                    ms.push(item);
                                }
                            }
                        }
                    }
                }
            }
            console.log(ms);
        }
     })
     if(ms.length>0)
     {
    let itemdiv=document.createElement('div');
    itemdiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item mt-4')
    let rowdiv=document.createElement('div');
    rowdiv.setAttribute('class', 'row')
    let coldiv=document.createElement('div');
    coldiv.setAttribute('class', 'col-7')
    let ithediv=document.createElement('div');
    ithediv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-header')
    let firindiv=document.createElement('div');
    firindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-avatar pxp-cover')
    firindiv.style.backgroundImage='url({% static 'images/company-logo-2.png' %})';
    let secindiv=document.createElement('div');
    secindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-name ms-2')
    secindiv.innerHTML="1"
    let thiindiv=document.createElement('div');
    thiindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-time pxp-text-light ms-3')
    thiindiv.innerHTML="1"
    ithediv.append(firindiv);
    ithediv.append(secindiv);
    ithediv.append(thiindiv);
    let indiv=document.createElement('div');
    indiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-message pxp-is-self mt-2')
    indiv.innerHTML="1"
    coldiv.append(ithediv);
    coldiv.append(indiv);
    rowdiv.append(coldiv);
    itemdiv.append(rowdiv);
    $('.pxp-dashboard-inbox-messages-content').append(itemdiv)
     }
 }



 
 function temp(id)
 {
    $.ajax(
    {
        type:"GET",
        url: "fetchmess/",
        data:{
                employer: $('[name="employer"]').val()
        },
        success: function( data ) 
        {
            let mes=data['mess'];
            let ms=[];
            let tempele=$('.pxp-dashboard-inbox-messages-item-time');
            let flag=0;
            console.log(data)
            for (let i = 0; i < mes.length; i++) {
                if(JSON.parse(mes[i])[0])
                {
                    if(JSON.parse(mes[i])[0].msg_id_id==id)
                    {
                        JSON.parse(mes[i]).forEach(myFunction);
                        function myFunction(item, index) {
                            ms.push(item);
                        }
                    }
                }
            }
            for(let i=0;i<ms.length;i++)
            {
                if(ms[i].receiver_user_id != thre.receiver_id)
                {
                    let itemdiv=document.createElement('div');
                    itemdiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item')
                    let rowdiv=document.createElement('div');
                    rowdiv.setAttribute('class', 'row justify-content-end')
                    let coldiv=document.createElement('div');
                    coldiv.setAttribute('class', 'col-7')
                    let ithediv=document.createElement('div');
                    ithediv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-header flex-row-reverse')
                    let firindiv=document.createElement('div');
                    firindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-avatar pxp-cover')
                    firindiv.style.backgroundImage='url({% static 'images/company-logo-2.png' %})';
                    let secindiv=document.createElement('div');
                    secindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-name me-2')
                    secindiv.innerHTML=ms[i].sender_user_id
                    let thiindiv=document.createElement('div');
                    thiindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-time pxp-text-light me-3')
                    thiindiv.innerHTML=ms[i].date
                    ithediv.append(firindiv);
                    ithediv.append(secindiv);
                    ithediv.append(thiindiv);
                    let indiv=document.createElement('div');
                    indiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-message pxp-is-other mt-2')
                    indiv.innerHTML=ms[i].body
                    coldiv.append(ithediv);
                    coldiv.append(indiv);
                    rowdiv.append(coldiv);
                    itemdiv.append(rowdiv);
                    firstDiv.append(itemdiv)
                }
                else
                {
                    let itemdiv=document.createElement('div');
                    itemdiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item mt-4')
                    let rowdiv=document.createElement('div');
                    rowdiv.setAttribute('class', 'row')
                    let coldiv=document.createElement('div');
                    coldiv.setAttribute('class', 'col-7')
                    let ithediv=document.createElement('div');
                    ithediv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-header')
                    let firindiv=document.createElement('div');
                    firindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-avatar pxp-cover')
                    firindiv.style.backgroundImage='url({% static 'images/company-logo-2.png' %})';
                    let secindiv=document.createElement('div');
                    secindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-name ms-2')
                    secindiv.innerHTML=ms[i].sender_user_id
                    let thiindiv=document.createElement('div');
                    thiindiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-time pxp-text-light ms-3')
                    thiindiv.innerHTML=ms[i].date
                    ithediv.append(firindiv);
                    ithediv.append(secindiv);
                    ithediv.append(thiindiv);
                    let indiv=document.createElement('div');
                    indiv.setAttribute('class', 'pxp-dashboard-inbox-messages-item-message pxp-is-self mt-2')
                    indiv.innerHTML=ms[i].body
                    coldiv.append(ithediv);
                    coldiv.append(indiv);
                    rowdiv.append(coldiv);
                    itemdiv.append(rowdiv);
                    firstDiv.append(itemdiv)
                }
            }

        }
     })
 }



 
# def candidates(request, pk):
#     if request.method=="POST":
#         if 'approve' in request.POST:
#             apps=Application.objects.get(apply_id=request.POST['apply_id'])
#             apps.status=1
#             apps.save()
#             return redirect('employer:candidates', pk=pk)
#         if 'reject' in request.POST:
#             apps=Application.objects.get(apply_id=request.POST['apply_id'])
#             apps.status=2
#             apps.save()
#             return redirect('employer:candidates', pk=pk)
#         if 'act' in request.POST:
#             if(request.POST['act']=="delall"):
#                 for i in request.POST.getlist('ids[]'):
#                     Application.objects.filter(apply_id=i).delete()
#             if(request.POST['act']=="appall"):
#                 for i in request.POST.getlist('ids[]'):
#                     apps=Application.objects.get(apply_id=i)
#                     apps.status=1
#                     apps.save()
#             if(request.POST['act']=="rejall"):
#                 for i in request.POST.getlist('ids[]'):
#                     apps=Application.objects.get(apply_id=i)
#                     apps.status=2
#                     apps.save()
#             return redirect('employer:candidates', pk=pk)
#         Application.objects.filter(apply_id=request.POST['apply_id']).delete()
#         return redirect('employer:candidates', pk=pk)
#     applics=Application.objects.filter(eid=pk)
#     jobs=Jobs.objects.filter(eid=pk).order_by('-postdate')
#     app_count=[]
#     for i in jobs:
#         app_count.append(len(Application.objects.filter(job_id=i.jobid)))
#     all_can=[]
#     for i in applics:
#         single_can={}
#         user=JobSeeker.objects.get(user_id=i.user_id.user_id)
#         single_can['user_id']=user.user_id
#         single_can['name']=user.name
#         single_can['location']=user.location
#         single_can['photo']=user.photo
#         job=Jobs.objects.get(jobid=i.job_id.jobid)
#         single_can['jobid']=job.jobid
#         single_can['title']=job.title
#         single_can['status']=i.status
#         single_can['date_applied']=i.date_applied
#         single_can['apply_id']=i.apply_id
#         single_can['log_id']=user.log_id.log_id
#         all_can.append(single_can)
#     count=len(all_can)
#     all_can = sorted(all_can, key=lambda d: d['date_applied'])
#     all_can.reverse()
#     GET_params = request.GET.copy()
#     if('page' in GET_params):
#         last=GET_params['page'][-1]
#         GET_params['page']=last[0]
#     p=Paginator(all_can, 5)
#     page_number = request.GET.get('page')
#     try:
#         page_obj = p.get_page(page_number)
#     except PageNotAnInteger:
#         page_obj = p.page(1)
#     except EmptyPage:
#         page_obj = p.page(p.num_pages)
#     return render(request, 'temp-employer.html', {'pk': pk, 'pe': page_obj, 'count': count, 'jobs': jobs, 'app_count': app_count})
#     # return render(request, 'candidates-employer.html', {'pk': pk, 'pe': page_obj, 'count': count})
