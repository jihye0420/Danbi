from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


# class IsOwner(BasePermission):
#     """
#     has_permission : 로그인 한 유저는 모두 접근 가능
#
#     has_object_permission(오브젝트 접근 권한)
#     - 관리자는 모든 접근 가능
#     - 작성자가 본인일 경우 접근 가능
#     """
#
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#
#         if user.is_authenticated:
#             if user.is_admin:
#                 return True
#             elif obj.__class__ == get_user_model():
#                 return obj.id == user.id
#             elif hasattr(obj, "user"):
#                 return obj.user.id == user.id
#             elif hasattr(obj, "account_book"):
#                 return obj.account_book.user.id == user.id
#             return False
#         return False
#
#     def has_permission(self, request, view):
#         user = request.user
#
#         if user.is_authenticated:
#             return True
#         return False


class IsOwner(BasePermission):
    """
    권한
    Task 조회: 로그인 한 사용자
    Task 생성: 로그인 한 사용자
    Task 수정 및 삭제: 글 작성자
    """

    def has_permission(self, request, view):
        """
        전체 객체에 대한 권한
        로그인 한 유저는 모두 접근 가능
        """
        user = request.user

        if user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        작성자가 본인일 경우 접근 가능
        """
        user = request.user

        if user.is_authenticated:
            if user.is_admin:
                return True
            elif request.method in SAFE_METHODS:
                return True
            elif obj.__class__ == get_user_model():
                return obj.id == user.user_id
            elif hasattr(obj, "create_user"):
                return obj.create_user.user_id == user.user_id
            # elif hasattr(obj, "team"):
            #     return obj.team.team_id == user.team.team_id
            return False
        else:
            return False
