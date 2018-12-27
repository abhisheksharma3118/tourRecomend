from django.shortcuts import get_object_or_404, render
from .models import Review, Tour
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Review, Tour,Cluster
from django.contrib.auth.models import User
from .forms import ReviewForm
from .suggestions import update_clusters
import datetime
from django.contrib.auth.decorators import login_required



def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def tour_list(request):
    tour_list = Tour.objects.order_by('-name')
    context = {'tour_list':tour_list}
    return render(request, 'reviews/tour_list.html', context)


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    form = ReviewForm()
    return render(request, 'reviews/tour_detail.html', {'tour': tour, 'form': form})

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.tour = tour
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:tour_detail', args=(tour.id,)))

    return render(request, 'reviews/tour_detail.html', {'tour': tour, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):

    # get request user reviewed wines
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('tour')
    user_reviews_tour_ids = set(map(lambda x: x.tour.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding wines reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(tour__id__in=user_reviews_tour_ids)
    other_users_reviews_tour_ids = set(map(lambda x: x.tour.id, other_users_reviews))

    # then get a wine list including the previous IDs, order by rating
    tour_list = sorted(
        list(Tour.objects.filter(id__in=other_users_reviews_tour_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    return render(
        request,
        'reviews/user_recommendation_list.html',
        {'username': request.user.username,'tour_list': tour_list}
)
