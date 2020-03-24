from django.db import models

class Professor(models.Model):
    pid = models.CharField(primary_key=True, unique=True, max_length=32)
    pname = models.CharField(max_length=32)

    def __str__(self):
        return self.pname

    class Meta:
        db_table = 'Professors'

class Module(models.Model):
    mcode = models.CharField(primary_key=True, unique=True, max_length=32)
    mname = models.CharField(max_length=32)

    def __str__(self):
        return self.mname

    class Meta:
        db_table = 'Modules'

class Instance(models.Model):
    module = models.ForeignKey('Module', to_field='mcode', on_delete=models.CASCADE)
    year = models.IntegerField(default=2020)
    semester = models.IntegerField(default=1)
    professor = models.ManyToManyField('Professor')

    def __str__(self):
        return str(self.module.mname) + ' ' + str(self.year) + ' ' + str(self.semester)

    class Meta:
        db_table = "Module Instances"
        unique_together = ('module', 'year', 'semester')

class Rate(models.Model):
    module = models.ForeignKey('Module', to_field='mcode', on_delete=models.CASCADE)
    year = models.IntegerField(default=2020)
    semester = models.IntegerField(default=1)
    professor = models.ForeignKey('Professor', to_field='pid', on_delete=models.CASCADE)
    rate = models.IntegerField(default=5)

    def __str__(self):
        return str(self.module.mcode) + ' ' + str(self.professor.pid) + ' ' + str(self.rate)

    class Meta:
        db_table = "Rates"
