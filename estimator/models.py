from django.db import models

# 1. Project MUST come first
class Project(models.Model):
    name = models.CharField(max_length=255)
    pitch = models.FloatField(default=0)
    waste_percentage = models.FloatField(default=10.0)
    dump_fee = models.FloatField(default=500.0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def calculate_totals(self):
        # This lets Claude just say 'project.calculate_totals' to get all the answers
        flat_area = sum(m.length * m.width for m in self.measurements.all())
        multiplier = math.sqrt(1 + (self.pitch / 12)**2)
        net_sqft = flat_area * multiplier
        net_squares = net_sqft / 100
        order_squares = math.ceil(net_squares * (1 + (self.waste_percentage / 100)))
        
        return {
            'net_squares': round(net_squares, 2),
            'order_squares': order_squares,
            'total_sqft': round(net_sqft, 2)
        }

# 2. MeasurementRow comes second because it "points" to Project
class MeasurementRow(models.Model):
    project = models.ForeignKey(Project, related_name='measurements', on_delete=models.CASCADE)
    length = models.FloatField()
    width = models.FloatField()
    description = models.CharField(max_length=100, blank=True)

