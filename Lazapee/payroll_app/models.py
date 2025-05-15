from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    rate = models.FloatField()
    overtime_pay = models.FloatField(max_length=20,null=True, blank=True)
    allowance = models.FloatField(null=True, blank=True)
    

    def getName(self):
        return self.name

    def getID(self):
        return self.id_number

    def getRate(self):
        return self.rate

    def getOvertime(self):
        return self.overtime_pay

    def resetOvertime(self):
        self.overtime_pay = 0
        self.save()

    def getAllowance(self):
        return self.allowance

    def __str__(self):
        return f"pk: {self.id_number}, rate: {self.rate}"
    


class Payslip(models.Model):
    id_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=100)
    date_range = models.CharField(max_length=250)
    year = models.CharField(max_length=100)
    pay_cycle = models.IntegerField(default=0)
    rate = models.FloatField()
    monthlyRate = models.FloatField()
    earnings_allowance = models.FloatField(null=True, blank=True)
    deductions_tax = models.FloatField(null=True, blank=True)
    deductions_health = models.FloatField(null=True, blank=True)
    pag_ibig = models.FloatField(null=True, blank=True)
    overtime = models.FloatField(max_length=20,  null=True, blank=True)
    total_pay = models.FloatField()
    sss = models.FloatField(null=True, blank=True)
    gross_pay = models.FloatField()
    
    def getIDNumber(self):
        return self.id_number
    def getMonth(self):
        return self.month
    def getRate(self):
        return self.rate
    def getDate_range(self):
        return self.date_range
    def getYear(self):
        return self.year
    def getPayCycle(self):
        return self.pay_cycle
    def getEarnings_Allowance(self):
        return self.earnings_allowance
    def getOvertime(self):
        return self.overtime
    def getTotal_pay(self):
        return self.total_pay
    def getS(self):
        return self.sss
    def getGross_Pay(self):
        return self.gross_pay
    def getDeductions_tax(self):
        return self.deductions_tax
    def getDeductions_health(self):
        return self.deductions_health
    
    

    def __str__(self):
        return f"pk: {self.id_number}, Period: {self.month} {self.year}, Cycle: {self.pay_cycle}, Total Pay:{self.total_pay}"
        