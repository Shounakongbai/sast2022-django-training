from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponseNotAllowed,
)
from lb.models import Submission, User
from django.forms.models import model_to_dict
from django.db.models import F
import json
from lb import utils
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_http_methods as method

def hello(req: HttpRequest):
    return JsonResponse({
        "code": 0,
        "msg": "hello"
    })

# TODO: Add HTTP method check
@method(["GET"])
def leaderboard(req: HttpRequest):
    return JsonResponse(
        utils.get_leaderboard(),
        safe=False,
    )


@method(["GET"])
def history(req: HttpRequest, username: str):
    # TODO: Complete `/history/<slug:username>` API
    return JsonResponse(
        utils.get_history(username),
        safe=False
    )


@method(["POST"])
@csrf_exempt
def submit(req: HttpRequest):
    # TODO: Complete `/submit` API
    info = json.loads(req.body.decode('utf8'))
    try:
        username = info["user"]
        try:
            avatar = info["avatar"]
        except Exception:
            avatar = None
        content = info["content"]
        if len(username) > 255:
            return JsonResponse(
                {
                    "code": -1,
                    "msg": "用户名太长了"
                }
            )
        if avatar != None:
            if len(avatar) > 100*1024:
                return JsonResponse(
                    {
                        "code": -2,
                        "msg": "图像太大了"
                    }
                )
        try:
            meaningless, subs = utils.judge(content)
            subs = f"{subs[0]} {subs[1]} {subs[2]}"
        except Exception:
            return JsonResponse(
                {
                    "code": -3,
                    "msg": "你这结果保熟吗"
                }
            )
        try:
            user = User.objects.get(username=username)
        except Exception:
            user = User.objects.create(username=username)
        Submission.objects.create(user=user, avatar=avatar, score=meaningless, subs=subs)
        return JsonResponse(
            {
                "code": 0,
                "msg": "提交成功",
                "data": {
                    "leaderboard": utils.get_leaderboard()
                }
            }
        )
    except Exception:
        return JsonResponse(
            {
                "code": 1,
                "msg": "你这参数保熟吗"
            }
        )


@method(["POST"])
@csrf_exempt
def vote(req: HttpRequest):
    if 'User-Agent' not in req.headers \
            or 'requests' in req.headers['User-Agent']:
        return JsonResponse({
            "code": -1
        })

    # TODO: Complete `/vote` API
    info = json.loads(req.body)
    try:
        user = User.objects.get(username=info["user"])
    except Exception:
        return JsonResponse({
            "code": -1
        })
    user.votes = user.votes + 1
    user.save()
    return JsonResponse({
        "code": 0,
        "data": {
            "leaderboard": utils.get_leaderboard()
        }
    })
