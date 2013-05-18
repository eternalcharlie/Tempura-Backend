import urllib2
import threading
import config
import time
import json
from django.http import HttpResponse
# Create your views here.


def create_new_task(dep, id):
    # Assume course is in the format of COURSEID/COURSENUMBER
    while True:
        response = urllib2.urlopen(config.url+config.term+dep+'/'+id).read()
        print response
        if "<span class=\"fl-offScreen-hidden\">section open</span>" in response:
            print "Course Available"
            config.thread_count = config.thread_count-1
            break
        print "Course Currently Unavailable"
        time.sleep(10)


def receive_new_task(request):
    task_course_dep = request.GET.get('c_dep', False)
    task_course_id = request.GET.get('c_id', False)
    if task_course_dep and task_course_id:
        if config.thread_count < config.max_thread:
            task = threading.Thread(target=create_new_task, args=(task_course_dep, task_course_id))
            task.daemon = True
            task.start()
            config.thread_count = config.thread_count+1
            return HttpResponse(json.dumps({'status': 'Created'}), 'application/json')
    return HttpResponse(json.dumps({'status': 'Failed'}), 'application/json')
