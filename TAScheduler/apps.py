from django.apps import AppConfig

class TASchedulerAppConfig(AppConfig):
    name = 'TAScheduler'
    verbose_name = 'TA Scheduler Application'

    def ready(self):
        # If we imported these models at the top of the file, we'd encounter an error, as they're part of a Django module that isn't loaded at application start.
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        
        # If they don't already exist, create the TA, Instructor, and Manager groups and assign them the proper permissions.
        
        taSchedulerGroups = {   # Key is the group name, value is an array of permission codenames.
            'ta': [],
            'instructor': [],
            'manager': [],
        }
        
        # For each group within the taSchedulerGroups array...
        for groupName, permissions in taSchedulerGroups.items():
            # If the group doeesn't already exist, create it.
            group, wasCreated = Group.objects.get_or_create(name=groupName)
            
            if wasCreated:  # Did we just create the group?
                for permissionCodename in permissions:  # For each permission codename associated with the group...
                    permission = Permission.objects.get(codename = permissionCodename)  # Get the permission from the database.
                    group.permissions.add(permission)   # Associate it with the group.
                
                print(f'Created \'{groupName}\' group.')
        pass
