from datetime import date
from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from django.db.models import Avg
from django.http import JsonResponse

from . import models
from . import forms


""" トップ画面 ====================================="""

class TopPageView(generic.ListView):
    template_name = "top_page.html"
    model = models.Restaurant
    
    guery_set = models.Restaurant.objects.order_by('-rate')
    context_object_name = 'retaurant_list'
    
    def get_context_data(self, **kwargs):
        if 'price_session' in self.request.session:
            self.request.session['price_session'] = 0
        
        if 'keyword_session' in self.request.session:
            self.request.session['keyword_session'] = ''
        
        if 'category_session' in self.request.session:
            self.request.session['category_session'] = ''
        
        if 'select_sort' in self.request.session:
            self.request.session['select_sort'] = '-created_at'
        
        context = super(TopPageView, self).get_context_data(**kwargs)
        category_list = models.Category.objects.all()
        new_restaurant_list = models.Restaurant.objects.all().order_by('-created_at')
        restaurant_list = models.Restaurant.objects.all()
        
        # querysetに含まれるレストランの平均レートを、レストランごとに取得して配列に格納
        average_rate_list = []
        average_rate_star_list = []
        rate_num_list = []
        
        # for restaurant in context['restaurant_list']:
        for restaurant in restaurant_list:
            average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
            average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
            average_rate_list.append(round(average_rate, 2))
            rate_num = models.Review.objects.filter(restaurant=restaurant).count()
            rate_num_list.append(rate_num)
            
            if average_rate % 1 == 0:
                average_rate = int(average_rate)
            else:
                average_rate = round(average_rate * 2) / 2
        
            average_rate_star_list.append(average_rate)

            # print('⭐️⭐️⭐️')
            # print(restaurant.name)
            # print(average_rate_list)
            # print('🤩🤩🤩🤩🤩🤩🤩')
            # print(average_rate_star_list)
            # print(self.queryset)
        tmp_restaurat_list = zip(restaurant_list, average_rate_list, average_rate_star_list, rate_num_list)
        tmp_list = (list(tmp_restaurat_list))
        tmp_list = sorted(tmp_list, reverse=True, key=lambda x:(x[1], x[3]))
        
        # print(tmp_list)
        
        context.update({
            'category_list': category_list,
            'new_restaurant_list': new_restaurant_list,
            # 'restaurant_list': zip(self.queryset, average_rate_list, average_rate_star_list),
            # 'restaurant_list': zip(restaurant_list, average_rate_list, average_rate_star_list),
            'restaurant_list': tmp_list,
        })
        return context
    
""" 会社概要 ====================================="""

class CompanyView(generic.TemplateView):
    template_name = "layout/company.html"
    
""" 利用規約 ====================================="""

class TermsView(generic.TemplateView):
    template_name = "layout/terms.html"
    
# class RestaurantDetailView(generic.DetailView):

#     """ レストラン詳細画面 ====================================="""
#     template_name = "restaurant/restaurant_detail.html"
#     model = models.Restaurant
    

class RestaurantListView(generic.ListView):
    """ レストラン一覧画面 ================================== """
    template_name = "restaurant_list.html"
    model = models.Restaurant
    def get_context_data(self, **kwargs):
        context = super(RestaurantListView, self).get_context_data(**kwargs)
        # get input value
        keyword = self.request.GET.get('keyword')
        category = self.request.GET.get('category')
        price = self.request.GET.get('price')
        select_sort = self.request.GET.get('select_sort')
        button_type = self.request.GET.get('button_type')
        keyword = keyword if keyword is not None else ''
        category = category if category is not None else ''
        price = price if price is not None else '0'
        select_sort = select_sort if select_sort is not None else '-created_at'
        
        # session control
        self.request.session['select_sort'] = select_sort
        
        if button_type == 'keyword':
            self.request.session['keyword_session'] = keyword
            self.request.session['category_session'] = ''
            self.request.session['price_session'] = '0'
        if button_type == 'category':
            self.request.session['category_session'] = category
            self.request.session['keyword_session'] = ''
            self.request.session['price_session'] = '0'
        if button_type == 'price':
            self.request.session['price_session'] = price
            self.request.session['keyword_session'] = ''
            self.request.session['category_session'] = ''
        if button_type == 'select_sort':
            self.request.session['select_sort'] = select_sort
        
        keyword_session = self.request.session.get('keyword_session')
        category_session = self.request.session.get('category_session')
        price_session = self.request.session.get('price_session')
        select_sort_session = self.request.session.get('select_sort')
        
        # filtering queryset
        restaurant_list = models.Restaurant.objects.filter(Q(name__icontains=keyword_session) | Q(address__icontains=keyword_session) | Q(category__name__icontains=keyword_session))
        restaurant_list = restaurant_list.filter(category__name__icontains=category_session)
        
        if int(price_session) > 0:
            # restaurant_data = models.Restaurant.objects.values('id', 'price')
            restaurant_data = models.Restaurant.objects.values('id', 'price_max', 'price_min')
            target_id_list = []
            for data in restaurant_data:
                
                # price_str = data['price']
                # price_str = price_str.replace('円', '')
                # price_str = price_str.replace(',', '')
                # price_list = price_str.split('～')
                # if int(price_list[0]) <= int(price_session) <= int(price_list[1]):
                
                # if data['price_min'] is None:
                #     data['price_min'] = 0
                # if data['price_max'] is None:
                #     data['price_max'] = 10000
                if data['price_min'] <= int(price_session) <= data['price_max']:
                    target_id_list.append(data['id'])
            restaurant_list = restaurant_list.filter(id__in=target_id_list)
        # 表示順
        if select_sort_session != '-reservation_num':
            restaurant_list = restaurant_list.order_by(select_sort_session)
        else:
            reservation_restaurant_list = models.Reservation.objects.filter(~Q(status='予約取消')).values("restaurant")#.annotate(count=sum(restaurant)) #.order_by('count')
            for reservation in reservation_restaurant_list:
                # print('⭐️⭐️')
                # print(reservation.restaurant.name)
                # print(f'{reservation["restaurant"]}')
                reservation_num = len(models.Reservation.objects.filter(restaurant=reservation["restaurant"]))        
                print('⭐️⭐️')
                print(reservation_num)
                
                # for restaurant_obj in reservation_num:
                #     print('⭐️⭐️')
                #     print(restaurant_obj.restaurant.name)
                    
        
        category_list = models.Category.objects.all()
        
        # querysetに含まれるレストランの平均レートを、レストランごとに取得して配列に格納
        average_rate_list = []
        average_rate_star_list = []
        rate_num_list = []
        
        for restaurant in restaurant_list:
            average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
            average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
            
            average_rate_list.append(round(average_rate, 2))
            
            if average_rate % 1 == 0:
                average_rate = int(average_rate)
            else:
                average_rate = round(average_rate * 2) / 2
            average_rate_star_list.append(average_rate)
            rate_num = models.Review.objects.filter(restaurant=restaurant).count()
            rate_num_list.append(rate_num)
        
        tmp_restaurat_list = zip(restaurant_list, average_rate_list, average_rate_star_list, rate_num_list)
        tmp_list = (list(tmp_restaurat_list))
        if select_sort_session == '-rate':   
            tmp_list = sorted(tmp_list, reverse=True, key=lambda x:(x[1], x[3]))
        
        context.update({
            'category_list': category_list,
            'keyword_session': keyword_session,
            'category_session': category_session,
            'price_session': price_session,
            'select_sort_session': select_sort_session,
            # 'restaurant_list': zip(restaurant_list, average_rate_list, average_rate_star_list, rate_num_list),
            'restaurant_list': tmp_list,
        })
        
        return context
    

class RestaurantDetailView(generic.DetailView):
    """ レストラン詳細画面 ================================== """
    template_name = "restaurant/restaurant_detail.html"
    model = models.Restaurant

    def get_context_data(self, **kwargs):
        user = self.request.user
        pk = self.kwargs['pk']
        context = super(RestaurantDetailView, self).get_context_data(**kwargs)
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        is_favorite = False
        if user.is_authenticated:
            is_favorite = models.FavoriteRestaurant.objects.filter(user=user).filter(restaurant=models.Restaurant.objects.get(pk=pk)).exists()
        
        average_rate =models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)
        
        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
        rate_count =models.Review.objects.filter(restaurant=restaurant).count()
        
        context.update({
            'is_favorite': is_favorite,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
        })
        
        return context

    def post(self, request, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect(reverse_lazy('account_login'))

        if not user.is_subscribed:
            return redirect(reverse_lazy('subscribe_register'))
        
        pk = kwargs['pk']
        is_favorite = models.FavoriteRestaurant.objects.filter(user=user).filter(
        restaurant=models.Restaurant.objects.get(pk=pk)).exists()
        if is_favorite:
            models.FavoriteRestaurant.objects.filter(user=user).filter(restaurant=models.Restaurant.objects.get(pk=pk)).delete()
            is_favorite = False
        else:
            favorite = models.FavoriteRestaurant()
            user = request.user
            favorite.restaurant = models.Restaurant.objects.get(pk=pk)
            favorite.user = user
            favorite.save()
            is_favorite = True
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)

        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
 
        rate_count = models.Review.objects.filter(restaurant=restaurant).count()
        context = {
            'object': models.Restaurant.objects.get(pk=kwargs['pk']),
            'is_favorite': is_favorite,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
        }
        return render(request, self.template_name, context)
    
class FavoriteListView(generic.ListView):
    """ お気に入り一覧画面 ================================== """
    model = models.FavoriteRestaurant
    template_name = 'favorite/favorite_list.html'
    
    def get_queryset(self):
        user_id = self.request.user.id
        # queryset = models.FavoriteRestaurant.objects.filter(user_id=user_id).order_by('-created_at')
        queryset = models.FavoriteRestaurant.objects.filter(user_id=user_id)#.order_by('-created_at')
        
        return queryset
    
def favorite_delete(request):
    pk = request.GET.get('pk')
    is_success = True
    if pk:
        try:
            models.FavoriteRestaurant.objects.filter(id=pk).delete()
        except:
            is_success = False
    else:
        is_success = False

    return JsonResponse({'is_success': is_success})


class ReservationCreateView(generic.CreateView):
    """ 新規予約登録画面 ================================== """
    template_name = "reservation/reservation_create.html"
    model = models.Reservation
    form_class = forms.ReservationCreateForm
    success_url = reverse_lazy('top_page')

    def get(self, request, **kwargs):
        user = request.user
        
        if user.is_authenticated and user.is_subscribed:
            return super().get(request, **kwargs)
        
        if not user.is_authenticated:
            return redirect(reverse_lazy('account_login'))
        
        if not user.is_subscribed:
            return redirect(reverse_lazy('subscribe_register'))

    def form_valid(self, form):
        user_instance = self.request.user
        restaurant_instance = models.Restaurant(id=self.kwargs['pk'])
        reservation = form.save(commit=False)
        reservation.user = user_instance
        reservation.restaurant = restaurant_instance
        reservation.status = '予約受付'
        reservation.save()
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        average_rate =models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)
        
        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
        
        rate_count = models.Review.objects.filter(restaurant=restaurant).count()
        close_day_list = self.make_close_list(restaurant.close_day_of_week)
        
        context.update({
            'restaurant': restaurant,
            'close_day_list': close_day_list,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
        })
        return context


    def make_close_list(self, close_day):
        close_list = []
        if '月曜日' in close_day:
            close_list.append(1)
        if '火曜日' in close_day:
            close_list.append(2)
        if '水曜日' in close_day:
            close_list.append(3)
        if '木曜日' in close_day:
            close_list.append(4)
        if '金曜日' in close_day:
            close_list.append(5)
        if '土曜日' in close_day:
            close_list.append(6)
        if '日曜日' in close_day:
            close_list.append(0)
        
        return close_list
    
class ReservationListView(generic.ListView):
    """ 予約一覧表示画面 ================================== """
    model = models.Reservation
    template_name = 'reservation/reservation_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset =models.Reservation.objects.filter(user_id=self.request.user.id).order_by('-reservation_date')
        print('🤩🤩🤩🤩')
        for rest in queryset:
            print(f'restaurant:{rest.restaurant.name} reservation:{rest.reservation_date}')
            print(type(rest.reservation_date))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ReservationListView, self).get_context_data(**kwargs)
        context.update({'today': datetime.today().astimezone(),})
        print('⭐️⭐️⭐️⭐️')
        print(datetime.today().astimezone())
        print(type(datetime.today().astimezone()))
        
        return context
    
def reservation_delete(request):
    """ 予約の削除 ================================== """
    pk = request.GET.get('pk')
    is_success = True
    if pk:
        try:
            models.Reservation.objects.filter(id=pk).delete()
        except:
            is_success = False
    else:
        is_success = False
    
    return JsonResponse({'is_success': is_success})


class ReviewListView(generic.ListView):
    """ レビューの一覧表示 ================================== """
    template_name = "review/review_list.html"
    model = models.Review
    restaurant_id = None
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        restaurant_id = self.kwargs['pk']
        queryset = super(ReviewListView, self).get_queryset().order_by('-rate')

        return queryset.filter(restaurant=restaurant_id)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ReviewListView, self).get_context_data(**kwargs)
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        is_posted = models.Review.objects.filter(user=self.request.user).filter(restaurant=restaurant).exists()
        average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)
        
        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
        rate_count = models.Review.objects.filter(restaurant=restaurant).count()
        
        context.update({
            'restaurant': restaurant,
            'is_posted': is_posted,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count
        })
        return context
    
class ReviewCreateView(generic.CreateView):
    template_name = "review/review_create.html"
    model = models.Review
    form_class = forms.ReviewCreateForm
    success_url = None

    def get(self, request, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_subscribed:
            return super().get(request, **kwargs)

        if not user.is_authenticated:
            return redirect(reverse_lazy('account_login'))

        if not user.is_subscribed:
            return redirect(reverse_lazy('subscribe_register'))

    def form_valid(self, form):
        user_instance = self.request.user
        restaurant_instance = models.Restaurant(id=self.kwargs['pk'])
        review = form.save(commit=False)
        review.restaurant = restaurant_instance
        review.user = user_instance
        review.save()
        self.success_url = reverse_lazy('review_list', kwargs={'pk':
        self.kwargs['pk']})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        self.success_url = reverse_lazy('review_create', kwargs={'pk':self.kwargs['pk']})
        
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        restaurant = models.Restaurant.objects.filter(id=pk).first()
        average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)

        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
        rate_count = models.Review.objects.filter(restaurant=restaurant).count()
        
        context.update({
            'restaurant': restaurant,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
        })
        
        return context
    

class ReviewUpdateView(generic.UpdateView):
    """ レビューの更新 ================================== """
    model = models.Review
    template_name = 'review/review_update.html'
    form_class = forms.ReviewCreateForm
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = models.Review.objects.filter(id=pk).first().restaurant.id
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ReviewUpdateView, self).get_context_data(**kwargs)
        restaurant_id = models.Review.objects.filter(id=pk).first().restaurant.id
        restaurant = models.Restaurant.objects.filter(id=restaurant_id).first()
        average_rate = models.Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))
        average_rate = average_rate['rate__avg'] if average_rate['rate__avg'] is not None else 0
        average_rate = round(average_rate, 2)

        if average_rate % 1 == 0:
            average_rate_star = int(average_rate)
        else:
            average_rate_star = round(average_rate * 2) / 2
        
        rate_count = models.Review.objects.filter(restaurant=restaurant).count()
        
        context.update({
            'restaurant': restaurant,
            'average_rate': average_rate,
            'average_rate_star': average_rate_star,
            'rate_count': rate_count,
            })
        return context
    
def review_delete(request):
    """ レビューの削除 ================================== """
    pk = request.GET.get('pk')
    is_success = True
    
    if pk:
        try:
            models.Review.objects.filter(id=pk).delete()
        except:
            is_success = False
    else:
        is_success = False
    
    return JsonResponse({'is_success': is_success})