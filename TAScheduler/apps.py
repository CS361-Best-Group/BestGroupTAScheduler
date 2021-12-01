from django.apps import AppConfig

class TASchedulerAppConfig(AppConfig):
    name = 'TAScheduler'
    verbose_name = 'TA Scheduler Application'

    def ready(self):
        # If we imported these models at the top of the file, we'd encounter an error, as they're part of a Django module that isn't loaded at application start.
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        
        print("don't awoo $350 penalty")
        
        # If they don't already exist, create the TA, Instructor, and Manager groups and assign them the proper permissions.
        pass
