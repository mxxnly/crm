from authentication.models import CustomUser
from task_system.models import TaskModel
def update_count_of_tasks(user):
    task_count = TaskModel.objects.filter(for_who__id=user.id).distinct().count()

    user.profile.count_of_tasks = task_count
    user.profile.save() 


def update_count_of_completed_tasks(user):
    task_completed_count = TaskModel.objects.filter(for_who__id=user.id, is_completed=True).distinct().count()
    
    user.profile.count_of_done_tasks = task_completed_count
    user.profile.save()
