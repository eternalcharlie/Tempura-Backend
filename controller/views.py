import urllib2
import threading
import config
import time
import json
from django.http import HttpResponse
# Create your views here.


def create_new_task(dep, id, crn):
    # Assume course is in the format of COURSEID/COURSENUMBER
    if crn:  # If crn is set
        crn_available = '<tdclass="w50"><divclass="section-meeting"><spanclass="fl-offScreen-hidden">sectionopen</span><imgclass="section-img"alt="Open"title="Open"src="/cis-pac/rs/portlets/cis/img/sectionOpen.png"/></div></td><tdclass="w50"><divclass="section-meeting">'+crn+'</div></td>'
        while True:
            response = urllib2.urlopen(config.url+config.term+dep+'/'+id).read()
            response = "".join(response.split())
            if crn_available in response:
                print "Course Available"
                config.thread_count = config.thread_count-1
                break
            print "Course Currently Unavailable"
            time.sleep(10)
    else:
        while True:
            response = urllib2.urlopen(config.url+config.term+dep+'/'+id).read()
            if "<span class=\"fl-offScreen-hidden\">section open</span>" in response:
                print "Course Available"
                config.thread_count = config.thread_count-1
                break
            print "Course Currently Unavailable"
            time.sleep(10)

    print "Thead Exit"


def receive_new_task(request):
    task_course_dep = request.GET.get('c_dep', False)
    task_course_id = request.GET.get('c_id', False)
    task_course_crn = request.GET.get('c_crn', False)
    if task_course_dep and task_course_id:
        if config.thread_count < config.max_thread:
            task = threading.Thread(target=create_new_task, args=(task_course_dep, task_course_id, task_course_crn))
            task.daemon = True
            task.start()
            config.thread_count = config.thread_count+1
            return HttpResponse(json.dumps({'status': 'Created'}), 'application/json')
    return HttpResponse(json.dumps({'status': 'Failed'}), 'application/json')
