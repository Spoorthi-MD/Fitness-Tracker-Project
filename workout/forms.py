from django.forms import ModelForm
from workout.models import Exercise_add



class Exercise_add_Form(ModelForm):
    class Meta:
        model = Exercise_add

        fields = ['Exercise', 'Reps', 'Sets', 'Description']





