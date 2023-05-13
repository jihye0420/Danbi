from datetime import datetime

import jwt
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.settings.base import SECRET_KEY
from config.settings.permissions import IsOwner as CustomReadOnly
from task.models import Task, SubTask
from task.serializers import SubTaskDetailSerializer
from task.serializers import TaskDetailSerializer, TaskListSerializer, TaskCreateSerializer, \
    TaskUpdateSerializer, SubTaskCreateSerializer
from users.models import User, Team
from utils.response import custom_response


class TasksView(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Task 목록 조회
        """
        tasks = Task.objects.all()
        team = get_object_or_404(Team, pk=request.user.team.team_id)
        sub_tasks = SubTask.objects.filter(team=team)
        # print(data)

        # self.check_object_permissions(self.request, tasks[0])

        # task_list = TaskListSerializer(tasks, many=True).data
        if sub_tasks:
            data = {
                'task': TaskListSerializer(tasks, many=True).data,
                'sub_task': SubTaskDetailSerializer(sub_tasks, many=True).data
            }
            res = custom_response(status=200, data=data)
        else:
            data = {
                'task': TaskListSerializer(tasks, many=True).data
            }
            res = custom_response(status=200, data=data)
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Task 생성

        :args:
        - title: Task 이름
        - content: Task 설명
        - team_list: 하위 업무로 지정할 팀 ID 리스트
        """
        try:
            title = request.data['title']
            content = request.data['content']
            team_list = request.data['team_list']

            if title == '' or content == '' or len(team_list) == 0 or (not team_list):
                res = custom_response(status=400)
                return Response(res, status=status.HTTP_200_OK)
        except KeyError:
            res = custom_response(status=400)
            return Response(res, status=status.HTTP_200_OK)

        team_list = [get_object_or_404(Team, pk=team) for team in team_list]

        task = Task.objects.create(
            create_user=request.user,
            title=title,
            content=content,
            team=request.user.team
        )
        task.save()

        sub_task_list = {
            "team_id": [],
            "name": []
        }
        for team in team_list:
            sub_task = SubTask.objects.create(
                team=team,
                task_id=task
            )
            sub_task.save()
            sub_task_list["team_id"].append(SubTaskCreateSerializer(sub_task).data['team']['team_id'])
            sub_task_list["name"].append(SubTaskCreateSerializer(sub_task).data['team']['name'])

        response = TaskCreateSerializer(task).data
        response['sub_task'] = sub_task_list
        return Response(response, status=status.HTTP_201_CREATED)


