from django.urls import path
from . import views

urlpatterns = [
    #   LOGIN AND REGISTRATION
    path('', views.index),
    path('new_user', views.new_user),
    path('login', views.login),
    path('logout', views.logout),

    #   HOME PAGE
    path('home', views.homepage),

    #   TO-DO LIST
    path('toDo_list', views.toDo_list),
#   NEED TO KEEP CHECKBOXES CHECKED ON TO-DO LIST PAGE

    #   MESSAGE BOARD
    path('messages', views.message_board),
    path('new_post', views.new_post),
    path('delete/<int:message_id>', views.delete_message),
    path('new_comment', views.new_comment),

    #   MYACCOUNT
    path('myaccount_documents', views.uploads),
    path('myaccount_editprofile', views.editprofile),
    path('update_profile/<int:user_id>', views.update_profile),
    path('new_pcsinfo', views.add_pcs),
    path('update_pcs/<int:user_id>', views.update_pcs),



]