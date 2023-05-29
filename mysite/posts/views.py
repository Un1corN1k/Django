from django.shortcuts import render

posts = [
    {
        "id": 1,
        "author": "author 1",
        "description": "description 1"
    },
    {
        "id": 2,
        "author": "author 2",
        "description": "description 2"
    },
    {
        "id": 3,
        "author": "author 3",
        "description": "description 3"
    },
    {
        "id": 4,
        "author": "author 4",
        "description": "description 4"
    }
]


def all_posts(request):
    return render(request, "posts/posts.html", {"posts": posts})


def post_detail(request, post_id):
    for post in posts:
        if post["id"] == post_id:
            return render(request, "posts/post_detail.html", {"post":post})
    return render(request, "base.html")
