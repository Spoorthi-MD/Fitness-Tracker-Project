from django.urls import path
from workout.views import home, login, signup, add_exercise, signout, delete_exercise, change_exercise
from workout import views

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('add-exercise/', add_exercise),
    path('delete-exercise/<int:id>', delete_exercise),
    path('change-status/<int:id>/<str:status>', change_exercise),
    path('logout/', signout),
    # path('admin-index/', signout),

#==============================================================================

    path('extend-admin-index/', views.extend_index, name='extend-admin-index'),
    path('admin-index', views.index, name='admin-index'),
    path('add', views.ADD, name='add'),
    path('edit', views.Edit, name='edit'),
    path('update/<str:id>', views.Update, name='update'),
    path('delete/<str:id>', views.Delete, name='delete'),
    path('email', views.email, name='email'),

]




















