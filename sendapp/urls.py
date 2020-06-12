from django.urls import path,include
from .views import *

urlpatterns = [
    path('', homeView, name="home"),

    path('set-user/', EmailFromListView, name="set-user"),
    
    path('default-email/<int:uid>/', defaultEmailView, name="default-email"),
    path('unset-default/<int:uid>/', unsetDefaultView, name="unset-default"),
    path('edit-email/<int:eid>/', editEmailFromView, name="edit-email"),
    path('delete-email/<int:did>/', deleteEmailFromView, name="delete-email"),

    path('create-email-draft/', createEmailDraftView, name="create-email-draft"),
    path('edit-email-draft/<int:eid>/', editEmailDraftView, name="edit-email-draft"),
    path('delete-email-draft/<int:eid>/', deleteEmailDraftView, name="delete-email-draft"),

    path('send-email/<int:eid>/', sendEmailView, name="send-email"),

    path('first-step/', firstStepView, name="first-step"),
    path('second-step/', secondStepView, name="second-step"),
    path('delete-email-list/', deleteEmailListView, name="delete-email-list"),
    path('save-email-list/', saveEmailListView, name="save-email-list"),
    path('edit-email-list/<int:did>/', editEmailListView, name="edit-email-list"),
    path('delete-list/<int:did>/', deleteListView, name="delete-list"),

    path('delete-email-list-item/<int:did>/<int:index>/', deleteEmailListItemView, name="delete-email-list-item"),
    path('add-to-currlist/<int:eid>', addToCurrlistView, name="add-to-currlist"),
    path('save-edited-email-list/<int:eid>', saveEditedEmailListView, name="save-edited-email-list"),
    path('delete-edited-email-list/<int:eid>', deleteEditedEmailListView, name="delete-edited-email-list"),
    path('edit-email-item/<int:eid>/<int:index>/', editEmailItemView, name="edit-email-item"),

    path('select-email-list/<int:sid>/', selectEmailListView, name="select-email-list"),
    path('unselect-email-list/', unselectEmailListView, name="unselect-email-list"),

    path('register/', registerView, name="register"),
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
]
