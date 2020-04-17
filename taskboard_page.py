import logging
import os
from datetime import datetime

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from task import Task
from taskboard import TaskBoard

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class TaskBoardPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        welcome = ''
        login_status = ''
        error_message = ''

        user = users.get_current_user()

        if user:
            welcome = 'Welcome back to the workspace, we missed You!'
            url = users.create_logout_url('/')
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Hurray! Your First Login into the workspace, we hope you enjoy our application!'
                myuser = MyUser(id=user.user_id(),
                                identity=user.user_id(),
                                email=user.email())
                myuser.put()


        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        idd = self.request.get('id')
        decrypted_idd = ndb.Key(urlsafe=idd)
        taskboard_url_id = decrypted_idd.id()

        taskboard_ref = TaskBoard.get_by_id(taskboard_url_id, parent=decrypted_idd.parent())
        # taskboard_keys = taskboard_ref.creator_name
        # self.response.write(taskboard_ref.members)

        # SEARCH FOR USERS
        user_search = MyUser.query().fetch()

        # DO NOT MEMBER USER ALREADY IN TASK BOARD
        memberlist = []
        # memberlist_key = []

        for member in taskboard_ref.members_id:
            deciphered_member_email = MyUser.get_by_id(member).email
            memberlist.append(deciphered_member_email)

        count = 0

        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status,
            'user_email': user.email(),
            'user_search': user_search,
            'idd': idd,
            'taskboard_ref': taskboard_ref,
            'all_tasks': taskboard_ref.tasks,
            'members': taskboard_ref.members_id,
            'error_message': error_message,
            'memberlist': memberlist,
            'count': count,
            'MyUser': MyUser
        }

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        idd = self.request.get('id')
        decrypted_idd = ndb.Key(urlsafe=idd)
        logging.info(decrypted_idd)
        taskboard_url_id = decrypted_idd.id()
        logging.info(taskboard_url_id)

        # GET CURRENT TASKBOARD DETAILS
        taskboard_ref = TaskBoard.get_by_id(taskboard_url_id, parent=decrypted_idd.parent())

        action = self.request.get('button')

        # INVITING A NEW USER
        if action == 'Invite User':
            taskboard_info = TaskBoard.get_by_id(taskboard_url_id, parent=myuser_key)
            this_taskboard_info_key = taskboard_info.key

            invitee_details = self.request.get('invitee_id')
            invitee_id = MyUser.get_by_id(invitee_details)

            invitee_id.td_key.append(this_taskboard_info_key)
            invitee_id.td_name.append(taskboard_info.name)
            invitee_id.td_creator_id.append(user.user_id())
            invitee_id.put()
            # self.response.write(invitee_id)

            taskboard_ref.members_id.append(invitee_id.key.id())
            # taskboard_ref.members.append(invitee_id.email)
            taskboard_ref.put()

            self.redirect('/taskboard?id=' + str(idd))

        # CREATING A NEW TASK
        if action == 'Create Task':
            task_title = self.request.get('title')
            assign_to = self.request.get('assign_to')
            due_date = self.request.get('due_date')

            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

            task_list = []
            # memberlist = []

            for each in taskboard_ref.tasks:
                task_list.append(each.title)

            # for member in taskboard_ref.members:
            #     memberlist.append(member)

            if task_title in task_list:
                error_message = 'Task already exists'
                self.redirect('/taskboard?id=' + str(idd))
            else:
                new_task = Task(
                    title=task_title,
                    due_date=due_date,
                    assignee_id=assign_to,
                    status=False
                )

                taskboard_ref.tasks.append(new_task)
                taskboard_ref.put()
                self.redirect('/taskboard?id=' + str(idd))
                # self.response.write(taskboard_ref)

        # EDIT A TASK
        if action == 'Edit Task':
            edit_title = self.request.get('edit_title')
            edit_assign_to = self.request.get('edit_assign_to')
            edit_due_date = self.request.get('edit_due_date')
            index = int(self.request.get('index'))

            edit_due_date = datetime.strptime(edit_due_date, '%Y-%m-%d').date()

            new_task = Task(
                title=edit_title,
                due_date=edit_due_date,
                assignee_id=edit_assign_to,
                status=False
            )

            taskboard_ref.tasks.pop(index)
            taskboard_ref.tasks.insert(index, new_task)
            taskboard_ref.put()
            self.redirect('/taskboard?id=' + str(idd))

        # DELETING A TASK
        if action == 'Delete Task':
            index = int(self.request.get('index'))

            del taskboard_ref.tasks[index]
            taskboard_ref.put()
            self.redirect('/taskboard?id=' + str(idd))

        # HANDLE CHECKED BOK
        if action == 'Mark As Completed':
            title = self.request.get('check_title')
            assigned_to = self.request.get('check_assigned_to')
            due_date = self.request.get('check_due_date')
            index = int(self.request.get('check_index'))

            converted_due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

            new_task = Task(
                title=title,
                assignee_id=assigned_to,
                due_date=converted_due_date,
                status=True
            )

            taskboard_ref.tasks.pop(index)
            taskboard_ref.tasks.insert(index, new_task)
            taskboard_ref.put()
            self.redirect('/taskboard?id=' + str(idd))

        # HANDLE UNCHECKING BOK
        if action == 'Mark As Uncompleted':
            title = self.request.get('uncheck_title')
            assigned_to = self.request.get('uncheck_assigned_to')
            due_date = self.request.get('uncheck_due_date')
            index = int(self.request.get('uncheck_index'))

            converted_due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

            new_task = Task(
                title=title,
                assignee_id=assigned_to,
                due_date=converted_due_date,
                status=False
            )

            taskboard_ref.tasks.pop(index)
            taskboard_ref.tasks.insert(index, new_task)
            taskboard_ref.put()
            self.redirect('/taskboard?id=' + str(idd))

        # EDIT TASKBOARD
        if action == 'Edit Taskboard':
            name = self.request.get('taskboard_name')

            taskboard_ref.name = name
            taskboard_ref.put()
            self.redirect('/taskboard?id=' + str(idd))

        # REMOVE USER
        if action == 'Remove User':
            userID = self.request.get('user_id')
            indexy = self.request.get('index')
            invitee_details = MyUser.get_by_id(userID)

            asigned_tasks = []

            for assignees in taskboard_ref.tasks:
                asigned_tasks.append(assignees.assignee_id)

            for i, assignees in enumerate(taskboard_ref.tasks):
                if assignees.assignee_id == userID:
                    new_task = Task(
                        title=assignees.title,
                        due_date=assignees.due_date,
                        assignee_id='None',
                        status=assignees.status,
                        completion_date=assignees.completion_date
                    )
                    del taskboard_ref.tasks[i]
                    taskboard_ref.tasks.insert(i, new_task)
                    taskboard_ref.put()
                else:
                    self.response.write('Nothing to remove')

            self.redirect('/taskboard?id=' + str(idd))

            # self.response.write(asigned_tasks)
            # del taskboard_ref.tasks
            # del taskboard_ref.members_id[indexy]
            # taskboard_ref.put()
            # #
            # #
            # self.redirect('/taskboard?id=' + str(idd))
