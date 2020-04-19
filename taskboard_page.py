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
        show_delete_button = False

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

        # SEARCH FOR USERS
        user_search = MyUser.query().fetch()

        # MEMBERS IN TASK BOARD
        member_count = 0
        memberlist = []

        for member in taskboard_ref.members_id:
            deciphered_member_email = MyUser.get_by_id(member).email
            memberlist.append(deciphered_member_email)
            member_count = member_count + 1

        count = 0

        # CALCULATE TOTAL NUMBER OF TASKS
        total_tasks = 0
        active_tasks = 0
        completed_tasks = 0

        for i in taskboard_ref.tasks:
            total_tasks = total_tasks + 1

        for i in taskboard_ref.tasks:
            if i.status == False:
                active_tasks = active_tasks + 1

        for i in taskboard_ref.tasks:
            if i.status == True:
                completed_tasks = completed_tasks + 1

        if total_tasks == 0 and member_count == 1:
            show_delete_button = True

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
            'memberlist': memberlist,
            'count': count,
            'MyUser': MyUser,
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'show_delete_button': show_delete_button,
            'member_count': member_count
        }

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        error_message = False

        idd = self.request.get('id')
        decrypted_idd = ndb.Key(urlsafe=idd)
        taskboard_url_id = decrypted_idd.id()

        # GET CURRENT TASKBOARD DETAILS
        taskboard_ref = TaskBoard.get_by_id(taskboard_url_id, parent=decrypted_idd.parent())
        this_taskboard_info_key = taskboard_ref.key

        action = self.request.get('button')

        # INVITING A NEW USER
        if action == 'Invite User':
            invitee_details = self.request.get('invitee_id')
            invitee_id = MyUser.get_by_id(invitee_details)

            invitee_id.td_key.append(this_taskboard_info_key)
            invitee_id.put()

            taskboard_ref.members_id.append(invitee_id.key.id())
            taskboard_ref.put()

            self.redirect('/taskboard?id=' + str(idd))

        # CREATING A NEW TASK
        if action == 'Create Task':
            task_title = self.request.get('title')
            assign_to = self.request.get('assign_to')
            due_date = self.request.get('due_date')

            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

            task_list = []

            for each in taskboard_ref.tasks:
                task_list.append(each.title)

            if task_title in task_list:
                # RUNS THE WHOLE GET METHOD AGAIN SO AS TO DISPLAY THE VALUE OF ERROR
                url = ''
                welcome = ''
                login_status = ''
                show_delete_button = False
                error_message = True

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

                # SEARCH FOR USERS
                user_search = MyUser.query().fetch()

                # MEMBERS IN TASK BOARD
                member_count = 0
                memberlist = []

                for member in taskboard_ref.members_id:
                    deciphered_member_email = MyUser.get_by_id(member).email
                    memberlist.append(deciphered_member_email)
                    member_count = member_count + 1

                count = 0

                # CALCULATE TOTAL NUMBER OF TASKS
                total_tasks = 0
                active_tasks = 0
                completed_tasks = 0

                for i in taskboard_ref.tasks:
                    total_tasks = total_tasks + 1

                for i in taskboard_ref.tasks:
                    if i.status == False:
                        active_tasks = active_tasks + 1

                for i in taskboard_ref.tasks:
                    if i.status == True:
                        completed_tasks = completed_tasks + 1

                if total_tasks == 0 and member_count == 1:
                    show_delete_button = True
                # self.redirect('/taskboard?id=' + str(idd))

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
                    'memberlist': memberlist,
                    'count': count,
                    'MyUser': MyUser,
                    'total_tasks': total_tasks,
                    'active_tasks': active_tasks,
                    'completed_tasks': completed_tasks,
                    'show_delete_button': show_delete_button,
                    'member_count': member_count,
                    'error_message': error_message
                }

                template = JINJA_ENVIRONMENT.get_template('taskboard.html')
                self.response.write(template.render(template_values))

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

        # EDIT A TASK
        if action == 'Edit Task':
            edit_title = self.request.get('edit_title')
            edit_assign_to = self.request.get('edit_assign_to')
            edit_due_date = self.request.get('edit_due_date')
            edit_old_id = self.request.get('edit_old_id')
            index = int(self.request.get('index'))

            edit_due_date = datetime.strptime(edit_due_date, '%Y-%m-%d').date()

            task_list = []

            for each in taskboard_ref.tasks:
                task_list.append(each.title)

            if edit_title in task_list and edit_assign_to == edit_old_id:
                # RUNS THE WHOLE GET METHOD AGAIN SO AS TO DISPLAY THE VALUE OF ERROR
                url = ''
                welcome = ''
                login_status = ''
                show_delete_button = False
                error_message = True

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

                # SEARCH FOR USERS
                user_search = MyUser.query().fetch()

                # MEMBERS IN TASK BOARD
                member_count = 0
                memberlist = []

                for member in taskboard_ref.members_id:
                    deciphered_member_email = MyUser.get_by_id(member).email
                    memberlist.append(deciphered_member_email)
                    member_count = member_count + 1

                count = 0

                # CALCULATE TOTAL NUMBER OF TASKS
                total_tasks = 0
                active_tasks = 0
                completed_tasks = 0

                for i in taskboard_ref.tasks:
                    total_tasks = total_tasks + 1

                for i in taskboard_ref.tasks:
                    if i.status == False:
                        active_tasks = active_tasks + 1

                for i in taskboard_ref.tasks:
                    if i.status == True:
                        completed_tasks = completed_tasks + 1

                if total_tasks == 0 and member_count == 1:
                    show_delete_button = True
                # self.redirect('/taskboard?id=' + str(idd))

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
                    'memberlist': memberlist,
                    'count': count,
                    'MyUser': MyUser,
                    'total_tasks': total_tasks,
                    'active_tasks': active_tasks,
                    'completed_tasks': completed_tasks,
                    'show_delete_button': show_delete_button,
                    'member_count': member_count,
                    'error_message': error_message
                }

                template = JINJA_ENVIRONMENT.get_template('taskboard.html')
                self.response.write(template.render(template_values))
            else:
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

        # RENAME TASKBOARD
        if action == 'Rename Taskboard':
            name = self.request.get('taskboard_name')

            taskboard_ref.name = name
            taskboard_ref.put()
            self.redirect('/taskboard?id=' + str(idd))

        # REMOVE USER
        if action == 'Remove User':
            userID = self.request.get('user_id')
            indexy = int(self.request.get('index'))
            invitee_details = MyUser.get_by_id(userID)

            for i, assignees in enumerate(taskboard_ref.tasks):
                if assignees.assignee_id == userID:
                    taskboard_ref.tasks[i].assignee_id = str(01)
                else:
                    self.response.write('Nothing to remove')

            taskboard_ref.put()

            # DELETE MEMBER FROM TASKBOARD MEMBER LIST
            del taskboard_ref.members_id[indexy]
            taskboard_ref.put()

            # DELETE TASKBOARD FROM USER'S TASKBOARDS
            invitee_details.td_key.remove(this_taskboard_info_key)
            invitee_details.put()

            self.redirect('/taskboard?id=' + str(idd))

        # DELETE TASKBOARD
        if action == 'Delete Taskboard':
            member_list = []

            for m in taskboard_ref.members_id:
                member_list.append(m)

            for i, members in enumerate(member_list):
                invitee_details = MyUser.get_by_id(members)
                invitee_details.td_key.remove(this_taskboard_info_key)
                invitee_details.put()

            taskboard_ref.key.delete()
            self.redirect('/dashboard')
