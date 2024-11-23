import datetime
import calendar
import os
import stripe

from datetime import timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from allauth.account.views import EmailVerificationSentView
from . import forms
from . import models
from . import mixins

# Create your views here.
class UserDetailView(generic.DetailView):
    model = models.CustomUser
    template_name = 'user/user_detail.html'

class UserUpdateView(generic.UpdateView):
    model = models.CustomUser
    template_name = 'user/user_update.html'
    form_class = forms.UserUpdateForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('user_detail', kwargs={'pk': pk})
    def form_valid(self, form):
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)

# class UserEmailVerificationSentView(EmailVerificationSentView):
#     template_name = 'admin/verification_sent.html'
    
class SubscribeRegisterView(View):
    template = 'subscribe/subscribe_register.html'
    
    def get(self, request):
        context = {}
        return render(self.request, self.template, context)

    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        correct_cord_number = '4242424242424242'
        if card_number != correct_cord_number:
            context = {'error_message': 'クレジットカード番号が正しくありません'}

            return render(self.request, self.template, context)

        models.CustomUser.objects.filter(id=user_id).update(is_subscribed=True,card_name=card_name,card_number=card_number)

        return redirect(reverse_lazy('top_page'))

class SubscribeStripeRegisterView(View):
    template = 'subscribe/subscribe_stripe_payment.html'
    
    def get(self, request):
        context = {}
        return render(self.request, self.template, context)

class SubscribeCancelView(generic.TemplateView):
    template_name = 'subscribe/subscribe_cancel.html'

    def post(self, request):
        user_id = request.user.id
        
        models.CustomUser.objects.filter(id=user_id).update(is_subscribed=False)
        return redirect(reverse_lazy('top_page'))

   

class SubscribePaymentView(View):
    template = 'subscribe/subscribe_payment.html'

    def get(self, request):
        user_id = request.user.id
        user = models.CustomUser.objects.get(id=user_id)
        context = {'user': user}

        return render(self.request, self.template, context)


    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        print(card_name, card_number)

        models.CustomUser.objects.filter(id=user_id).update(card_name=card_name,card_number=card_number)

        return redirect(reverse_lazy('top_page'))


class UserListView(mixins.OnlyStuffUserMixin, generic.ListView):
    """ ユーザー一覧表示画面 ================================== """
    model = models.CustomUser
    template_name = 'admin/user_list.html'
    paginate_by = 20

    def get_queryset(self):
        
        keyword = self.request.GET.get('keyword')
        button_type = self.request.GET.get('button_type')
        print(f'button_type {button_type}')
        keyword = keyword if keyword is not None else ''
        if button_type == 'keyword':
            self.request.session['keyword_session'] = keyword
        
        keyword_session = self.request.session.get('keyword_session')
        if keyword_session is not None:
            queryset = models.CustomUser.objects.filter(Q(user_name_kanji__icontains=keyword_session) | Q(user_name_kana__icontains=keyword_session) | Q(username__contains=keyword_session)).order_by('id')
        else:
            queryset = models.CustomUser.objects.all().order_by('id')
                
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        
        return context

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    domain = "127.0.0.1:8000"
    subject_template_name = 'admin/mail/subject.txt'
    email_template_name = 'admin/mail/message.txt'
    template_name = 'admin/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'admin/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'admin/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'admin/password_reset_complete.html'
    

class SalesListView(generic.ListView):
    """ レストラン詳細画面 ================================== """
    template_name = "admin/sales_detail.html"
    model = models.CustomUser
    # paginate_by = 12
    
    # def get_queryset(self):
    #     query_set = self.get_context_data()
        
    #     return query_set
    
    def get_context_data(self, **kwargs):
        # サブスクの月額単価
        PRICE = 300
        context = super(SalesListView, self).get_context_data(**kwargs)
        
        date_list = []
        sales_list = []
        # ユーザー登録を5年前からにしたので売り上げ計算も5年前からとする。
        st_date = datetime.datetime(2024,10,12,23,59,59,tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))) - datetime.timedelta(days=365*5)
        last_day = calendar.monthrange(st_date.year,st_date.month)[1]
        tmp_date = datetime.datetime(st_date.year, st_date.month, last_day,23,59,59,tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
        # 今月までの売り上げを計算
        today = datetime.datetime.today()
        today = datetime.datetime(today.year, today.month, today.day, 23, 59, 59, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
        while tmp_date < today:
            # 月末の日付を作る
            last_day = calendar.monthrange(tmp_date.year, tmp_date.month)[1]
            tmp_date = datetime.datetime(tmp_date.year, tmp_date.month, last_day, 23, 59, 59, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
            # 更新日の時点で有料会員になったと仮定して計算
            user_num = models.CustomUser.objects.filter(is_subscribed=True, updated_day__lte=tmp_date ).count()
            print(f'{tmp_date.strftime("%Y-%m-%d")}, {user_num}')
            tmp_date = tmp_date + relativedelta(months=1)
            
            date_list.append(tmp_date.strftime("%Y-%m-%d"))
            sales_list.append(user_num * PRICE )
        
        monthly_sales_list = zip(date_list, sales_list)
        
        context.update({
            'monthly_sales_list': monthly_sales_list,
        })
    
        return context
    
class MonthlySalesListView(generic.ListView):
    """ 月次売上一覧表示画面 ================================== """
    model = models.MonthlySales
    template_name = 'admin/sales_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset =models.MonthlySales.objects.all().order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MonthlySalesListView, self).get_context_data(**kwargs)
        
        return context

# payment/views.py

# class PaymentIndexView(generic.TemplateView):
#    template_name = "payment/index.html"

class SubscribeStripeRegisterView(View):
    template = 'subscribe/subscribe_stripe_payment.html'
    
    def get(self, request):
        context = {}
        return render(self.request, self.template, context)
    
# class PaymentCheckoutView(generic.TemplateView):
#    template_name = "payment/checkout.html"

class SubscribeStripeSuccessView(generic.View):
    template_name = "subscribe/subscribe_stripe_success.html"
#    ここに書く
    def get(self, request):
        # Stripe支払いが成功した時に有料会員フラグをTrueにする。
        user = request.user
        
        user.is_subscribed = True
        user.save()
        return render(request, "subscribe/subscribe_stripe_success.html", None)

class SubscribeStripeCancelView(generic.TemplateView):
   template_name = "subscribe/subscribe_stripe_cancel.html"

def create_checkout_session(request):
    pass

def create_checkout_session(request):
    stripe.api_key = os.environ["STRIPE_API_SECRET_KEY"]  
    print(request.user.id)
            
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': 'price_1QMPsEGrZpvyk0KLg8kZS5sB',
                    'quantity': 1,
                }
            ],
            success_url=request.build_absolute_uri(reverse('subscribe_stripe_success')),
            cancel_url=request.build_absolute_uri(reverse('subscribe_stripe_cancel')),
        
            )
         
        # checkout_session = stripe.checkout.Session.create(
        #     line_items=[
        #         {
        #             'price_data': {
        #                 'currency': 'jpy',
        #                 'unit_amount': 300,
        #                 'product_data': {
        #                     'name': 'NAGOYAMESHI 有料会員月額利用料',
        #                     #    'images': ['https://nagoyameshi-ichimura2.s3.amazonaws.com/static/images/logo/logo.png'],
        #                     #    'images': ['http://127.0.0.1:8000/images/logo/logo.png'],
        #                 },
        #             },
        #             'quantity': 1,
        #         },
        #     ],
        #     mode='payment',
        #     success_url=request.build_absolute_uri(reverse('subscribe_stripe_success')),
        #     cancel_url=request.build_absolute_uri(reverse('subscribe_stripe_cancel')),
        #     )

        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error':str(e)})
   
# class VerificationSentView(View):
#     """確認メールを送信しました。ページ"""
#     template_name = 'admin/verification_sent.html'

#     def get(self, request):
#         context = {}
#         return render(self.request, self.template, context)