from django.db import models
from employees.models import Employee


class Performance(models.Model):
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Below Average'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performances')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_date = models.DateField()
    goals_achieved = models.TextField(blank=True, null=True)
    areas_for_improvement = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_date', '-created_at']

    def __str__(self):
        return f"{self.employee.full_name} - {self.review_date} (Rating: {self.rating})"

    @property
    def rating_display(self):
        return dict(self.RATING_CHOICES)[self.rating]
