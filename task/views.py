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
        sub_tasks = SubTask.objects.filter(team=team, is_delete=False)
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
            title = request.data.get('title')
            content = request.data.get('content')
            team_list = request.data.get('team_list')

            if not (title and content and team_list):
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
                task=task
            )
            sub_task.save()
            sub_task_list["team_id"].append(SubTaskCreateSerializer(sub_task).data['team']['team_id'])
            sub_task_list["name"].append(SubTaskCreateSerializer(sub_task).data['team']['name'])

        data = TaskCreateSerializer(task).data
        data['sub_task'] = sub_task_list
        res = custom_response(status=status.HTTP_201_CREATED, data=data)
        return Response(res, status=status.HTTP_200_OK)


class TaskView(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        """
        Task 상세 조회

        :params:
        - pk: Task ID
        """
        task = get_object_or_404(Task, pk=pk)
        data = TaskDetailSerializer(task).data

        data['sub_task'] = [SubTaskDetailSerializer(s).data for s in
                            SubTask.objects.filter(task=task, is_delete=False).all()]
        res = custom_response(data=data, status=200)
        return Response(res, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Task 수정

        :params:
        - pk: Task ID

        :args:
        - title: Task 이름
        - content: Task 설명
        - team_list: 하위 업무로 지정할 팀 ID 리스트
        """
        try:
            task = get_object_or_404(Task, pk=pk)
            # 작성자 확인
            self.check_object_permissions(self.request, task)

            # # 작성자 확인 2
            # if request.user.user_id != task.create_user.user_id:
            #     return Response({'message': 'Task 작성자만 수정할 수 있습니다.'},
            #                     status=status.HTTP_401_UNAUTHORIZED)

            title = request.data.get('title')
            content = request.data.get('content')
            team_list = request.data.get('team_list')  # 새롭게 하위 업무를 담당할 팀 ID 리스트 (기존 팀 ID 리스트가 넘어올 수 있음)
            # 완료 여부
            is_complete = request.data.get('is_complete')
            # 필요한 데이터 검증
            if not (title and content and team_list):  # todo: 검사 로직 확인하기
                res = custom_response(status=400)
                return Response(res, status=status.HTTP_200_OK)
        except KeyError:
            res = custom_response(status=400)
            return Response(res, status=status.HTTP_200_OK)

        if is_complete:
            completed_date = datetime.now()
            task.completed_date = completed_date

        serializer = TaskDetailSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()

        # * 완료 되었다면 삭제 불가
        # 기존 sub_task_list를 가져온다.
        # 변경할 team_list를 가져온다.
        # 기존과 변경할 list를 비교한다.

        sub_task_list = SubTask.objects.filter(task=task, is_delete=False).all()

        sub_task_dict = {obj.team.pk: obj for obj in sub_task_list}
        for team_id in team_list:
            # team_id 가 존재한다면
            if team_id in sub_task_dict:
                sub_task_dict.pop(team_id)
                continue
            else:
                SubTask.objects.create(
                    team=get_object_or_404(Team, pk=team_id),
                    task=task
                )

        for sub_task in sub_task_dict.values():
            if not sub_task.is_complete:
                sub_task.is_delete = True
                sub_task.save()

        data = TaskUpdateSerializer(task).data
        data['sub_task'] = [SubTaskDetailSerializer(s).data for s in
                            SubTask.objects.filter(task=task, is_delete=False).all()]
        res = custom_response(data=data, status=200)
        return Response(res, status=status.HTTP_200_OK)


class SubTaskView(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def put(self, request, pk):
        """
        SubTask 수정

        :params:
        - pk: SubTask ID
        """

        try:
            sub_task = get_object_or_404(SubTask, pk=pk)

            # 하위 업무 완료 처리는 소속된 팀만 가능
            if request.user.team.team_id != sub_task.team.team_id:
                res = custom_response(status=status.HTTP_401_UNAUTHORIZED, message='하위 업무는 소속된 팀만 수정 가능합니다.')
                return Response(res, status=status.HTTP_200_OK)

            # 완료 여부 & 필요한 데이터 검증
            is_complete = request.data['is_complete']

        except KeyError:
            res = custom_response(status=status.HTTP_400_BAD_REQUEST)
            return Response(res, status=status.HTTP_200_OK)

        # sub_task.is_complete = True
        # end_time = datetime.now()
        # sub_task.modified_at = end_time
        # sub_task.completed_date = end_time

        if is_complete:
            sub_task.is_complete = is_complete
            completed_date = datetime.now()
            sub_task.completed_date = completed_date
        else:
            sub_task.is_complete = is_complete
            sub_task.completed_date = None
        sub_task.save()

        task = Task.objects.get(pk=sub_task.task.task_id)
        all_complete = True  # 하위 task가 모두 완료되었는지 검사용 변수

        for s in SubTask.objects.filter(task=task, is_delete=False).all():
            if not s.is_complete:
                all_complete = False
                break

        if all_complete:
            task.is_complete = True
            task.completed_date = datetime.now()
            task.save()

        res = custom_response(data=SubTaskDetailSerializer(sub_task).data, status=status.HTTP_200_OK)
        return Response(res, status=status.HTTP_200_OK)
