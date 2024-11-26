from django.db import models
from tasks.models import Project


class WorkLevel(models.Model):
    project = models.ForeignKey('tasks.Project', on_delete=models.CASCADE)
    level_number = models.IntegerField()

    def __str__(self):
        return f'Work Level {self.level_number}'

class WorkPackage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='workpackages')

    def __str__(self):
        return self.name

class Work(models.Model):
    task = models.ForeignKey('prices.Task', on_delete=models.CASCADE)
    work_package = models.ForeignKey(WorkPackage, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=30, decimal_places=3)

    @property
    def work_amount(self):
        return round(self.task.price * self.quantity, 2)
    

class Measurement(models.Model):
    work = models.ForeignKey('Work', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    nr = models.IntegerField()
    width = models.DecimalField(max_digits=10, decimal_places=3)
    length = models.DecimalField(max_digits=10, decimal_places=3)
    height = models.DecimalField(max_digits=10, decimal_places=3)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Measurement for {self.work.task.name} ({self.nr} x {self.width} x {self.length} x {self.height})"
    
    @property
    def partial(self):
        return round(self.nr * self.width * self.length * self.height, 3)
    

class WorkpackageTotals(models.Model):
    workpackage = models.ForeignKey('Workpackage', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self):
        return f"Total for Workpackage {self.workpackage.name}: {self.total}"